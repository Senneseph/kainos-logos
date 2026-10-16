"""Unit tests for E6.11 (SAVANT-TRACK S7: the arithmetical half
"tower => disproof" — THE SAVANT TEST PROPER). The full 75-turn band
is the experiment (e611.py); these pin the mechanism: the five savant
S7 concepts, the seven tower seam lemmas + six theorem compositions,
the gsslack beds on the UNCHANGED 0..84 line ((9,3) +9, (9,7) no
slack, (10,3) the 100 off-line wall), the conjecture flip (M8: the
store-mediated upsert open -> falsified, by theorem:theorem-main,
grounded empty — a status surface, never a premise), the Stage B
reconstruction (the M-chain in evidence), the confounder route (a
normed-plane fact does not construct), and the power probe's THIRD
state (the unconditional yes, grounded on theorem-main + the chain)."""

from __future__ import annotations

import pytest

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT7,
    S7_LESSONS,
    S7_THEOREMS,
    det_classify,
)
from kainos.tutor.e610 import CONCEPTS_E610
from kainos.tutor.e611 import (
    _LESSON_META_S7,
    _THEOREM_META_S7,
    CONCEPTS_E611,
    FROZEN,
    GAP_ARTICULATION,
    SCRIPT_HASH,
    _resolve_seed,
    _st7,
    _th7,
)
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime


@pytest.fixture()
def rt_s7(tmp_path):
    """The S7 band's real store: the OFFICIAL e6.10 S6 seed (734
    assertions, line 84) with the full S7 concept registry (session 2
    live). The line STAYS 0..84 (S7 adds no successor facts)."""

    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS_E611))
    seed = _resolve_seed()
    assert seed.exists(), f"the official e6.10 seed store is missing: {seed}"
    (tmp_path / "codeX-S01.json").write_bytes(seed.read_bytes())
    runtime.boot(2)
    return runtime


def _lesson7(slug: str) -> str:
    return _LESSON_META_S7[slug]["statement"]


def _teach_s7(runtime):
    """Teach all seven S7 tower lessons, then run the six sanctioned
    derives in DAG order (the full arithmetical half up to
    theorem-main — the flip is NOT part of the chain)."""

    for slug in (
        "tower-base",
        "tower-unramified",
        "base-rd",
        "chebotarev-selection",
        "k-3t",
        "class-tower",
        "slack-quadratic",
    ):
        runtime.turn(_lesson7(slug))
    runtime.turn("derive gen-lower from tower-unramified and fratin")
    runtime.turn("derive gs-infinite from shafbound, fratin, k-3t, gstest and slack-quadratic")
    runtime.turn("derive splitting from gs-infinite and chebotarev-selection")
    runtime.turn("derive gamma-achieved from class-tower, chebotarev-selection, slack-quadratic and gamma-positive")
    runtime.turn(
        "derive tower-feeds from gs-infinite, splitting, class-tower, "
        "gamma-achieved, hypo-infinity and gamma-positive"
    )
    runtime.turn("derive theorem-main from tower-feeds and infinity-end")


def test_savant4_implemented_in_the_band_map():
    b = band_by_name("savant-4")
    assert b.status == "implemented"
    assert b.evidence == ("e6.11",)
    assert set(b.concepts) == {c.id for c in CONCEPT_SAVANT7}


def test_concepts_e611_carry_the_savant_band():
    ids = [c.id for c in CONCEPTS_E611]
    assert len(CONCEPTS_E611) == len(CONCEPTS_E610) + 5
    for c in CONCEPT_SAVANT7:
        assert c.id in ids
    by_id = {c.id: c for c in CONCEPTS_E611}
    assert by_id["tower-base"].prereqs == ("cyclotomic-cubic", "char-cutout")
    assert by_id["tower-group"].prereqs == ("tower-base", "frattini", "golod-shaf", "shafarevich")
    assert by_id["tower-primes"].prereqs == ("tower-base", "chebotarev", "mod4-split")
    assert by_id["tower-class"].prereqs == ("tower-base", "class-bound", "adjoin-i", "slack-margins")
    assert by_id["disproof"].prereqs == ("criterion-chain", "tower-group", "tower-primes", "tower-class")


