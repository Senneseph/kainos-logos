"""Unit tests for E6.8 (SAVANT-TRACK S4: the unit-distance problem
band, with the theorem/lemma seam). The full 61-turn band is the
experiment (e68.py); these pin the mechanism: the ten savant
concepts, the seam facts (lemma/conjecture as store data), the eight
grammar families, the CONJECTURE-NEVER-A-PREMISE invariance, and the
measured walls (power-growth not-yet-taught; 7x7 off the line)."""

from __future__ import annotations

import pytest

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT4,
    det_classify,
)
from kainos.tutor.e67 import CONCEPTS_E67
from kainos.tutor.e68 import (
    ANS_OPEN,
    ANS_PROVEN,
    CONCEPTS_E68,
    CONF_ANS,
    FROZEN,
    GAP_ARTICULATION,
    SCRIPT_HASH,
    ST_ERDOS,
    ST_FLATAREA,
    ST_KST,
)
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime


@pytest.fixture()
def rt_line72(tmp_path):
    """The S4 band's real line (0..72, the e6.7 line end) with the
    full S4 concept registry."""

    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS_E68))
    runtime.boot(1)
    for n in range(72):
        runtime.turn(f"after {n} comes {n + 1}")
    return runtime


def test_savant1_implemented_in_the_band_map():
    b = band_by_name("savant-1")
    assert b.status == "implemented"
    assert b.evidence == ("e6.8",)
    assert set(b.concepts) == {c.id for c in CONCEPT_SAVANT4}
    assert band_by_name("savant-4").status == "implemented"  # official with e6.11 (S7: the savant test proper)
    assert band_by_name("savant-4").evidence == ("e6.11",)
    # savant-2 (the number-field toolkit) is official with e6.9
    b5 = band_by_name("savant-2")
    assert b5.status == "implemented"
    assert b5.evidence == ("e6.9",)
    from kainos.tutor.brainstem import CONCEPT_SAVANT5

    assert set(b5.concepts) == {c.id for c in CONCEPT_SAVANT5}


def test_concepts_e68_carry_the_savant_band():
    ids = [c.id for c in CONCEPTS_E68]
    assert len(CONCEPTS_E68) == len(CONCEPTS_E67) + 10
    for cid in (cid for c in CONCEPT_SAVANT4 for cid in (c.id,)):
        assert cid in ids
    # the prereq edges are declared (kst-bound rides on circle-pair-2;
    # grid-lattice / erdos-conj / the three norm confounders ride the
    # unit-distance quantity)
    by_id = {c.id: c for c in CONCEPTS_E68}
    assert by_id["kst-bound"].prereqs == ("circle-pair-2",)
    assert by_id["grid-lattice"].prereqs == ("unit-distance",)
    assert by_id["erdos-conj"].prereqs == ("unit-distance",)
    assert by_id["norm-flat"].prereqs == ("unit-distance",)
    assert by_id["norm-convex"].prereqs == ("unit-distance",)
    assert by_id["norm-generic"].prereqs == ("unit-distance",)
    # the band-1..3 concepts are untouched by the sweep
    assert all(any(c.id == old_id for c in CONCEPTS_E68) for old_id in (c.id for c in CONCEPTS_E67))


def test_grammar_the_savant_families():
    assert det_classify("state the unitpairs rule") == ("question", {"mode": "lem-state", "slug": "unitpairs"})
    assert det_classify("state the kstbound rule") == ("question", {"mode": "lem-state", "slug": "kstbound"})
    assert det_classify("what is the griddiag for") == ("question", {"mode": "lem-why", "slug": "griddiag"})
    assert det_classify("what is the status of the erdosguess?") == ("question", {"mode": "conj-state", "proven": False})
    assert det_classify("is the erdosguess proven?") == ("question", {"mode": "conj-state", "proven": True})
    assert det_classify("how many unit pairs does the 3 by 3 grid have?") == (
        "question",
        {"mode": "grid-pairs", "a": 3, "b": 3},
    )
    assert det_classify("in how many ways is 25 a sum of two squares?") == ("question", {"mode": "twosq", "n": 25})
    assert det_classify("unit circles whose centers are 1 over and 1 across: how many meeting points?") == (
        "question",
        {"mode": "circle-pairs", "x": 1, "y": 1},
    )
    assert det_classify("does the flatarea rule disprove the erdosguess?") == (
        "question",
        {"mode": "confounder-no", "slug": "flatarea"},
    )
    assert det_classify("can you prove that for infinitely many n the unit pairs grow to a power above one?") == (
        "question",
        {"mode": "savant-wall"},
    )


