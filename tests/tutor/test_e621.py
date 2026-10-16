from __future__ import annotations

import hashlib
import json

from kainos.tutor.brainstem import (
    CONCEPT_S17,
    S4_LESSONS,
    S5_LESSONS,
    S6_LESSONS,
    S6_THEOREMS,
    S7_LESSONS,
    S7_THEOREMS,
    S8_LESSONS,
    S8_THEOREMS,
    S9_DENYLIST,
    S9_LESSONS,
    S9_THEOREMS,
    S10_THEOREMS,
    S11_LESSONS,
    S11_THEOREMS,
    S12_LESSONS,
    S12_THEOREMS,
    S13_LESSONS,
    S13_THEOREMS,
    S14_LESSONS,
    S14_THEOREMS,
    S15_LESSONS,
    S15_THEOREMS,
    S16_LESSONS,
    S16_THEOREMS,
    S17_BEDS,
    S17_LESSONS,
    S17_THEOREMS,
    Brainstem,
    _beal_py_census,
    _beal_py_lte_box,
    _beal_py_v_p,
    det_classify,
)
from kainos.tutor.e620 import CONCEPTS_E620
from kainos.tutor.e621 import CONCEPTS_E621, FROZEN, SCRIPT_HASH

S17_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S17_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS)
    + list(S13_LESSONS) + list(S14_LESSONS) + list(S15_LESSONS)
    + list(S16_LESSONS)
)


def test_new_concepts_prereqs_point_down() -> None:
    """S17 adds the four valuation-line concepts; prereqs point DOWN
    (the S11 soil: first-divisor, divides, scan-ledger; the band's own
    valuation over the lte form; the census over the summit)."""
    carried = tuple(c.id for c in CONCEPTS_E620)
    assert tuple(c.id for c in CONCEPTS_E621) == carried + (
        CONCEPT_S17[0].id, CONCEPT_S17[1].id, CONCEPT_S17[2].id, CONCEPT_S17[3].id,
    )
    existing = set(carried)
    for c in CONCEPT_S17:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S17}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id: c for c in CONCEPT_S17}
    # the soil edges: the valuation over the spf soil, the lte form
    # over the valuation, the summit over the valuation + divides, the
    # census over the summit + the scan-ledger.
    assert by_id["valuation"].prereqs == ("first-divisor", "divides")
    assert by_id["lte-form"].prereqs == ("valuation",)
    assert by_id["beal-summit"].prereqs == ("valuation", "divides")
    assert by_id["beal-census"].prereqs == ("beal-summit", "scan-ledger")
    for c in CONCEPT_S17:
        assert c.band == "college-1"
        assert c.domain == "beal"


