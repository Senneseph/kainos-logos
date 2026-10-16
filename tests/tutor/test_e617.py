"""E6.17 (S13 — the zeta variants, three families) — the
pre-registered frozen-table tests."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction

from kainos.tutor.bands import band_by_name
from kainos.tutor.brainstem import (
    CONCEPT_S13,
    CONCEPT_S13_FACTOR,
    CONCEPT_S13_PARTIAL,
    CONCEPT_S13_REMOVAL,
    CONCEPT_S13_SPLIT,
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
    S12_LESSONS,
    S12_THEOREMS,
    S13_BEDS,
    S13_LESSONS,
    S13_THEOREMS,
    _s11_py_chain,
    _s11_py_spf,
    _s13_py_family,
    _s13_py_primes,
    _s13_py_removal,
    _s13_py_telescope,
    det_classify,
)
from kainos.tutor.e611 import _ANSWER_ as E611_ANSWER
from kainos.tutor.e616 import CONCEPTS_E616
from kainos.tutor.e616 import FROZEN as E616_FROZEN
from kainos.tutor.e617 import (
    CONCEPTS_E617,
    FROZEN,
    SCRIPT_HASH,
    W_S13_1,
    W_S13_2,
    W_S13_3,
    W_S13_4,
    W_S13_5,
    W_S13_6,
    W_S13_7,
)

ALL_CARRIED_LESSONS = {
    **S4_LESSONS,
    **S5_LESSONS,
    **S6_LESSONS,
    **S7_LESSONS,
    **S8_LESSONS,
    **S9_LESSONS,
    **S11_LESSONS,
    **S12_LESSONS,
}

S13_LESSON_SLUGS = ("factor-def", "split-def", "removal-def", "region-def")

#: The S13 modes (the closed set the det arm classifies into).
S13_MODES_REF: tuple[str, ...] = (
    "s13-partial",
    "s13-factor",
    "s13-factor-prime",
    "s13-split-census",
    "s13-index-count",
    "s13-partition-hold",
    "s13-limit",
    "s13-limit-boundary",
    "s13-removal",
    "s13-removal-set",
    "s13-removal-below",
    "s13-removal-max",
    "s13-removal-all",
    "s13-spot-above",
    "s13-closed-form",
    "s13-compare3",
    "s13-compare-same",
    "s13-compare6",
    "s13-descent",
    "s13-plus-side",
    "s13-unclass",
    "s13-uncond",
    "s13-seam-count",
    "s13-seam-sameset",
    "s13-rhzero",
    "s13-rh-touch",
    "s13-bandstate",
    "s13-state",
)


def test_new_concepts_prereqs_point_down() -> None:
    # S13 adds the four zeta-variant concepts; the carried
    # registry is unchanged; prereqs point DOWN at existing
    # concepts only (the house invariant).
    carried = tuple(c.id for c in CONCEPTS_E616)
    assert tuple(c.id for c in CONCEPTS_E617) == carried + (
        CONCEPT_S13_FACTOR,
        CONCEPT_S13_SPLIT,
        CONCEPT_S13_PARTIAL,
        CONCEPT_S13_REMOVAL,
    )
    existing = set(carried)
    for c in CONCEPT_S13:
        for p in c.prereqs:
            assert p in existing or p in {
                CONCEPT_S13_FACTOR,
                CONCEPT_S13_SPLIT,
                CONCEPT_S13_PARTIAL,
                CONCEPT_S13_REMOVAL,
            }, f"{c.id}: prereq {p!r} does not point down at an existing concept"
        existing.add(c.id)
    labels = {c.id: c.label for c in CONCEPT_S13}
    assert labels[CONCEPT_S13_FACTOR] == "the family factor: the term each index number carries"
    assert (
        labels[CONCEPT_S13_SPLIT]
        == "the index split: primes, composites, all — a partition of the integers above one"
    )
    assert labels[CONCEPT_S13_PARTIAL] == (
        "the line partial: what a family holds up to the line end, a rational the store holds"
    )
    assert labels[CONCEPT_S13_REMOVAL] == (
        "the term-removal: the product is multiplied by the reciprocal of the removed term"
    )
    for c in CONCEPT_S13:
        assert c.band == "college-1"
        assert c.domain == "rh"


def test_script_shape_and_teaching() -> None:
    assert FROZEN["total_turns"] == 85
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 28
    assert len(FROZEN["script"][4]) == 32
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    # the four TEACH turns are the exact lesson phrases (verbatim).
    for slug in S13_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S13_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    # no S4–S12 seam statement appears IN the script verbatim (the
    # carried corpus is reproduced by PROBE, never by re-assertion).
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for m in S10_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S11_THEOREMS.values():
        assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the teaches (the S13 P1/P2).
    assert FROZEN["script"][2][0] == "what does the minus family over all the numbers hold up to my line end?"
    assert FROZEN["script"][2][1] == "how do the index numbers of my line split?"
    assert FROZEN["script"][2][2] == "state the factor-def rule"
    # the zero-derive wall (the off-band discipline) sits in S4.
    assert "derive the Riemann hypothesis from the telescope on my line" in FROZEN["script"][4]


def test_frozen_shape() -> None:
    assert FROZEN["seed_total"] == 1296
    assert FROZEN["seed_identity"] == "8ccb13defebb9e95"
    assert FROZEN["line_end_final"] == 84
    assert FROZEN["new_facts"] == 7
    assert FROZEN["new_fact_ids"] == [
        "lemma:factor-def",
        "lemma:split-def",
        "lemma:removal-def",
        "lemma:region-def",
        "theorem:partition-identity",
        "theorem:telescope-line",
        "theorem:removal-single",
    ]
    assert FROZEN["total_seam_facts"] == 102  # 96 `lemma:` + 26 `theorem:` (S12's 95 + the SEVEN)
    assert len(FROZEN["theorem_dag"]) == 26  # S6 + S7 + S8 + S9 + S10 + S11 + S12 + S13
    assert len(FROZEN["walls_honest"]) == 9
    assert len(FROZEN["beds_exact"]) == 32
    assert len(FROZEN["derived_table"]) == 54  # the S04:03-09 carry rows are P6-owned
    assert len(FROZEN["pre_teach_gaps"]) == 5  # three pre-teach + two state probes
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 2
    assert len(FROZEN["missing_parts_failure"]) == 1
    assert FROZEN["rederive"] is None  # the S13 script has no re-derive turn
    assert len(FROZEN["seam_carry_refs"]) == 7
    # the control #1 store census (the D-e6y family at the S13 rung).
    assert FROZEN["final_total"] == 1388
    assert FROZEN["new_events"] == 85
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1; D-e6h(d)).
    assert FROZEN["domain_sequence"][2] == "UUULSSSSLSSTSSSSSSSFHHHHH"
    assert FROZEN["domain_sequence"][3] == "UUFLSSSSLTSSSSSHSSHHTSSFSHSS"
    assert FROZEN["domain_sequence"][4] == "SSSHSSSSSUHSSSSSSSSSSSSSSSSSSSSH"


def test_pre_s13_states_carry_e616_final() -> None:
    # the 88 carried concepts at their S12-final values, built
    # from the e6.16 frozen tables (the mechanism's own data).
    pre = FROZEN["pre_s13_states"]
    assert len(pre) == 88
    for cid, base in E616_FROZEN["pre_s12_states"].items():
        want = base["correct"] + E616_FROZEN["pre_s12_drilled"].get(cid, 0)
        assert pre[cid] == {"state": base["state"], "correct": want}
    for cid, v in E616_FROZEN["mastery_expected"].items():
        assert pre[cid] == {"state": v["state"], "correct": v["correct"]}
    # the S13 drill at the NEW coordinates (control #1).
    assert FROZEN["pre_s13_drilled"] == {"composite": 1, "factor-route": 2}
    # the four NEW concepts at their frozen band-end values.
    assert FROZEN["mastery_expected"] == {
        "family-factor": {"correct": 24, "state": "stable"},
        "index-split": {"correct": 9, "state": "stable"},
        "line-partial": {"correct": 9, "state": "stable"},
        "removal-rule": {"correct": 12, "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "family-factor": [],
        "index-split": [],
        "line-partial": [],
        "removal-rule": [],
    }


def test_denylist_is_the_s9_44() -> None:
    # S13 carries the S9 denylist UNCHANGED (the 44: S7-34 + the
    # RH ten) in addition to its own UNCONDITIONAL marker rule.
    assert len(S9_DENYLIST) == 44


def test_unconditional_marker_absent() -> None:
    # P0 (INVERTED from S12): NO S13 lesson or theorem statement
    # carries the hypothesis marker — the zeta variants are
    # unconditional mathematics. The four S12 marker statements
    # keep theirs (the carried tables are byte-frozen).
    marker = "under the condition of the Riemann hypothesis"
    for phrase in S13_LESSONS:
        assert marker not in phrase, f"the S13 lesson carries the marker: {phrase[:50]}..."
    for slug, meta in S13_THEOREMS.items():
        assert marker not in meta["statement"], f"{slug}: the S13 theorem carries the marker"
    # the S12 conditional layer keeps its marker (unchanged).
    for slug in ("conditional-def", "rh-bound-scale", "rh-upf"):
        text = next(p for p, (_c, s, _k, _es, _d, _l) in S12_LESSONS.items() if s == slug)
        assert marker in text or "under the condition that" in text, f"{slug}: the S12 marker dropped"
    assert (
        marker in S12_THEOREMS["two-routes-one-guarantee"]["statement"]
        or "under the condition that" in S12_THEOREMS["two-routes-one-guarantee"]["statement"]
    )


def test_compositions_sanctioned() -> None:
    # the three S13 compositions: the EXACT part sets, the owning
    # concepts, byte-frozen full-canonical statements.
    assert S13_THEOREMS["partition-identity"]["parts"] == ("split-def", "factor-def")
    assert S13_THEOREMS["telescope-line"]["parts"] == ("factor-def", "region-def")
    assert S13_THEOREMS["removal-single"]["parts"] == ("removal-def", "factor-def")
    assert S13_THEOREMS["partition-identity"]["concept"] == CONCEPT_S13_SPLIT
    assert S13_THEOREMS["telescope-line"]["concept"] == CONCEPT_S13_PARTIAL
    assert S13_THEOREMS["removal-single"]["concept"] == CONCEPT_S13_REMOVAL
    for slug, meta in S13_THEOREMS.items():
        assert len(meta["statement"]) > 80, f"{slug}: the statement is not a full canonical statement"
    # the strict part-set failures name the missing part(s) (the
    # shared strict branch's own bytes — frozen from control #1).
    fail220 = FROZEN["scaffold_failures"]["S02:20"]
    if "##FREEZE-S13##" not in str(fail220):
        assert "partition-identity wants its exact set" in fail220
        assert "short the factor-def" in fail220
    fail324 = FROZEN["scaffold_failures"]["S03:24"]
    if "##FREEZE-S13##" not in str(fail324):
        assert "telescope-line wants its exact set" in fail324
        assert "short the factor-def" in fail324
    # the missing-part articulation names the untaught rule.
    missing = FROZEN["missing_parts_failure"]["S03:03"]
    assert "i have not been taught the region-def" in missing
    # the derive turns ground on the exact sanctioned parts.
    for ref, want in (
        ("S02:12", ("partition-identity", {"lemma:split-def", "lemma:factor-def"})),
        ("S03:10", ("telescope-line", {"lemma:factor-def", "lemma:region-def"})),
        ("S03:21", ("removal-single", {"lemma:removal-def", "lemma:factor-def"})),
    ):
        slug, parts = FROZEN["derive_successes"][ref]
        assert slug == want[0] and set(parts) == want[1], f"{ref}: {(slug, set(parts))} != {want}"


def test_walls_bytes() -> None:
    # the NINE walls are honest needs_info; the off-line
    # instances name the value AND the 0..84 line end (the
    # D-e6z(b) pattern).
    for ref, wall in FROZEN["walls_honest"].items():
        assert wall.startswith("needs_info: "), ref
        assert "line end 84" in wall or "line end is 84" in wall or "my line end 84" in wall, (
            f"{ref}: the line end is not named"
        )
    assert "one half" in FROZEN["walls_honest"]["S02:21"]
    assert "0.6079271019" in FROZEN["walls_honest"]["S02:22"]
    assert "0.8224670334" in FROZEN["walls_honest"]["S02:23"]
    assert "1.5198177546" in FROZEN["walls_honest"]["S02:24"]
    assert "no closed form in my store" in FROZEN["walls_honest"]["S02:25"]
    assert "1.8380389552" in FROZEN["walls_honest"]["S02:25"]  # D-e6h(a)
    assert "101 over 200" in FROZEN["walls_honest"]["S03:16"]
    assert "0.8319073726" in FROZEN["walls_honest"]["S03:19"]
    assert "harmonic series" in FROZEN["walls_honest"]["S03:20"]
    assert "0.8319073726" in FROZEN["walls_honest"]["S04:32"]
    # the wall constants are the frozen pre-reg bytes (D-e6h(a)).
    assert W_S13_1 == FROZEN["walls_honest"]["S02:21"].removeprefix("needs_info: ")
    assert W_S13_2 == FROZEN["walls_honest"]["S02:22"].removeprefix("needs_info: ")
    assert W_S13_5 == FROZEN["walls_honest"]["S02:25"].removeprefix("needs_info: ")
    assert W_S13_7 == FROZEN["walls_honest"]["S03:16"].removeprefix("needs_info: ")


def _over(fr: Fraction) -> str:
    return f"{fr.numerator} over {fr.denominator}"


def test_beds_match_the_python_reference() -> None:
    # the ON-LINE beds are the mechanism's own reference values
    # (the store's walkers must reproduce them; the hand value and
    # the reference agree pre-freeze — D-e6h).
    primes = _s13_py_primes(84)
    assert len(primes) == 23
    assert FROZEN["beds_exact"]["S02:10"] == "83"
    assert (
        FROZEN["beds_exact"]["S02:11"]
        == "23 primes and 60 composites — every integer above one is one or the other, and neither is both"
    )
    assert (
        FROZEN["beds_exact"]["S04:01"]
        == "83 integers — 23 prime and 60 composite — the split the sieve layer holds on the same line"
    )
    assert (
        FROZEN["beds_exact"]["S04:02"]
        == "they are the same 23 — the index split is the sieve's split, counted by the prime test"
    )
    # the family factor (the (1 ± n^{-s}) term) — the S2:05-08 beds.
    assert FROZEN["beds_exact"]["S02:05"] == "(1 minus 5 to the power minus s)"
    assert FROZEN["beds_exact"]["S02:06"] == "(1 plus 5 to the power minus s)"
    assert FROZEN["beds_exact"]["S02:07"] == "(1 minus 83 to the power minus s)"
    assert FROZEN["beds_exact"]["S02:08"] == "84 is not a prime — the prime family carries no factor of it"
    # the line partials: the EXACT rationals (the s = 2 family,
    # the s = 3 family).
    assert FROZEN["beds_exact"]["S02:13"] == _over(_s13_py_family(-1, "all", 2, 84)) == "85 over 168"
    assert FROZEN["beds_exact"]["S02:14"] == _over(_s13_py_family(-1, "primes", 2, 84))
    assert FROZEN["beds_exact"]["S02:15"] == _over(_s13_py_family(-1, "comp", 2, 84))
    assert FROZEN["beds_exact"]["S02:17"] == _over(_s13_py_family(1, "all", 2, 84))
    assert FROZEN["beds_exact"]["S02:18"] == _over(_s13_py_family(1, "primes", 2, 84))
    assert FROZEN["beds_exact"]["S02:19"] == _over(_s13_py_family(1, "comp", 2, 84))
    assert FROZEN["beds_exact"]["S03:11"] == _over(_s13_py_telescope(8)) == "9 over 16"
    assert FROZEN["beds_exact"]["S03:12"] == _over(_s13_py_telescope(10)) == "11 over 20"
    assert FROZEN["beds_exact"]["S03:13"] == _over(_s13_py_telescope(20)) == "21 over 40"
    assert FROZEN["beds_exact"]["S03:14"] == _over(_s13_py_telescope(50)) == "51 over 100"
    assert FROZEN["beds_exact"]["S03:15"] == _over(_s13_py_telescope(84)) == "85 over 168"
    assert FROZEN["beds_exact"]["S03:17"] == _over(_s13_py_family(-1, "all", 3, 84))
    assert FROZEN["beds_exact"]["S03:18"] == _over(_s13_py_family(-1, "primes", 3, 84))
    assert FROZEN["beds_exact"]["S03:27"] == _over(_s13_py_family(1, "all", 3, 84))
    assert FROZEN["beds_exact"]["S04:26"] == _over(_s13_py_family(-1, "comp", 3, 84))
    assert FROZEN["beds_exact"]["S04:27"] == _over(_s13_py_family(1, "primes", 3, 84))
    # the partition identity holds EXACT on the line (s = 2 and
    # s = 3); the six partials order D-e6h.
    assert (
        _s13_py_family(-1, "all", 2, 84)
        == _s13_py_family(-1, "primes", 2, 84) * _s13_py_family(-1, "comp", 2, 84)
        == _s13_py_telescope(84)
    )
    assert (
        _s13_py_family(-1, "all", 3, 84)
        == _s13_py_family(-1, "primes", 3, 84) * _s13_py_family(-1, "comp", 3, 84)
    )
    assert S13_BEDS["order_s2"] == [
        "minus-all",
        "minus-prime",
        "minus-comp",
        "plus-comp",
        "plus-prime",
        "plus-all",
    ]
    # the removal rule: the multipliers, the maxes, the set
    # removals (D-e6h(c): {2,3,5} -> 25/16, not 75/64).
    assert FROZEN["beds_exact"]["S03:05"] == "it multiplies by 4 over 3"
    assert FROZEN["beds_exact"]["S03:06"] == "it multiplies by 9 over 8"
    assert _s13_py_removal(2, 2) == Fraction(4, 3)
    assert _s13_py_removal(3, 2) == Fraction(9, 8)
    assert _s13_py_removal(83, 2) == Fraction(6889, 6888)
    assert _s13_py_removal(2, 3) == Fraction(8, 7)
    assert FROZEN["beds_exact"]["S03:08"] == "it multiplies by 8 over 7"
    assert FROZEN["beds_exact"]["S03:22"] == _over(
        _s13_py_removal(2, 2) * _s13_py_removal(3, 2)
    ) == "3 over 2"
    assert FROZEN["beds_exact"]["S03:23"] == _over(
        _s13_py_removal(2, 2) * _s13_py_removal(3, 2) * _s13_py_removal(5, 2)
    ) == "25 over 16"  # D-e6h(c)
    assert max(_s13_py_removal(p, 2) for p in primes) == Fraction(4, 3)
    assert max(_s13_py_removal(p, 3) for p in primes) == Fraction(8, 7)
    assert FROZEN["beds_exact"]["S04:21"] == "all 23 — the largest is 4 over 3, at the prime 2"
    assert (
        FROZEN["beds_exact"]["S04:22"]
        == "8 over 7, at the prime 2 — the multiplier descends toward one as the prime grows"
    )
    # the whole-prime-family removal (S04:23): the composite
    # partial remains (all / prime on the line, s = 2).
    over23 = _over(_s13_py_family(-1, "comp", 2, 84))
    assert (
        _s13_py_family(-1, "all", 2, 84) / _s13_py_family(-1, "primes", 2, 84)
        == _s13_py_family(-1, "comp", 2, 84)
    )
    assert over23 in FROZEN["derived_table"]["S04:23"], "the s = 2 composite partial fraction is not in the S04:23 bytes"
    # the telescoping spots and the one-half boundary (the W-S13-7
    # off-line value 101/200 stays in the wall).
    assert _s13_py_telescope(100) == Fraction(101, 200)
    assert all(
        _s13_py_telescope(int(n)) == Fraction(*map(int, spot.split("/")))
        for n, spot in S13_BEDS["telescope_spots"].items()
    )
    assert (
        FROZEN["derived_table"]["S03:25"]
        == "none — (N plus 1) over 2N is one half plus 1 over 2N — the spots 3 over 4, 2 over 3, 5 over 8, 11 over 20 and 85 over 168 all stand above it, descending toward the limit"
    )
    assert (
        FROZEN["derived_table"]["S03:28"]
        == "the plus family over all the numbers stands largest; the minus family over all the numbers stands smallest"
    )


def test_offline_values_never_store_answers() -> None:
    # D-e6z(b) at the S13 rung: the OFF-LINE limit values
    # (0.6079271019, 0.8224670334, 1.5198177546, 1.8380389552,
    # 1.2093811574, 0.8319073726, 101/200) appear ONLY in the
    # walls that name them, never as a derived (store) answer.
    off = ("0.6079271019", "0.8224670334", "1.5198177546", "1.8380389552", "1.2093811574", "0.8319073726", "101 over 200")
    for ref, ans in FROZEN["derived_table"].items():
        s = str(ans)
        for v in off:
            assert v not in s, f"{ref}: the off-line value {v} in a store answer"
    # and they DO name themselves in the walls.
    for v in ("0.6079271019",):
        assert v in W_S13_2
    for v in ("0.8224670334",):
        assert v in W_S13_3
    for v in ("1.5198177546",):
        assert v in W_S13_4
    for v in ("1.8380389552",):
        assert v in W_S13_5
    for v in ("0.8319073726",):
        assert v in W_S13_6
    assert "101 over 200" in W_S13_7
    # the beds keep the off-line censuses for the P4 referee.
    assert S13_BEDS["telescope_offline_N100"] == "101/200"
    assert S13_BEDS["set_removal_s2"] == {"2,3": "3/2", "2,3,5": "25/16"}


def test_seam_carry_and_semantic_seam() -> None:
    # P6: the SEVEN carry rows (byte-identical to the seed
    # store's answers); P5: the two-routes destination (the
    # mechanism's own spf walk classifies every n in 2..84 with
    # parts all prime and product n) + the queue grounding.
    assert FROZEN["seam_carry_refs"] == (
        "S04:03",
        "S04:04",
        "S04:05",
        "S04:06",
        "S04:07",
        "S04:08",
        "S04:09",
    )
    # the off-script carry probes (the SAVANT-TRACK standing check).
    assert FROZEN["offscript_carry"]["what is the status of the erdosguess?"] == E611_ANSWER["CONJ_FALSIFIED"]
    assert FROZEN["offscript_carry"]["state the kstbound rule"] == next(
        p for p, (_c, s, _k, _es, _d, _l) in S4_LESSONS.items() if s == "kstbound"
    )
    # the semantic seam (a): the two-routes destination by the
    # python reference — every n in 2..84 factors into primes
    # whose product is n.
    for n in range(2, 85):
        parts = list(_s11_py_chain(n))
        assert all(_s11_py_spf(p) == p for p in parts)
        prod = 1
        for p in parts:
            prod *= p
        assert prod == n
    # (b) the queue grounding: every lot name is a fact id that
    # the seed (or the S13 run) provides.
    assert "conjecture:riemann" in FROZEN["seam_crosscheck"]["queue_referenced_ids"]
    assert "theorem:queue-declared" not in FROZEN["seam_crosscheck"]["queue_referenced_ids"]
    # the zero-derive wall (S4:10): the mechanism's own bytes
    # (the hand draft said otherwise — D-e6h(d)).
    assert FROZEN["rh_zero_text"].startswith("honestly, i can't do that yet")
    assert "it remains open, at the line end 84." in FROZEN["rh_zero_text"]
    # the rh-touch wall (S4:11) and the closed-form wall (S3:26).
    assert FROZEN["rh_touch_wall"].startswith("needs_info: nothing this band holds settles the conjecture")
    assert "the condition remains open, at the line end 84" in FROZEN["rh_touch_wall"]
    assert FROZEN["unclassified_honest"]["expected"].startswith("needs_info: the plus family over all the numbers")
    assert "the standing invitation, at the line end 84" in FROZEN["unclassified_honest"]["expected"]


def test_probe_grammar_classifies() -> None:
    # the eighty-five script surfaces classify on the det arm:
    # the S13 surfaces into the 28 S13 modes, the carry surfaces
    # into the CARRIED modes (pi-count, s12-queue, ...), the teach
    # turns as lesson assertions, the derive turns as derive.
    expected_modes = {
        "S02:01": "s13-partial",
        "S02:02": "s13-split-census",
        "S02:03": "s13-state",
        "S02:04": "assertion",
        "S02:05": "s13-factor",
        "S02:06": "s13-factor",
        "S02:07": "s13-factor",
        "S02:08": "s13-factor-prime",
        "S02:09": "assertion",
        "S02:10": "s13-index-count",
        "S02:11": "s13-split-census",
        "S02:12": "derive",
        "S02:20": "derive",
        "S02:21": "s13-limit",
        "S02:22": "s13-limit",
        "S02:23": "s13-limit",
        "S02:24": "s13-limit",
        "S02:25": "s13-limit",
        "S03:01": "s13-state",
        "S03:02": "s13-state",
        "S03:03": "derive",
        "S03:04": "assertion",
        "S03:09": "assertion",
        "S03:10": "derive",
        "S03:16": "s13-partial",
        "S03:19": "s13-limit",
        "S03:20": "s13-limit-boundary",
        "S03:21": "derive",
        "S03:24": "derive",
        "S03:25": "s13-spot-above",
        "S03:26": "s13-closed-form",
        "S03:28": "s13-compare6",
        "S04:03": "s12-queue",
        "S04:04": "s12-queue-lot",
        "S04:05": "s12-uncond",
        "S04:06": "s12-roads-how",
        "S04:07": "pi-count",
        "S04:08": "comp-count",
        "S04:09": "prime-ledger",
        "S04:10": "s13-rhzero",
        "S04:11": "s13-rh-touch",
        "S04:29": "s13-bandstate",
        "S04:30": "s13-uncond",
        "S04:31": "s13-unclass",
    }
    for snum, rows in FROZEN["script"].items():
        for i, surface in enumerate(rows, 1):
            ref = f"S{snum:02d}:{i:02d}"
            kind, slots = det_classify(surface)
            want = expected_modes.get(ref)
            if want == "assertion":
                assert kind == "assertion" and slots.get("lemma"), f"{ref}: expected a lesson assertion"
            elif want == "derive":
                assert kind == "question" and (slots or {}).get("mode") == "derive", (
                    f"{ref}: expected derive, got {(slots or {}).get('mode')}"
                )
            elif want is not None:
                assert kind == "question" and (slots or {}).get("mode") == want, (
                    f"{ref}: expected mode {want}, got {(slots or {}).get('mode')}"
                )
            else:
                # the remaining S13 surfaces classify into S13
                # modes (the closed set — no shadow, no ambiguity).
                assert kind == "question" and (slots or {}).get("mode") in S13_MODES_REF, (
                    f"{ref}: not an S13 mode: {(slots or {}).get('mode')}"
                )
    # no S13 surface may shadow an S4–S12 surface: the carried
    # censuses and the carried lesson states still classify as
    # before.
    kind, slots = det_classify("how many primes are at most 84?")
    assert slots["mode"] == "pi-count"
    kind, slots = det_classify("is 83 a prime?")
    assert slots["mode"] == "prime-test" and slots["n"] == 83
    kind, slots = det_classify("state the ledger-growth rule")
    assert slots["mode"] == "s11-state"
    kind, slots = det_classify("state the rh-reach rule")
    assert slots["mode"] == "s9-state"
    kind, slots = det_classify("what are the prime parts of 84?")
    assert slots["mode"] == "parts"
    kind, slots = det_classify("state the factor-def rule")
    assert slots["mode"] == "s13-state" and slots["slug"] == "factor-def"


def test_theorem_allowed_and_dag() -> None:
    # the theorem allow-set covers exactly the script turns whose
    # grounded lists carry a theorem id; the DAG is the sanctioned
    # twenty-six with byte-exact parts.
    allow = FROZEN["theorem_allowed"]
    assert allow["S02:16"] == ["partition-identity"]
    assert allow["S03:15"] == ["telescope-line"]
    assert allow["S03:25"] == ["telescope-line"]
    assert allow["S04:03"] == ["queue-declared"]
    assert allow["S04:05"] == ["spf-chain"]
    assert allow["S04:06"] == ["two-routes-one-guarantee"]
    assert allow["S04:12"] == ["partition-identity"]
    assert allow["S04:13"] == ["telescope-line"]
    assert allow["S04:14"] == ["removal-single"]
    assert allow["S04:24"] == ["telescope-line"]
    assert allow["S04:28"] == ["partition-identity"]
    assert allow["S04:29"] == ["partition-identity", "removal-single", "telescope-line"]
    assert FROZEN["theorem_dag"]["partition-identity"] == ("split-def", "factor-def")
    assert FROZEN["theorem_dag"]["telescope-line"] == ("factor-def", "region-def")
    assert FROZEN["theorem_dag"]["removal-single"] == ("removal-def", "factor-def")
    # the carried DAG is intact (a sample).
    assert FROZEN["theorem_dag"]["rh-reach"] == ("strip", "mirror-region", "criterion-gap")
    assert FROZEN["theorem_dag"]["queue-declared"] == ("rh-relevance-def", "rh-bound-scale", "rh-upf")


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


def test_band_map_fundamentals_track_untouched() -> None:
    # S13 has NO band-map change: the fundamentals-track bands
    # (including the parallel RH tracks) are tracked in the plan
    # doc, not the bands.py census (10 of 12 implemented carry).
    rh3 = band_by_name("rh-3")
    assert rh3.status == "implemented"
    assert rh3.evidence == ("e6.14",)


def test_domain_sequences_are_control_one() -> None:
    # the frozen per-turn domain letters: lengths match the
    # per-session script lengths, the impossible set is exactly
    # the five pre-lesson gaps + the S4:10 zero-derive wall, the
    # teach turns are the four L's, the derive turns the T's.
    for snum in (2, 3, 4):
        assert len(FROZEN["domain_sequence"][snum]) == len(FROZEN["script"][snum])
    seq = {f"S{snum:02d}:{i:02d}": ch for snum in (2, 3, 4) for i, ch in enumerate(FROZEN["domain_sequence"][snum], 1)}
    impossible = sorted(ref for ref, ch in seq.items() if ch == "U")
    assert impossible == sorted(FROZEN["pre_teach_gaps"]) + ["S04:10"]
    assert sorted(k for k, v in seq.items() if v == "L") == sorted(FROZEN["teach_turns"])
    assert sorted(k for k, v in seq.items() if v == "T") == sorted(FROZEN["derive_successes"])
    assert {k for k, v in seq.items() if v == "F"} == set(FROZEN["scaffold_failures"]) | {
        "S03:03",  # the missing-part articulation
    }
