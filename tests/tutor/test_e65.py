"""Unit tests for the E6.5 geometry strip (T7 #157, band 1: numerics ∥
geometry). The full 48-turn band is the experiment (e65.py); these pin
the mechanism: rule-gated shape capability, the single-current-claimant
arc, the vocabulary-slot phrasology, and the frozen band map."""

from __future__ import annotations

import pytest

from kainos.codex.models import EpistemicState
from kainos.tutor.bands import band_by_name, validate_band_map
from kainos.tutor.brainstem import (
    CONCEPT_SHAPES,
    SHAPE_LESSON_CIRCLE,
    canonical_shape_lesson,
    det_classify,
    slots_ok_shape,
)
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime

CONCEPTS = list(InfantRuntime.PILOT_CONCEPTS) + [c for c in CONCEPT_SHAPES]


@pytest.fixture()
def rt(tmp_path):
    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=CONCEPTS)
    runtime.boot(1)
    return runtime


def test_grammar_shape_lessons(rt):
    assert det_classify("the triangle has 3 sides and 3 corners") == ("assertion", {"shape": "triangle", "sides": 3, "corners": 3})
    assert det_classify("no — that was a mistake; the square has 4 sides and 4 corners") == (
        "correction",
        {"shape": "square", "sides": 4, "corners": 4},
    )
    assert det_classify(SHAPE_LESSON_CIRCLE) == ("assertion", {"shape": "circle"})
    assert det_classify("how many sides does a triangle have?") == ("question", {"mode": "shape", "shape": "triangle", "property": "sides"})
    assert det_classify("how many corners does a circle have?") == ("question", {"mode": "shape", "shape": "circle", "property": "corners"})
    # the grammar is untouched where it used to win
    assert det_classify("what comes after 5?") == ("question", {"mode": "succ", "n": 5})


def test_grammar_out_of_band_is_ambiguous(rt):
    assert det_classify("how many edges does a pentagon have?") == ("ambiguous", {})


def test_pre_teach_honest_gap(rt):
    t = rt.turn("how many sides does a square have?")
    assert t.kind == "impossible"
    assert "not a capability i have been taught" in t.response_text
    assert t.memory_diff == []
    assert t.grounded == []
    assert "the square's definition" in t.response_ir["gap"]
    assert canonical_shape_lesson("square") in t.response_ir["nearest_plan"][0]


def test_lesson_then_drill_is_grounded(rt):
    rt.turn("the triangle has 3 sides and 3 corners")
    t = rt.turn("how many sides does a triangle have?")
    assert t.response_ir["answer"] == "3"
    assert t.response_ir["uncertainty_state"] == "derived"
    assert len(t.grounded) == 1
    store = rt._brainstem._codex
    fact = store.get(t.grounded[0])
    assert fact is not None and fact.context.data["concept"] == "shape-triangle"
    assert fact.context.data["sides"] == 3


def test_wrong_value_arc_single_claimant(rt):
    rt.turn("the square has 4 sides and 3 corners")  # the WRONG value, first claimant
    wrong = rt.turn("how many corners does a square have?")
    assert wrong.response_ir["answer"] == "3"  # measured while the wrong claim is active
    corr = rt.turn("no — that was a mistake; the square has 4 sides and 4 corners")
    assert corr.kind == "correction"
    assert corr.conflict is not None and corr.conflict["fact"] == "definition:shape-square"
    after = rt.turn("how many corners does a square have?")
    assert after.response_ir["answer"] == "4"
    store = rt._brainstem._codex
    from kainos.tutor.brainstem import REL_POLICY

    square_defs = [
        a
        for a in store.query(relation=REL_POLICY)
        if a.context.data.get("concept") == "shape-square" and a.context.data.get("kind") == "definition"
    ]
    est = [a for a in square_defs if a.status == EpistemicState.established and (a.validity is None or a.validity.to is None)]
    obs = [a for a in square_defs if a.status == EpistemicState.obsolete]
    assert len(est) == 1 and len(obs) == 1
    assert est[0].context.data["corners"] == 4
    assert obs[0].validity is not None and obs[0].validity.to is not None
    # linked: the replacement cites the superseded side
    assert obs[0].id in est[0].provenance.evidence or est[0].id in obs[0].provenance.evidence


def test_no_marker_conflict_disputes_never_overwrites(rt):
    rt.turn("the square has 4 sides and 4 corners")
    t = rt.turn("the square has 5 sides and 4 corners")  # no marker: a conflicting claim
    assert t.kind == "assertion"
    assert t.response_ir["epistemic_state"] == "candidate"
    store = rt._brainstem._codex
    est = [
        a
        for a in store.query(subject="capability:shape-square")
        if a.status == EpistemicState.established and (a.validity is None or a.validity.to is None)
    ]
    disp = [a for a in store.query(subject="capability:shape-square") if a.status == EpistemicState.disputed]
    cand = [a for a in store.query(subject="capability:shape-square") if a.status == EpistemicState.candidate]
    assert len(est) == 0 and len(disp) == 1 and len(cand) == 1  # the old claim is disputed, the new one is a candidate — never overwritten
    # with two live claimants the drill is an HONEST gap, never a guess
    drill = rt.turn("how many sides does a square have?")
    assert drill.kind == "impossible"
    assert drill.grounded == []


def test_circle_none(rt):
    rt.turn(SHAPE_LESSON_CIRCLE)
    t = rt.turn("how many sides does a circle have?")
    assert t.response_ir["answer"] == "none"
    assert "no sides" in t.response_text
    c = rt.turn("how many corners does a circle have?")
    assert c.response_ir["answer"] == "none"