def test_script_shape_and_teaching() -> None:
    """51 turns; the four teaches are the lesson phrases verbatim;
    no carried seam statement appears in the script (Stage-A)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S17_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S17_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for mod in (
        S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS, S10_THEOREMS,
        S11_THEOREMS, S12_THEOREMS, S13_THEOREMS, S14_THEOREMS, S15_THEOREMS,
        S16_THEOREMS,
    ):
        for m in mod.values():
            assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the first teach (S2:01-02, then
    # the teach at S2:03 — two gaps, the S17 shape)
    assert FROZEN["script"][2][0] == "what is the p-adic depth of sixty-four at the prime two of record?"
    assert FROZEN["script"][2][1] == "state the valuation-def rule"
    assert (
        FROZEN["script"][2][2]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S17_LESSONS.items() if s == "valuation-def")
    )
    assert FROZEN["script"][3][0] == "what is the statement of the beal island of record?"
    # the Beal island's summit fact is declared and derived in-band
    assert "what is the statement of the beal island of record?" in script_lines
    assert "how many triples does the verification census of the beal island hold in the line's box?" in script_lines


def test_frozen_shape() -> None:
    """The control #1 census (D-e6l: the mechanism spoke, never the
    hand)."""
    assert FROZEN["seed_total"] == 1581
    assert FROZEN["seed_identity"] == "e21eaaf32b475930"
    assert FROZEN["line_end_final"] == 84  # S17 writes NO successor facts
    assert FROZEN["new_facts"] == 6
    assert FROZEN["new_fact_ids"] == [
        "lemma:valuation-def",
        "lemma:lte-def",
        "lemma:beal-def",
        "lemma:census-def",
        "theorem:lte-ledger",
        "theorem:beal-line-satisfaction",
    ]
    assert FROZEN["total_seam_facts"] == 128  # 112 lemma + 16 theorem (S16 122 + the SIX)
    assert len(FROZEN["theorem_dag"]) == 36  # S6..S17
    assert len(FROZEN["walls_honest"]) == 3
    assert len(FROZEN["beds_exact"]) == 15
    assert len(FROZEN["derived_table"]) == 19  # the two derives + the seventeen S4 rows (beds are beds_exact)
    assert len(FROZEN["pre_teach_gaps"]) == 7  # the seven pre-lesson gaps
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 2
    assert len(FROZEN["missing_parts_failure"]) == 1
    assert FROZEN["rederive"] is None
    assert len(FROZEN["seam_carry_refs"]) == 6
    assert FROZEN["final_total"] == 1641  # 1581 + 6 facts + 54 events (D-e6l(c))
    assert FROZEN["new_events"] == 54
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "UULSSSUULSSSFFTSS"
    assert FROZEN["domain_sequence"][3] == "UULULSSSFTHHHSSSS"
    assert FROZEN["domain_sequence"][4] == "SSSHSSSSSSSSSSSSH"


def test_pre_s17_states_carry_e620_final() -> None:
    """The 104 carried concepts at their S16-final values (the live
    control census, excluding the four new concepts — the e620
    convention, carried)."""
    pre = FROZEN["pre_s17_states"]
    assert len(pre) == 104
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S17}, "a NEW concept leaked into the pre-states"
    # the BSD soil as the S16 store held it
    assert pre["bsd-summit"] == {"state": "stable", "correct": 10}
    assert pre["analytic-order"] == {"state": "stable", "correct": 4}
    assert pre["algebraic-rank"] == {"state": "stable", "correct": 11}
    assert pre["line-reaching"] == {"state": "stable", "correct": 5}
    assert pre["l-partial"]["state"] == "stable"
    assert pre["l-correction"] == {"state": "stable", "correct": 8}
    assert pre["euler-factor"]["state"] == "stable"
    assert pre["rh-relevance"]["state"] == "practicing"  # the store held it practicing (17 correct)
    # the S11 soil the valuation line stands on
    assert pre["first-divisor"]["state"] == "stable"
    assert pre["divides"]["state"] == "stable"
    assert pre["scan-ledger"]["state"] == "stable"
    # the S17 soil drill at the NEW coordinates (control #1: the S4
    # carries S04:01-03 + the S15 correction carry S04:05)
    assert FROZEN["pre_s17_drilled"] == {
        "algebraic-rank": 1,
        "analytic-order": 1,
        "bsd-summit": 1,
        "l-correction": 1,
    }
    # the four NEW concepts at their frozen band-end values (all
    # stable: the four-correct-derivation rule held for each)
    assert FROZEN["mastery_expected"] == {
        "valuation": {"correct": 6, "prereq_gaps": [], "state": "stable"},
        "lte-form": {"correct": 7, "prereq_gaps": [], "state": "stable"},
        "beal-summit": {"correct": 4, "prereq_gaps": [], "state": "stable"},
        "beal-census": {"correct": 10, "prereq_gaps": [], "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "valuation": [],
        "lte-form": [],
        "beal-summit": [],
        "beal-census": [],
    }


def test_denylist_is_the_s9_44() -> None:
    # S17 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44


def test_unconditional_marker_absent() -> None:
    """The S17 facts are the unconditional valuation band: none
    carries the RH marker; the uncond probe says so of record on the
    line."""
    marker = "under the condition of the Riemann hypothesis"
    for th in S17_THEOREMS.values():
        assert marker not in th["statement"]
    for phrase in S17_LESSONS:
        assert marker not in phrase
    # the seed is the official S16 store (e6.20 run 1)
    assert FROZEN["seed"].startswith("results/phase-6/e6.20-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S17_THEOREMS) == {"lte-ledger", "beal-line-satisfaction"}
    assert S17_THEOREMS["lte-ledger"]["parts"] == ("lte-def", "valuation-def")
    assert S17_THEOREMS["beal-line-satisfaction"]["parts"] == ("beal-def", "census-def")
    # the frozen derive turns carry the SAME sanctioned part sets
    assert FROZEN["derive_successes"] == {
        "S02:15": ["lte-ledger", ["lte-def", "valuation-def"]],
        "S03:10": ["beal-line-satisfaction", ["beal-def", "census-def"]],
    }
    # the honest-turn bytes (D-e6l(a): the missing-parts probe NAMES
    # BOTH untaught parts — 'the beal-def or the census-def ... needs
    # them'; the scaffolds each name the single short part)
    assert FROZEN["missing_parts_failure"] == {
        "S02:13": "needs_info: i have not been taught the beal-def or the census-def — the rule for beal-line-satisfaction needs them before i can put it together"
    }
    assert "short the valuation-def" in FROZEN["scaffold_failures"]["S02:14"]
    assert "short the census-def" in FROZEN["scaffold_failures"]["S03:09"]


def test_walls_bytes() -> None:
    # the three walls are the Brainstem class attributes, byte-frozen:
    # S03:11 W-S17-1 (the primitive territory), S03:12 W-S17-2 (the
    # fermat-catalan boundary), S03:13 W-S17-3 (the fermat anchor)
    wall_attrs = {
        "S03:11": Brainstem.W_S17_1,
        "S03:12": Brainstem.W_S17_2,
        "S03:13": Brainstem.W_S17_3,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the no-new-decimals rule: the 3-powerful counterexample scale is
    # named AT ITS ORDER (seventeen digits), never as its digit string
    for _wall in FROZEN["walls_honest"].values():
        assert "776151559" not in _wall
        assert "776,151,559" not in _wall
    assert "seventeen digits" in Brainstem.W_S17_1
    # no honest-zero bytes (the S17 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The 15 on-line beds re-derive against the mechanism's own
    references (never hand-written values)."""
    # the CENSUS: 83 triples, zero primitive, every row a true
    # equation carrying its common factor
    count, prim, rows = _beal_py_census()
    assert (count, prim) == (83, 0)
    assert rows == S17_BEDS["census"]
    assert S17_BEDS["census_count"] == 83 and S17_BEDS["primitive_count"] == 0
    for r in rows:
        assert r[0] ** r[3] + r[1] ** r[4] == r[2] ** r[5], f"triple {r[:6]} is not a true equation"
    # the LEDGER: 249,280 instances, zero deviations
    inst, fail, _dig = _beal_py_lte_box()
    assert (inst, fail) == (249280, 0)
    assert S17_BEDS["lte_instances"] == 249280 and S17_BEDS["lte_failures"] == 0
    # the valuation probes: the p-rung of the chain
    for (n, p), depth in S17_BEDS["vp"].items():
        assert _beal_py_v_p(n, p) == depth, (n, p)
    # the panel families of record (named in the census lesson)
    for key in ("twin", "three", "seven", "fifteen"):
        r = S17_BEDS[key]
        assert r[0] ** r[3] + r[1] ** r[4] == r[2] ** r[5], key
    # the bed bytes name the records (the house wording)
    assert "the p-adic depth of sixty-four at the prime two of record is six" in FROZEN["beds_exact"]["S02:04"]
    assert "two hundred forty-nine thousand two hundred eighty" in FROZEN["beds_exact"]["S02:12"]
    assert "zero deviations" in FROZEN["beds_exact"]["S02:12"]
    assert "eighty-three triples in the box" in FROZEN["beds_exact"]["S03:06"]
    assert "zero — no primitive triple lives on my line" in FROZEN["beds_exact"]["S03:07"]
    assert "the ams beal prize holds it" in FROZEN["derived_table"]["S04:11"]  # the statement bed, re-probed


