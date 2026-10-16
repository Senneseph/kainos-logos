"""E6.15 (S11 — the sieve: the full process + the scan ledger) —
the pre-registered frozen-table tests."""

from __future__ import annotations

import hashlib
import json

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    CONCEPT_S11,
    CONCEPT_S11_COMP,
    CONCEPT_S11_DIVID,
    CONCEPT_S11_LEDGER,
    CONCEPT_S11_SPF,
    S4_LESSONS,
    S6_LESSONS,
    S7_LESSONS,
    S8_LESSONS,
    S9_DENYLIST,
    S9_LESSONS,
    S10_THEOREMS,
    S11_BEDS,
    S11_LESSONS,
    S11_THEOREMS,
    _s11_py_cand_row,
    _s11_py_chain,
    _s11_py_comp_count,
    _s11_py_est_total,
    _s11_py_fd_count,
    _s11_py_kill_trials,
    _s11_py_prime_row,
    _s11_py_spf,
    det_classify,
)
from kainos.tutor.e611 import _ANSWER_ as E611_ANSWER
from kainos.tutor.e612 import _ANSWER_ as E612_ANSWER
from kainos.tutor.e614 import (
    CONCEPTS_E614,
)
from kainos.tutor.e614 import (
    FROZEN as E614_FROZEN,
)
from kainos.tutor.e615 import (
    AUDIT,
    CONCEPTS_E615,
    FROZEN,
    SCRIPT_HASH,
)

ALL_CARRIED_LESSONS = {**S4_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS, **S9_LESSONS}

GAP_FRAGMENT = "not a capability i have been taught"


def test_new_concepts_prereqs_point_down() -> None:
    # S11 adds the four divisibility-layer concepts; the carried
    # registry is unchanged; prereqs point DOWN at existing
    # concepts only (the house invariant).
    carried = tuple(c.id for c in CONCEPTS_E614)
    assert tuple(c.id for c in CONCEPTS_E615) == carried + (CONCEPT_S11_DIVID, CONCEPT_S11_COMP, CONCEPT_S11_SPF, CONCEPT_S11_LEDGER)
    existing = set(carried)
    for c in CONCEPT_S11:
        for p in c.prereqs:
            assert p in existing or p in {CONCEPT_S11_DIVID, CONCEPT_S11_COMP, CONCEPT_S11_SPF}, (
                f"{c.id}: prereq {p!r} does not point down at an existing concept"
            )
        existing.add(c.id)
    labels = {c.id: c.label for c in CONCEPT_S11}
    assert labels[CONCEPT_S11_DIVID] == "divisibility: k times m is n"
    assert labels[CONCEPT_S11_COMP] == "the composites: what a number is made of when it is not prime"
    assert labels[CONCEPT_S11_SPF] == "the first divisor: the smallest one above 1"
    assert labels[CONCEPT_S11_LEDGER] == "the scan ledger: what the full process records"


def test_script_shape_and_teaching() -> None:
    assert FROZEN["total_turns"] == 85
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 28
    assert len(FROZEN["script"][4]) == 32
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    # the four TEACH turns are the exact lesson phrases (verbatim).
    for slug in ("divides-def", "composite-def", "spf-def", "ledger-growth"):
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S11_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    # no S4–S10 seam statement appears IN the script verbatim (the
    # carried corpus is reproduced by PROBE, never by re-assertion).
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for m in S10_THEOREMS.values():
        assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the teaches (S11 P1).
    assert FROZEN["script"][2][0] == "does 3 divide 21?"
    assert FROZEN["script"][2][1] == "is 49 composite?"
    assert FROZEN["script"][2][2] == "what is the first divisor of 12?"


def test_frozen_shape() -> None:
    assert FROZEN["seed_total"] == 1101
    assert FROZEN["seed_identity"] == "b68e23bae96eca13"
    assert FROZEN["line_end_final"] == 84
    assert FROZEN["new_facts"] == 7
    assert FROZEN["new_fact_ids"] == [
        "lemma:divides-def",
        "lemma:composite-def",
        "lemma:spf-def",
        "lemma:ledger-growth",
        "theorem:first-divisor-prime",
        "theorem:sieve-equality",
        "theorem:spf-chain",
    ]
    assert FROZEN["total_seam_facts"] == 88  # 68 `lemma:` + 20 `theorem:`
    assert len(FROZEN["theorem_dag"]) == 20  # S6 + S7 + S8 + S9 + S10 + S11
    assert len(FROZEN["walls_honest"]) == 16
    assert len(FROZEN["beds_exact"]) == 34
    assert FROZEN["pre_teach_gaps"] == {"S02:01": "divides", "S02:02": "composite", "S02:03": "first-divisor"}
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 2


