"""Session runtime (T3): boot / restore / lapse over the persistent CODEX.

An infant session is a fresh WORKSPACE (lifetime SESSION) over the
persistent, provenance-mandatory CODEX. `lapse` dumps the session
workspace and logs the forgetting (a lapse is a LOGGED event, never a
silent data loss; nothing un-promoted ever enters the CODEX); `boot`
restores the CODEX from the previous lapse and starts an EMPTY workspace
(no session-context leak across lifetimes — C5's "restored, empty"
clause). Learning lives in the CODEX, so it must survive the restart;
that is the difference between retained knowledge and session context.

Determinism (e5.x discipline): no wall clock (fixed epochs from
(session, turn); see brainstem.fixed_epoch) and no randomness — every
persisted file is `json.dumps(..., sort_keys=True)` and byte-identical
across re-execution (C7 compares run1 vs run2 at the byte level).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion
from kainos.tutor.brainstem import Brainstem
from kainos.tutor.mastery import Concept, mastery_view
from kainos.workspace.workspace import Lifetime, WorkSpace

if TYPE_CHECKING:  # pragma: no cover
    from kainos.lang.llm import Backend
    from kainos.tutor.brainstem import TurnResult

__all__ = ["InfantRuntime", "SessionReport", "deterministic_bytes"]


def deterministic_bytes(d: Any) -> str:
    """The one serialization the persistence layer uses (byte-stable)."""

    return json.dumps(d, sort_keys=True, separators=(",", ":")) + "\n"


def _file_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def codex_dump_path(persist: Path, session: int) -> Path:
    return persist / f"codeX-S{session:02d}.json"


def session_report_path(persist: Path, session: int) -> Path:
    return persist / f"session-S{session:02d}.json"


def dump_store(codex: InMemoryCodexStore, session: int) -> dict:
    """The byte-stable CODEX dump after session N (all assertions, id-sorted)."""

    return {
        "session": session,
        "assertions": [a.to_dict() for a in sorted(codex.query(), key=lambda a: a.id)],
    }


def load_store(path: Path) -> InMemoryCodexStore:
    d = json.loads(path.read_text())
    codex = InMemoryCodexStore()
    for row in d["assertions"]:
        codex.add(Assertion.from_dict(row))
    return codex


@dataclass
class SessionReport:
    """One session's machine-readable report — the input of the analysis
    arm (T5) and of this phase's offline checks. Deterministic dict form."""

    session: int
    restored: bool
    workspace_empty_at_boot: bool
    turns: list[dict[str, Any]]
    mastery: dict[str, dict[str, Any]]  # session-final recompute, per concept
    attention: list[dict[str, Any]]
    codex: dict[str, Any]  # {"total": n, "added_this_session": [...]}
    workspace: dict[str, Any]  # {"entries": n, "dump_hash": sha256}
    arm: dict[str, Any]  # {"llm_events": n, "fallback_events": n}

    def to_dict(self) -> dict[str, Any]:
        return {
            "session": self.session,
            "restored": self.restored,
            "workspace_empty_at_boot": self.workspace_empty_at_boot,
            "turns": [dict(t) for t in self.turns],
            "mastery": {k: dict(v) for k, v in sorted(self.mastery.items())},
            "attention": [dict(a) for a in self.attention],
            "codex": dict(self.codex),
            "workspace": dict(self.workspace),
            "arm": dict(self.arm),
        }