def test_statement_is_the_prize_verbatim() -> None:
    """The summit fact stores the Beal statement declared from its
    record source (the ams beal prize): the verbatim core of the
    declarative form stands in the lesson phrase, house-voiced
    (lettered, lowercased — the store voice)."""
    statement = next(p for p, (_c, s, _k, _es, _d, _l) in S17_LESSONS.items() if s == "beal-def")
    # the house-voiced core of the AMS declarative form
    assert "if a to the x power plus b to the y power equals c to the z power" in statement
    assert "positive integers with x, y and z each above two" in statement
    assert "a, b and c have a common prime factor" in statement
    # the equivalent form (the pairwise-coprime form)
    assert "no solution in pairwise coprime a, b and c once every exponent is above two" in statement
    # the record source named in the fact
    assert "the ams beal prize holds it" in statement
    # the line end (the floor discipline)
    assert "at the line end 84" in statement
    # the derivation files it on the line (the composition statement)
    comp = S17_THEOREMS["beal-line-satisfaction"]["statement"]
    assert "eighty-three triples of the box each carry their common prime factor" in comp
    assert "no primitive triple lives in the box" in comp
    assert "at the line end 84" in comp


def test_offline_values_never_store_answers() -> None:
    """S17 brings NO new off-line value: expect.offline_watch is
    empty, the 3-powerful counterexample scale is named at its order
    (never as its digit string), and no off-line decimal floats into
    an on-line answer or a wall."""
    with open("bands/spec-e6.21.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    watch = ["776151559", "776,151,559", "3,518,958,160,000", "3518958160000"]
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        for w in watch:
            assert w not in str(v), f"off-line value {w!r} floated into an on-line answer"
    for v in list(FROZEN["walls_honest"].values()):
        for w in watch:
            assert w not in v, "a carried off-line witness must not move into an S17 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the SIX carry rows (P6: byte-identical to the seed store):
    # the BSD summit carry, the S16 order carry, the S16 torsion
    # carry, the S16 L-value WALL carry, the S15 ramification
    # correction, and the queue
    assert FROZEN["seam_carry_refs"] == ["S04:01", "S04:02", "S04:03", "S04:04", "S04:05", "S04:06"]
    # the carried wall row stays honest (P3 wall-carried): the S16
    # L-value-of-record wall (W-S16-2)
    assert FROZEN["derived_table"]["S04:04"].startswith("needs_info: the exact L value at s equal to one is of record")
    # the off-script standing check: the S16 summit state, byte-
    # identical to the store's own theorem statement
    assert FROZEN["offscript_carry"] == {
        "state the bsd-panel-satisfaction rule": S16_THEOREMS["bsd-panel-satisfaction"]["statement"]
    }
    # the seam crosscheck expected value
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"


def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]


