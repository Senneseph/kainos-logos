"""Unit tests for E6.12 (RH-TRACK S8: the ζ apparatus — band 1 of 3).
The full 75-turn band is the experiment (e612.py); these pin the
mechanism: the nine RH concepts (zeta-series the no-prereq root),
the eleven declared seam lemmas + the riemann CONJECTURE (status
open, declared-source, the single M8 self-citation), the two
sanctioned compositions (reflect ← func-eq; strip ← reflect +
nozero-s1 + trivial-zeros), the grounded line censuses (π(84) = 23,
π(36) = 11, J(12) = 35, J(18) = 71 — no new assertions) versus the
off-line walls (J(84) = 1053, π(100) — the W-S7-1 pattern), the
attempt wall (the frozen probe line's terminal form), and the
confounder walls (directionality / scope / verification-not-proof /
open-question / value-tables)."""

from __future__ import annotations

import hashlib
import json

import pytest

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    S7_DENYLIST,
    S8_DENYLIST,
    S8_LESSONS,
    S8_THEOREMS,
    det_classify,
)
from kainos.tutor.e611 import CONCEPTS_E611
from kainos.tutor.e612 import (
    _LESSON_META_S8,
    _THEOREM_META_S8,
    CONCEPTS_E612,
    FROZEN,
    GAP_ARTICULATION,
    S8_CONCEPT_IDS,
    SCRIPT_HASH,
    _resolve_seed,
    _st8,
    _th8,
)
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime


@pytest.fixture()
def rt_s8(tmp_path):
    """The S8 band's real store: the OFFICIAL e6.11 S7 seed (840
    assertions, line 84) with the full S8 concept registry (session 2
    live). The line STAYS 0..84 (S8 adds no successor facts)."""

    reset_concepts()
    runtime = InfantRuntime(tmp_path, concepts=list(CONCEPTS_E612))
    seed = _resolve_seed()
    assert seed.exists(), f"the official e6.11 seed store is missing: {seed}"
    (tmp_path / "codeX-S01.json").write_bytes(seed.read_bytes())
    runtime.boot(2)
    return runtime


def _teach_s8(runtime):
    """Teach all twelve S8 seam facts (eleven lemmas + the
    conjecture), then run the two sanctioned derives in DAG order
    (reflect, then strip)."""

    for slug in (
        "zeta-series",
        "euler-product",
        "zeta-cont",
        "func-eq",
        "trivial-zeros",
        "nozero-s1",
        "von-mangoldt",
        "pnt",
        "rv-count",
        "s-of-t",
        "num-zeros",
        "riemann",
    ):
        runtime.turn(_st8(slug))
    runtime.turn("derive reflect from func-eq")
    runtime.turn("derive strip from reflect, nozero-s1 and trivial-zeros")


def live_store(rt):
    """The brainstem's live codex store (no lapse needed)."""

    return rt._brainstem._codex


def test_rh1_implemented_in_the_band_map():
    b = band_by_name("rh-1")
    assert b.status == "implemented"
    assert b.evidence == ("e6.12",)
    assert set(b.concepts) == set(S8_CONCEPT_IDS)
    assert band_by_name("rh-2").status == "implemented"  # official: e6.13 (the S9 flip)
    assert band_by_name("rh-3").status == "implemented"  # official: e6.14 (the S10 flip)


def test_concepts_e612_carry_the_rh_band():
    assert len(CONCEPTS_E612) == len(CONCEPTS_E611) + 9
    by_id = {c.id: c for c in CONCEPTS_E612}
    # zeta-series: the track root — NO prereqs (the mastery gate that
    # lets it stabilize first)
    assert by_id["zeta-series"].prereqs == ()
    assert by_id["zeta-cont"].prereqs == ("zeta-series",)
    assert by_id["func-eq"].prereqs == ("zeta-cont",)
    assert by_id["critical-strip"].prereqs == ("func-eq",)
    assert by_id["prime-count"].prereqs == ("zeta-series",)
    assert by_id["pnt"].prereqs == ("prime-count",)
    assert by_id["rv-count"].prereqs == ("zeta-cont",)
    assert by_id["s-of-t"].prereqs == ("rv-count", "func-eq")
    assert by_id["riemann"].prereqs == ("critical-strip", "rv-count")