def test_pre_s11_states_carry_e614_final() -> None:
    # the 80 seed concepts at their S10-final values, built from
    # the e6.14 frozen tables (the mechanism's own data).
    pre = FROZEN["pre_s11_states"]
    assert len(pre) == 80
    for cid, base in E614_FROZEN["pre_s10_states"].items():
        want = base["correct"] + E614_FROZEN["pre_s10_drilled"].get(cid, 0)
        assert pre[cid] == {"state": base["state"], "correct": want}
    for cid, v in E614_FROZEN["mastery_expected"].items():
        assert pre[cid] == {"state": v["state"], "correct": v["correct"]}


def test_denylist_is_the_s9_44() -> None:
    # S11 carries the S9 denylist UNCHANGED (the 44: S7-34 + the RH ten).
    assert len(S9_DENYLIST) == 44


def test_compositions_sanctioned() -> None:
    # the three S11 compositions: the EXACT part sets, the owning
    # concept first-divisor, byte-frozen statements.
    assert S11_THEOREMS["first-divisor-prime"]["parts"] == ("composite-def", "spf-def")
    assert S11_THEOREMS["sieve-equality"]["parts"] == ("first-divisor-prime", "divides-def")
    assert S11_THEOREMS["spf-chain"]["parts"] == ("sieve-equality", "spf-def", "divides-def")
    for slug, meta in S11_THEOREMS.items():
        assert meta["concept"] == CONCEPT_S11_SPF, f"{slug}: the owning concept is first-divisor"
        assert len(meta["statement"]) > 80
    # the strict part-set failures name the missing part.
    assert "short the first-divisor-prime" in FROZEN["scaffold_failures"]["S03:09"]
    assert "short the spf-def" in FROZEN["scaffold_failures"]["S04:02"]
    # the derive turns ground on the exact sanctioned parts.
    assert FROZEN["derive_successes"]["S03:07"] == ("first-divisor-prime", {"lemma:composite-def", "lemma:spf-def"})
    assert FROZEN["derive_successes"]["S03:08"] == ("sieve-equality", {"theorem:first-divisor-prime", "lemma:divides-def"})
    assert FROZEN["derive_successes"]["S04:01"] == ("spf-chain", {"theorem:sieve-equality", "lemma:spf-def", "lemma:divides-def"})
    assert FROZEN["rederive"] == ("S03:27", "sieve-equality")


def test_walls_bytes() -> None:
    # every wall is honest needs_info; every off-line instance
    # names the value AND the 0..84 line end (the D-e6z(b) pattern);
    # the value-named aggregates name the mechanism's own number.
    for ref, wall in FROZEN["walls_honest"].items():
        assert wall.startswith("needs_info: "), ref
        for art in FROZEN["wall_articulations"].get(ref, ()):
            assert art in wall, f"{ref}: articulation {art!r} missing"
    assert "91 is off my 0..84 line" in FROZEN["walls_honest"]["S02:15"]
    assert "90 is off my 0..84 line" in FROZEN["walls_honest"]["S02:23"]
    assert "87 is off my 0..84 line" in FROZEN["walls_honest"]["S02:24"]
    assert "200 is off my 0..84 line — i cannot count" in FROZEN["walls_honest"]["S03:26"]
    assert "85 is off my 0..84 line — i cannot strip" in FROZEN["walls_honest"]["S04:10"]
    assert "97 is off my 0..84 line" in FROZEN["walls_honest"]["S04:15"]
    assert "120 is off my 0..84 line" in FROZEN["walls_honest"]["S04:28"]
    assert "121 is off my 0..84 line" in FROZEN["walls_honest"]["S04:29"]
    assert "are 95 — past my line which ends at 84" in FROZEN["walls_honest"]["S03:10"]
    assert "are 87 — past my line which ends at 84" in FROZEN["walls_honest"]["S03:11"]
    assert "are 828 — past my line which ends at 84" in FROZEN["walls_honest"]["S04:19"]
    assert "1000 is off my line — i sieve where the line runs: to 84" in FROZEN["walls_honest"]["S04:27"]
    assert "84 is composite — 2 is its first divisor" in FROZEN["walls_honest"]["S04:20"]
    assert "zero is not on my line" in FROZEN["walls_honest"]["S02:25"]
    assert "i begin the census at two" in FROZEN["walls_honest"]["S02:16"]


