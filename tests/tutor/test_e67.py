"""Unit tests for the E6.7 product band (T7 #157, band 3:
geometry-advanced ∥ vectors/statics). The full 48-turn band is the
experiment (e67.py); these pin the mechanism: the seven grounded
families, the shared one-corridor/many-doors alignment (product:
area ≡ moment; taking: lever ≡ algebra), the THREE honest walls
(product / negative / inexact), and the frozen band map."""

from __future__ import annotations

import pytest

from kainos.tutor.bands import band_by_name, validate_band_map
from kainos.tutor.brainstem import (
    CONCEPT_ALG_MUL,
    CONCEPT_BAND2,
    CONCEPT_BAND3,
    CONCEPT_GEO_AREA,
    CONCEPT_GEO_PERIM,
    CONCEPT_GEO_TRI,
    CONCEPT_STA_BAL,
    CONCEPT_STA_MOM,
    CONCEPT_STA_NET,
    det_classify,
)
from kainos.tutor.e67 import CONCEPTS_E67, FROZEN
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime

CONCEPTS = InfantRuntime.PILOT_CONCEPTS + CONCEPT_BAND2 + CONCEPT_BAND3

LESSONS_3 = {
    CONCEPT_GEO_AREA: "the area of a rectangle is the length times the width",
    CONCEPT_GEO_PERIM: "the perimeter of a rectangle is twice what you get by adding the length to the width",
    CONCEPT_GEO_TRI: "the area of a triangle is half of the base times the height",
    CONCEPT_STA_NET: "moving east then west, the net is what is left after you take the west part away from the east part",
    CONCEPT_STA_MOM: "a moment is the force times its distance from the pivot",
    CONCEPT_STA_BAL: "a beam balances when the moment on one side equals the moment on the other",
}

#: the band-2 repeated-taking inverse (the taking corridor its twin shares)
ALG_MUL_LESSON = "an unknown that a number times gives a total is found by taking away that number again and again until the total is gone"


@pytest.fixture()
def rt(tmp_path):
    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS))
    runtime.boot(1)
    for n in range(12):
        runtime.turn(f"after {n} comes {n + 1}")  # the line: 0..12
    return runtime


@pytest.fixture()
def rt_line72(tmp_path):
    """The band's real line (0..72) for the wall/off-line tests."""

    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS))
    runtime.boot(1)
    for n in range(72):
        runtime.turn(f"after {n} comes {n + 1}")
    return runtime


def teach(rt, concept_id: str) -> None:
    rt.turn(LESSONS_3[concept_id])


def test_grammar_the_seven_families():
    assert det_classify("what is the area of a 6 by 4 rectangle?") == (
        "question",
        {"mode": "geo-area", "l": 6, "w": 4},
    )
    assert det_classify("what is the perimeter of a 6 by 4 rectangle?") == (
        "question",
        {"mode": "geo-perim", "l": 6, "w": 4},
    )
    assert det_classify("what is the area of a triangle with base 5 and height 7?") == (
        "question",
        {"mode": "geo-tri", "b": 5, "h": 7},
    )
    assert det_classify("is a 4 by 6 rectangle bigger than a 3 by 8 rectangle?") == (
        "question",
        {"mode": "geo-cmp", "l1": 4, "w1": 6, "l2": 3, "w2": 8},
    )
    assert det_classify(
        "a cart moves 5 meters east then 8 meters west: how far from the start?"
    ) == (
        "question",
        {"mode": "sta-net", "e": 5, "w": 8},
    )
    assert det_classify("what is the moment of a 6 newton force at 4 meters?") == (
        "question",
        {"mode": "sta-mom", "f": 6, "d": 4},
    )
    assert det_classify(
        "a beam balances a 4 newton at 6 meters against what force at 3 meters?"
    ) == (
        "question",
        {"mode": "sta-bal", "f1": 4, "d1": 6, "d2": 3},
    )


