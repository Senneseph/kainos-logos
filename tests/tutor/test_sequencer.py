"""The sequencer + spaced re-exposure queue (T4 layer 4): pure recompute,
prereq-gated, deterministic, and honestly empty when nothing is derivable.
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor import sequencer
from kainos.tutor.brainstem import Brainstem
from kainos.tutor.mastery import Concept, reset_concepts
from kainos.tutor.sequencer import (
    REEXPOSE_INTERVAL,
    due_concepts,
    next_drill,
    strip_candidates,
)

CONCEPTS = (
    Concept("count-successor", "Successor on the number line", "pre-k", "arithmetic"),
    Concept("add-within-10", "Addition with sum within the number line", "k-5", "arithmetic", prereqs=("count-successor",)),
)
IDS = [c.id for c in CONCEPTS]
K = 4  # STABLE_EVIDENCE_K


@pytest.fixture(autouse=True)
def _clean_registry():
    reset_concepts()
    yield
    reset_concepts()


def _store_with_successor_facts(n: int) -> InMemoryCodexStore:
    """A fresh runtime session whose teacher taught succ(0..n-1)."""

    codex = InMemoryCodexStore()
    b = Brainstem(codex, concepts=CONCEPTS)
    b._set_session(1)
    for m in range(n):
        b.turn(f"after {m} comes {m + 1}")
    return codex


def _store_with_stable_successor() -> InMemoryCodexStore:
    codex = _store_with_successor_facts(6)
    b = Brainstem(codex, concepts=CONCEPTS)
    b._set_session(1)
    for n in range(K):  # four correct derivations -> stable
        b.turn(f"what comes after {n}?")
    return codex


def test_nothing_due_in_a_fresh_store():
    codex = InMemoryCodexStore()
    Brainstem(codex, concepts=CONCEPTS)  # seeds the curriculum only
    assert due_concepts(codex, IDS, 1) == []
    assert next_drill(codex, IDS, 1) is None


def test_addition_blocked_until_prereq_stable():
    codex = _store_with_successor_facts(6)  # taught but NOT drilled -> exposed
    due = due_concepts(codex, IDS, 1)
    assert [d["concept"] for d in due] == ["count-successor"]  # only the exposed one; addition not ready
    assert next_drill(codex, IDS, 1)["concept"] == "count-successor"


def test_practicing_beats_exposed_beats_unexposed():
    codex = _store_with_stable_successor()  # count-successor stable
    b = Brainstem(codex, concepts=CONCEPTS)
    b._set_session(2)
    b.turn("2 + 3 is what?")  # addition: exposed+derived -> practicing
    b.turn("4 + 2 is what?")
    b.turn("0 + 5 is what?")
    due = due_concepts(codex, IDS, 2)
    # addition is practicing (highest value); count-successor is stable with last derivation S01
    assert due[0]["concept"] == "add-within-10"
    assert next_drill(codex, IDS, 2)["concept"] == "add-within-10"
    d = next_drill(codex, IDS, 2)
    assert d["surface"].endswith("is what?") and d["slots"]["mode"] == "add"


def test_stable_spacing_interval():
    codex = _store_with_stable_successor()  # last derivation in S1
    # S2, S3: within the interval -> not due
    assert due_concepts(codex, IDS, 2) == []
    assert due_concepts(codex, IDS, 1 + REEXPOSE_INTERVAL - 1) == []
    # S1 + interval: due for the spaced retest
    due = due_concepts(codex, IDS, 1 + REEXPOSE_INTERVAL)
    assert [d["concept"] for d in due] == ["count-successor"]
    assert "stable spacing" in due[0]["reason"]
    d = next_drill(codex, IDS, 1 + REEXPOSE_INTERVAL)
    assert d is not None and d["concept"] == "count-successor"
    assert d["slots"]["mode"] == "succ" and d["slots"]["n"] <= 5  # grounded in what was taught


def test_proposals_are_grounded_and_deterministic():
    codex = _store_with_successor_facts(4)
    cands = strip_candidates("count-successor", codex)
    assert {c["slots"]["n"] for c in cands} == {0, 1, 2, 3}  # exactly the taught facts
    for s in (2, 2, 2, 3):
        d1 = next_drill(codex, IDS, s)
        d2 = next_drill(codex, IDS, s)
        assert d1 == d2  # pure recompute
    d = next_drill(codex, IDS, 2)
    assert d is not None and d["slots"]["n"] in (0, 1, 2, 3)


def test_pure_recompute_is_stable_across_calls():
    codex = _store_with_stable_successor()
    a = due_concepts(codex, IDS, 1 + REEXPOSE_INTERVAL)
    b = due_concepts(codex, IDS, 1 + REEXPOSE_INTERVAL)
    assert a == b
    assert sequencer.strip_candidates("add-within-10", codex)
    # the addition strip is non-empty once the prereq has facts
    add = {c["surface"] for c in sequencer.strip_candidates("add-within-10", codex)}
    assert "2 + 3 is what?" in add
