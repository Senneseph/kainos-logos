"""Store I/O and mechanism census for bandgen.

Read-only probes mirror the experiment helpers (e617's
``_store_identity`` / ``_line_end`` / ``_successor_objects``) so the
compiler's numbers are comparable 1:1 with the experiments' frozen
tables. The runtime drivers (``run_main`` / ``run_carry``) drive
``InfantRuntime`` exactly as the experiments' ``_run_once`` / P6 do:
boot(s), turn(text), lapse() — nothing more, nothing less.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from kainos.tutor.mastery import mastery_view, reset_concepts, seed_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

#: The successor-line probes (mirrors e617._line_end / _successor_objects).
_COUNT = "count-successor"


def store_identity(store: Any) -> str:
    """16-hex identity of a store's assertions: sha256 over the
    sorted (id, canonical-json) pairs (exactly the experiments' way)."""
    pairs = []
    for a in store.query():
        pairs.append((a.id, json.dumps(a.to_dict(), sort_keys=True, default=str)))
    pairs.sort()
    return hashlib.sha256(json.dumps(pairs, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


def line_end(store: Any) -> int:
    end = 0
    for a in store.query(context_match={"kind": "fact", "concept": _COUNT}):
        sid, oid = a.subject.id, a.object_id
        if (
            sid.startswith(f"{_COUNT}:succ-of(")
            and oid.startswith(f"{_COUNT}:num(")
            and (a.validity is None or a.validity.to is None)
        ):
            end = max(end, int(oid[len(f"{_COUNT}:num(") : -1]))
    return end


def successor_objects(store: Any) -> set[int]:
    out: set[int] = set()
    for a in store.query(context_match={"kind": "fact", "concept": _COUNT}):
        oid = a.object_id
        if (
            isinstance(oid, str)
            and oid.startswith(f"{_COUNT}:num(")
            and (a.validity is None or a.validity.to is None)
        ):
            out.add(int(oid[len(f"{_COUNT}:num(") : -1]))
    return out


def concept_registry(getattr_registry: Any) -> list[str]:
    """The ids of the booted registry (a brainstem concepts tuple)."""
    return [c.id for c in getattr_registry]


def _fresh_store(root: Path, s: int) -> Any:
    p = codex_dump_path(root, s)
    if p is None or not p.exists():
        raise FileNotFoundError(f"expected store dump missing: {p}")
    return load_store(p)


def place_seed(seed_path: Path, root: Path) -> None:
    """The house seeding pattern: the seed sits at codeX-S01.json and
    session 2 boots over it (session 1 is empty)."""
    if not seed_path.exists():
        raise FileNotFoundError(f"seed store missing: {seed_path}")
    root.mkdir(parents=True, exist_ok=True)
    (root / "codeX-S01.json").write_bytes(seed_path.read_bytes())


def run_main(root: Path, sessions: list[int], registry: tuple, script: dict[int, list[str]]) -> list[dict[str, Any]]:
    """The labeled run, exactly as the experiments' _run_once:
    reset_concepts, boot/turn/lapse per session. Returns the session
    dumps (the mechanism's own turn records)."""
    reset_concepts()
    rt = InfantRuntime(root, concepts=registry)
    out: list[dict[str, Any]] = []
    for s in sessions:
        rt.boot(s)
        for text in script[s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def run_carry(root: Path, registry: tuple, surfaces: list[str]) -> list[Any]:
    """The P6 pattern: a SEED-ONLY runtime (boot(2) over the seed)
    re-runs the carry + off-script surfaces; returns the per-surface
    turn records."""
    reset_concepts()
    rt = InfantRuntime(root, concepts=registry)
    rt.boot(2)
    out: list[Any] = []
    for text in surfaces:
        out.append(rt.turn(text))
    rt.lapse()
    return out


def pre_states(seed_path: Path, registry: tuple) -> dict[str, dict]:
    """The PRE-states: the mastery view of the seed store (every
    registry concept the seed already holds). Computed by the
    mechanism — this replaces the hand-built E616_FROZEN chain that
    produced the D-e6h(e) count-class deviations."""
    reset_concepts()
    seed_concepts(tuple(registry))
    store = load_store(seed_path)
    mv = mastery_view(store, concept_registry(registry))
    out: dict[str, dict] = {}
    for cid in concept_registry(registry):
        v = mv.get(cid)
        if v is None:
            continue
        out[cid] = {"state": v.state, "correct": v.correct_derivations}
    return out


def mastery_snapshot(store: Any, registry: tuple) -> dict[str, dict]:
    """The post-state mastery census of a final store."""
    mv = mastery_view(store, concept_registry(registry))
    out: dict[str, dict] = {}
    for cid in concept_registry(registry):
        v = mv.get(cid)
        if v is None:
            continue
        out[cid] = {
            "state": v.state,
            "correct": v.correct_derivations,
            "prereq_gaps": list(v.prereq_gaps),
        }
    return out


def fresh_final(root: Path, session: int) -> Any:
    return _fresh_store(root, session)
