"""E6.2 — the curriculum ladder to the edge of grasp (unit + full bench).

Unit tests: the rule-gated derivation policies (sub/mult/cmp/sqrt), the
data-driven activation (the A/B flip), the add-strip routing, and the
honest edges (walk-off, line-end, partial bracket). The last test runs
the full 131-turn bench in a tmp dir (replay + ladder, twice) and pins
the frozen checks.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.projection.contract import validate_response
from kainos.tutor.brainstem import Brainstem, det_classify
from kainos.tutor.e62 import CHECKS, LADDER_CONCEPTS, run_e6_2
from kainos.tutor.mastery import reset_concepts


@pytest.fixture(autouse=True)
def _clean_registry():
    reset_concepts()
    yield
    reset_concepts()


@pytest.fixture()
def brainstem() -> Brainstem:
    b = Brainstem(InMemoryCodexStore(), concepts=LADDER_CONCEPTS)
    b._set_session(1)
    return b


def _teach_line(b: Brainstem, n: int) -> None:
    for i in range(n):
        b.turn(f"after {i} comes {i + 1}")


# ── the extended frozen grammar ──────────────────────────────────────────────


@pytest.mark.parametrize(
    ("text", "kind", "slots"),
    [
        ("7 - 2 is what?", "question", {"mode": "sub", "a": 7, "b": 2}),
        ("6 * 7 is what?", "question", {"mode": "mult", "a": 6, "b": 7}),
        ("is 17 larger than 9?", "question", {"mode": "cmp", "a": 17, "b": 9}),
        ("the square root of 20 is what?", "question", {"mode": "sqrt", "n": 20}),
        ("subtraction is walking backward", "assertion", {"rule": "subtraction is walking backward"}),
        ("multiplication is repeated addition", "assertion", {"rule": "multiplication is repeated addition"}),
        ("comparison is walking the line", "assertion", {"rule": "comparison is walking the line"}),
        (
            "a square root of a number is the number which when multiplied by itself is that number",
            "assertion",
            {"rule": "a square root of a number is the number which when multiplied by itself is that number"},
        ),
    ],
)
def test_ladder_grammar(text, kind, slots):
    assert det_classify(text) == (kind, slots)


# ── rule lessons: capability is store data ──────────────────────────────────


def test_rule_lesson_writes_the_capability_fact(brainstem):
    r = brainstem.turn("subtraction is walking backward")
    ok, viol = validate_response(r.response_ir, "assertion")
    assert ok and not viol and r.contract_valid
    a = brainstem._codex.get("cap:sub-within-30:rule")
    assert a.status == EpistemicState.established
    assert a.provenance is not None and a.provenance.observer == "teacher"
    assert a.context.data["kind"] == "rule" and a.context.data["concept"] == "sub-within-30"
    # re-teaching corroborates: still ONE active policy fact for the concept
    brainstem.turn("subtraction is walking backward")
    acts = [x for x in brainstem._codex.query(relation="policy") if x.context.data.get("concept") == "sub-within-30"]
    assert len(acts) == 1 and [x.id for x in acts] == ["cap:sub-within-30:rule"]


def test_rule_gating_a_b_flip(brainstem):
    _teach_line(brainstem, 8)
    before = brainstem.turn("7 - 2 is what?")
    assert before.kind == "impossible"
    assert before.response_ir["gap"] == "not yet learned: walking backward (subtraction)"
    assert before.memory_diff == [] and before.grounded == []
    brainstem.turn("subtraction is walking backward")
    after = brainstem.turn("7 - 2 is what?")
    assert after.kind == "question" and after.response_ir["uncertainty_state"] == "derived"
    assert after.response_ir["answer"] == "5"
    assert "cap:sub-within-30:rule" in after.response_ir["evidence"]  # the capability is cited


# ── subtraction by walk-back ────────────────────────────────────────────────


def test_sub_derivation_and_walk_off(brainstem):
    _teach_line(brainstem, 8)
    brainstem.turn("subtraction is walking backward")
    r = brainstem.turn("7 - 2 is what?")
    assert r.response_ir["answer"] == "5" and r.response_ir["uncertainty_state"] == "derived"
    # two walk-back steps + the rule-fact cite
    assert len(r.response_ir["evidence"]) == 3
    r2 = brainstem.turn("3 - 5 is what?")
    assert r2.response_ir["uncertainty_state"] == "needs_info"
    assert any(str(e).startswith("walk-off:") for e in r2.response_ir["evidence"])
    ok, viol = validate_response(r2.response_ir, "question")
    assert ok and not viol


def test_sub_to_zero_is_exact(brainstem):
    _teach_line(brainstem, 4)
    brainstem.turn("subtraction is walking backward")
    r = brainstem.turn("2 - 2 is what?")
    assert r.response_ir["answer"] == "0"


# ── multiplication by composed repeated addition ────────────────────────────


def test_mult_composed_addition_and_zero_identity(brainstem):
    _teach_line(brainstem, 20)
    brainstem.turn("multiplication is repeated addition")
    r = brainstem.turn("3 * 4 is what?")
    assert r.response_ir["answer"] == "12" and r.response_ir["uncertainty_state"] == "derived"
    # 3 chains of 4 steps (12 fact cites) + the rule-fact cite
    assert r.response_ir["evidence"][-1] == "cap:mult-within-100:rule"
    assert len(r.response_ir["evidence"]) == 13
    r0 = brainstem.turn("2 * 0 is what?")
    assert r0.response_ir["answer"] == "0"
    assert r0.response_ir["evidence"] == ["cap:mult-within-100:rule"]  # identity cites the rule
    ok, viol = validate_response(r0.response_ir, "question")
    assert ok and not viol


def test_mult_line_end_is_honest(brainstem):
    _teach_line(brainstem, 5)  # line 0..5: 6 * 2 already over the line
    brainstem.turn("multiplication is repeated addition")
    r = brainstem.turn("6 * 2 is what?")
    assert r.response_ir["uncertainty_state"] == "needs_info"
    assert any(str(e).startswith("line-end:") for e in r.response_ir["evidence"])
    assert "my number line ends at 5" in r.response_text


# ── comparison by walking the line ──────────────────────────────────────────


def test_cmp_both_directions_and_equal(brainstem):
    _teach_line(brainstem, 4)
    brainstem.turn("comparison is walking the line")
    r = brainstem.turn("is 3 larger than 1?")
    assert r.response_ir["answer"] == "yes — 3 is 2 steps beyond 1"
    r2 = brainstem.turn("is 1 larger than 3?")
    assert r2.response_ir["answer"] == "no — 3 is 2 steps beyond 1"
    r3 = brainstem.turn("is 3 larger than 3?")
    assert r3.response_ir["answer"] == "neither — 3 is 3"
    assert r3.response_ir["evidence"] == ["cap:compare-numbers:rule"]  # zero steps cites the rule
    for x in (r, r2, r3):
        ok, viol = validate_response(x.response_ir, "question")
        assert ok and not viol


# ── the sqrt rung: exact, bracket, partial ──────────────────────────────────


def test_sqrt_exact_bracket_and_partial(brainstem):
    _teach_line(brainstem, 70)
    brainstem.turn("a square root of a number is the number which when multiplied by itself is that number")
    e = brainstem.turn("the square root of 16 is what?")
    assert e.response_ir["answer"] == "4" and e.response_ir["uncertainty_state"] == "derived"
    b20 = brainstem.turn("the square root of 20 is what?")
    assert b20.response_ir["uncertainty_state"] == "bracketed"
    assert "between 4 and 5" in str(b20.response_ir["answer"])
    assert "4 * 4 is 16" in b20.response_text and "5 * 5 is 25" in b20.response_text
    b50 = brainstem.turn("the square root of 50 is what?")
    assert "between 7 and 8" in str(b50.response_ir["answer"])
    p70 = brainstem.turn("the square root of 70 is what?")
    assert "greater than 8" in str(p70.response_ir["answer"])
    assert "my number line ends at 70" in p70.response_text
    for x in (e, b20, b50, p70):
        ok, viol = validate_response(x.response_ir, "question")
        assert ok and not viol


def test_sqrt_unlearned_before_definition(brainstem):
    _teach_line(brainstem, 70)
    r = brainstem.turn("the square root of 16 is what?")
    assert r.kind == "impossible"
    assert r.response_ir["gap"] == "not yet learned: the definition of square root"


# ── add-strip routing (E6.2: wide derived drills expose the wider strip) ───


def test_add_routing_derived_wide_exposes_wider_strip(brainstem):
    _teach_line(brainstem, 20)
    r = brainstem.turn("9 + 7 is what?")  # first wide drill: success -> add-two-digit
    assert r.response_ir["answer"] == "16"
    events = brainstem._codex.query(context_match={"kind": "mastery-event"})
    concepts = {a.context.data.get("concept") for a in events}
    assert "add-two-digit" in concepts and "add-within-10" not in concepts
    r2 = brainstem.turn("2 + 3 is what?")  # small sum stays on the pilot strip
    assert r2.response_ir["answer"] == "5"
    events = brainstem._codex.query(context_match={"kind": "mastery-event"})
    assert {a.context.data.get("concept") for a in events} == {"add-two-digit", "add-within-10", "count-successor"}


# ── the full bench (131 turns x 2 runs, all 8 checks) ───────────────────────


def test_e62_full_bench(tmp_path: Path):
    base = tmp_path / "phase-6"
    (base / "e6.1-run1").mkdir(parents=True)  # no official reference -> continuity reports None
    rep = run_e6_2(base)
    assert rep["checks_passed"] == CHECKS, {k: v for k, v in rep["checks"].items() if not v["pass"]}
    for name, c in rep["checks"].items():
        assert c["pass"], f"{name} failed: {c}"
    # frozen trajectory spot-pins
    traj = rep["checks"]["c2_learning"]["trajectory"]
    assert traj["sub-within-30"] == ["unexposed", "stable", "stable", "stable", "stable"]
    assert traj["compare-numbers"] == ["unexposed", "unexposed", "unexposed", "stable", "stable"]
    # the frozen attention set (the ladder continues the e6.1 conflict history)
    att = rep["checks"]["c6_disputes_attention"]["attention"]
    assert [a["turn"] for a in att] == ["S04:03", "S05:15", "S07:33"]
    # the wall: brackets + line end
    assert rep["derived"]["line_end"] == 70
    assert rep["checks"]["c8_stopping_point"]["honest_stops"] == ["S06:07", "S09:06", "S09:07", "S09:11", "S09:12"]
    assert rep["checks"]["c8_stopping_point"]["store_line_end"] == 70
    # determinism
    assert rep["checks"]["c7_determinism_continuity"]["byte_identical_run1_run2"] is True
    # 135 turns (30 replay + 105 ladder), 9 sessions
    assert rep["checks"]["c1_contract_valid"]["turns_validated"] == 135
    assert len(rep["derived"]["per_session"]) == 9
