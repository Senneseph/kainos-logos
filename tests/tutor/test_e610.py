"""Unit tests for E6.10 (SAVANT-TRACK S6: the geometric criterion
band — scaffolded generation, THE LEAP). The full 70-turn band is
the experiment (e610.py); these pin the mechanism: the six savant
S6 concepts, the ten seam facts + six theorem compositions, the
derive grammar (typed scaffold failures: missing parts / no rule),
the why-split (declared lemmas keep the proof wall; derived
theorems answer with the in-store chain), the beds on the extended
0..84 line (144/243/128 off-line walls), the show-one wall (limit
#3), and the store-mediated power probe (H before the chain, C
after it — the erdosguess stays open)."""

from __future__ import annotations

import pytest

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT6,
    S6_LESSONS,
    S6_THEOREMS,
    det_classify,
)
from kainos.tutor.e69 import CONCEPTS_E69
from kainos.tutor.e610 import (
    _LESSON_META_S6,
    _THEOREM_META_S6,
    CONCEPTS_E610,
    FROZEN,
    GAP_ARTICULATION,
    SCRIPT_HASH,
    _resolve_seed,
    _st6,
    _th,
)
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime


@pytest.fixture()
def rt_s6(tmp_path):
    """The S6 band's real store: the OFFICIAL e6.9 S5 seed (636
    assertions, line 72) extended to the declared 0..84 line, with
    the full S6 concept registry (session 2 live)."""

    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS_E610))
    seed = _resolve_seed()
    assert seed.exists(), f"the official e6.9 seed store is missing: {seed}"
    (tmp_path / "codeX-S01.json").write_bytes(seed.read_bytes())
    runtime.boot(2)
    for n in range(72, 84):
        runtime.turn(f"after {n} comes {n + 1}")
    return runtime


def _lesson6(slug: str) -> str:
    return _LESSON_META_S6[slug]["statement"]


def _teach_chain(runtime):
    """Teach all ten S6 part lessons, then run the six sanctioned
    derives in DAG order (the full criterion)."""

    for slug in (
        "normonecount",
        "gamma-positive",
        "overlap-ratio",
        "torus-average",
        "one-embed-zero",
        "denom-d",
        "vol-compare",
        "b-positive",
        "slack-compose-rule",
        "hypo-infinity",
    ):
        runtime.turn(_lesson6(slug))
    for target in S6_THEOREMS:
        parts = ", ".join(S6_THEOREMS[target]["parts"])
        runtime.turn(f"derive {target} from {parts}")


def test_savant3_implemented_in_the_band_map():
    b = band_by_name("savant-3")
    assert b.status == "implemented"
    assert b.evidence == ("e6.10",)
    assert set(b.concepts) == {c.id for c in CONCEPT_SAVANT6}
    assert band_by_name("savant-4").status == "implemented"  # official with e6.11 (S7: the savant test proper)
    assert band_by_name("savant-4").evidence == ("e6.11",)


def test_concepts_e610_carry_the_savant_band():
    ids = [c.id for c in CONCEPTS_E610]
    assert len(CONCEPTS_E610) == len(CONCEPTS_E69) + 6
    for c in CONCEPT_SAVANT6:
        assert c.id in ids
    by_id = {c.id: c for c in CONCEPTS_E610}
    assert by_id["window-setup"].prereqs == ("minkowski-embed", "cm-conj")
    assert by_id["averaging"].prereqs == ("window-setup",)
    assert by_id["projection"].prereqs == ("window-setup",)
    assert by_id["packing"].prereqs == ("window-setup", "number-field")
    assert by_id["slack-margins"].prereqs == ("packing",)
    assert by_id["criterion-chain"].prereqs == (
        "averaging",
        "projection",
        "packing",
        "slack-margins",
    )


