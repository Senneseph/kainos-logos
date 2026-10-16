"""E6.16 (S12 — the RH neighborhood: the conditional layer, the two
roads, the declared queue) — the pre-registered frozen-table tests."""

from __future__ import annotations

import hashlib
import json

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    CONCEPT_S12,
    CONCEPT_S12_COND,
    CONCEPT_S12_REL,
    CONCEPT_S12_ROUTE,
    CONCEPT_S12_SCALE,
    S4_LESSONS,
    S5_LESSONS,
    S6_LESSONS,
    S7_LESSONS,
    S8_LESSONS,
    S9_DENYLIST,
    S9_LESSONS,
    S10_THEOREMS,
    S11_LESSONS,
    S11_THEOREMS,
    S12_BEDS,
    S12_LESSONS,
    S12_THEOREMS,
    _s11_py_chain,
    _s11_py_spf,
    _s12_py_gaps,
    _s12_py_M,
    _s12_py_scale,
    det_classify,
)
from kainos.tutor.e611 import _ANSWER_ as E611_ANSWER
from kainos.tutor.e612 import _ANSWER_ as E612_ANSWER
from kainos.tutor.e615 import (
    CONCEPTS_E615,
)
from kainos.tutor.e615 import (
    FROZEN as E615_FROZEN,
)
from kainos.tutor.e616 import (
    CONCEPTS_E616,
    FROZEN,
    SCRIPT_HASH,
    W_S12_2,
    W_S12_8,
)

ALL_CARRIED_LESSONS = {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS, **S9_LESSONS, **S11_LESSONS}

S12_LESSON_SLUGS = ("conditional-def", "rh-bound-scale", "rh-upf", "rh-relevance-def")

#: The S12 modes (the closed set the det arm classifies into).
S12_MODES_REF: tuple[str, ...] = (
    "s12-gap",
    "s12-gapmax",
    "s12-gapmax-whole",
    "s12-gapsize",
    "s12-gapcount",
    "s12-scale",
    "s12-scalecount",
    "s12-mod4-1",
    "s12-mod4-3",
    "s12-mod4q",
    "s12-mlab",
    "s12-mat",
    "s12-mroot",
    "s12-mpast",
    "s12-condgive",
    "s12-uncond",
    "s12-queue",
    "s12-queue-lot",
    "s12-class",
    "s12-agree",
    "s12-roads-how",
    "s12-roads-uncond",
    "s12-roads-cond",
    "s12-roadneg",
    "s12-reachscale",
    "s12-selved",
    "s12-prove",
    "s12-bandstate",
    "s12-state",
)


def test_new_concepts_prereqs_point_down() -> None:
    # S12 adds the four RH-neighborhood concepts; the carried
    # registry is unchanged; prereqs point DOWN at existing
    # concepts only (the house invariant).
    carried = tuple(c.id for c in CONCEPTS_E615)
    assert tuple(c.id for c in CONCEPTS_E616) == carried + (CONCEPT_S12_COND, CONCEPT_S12_SCALE, CONCEPT_S12_ROUTE, CONCEPT_S12_REL)
    existing = set(carried)
    for c in CONCEPT_S12:
        for p in c.prereqs:
            assert p in existing or p in {CONCEPT_S12_COND, CONCEPT_S12_SCALE, CONCEPT_S12_ROUTE, CONCEPT_S12_REL}, (
                f"{c.id}: prereq {p!r} does not point down at an existing concept"
            )
        existing.add(c.id)
    labels = {c.id: c.label for c in CONCEPT_S12}
    assert labels[CONCEPT_S12_COND] == "a conditional lot: a conclusion under the condition that the zeros lie on the line"
    assert labels[CONCEPT_S12_SCALE] == "the root scale: the error and the gap the condition installs"
    assert labels[CONCEPT_S12_ROUTE] == "the two roads to prime-parts uniqueness: the scan, and the condition"
    assert labels[CONCEPT_S12_REL] == "the declared RH-relevance classes that select the cross-pollination queue"