def test_grammar_no_collision_with_old_families():
    # the frozen families keep their claims (bands 1-2)
    assert det_classify("what comes after 5?") == ("question", {"mode": "succ", "n": 5})
    assert det_classify("4 times x is 28: what is x?") == (
        "question",
        {"mode": "alg-mul", "a": 4, "b": 28},
    )
    assert det_classify(
        "a cart starts at 5 and goes 6 every minute: where is it after 4 minutes?"
    ) == (
        "question",
        {"mode": "kin-pos", "start": 5, "r": 6, "t": 4},
    )
    # near-misses of the band-3 grammar are honestly ambiguous
    assert det_classify("what is the area of a 6 by 4 rectangle") == (
        "ambiguous",
        {},
    )  # no question mark
    assert det_classify("a cart moves 5 meters east then 8 meters west how far?") == (
        "ambiguous",
        {},
    )
    assert det_classify("what is the moment of a 6 newton force at 4 meters away?") == (
        "ambiguous",
        {},
    )  # not the frozen form


def test_pre_teach_honest_gap_geometry(rt):
    t = rt.turn("what is the area of a 6 by 4 rectangle?")
    assert t.kind == "impossible"
    assert "not a capability i have been taught" in t.response_text
    assert t.memory_diff == [] and t.grounded == []
    assert t.concept == CONCEPT_GEO_AREA
    assert LESSONS_3[CONCEPT_GEO_AREA] in t.response_ir["nearest_plan"][0]


def test_pre_teach_honest_gap_statics(rt):
    t = rt.turn("what is the moment of a 6 newton force at 4 meters?")
    assert t.kind == "impossible"
    assert "not a capability i have been taught" in t.response_text
    assert t.memory_diff == [] and t.grounded == []
    assert t.concept == CONCEPT_STA_MOM


