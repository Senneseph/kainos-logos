"""E3.7 runner — recursive workspace memory (X3, anti-corruption, P12).

Scripted per `phase-3-generalization/experiments.md` → E3.7:

- ``PROJECT_GAME`` (PROJECT) → child ``WORLD`` → grandchild ``TRANSPORT``;
  sibling child ``COMBAT``. A transport-decision IR lives in the grandchild;
  a combat-decision IR in the sibling.
- **Query check** (recursion ≥ 2): from the project root, ``query("transport")``
  returns the grandchild's decision — a graph query, no reprocessing.
- **Fork/revise**: fork ``PROJECT_GAME``; in the fork the transport decision is
  revised. The root still returns the original; the fork returns the revision.
- **Promote**: ``promote(fork, "transport_decision", codex)`` → candidate
  assertion with ``source = workspace_<fork_id>`` (verified against the store).
- **Negative control (mandatory, in the result file)**: the un-promoted combat
  IR yields ZERO CODEX assertions (P12: un-promoted content is invisible).
- **Source check**: a local file source with two append-only analyses (latest
  = v2, v1 immutable); a simulated hash change flags the ``derived_from``
  derivations stale.

Deterministic: fixed script, fixed source content, fixed analysis timestamps
(see D-m5 in results.md for why the demo pins the wall clock), no RNG. Exit 0
iff every check passes.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion
from kainos.harness.paths import default_results_dir
from kainos.workspace.promote import promote
from kainos.workspace.source import DERIVED_FROM, SourceRef, SourceRegistry, hash_file
from kainos.workspace.workspace import Lifetime, WorkSpace

__all__ = ["E3_7Experiment", "run_e3_7"]

#: Fixed analysis timestamps (D-m5 discipline: reproducible demo).
_T1 = "2026-08-21T09:00:00+00:00"
_T2 = "2026-08-21T09:30:00+00:00"

_TRANSPORT_DECISION: dict[str, Any] = {
    "kind": "state",
    "relationships": [{"subject": "game_plan", "relation": "decides_transport", "object": "convoy_route_a"}],
}
_TRANSPORT_REVISION: dict[str, Any] = {
    "kind": "state",
    "relationships": [{"subject": "game_plan", "relation": "decides_transport", "object": "convoy_route_b"}],
}
_COMBAT_DECISION: dict[str, Any] = {
    "kind": "state",
    "relationships": [{"subject": "game_plan", "relation": "decides_combat", "object": "ambush_at_ford"}],
}
_SOURCE_URI = "data/e3.7_game_notes.txt"
_SOURCE_TEXT = "Chapter 3 — transport: the convoy crosses at the ford at dawn.\n"


def _promoted_sources(promoted: list[Assertion]) -> list[str]:
    """Provenance source URIs (narrowing the optional wrapper for mypy)."""

    out: list[str] = []
    for a in promoted:
        prov = a.provenance
        assert prov is not None, "promoted assertions carry provenance"
        src = prov.source
        assert src is not None, "promoted assertions name a source"
        out.append(src.uri)
    return out


def _build_project_game() -> WorkSpace:
    world = WorkSpace(id="WORLD", label="world state", lifetime=Lifetime.SESSION)
    transport = WorkSpace(id="TRANSPORT", label="transport planning", lifetime=Lifetime.SESSION)
    transport.add_ir(_TRANSPORT_DECISION, "transport_decision")
    world.add_child(transport)

    combat = WorkSpace(id="COMBAT", label="combat planning", lifetime=Lifetime.SESSION)
    combat.add_ir(_COMBAT_DECISION, "combat_decision")

    root = WorkSpace(id="PROJECT_GAME", label="the game project", lifetime=Lifetime.PROJECT)
    root.add_child(world)
    root.add_child(combat)
    return root


def run_e3_7(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = Path(out_dir) if out_dir is not None else default_results_dir()  # results hygiene
    root = _build_project_game()
    checks: list[bool] = []
    notes: list[str] = []

    # ── 1. Query check: the grandchild's decision, from the project root ──
    q = root.query("transport")
    row = q[0] if q else None
    checks.append(row is not None and row["workspace"] == "TRANSPORT" and row["object"] == "convoy_route_a")
    checks.append(all(r["workspace"] != "PROJECT_GAME" for r in q))  # not a root-level echo
    recursion_depth = 2 if row is not None else 0
    notes.append(f"root.query('transport') → {len(q)} row(s), depth {recursion_depth}")

    # ── 2. Fork / revise ─────────────────────────────────────────────────
    fork = root.fork("PROJECT_GAME_fork")
    # revision: inside the fork, replace the transport decision
    fork_ws = fork.children["WORLD"].children["TRANSPORT"]
    fork_ws.add_ir(_TRANSPORT_REVISION, "transport_decision")

    root_q = root.query("transport")
    fork_q = fork.query("transport")
    root_latest = root_q[0]["object"] if root_q else None
    fork_latest = frozenset(r["object"] for r in fork_q if r["relation"] == "decides_transport")
    checks.append(root_latest == "convoy_route_a")          # root untouched
    checks.append(fork_latest == {"convoy_route_b"})        # fork carries the revision
    fork_isolation = fork.id == "PROJECT_GAME_fork" and fork.parent is None and root_latest == "convoy_route_a"

    # ── 3. Promote (explicit, candidate-only, provenance-carrying) ───────
    codex = InMemoryCodexStore()
    ids = promote(fork, "transport_decision", codex, observer="e3.7")
    promoted = [codex.get(aid) for aid in ids]
    via_query = codex.query(relation="decides_transport")
    uris = _promoted_sources(promoted)
    checks.append(len(ids) == 1 and len(via_query) == 1)
    checks.append(all(a.status.value == "candidate" for a in promoted))
    checks.append(all(u == "workspace_PROJECT_GAME_fork" for u in uris))
    checks.append(all(a.provenance is not None and a.provenance.derived for a in promoted))
    checks.append(all(a.object == "convoy_route_b" for a in via_query))  # the revision, not the original
    promotion = {
        "assertion_count": len(ids),
        "status": {a.id: a.status.value for a in promoted},
        "source": {a.id: u for a, u in zip(promoted, uris, strict=True)},
    }

    # ── 4. Negative control: un-promoted content is INVISIBLE ────────────
    combat_leak = codex.query(relation="decides_combat")
    original_leak = [a for a in codex.query(relation="decides_transport") if a.object == "convoy_route_a"]
    negative_control_passed = len(combat_leak) == 0 and len(original_leak) == 0
    notes.append(f"negative control: combat rows in codex = {len(combat_leak)}, original-route rows = {len(original_leak)}")

    # ── 5. Sources: versioned, append-only, stale-on-hash-change ─────────
    src_path = out_dir / ".sources" / "e3.7_game_notes.txt"
    src_path.parent.mkdir(parents=True, exist_ok=True)
    src_path.write_text(_SOURCE_TEXT)
    registry = SourceRegistry()
    registry.register(SourceRef(uri=_SOURCE_URI, hash=hash_file(src_path)))

    a1 = registry.add_analysis(
        _SOURCE_URI,
        {"kind": "state", "relationships": [{"subject": "analysis_v1", "relation": DERIVED_FROM, "object": _SOURCE_URI}]},
        created_at=_T1,
    )
    a1_snapshot = a1
    a2 = registry.add_analysis(
        _SOURCE_URI,
        {"kind": "state", "relationships": [
            {"subject": "analysis_v2", "relation": DERIVED_FROM, "object": _SOURCE_URI},
            {"subject": "analysis_v2", "relation": "concludes", "object": "ford_is_the_route"},
        ]},
        created_at=_T2,
    )
    v1_immutable = registry.analyses(_SOURCE_URI)[0] == a1_snapshot and len(registry.analyses(_SOURCE_URI)) == 2
    latest = registry.latest_analysis(_SOURCE_URI)
    stale_changed = registry.stale_derivations(_SOURCE_URI, "0" * 64)
    stale_same = registry.stale_derivations(_SOURCE_URI, registry.source(_SOURCE_URI).hash)
    source_versioning = {
        "analyses": len(registry.analyses(_SOURCE_URI)),
        "latest_version": latest.version,
        "v1_immutable_after_v2": v1_immutable,
        "stale_on_hash_change": stale_changed,
        "stale_on_same_hash": stale_same,
    }
    checks.append(latest.version == 2 and latest == a2 and v1_immutable)
    checks.append(stale_changed == [f"{_SOURCE_URI}:1", f"{_SOURCE_URI}:2"] and stale_same == [])

    query_accuracy = round(sum(checks[:4]) / 4, 6)
    passed = all(checks) and query_accuracy == 1.0 and fork_isolation and negative_control_passed

    report: dict[str, Any] = {
        "config": {
            "seed": None,  # no RNG — fully scripted
            "commit": os.environ.get("KAINOS_GIT_COMMIT", "unknown"),
            "script": "e3.7-project-game",
            "structure": "PROJECT_GAME → {WORLD → TRANSPORT, COMBAT}",
            "source_uri": _SOURCE_URI,
            "source_hash": registry.source(_SOURCE_URI).hash,
        },
        "query_accuracy": query_accuracy,
        "recursion_depth": recursion_depth,
        "fork_isolation": bool(fork_isolation),
        "promotion": promotion,
        "negative_control_passed": bool(negative_control_passed),
        "source_versioning": source_versioning,
        "checks": len(checks),
        "checks_passed": sum(checks),
        "notes": notes,
        "passed": bool(passed),
    }
    (out_dir / "phase-3").mkdir(parents=True, exist_ok=True)
    (out_dir / "phase-3" / "e3.7.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


class E3_7Experiment:
    """Phase-2-harness Experiment for the E3.7 workspace check (P12).

    ``value`` = 1.0 iff every scripted check passes — all four E3.7 checks
    (query, fork, promotion, sources) plus the mandatory anti-corruption
    negative control."""

    name = "e3.7"
    hypothesis = (
        "a WORKSPACE container holds, nests, forks, revises and QUERIES IRs — "
        "'what did we decide?' is a graph query (no reprocessing) — and "
        "promotion discipline holds: the CODEX gains only explicit, "
        "provenance-carrying candidates; un-promoted content is invisible"
    )
    metric = (
        "query accuracy on the transport decision (latest IR, post-revision); "
        "recursion depth exercised (>= 2); promote() output = candidate assertions "
        "with source=workspace_<id>; negative control: un-promoted content returns "
        "NO CODEX assertions"
    )
    threshold = (
        "all four checks pass; no un-promoted content visible in the CODEX "
        "(the anti-corruption invariant, P12)"
    )

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e3_7()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=1.0 if report["passed"] else 0.0,
            evidence=[Path("results/phase-3/e3.7.json")],
            config={
                "query_accuracy": report["query_accuracy"],
                "recursion_depth": report["recursion_depth"],
                "fork_isolation": report["fork_isolation"],
                "negative_control_passed": report["negative_control_passed"],
                "promotion": report["promotion"],
                "source_versioning": report["source_versioning"],
            },
        )