def test_script_shape_and_teaching() -> None:
    assert FROZEN["total_turns"] == 85
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 28
    assert len(FROZEN["script"][4]) == 32
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    # the four TEACH turns are the exact lesson phrases (verbatim).
    for slug in S12_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S12_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    # no S4–S11 seam statement appears IN the script verbatim (the
    # carried corpus is reproduced by PROBE, never by re-assertion).
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for m in S10_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S11_THEOREMS.values():
        assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the teaches (the S12 P1).
    assert FROZEN["script"][2][0] == "what does the condition give for the error of the prime count?"
    assert FROZEN["script"][2][1] == "what is the queue above my line?"
    assert FROZEN["script"][2][2] == "what does the condition give for the prime parts of a number?"
    # the prove turn (the off-band discipline) sits in S4.
    assert "prove the condition from its own lots?" in FROZEN["script"][4]


def test_frozen_shape() -> None:
    assert FROZEN["seed_total"] == 1200
    assert FROZEN["seed_identity"] == "ac75896f909858d5"
    assert FROZEN["line_end_final"] == 84
    assert FROZEN["new_facts"] == 7
    assert FROZEN["new_fact_ids"] == [
        "lemma:conditional-def",
        "lemma:rh-bound-scale",
        "lemma:rh-upf",
        "lemma:rh-relevance-def",
        "theorem:gap-scale-agreement",
        "theorem:two-routes-one-guarantee",
        "theorem:queue-declared",
    ]
    assert FROZEN["total_seam_facts"] == 95  # 72 `lemma:` + 23 `theorem:`
    assert len(FROZEN["theorem_dag"]) == 23  # S6 + S7 + S8 + S9 + S10 + S11 + S12
    assert len(FROZEN["walls_honest"]) == 7
    assert len(FROZEN["beds_exact"]) == 23
    assert len(FROZEN["derived_table"]) == 68
    assert FROZEN["pre_teach_gaps"] == {"S02:01": "rh-scale", "S02:02": "rh-relevance", "S02:03": "factor-route"}
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 2
    assert FROZEN["rederive"] is None  # the S12 script has no re-derive turn
    assert len(FROZEN["seam_carry_refs"]) == 19


def test_pre_s12_states_carry_e615_final() -> None:
    # the 84 seed concepts at their S11-final values, built from
    # the e6.15 frozen tables (the mechanism's own data).
    pre = FROZEN["pre_s12_states"]
    assert len(pre) == 84
    for cid, base in E615_FROZEN["pre_s11_states"].items():
        want = base["correct"] + E615_FROZEN["pre_s11_drilled"].get(cid, 0)
        assert pre[cid] == {"state": base["state"], "correct": want}
    for cid, v in E615_FROZEN["mastery_expected"].items():
        assert pre[cid] == {"state": v["state"], "correct": v["correct"]}


def test_denylist_is_the_s9_44() -> None:
    # S12 carries the S9 denylist UNCHANGED (the 44: S7-34 + the
    # RH ten) in addition to its own marker rule.
    assert len(S9_DENYLIST) == 44


def test_hypothesis_marker_rule() -> None:
    # P0: the four marker facts (the conditional-def lesson + the
    # two conditional lessons + the two-routes composition) carry
    # the condition's text in their FROZEN statements (the store
    # bytes must match at run time).
    marker_statements = {
        "conditional-def": next(p for p, (_c, s, _k, _es, _d, _l) in S12_LESSONS.items() if s == "conditional-def"),
        "rh-bound-scale": next(p for p, (_c, s, _k, _es, _d, _l) in S12_LESSONS.items() if s == "rh-bound-scale"),
        "rh-upf": next(p for p, (_c, s, _k, _es, _d, _l) in S12_LESSONS.items() if s == "rh-upf"),
        "two-routes-one-guarantee": S12_THEOREMS["two-routes-one-guarantee"]["statement"],
    }
    for slug, text in marker_statements.items():
        assert (
            "under the condition of the Riemann hypothesis" in text or "under the condition that" in text
        ), f"{slug}: the condition's text is not in the frozen statement"
    # the non-marker lot (gap-scale-agreement) states an agreement,
    # not a conditional conclusion — it carries no marker.
    assert "under the condition of the Riemann hypothesis" not in S12_THEOREMS["gap-scale-agreement"]["statement"]


