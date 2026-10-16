"""Unit tests for E6.9 (SAVANT-TRACK S5: the number-field toolkit
band, A-cluster, shallow). The full 65-turn band is the experiment
(e69.py); these pin the mechanism: the sixteen savant concepts, the
sixteen seam facts, the six new grammar families (sqmod / gsay /
sumsq / holes / whydeep / duopow), the WHY wall (the proof object is
missing — honest needs_info), the MAGNITUDE wall (128 off the line
at 72), and the seam invariance (the conjecture never a premise)."""

from __future__ import annotations

import pytest

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT5,
    S5_LESSONS,
    det_classify,
)
from kainos.tutor.e68 import CONCEPTS_E68
from kainos.tutor.e69 import (
    _LESSON_META_S5,
    CONCEPTS_E69,
    FROZEN,
    GAP_ARTICULATION,
    SCRIPT_HASH,
    _st,
)
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime


@pytest.fixture()
def rt_line72(tmp_path):
    """The S5 band's real line (0..72, the e6.8 line end) with the
    full S5 concept registry."""

    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS_E69))
    runtime.boot(1)
    for n in range(72):
        runtime.turn(f"after {n} comes {n + 1}")
    return runtime


def _lesson(slug: str) -> str:
    return _LESSON_META_S5[slug]["statement"]


def test_savant2_implemented_in_the_band_map():
    b = band_by_name("savant-2")
    assert b.status == "implemented"
    assert b.evidence == ("e6.9",)
    assert set(b.concepts) == {c.id for c in CONCEPT_SAVANT5}
    assert band_by_name("savant-4").status == "implemented"  # official with e6.11 (S7: the savant test proper)
    assert band_by_name("savant-4").evidence == ("e6.11",)


def test_concepts_e69_carry_the_savant_band():
    ids = [c.id for c in CONCEPTS_E69]
    assert len(CONCEPTS_E69) == len(CONCEPTS_E68) + 16
    for c in CONCEPT_SAVANT5:
        assert c.id in ids
    # the prereq edges are declared (the curriculum data of the tower
    # — every S5 concept rides the arithmetic ground it needs)
    by_id = {c.id: c for c in CONCEPTS_E69}
    assert by_id["number-field"].prereqs == ("count-successor",)
    assert by_id["prime-split"].prereqs == ("number-field",)
    assert by_id["mod4-split"].prereqs == ("prime-split",)
    assert by_id["disc-rd"].prereqs == ("number-field",)
    assert by_id["adjoin-i"].prereqs == ("disc-rd",)
    assert by_id["cyclotomic-cubic"].prereqs == ("prime-split", "disc-rd")
    assert by_id["char-cutout"].prereqs == ("cyclotomic-cubic",)
    assert by_id["class-bound"].prereqs == ("number-field",)
    assert by_id["chebotarev"].prereqs == ("prime-split",)
    assert by_id["pnt-ap"].prereqs == ("chebotarev",)
    assert by_id["frattini"].prereqs == ("number-field",)
    assert by_id["golod-shaf"].prereqs == ("frattini",)
    assert by_id["shafarevich"].prereqs == ("golod-shaf", "number-field")
    assert by_id["cm-conj"].prereqs == ("number-field",)
    assert by_id["minkowski-embed"].prereqs == ("number-field",)
    assert by_id["hajir-maire"].prereqs == ("shafarevich", "class-bound", "golod-shaf")


def test_grammar_the_sav5_families():
    assert det_classify("state the numberfields rule") == ("question", {"mode": "lem-state", "slug": "numberfields"})
    assert det_classify("what is the gstest for") == ("question", {"mode": "lem-why", "slug": "gstest"})
    assert det_classify("explain why the shafbound holds") == ("question", {"mode": "whydeep", "slug": "shafbound"})
    assert det_classify("explain why the kstbound holds") == ("question", {"mode": "whydeep", "slug": "kstbound"})
    assert det_classify("does 2 squared plus one vanish modulo 5?") == ("question", {"mode": "sqmod", "x": 2, "q": 5})
    assert det_classify("does the gs test say infinite for 3 generators and 2 relations?") == (
        "question",
        {"mode": "gsay", "d": 3, "r": 2},
    )
    assert det_classify("what is 3 squared plus 4 squared?") == ("question", {"mode": "sumsq", "a": 3, "b": 4})
    assert det_classify("what is the biggest hole guaranteed when 5 items go into 2 holes?") == (
        "question",
        {"mode": "holes", "p": 5, "m": 2},
    )
    assert det_classify("how large is two raised to the 7?") == ("question", {"mode": "duopow", "e": 7})


