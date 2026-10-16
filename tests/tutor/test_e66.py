"""Unit tests for the E6.6 aligned band (T7 #157, band 2: algebra ∥
kinematics). The full 48-turn band is the experiment (e66.py); these
pin the mechanism: the seven grounded inverses, the shared
one-solver/two-doors corridor, the honest inexact/off-line
articulations, the name-bijection phrasology discipline, and the
frozen band map."""

from __future__ import annotations

import pytest

from kainos.tutor.bands import band_by_name, validate_band_map
from kainos.tutor.brainstem import (
    CONCEPT_ALG_2STEP,
    CONCEPT_ALG_ADD1,
    CONCEPT_ALG_MUL,
    CONCEPT_BAND2,
    CONCEPT_KIN_FAR,
    CONCEPT_KIN_POS,
    CONCEPT_KIN_RATE,
    CONCEPT_KIN_TIME,
    det_classify,
)
from kainos.tutor.e66 import CONCEPTS_E66, FROZEN
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime

CONCEPTS = InfantRuntime.PILOT_CONCEPTS + CONCEPT_BAND2

LESSONS = {
    CONCEPT_ALG_ADD1: "an unknown added to a number is found by taking that number away from the total",
    CONCEPT_ALG_MUL: "an unknown that a number times gives a total is found by taking away that number again and again until the total is gone",
    CONCEPT_ALG_2STEP: "two changes in a row are undone in reverse order",
    CONCEPT_KIN_FAR: "at a steady pace, the distance is the pace times the time",
    CONCEPT_KIN_POS: "position is the start plus the distance",
    CONCEPT_KIN_TIME: "time is found the same way any unknown is found: undo the equation",
    CONCEPT_KIN_RATE: "a steady pace is found by taking the time away from the distance again and again until the distance is gone",
}


@pytest.fixture()
def rt(tmp_path):
    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS))
    runtime.boot(1)
    for n in range(12):
        runtime.turn(f"after {n} comes {n+1}")  # the line: 0..12
    return runtime


@pytest.fixture()
def rt_line72(tmp_path):
    """The band's real line (0..72) for the wall/off-line tests."""

    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS))
    runtime.boot(1)
    for n in range(72):
        runtime.turn(f"after {n} comes {n+1}")
    return runtime


def teach(rt, concept_id: str) -> None:
    rt.turn(LESSONS[concept_id])


def test_grammar_the_seven_families(rt):
    assert det_classify("what is x, if x + 6 is 12?") == ("question", {"mode": "alg-add", "a": 6, "b": 12})
    assert det_classify("4 times x is 28: what is x?") == ("question", {"mode": "alg-mul", "a": 4, "b": 28})
    assert det_classify("6 times x plus 4 is 40: what is x?") == ("question", {"mode": "alg-2step", "a": 6, "b": 4, "c": 40})
    assert det_classify("how far does a cart go in 4 minutes at 6 a minute?") == ("question", {"mode": "kin-far", "r": 6, "t": 4})
    assert det_classify("a cart starts at 5 and goes 6 every minute: where is it after 4 minutes?") == (
        "question",
        {"mode": "kin-pos", "start": 5, "r": 6, "t": 4},
    )
    assert det_classify("a cart starts at 4 and goes 6 every minute and is at 40: how many minutes did it take?") == (
        "question",
        {"mode": "kin-time", "start": 4, "r": 6, "c": 40},
    )
    assert det_classify("a cart covers 36 miles in 4 minutes: how many miles every minute was that?") == (
        "question",
        {"mode": "kin-rate", "d": 36, "t": 4},
    )


def test_grammar_no_collision_with_old_families(rt):
    # the frozen families keep their claims
    assert det_classify("what comes after 5?") == ("question", {"mode": "succ", "n": 5})
    assert det_classify("17 + 25 is what?") == ("question", {"mode": "add", "a": 17, "b": 25})
    assert det_classify("how many sides does a triangle have?") == (
        "question",
        {"mode": "shape", "shape": "triangle", "property": "sides"},
    )
    # near-misses of the band-2 grammar are honestly ambiguous
    assert det_classify("what is x, if x + 6 is 12") == ("ambiguous", {})  # no question mark
    assert det_classify("a cart starts at 5 and goes 6 every minute where is it after 4 minutes?") == ("ambiguous", {})
    assert det_classify("what is x, if x plus 6 is 12?") == ("ambiguous", {})  # "plus" spelled out is not the frozen form