def test_compositions_sanctioned() -> None:
    # the three S12 compositions: the EXACT part sets, the owning
    # concepts (owner first in the declaration), byte-frozen
    # statements.
    assert S12_THEOREMS["gap-scale-agreement"]["parts"] == ("rh-bound-scale", "ledger-growth", "spf-chain")
    assert S12_THEOREMS["two-routes-one-guarantee"]["parts"] == ("rh-upf", "spf-chain")
    assert S12_THEOREMS["queue-declared"]["parts"] == ("rh-relevance-def", "rh-bound-scale", "rh-upf")
    assert S12_THEOREMS["gap-scale-agreement"]["concept"] == CONCEPT_S12_SCALE
    assert S12_THEOREMS["two-routes-one-guarantee"]["concept"] == CONCEPT_S12_ROUTE
    assert S12_THEOREMS["queue-declared"]["concept"] == CONCEPT_S12_REL
    for slug, meta in S12_THEOREMS.items():
        assert len(meta["statement"]) > 80, f"{slug}: the statement is not a full canonical statement"
    # the strict part-set failures name the missing part(s) (the
    # shared strict branch's own bytes — frozen from control #1).
    fail220 = FROZEN["scaffold_failures"]["S02:20"]
    if "##FREEZE-S12##" not in str(fail220):
        assert "queue-declared wants its exact set" in fail220
        assert "short the rh-bound-scale and the rh-upf" in fail220
    fail318 = FROZEN["scaffold_failures"]["S03:18"]
    if "##FREEZE-S12##" not in str(fail318):
        assert "two-routes-one-guarantee wants its exact set" in fail318
        assert "short the spf-chain" in fail318
    # the derive turns ground on the exact sanctioned parts.
    assert FROZEN["derive_successes"]["S03:14"] == (
        "gap-scale-agreement",
        {"lemma:rh-bound-scale", "lemma:ledger-growth", "theorem:spf-chain"},
    )
    assert FROZEN["derive_successes"]["S03:16"] == ("two-routes-one-guarantee", {"lemma:rh-upf", "theorem:spf-chain"})
    assert FROZEN["derive_successes"]["S04:01"] == (
        "queue-declared",
        {"lemma:rh-relevance-def", "lemma:rh-bound-scale", "lemma:rh-upf"},
    )


def test_walls_bytes() -> None:
    # the SEVEN walls are honest needs_info; the off-line
    # instances name the value AND the 0..84 line end (the
    # D-e6z(b) pattern).
    for ref, wall in FROZEN["walls_honest"].items():
        assert wall.startswith("needs_info: "), ref
        assert (
            "line end 84" in wall
            or "line end is 84" in wall
            or "my line end 84" in wall
        ), f"{ref}: the line end is not named"
    assert "zero-free region" in FROZEN["walls_honest"]["S02:10"]
    assert "zero density" in FROZEN["walls_honest"]["S02:10"]
    assert "the next prime is 89" in FROZEN["walls_honest"]["S02:23"]
    assert "off the line" in FROZEN["walls_honest"]["S02:23"]
    assert "whole prime line" in FROZEN["walls_honest"]["S03:13"]
    assert "the condition does not close the condition" in FROZEN["walls_honest"]["S03:21"]
    assert "factor-count deviation ledger" in FROZEN["walls_honest"]["S03:24"]
    assert "four lots and no fifth" in FROZEN["walls_honest"]["S04:07"]
    assert "the condition is the statement about the zeros" in FROZEN["walls_honest"]["S04:26"]