def test_grammar_the_sav6_families():
    assert det_classify("derive window-rich from normonecount, overlap-ratio and torus-average") == (
        "question",
        {"mode": "derive", "target": "window-rich", "parts": ("normonecount", "overlap-ratio", "torus-average")},
    )
    assert det_classify("derive pack-bound from numberfields, denom-d, vol-compare and b-positive") == (
        "question",
        {"mode": "derive", "target": "pack-bound", "parts": ("numberfields", "denom-d", "vol-compare", "b-positive")},
    )
    assert det_classify("how many points does the packing bound allow when the outer radius is 2 times the inner?") == (
        "question",
        {"mode": "packcount", "k": 2},
    )
    assert det_classify("how large is three raised to the 4?") == ("question", {"mode": "tripow", "e": 4})
    assert det_classify("name a concrete n for which the unit pairs exceed n to the 1 plus delta") == (
        "question",
        {"mode": "showone"},
    )
    assert det_classify("state the torus-average rule") == ("question", {"mode": "s6-state", "slug": "torus-average"})
    assert det_classify("explain why the infinity-end holds") == ("question", {"mode": "s6-whydeep", "slug": "infinity-end"})
    # a lesson surface is a bare canonical statement (the assertion path)
    assert det_classify(_lesson6("normonecount")) == ("assertion", {"lemma": _lesson6("normonecount")})


def test_grammar_no_collision_with_old_families():
    # an unknown slug must NOT classify as an S6 state/whydeep probe
    assert det_classify("state the frobnicate rule")[1].get("mode") != "s6-state"
    assert det_classify("explain why the frobnicate holds")[1].get("mode") != "s6-whydeep"
    # the S4/S5 families are untouched by the seam growth
    assert det_classify("what is the status of the erdosguess?") == (
        "question",
        {"mode": "conj-state", "proven": False},
    )
    assert det_classify("does 2 squared plus one vanish modulo 5?") == ("question", {"mode": "sqmod", "x": 2, "q": 5})


def live_store(rt):
    """The brainstem's live codex store (no lapse needed)."""

    return rt._brainstem._codex


def test_lesson_writes_the_seam_fact_established(rt_s6):
    r1 = rt_s6.turn(_lesson6("vol-compare"))
    assert r1.kind == "assertion"
    assert "lemma:vol-compare" in (r1.memory_diff or [])
    # re-teaching is a corroboration (no duplicate fact)
    r2 = rt_s6.turn(_lesson6("vol-compare"))
    assert not (r2.memory_diff or [])
    store = live_store(rt_s6)
    fact = None
    for a in store.query():
        if a.id == "lemma:vol-compare":
            fact = a
            break
    assert fact is not None
    assert fact.object == _st6("vol-compare")
    assert fact.context.data["kind"] == "lemma"
    assert fact.context.data["source_role"] == "declared-source"
    assert fact.context.data["source_lines"]


def test_derive_missing_parts_is_a_typed_failure(rt_s6):
    # both window-rich and one-embed-zero are untaught in the seed
    r = rt_s6.turn("derive proj-inj from minkembed, one-embed-zero and window-rich")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "i have not been taught" in ir["answer"]
    assert not (r.grounded or [])
    assert not (r.memory_diff or [])
    # and the drill-unable event landed on the owning concept
    unable = [a for a in live_store(rt_s6).query() if "drill-unable" in a.id]
    assert unable


def test_no_rule_derive_is_honest(rt_s6):
    # b-positive is a given from a source, not a sanctioned target
    r = rt_s6.turn("derive b-positive from slack-compose-rule and window-rich")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "not a derivation i have been taught" in ir["answer"]
    assert not (r.memory_diff or [])