def test_grammar_no_collision_with_old_families():
    # an unknown slug must NOT classify as a savant probe
    assert det_classify("state the frobnicate rule")[1].get("mode") != "lem-state"
    assert det_classify("does the frobnicate rule disprove the erdosguess?")[1].get("mode") != "confounder-no"
    # the band-3 geometry grammar is untouched by the seam
    assert det_classify("what is the area of a 6 by 4 rectangle?")[1].get("mode") == "geo-area"


def live_store(rt):
    """The brainstem's live codex store (no lapse needed)."""

    return rt._brainstem._codex


def test_lesson_writes_the_seam_fact_established(rt_line72):
    lesson = "the erdosguess is that for all large n the unit pairs among any n points are at most n to the power one plus c over log log n, for an absolute constant c"
    r1 = rt_line72.turn(lesson)
    assert r1.kind == "assertion"
    assert "conjecture:erdosguess" in (r1.memory_diff or [])
    # re-teaching is a corroboration (no duplicate fact)
    r2 = rt_line72.turn(lesson)
    assert not (r2.memory_diff or [])
    # the fact: established, declared-source, conjecture_status=open

    store = live_store(rt_line72)
    fact = None
    for a in store.query():
        if a.id == "conjecture:erdosguess":
            fact = a
            break
    assert fact is not None
    assert fact.object == ST_ERDOS
    assert fact.context.data["kind"] == "conjecture"
    assert fact.context.data["source_role"] == "declared-source"
    assert fact.context.data["conjecture_status"] == "open"
    assert fact.context.data["source_lines"]


def test_state_why_exact_after_lesson(rt_line72):
    rt_line72.turn("the number of unit pairs of a point set is the count of the pairs of its points that are exactly one apart")
    r = rt_line72.turn("state the unitpairs rule")
    assert r.kind == "question"
    assert (r.response_ir or {}).get("answer").startswith("the number of unit pairs of a point set")
    assert (r.response_ir or {}).get("uncertainty_state") == "derived"
    assert "lemma:unitpairs" in (r.grounded or [])
    w = rt_line72.turn("what is the unitpairs for")
    assert "it names the quantity this whole course counts" == (w.response_ir or {}).get("answer")
    assert (w.response_text or "").startswith("it is for this: ")


def test_pre_lesson_probes_are_honest_gaps(rt_line72):
    for probe in (
        "state the unitpairs rule",
        "in how many ways is 25 a sum of two squares?",
        "unit circles whose centers are 1 over and 1 across: how many meeting points?",
        "what is the status of the erdosguess?",
        "how many unit pairs does the 3 by 3 grid have?",
        "does the flatarea rule disprove the erdosguess?",
    ):
        r = rt_line72.turn(probe)
        assert r.kind == "impossible", probe
        assert GAP_ARTICULATION in (r.response_text or "")
        assert not (r.grounded or [])
        assert not (r.memory_diff or [])


def test_conj_status_open_and_never_a_premise(rt_line72):
    rt_line72.turn(
        "the erdosguess is that for all large n the unit pairs among any n points are at most n to the power one plus c over log log n, for an absolute constant c"
    )
    r = rt_line72.turn("what is the status of the erdosguess?")
    assert (r.response_ir or {}).get("answer") == ANS_OPEN
    assert "conjecture:erdosguess" in ((r.response_ir or {}).get("evidence") or [])
    # the conjecture is a STATUS surface: never in `grounded`
    assert "conjecture:erdosguess" not in (r.grounded or [])
    rp = rt_line72.turn("is the erdosguess proven?")
    assert (rp.response_ir or {}).get("answer") == ANS_PROVEN
    # the derivation turns never cite the conjecture as a premise
    rt_line72.turn("the products of numbers that are sums of two squares are sums of two squares in many ways")
    rt_line72.turn("in how many ways is 25 a sum of two squares?")
    rt_line72.turn("among the points of an integer grid the unit pairs are exactly the horizontal and vertical neighbor pairs, for a diagonal step is never exactly one apart")
    r12 = rt_line72.turn("how many unit pairs does the 3 by 3 grid have?")
    assert "12" == (r12.response_ir or {}).get("answer")
    assert "conjecture:erdosguess" not in (r12.grounded or [])