def test_beds_match_the_python_reference() -> None:
    # the ON-LINE beds are the mechanism's own reference values
    # (the store's walkers must reproduce them; the hand value and
    # the reference agree pre-freeze — D-e6g).
    gaps = _s12_py_gaps(84)
    assert len(gaps) == 22
    assert FROZEN["beds_exact"]["S03:06"] == "22 (between the 23 primes on my line)"
    assert FROZEN["beds_exact"]["S02:22"] == "the gap after 23 on my line is 6 (to 29)"
    assert FROZEN["beds_exact"]["S03:03"] == "the gap after 31 on my line is 6 (to 37)"
    assert FROZEN["beds_exact"]["S03:04"] == "the gap after 73 on my line is 6 (to 79)"
    gap6 = [f"{p} to {p + g}" for p, g in gaps if g == 6]
    assert len(gap6) == 6
    assert FROZEN["beds_exact"]["S03:05"] == "six (" + ", ".join(gap6) + ")"
    assert (
        FROZEN["beds_exact"]["S02:24"]
        == "the greatest gap on my line is 6, first at 23, and six gaps reach it (" + ", ".join(gap6) + ")"
    )
    # the bare scale: covering exactly 20 of the 22 gaps, failing
    # at exactly 2 (0.98 < 1) and 3 (1.90 < 2) — the witness values
    # live in the walls, never in the answer bytes.
    fail = [p for p, g in gaps if _s12_py_scale(p) < g]
    assert fail == [2, 3]
    assert FROZEN["beds_exact"]["S03:12"] == "of the 22 gaps on my line the bare scale covers 20, failing at exactly 2 and 3"
    assert FROZEN["beds_exact"]["S03:09"] == "yes — the square root of 5 times the log of 5 is at least the gap of 2"
    assert FROZEN["beds_exact"]["S03:11"] == "yes — the square root of 61 times the log of 61 is at least the gap of 6"
    # the ledger: greatest absolute 4, first at 31, eight places,
    # M(84) = -4.
    M = _s12_py_M(84)
    assert max(abs(v) for v in M.values()) == 4
    assert min(n for n in M if abs(M[n]) == 4) == 31
    assert len([n for n in M if abs(M[n]) == 4]) == 8
    assert M[84] == -4
    assert (
        FROZEN["beds_exact"]["S03:22"]
        == "4 on my line, first at 31, and it reaches it at eight places, all negative; the ledger at the line end 84 is minus 4"
    )
    assert FROZEN["beds_exact"]["S04:30"] == "the ledger at 31 is minus 4 — the first place the ledger reaches its greatest absolute on my line"
    # the mod-4 split: 9 one-mod-four, 13 three-mod-four, 2 alone.
    primes = [p for p in range(2, 85) if _s11_py_spf(p) == p]
    m1 = [p for p in primes if p % 4 == 1]
    m3 = [p for p in primes if p % 4 == 3]
    assert len(m1) == 9 and len(m3) == 13
    assert FROZEN["beds_exact"]["S03:27"] == "yes — 9 primes one mod four and 13 primes three mod four on my line, and 2 stands alone"
    assert FROZEN["beds_exact"]["S03:28"] == "9 on my line (" + ", ".join(map(str, m1)) + ")"
    assert FROZEN["beds_exact"]["S04:08"] == "13 on my line (" + ", ".join(map(str, m3)) + ")"
    # the S11 part carries (the seed-only bytes).
    assert FROZEN["beds_exact"]["S03:25"] == ", ".join(map(str, _s11_py_chain(84))) == "2, 2, 3, 7"
    assert FROZEN["beds_exact"]["S03:26"] == ", ".join(map(str, _s11_py_chain(60))) == "2, 2, 3, 5"
    # the witness values name themselves in the WALLS only.
    assert "0.98" in W_S12_8 and "1.90" in W_S12_8 and "9.17" in W_S12_8
    assert "89" in W_S12_2
    assert round(_s12_py_scale(2), 2) == 0.98 and round(_s12_py_scale(3), 2) == 1.90
    assert round(84**0.5, 2) == 9.17


