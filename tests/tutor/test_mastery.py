"""Mastery & curriculum (T4): P11 — mastery is STORE DATA, a pure recompute.

Covers the state machine (unexposed/exposed/practicing/stable), the K
evidence bar, prerequisite gating, conflict blocking, and the purity of
the recompute (same store => same view, always).
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    Provenance,
    Source,
    TermRef,
)
from kainos.tutor import mastery
from kainos.tutor.mastery import (
    STABLE_EVIDENCE_K,
    Concept,
    MasteryState,
    reset_concepts,
)


@pytest.fixture(autouse=True)
def _clean_registry():
    reset_concepts()
    yield
    reset_concepts()


def _event(codex: InMemoryCodexStore, concept: str, kind: str, n: int) -> str:
    eid = f"{concept}:ev-test:{kind}:{n}"
    codex.add(
        Assertion(
            id=eid,
            subject=TermRef(kind="entity", id=concept),
            relation=TermRef(kind="concept", id="has_event"),
            object=TermRef(kind="term", id=kind),
            context=Context(data={"kind": "mastery-event", "concept": concept}),
            status=EpistemicState.established,
            provenance=Provenance(
                source=Source(uri=f"turn:test:{n}", media_type="text/plain"),
                observer="infant",
                verified=True,
                evidence=[f"turn:test:{n}"],
            ),
        )
    )
    return eid


@pytest.fixture()
def codex() -> InMemoryCodexStore:
    mastery.seed_concepts(
        [
            Concept("cs", "counting", "pre-k", "arithmetic"),
            Concept("add", "addition", "k-5", "arithmetic", prereqs=("cs",)),
        ]
    )
    return InMemoryCodexStore()


def test_unexposed_when_no_events(codex):
    view = mastery.mastery_view(codex, ["cs", "add"])["cs"]
    assert view.state is MasteryState.UNEXPOSED
    assert view.events == 0 and view.correct_derivations == 0


def test_exposed_when_events_but_no_correct(codex):
    _event(codex, "cs", "lesson", 1)
    _event(codex, "cs", "drill-unable", 2)
    view = mastery.mastery_view(codex, ["cs"])["cs"]
    assert view.state is MasteryState.EXPOSED
    assert view.events == 2 and view.correct_derivations == 0


def test_practicing_when_some_correct_below_k(codex):
    for n in range(STABLE_EVIDENCE_K - 1):
        _event(codex, "cs", "derivation-correct", n)
    view = mastery.mastery_view(codex, ["cs"])["cs"]
    assert view.state is MasteryState.PRACTICING


def test_stable_at_k_with_no_prereqs(codex):
    for n in range(STABLE_EVIDENCE_K):
        _event(codex, "cs", "derivation-correct", n)
    view = mastery.mastery_view(codex, ["cs"])["cs"]
    assert view.state is MasteryState.STABLE
    assert view.correct_derivations == STABLE_EVIDENCE_K


def test_prereq_gate_blocks_stable(codex):
    for n in range(STABLE_EVIDENCE_K):
        _event(codex, "cs", "derivation-correct", n)
        _event(codex, "add", "derivation-correct", n)
    # `cs` is stable, so `add` may be stable too
    view = mastery.mastery_view(codex, ["cs", "add"])
    assert view["add"].state is MasteryState.STABLE
    # now drop `cs` below K by... (pure recompute: fresh store with add only events)
    codex2 = InMemoryCodexStore()
    for n in range(STABLE_EVIDENCE_K):
        _event(codex2, "add", "derivation-correct", n)
    _event(codex2, "cs", "lesson", 1)  # cs: exposed only
    view2 = mastery.mastery_view(codex2, ["cs", "add"])
    assert view2["add"].state is MasteryState.PRACTICING
    assert view2["add"].prereq_gaps == ("cs",)


def test_unreconciled_conflict_blocks_stable(codex):
    for n in range(STABLE_EVIDENCE_K):
        _event(codex, "cs", "derivation-correct", n)
    assert mastery.mastery_view(codex, ["cs"])["cs"].state is MasteryState.STABLE
    # a disputed fact in the concept namespace
    codex.add(
        Assertion(
            id="cs:succ-of(7)=9",
            subject=TermRef(kind="term", id="cs:succ-of(7)"),
            relation=TermRef(kind="concept", id="succ"),
            object=TermRef(kind="term", id="cs:num(9)"),
            context=Context(data={"kind": "fact", "concept": "cs"}),
            status=EpistemicState.disputed,
            provenance=Provenance(
                source=Source(uri="turn:test:88", media_type="text/plain"), observer="teacher", verified=True, evidence=[]
            ),
        )
    )
    view = mastery.mastery_view(codex, ["cs"])["cs"]
    assert view.state is MasteryState.PRACTICING
    assert view.unresolved_conflicts == 1


def test_recompute_is_pure(codex):
    for n in range(STABLE_EVIDENCE_K):
        _event(codex, "cs", "derivation-correct", n)
    v1 = mastery.mastery_view(codex, ["cs", "add"])
    v2 = mastery.mastery_view(codex, ["cs", "add"])
    assert v1 == v2
    d1 = {k: v.to_dict() for k, v in v1.items()}
    d2 = {k: v.to_dict() for k, v in v2.items()}
    assert d1 == d2


def test_concept_registry_conflict_rejected():
    mastery.seed_concepts([Concept("cs", "counting", "pre-k", "arithmetic")])
    with pytest.raises(ValueError, match="conflicting re-registration"):
        mastery.seed_concepts([Concept("cs", "counting (different)", "pre-k", "arithmetic")])
    # equal re-registration is idempotent
    mastery.seed_concepts([Concept("cs", "counting", "pre-k", "arithmetic")])
    assert mastery.concept("cs").label == "counting"