def test_beds_match_the_python_reference() -> None:
    # the ON-LINE beds are the mechanism's own reference values
    # (the store's walkers must reproduce them; the hand value and
    # the reference agree pre-freeze).
    assert FROZEN["beds_exact"]["S03:01"] == str(_s11_py_comp_count(10)) == "5"
    assert FROZEN["beds_exact"]["S03:02"] == str(_s11_py_comp_count(84)) == "60"
    assert FROZEN["beds_exact"]["S03:03"] == str(_s11_py_fd_count(84, 2)) == "41"
    assert FROZEN["beds_exact"]["S03:04"] == str(_s11_py_fd_count(84, 3)) == "13"
    assert FROZEN["beds_exact"]["S03:05"] == str(_s11_py_fd_count(84, 5)) == "4"
    assert FROZEN["beds_exact"]["S03:06"] == str(_s11_py_fd_count(84, 7)) == "2"
    assert FROZEN["beds_exact"]["S03:12"] == str(_s11_py_kill_trials(10, False)) == "6"
    assert FROZEN["beds_exact"]["S03:13"] == str(_s11_py_kill_trials(10, True)) == "6"
    assert FROZEN["beds_exact"]["S03:14"] == str(_s11_py_kill_trials(25, False)) == "21"
    assert FROZEN["beds_exact"]["S03:15"] == str(_s11_py_kill_trials(25, True)) == "20"
    assert FROZEN["beds_exact"]["S03:18"] == str(_s11_py_cand_row(2, 84)[1]) == "41"
    assert FROZEN["beds_exact"]["S03:19"] == str(_s11_py_cand_row(2, 84)[0]) == "82"
    assert FROZEN["beds_exact"]["S03:20"] == str(_s11_py_cand_row(3, 84)[0]) == "40"
    assert FROZEN["beds_exact"]["S03:21"] == str(_s11_py_cand_row(7, 84)[0]) == "21"
    assert FROZEN["beds_exact"]["S03:22"] == str(_s11_py_cand_row(7, 84)[1]) == "2"
    assert FROZEN["beds_exact"]["S03:23"] == str(_s11_py_cand_row(4, 84)[2]) == "27"
    assert FROZEN["beds_exact"]["S03:24"] == str(_s11_py_cand_row(5, 84)[2]) == "22"
    assert FROZEN["beds_exact"]["S03:25"] == str(_s11_py_cand_row(6, 84)[2]) == "22"
    assert FROZEN["beds_exact"]["S03:28"] == str(_s11_py_spf(25)) == "5"
    assert FROZEN["beds_exact"]["S04:03"] == ", ".join(map(str, _s11_py_chain(60))) == "2, 2, 3, 5"
    assert FROZEN["beds_exact"]["S04:04"] == ", ".join(map(str, _s11_py_chain(84))) == "2, 2, 3, 7"
    for ref, n in (("S04:05", 49), ("S04:06", 77), ("S04:07", 72), ("S04:08", 81)):
        assert FROZEN["beds_exact"][ref] == ", ".join(map(str, _s11_py_chain(n)))
    assert FROZEN["beds_exact"]["S04:09"] == "83 is prime — its only part is itself"
    pm, im = _s11_py_prime_row(83)
    assert FROZEN["beds_exact"]["S04:16"] == f"{pm} primes and {im} integers" == "22 primes and 59 integers"
    pm, im = _s11_py_prime_row(11)
    assert FROZEN["beds_exact"]["S04:17"] == f"{pm} primes and {im} integers" == "4 primes and 5 integers"
    pm, im = _s11_py_prime_row(5)
    assert FROZEN["beds_exact"]["S04:18"] == f"{pm} primes and {im} integer" == "2 primes and 1 integer"
    assert FROZEN["beds_exact"]["S04:22"] == "23"  # the S8 π-census (the SEAM row)
    # the est-total on-line maximum (bed D of the pre-reg).
    assert _s11_py_est_total(23) == 82
    assert _s11_py_est_total(84) == 828  # off-line: a wall, not an answer