def test_offline_values_never_store_answers() -> None:
    # D-e6z(b) at the S12 rung: the OFF-LINE witness values
    # (0.98, 1.90, 9.17, 89) appear ONLY in the walls that name
    # them, never as a derived (store) answer.
    for ref, ans in FROZEN["derived_table"].items():
        s = str(ans)
        for off in ("0.98", "1.90", "9.17"):
            assert off not in s, f"{ref}: the off-line value {off} in a store answer"
        assert "89" not in s, f"{ref}: the off-line value 89 in a store answer"
    # and they DO name themselves in the walls (the reference
    # wall + the gap-after-83 wall).
    for off in ("0.98", "1.90", "9.17", "line end 84"):
        assert off in W_S12_8
    assert "line end 84" in W_S12_2
    # the beds keep the off-line censuses for the P4 referee.
    assert S12_BEDS["scale_wall_values"] == {"2": 0.98, "3": 1.90}
    assert S12_BEDS["sqrt_line_end"] == 9.17
    assert S12_BEDS["next_prime_past_83"] == 89


def test_seam_carry_and_semantic_seam() -> None:
    # P6: the NINETEEN carry rows (byte-identical to the seed
    # store's answers); P5: the two-routes destination (the
    # mechanism's own spf walk classifies every n in 2..84 with
    # parts all prime and product n) + the queue grounding.
    assert FROZEN["seam_carry_refs"] == (
        "S02:25", "S03:25", "S03:26", "S04:09", "S04:10", "S04:11", "S04:14", "S04:15",
        "S04:16", "S04:17", "S04:18", "S04:19", "S04:20", "S04:21", "S04:22", "S04:23",
        "S04:24", "S04:25", "S04:32",
    )
    for ref in FROZEN["seam_carry_refs"]:
        assert ref in FROZEN["derived_table"]
    assert FROZEN["derived_table"]["S02:25"] == E612_ANSWER["CONJ_OPEN"]
    assert FROZEN["derived_table"]["S04:14"] == S10_THEOREMS["rh-reach"]["statement"]
    assert FROZEN["derived_table"]["S04:23"] == "23"  # the S8 pi-census (the SEAM row)
    assert FROZEN["derived_table"]["S04:32"] == "yes — 2 is the first prime: there is no k above 1 below it"
    # the off-script carry probes (the SAVANT-TRACK standing check).
    assert FROZEN["offscript_carry"]["what is the status of the erdosguess?"] == E611_ANSWER["CONJ_FALSIFIED"]
    assert FROZEN["offscript_carry"]["state the kstbound rule"] == next(
        p for p, (_c, s, _k, _es, _d, _l) in S4_LESSONS.items() if s == "kstbound"
    )
    # the semantic seam (a): the two-routes destination by the
    # python reference — every n in 2..84 factors into primes whose
    # product is n.
    for n in range(2, 85):
        parts = list(_s11_py_chain(n))
        assert all(_s11_py_spf(p) == p for p in parts)
        prod = 1
        for p in parts:
            prod *= p
        assert prod == n
    # (b) the queue grounding: every lot name is a fact id that
    # the seed (or the S12 run) provides.
    assert "conjecture:riemann" in FROZEN["seam_crosscheck"]["queue_referenced_ids"]
    assert "theorem:queue-declared" not in FROZEN["seam_crosscheck"]["queue_referenced_ids"]  # the queue is checked by the theorem itself