def test_grammar_the_s8_families():
    assert det_classify("how many primes are at most 84?") == (
        "question",
        {"mode": "pi-count", "n": 84},
    )
    assert det_classify("how many primes are at most 100?") == (
        "question",
        {"mode": "pi-count", "n": 100},
    )
    assert det_classify("what is the prime-power phi count at 12?") == (
        "question",
        {"mode": "jfunc", "n": 12},
    )
    assert det_classify("does the sine vanish at every integer multiple of pi from one to 84?") == (
        "question",
        {"mode": "sincycle"},
    )
    assert det_classify("what is the expected growth of the prime-power phi count?") == (
        "question",
        {"mode": "growth-claim"},
    )
    assert det_classify("what is the height of the first nontrivial zero?") == (
        "question",
        {"mode": "numzero-first"},
    )
    assert det_classify("can you derive the riemann hypothesis from the store?") == (
        "question",
        {"mode": "rh-attempt"},
    )
    assert det_classify("what is the status of the riemann hypothesis?") == (
        "question",
        {"mode": "rh-conj-state"},
    )
    assert det_classify(
        "does the numerical check of the first ten to the thirteenth zeros prove the conjecture?"
    ) == ("question", {"mode": "rh-numcheck"})
    assert det_classify("what is the smallest zero off the critical line, if one exists?") == (
        "question",
        {"mode": "rh-offzero"},
    )
    assert det_classify("does the prime number theorem imply the riemann hypothesis?") == (
        "question",
        {"mode": "rh-pnt-conf"},
    )
    assert det_classify("does the euler product alone settle the location of the zeros?") == (
        "question",
        {"mode": "rh-prod-conf"},
    )
    assert det_classify("what is the value of zeta at three quarters?") == (
        "question",
        {"mode": "rh-zeta-val"},
    )
    # the tight-bound probe: the mathematical "S of T" keeps its case
    assert det_classify("what is the tight bound for S of T?") == ("question", {"mode": "rh-s-tight"})
    assert det_classify("state the zeta-series rule") == (
        "question",
        {"mode": "s8-state", "slug": "zeta-series"},
    )
    assert det_classify("state the num-zeros rule") == ("question", {"mode": "s8-state", "slug": "num-zeros"})
    assert det_classify("what is the pnt for") == ("question", {"mode": "s8-why", "slug": "pnt"})
    assert det_classify("explain why the strip holds") == ("question", {"mode": "s8-whydeep", "slug": "strip"})
    # the S8 derive targets classify on the unified table
    assert det_classify("derive reflect from func-eq") == (
        "question",
        {"mode": "derive", "target": "reflect", "parts": ("func-eq",)},
    )
    assert det_classify("derive strip from reflect, nozero-s1 and trivial-zeros") == (
        "question",
        {"mode": "derive", "target": "strip", "parts": ("reflect", "nozero-s1", "trivial-zeros")},
    )
    # a lesson surface is a bare canonical statement (the assertion path)
    assert det_classify(_st8("func-eq")) == ("assertion", {"lemma": _st8("func-eq")})


def test_grammar_no_collision_with_carried_families():
    # an unknown slug must NOT classify as an S8 state/whydeep probe
    assert det_classify("state the frobnicate rule")[1].get("mode") != "s8-state"
    assert det_classify("explain why the frobnicate holds")[1].get("mode") != "s8-whydeep"
    # the S7 vocabulary still routes to S7 (the unified tables)
    assert det_classify("state the tower-base rule") == ("question", {"mode": "s7-state", "slug": "tower-base"})
    assert det_classify("what is the tight bound for distinct distances in the plane?") == (
        "question",
        {"mode": "distdist"},
    )
    assert det_classify("what is the status of the erdosguess?") == (
        "question",
        {"mode": "conj-state", "proven": False},
    )
    # the S4 grid probe is not the pi-count probe
    assert det_classify("how many unit pairs does the 7 by 7 grid have?") == (
        "question",
        {"mode": "grid-pairs", "a": 7, "b": 7},
    )