def test_grammar_no_collision_with_old_families():
    # an unknown slug must NOT classify as an S5 state/why/whydeep probe
    assert det_classify("state the frobnicate rule")[1].get("mode") != "lem-state"
    assert det_classify("what is the frobnicate for")[1].get("mode") != "lem-why"
    assert det_classify("explain why the frobnicate holds")[1].get("mode") != "whydeep"
    # the S4 families are untouched by the seam growth
    assert det_classify("what is the status of the erdosguess?") == ("question", {"mode": "conj-state", "proven": False})


def live_store(rt):
    """The brainstem's live codex store (no lapse needed)."""

    return rt._brainstem._codex


def test_lesson_writes_the_seam_fact_established(rt_line72):
    r1 = rt_line72.turn(_lesson("mod4minusone"))
    assert r1.kind == "assertion"
    assert "lemma:mod4minusone" in (r1.memory_diff or [])
    # re-teaching is a corroboration (no duplicate fact)
    r2 = rt_line72.turn(_lesson("mod4minusone"))
    assert not (r2.memory_diff or [])
    # the fact: established, declared-source, with the line crosswalk
    store = live_store(rt_line72)
    fact = None
    for a in store.query():
        if a.id == "lemma:mod4minusone":
            fact = a
            break
    assert fact is not None
    assert fact.object == _st("mod4minusone")
    assert fact.context.data["kind"] == "lemma"
    assert fact.context.data["source_role"] == "declared-source"
    assert fact.context.data["source_lines"]


def test_state_why_exact_after_lesson(rt_line72):
    rt_line72.turn(_lesson("numberfields"))
    r = rt_line72.turn("state the numberfields rule")
    assert r.kind == "question"
    assert (r.response_ir or {}).get("answer") == _st("numberfields")
    assert (r.response_ir or {}).get("uncertainty_state") == "derived"
    assert "lemma:numberfields" in (r.grounded or [])
    w = rt_line72.turn("what is the numberfields for")
    assert (w.response_ir or {}).get("answer") == _LESSON_META_S5["numberfields"]["essence"]
    assert (w.response_text or "").startswith("it is for this: ")


def test_pre_lesson_probes_are_honest_gaps(rt_line72):
    for probe in (
        "state the numberfields rule",
        "does 2 squared plus one vanish modulo 5?",
        "what is the biggest hole guaranteed when 5 items go into 2 holes?",
        "does the gs test say infinite for 3 generators and 2 relations?",
        "what is 3 squared plus 4 squared?",
    ):
        r = rt_line72.turn(probe)
        assert r.kind == "impossible", probe
        assert GAP_ARTICULATION in (r.response_text or "")
        assert not (r.grounded or [])
        assert not (r.memory_diff or [])


def test_sqmod_beds_on_the_line(rt_line72):
    rt_line72.turn(_lesson("mod4minusone"))
    cases = {
        "does 2 squared plus one vanish modulo 5?": "yes — 2 squared plus one is 1 times 5",
        "does 1 squared plus one vanish modulo 7?": "no — the residue is 2",
        "does 3 squared plus one vanish modulo 7?": "no — the residue is 3 after taking one lot of 7",
        "does 5 squared plus one vanish modulo 13?": "yes — 5 squared plus one is 2 times 13",
        "does 4 squared plus one vanish modulo 17?": "yes — 4 squared plus one is 1 times 17",
        "does 3 squared plus one vanish modulo 11?": "no — the residue is 10",
        "does 6 squared plus one vanish modulo 19?": "no — the residue is 18 after taking one lot of 19",
    }
    for q, expected in cases.items():
        r = rt_line72.turn(q)
        assert (r.response_ir or {}).get("answer") == expected, q
        assert (r.response_ir or {}).get("uncertainty_state") == "derived"
        assert "lemma:mod4minusone" in (r.grounded or [])