def test_grammar_the_sav7_families():
    assert det_classify("what is the gs slack for 9 generators and 3 split primes?") == (
        "question",
        {"mode": "gsslack", "d": 9, "t": 3},
    )
    assert det_classify("falsify the erdosguess by theorem-main") == (
        "question",
        {"mode": "conj-flip", "theorem": "theorem-main"},
    )
    assert det_classify("reconstruct the disproof from the erdosguess") == ("question", {"mode": "showdisproof"})
    assert det_classify("does the convexnorm route construct more unit distances in the euclidean plane?") == (
        "question",
        {"mode": "confounder-route", "slug": "convexnorm"},
    )
    assert det_classify("what is the exact value of delta?") == ("question", {"mode": "delta-value"})
    assert det_classify("what is the tight bound for distinct distances in the plane?") == ("question", {"mode": "distdist"})
    assert det_classify("state the tower-feeds rule") == ("question", {"mode": "s7-state", "slug": "tower-feeds"})
    assert det_classify("what is the k-3t for") == ("question", {"mode": "s7-why", "slug": "k-3t"})
    assert det_classify("explain why the gs-infinite holds") == ("question", {"mode": "s7-whydeep", "slug": "gs-infinite"})
    # the S7 derive targets classify on the unified table
    assert det_classify("derive theorem-main from tower-feeds and infinity-end") == (
        "question",
        {"mode": "derive", "target": "theorem-main", "parts": ("tower-feeds", "infinity-end")},
    )
    # a lesson surface is a bare canonical statement (the assertion path)
    assert det_classify(_lesson7("k-3t")) == ("assertion", {"lemma": _lesson7("k-3t")})


def test_grammar_no_collision_with_old_families():
    # an unknown slug must NOT classify as an S7 state/whydeep probe
    assert det_classify("state the frobnicate rule")[1].get("mode") != "s7-state"
    assert det_classify("explain why the frobnicate holds")[1].get("mode") != "s7-whydeep"
    # S5's `chebot` slug is not S7's `chebotarev-selection`, and
    # S6's `slack-compose-rule` is not S7's `slack-quadratic`
    assert det_classify("state the chebot rule") == ("question", {"mode": "lem-state", "slug": "chebot"})
    assert det_classify("state the slack-compose-rule rule") == ("question", {"mode": "s6-state", "slug": "slack-compose-rule"})
    assert det_classify("state the slack-quadratic rule") == ("question", {"mode": "s7-state", "slug": "slack-quadratic"})
    # slack-margins is a CONCEPT id (no such fact slug): ambiguous, never S7
    assert det_classify("state the slack-margins rule")[1].get("mode") != "s7-state"
    # the S4 confounder surface is untouched (the S7 one says `route construct`)
    assert det_classify("does the flatarea rule disprove the erdosguess?") == (
        "question",
        {"mode": "confounder-no", "slug": "flatarea"},
    )
    assert det_classify("what is the status of the erdosguess?") == (
        "question",
        {"mode": "conj-state", "proven": False},
    )


def live_store(rt):
    """The brainstem's live codex store (no lapse needed)."""

    return rt._brainstem._codex


def test_lesson_writes_the_seam_fact_established(rt_s7):
    r1 = rt_s7.turn(_lesson7("class-tower"))
    assert r1.kind == "assertion"
    assert "lemma:class-tower" in (r1.memory_diff or [])
    # re-teaching is a corroboration (no duplicate fact)
    r2 = rt_s7.turn(_lesson7("class-tower"))
    assert not (r2.memory_diff or [])
    store = live_store(rt_s7)
    fact = None
    for a in store.query():
        if a.id == "lemma:class-tower":
            fact = a
            break
    assert fact is not None
    assert fact.object == _st7("class-tower")
    assert fact.context.data["kind"] == "lemma"
    assert fact.context.data["source_role"] == "declared-source"
    assert fact.context.data["source_lines"]


