"""Mastery & curriculum (T4) — P11: mastery is STORE DATA.

The concept graph (concepts + prerequisites + band + domain) is CODEX
terms + relations — curriculum changes are data edits with provenance,
not code changes. Mastery state per concept is a PURE FUNCTION of (the
concept graph, the mastery-event assertions, the dispute state): no
mutable "progress" object exists anywhere — "it learned X" must be
re-derivable from the store at all times (the spec's "the CODEX can
produce the evidence", generalized to the state machine).

State machine (frozen per plan/30-phases/phase-6-tutor/experiments.md):

    unexposed:  no mastery events for the concept
    exposed:    >=1 event, zero correct derivations
    practicing: >=1 correct derivation, and not stable
    stable:     >=K derivation-correct events AND every prerequisite
                concept is stable AND no unreconciled dispute touches
                the concept's fact set

K = 4 (the evidence bar for stable) — a frozen mechanism, not a tuned
parameter (spec: mastery transitions require experiment-grade
evidence, never self-report).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from kainos.codex.memory import InMemoryCodexStore

__all__ = [
    "BANDS",
    "STABLE_EVIDENCE_K",
    "Concept",
    "MasteryState",
    "MasteryView",
    "mastery_view",
]

#: The curriculum bands (frozen vocabulary; the spec's band ladder).
BANDS: tuple[str, ...] = ("pre-k", "k-5", "6-8", "9-12", "college-1")

#: Evidence bar for `stable` (frozen): >= K correct derivations.
STABLE_EVIDENCE_K = 4

# Store vocabulary (the concept graph is STORE DATA — terms/contexts, not code).
CONCEPT_KIND = "concept"
PREREQ_RELATION = "prereq"
MASTERY_EVENT_KIND = "mastery-event"
EVENT_RELATION = "has_event"


class MasteryState(str, Enum):
    UNEXPOSED = "unexposed"
    EXPOSED = "exposed"
    PRACTICING = "practicing"
    STABLE = "stable"


@dataclass(frozen=True)
class Concept:
    """One node of the curriculum graph, as store data would express it."""

    id: str
    label: str
    band: str
    domain: str
    prereqs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.band not in BANDS:
            raise ValueError(f"unknown band: {self.band!r} (bands: {', '.join(BANDS)})")


@dataclass(frozen=True)
class MasteryView:
    """The recomputed mastery row for one concept (a VALUE, never state)."""

    concept_id: str
    state: MasteryState
    events: int
    correct_derivations: int
    unresolved_conflicts: int
    prereq_gaps: tuple[str, ...]  # prereqs not yet stable

    def to_dict(self) -> dict[str, Any]:
        return {
            "concept": self.concept_id,
            "state": self.state.value,
            "events": self.events,
            "correct_derivations": self.correct_derivations,
            "unresolved_conflicts": self.unresolved_conflicts,
            "prereq_gaps": list(self.prereq_gaps),
        }


_CONCEPTS: dict[str, Concept] = {}


def _register(concept: Concept) -> None:
    _CONCEPTS[concept.id] = concept


def concept(id: str) -> Concept:
    if id not in _CONCEPTS:
        raise KeyError(f"unknown concept: {id!r}")
    return _CONCEPTS[id]


def registry() -> dict[str, Concept]:
    return dict(_CONCEPTS)


def seed_concepts(concepts: tuple[Concept, ...] | list[Concept]) -> None:
    """Register the pilot's curriculum (idempotent by id; the CODEX is
    the durable copy — this is the in-process twin of the store terms)."""

    for c in concepts:
        if c.id in _CONCEPTS and _CONCEPTS[c.id] != c:
            raise ValueError(f"conflicting re-registration for concept {c.id!r}")
        _register(c)


def reset_concepts() -> None:
    """Test seam: clear the in-process concept registry."""

    _CONCEPTS.clear()


def _events_for(codex: InMemoryCodexStore, concept_id: str) -> list[dict[str, Any]]:
    """The concept's mastery-event rows (context kind=mastery-event,
    concept=<id>), oldest-stable order (by assertion id — ids embed the
    (session, turn) order, so this is the timeline)."""

    out: list[dict[str, Any]] = []
    for a in codex.query(context_match={"kind": MASTERY_EVENT_KIND, "concept": concept_id}):
        data = dict(a.context.data)
        out.append(
            {
                "id": a.id,
                "object": a.object if isinstance(a.object, str) else a.object.id,
                "status": a.status.value,
                "detail": data,
            }
        )
    return sorted(out, key=lambda r: r["id"])


def _disputed_in_namespace(codex: InMemoryCodexStore, prefix: str) -> int:
    n = 0
    for a in codex.query():
        if not a.subject.id.startswith(f"{prefix}:"):
            continue
        if a.status.value == "disputed":
            n += 1
    return n


def _prereq_gaps(codex: InMemoryCodexStore, c: Concept, seen: set[str] | None = None) -> tuple[str, ...]:
    seen = set(seen or ())
    gaps: list[str] = []
    for pre in c.prereqs:
        if not _is_stable(codex, pre, seen | {c.id}):
            gaps.append(pre)
    return tuple(sorted(gaps))


def _is_stable(codex: InMemoryCodexStore, pre: str, seen: set[str]) -> bool:
    if pre in seen:
        raise ValueError(f"concept graph cycle at {pre!r}")
    return _state_of(codex, pre, seen | {pre}) == MasteryState.STABLE


def _state_of(codex: InMemoryCodexStore, concept_id: str, seen: set[str]) -> MasteryState:
    events = _events_for(codex, concept_id)
    correct = sum(1 for e in events if e["object"] == "derivation-correct")
    conflicts = _disputed_in_namespace(codex, concept_id)
    if not events:
        return MasteryState.UNEXPOSED
    if correct == 0:
        return MasteryState.EXPOSED
    c = concept(concept_id)
    gaps = _prereq_gaps(codex, c, seen)
    if correct >= STABLE_EVIDENCE_K and not gaps and conflicts == 0:
        return MasteryState.STABLE
    return MasteryState.PRACTICING


def mastery_view(codex: InMemoryCodexStore, concept_ids: list[str]) -> dict[str, MasteryView]:
    """The pure recompute: concept ids -> MasteryView (deterministic)."""

    out: dict[str, MasteryView] = {}
    for cid in concept_ids:
        events = _events_for(codex, cid)
        correct = sum(1 for e in events if e["object"] == "derivation-correct")
        conflicts = _disputed_in_namespace(codex, cid)
        gaps = _prereq_gaps(codex, concept(cid), set())
        state = _state_of(codex, cid, set())
        out[cid] = MasteryView(
            concept_id=cid,
            state=state,
            events=len(events),
            correct_derivations=correct,
            unresolved_conflicts=conflicts,
            prereq_gaps=gaps,
        )
    return out