def test_lesson_writes_the_seam_fact_established(rt_s8):
    r1 = rt_s8.turn(_st8("zeta-series"))
    assert r1.kind == "assertion"
    assert "lemma:zeta-series" in (r1.memory_diff or [])
    # re-teaching is a corroboration (no duplicate fact)
    r2 = rt_s8.turn(_st8("zeta-series"))
    assert not (r2.memory_diff or [])
    store = live_store(rt_s8)
    fact = None
    for a in store.query():
        if a.id == "lemma:zeta-series":
            fact = a
            break
    assert fact is not None
    assert fact.object == _st8("zeta-series")
    assert fact.context.data["kind"] == "lemma"
    assert fact.context.data["source_role"] == "declared-source"
    assert fact.context.data["source_lines"]


def test_conj_teach_is_the_m8_declaration(rt_s8):
    r = rt_s8.turn(_st8("riemann"))
    assert r.kind == "assertion"
    store = live_store(rt_s8)
    conj = None
    for a in store.query():
        if a.id == "conjecture:riemann":
            conj = a
            break
    assert conj is not None
    assert conj.context.data["conjecture_status"] == "open"
    assert conj.context.data["source_role"] == "declared-source"
    # the single self-citation (the declaration cites the id it just
    # stored — never a premise of a derivation)
    assert [str(x) for x in (r.grounded or [])] == ["conjecture:riemann"]


def test_pre_lesson_state_is_the_honest_gap(rt_s8):
    r = rt_s8.turn("state the zeta-series rule")
    assert r.kind == "impossible"
    assert GAP_ARTICULATION in (r.response_text or "")
    assert not (r.memory_diff or [])
    assert not (r.grounded or [])


def test_derive_missing_parts_is_a_typed_failure(rt_s8):
    # func-eq is untaught — the scaffold failure names it exactly
    rt_s8.turn(_st8("zeta-series"))
    r = rt_s8.turn("derive reflect from func-eq")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "needs_info"
    assert (
        ir["answer"]
        == "needs_info: i have not been taught the func-eq — the rule for reflect needs it before i can put it together"
    )
    assert not (r.grounded or [])
    assert not (r.memory_diff or [])


def test_derive_success_stores_the_derived_theorems(rt_s8):
    _teach_s8(rt_s8)
    store = live_store(rt_s8)
    for slug, parts in (("reflect", ("func-eq",)), ("strip", ("reflect", "nozero-s1", "trivial-zeros"))):
        fact = None
        for a in store.query():
            if a.id == f"theorem:{slug}":
                fact = a
                break
        assert fact is not None, slug
        assert fact.object == _th8(slug)
        assert fact.provenance.observer == "infant"
        assert fact.provenance.derived is True
        assert fact.provenance.source is not None and fact.provenance.source.authority == "infant"
        assert tuple(fact.context.data["derived_from"]) == parts
    # the strip's why chain cites the sanctioned parts, ordered
    rc = rt_s8.turn("explain why the strip holds")
    irc = rc.response_ir or {}
    assert irc["uncertainty_state"] == "derived"
    assert irc["answer"].startswith("i derived it from reflect, nozero-s1, trivial-zeros:")
    assert "theorem:strip" not in [str(x) for x in (irc.get("evidence") or [])]