def test_gsay_beds_on_the_line(rt_line72):
    rt_line72.turn(_lesson("gstest"))
    yes = rt_line72.turn("does the gs test say infinite for 3 generators and 2 relations?")
    assert (yes.response_ir or {}).get("answer") == "yes — four times r is 8, at most d squared, 9, so the test says infinite"
    yes2 = rt_line72.turn("does the gs test say infinite for 5 generators and 3 relations?")
    assert (yes2.response_ir or {}).get("answer") == "yes — four times r is 12, at most d squared, 25, so the test says infinite"
    silent = rt_line72.turn("does the gs test say infinite for 3 generators and 6 relations?")
    assert (silent.response_ir or {}).get("answer") == "no — the test is silent, four times r is 24, above d squared, 9"
    for r in (yes, yes2, silent):
        assert (r.response_ir or {}).get("uncertainty_state") == "derived", r.response_ir
        assert "lemma:gstest" in (r.grounded or [])


def test_sumsq_holes_duopow_on_the_line_and_wall(rt_line72):
    rt_line72.turn(_lesson("cmunit"))
    rt_line72.turn(_lesson("classbound"))
    assert "25" == (rt_line72.turn("what is 3 squared plus 4 squared?").response_ir or {}).get("answer")
    assert "50" == (rt_line72.turn("what is 1 squared plus 7 squared?").response_ir or {}).get("answer")
    assert "3" == (rt_line72.turn("what is the biggest hole guaranteed when 5 items go into 2 holes?").response_ir or {}).get("answer")
    assert "3" == (rt_line72.turn("what is the biggest hole guaranteed when 7 items go into 3 holes?").response_ir or {}).get("answer")
    # duopow: 2^6 = 64 is ON the line; 2^7 = 128 is the MAGNITUDE WALL
    d6 = rt_line72.turn("how large is two raised to the 6?")
    assert "64" == (d6.response_ir or {}).get("answer")
    assert (d6.response_ir or {}).get("uncertainty_state") == "derived"
    d7 = rt_line72.turn("how large is two raised to the 7?")
    ir = d7.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "128" in ir["answer"] and "72" in ir["answer"]
    assert not (d7.grounded or [])


def test_whydeep_is_the_honest_wall(rt_line72):
    # pre-lesson: the honest not-yet-learned gap
    r0 = rt_line72.turn("explain why the gstest holds")
    assert r0.kind == "impossible"
    # post-lesson: the WHY wall — the proof itself is not a store object
    rt_line72.turn(_lesson("gstest"))
    r = rt_line72.turn("explain why the gstest holds")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "not in my store" in ir["answer"]
    assert not (r.grounded or [])
    # and the drill-unable event landed on the concept
    unable = 0
    for a in live_store(rt_line72).query():
        if a.id.endswith(":drill-unable"):
            unable += 1
    assert unable >= 1


def test_power_growth_wall_carries_into_s5(rt_line72):
    # the S4 power wall re-probes STILL a wall on the S5 store
    r = rt_line72.turn("can you prove that for infinitely many n the unit pairs grow to a power above one?")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert GAP_ARTICULATION in ir["answer"]
    assert not (r.grounded or [])


def test_script_hash_and_store_decomposition():
    # the frozen script's identity is a function of the script alone
    import hashlib
    import json

    assert SCRIPT_HASH == hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    total = sum(len(v) for v in FROZEN["script"].values())
    assert total == FROZEN["total_turns"] == 65
    # the frozen decomposition: 523 seed + 52 facts + 61 events = 636
    assert FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"] == FROZEN["final_total"]
    # all sixteen canonical statements carry a line crosswalk (P0(b))
    for slug, meta in _LESSON_META_S5.items():
        assert meta["source_lines"], slug
    # all sixteen lesson phrases are byte-present in the frozen script
    all_surface = [t for s in FROZEN["script"].values() for t in s]
    for slug, meta in _LESSON_META_S5.items():
        assert meta["statement"] in all_surface, slug
    # the sixteen S5 concepts: exactly the seam slugs' owners
    assert len(S5_LESSONS) == 16