def test_pre_lesson_state_is_the_honest_gap(rt_s7):
    r = rt_s7.turn("state the tower-base rule")
    assert r.kind == "impossible"
    assert GAP_ARTICULATION in (r.response_text or "")
    assert not (r.memory_diff or [])
    assert not (r.grounded or [])


def test_derive_missing_parts_is_a_typed_failure(rt_s7):
    # k-3t and slack-quadratic are untaught in the S6 seed
    r = rt_s7.turn("derive gs-infinite from shafbound, fratin, k-3t, gstest and slack-quadratic")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "i have not been taught" in ir["answer"]
    assert "k-3t" in ir["answer"] and "slack-quadratic" in ir["answer"]
    assert not (r.grounded or [])
    assert not (r.memory_diff or [])
    # the drill-unable event landed on the owning concept
    unable = [a for a in live_store(rt_s7).query() if "tower-group:ev-" in a.id and "drill-unable" in a.id]
    assert unable


def test_derive_success_stores_the_derived_theorem(rt_s7):
    rt_s7.turn(_lesson7("tower-unramified"))
    r = rt_s7.turn("derive gen-lower from tower-unramified and fratin")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    assert ir["answer"] == _th7("gen-lower")
    assert "theorem:gen-lower" in (r.memory_diff or [])
    assert "lemma:tower-unramified" in (r.grounded or [])
    assert "lemma:fratin" in (r.grounded or [])
    # the fact: infant-observed, derived provenance, derived_from parts
    store = live_store(rt_s7)
    fact = None
    for a in store.query():
        if a.id == "theorem:gen-lower":
            fact = a
            break
    assert fact is not None
    assert fact.object == _th7("gen-lower")
    assert fact.context.data["kind"] == "theorem"
    assert fact.provenance.observer == "infant"
    assert fact.provenance.derived is True
    assert fact.provenance.source is not None and fact.provenance.source.authority == "infant"
    assert fact.context.data.get("source_role") != "declared-source"
    assert tuple(fact.context.data["derived_from"]) == ("tower-unramified", "fratin")
    # a re-derive corroborates (no duplicate fact)
    r2 = rt_s7.turn("derive gen-lower from tower-unramified and fratin")
    assert not (r2.memory_diff or [])
    assert (r2.response_ir or {}).get("uncertainty_state") == "derived"


def test_gsslack_beds_and_wall(rt_s7):
    # (9,3): 81 - 36 - 36 = 9 — positive slack, grounded on the line
    p = rt_s7.turn("what is the gs slack for 9 generators and 3 split primes?")
    ir = p.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    assert ir["answer"].startswith("four times the slack is 9 — positive:")
    g = [str(x) for x in (p.grounded or [])]
    assert g, "the gs-slack bed must be grounded on the line"
    assert all(x.startswith("cs-") or x == "lemma:gstest" for x in g), "the gs-slack bed must cite only line facts + the gstest lemma"
    assert "lemma:gstest" in g
    # (9,7): 81 - 36 - 84 — the slack is negative; the line holds the
    # magnitude (39 below zero), not a negative number
    q = rt_s7.turn("what is the gs slack for 9 generators and 7 split primes?")
    irq = q.response_ir or {}
    assert irq["uncertainty_state"] == "derived"
    assert "39 below zero" in irq["answer"]
    assert "no slack at this size" in irq["answer"]
    # (10,3): d squared = 100 is OFF the 0..84 line (W-S7-1)
    w = rt_s7.turn("what is the gs slack for 10 generators and 3 split primes?")
    irw = w.response_ir or {}
    assert irw["uncertainty_state"] == "needs_info"
    assert "100" in irw["answer"] and "84" in irw["answer"]
    assert not (w.grounded or [])