def test_offline_values_never_store_answers() -> None:
    # D-e6f(a) (the house convention): the OFF-LINE aggregates
    # (95, 87, 828, 923, 340, 583) appear ONLY in the walls that
    # name them, never as a derived (store) answer.
    for ref, ans in FROZEN["derived_table"].items():
        s = str(ans)
        for off in ("923", "828", "340", "583"):
            assert off not in s, f"{ref}: the off-line value {off} in a store answer"
        assert "are 95 —" not in s and "are 87 —" not in s
    # and they DO name themselves in the walls.
    assert S11_BEDS["whole_process_84"] == (923, 340, 583)  # the beds carry the census
    assert S11_BEDS["kill_trials_full"][84] == 95
    assert S11_BEDS["kill_trials_prime"][84] == 87
    assert S11_BEDS["est_total"][84] == 828


def test_audit_string() -> None:
    # the owner's own question, answerable from the store's own
    # ledger — the D-e6f(a) corrected string (on-line rows only).
    assert "both sieves mark the same 60 composites from 2 to 84" in AUDIT
    assert "candidate 4: 27 tests, 0 hits" in AUDIT
    assert "candidate 6: 22 tests, 0 hits" in AUDIT
    assert "nothing more is kept, and there are no different marks" in AUDIT
    # the grand totals live in the walls/beds, never in the audit.
    for off in ("923", "340", "583"):
        assert off not in AUDIT
    # the audit re-probe sits at a NEW coordinate (S4:31).
    assert FROZEN["derived_table"]["S03:16"] == AUDIT
    assert FROZEN["derived_table"]["S04:31"] == AUDIT
    assert set(S11_BEDS["audit_rows"]) <= {0, 22, 27, 41, 60}
    assert S11_BEDS["audit_rows"] == (60, 41, 27, 0, 22, 0)


def test_seam_carry_and_semantic_seam() -> None:
    # P6: the S4:22–26 + S4:30 rows are the SEAM carry (byte-
    # identical to the seed store's answers); P5: the S11 lower
    # layer's prime test must classify EXACTLY the S8 π-census set
    # (23 = 23, the frozen AGREEMENT).
    assert FROZEN["seam_carry_refs"] == ("S04:22", "S04:23", "S04:24", "S04:25", "S04:26", "S04:30")
    for ref in FROZEN["seam_carry_refs"]:
        assert ref in FROZEN["derived_table"]
    assert FROZEN["derived_table"]["S04:23"] == E612_ANSWER["NUMZERO"]
    assert FROZEN["derived_table"]["S04:24"] == E612_ANSWER["CONJ_OPEN"]
    assert FROZEN["derived_table"]["S04:25"] == S10_THEOREMS["rh-reach"]["statement"]
    # the off-script carry probes (the SAVANT-TRACK carry, the
    # owner's 2026-08-23 question, encoded as a standing check).
    assert FROZEN["offscript_carry"]["what is the status of the erdosguess?"] == E611_ANSWER["CONJ_FALSIFIED"]
    assert FROZEN["offscript_carry"]["state the kstbound rule"] == next(
        p for p, (_c, s, _k, _es, _d, _l) in S4_LESSONS.items() if s == "kstbound"
    )
    # the semantic seam: the python reference classifies 23 primes,
    # agreeing with the S8 π(84) census.
    s11_primes = {n for n in range(2, 85) if _s11_py_spf(n) == n}
    assert len(s11_primes) == FROZEN["seam_crosscheck"]["s8_pi_count"] == 23
    assert len(s11_primes) == FROZEN["seam_crosscheck"]["s11_prime_set_size"]
    assert sum(n for n in s11_primes) == 874  # bed D: the sum of the primes