def test_probe_grammar_classifies() -> None:
    # the full 51-surface map (det_classify is the referee)
    plain = {
        "S02:01": "s17-vp",
        "S02:04": "s17-vp", "S02:05": "s17-vp", "S02:06": "s17-vp",
        "S02:07": "s17-lte-a",
        "S02:10": "s17-lte-a", "S02:11": "s17-lte-b",
        "S02:12": "s17-lte-ledger",
        "S02:16": "s17-vp", "S02:17": "s17-lte-ledger",
        "S03:01": "s17-beal", "S03:04": "s17-census",
        "S03:06": "s17-census", "S03:07": "s17-empt", "S03:08": "s17-family",
        "S03:11": "s17-prim", "S03:12": "s17-fc", "S03:13": "s17-flt",
        "S03:14": "s17-census", "S03:15": "s17-bandstate", "S03:17": "s17-uncond",
        "S04:01": "s16-bsd", "S04:02": "s16-order", "S04:03": "s16-torsion",
        "S04:04": "s16-lvalwall", "S04:05": "s15-corr", "S04:06": "s12-queue",
        "S04:07": "s17-vp", "S04:08": "s17-vp", "S04:09": "s17-lte-a",
        "S04:10": "s17-lte-ledger", "S04:11": "s17-beal", "S04:12": "s17-census",
        "S04:13": "s17-empt", "S04:14": "s17-family", "S04:16": "s17-bandstate",
        "S04:17": "s17-prim",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:02": "valuation-def",
        "S02:08": "lte-def",
        "S03:02": "beal-def",
        "S03:16": "beal-line-satisfaction",
        "S04:15": "census-def",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", "s17-state", want), ref
    derive_turns = {
        "S02:13": "derive",
        "S02:14": "derive",
        "S02:15": "derive",
        "S03:09": "derive",
        "S03:10": "derive",
    }
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    assertion_turns = ["S02:03", "S02:09", "S03:03", "S03:05"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the summit fact of the island?")[1]["mode"] == "s16-bsd"
    assert det_classify("what does the first panel member's L product hold at my line end?")[1]["mode"] == "s14-lpar"
    assert det_classify("what is the ramification correction of the first panel member?")[1]["mode"] == "s15-corr"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("state the bsd-panel-satisfaction rule")[1]["mode"] == "s16-state"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: the summit's own state readout cites the beal
    # composition; the queue carry row cites the carried queue theorem
    assert FROZEN["theorem_allowed"] == {
        "S03:16": ["beal-line-satisfaction"],
        "S04:06": ["queue-declared"],
    }
    # the full sanctioned DAG: thirty-six theorem facts (the S16
    # thirty-four + the two compositions)
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 36
    assert "theorem:lte-ledger" in dag
    assert "theorem:beal-line-satisfaction" in dag
    assert "theorem:beal" not in dag, "the bare conj id must NOT exist (the summit is the declared record fact + the composition)"
    assert "theorem:bsd" not in dag, "the BSD bare conj id stayed gone (the S16 invariant holds)"


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH
    assert SCRIPT_HASH == "e69997696f25cbcb"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:11": ["primitive", "line end 84"],
        "S03:12": ["fermat-catalan", "line end 84"],
        "S03:13": ["wiles", "line end 84"],
    }


def test_band_map_frozen_untouched() -> None:
    # the Beal island is research-adjacent: the frozen bands-map
    # (S10) stays untouched; e6.21 validates the map as-is against
    # the extended registry.
    from kainos.tutor.bands import BAND_MAP

    domains = {d for b in BAND_MAP for d in b.domains}
    assert "beal" not in domains, "the band map is frozen at S10 — no new band entries"
    assert len(CONCEPTS_E621) == 108  # the S16 104 + the four valuation-line concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (the D-e6l family: the
    # missing-parts byte names both untaught parts, the two scaffolds
    # name their single short parts — all show through as F turns;
    # no ambiguous letters)
    assert FROZEN["domain_sequence"] == {
        2: "UULSSSUULSSSFFTSS",
        3: "UULULSSSFTHHHSSSS",
        4: "SSSHSSSSSSSSSSSSH",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"