def test_derive_success_stores_the_derived_theorem(rt_s6):
    for slug in ("normonecount", "overlap-ratio", "torus-average"):
        rt_s6.turn(_lesson6(slug))
    r = rt_s6.turn("derive window-rich from normonecount, overlap-ratio and torus-average")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    assert ir["answer"] == _th("window-rich")
    assert "theorem:window-rich" in (r.memory_diff or [])
    assert "lemma:normonecount" in (r.grounded or [])
    assert "lemma:overlap-ratio" in (r.grounded or [])
    assert "lemma:torus-average" in (r.grounded or [])
    # the fact: infant-observed, NO source, derived_from the parts
    store = live_store(rt_s6)
    fact = None
    for a in store.query():
        if a.id == "theorem:window-rich":
            fact = a
            break
    assert fact is not None
    assert fact.object == _th("window-rich")
    assert fact.context.data["kind"] == "theorem"
    assert fact.provenance.observer == "infant"
    assert fact.provenance.derived is True
    assert fact.provenance.source is not None and fact.provenance.source.authority == "infant"
    assert fact.context.data.get("source_role") != "declared-source"
    assert tuple(fact.context.data["derived_from"]) == (
        "normonecount",
        "overlap-ratio",
        "torus-average",
    )
    # a re-derive corroborates (no duplicate fact)
    r2 = rt_s6.turn("derive window-rich from normonecount, overlap-ratio and torus-average")
    assert not (r2.memory_diff or [])
    assert (r2.response_ir or {}).get("uncertainty_state") == "derived"


def test_packcount_beds_and_wall(rt_s6):
    # before the pack-bound theorem exists: the honest U gap
    r0 = rt_s6.turn("how many points does the packing bound allow when the outer radius is 1 times the inner?")
    assert r0.kind == "impossible"
    assert GAP_ARTICULATION in (r0.response_text or "")
    # teach the parts and derive the theorem
    for slug in ("denom-d", "vol-compare", "b-positive"):
        rt_s6.turn(_lesson6(slug))
    rt_s6.turn("derive pack-bound from numberfields, denom-d, vol-compare and b-positive")
    p1 = rt_s6.turn("how many points does the packing bound allow when the outer radius is 1 times the inner?")
    assert (p1.response_ir or {}).get("answer") == "16"
    p2 = rt_s6.turn("how many points does the packing bound allow when the outer radius is 2 times the inner?")
    assert (p2.response_ir or {}).get("answer") == "64"  # = duopow 6 (one number, two beds)
    for r in (p1, p2):
        assert (r.response_ir or {}).get("uncertainty_state") == "derived"
        g = [str(x) for x in (r.grounded or [])]
        assert g, "the pack bed must be grounded on the line"
        assert all(x.startswith("cs-") or x == "theorem:pack-bound" for x in g), "the pack bed must cite only line facts + its theorem"
        assert "theorem:pack-bound" in g, "the pack bed must cite its owning theorem"
    # k = 3: (4*3)^2 = 144 is OFF the 0..84 line (the wall)
    p3 = rt_s6.turn("how many points does the packing bound allow when the outer radius is 3 times the inner?")
    ir = p3.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "144" in ir["answer"] and "84" in ir["answer"]
    assert not (p3.grounded or [])


def test_tripow_beds_and_wall(rt_s6):
    t4 = rt_s6.turn("how large is three raised to the 4?")
    assert (t4.response_ir or {}).get("answer") == "81"
    assert (t4.response_ir or {}).get("uncertainty_state") == "derived"
    g4 = [str(x) for x in (t4.grounded or [])]
    assert g4, "the tripow bed must be grounded on the line"
    assert all(x.startswith("cs-") for x in g4), "the tripow bed must cite only line facts"
    # it must cite the EXTENDED successor fact (81 > the S5 line end 72)
    store = live_store(rt_s6)
    fact81 = None
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        if a.object_id == "count-successor:num(81)":
            fact81 = a
            break
    assert fact81 is not None, "the extended successor fact num(81) is not in the store"
    assert fact81.id in g4, "the tripow bed did not cite the extended successor fact 81"
    t5 = rt_s6.turn("how large is three raised to the 5?")
    ir = t5.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "243" in ir["answer"] and "84" in ir["answer"]
    assert not (t5.grounded or [])


def test_showone_is_the_honest_wall(rt_s6):
    r = rt_s6.turn("name a concrete n for which the unit pairs exceed n to the 1 plus delta")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert "not one instance number" in ir["answer"]
    assert not (r.grounded or [])