class InfantRuntime:
    """The attended pilot's driver (the un-attended regime (T5) replaces
    the scripted teacher with the LLM authoring arm through the same
    `turn` seam — nothing else changes)."""

    # E6.2 — the curriculum ladder (concept-wall pre-registration). The two
    # pilot strips stay; the five ladder concepts activate via their
    # rule/definition facts in the store (capability is store data).
    PILOT_CONCEPTS: tuple[Concept, ...] = (
        Concept("count-successor", "Successor on the number line", "pre-k", "arithmetic"),
        Concept("add-within-10", "Addition with sum within the number line", "k-5", "arithmetic", prereqs=("count-successor",)),
        Concept("add-two-digit", "Addition with two-digit sums (the extended line)", "k-5", "arithmetic", prereqs=("count-successor",)),
        Concept("sub-within-30", "Subtraction by walking the line backward", "k-5", "arithmetic", prereqs=("count-successor",)),
        Concept("mult-within-100", "Multiplication by repeated addition", "k-5", "arithmetic", prereqs=("count-successor", "add-two-digit")),
        Concept("compare-numbers", "Comparison by walking the line", "k-5", "arithmetic", prereqs=("count-successor",)),
        # sqrt-bracket is DEFERRED with its rung (owner 2026-08-21, D-e6f)
        # to the future lattice-wall experiment; the dormant machinery in
        # the brainstem stays unregistered here.
    )

    def __init__(self, persist_dir: str | Path, backend: Backend | None = None, concepts: tuple | list | None = None) -> None:
        self._persist = Path(persist_dir)
        self._backend = backend
        self._concepts = tuple(concepts) if concepts is not None else self.PILOT_CONCEPTS
        self._codex: InMemoryCodexStore | None = None
        self._ws: WorkSpace | None = None
        self._brainstem: Brainstem | None = None
        self._session: int | None = None
        self._lapsed_session: int = 0
        self._turns: list[TurnResult] = []
        self._added: list[str] = []
        self._attention: list[dict[str, Any]] = []
        self._restored = False
        self._ws_empty_at_boot = False

    # ── lifecycle ───────────────────────────────────────────────────────

    def boot(self, session: int) -> None:
        """Start session N: restore the CODEX from lapse N-1 (if any),
        start an EMPTY session WORKSPACE, seed the curriculum (idempotent)."""

        if self._session is not None:
            raise RuntimeError("lapse the current session before booting a new one")
        if session <= self._lapsed_session:
            raise ValueError(f"session {session} cannot boot: {self._lapsed_session} already lapsed (no replaying history)")
        self._persist.mkdir(parents=True, exist_ok=True)
        prev = codex_dump_path(self._persist, session - 1) if session >= 2 else None
        if session >= 2 and (prev is None or not prev.exists()):
            raise FileNotFoundError(f"missing CODEX dump for session {session} ({prev}); sessions are strictly sequential")
        self._codex = load_store(prev) if (prev is not None and prev.exists()) else InMemoryCodexStore()
        self._restored = prev is not None and prev.exists()
        self._ws = WorkSpace(id=f"session-S{session:02d}", label=f"tutor session {session}", lifetime=Lifetime.SESSION)
        self._ws_empty_at_boot = len(self._ws.irs) == 0
        self._brainstem = Brainstem(self._codex, backend=self._backend, concepts=self._concepts)
        self._brainstem._set_session(session)
        self._session = session
        self._turns = []
        self._added = []
        self._attention = []

    def turn(self, surface_text: str) -> TurnResult:
        if self._brainstem is None or self._session is None or self._ws is None:
            raise RuntimeError("boot a session before turning")
        ws = self._ws
        r = self._brainstem.turn(surface_text)
        self._turns.append(r)
        ws.add_ir(r.to_dict(), role=f"turn:{r.turn.split(':')[1]}")
        for aid in r.memory_diff:
            if aid not in self._added:
                self._added.append(aid)
        for eid in r.events:
            if eid not in self._added:
                self._added.append(eid)
        if r.attention is not None:
            self._attention.append(dict(r.attention))
        return r

    def lapse(self) -> SessionReport:
        """End the session: dump the CODEX (post-state) + the session
        report (with the workspace dump hashed in). Forgetting is logged
        here — and nothing un-promoted ever enters the CODEX, so the dump
        gains nothing silent."""

        if self._brainstem is None or self._session is None:
            raise RuntimeError("nothing to lapse")
        assert self._codex is not None and self._ws is not None
        session = self._session
        ws_dump = self._ws.dump()
        report = SessionReport(
            session=session,
            restored=self._restored,
            workspace_empty_at_boot=self._ws_empty_at_boot,
            turns=[t.to_dict() for t in self._turns],
            mastery={cid: v.to_dict() for cid, v in sorted(mastery_view(self._codex, [c.id for c in self._concepts]).items())},
            attention=[dict(a) for a in self._attention],
            codex={"total": len(self._codex.query()), "added_this_session": list(self._added)},
            workspace={"entries": len(self._ws.irs), "dump_hash": _file_hash(json.dumps(ws_dump, sort_keys=True))},
            arm={"llm_events": self._brainstem.llm_events, "fallback_events": self._brainstem.fallback_events},
        )
        codex_text = deterministic_bytes(dump_store(self._codex, session))
        codex_dump_path(self._persist, session).write_text(codex_text)
        session_report_path(self._persist, session).write_text(deterministic_bytes(report.to_dict()))
        self._lapsed_session = session
        self._session = None
        self._codex = None
        self._ws = None
        self._brainstem = None
        return report

    # ── convenience for the bench / checks ──────────────────────────────

    @property
    def session_number(self) -> int | None:
        return self._session

    def final_store(self) -> InMemoryCodexStore | None:
        """The live store while a session is open (checks re-audit it)."""

        return self._codex