def test_censuses_are_grounded_on_the_line(rt_s8):
    _teach_s8(rt_s8)
    # π(84) = 23, grounded on the line + the owning seam fact
    r = rt_s8.turn("how many primes are at most 84?")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    assert ir["answer"] == "23"
    g = [str(x) for x in (r.grounded or [])]
    assert g
    assert all(x.startswith("cs-") or "count-successor" in x or x == "lemma:euler-product" for x in g)
    assert "lemma:euler-product" in g
    # π(36) = 11
    r36 = rt_s8.turn("how many primes are at most 36?")
    assert (r36.response_ir or {}).get("answer") == "11"
    # J(12) = 35 and J(18) = 71
    r12 = rt_s8.turn("what is the prime-power phi count at 12?")
    assert (r12.response_ir or {}).get("answer") == "35"
    r18 = rt_s8.turn("what is the prime-power phi count at 18?")
    assert (r18.response_ir or {}).get("answer") == "71"
    # the censuses write NO new assertions (they cite the existing line)
    store = live_store(rt_s8)
    succ = [
        a
        for a in store.query()
        if a.object_id.startswith("count-successor:num(")
        and (a.validity is None or a.validity.to is None)
    ]
    assert {int(a.object_id[len("count-successor:num(") : -1]) for a in succ} == set(range(1, 85))


def test_off_line_censuses_are_walls(rt_s8):
    _teach_s8(rt_s8)
    # the W-RH-7 pattern: names the argument and the line end
    w = rt_s8.turn("how many primes are at most 100?")
    irw = w.response_ir or {}
    assert irw["uncertainty_state"] == "needs_info"
    assert "100" in irw["answer"] and "84" in irw["answer"]
    assert not (w.grounded or [])
    # the W-RH-9 pattern: J(84) = 1053 named, the line end named
    w9 = rt_s8.turn("what is the prime-power phi count at 84?")
    ir9 = w9.response_ir or {}
    assert ir9["uncertainty_state"] == "needs_info"
    assert "1053" in ir9["answer"] and "84" in ir9["answer"]
    assert not (w9.grounded or [])


def test_growth_claim_and_sincycle_beds(rt_s8):
    _teach_s8(rt_s8)
    g = rt_s8.turn("what is the expected growth of the prime-power phi count?")
    irg = g.response_ir or {}
    assert irg["uncertainty_state"] == "derived"
    assert "asymptotic to x" in irg["answer"]
    assert "not a number in my store" in irg["answer"]  # the free-parameter split
    assert "lemma:pnt" in [str(x) for x in (g.grounded or [])]
    s = rt_s8.turn("does the sine vanish at every integer multiple of pi from one to 84?")
    irs = s.response_ir or {}
    assert irs["uncertainty_state"] == "derived"
    assert irs["answer"].startswith("yes — all eighty-four multiples of pi")
    assert "lemma:trivial-zeros" in [str(x) for x in (s.grounded or [])]


def test_numzero_is_the_declared_partial(rt_s8):
    _teach_s8(rt_s8)
    r = rt_s8.turn("what is the height of the first nontrivial zero?")
    ir = r.response_ir or {}
    assert ir["uncertainty_state"] == "derived"
    assert "14.1347" in ir["answer"]
    assert "declared numerical fact" in ir["answer"]
    assert "lemma:num-zeros" in [str(x) for x in (r.grounded or [])]


def test_attempt_wall_and_conj_state(rt_s8):
    _teach_s8(rt_s8)
    # the attempt: the frozen probe line's terminal-form articulation
    a = rt_s8.turn("can you derive the riemann hypothesis from the store?")
    ira = a.response_ir or {}
    assert ira["uncertainty_state"] == "needs_info"
    assert "not a capability i have been taught" in ira["answer"]
    assert "the farthest the store reaches is the strip" in ira["answer"]
    assert not (a.grounded or [])
    # the conj state: open, grounded EMPTY, evidence the conj id
    c = rt_s8.turn("what is the status of the riemann hypothesis?")
    irc = c.response_ir or {}
    assert irc["answer"] == "open — believed, not known"
    assert not (c.grounded or [])
    assert any("conjecture:riemann" in str(x) for x in (irc.get("evidence") or []))