def test_probe_grammar_classifies() -> None:
    # the S12 surfaces classify on the det arm into the S12 modes
    # (no shadowing of the S4–S11 surfaces — the pre-reg §B table).
    kind, slots = det_classify("the gap after 23 on my line, what is it?")
    assert kind == "question" and slots["mode"] == "s12-gap" and slots["p"] == 23
    kind, slots = det_classify("the gap on my line, greatest, what is it?")
    assert slots["mode"] == "s12-gapmax"
    kind, slots = det_classify("the greatest gap of the whole prime line, what is it?")
    assert slots["mode"] == "s12-gapmax-whole"
    kind, slots = det_classify("the gaps of size 6 on my line, how many?")
    assert slots["mode"] == "s12-gapsize" and slots["k"] == 6
    kind, slots = det_classify("the gaps on my line, how many?")
    assert slots["mode"] == "s12-gapcount"
    kind, slots = det_classify("does the bare scale at 61 on my line cover the gap?")
    assert slots["mode"] == "s12-scale" and slots["p"] == 61
    kind, slots = det_classify("the gaps on my line covered by the bare scale, how many?")
    assert slots["mode"] == "s12-scalecount"
    kind, slots = det_classify("the primes one mod four on my line, how many?")
    assert slots["mode"] == "s12-mod4-1" and slots["which"] == "how many"
    kind, slots = det_classify("the primes three mod four on my line, how many?")
    assert slots["mode"] == "s12-mod4-3"
    kind, slots = det_classify("does my line carry the mod-4 split of the primes?")
    assert slots["mode"] == "s12-mod4q"
    kind, slots = det_classify("the factor-count deviation ledger on my line, greatest absolute, what is it?")
    assert slots["mode"] == "s12-mlab"
    kind, slots = det_classify("the factor-count deviation ledger at 31, what is it?")
    assert slots["mode"] == "s12-mat" and slots["n"] == 31
    kind, slots = det_classify("is the factor-count deviation ledger of my line below the root of my line end?")
    assert slots["mode"] == "s12-mroot"
    kind, slots = det_classify("the factor-count deviation ledger past my line end, below the root smallness, is it?")
    assert slots["mode"] == "s12-mpast"
    kind, slots = det_classify("what does the condition give for the error of the prime count?")
    assert slots["mode"] == "s12-condgive" and slots["x"] == "the error of the prime count"
    kind, slots = det_classify("what does the condition give for the zeros of the zeta function?")
    assert slots["x"] == "the zeros of the zeta function"
    kind, slots = det_classify("is the prime-parts uniqueness established without the condition?")
    assert slots["mode"] == "s12-uncond"
    kind, slots = det_classify("what is the queue above my line?")
    assert slots["mode"] == "s12-queue"
    kind, slots = det_classify("the queue above my line, fifth lot, which?")
    assert slots["mode"] == "s12-queue-lot" and slots["lot"] == "fifth"
    kind, slots = det_classify("the lots of this band condition-closing, which?")
    assert slots["mode"] == "s12-class" and slots["cls"] == "condition-closing"
    kind, slots = det_classify("does my line agree with the conditional root scale?")
    assert slots["mode"] == "s12-agree"
    kind, slots = det_classify("how do the two roads to prime-parts uniqueness differ?")
    assert slots["mode"] == "s12-roads-how"
    kind, slots = det_classify("which road to prime-parts uniqueness carries without the condition?")
    assert slots["mode"] == "s12-roads-uncond"
    kind, slots = det_classify("which road asks for the condition?")
    assert slots["mode"] == "s12-roads-cond"
    kind, slots = det_classify("does the condition road carry the guarantee without the condition?")
    assert slots["mode"] == "s12-roadneg"
    kind, slots = det_classify("which scale does the theorem rh-reach demand?")
    assert slots["mode"] == "s12-reachscale"
    kind, slots = det_classify("is the conjecture closed by any lot of this band?")
    assert slots["mode"] == "s12-selved"
    kind, slots = det_classify("prove the condition from its own lots?")
    assert slots["mode"] == "s12-prove"
    kind, slots = det_classify("the band at the line end, state?")
    assert slots["mode"] == "s12-bandstate"
    kind, slots = det_classify("state the rh-bound-scale rule")
    assert slots["mode"] == "s12-state" and slots["slug"] == "rh-bound-scale"
    # no S12 surface may shadow an S4–S11 surface: the S8 pi-count,
    # the S11 part carries, and the carried lesson states still
    # classify as before.
    kind, slots = det_classify("how many primes are at most 84?")
    assert slots["mode"] not in S12_MODES_REF
    kind, slots = det_classify("what are the prime parts of 84?")
    assert slots["mode"] == "parts"
    kind, slots = det_classify("is 83 a prime?")
    assert slots["mode"] == "prime-test" and slots["n"] == 83
    kind, slots = det_classify("state the ledger-growth rule")
    assert slots["mode"] == "s11-state"
    kind, slots = det_classify("state the rh-reach rule")
    assert slots["mode"] == "s9-state"
    kind, slots = det_classify("what is the status of the riemann hypothesis?")
    assert slots["mode"] not in S12_MODES_REF