def test_conj_state_is_store_mediated_and_open_in_seed(rt_s7):
    r = rt_s7.turn("what is the status of the erdosguess?")
    assert (r.response_ir or {}).get("answer") == "open — believed, not known"
    assert not (r.grounded or [])  # a status surface, never a premise


def test_conj_flip_requires_a_derived_theorem(rt_s7):
    # a declared lemma is not a theorem — the typed honest failure
    rt_s7.turn(_lesson7("tower-base"))
    r = rt_s7.turn("falsify the erdosguess by tower-base")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "not in my store as a derived theorem" in ir["answer"]
    assert not (r.memory_diff or [])


def test_conj_flip_is_the_m8_upsert(rt_s7):
    _teach_s7(rt_s7)
    r = rt_s7.turn("falsify the erdosguess by theorem-main")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    ev = [str(x) for x in (ir.get("evidence") or [])]
    assert "theorem:theorem-main" in ev and "conjecture:erdosguess" in ev
    assert not (r.grounded or [])  # never a premise
    assert "conjecture:erdosguess" in (r.memory_diff or [])  # the upsert
    # the store now says falsified, by the theorem, derived provenance
    store = live_store(rt_s7)
    conj = None
    for a in store.query():
        if a.id == "conjecture:erdosguess":
            conj = a
            break
    assert conj is not None
    assert conj.context.data["conjecture_status"] == "falsified"
    assert conj.context.data["by"] == "theorem:theorem-main"
    assert conj.provenance.derived is True
    assert conj.provenance.observer == "infant"
    # the status surfaces flip with the store
    rs = rt_s7.turn("what is the status of the erdosguess?")
    assert (rs.response_ir or {}).get("answer") == (
        "falsified by theorem:theorem-main — the tower beats its cap for infinitely many n"
    )
    rp = rt_s7.turn("is the erdosguess proven?")
    assert (rp.response_ir or {}).get("answer") == (
        "yes — it was falsified by theorem:theorem-main; the tower gives infinitely many n "
        "with the unit pairs at least n to the one plus delta"
    )
    # the flip event landed on the disproof concept
    asserts = [a for a in store.query() if "disproof:ev-" in a.id and "conjecture-falsified" in a.id]
    assert asserts
    # flipping twice is the typed already-falsified failure
    r2 = rt_s7.turn("falsify the erdosguess by theorem-main")
    ir2 = r2.response_ir or {}
    assert ir2["uncertainty_state"] == "needs_info"
    assert "already falsified" in ir2["answer"]
    assert not (r2.memory_diff or [])


def test_showdisproof_requires_the_chain_then_reconstructs(rt_s7):
    r0 = rt_s7.turn("reconstruct the disproof from the erdosguess")
    ir0 = r0.response_ir or {}
    assert ir0["uncertainty_state"] == "needs_info"
    assert "not yet in my store" in ir0["answer"]
    assert not (r0.memory_diff or [])
    _teach_s7(rt_s7)
    r = rt_s7.turn("reconstruct the disproof from the erdosguess")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    ev = [str(x) for x in (ir.get("evidence") or [])]
    assert ev == [
        "theorem:gs-infinite",
        "theorem:splitting",
        "theorem:gamma-achieved",
        "theorem:tower-feeds",
        "theorem:infinity-end",
        "theorem:theorem-main",
    ]
    assert [str(x) for x in (r.grounded or [])] == ev  # the M-chain, ordered


def test_power_probe_has_a_third_state(rt_s7):
    # on the S6 seed: the chain is C (hypotheses unestablished)
    r0 = rt_s7.turn("can you prove that for infinitely many n the unit pairs grow to a power above one?")
    ir0 = r0.response_ir or {}
    assert ir0["uncertainty_state"] == "conditional"
    assert not (r0.grounded or [])
    # after the full S7 chain: the UNCONDITIONAL yes (domain S)
    _teach_s7(rt_s7)
    r1 = rt_s7.turn("can you prove that for infinitely many n the unit pairs grow to a power above one?")
    ir1 = r1.response_ir or {}
    assert ir1["uncertainty_state"] == "derived"
    assert ir1["answer"].startswith("yes — i have put it together:")
    assert [str(x) for x in (r1.grounded or [])] == ["theorem:theorem-main", "theorem:tower-feeds"]