def test_grid_twosq_circle_on_the_line(rt_line72):
    # grid: the on-line counts exact, the off-line wall honest
    rt_line72.turn("among the points of an integer grid the unit pairs are exactly the horizontal and vertical neighbor pairs, for a diagonal step is never exactly one apart")
    assert "12" == (rt_line72.turn("how many unit pairs does the 3 by 3 grid have?").response_ir or {}).get("answer")
    assert "24" == (rt_line72.turn("how many unit pairs does the 4 by 4 grid have?").response_ir or {}).get("answer")
    assert "60" == (rt_line72.turn("how many unit pairs does the 6 by 6 grid have?").response_ir or {}).get("answer")
    w = rt_line72.turn("how many unit pairs does the 7 by 7 grid have?")
    ir = w.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "84" in ir["answer"] and "72" in ir["answer"]
    ns = rt_line72.turn("how many unit pairs does the 3 by 4 grid have?")
    assert (ns.response_ir or {}).get("uncertainty_state") == "needs_info"
    # two-square counts (ordered pairs, verified on the line)
    rt_line72.turn("the products of numbers that are sums of two squares are sums of two squares in many ways")
    assert "4" == (rt_line72.turn("in how many ways is 25 a sum of two squares?").response_ir or {}).get("answer")
    assert "3" == (rt_line72.turn("in how many ways is 50 a sum of two squares?").response_ir or {}).get("answer")
    assert "0" == (rt_line72.turn("in how many ways is 3 a sum of two squares?").response_ir or {}).get("answer")
    # circle meetings by the d2 rule
    rt_line72.turn(
        "two unit circles with different centers meet in two points when the squared distance between the centers is below four, in exactly one point when it is four, and in no point when it is above four"
    )
    assert "2" == (rt_line72.turn("unit circles whose centers are 1 over and 1 across: how many meeting points?").response_ir or {}).get("answer")
    assert "1" == (rt_line72.turn("unit circles whose centers are 2 over and 0 across: how many meeting points?").response_ir or {}).get("answer")
    assert "0" == (rt_line72.turn("unit circles whose centers are 1 over and 2 across: how many meeting points?").response_ir or {}).get("answer")
    same = rt_line72.turn("unit circles whose centers are 0 over and 0 across: how many meeting points?")
    assert (same.response_ir or {}).get("uncertainty_state") == "needs_info"


def test_confounders_true_but_irrelevant(rt_line72):
    rt_line72.turn(ST_FLATAREA)
    r = rt_line72.turn("does the flatarea rule disprove the erdosguess?")
    assert (r.response_ir or {}).get("answer") == CONF_ANS["flatarea"]
    assert (r.response_ir or {}).get("uncertainty_state") == "derived"
    assert "lemma:flatarea" in (r.grounded or [])
    # and the stored confounder lemma is declared-source

    fact = None
    for a in live_store(rt_line72).query():
        if a.id == "lemma:flatarea":
            fact = a
            break
    assert fact is not None and fact.context.data["source_role"] == "declared-source"


def test_power_growth_probe_is_the_honest_wall(rt_line72):
    r = rt_line72.turn("can you prove that for infinitely many n the unit pairs grow to a power above one?")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert GAP_ARTICULATION in ir["answer"]
    assert not (r.grounded or [])
    # the wall holds even AFTER the band is fully taught (the leap is
    # S6's, not S4's)
    for lesson in (
        "the number of unit pairs of a point set is the count of the pairs of its points that are exactly one apart",
        "the erdosguess is that for all large n the unit pairs among any n points are at most n to the power one plus c over log log n, for an absolute constant c",
        "the products of numbers that are sums of two squares are sums of two squares in many ways",
    ):
        rt_line72.turn(lesson)
    r2 = rt_line72.turn("can you prove that for infinitely many n the unit pairs grow to a power above one?")
    assert (r2.response_ir or {})["uncertainty_state"] == "needs_info"
    assert GAP_ARTICULATION in (r2.response_ir or {})["answer"]
    assert not (r2.grounded or [])


def test_kst_lesson_and_state(rt_line72):
    rt_line72.turn(
        "two unit circles with different centers meet in two points when the squared distance between the centers is below four, in exactly one point when it is four, and in no point when it is above four"
    )
    rt_line72.turn(
        "because two unit circles meet in at most two points the unit pair graph of a planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs at a constant times n to the three halves power"
    )
    r = rt_line72.turn("state the kstbound rule")
    assert (r.response_ir or {}).get("answer") == ST_KST
    assert "lemma:kstbound" in (r.grounded or [])


def test_script_hash_is_stable():
    # the frozen script's identity is a function of the script alone
    import hashlib
    import json

    assert SCRIPT_HASH == hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    total = sum(len(v) for v in FROZEN["script"].values())
    assert total == FROZEN["total_turns"] == 61