def test_theorem_allowed_and_dag() -> None:
    # the theorem allow-set covers exactly the script turns whose
    # grounded lists carry a theorem id; the DAG is the sanctioned
    # twenty-three with byte-exact parts.
    for ref in FROZEN["theorem_allowed"]:
        assert ref in FROZEN["derived_table"], f"{ref}: an allow-set ref not in the derived table"
    assert FROZEN["theorem_allowed"]["S02:14"] == ("spf-chain",)
    assert FROZEN["theorem_allowed"]["S03:15"] == ("gap-scale-agreement",)
    assert FROZEN["theorem_allowed"]["S03:17"] == ("two-routes-one-guarantee",)
    assert FROZEN["theorem_allowed"]["S03:19"] == ("two-routes-one-guarantee", "spf-chain")
    assert FROZEN["theorem_allowed"]["S04:02"] == ("queue-declared",)
    assert FROZEN["theorem_allowed"]["S04:29"] == ("rh-reach",)
    assert FROZEN["theorem_allowed"]["S04:31"] == ("gap-scale-agreement", "two-routes-one-guarantee", "queue-declared")
    assert FROZEN["theorem_dag"]["gap-scale-agreement"] == ("rh-bound-scale", "ledger-growth", "spf-chain")
    assert FROZEN["theorem_dag"]["two-routes-one-guarantee"] == ("rh-upf", "spf-chain")
    assert FROZEN["theorem_dag"]["queue-declared"] == ("rh-relevance-def", "rh-bound-scale", "rh-upf")
    assert FROZEN["theorem_dag"]["rh-reach"] == ("strip", "mirror-region", "criterion-gap")


def test_script_hash_is_stable() -> None:
    computed = hashlib.sha256(
        json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    assert computed == SCRIPT_HASH


def test_wall_articulations_match_walls() -> None:
    for ref, arts in FROZEN["wall_articulations"].items():
        wall = FROZEN["walls_honest"][ref]
        for art in arts:
            assert art in wall, f"{ref}: articulation {art!r} not in the frozen wall"


def test_band_map_rh_track_untouched() -> None:
    # S12 has NO band flip: the fundamentals bands (including the
    # parallel RH-neighborhood band) are tracked in the plan doc,
    # not the bands.py census (the rh tracks carry — 10 of 12).
    rh3 = band_by_name("rh-3")
    assert rh3.status == "implemented"
    assert rh3.evidence == ("e6.14",)


def test_pre_s11_carry_is_byte_stable() -> None:
    # the pre_s12 states are the S11-final census: the carried
    # frontier concepts keep their S11-final states (nothing S12
    # drilled may regress a carried state at the frozen rung).
    pre = FROZEN["pre_s12_states"]
    stable = {cid for cid, v in pre.items() if v["state"] == "stable"}
    assert "prime-count" in stable
    assert "psi-eq" in stable
    assert "scan-ledger" in stable
    assert "first-divisor" in stable