def test_confounder_route_does_not_construct(rt_s7):
    r = rt_s7.turn("does the convexnorm route construct more unit distances in the euclidean plane?")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    assert ir["answer"].startswith("no —")
    assert "not a construction" in ir["answer"]
    assert "lemma:convexnorm" in [str(x) for x in (r.grounded or [])]


def test_beyond_store_walls_are_honest(rt_s7):
    r1 = rt_s7.turn("what is the tight bound for distinct distances in the plane?")
    ir1 = r1.response_ir or {}
    assert ir1["uncertainty_state"] == "needs_info"
    assert "not been taught" in ir1["answer"]
    assert not (r1.grounded or [])
    r2 = rt_s7.turn("what is the exact value of delta?")
    ir2 = r2.response_ir or {}
    assert ir2["uncertainty_state"] == "needs_info"
    assert "not in my store" in ir2["answer"]
    assert not (r2.grounded or [])
    r3 = rt_s7.turn("name a concrete n for which the unit pairs exceed n to the 1 plus delta")
    ir3 = r3.response_ir or {}
    assert ir3["uncertainty_state"] == "needs_info"
    assert "not one instance number" in ir3["answer"]
    assert not (r3.grounded or [])


def test_why_split_is_mechanical_on_s7(rt_s7):
    # declared lemma: the proof wall (W-S7-6)
    rt_s7.turn(_lesson7("tower-unramified"))
    rw = rt_s7.turn("explain why the tower-unramified holds")
    irw = rw.response_ir or {}
    assert irw["uncertainty_state"] == "needs_info"
    assert "the proof of tower-unramified is not in my store" in irw["answer"]
    assert not (rw.grounded or [])
    # the why (essence) of a declared lemma is still served
    rte = rt_s7.turn("what is the tower-unramified for")
    assert (rte.response_ir or {}).get("uncertainty_state") == "derived"
    # derived theorem: the in-store chain
    rt_s7.turn(_lesson7("tower-base"))
    rt_s7.turn("derive gen-lower from tower-unramified and fratin")
    rc = rt_s7.turn("explain why the gen-lower holds")
    irc = rc.response_ir or {}
    assert irc["uncertainty_state"] == "derived"
    assert irc["answer"].startswith("i derived it from tower-unramified, fratin:")
    assert "theorem:gen-lower" not in (irc.get("evidence") or [])  # cites the PARTS


def test_script_hash_and_store_decomposition():
    # the frozen script's identity is a function of the script alone
    import hashlib
    import json

    assert SCRIPT_HASH == hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    total = sum(len(v) for v in FROZEN["script"].values())
    assert total == FROZEN["total_turns"] == 75
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 20
    assert len(FROZEN["script"][4]) == 30
    # the frozen decomposition: 734 seed + 35 facts + 71 events = 840
    # (one event id collides with the S5 seed — the D-e6w pattern;
    # the ACTUAL total is frozen, never the hand count)
    assert FROZEN["seed_total"] == 734
    assert FROZEN["new_facts"] == 35
    assert FROZEN["final_total"] == 840
    assert FROZEN["line_end_final"] == 84  # the line STAYS 0..84
    # all seven canonical statements carry a line crosswalk (P0(b))
    for slug, meta in _LESSON_META_S7.items():
        assert meta["source_lines"], slug
    # all six theorem compositions carry their sanctioned parts
    for slug, meta in _THEOREM_META_S7.items():
        assert meta["parts"], slug
    # the seven lesson phrases are byte-present in the frozen script
    all_surface = [t for s in FROZEN["script"].values() for t in s]
    for slug, meta in _LESSON_META_S7.items():
        assert meta["statement"] in all_surface, slug
    assert len(S7_LESSONS) == 7
    assert len(S7_THEOREMS) == 6