def test_probe_grammar_classifies() -> None:
    # the S11 surfaces classify on the det arm into the S11 modes
    # (no shadowing of the S4–S10 surfaces — the pre-reg §B table).
    kind, slots = det_classify("does 3 divide 21?")
    assert kind == "question" and slots["mode"] == "div-test" and (slots["k"], slots["n"]) == (3, 21)
    kind, slots = det_classify("is 49 composite?")
    assert slots["mode"] == "comp-test" and slots["n"] == 49
    kind, slots = det_classify("is 79 a prime?")
    assert slots["mode"] == "prime-test" and slots["n"] == 79
    kind, slots = det_classify("what is the first divisor of 12?")
    assert slots["mode"] == "fd-query" and slots["n"] == 12
    kind, slots = det_classify("how many composites are there up to 84?")
    assert slots["mode"] == "comp-count" and slots["n"] == 84
    kind, slots = det_classify("how many composites up to 84 have first divisor 2?")
    assert slots["mode"] == "fd-count" and (slots["n"], slots["d"]) == (84, 2)
    kind, slots = det_classify("how many trials does the full sieve spend on the composites up to 25?")
    assert slots["mode"] == "full-trials" and slots["n"] == 25
    kind, slots = det_classify("how many trials does the prime sieve spend on the composites up to 25?")
    assert slots["mode"] == "prime-trials" and slots["n"] == 25
    kind, slots = det_classify("how many times does the full sieve check an even number for divisibility by 2?")
    assert slots["mode"] == "cand-even2"
    kind, slots = det_classify("how many times does the full sieve test the candidate 7 up to 84?")
    assert slots["mode"] == "cand-tests" and (slots["d"], slots["n"]) == (7, 84)
    kind, slots = det_classify("how many times does the full sieve miss the candidate 6 up to 84?")
    assert slots["mode"] == "cand-misses" and (slots["d"], slots["n"]) == (6, 84)
    kind, slots = det_classify("for the prime 83, how many primes and how many integers did the sieve compare?")
    assert slots["mode"] == "prime-ledger" and slots["p"] == 83
    kind, slots = det_classify("how many comparisons did the sieve spend in total establishing the primes up to 23?")
    assert slots["mode"] == "est-total" and slots["n"] == 23
    kind, slots = det_classify("what are the prime parts of 60?")
    assert slots["mode"] == "parts" and slots["n"] == 60
    kind, slots = det_classify("does the full sieve keep anything the prime sieve throws away?")
    assert slots["mode"] == "audit"
    kind, slots = det_classify("run the sieve up to 84?")
    assert slots["mode"] == "sieverun" and slots["n"] == 84
    kind, slots = det_classify("what is the first-divisor-prime for")
    assert slots["mode"] == "s11-why" and slots["slug"] == "first-divisor-prime"
    kind, slots = det_classify("state the ledger-growth rule")
    assert slots["mode"] == "s11-state" and slots["slug"] == "ledger-growth"
    # no S11 surface may shadow an S4–S10 surface: the S8 π-count
    # and the carried lesson states still classify as before.
    kind, slots = det_classify("how many primes are at most 84?")
    assert slots["mode"] not in S11_MODES_REF
    kind, slots = det_classify("state the tower-base rule")
    assert slots["mode"] != "s11-state"


S11_MODES_REF: tuple[str, ...] = (
    "div-test",
    "comp-test",
    "prime-test",
    "fd-query",
    "comp-count",
    "fd-count",
    "full-trials",
    "prime-trials",
    "cand-even2",
    "cand-tests",
    "cand-hits",
    "cand-misses",
    "prime-ledger",
    "est-total",
    "parts",
    "audit",
    "sieverun",
    "s11-state",
    "s11-why",
    "s11-whydeep",
)


def test_theorem_allowed_and_dag() -> None:
    # the theorem allow-set covers exactly the script turns whose
    # grounded lists carry a theorem id; the DAG is the sanctioned
    # twenty with byte-exact parts.
    for ref in FROZEN["theorem_allowed"]:
        assert ref in FROZEN["derived_table"], f"{ref}: an allow-set ref not in the derived table"
    assert FROZEN["theorem_allowed"]["S03:08"] == ("first-divisor-prime",)
    assert FROZEN["theorem_allowed"]["S04:01"] == ("sieve-equality",)
    assert FROZEN["theorem_allowed"]["S04:09"] == ("spf-chain",)
    assert FROZEN["theorem_allowed"]["S04:31"] == ("sieve-equality",)
    assert FROZEN["theorem_dag"]["first-divisor-prime"] == ("composite-def", "spf-def")
    assert FROZEN["theorem_dag"]["sieve-equality"] == ("first-divisor-prime", "divides-def")
    assert FROZEN["theorem_dag"]["spf-chain"] == ("sieve-equality", "spf-def", "divides-def")
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
    # S11 has NO band flip: the fundamentals bands are tracked in
    # the plan doc, not the bands.py census (the rh tracks carry).
    rh3 = band_by_name("rh-3")
    assert rh3.status == "implemented"
    assert rh3.evidence == ("e6.14",)


def test_pre_s10_carry_is_byte_stable() -> None:
    # the pre_s11 states are the S10-final census: the 20 S9/S10
    # frontier concepts keep their S10-final states (nothing S11
    # drilled may regress a carried state at the frozen rung).
    pre = FROZEN["pre_s11_states"]
    stable = {cid for cid, v in pre.items() if v["state"] == "stable"}
    assert "prime-count" in stable
    assert "psi-eq" in stable