def test_area_is_a_product_chain_and_the_product_wall(rt_line72):
    teach(rt_line72, CONCEPT_GEO_AREA)
    t = rt_line72.turn("what is the area of a 6 by 4 rectangle?")
    assert t.response_ir["answer"] == "24"
    assert t.response_ir["uncertainty_state"] == "derived"
    assert f"cap:{CONCEPT_GEO_AREA}:rule" in t.response_ir["evidence"]
    assert len(t.grounded) > 1  # the product chain + the rule
    # the line ends at 72: 8x9 = 72 fits, 9x9 = 81 does not
    t = rt_line72.turn("what is the area of a 8 by 9 rectangle?")
    assert t.response_ir["answer"] == "72"
    t = rt_line72.turn("what is the area of a 9 by 9 rectangle?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "my number line ends at 72" in t.response_text
    assert t.grounded == []  # a wall cites nothing


def test_perimeter_sum_then_double(rt):
    teach(rt, CONCEPT_GEO_PERIM)
    t = rt.turn("what is the perimeter of a 2 by 3 rectangle?")
    assert t.response_ir["answer"] == "10"
    assert t.response_ir["uncertainty_state"] == "derived"
    assert f"cap:{CONCEPT_GEO_PERIM}:rule" in t.response_ir["evidence"]
    # 2·(4+3) = 14 is OFF the unit line (ends at 12) — the honest wall
    t = rt.turn("what is the perimeter of a 4 by 3 rectangle?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "my number line ends at 12" in t.response_text


def test_triangle_half_product_exact_and_inexact(rt_line72):
    teach(rt_line72, CONCEPT_GEO_TRI)
    t = rt_line72.turn("what is the area of a triangle with base 6 and height 5?")
    assert t.response_ir["answer"] == "15"
    assert t.response_ir["uncertainty_state"] == "derived"
    assert f"cap:{CONCEPT_GEO_TRI}:rule" in t.response_ir["evidence"]
    # inexact: half of 35 leaves 1 — honest, never rounded
    t = rt_line72.turn("what is the area of a triangle with base 5 and height 7?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "not a whole number on my line" in t.response_text
    assert "leaves 1" in t.response_text


def test_comparison_two_products_one_compare(rt):
    teach(rt, CONCEPT_GEO_AREA)
    t = rt.turn("is a 3 by 4 rectangle bigger than a 2 by 6 rectangle?")
    assert t.response_ir["answer"] == "no"  # 12 = 12 (equal)
    t = rt.turn("is a 4 by 3 rectangle bigger than a 2 by 5 rectangle?")
    assert t.response_ir["answer"] == "yes"  # 12 > 10
    assert t.concept == CONCEPT_GEO_AREA  # comparison rides the AREA concept


def test_net_east_west_exact_zero_and_the_negative_wall(rt):
    teach(rt, CONCEPT_STA_NET)
    t = rt.turn(
        "a cart moves 10 meters east then 3 meters west: how far from the start?"
    )
    assert t.response_ir["answer"] == "7"
    assert t.response_ir["uncertainty_state"] == "derived"
    t = rt.turn(
        "a cart moves 6 meters east then 6 meters west: how far from the start?"
    )
    assert t.response_ir["answer"] == "0"
    # the NEGATIVE wall: west of the start is past the line's origin
    t = rt.turn(
        "a cart moves 3 meters east then 8 meters west: how far from the start?"
    )
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "past the start by 5" in t.response_ir["answer"]
    assert "does not reach past the start" in t.response_text
    assert t.grounded  # the grounded difference IS cited (real, not fabricated)


def test_moment_is_a_product_and_the_wall_is_domain_agnostic(rt_line72):
    teach(rt_line72, CONCEPT_STA_MOM)
    t = rt_line72.turn("what is the moment of a 6 newton force at 4 meters?")
    assert t.response_ir["answer"] == "24"
    assert t.response_ir["uncertainty_state"] == "derived"
    assert f"cap:{CONCEPT_STA_MOM}:rule" in t.response_ir["evidence"]
    # the SAME 81 wall the area door hits (9x9 = 81 off the line)
    t = rt_line72.turn("what is the moment of a 9 newton force at 9 meters?")
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "my number line ends at 72" in t.response_text
    assert t.grounded == []


def test_lever_taking_exact_and_inexact(rt_line72):
    teach(rt_line72, CONCEPT_STA_BAL)
    t = rt_line72.turn(
        "a beam balances a 4 newton at 6 meters against what force at 3 meters?"
    )
    assert t.response_ir["answer"] == "8"
    assert t.response_ir["uncertainty_state"] == "derived"
    assert f"cap:{CONCEPT_STA_BAL}:rule" in t.response_ir["evidence"]
    # inexact: 30 taken in 4s leaves 2
    t = rt_line72.turn(
        "a beam balances a 5 newton at 6 meters against what force at 4 meters?"
    )
    assert str(t.response_ir["answer"]).startswith("needs_info")
    assert "not a whole number on my line" in t.response_text
    assert "leaves 2" in t.response_text


def test_product_corridor_the_area_moment_twins(rt_line72):
    """ONE corridor, two doors: the SAME numbers through the area door
    and the moment door cite byte-equal chains, differing only in the
    rule fact (the alignment, measured)."""

    rt = rt_line72
    teach(rt, CONCEPT_GEO_AREA)
    teach(rt, CONCEPT_STA_MOM)
    ta = rt.turn("what is the area of a 7 by 8 rectangle?")  # the area door
    tm = rt.turn(
        "what is the moment of a 7 newton force at 8 meters?"
    )  # the moment door
    assert ta.response_ir["answer"] == "56"
    assert tm.response_ir["answer"] == "56"
    ea, em = ta.response_ir["evidence"], tm.response_ir["evidence"]
    assert sorted(ea[:-1]) == sorted(em[:-1])  # the SAME product chain
    assert ea[-1] == f"cap:{CONCEPT_GEO_AREA}:rule"
    assert em[-1] == f"cap:{CONCEPT_STA_MOM}:rule"


def test_taking_corridor_the_lever_algebra_twins(rt_line72):
    """The taking corridor's third door shares the band-2 algebra
    door's taking cites for the same product (24 taken in 3s -> 8)."""

    rt = rt_line72
    rt.turn(ALG_MUL_LESSON)  # the band-2 repeated-taking inverse
    teach(rt, CONCEPT_STA_BAL)
    tb = rt.turn(
        "a beam balances a 4 newton at 6 meters against what force at 3 meters?"
    )
    tx = rt.turn("3 times x is 24: what is x?")
    assert tb.response_ir["answer"] == "8"
    assert tx.response_ir["answer"] == "8"
    eb, ex = tb.response_ir["evidence"], tx.response_ir["evidence"]
    assert eb[-1] == f"cap:{CONCEPT_STA_BAL}:rule"
    assert ex[-1] == f"cap:{CONCEPT_ALG_MUL}:rule"
    taking = [c for c in ex if c != f"cap:{CONCEPT_ALG_MUL}:rule"]
    assert taking  # the taking chain is non-empty
    assert all(c in eb for c in taking)  # the SAME taking cites
    assert len(eb) > len(ex)  # the balance door adds the product chain


def test_stored_alignment_edges_in_the_final_store(tmp_path):
    """The alignment is STORED CURRICULUM DATA: the cross-domain prereq
    edges are established in the store from boot (P11)."""

    reset_concepts()
    rt = InfantRuntime(tmp_path, concepts=list(CONCEPTS_E67))
    rt.boot(1)
    store = rt._brainstem._codex
    for edge_id in (
        "curriculum:prereq:stat-moment>geom-area",  # cross-domain, intra-band
        "curriculum:prereq:geom-area-triangle>alg-inverse-mul",  # cross-band
        "curriculum:prereq:stat-balance>alg-inverse-mul",  # cross-band
        "curriculum:prereq:stat-balance>stat-moment",
        "curriculum:prereq:geom-area-triangle>geom-area",
        "curriculum:prereq:geom-perimeter>add-two-digit",
        "curriculum:prereq:geom-area>mult-within-100",
        "curriculum:prereq:stat-net-1d>sub-within-30",
    ):
        edge = store.get(edge_id)
        assert edge is not None, f"missing stored edge {edge_id}"
        assert edge.validity is None or edge.validity.to is None, (
            f"edge {edge_id} not active"
        )


def test_band_map_band3_implemented():
    b3 = band_by_name("band-3")
    assert b3 is not None
    assert b3.status == "implemented"
    assert b3.band == "9-12"
    assert set(b3.domains) == {"geometry-advanced"}
    assert set(b3.aligned_physics) == {"vectors", "statics"}
    assert set(b3.concepts) == {c.id for c in CONCEPT_BAND3}
    # the prereq edges ARE the alignment (curriculum data)
    by_id = {c.id: c for c in CONCEPT_BAND3}
    assert by_id[CONCEPT_STA_MOM].prereqs == (CONCEPT_GEO_AREA,)
    assert by_id[CONCEPT_GEO_TRI].prereqs == (CONCEPT_GEO_AREA, CONCEPT_ALG_MUL)
    assert by_id[CONCEPT_STA_BAL].prereqs == (CONCEPT_STA_MOM, CONCEPT_ALG_MUL)
    # the map's registry moves with the sweep (savant-2 arrives with e6.9)
    from kainos.tutor.e69 import CONCEPTS_E69

    assert validate_band_map({c.id: c for c in CONCEPTS_E69})


def test_concepts_e67_carry_the_whole_band():
    ids = [c.id for c in CONCEPTS_E67]
    for cid in (
        CONCEPT_GEO_PERIM,
        CONCEPT_GEO_AREA,
        CONCEPT_GEO_TRI,
        CONCEPT_STA_NET,
        CONCEPT_STA_MOM,
        CONCEPT_STA_BAL,
    ):
        assert cid in ids
    assert ids.count(CONCEPT_GEO_AREA) == 1  # no duplicate concepts in the registry
    # the frozen script is the frozen script
    assert sum(len(v) for v in FROZEN["script"].values()) == FROZEN["total_turns"] == 48
    assert FROZEN["line_end_start"] == FROZEN["line_end_final"] == 72
    assert FROZEN["seed_total"] == 375
    # the control-frozen derived constants (the official run reproduces)
    assert FROZEN["final_total"] == 441
    assert FROZEN["new_facts"] == 20
    assert FROZEN["new_events"] == 46