def test_vocab_slot_phrasology(rt):
    rt.turn("the triangle has 3 sides and 3 corners")
    pre = rt.turn("how many edges does a triangle have?")  # untaught phrasing
    assert pre.kind == "ambiguous"
    teach = rt.turn('the phrasing "how many edges does a {shape} have?" is the same as "how many sides does a {shape} have?"')
    assert teach.kind == "assertion"
    assert teach.response_ir["epistemic_state"] == "established"
    post = rt.turn("how many edges does a triangle have?")
    assert post.kind == "question"
    assert post.response_ir.get("parse_source", "").startswith("lexicon:")
    assert post.response_ir["answer"] == "3"
    assert post.grounded  # content is still grounded (parse != content)


def test_vocab_slot_fixed_word_rejected(rt):
    t = rt.turn('the phrasing "how many edges does a square have?" is the same as "how many sides does a {shape} have?"')
    assert t.kind == "ambiguous"
    assert "i can't take that as a mapping" in t.response_text
    assert t.memory_diff == []


def test_slot_type_mismatch_rejected(rt):
    t = rt.turn('the phrasing "how many sides does a {shape} have?" is the same as "what comes after {n}?"')
    assert t.kind == "ambiguous"
    assert t.memory_diff == []


def test_sibling_mapping_corrected_via_lexicon_pair(rt):
    rt.turn("the circle has no sides and no corners")
    rt.turn('the phrasing "how many points does a {shape} have?" is the same as "how many sides does a {shape} have?"')
    mid = rt.turn("how many points does a circle have?")
    assert mid.response_ir["answer"] == "none"  # the circle is 0/0: the value is family-blind (recorded honestly)
    rt.turn('no — that was a mistake; the phrasing "how many points does a {shape} have?" is the same as "how many corners does a {shape} have?"')
    after = rt.turn("how many points does a circle have?")
    assert after.response_ir["answer"] == "none"
    store = rt._brainstem._codex
    from kainos.tutor.brainstem import REL_PHRASING

    pts = [a for a in store.query(relation=REL_PHRASING) if "points" in a.context.data.get("new", "")]
    est = [a for a in pts if a.status == EpistemicState.established and (a.validity is None or a.validity.to is None)]
    obs = [a for a in pts if a.status == EpistemicState.obsolete]
    assert len(est) == 1 and est[0].object_id == "pat:shape-corners"
    assert len(obs) == 1 and obs[0].object_id == "pat:shape-sides"


def test_geometry_writes_no_successor_facts(rt):
    rt.turn("the triangle has 3 sides and 3 corners")
    rt.turn("how many sides does a triangle have?")
    store = rt._brainstem._codex
    succ = [a for a in store.query(context_match={"kind": "fact", "concept": "count-successor"})]
    assert succ == []  # the geometry strip is orthogonal to the numeric line


def test_slots_ok_shape_schemas(rt):
    assert slots_ok_shape({"shape": "triangle", "sides": 3, "corners": 3})
    assert slots_ok_shape({"shape": "circle"})
    assert not slots_ok_shape({"shape": "pentagon", "sides": 5, "corners": 5})
    assert not slots_ok_shape({"shape": "triangle", "sides": "three", "corners": 3})
    assert not slots_ok_shape({"shape": "triangle", "sides": 3})


def test_canonical_lesson_wording(rt):
    assert canonical_shape_lesson("triangle") == "the triangle has 3 sides and 3 corners"
    assert canonical_shape_lesson("circle") == "the circle has no sides and no corners"


def test_band_map_declares_directive_alignment(rt):
    # the map is validated against the WHOLE sweep-so-far registry (band 1 +
    # band 2 + band 3 + savant 1..4 + rh 1..3) — S10 added NO concepts
    # (a measurement band), so the registry is still the e6.13 one
    from kainos.tutor.e613 import CONCEPTS_E613

    doc = validate_band_map({c.id: c for c in CONCEPTS_E613})
    assert doc["bands"] == 12 and doc["implemented"] == 10 and doc["problems"] == []  # rh-1 + rh-2 + rh-3 official (e6.12 + e6.13 + e6.14)
    assert band_by_name("band-1").status == "implemented"
    assert band_by_name("band-1").domains == ("arithmetic", "geometry")
    assert band_by_name("band-2").aligned_physics == ("kinematics",)
    assert band_by_name("band-3").aligned_physics == ("vectors", "statics")
    assert band_by_name("band-4").aligned_physics == ("mechanics",)
    assert band_by_name("band-5").aligned_physics == ("probabilistic physics",)
    assert band_by_name("band-2").status == "implemented"  # official: e6.6
    assert band_by_name("band-3").status == "implemented"  # official: e6.7
    assert band_by_name("savant-1").status == "implemented"  # official: e6.8
    assert band_by_name("savant-2").status == "implemented"  # official: e6.9
    assert band_by_name("savant-3").status == "implemented"  # official: e6.10
    assert band_by_name("savant-4").status == "implemented"  # official: e6.11
    assert band_by_name("rh-1").status == "implemented"  # official: e6.12
    assert band_by_name("rh-2").status == "implemented"  # official: e6.13
    assert band_by_name("rh-3").status == "implemented"  # official: e6.14 (S10: the attempt)
    declared_tail = (band_by_name("band-4"), band_by_name("band-5"))
    assert all(b.status == "declared" and b.concepts == () for b in declared_tail)


def test_mastery_events_land_on_the_shape_concept(rt):
    rt.turn("the square has 4 sides and 4 corners")
    t = rt.turn("how many sides does a square have?")
    assert t.concept == "shape-square"
    from kainos.tutor.brainstem import REL_HAS_EVENT

    store = rt._brainstem._codex
    evs = [a for a in store.query(relation=REL_HAS_EVENT) if a.context.data.get("concept") == "shape-square" and a.object_id == "derivation-correct"]
    assert len(evs) == 1