def test_theorem_whydeep_is_the_chain_and_lemma_is_the_wall(rt_s6):
    # pre-lesson theorem: the honest not-yet-learned gap
    r0 = rt_s6.turn("explain why the proj-inj holds")
    assert r0.kind == "impossible"
    # the declared lemma keeps the S5 proof wall (W-S6-6)
    rt_s6.turn(_lesson6("b-positive"))
    rw = rt_s6.turn("explain why the b-positive holds")
    irw = rw.response_ir or {}
    assert irw["uncertainty_state"] == "needs_info"
    assert "the proof of b-positive is not in my store" in irw["answer"]
    assert not (rw.grounded or [])
    # the derived theorem answers with the in-store chain
    for slug in ("normonecount", "overlap-ratio", "torus-average", "one-embed-zero"):
        rt_s6.turn(_lesson6(slug))
    rt_s6.turn("derive window-rich from normonecount, overlap-ratio and torus-average")
    rt_s6.turn("derive proj-inj from minkembed, one-embed-zero and window-rich")
    rc = rt_s6.turn("explain why the proj-inj holds")
    irc = rc.response_ir or {}
    assert irc["uncertainty_state"] == "derived"
    assert irc["answer"].startswith("i derived it from minkembed, one-embed-zero, window-rich:")
    assert "theorem:window-rich" in (rc.grounded or [])
    assert "lemma:minkembed" in (rc.grounded or [])


def test_savant_wall_is_store_mediated(rt_s6):
    # pre-chain: the SAME probe is the S4/S5 articulation (H)
    r0 = rt_s6.turn("can you prove that for infinitely many n the unit pairs grow to a power above one?")
    ir0 = r0.response_ir or {}
    assert ir0["uncertainty_state"] == "needs_info"
    assert GAP_ARTICULATION in ir0["answer"]
    assert not (r0.grounded or [])
    # the full chain in the store
    _teach_chain(rt_s6)
    r1 = rt_s6.turn("can you prove that for infinitely many n the unit pairs grow to a power above one?")
    ir1 = r1.response_ir or {}
    assert ir1["uncertainty_state"] == "conditional"
    assert ir1["answer"].startswith("conditionally i can")
    assert not (r1.grounded or [])  # the hypotheses are not established facts
    ev = [str(x) for x in (ir1.get("evidence") or [])]
    assert "theorem:infinity-end" in ev
    assert "hypotheses:unestablished" in ev
    # and the erdosguess is STILL open (the flip is S7's)
    rc = rt_s6.turn("what is the status of the erdosguess?")
    assert (rc.response_ir or {}).get("answer") == "open — believed, not known"
    rp = rt_s6.turn("is the erdosguess proven?")
    assert (rp.response_ir or {}).get("answer") == "no — the erdosguess is believed, not known; its status is open"


def test_script_hash_and_store_decomposition():
    # the frozen script's identity is a function of the script alone
    import hashlib
    import json

    assert SCRIPT_HASH == hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    total = sum(len(v) for v in FROZEN["script"].values())
    assert total == FROZEN["total_turns"] == 70
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 19
    assert len(FROZEN["script"][4]) == 26
    # the frozen decomposition: 636 seed + 45 facts + 66 events = 747
    assert FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"] == FROZEN["final_total"]
    # all ten canonical statements carry a line crosswalk (P0(b))
    for slug, meta in _LESSON_META_S6.items():
        assert meta["source_lines"], slug
    # all six theorem compositions carry their sanctioned parts
    for slug, meta in _THEOREM_META_S6.items():
        assert meta["parts"], slug
    # the ten lesson phrases + the twelve line lessons are byte-present
    all_surface = [t for s in FROZEN["script"].values() for t in s]
    for slug, meta in _LESSON_META_S6.items():
        assert meta["statement"] in all_surface, slug
    assert len(S6_LESSONS) == 10
    assert len(S6_THEOREMS) == 6