def test_pre_teach_honest_gap_algebra(rt):
    t = rt.turn("what is x, if x + 6 is 12?")
    assert t.kind == "impossible"
    assert "not a capability i have been taught" in t.response_text
    assert t.memory_diff == [] and t.grounded == []
    assert t.concept == CONCEPT_ALG_ADD1
    assert LESSONS[CONCEPT_ALG_ADD1] in t.response_ir["nearest_plan"][0]


def test_pre_teach_honest_gap_kinematics(rt):
    t = rt.turn("a cart starts at 0 and goes 6 every minute: where is it after 4 minutes?")
    assert t.kind == "impossible"
    assert "not a capability i have been taught" in t.response_text
    assert t.memory_diff == [] and t.grounded == []
    assert t.concept == CONCEPT_KIN_POS


def test_algebra_one_step_is_a_grounding_walk_back(rt):
    teach(rt, CONCEPT_ALG_ADD1)
    t = rt.turn("what is x, if x + 6 is 12?")
    assert t.response_ir["answer"] == "6"
    assert t.response_ir["uncertainty_state"] == "derived"
    assert f"cap:{CONCEPT_ALG_ADD1}:rule" in t.response_ir["evidence"]
    assert len(t.grounded) > 1  # the line steps + the rule


def test_algebra_repeated_taking_exact_and_inexact(rt):
    teach(rt, CONCEPT_ALG_MUL)
    t = rt.turn("4 times x is 12: what is x?")
    assert t.response_ir["answer"] == "3"
    assert t.response_ir["uncertainty_state"] == "derived"
    # inexact: NOT a whole number on the line — honest, never rounded
    t = rt.turn("5 times x is 11: what is x?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "not a whole number on my line" in t.response_text
    assert "leaves 1" in t.response_text  # 11 - 5 - 5 = 1
    # smaller than one step
    t = rt.turn("4 times x is 3: what is x?")
    assert str(t.response_ir["answer"]).startswith("needs_info")


def test_repeated_taking_offline_the_wall(rt):
    teach(rt, CONCEPT_ALG_MUL)
    # line 0..12: 15 is OFF the line even though 15/5 = 3 is exact in the math
    t = rt.turn("15 times x is 45: what is x?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "my number line ends at 12" in t.response_text
    assert t.grounded == []  # a wall cites nothing


def test_take_away_guardrails(rt):
    b = rt._brainstem  # the brainstem
    # a <= 0 is not a taking
    assert b._take_away(10, 0)[0] == "offline"
    # n off the line
    assert b._take_away(99, 3)[0] == "offline"
    # exact identity: zero times taken
    assert b._take_away(0, 5) == ("exact", 0, [])


def test_the_alignment_one_solver_two_doors(rt_line72):
    rt = rt_line72
    teach(rt, CONCEPT_ALG_2STEP)
    teach(rt, CONCEPT_KIN_TIME)
    ta = rt.turn("6 times x plus 4 is 40: what is x?")  # the algebra door
    tk = rt.turn("a cart starts at 4 and goes 6 every minute and is at 40: how many minutes did it take?")  # the kin door
    assert ta.response_ir["answer"] == "6"
    assert tk.response_ir["answer"] == "6"
    ea, ek = ta.response_ir["evidence"], tk.response_ir["evidence"]
    # the two doors cite the SAME line steps (the one corridor)
    assert sorted(ea[:-1]) == sorted(ek[:-1])
    # ...and differ ONLY in the rule fact
    assert ea[-1] == f"cap:{CONCEPT_ALG_2STEP}:rule"
    assert ek[-1] == f"cap:{CONCEPT_KIN_TIME}:rule"


def test_kin_position_composition_and_wall(rt):
    teach(rt, CONCEPT_KIN_FAR)
    teach(rt, CONCEPT_KIN_POS)
    # the line is 0..12: distance 3·2 = 6 fits, start+distance = 6+6 = 12 fits
    t = rt.turn("a cart starts at 6 and goes 3 every minute: where is it after 2 minutes?")
    assert t.response_ir["answer"] == "12"
    assert t.response_ir["uncertainty_state"] == "derived"
    # start 9 + distance 6 = 15 is OFF the line (the distance FITS — the wall names it)
    t = rt.turn("a cart starts at 9 and goes 3 every minute: where is it after 2 minutes?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "the cart would be at 15" in t.response_text and "number line ends at 12" in t.response_text


def test_kin_far_and_kin_rate(rt):
    teach(rt, CONCEPT_KIN_FAR)
    teach(rt, CONCEPT_KIN_RATE)
    t = rt.turn("how far does a cart go in 3 minutes at 4 a minute?")
    assert t.response_ir["answer"] == "12"
    assert t.response_ir["uncertainty_state"] == "derived"
    t = rt.turn("a cart covers 12 miles in 4 minutes: how many miles every minute was that?")
    assert t.response_ir["answer"] == "3"
    # an inexact pace is honest
    t = rt.turn("a cart covers 11 miles in 4 minutes: how many miles every minute was that?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "whole number on my line" in t.response_text  # the family-level honest articulation


def test_name_bijection_rejects_a_wrong_kin_mapping(rt):
    # every kin family carries DIFFERENT slot names: the leaving-phrasing
    # ({start} {r} {t}) can never map onto the time family ({start} {r} {c})
    t = rt.turn(
        'the phrasing "a cart leaving {start} at {r} a minute: where is it after {t} minutes?" '
        'is the same as "a cart starts at {start} and goes {r} every minute and is at {c}: how many minutes did it take?"'
    )
    assert t.kind == "ambiguous"
    assert "i can't take that as a mapping" in t.response_text
    assert "slot names" in t.response_text
    assert t.memory_diff == []  # a wrong family is never silently stored
    # a fixed number in a new template is rejected too (a pinned slot breaks
    # the name bijection first, so the honest rejection is by names — either
    # way: never silently stored)
    t = rt.turn(
        'the phrasing "a cart leaving 5 at {r} a minute: where is it after {t} minutes?" '
        'is the same as "a cart starts at {start} and goes {r} every minute: where is it after {t} minutes?"'
    )
    assert t.kind == "ambiguous"
    assert "i can't take that as a mapping" in t.response_text
    assert t.memory_diff == []


def test_kin_phrasology_twin_of_its_canonical(rt):
    teach(rt, CONCEPT_KIN_FAR)
    teach(rt, CONCEPT_KIN_POS)
    t = rt.turn(
        'the phrasing "a cart leaving {start} at {r} a minute: where is it after {t} minutes?" '
        'is the same as "a cart starts at {start} and goes {r} every minute: where is it after {t} minutes?"'
    )
    assert t.kind == "assertion"
    pid = t.memory_diff[0]
    t_lex = rt.turn("a cart leaving 5 at 3 a minute: where is it after 2 minutes?")
    t_canon = rt.turn("a cart starts at 5 and goes 3 every minute: where is it after 2 minutes?")
    assert t_lex.response_ir["answer"] == "11"
    assert t_canon.response_ir["answer"] == "11"
    assert t_lex.response_ir["parse_source"] == f"lexicon:{pid}"
    # parse != content: the content is byte-equal modulo the parse source
    strip = lambda ir: {k: v for k, v in ir.items() if k != "parse_source"}
    assert strip(t_lex.response_ir) == strip(t_canon.response_ir)
    assert t_lex.response_text == t_canon.response_text


def test_band_map_band2_implemented():
    b2 = band_by_name("band-2")
    assert b2 is not None
    assert b2.status == "implemented"
    assert b2.band == "6-8"
    assert set(b2.domains) == {"algebra"}
    assert set(b2.aligned_physics) == {"kinematics"}
    assert set(b2.concepts) == {c.id for c in CONCEPT_BAND2}
    # the prereq edges ARE the alignment (curriculum data)
    by_id = {c.id: c for c in CONCEPT_BAND2}
    assert by_id[CONCEPT_KIN_TIME].prereqs == (CONCEPT_ALG_2STEP,)
    assert by_id[CONCEPT_KIN_RATE].prereqs == (CONCEPT_ALG_MUL,)
    # the map's registry moves with the sweep (savant-2 arrives with e6.9)
    from kainos.tutor.e69 import CONCEPTS_E69

    assert validate_band_map({c.id: c for c in CONCEPTS_E69})


def test_concepts_e66_carry_the_whole_band():
    ids = [c.id for c in CONCEPTS_E66]
    for cid in (CONCEPT_ALG_ADD1, CONCEPT_ALG_MUL, CONCEPT_ALG_2STEP, CONCEPT_KIN_FAR, CONCEPT_KIN_POS, CONCEPT_KIN_TIME, CONCEPT_KIN_RATE):
        assert cid in ids
    assert ids.count(CONCEPT_KIN_POS) == 1  # no duplicate concepts in the registry
    # the frozen script is the frozen script
    assert sum(len(v) for v in FROZEN["script"].values()) == FROZEN["total_turns"]
    assert FROZEN["line_end_start"] == FROZEN["line_end_final"] == 72