def test_confounder_walls_are_honest(rt_s8):
    _teach_s8(rt_s8)
    probes = {
        "does the numerical check of the first ten to the thirteenth zeros prove the conjecture?": "not a proof",
        "what is the smallest zero off the critical line, if one exists?": "no proof that there is none",
        "does the prime number theorem imply the riemann hypothesis?": "the other way",
        "does the euler product alone settle the location of the zeros?": "away from the critical strip",
        "what is the value of zeta at three quarters?": "not in my store",
        "what is the tight bound for S of T?": "not in my store",
    }
    for probe, frag in probes.items():
        r = rt_s8.turn(probe)
        ir = r.response_ir or {}
        assert ir["uncertainty_state"] == "needs_info", probe
        assert frag in ir["answer"], probe
        assert not (r.grounded or []), probe


def test_why_split_is_mechanical_on_s8(rt_s8):
    _teach_s8(rt_s8)
    # declared lemma: the proof wall (no in-store mechanism)
    rw = rt_s8.turn("explain why the pnt holds")
    irw = rw.response_ir or {}
    assert irw["uncertainty_state"] == "needs_info"
    assert "the proof of pnt is not in my store" in irw["answer"]
    assert not (rw.grounded or [])
    # derived theorem: the in-store chain
    rc = rt_s8.turn("explain why the reflect holds")
    irc = rc.response_ir or {}
    assert irc["uncertainty_state"] == "derived"
    assert irc["answer"].startswith("i derived it from func-eq:")
    # the why (essence) of a declared lemma is still served
    re = rt_s8.turn("what is the s-of-t for")
    assert (re.response_ir or {}).get("uncertainty_state") == "derived"


def test_script_hash_and_store_decomposition():
    assert SCRIPT_HASH == hashlib.sha256(
        json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    total = sum(len(v) for v in FROZEN["script"].values())
    assert total == FROZEN["total_turns"] == 75
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 20
    assert len(FROZEN["script"][4]) == 30
    # the frozen decomposition: 840 seed + 33 facts + 71 events = 944
    # (the D-e6y collision at the S4:30 theorem-main reprobe dedupes)
    assert FROZEN["seed_total"] == 840
    assert FROZEN["new_facts"] == 33
    assert FROZEN["new_events"] == 71
    assert FROZEN["final_total"] == 944
    assert FROZEN["line_end_final"] == 84  # the line STAYS 0..84
    # every canonical statement carries a line crosswalk (P0(b))
    for slug, meta in _LESSON_META_S8.items():
        assert meta["source_lines"], slug
    # every theorem composition carries its sanctioned parts
    for slug, meta in _THEOREM_META_S8.items():
        assert meta["parts"], slug
    # the twelve lesson/conj phrases are byte-present in the frozen script
    all_surface = [t for s in FROZEN["script"].values() for t in s]
    for slug, meta in _LESSON_META_S8.items():
        assert meta["statement"] in all_surface, slug
    assert len(S8_LESSONS) == 12
    assert len(S8_THEOREMS) == 2
    # the P0 denylist: the S7 34 carried + 10 RH book/paper strings
    assert len(S8_DENYLIST) == 44
    assert set(S7_DENYLIST) <= set(S8_DENYLIST)
    # the ten prereq edges (the frozen curriculum data)
    assert len(FROZEN["prereq_edges"]) == 10
    # the domain sequences (control-1 frozen)
    assert FROZEN["domain_sequence"] == {
        2: "ULSLSLSFLSTSSLSSFLSTSSLSU",
        3: "LSSSHLSLSSHULSHLSSSH",
        4: "SSSSSSSSSSSSSSSSSSSSSHHHHHHSSS",
    }
    # the seam-family census: 55 carried + 14 new (11 lemmas + 1 conj + 2 theorems)
    assert FROZEN["total_seam_facts"] == 69
