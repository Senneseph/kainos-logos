"""The brainstem (T2): the 7-contract dispatch, grounded derivation,
verified memory writes, and the single-current-claimant invariant (D-e6c).

Every assertion here runs on a fresh in-memory CODEX (no persistence, no
wall clock); determinism is proven at the E6.1 level (byte-identity).
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.lang.llm import MockBackend
from kainos.projection.contract import CONTRACTS, validate_response
from kainos.tutor.brainstem import Brainstem, det_classify
from kainos.tutor.mastery import Concept, reset_concepts

CONCEPTS = (
    Concept("count-successor", "Successor on the number line", "pre-k", "arithmetic"),
    Concept("add-within-10", "Addition with sum within the number line", "k-5", "arithmetic", prereqs=("count-successor",)),
)


@pytest.fixture(autouse=True)
def _clean_registry():
    reset_concepts()
    yield
    reset_concepts()


@pytest.fixture()
def brainstem() -> Brainstem:
    b = Brainstem(InMemoryCodexStore(), concepts=CONCEPTS)
    b._set_session(1)
    return b


# ── the frozen grammar: all seven kinds + the ambiguous floor ───────────────


@pytest.mark.parametrize(
    ("text", "kind", "slots"),
    [
        ("after 2 comes 3", "assertion", {"a": 2, "b": 3}),
        ("no — that was a mistake; after 2 comes 3", "correction", {"a": 2, "b": 3}),
        ("i misspoke; after 3 comes 4", "correction", {"a": 3, "b": 4}),
        ("what comes after 7?", "question", {"mode": "succ", "n": 7}),
        ("2 + 3 is what?", "question", {"mode": "add", "a": 2, "b": 3}),
        ("3 * 4 is what?", "question", {"mode": "mult", "a": 3, "b": 4}),  # E6.2: a drill (the gap is policy-level, below)
        ("count from 2 to 5", "request", {"a": 2, "b": 5}),
        ("count to 4", "command", {"n": 4}),
        ("blue", "ambiguous", {}),
    ],
)
def test_det_classify_grammar(text, kind, slots):
    assert det_classify(text) == (kind, slots)


def test_all_seven_contract_kinds_are_frozen():
    assert set(CONTRACTS) == {"request", "question", "command", "assertion", "correction", "impossible", "ambiguous"}


# ── lessons, corroboration, and the single-claimant invariant ────────────────


def test_lesson_establishes_with_provenance(brainstem):
    r = brainstem.turn("after 2 comes 3")
    assert r.kind == "assertion" and r.contract_valid
    a = brainstem._codex.get(r.memory_diff[0])
    assert a.status is EpistemicState.established
    assert a.provenance.observer == "teacher"
    assert a.provenance.evidence == ["turn:S01:01"]


def test_reteaching_corroborates_not_duplicates(brainstem):
    r1 = brainstem.turn("after 2 comes 3")
    r2 = brainstem.turn("after 2 comes 3")
    assert r2.memory_diff == [r1.memory_diff[0]]  # SAME claimant, not a second one
    assert r2.text if False else r2.response_text.endswith("just as i have it.")
    fact = brainstem._codex.get(r1.memory_diff[0])
    assert "turn:S01:02" in fact.provenance.evidence  # corroboration appended
    # invariant: exactly one live claimant for the value
    live = [
        x
        for x in brainstem._codex.query(subject="count-successor:succ-of(2)", relation="succ")
        if x.status is EpistemicState.established
    ]
    assert [x.id for x in live] == [r1.memory_diff[0]]


# ── conflict: both sides disputed, kept, linked — never averaged ────────────


def test_conflict_disputes_both_and_flags_honestly(brainstem):
    brainstem.turn("after 2 comes 3")
    r = brainstem.turn("after 2 comes 5")
    assert r.kind == "assertion" and r.contract_valid
    assert r.conflict is not None
    old = brainstem._codex.get("cs-fS0101:2->3")
    new = brainstem._codex.get(r.conflict["new"])
    assert old.status is EpistemicState.disputed
    assert new.status is EpistemicState.disputed
    assert new.id in old.provenance.evidence and old.id in new.provenance.evidence
    assert "disputed" in r.response_text


def test_first_conflict_is_silent_second_fires_attention(brainstem):
    brainstem.turn("after 2 comes 3")
    r1 = brainstem.turn("after 2 comes 5")  # conflict episode 1
    brainstem.turn("no — that was a mistake; after 2 comes 3")  # reconciled
    brainstem.turn("after 3 comes 4")
    b2 = Brainstem(brainstem._codex, concepts=CONCEPTS)
    b2._set_session(1)
    r2 = b2.turn("after 3 comes 9")  # conflict episode 2 (same codex history)
    assert r1.attention is None
    assert r2.attention is not None and r2.attention["type"] == "repeated-conflict"


# ── correction: pair kept, closed, linked; the original is VINDICATED ───────


def test_correction_keeps_pair_and_vindicates_original(brainstem):
    brainstem.turn("after 2 comes 3")
    brainstem.turn("after 2 comes 5")  # conflict
    r = brainstem.turn("no — that was a mistake; after 2 comes 3")
    assert r.kind == "correction" and r.contract_valid
    ok, viol = validate_response(r.response_ir, "correction")
    assert ok and not viol
    assert r.response_ir["superseded"] == "after 2 comes 5"
    assert r.response_ir["replacement"] == "after 2 comes 3"
    sup = brainstem._codex.get("cs-fS0102:2->5")
    original = brainstem._codex.get("cs-fS0101:2->3")
    assert sup.status is EpistemicState.obsolete
    assert sup.validity is not None and sup.validity.to is not None
    assert original.status is EpistemicState.established  # vindicated, not replaced-by-new
    assert original.id in sup.provenance.evidence and sup.id in original.provenance.evidence
    open_disputes = [a for a in brainstem._codex.query() if a.status is EpistemicState.disputed]
    assert open_disputes == []


def test_correction_contract_rejects_identical_sides(brainstem):
    ok, viol = validate_response({"superseded": "x", "replacement": "x"}, "correction")
    assert not ok and viol


# ── grounded derivation + honest needs_info ───────────────────────────────────


def test_derivation_cites_the_chain(brainstem):
    for n in range(5):
        brainstem.turn(f"after {n} comes {n + 1}")
    r = brainstem.turn("2 + 3 is what?")
    assert r.kind == "question" and r.contract_valid
    assert r.response_ir["answer"] == "5"
    assert r.response_ir["uncertainty_state"] == "derived"
    assert len(r.grounded) == 3  # 2->3, 3->4, 4->5
    for cite in r.grounded:
        assert brainstem._codex.get(cite).status is EpistemicState.established


def test_honest_needs_info_with_absence_audit(brainstem):
    for n in range(3):
        brainstem.turn(f"after {n} comes {n + 1}")
    r = brainstem.turn("7 + 8 is what?")
    assert r.response_ir["uncertainty_state"] == "needs_info"
    assert str(r.response_ir["answer"]).startswith("needs_info")
    assert r.honest_gap is not None
    audits = r.response_ir["evidence"]
    assert audits and all(a.startswith("absence-audit:") for a in audits)
    # no fabricated fact entered the store
    assert brainstem._codex.query(subject="count-successor:succ-of(7)", relation="succ") == []


# ── the remaining contract kinds (request / command / impossible) ────────────


def test_request_counts_by_chained_facts(brainstem):
    for n in range(6):
        brainstem.turn(f"after {n} comes {n + 1}")
    r = brainstem.turn("count from 2 to 5")
    assert r.kind == "request" and r.contract_valid
    assert r.response_ir["result"] == [2, 3, 4, 5]
    assert len(r.response_ir["trace"]) == 3


def test_command_needs_info_when_incomplete(brainstem):
    brainstem.turn("after 0 comes 1")
    r = brainstem.turn("count to 4")
    assert r.kind == "command" and r.contract_valid
    assert str(r.response_ir["resulting_state"]).startswith("needs_info")


def test_unlearned_drill_names_the_gap_and_nearest_plan(brainstem):
    # E6.2: with no rule fact in the store, a multiplication drill is the
    # HONEST impossible (named gap + nearest plan = teach the rule first).
    brainstem.turn("after 0 comes 1")
    r = brainstem.turn("3 * 4 is what?")
    assert r.kind == "impossible" and r.contract_valid
    ok, viol = validate_response(r.response_ir, "impossible")
    assert ok and not viol
    assert "not yet learned: repeated addition (multiplication)" == r.response_ir["gap"]
    assert "teach it first" in r.response_ir["nearest_plan"][0]
    assert r.memory_diff == []  # nothing learned: capability not taught


def test_ambiguous_yields_clarifying_question_with_two_candidates(brainstem):
    r = brainstem.turn("blue")
    assert r.kind == "ambiguous" and r.contract_valid
    ok, viol = validate_response(r.response_ir, "ambiguous")
    assert ok and not viol
    assert 1 <= len(r.response_ir["candidates"]) <= 2
    assert r.memory_diff == [] and r.events == []  # ambiguous touches no concept


# ── the LLM seam: confirm-mode classification + phrasing (E3.1 SKIP) ────────


def test_llm_confirms_and_phrases_without_touching_content(brainstem):
    codex = InMemoryCodexStore()
    b_det = Brainstem(codex, concepts=CONCEPTS)
    b_det._set_session(1)
    for n in range(5):
        b_det.turn(f"after {n} comes {n + 1}")
    det_r = b_det.turn("2 + 3 is what?")
    mock = MockBackend(
        [
            '{"kind": "question", "slots": {"mode": "add", "a": 2, "b": 3}}',
            "Sure thing: the answer is 5.",
        ]
    )
    b3 = Brainstem(codex, backend=mock, concepts=CONCEPTS)
    b3._set_session(1)
    r = b3.turn("2 + 3 is what?")
    assert r.arm["classifier"] == "llm" and r.arm["phrasing"] == "llm"
    assert r.arm["content_from"] == "codeX"
    assert r.response_ir["answer"] == "5"
    assert len(r.response_ir["evidence"]) == 3
    assert r.response_text == "Sure thing: the answer is 5."
    assert r.response_ir == det_r.response_ir


def test_llm_disagreement_falls_back_to_grammar_recorded(brainstem):
    codex = InMemoryCodexStore()
    replies = [
        '{"kind": "impossible", "slots": {"a": 2, "b": 3, "op": "multiply"}}',  # disagrees with grammar
        "Whatever.",
    ]
    b = Brainstem(codex, backend=MockBackend(replies), concepts=CONCEPTS)
    b._set_session(1)
    r = b.turn("2 + 3 is what?")
    assert r.kind == "question"  # grammar stood
    assert r.arm["classifier"] == "det"
    assert r.arm["classifier_fallback"] is True
    assert b.fallback_events == 1


def test_llm_garbage_falls_back_without_error(brainstem):
    codex = InMemoryCodexStore()
    b = Brainstem(codex, backend=MockBackend(["sure thing", "that is 5."]), concepts=CONCEPTS)
    b._set_session(1)
    r = b.turn("what comes after?")  # ambiguous even to the grammar...
    assert r.kind == "ambiguous"
    assert r.arm["classifier_fallback"] is True
