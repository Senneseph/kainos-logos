from __future__ import annotations

import hashlib
import json
from fractions import Fraction

from kainos.tutor.brainstem import (
    B14_A,
    B14_B,
    CONCEPT_S16,
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
    S16_BEDS,
    S16_LESSONS,
    S16_THEOREMS,
    Brainstem,
    _bsd_py_gen_ledger,
    _bsd_py_lpartial_record,
    _bsd_py_lpartial_uniform,
    _bsd_py_torsion_points,
    _bsd_py_which,
    det_classify,
)
from kainos.tutor.e619 import CONCEPTS_E619
from kainos.tutor.e620 import FROZEN, SCRIPT_HASH

S16_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S16_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS)
    + list(S13_LESSONS) + list(S14_LESSONS) + list(S15_LESSONS)
)


def test_new_concepts_prereqs_point_down() -> None:
    """S16 adds the four summit concepts; prereqs point DOWN (the
    L-factor soil of band 2, the point soil of band 1)."""
    carried = tuple(c.id for c in CONCEPTS_E619)
    assert tuple(c.id for c in CONCEPTS_E620_IDS()) == carried + (
        CONCEPT_S16[0].id, CONCEPT_S16[1].id, CONCEPT_S16[2].id, CONCEPT_S16[3].id,
    )
    existing = set(carried)
    for c in CONCEPT_S16:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S16}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id: c for c in CONCEPT_S16}
    # the soil edges: analytic-order over the L-partial soil (band 2),
    # algebraic-rank over the point soil (band 1); the summit and the
    # reaching stand on the two sides.
    assert by_id["analytic-order"].prereqs == ("l-partial",)
    assert by_id["algebraic-rank"].prereqs == ("curve-law", "curve-shadow")
    assert by_id["bsd-summit"].prereqs == ("analytic-order", "algebraic-rank")
    assert by_id["line-reaching"].prereqs == ("analytic-order", "algebraic-rank")
    for c in CONCEPT_S16:
        assert c.band == "college-1"
        assert c.domain == "bsd"


def CONCEPTS_E620_IDS() -> tuple:
    from kainos.tutor.e620 import CONCEPTS_E620

    return CONCEPTS_E620


def test_script_shape_and_teaching() -> None:
    """51 turns; the four teaches are the lesson phrases verbatim;
    no carried seam statement appears in the script (Stage-A)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S16_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S16_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for mod in (
        S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS, S10_THEOREMS,
        S11_THEOREMS, S12_THEOREMS, S13_THEOREMS, S14_THEOREMS, S15_THEOREMS,
    ):
        for m in mod.values():
            assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the first teach
    assert (
        FROZEN["script"][2][0]
        == "what order of vanishing does the L product of the first panel member have at s equal to one of record?"
    )
    assert (
        FROZEN["script"][2][1]
        == "what is the algebraic rank of the second panel member of record?"
    )
    assert FROZEN["script"][2][2] == "state the vanish-def rule"
    assert FROZEN["script"][2][3] == next(p for p, (_c, s, _k, _es, _d, _l) in S16_LESSONS.items() if s == "vanish-def")
    assert FROZEN["script"][3][0] == "state the statement-def rule"
    # the BSD island's summit fact is declared and derived in-band
    assert "what is the summit fact of the island?" in script_lines
    assert "what does my line hold toward the summit of the island?" in script_lines


def test_frozen_shape() -> None:
    """The control #1 census (D-e6k: the mechanism spoke, never the
    hand)."""
    assert FROZEN["seed_total"] == 1522
    assert FROZEN["seed_identity"] == "adff69d61a3e4219"
    assert FROZEN["line_end_final"] == 84  # S16 writes NO successor facts
    assert FROZEN["new_facts"] == 5
    assert FROZEN["new_fact_ids"] == [
        "lemma:vanish-def",
        "lemma:rank-def",
        "lemma:statement-def",
        "lemma:reach-def",
        "theorem:bsd-panel-satisfaction",
    ]
    assert FROZEN["total_seam_facts"] == 122  # 108 lemma + 14 theorem (S15 117 + the FIVE)
    assert len(FROZEN["theorem_dag"]) == 34  # S6..S16
    assert len(FROZEN["walls_honest"]) == 4
    assert len(FROZEN["beds_exact"]) == 18
    assert len(FROZEN["derived_table"]) == 18
    assert len(FROZEN["pre_teach_gaps"]) == 5  # the five pre-lesson gaps (D-e6k: state-style bytes among them)
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 1
    assert len(FROZEN["missing_parts_failure"]) == 1
    assert FROZEN["rederive"] is None
    assert len(FROZEN["seam_carry_refs"]) == 6
    assert FROZEN["final_total"] == 1581  # 1522 + 5 facts + 54 events (D-e6k(c))
    assert FROZEN["new_events"] == 54
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "UUULSSULSSSSSSSSF"
    assert FROZEN["domain_sequence"][3] == "ULFLSSSTSSHHHHSSS"
    assert FROZEN["domain_sequence"][4] == "SSSSHSSSSSSSSSSSS"


def test_pre_s16_states_carry_e619_final() -> None:
    """The 100 carried concepts at their S15-final values (the live
    control census, excluding the four new concepts — the e618
    convention, carried)."""
    pre = FROZEN["pre_s16_states"]
    assert len(pre) == 100
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S16}, "a NEW concept leaked into the pre-states"
    # the BSD soil as the S15 store held it
    assert pre["l-partial"]["state"] == "stable"
    assert pre["l-correction"]["state"] == "stable"
    assert pre["euler-factor"]["state"] == "stable"
    assert pre["curve-shadow"]["state"] == "stable"
    assert pre["rh-relevance"]["state"] == "practicing"  # the S15 store held it practicing (17 correct)
    assert pre["l-partial"]["correct"] == 14
    assert pre["l-correction"]["correct"] == 7
    # the S16 soil drill at the NEW coordinates (control #1)
    assert FROZEN["pre_s16_drilled"] == {"euler-factor": 1, "l-correction": 1}
    # the four NEW concepts at their frozen band-end values (all stable:
    # the four-correct-derivation rule held for each)
    assert FROZEN["mastery_expected"] == {
        "analytic-order": {"correct": 4, "prereq_gaps": [], "state": "stable"},
        "algebraic-rank": {"correct": 11, "prereq_gaps": [], "state": "stable"},
        "bsd-summit": {"correct": 10, "prereq_gaps": [], "state": "stable"},
        "line-reaching": {"correct": 5, "prereq_gaps": [], "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "analytic-order": [],
        "algebraic-rank": [],
        "bsd-summit": [],
        "line-reaching": [],
    }


def test_denylist_is_the_s9_44() -> None:
    # S16 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44


def test_unconditional_marker_absent() -> None:
    """The S16 facts are the unconditional summit band: none carries
    the RH marker; the uncond probe says so of record on the line."""
    marker = "under the condition of the Riemann hypothesis"
    for th in S16_THEOREMS.values():
        assert marker not in th["statement"]
    for phrase in S16_LESSONS:
        assert marker not in phrase
    # the seed is the official S15 store (e6.19 run 1)
    assert FROZEN["seed"].startswith("results/phase-6/e6.19-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S16_THEOREMS) == {"bsd-panel-satisfaction"}
    assert S16_THEOREMS["bsd-panel-satisfaction"]["parts"] == ("statement-def", "vanish-def", "rank-def")
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:08": ["bsd-panel-satisfaction", ["statement-def", "vanish-def", "rank-def"]],
    }
    # the honest-turn bytes (D-e6k: the missing-parts probe names the
    # full part-set with the one untaught slug; the scaffold lists both
    # missing parts in the sanctioned order)
    assert FROZEN["missing_parts_failure"] == {
        "S02:17": "needs_info: i have not been taught the statement-def — the rule for bsd-panel-satisfaction needs it before i can put it together"
    }
    assert "short the vanish-def and the rank-def" in FROZEN["scaffold_failures"]["S03:03"]


def test_walls_bytes() -> None:
    # the four walls are the Brainstem class attributes, byte-frozen:
    # S03:11/S03:12 W-S16-1 (the descent of record, both members),
    # S03:13 W-S16-2 (the L-value of record, no new decimal),
    # S03:14 W-S16-3 (the panel's completeness)
    wall_attrs = {
        "S03:11": Brainstem.W_S16_1,
        "S03:12": Brainstem.W_S16_1,
        "S03:13": Brainstem.W_S16_2,
        "S03:14": Brainstem.W_S16_3,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the L-value wall names the leading coefficient WITHOUT its digit
    # string (the no-new-decimals rule): and none of the walls carries
    # any new off-line decimal (the carried 13.3586546916 stays in
    # W-S14-5's band, never resurfaced here)
    for _wall in FROZEN["walls_honest"].values():
        assert "13.3586546916" not in _wall
        assert "0.3059" not in _wall
    # no honest-zero bytes (the S16 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The 18 on-line beds re-derive against the mechanism's own
    references (never hand-written values)."""
    # the panel identity of the record
    assert _bsd_py_which(B14_A) == "A" and _bsd_py_which(B14_B) == "B"
    # the descent arithmetic (the exact sequence with trivial shaf):
    # bound = selmer dim - two-torsion dim, on both members
    for tag in ("A", "B"):
        assert S16_BEDS["descend_bound"][tag] == S16_BEDS["selmer_dim"][tag] - S16_BEDS["e2_dim"][tag], tag
        assert S16_BEDS["sha2_dim"][tag] == 0, tag
    # the POINT LEDGERS: A's three torsion points; B's generator with
    # ten of ten covered
    assert _bsd_py_torsion_points(B14_A) == [tuple(p) for p in S16_BEDS["torsion_A"]]
    assert _bsd_py_gen_ledger(B14_B) == S16_BEDS["gen_B"]
    # the LINE'S SIDE: the exact partials, re-derived off the mechanism
    assert Fraction(S16_BEDS["uniform_84_A"]) == _bsd_py_lpartial_uniform(*B14_A)
    assert Fraction(S16_BEDS["record_84_B"]) == _bsd_py_lpartial_record(*B14_B)
    assert Fraction(S16_BEDS["uniform_84_A"]) != 0  # the order-zero side stands nonzero
    assert Fraction(S16_BEDS["record_84_B"]) > 1  # the order-one side stands far from zero
    # the order/rank beds name the records (the house wording)
    assert "order zero of vanishing" in FROZEN["beds_exact"]["S02:05"]
    assert "order one" in FROZEN["beds_exact"]["S02:06"]
    assert "rank of the first panel member is zero" in FROZEN["beds_exact"]["S02:09"]
    assert "rank of the second panel member is one" in FROZEN["beds_exact"]["S02:10"]
    assert "no B S D is used" in FROZEN["beds_exact"]["S02:09"]  # the descent settles WITHOUT the statement
    assert "no B S D is used" in FROZEN["beds_exact"]["S02:10"]
    # the summit satisfaction beds
    assert "order zero equals the rank zero" in FROZEN["beds_exact"]["S03:09"]
    assert "order one equals the rank one" in FROZEN["beds_exact"]["S03:10"]
    assert "clay millennial booklet" in FROZEN["beds_exact"]["S03:05"]  # the declared record source


def test_statement_is_the_cmi_verbatim() -> None:
    """The summit fact stores the BSD statement declared from its
    record source (the clay millennial booklet, the wiles chapter):
    the verbatim core of the statement stands in the lesson phrase
    and in the stored fact bytes."""
    statement = next(p for p, (_c, s, _k, _es, _d, _l) in S16_LESSONS.items() if s == "statement-def")
    # the house-voiced core of the CMI 2000 booklet statement
    # (verbatim, lettered, lowercased — the store voice)
    assert (
        "in the taylor expansion of its L-product at s equal to one, the order r of vanishing equals the algebraic rank"
        in statement
    )
    assert "c times (s minus 1) to the power r" in statement
    assert "c not zero, r equals the rank of the group of rational points" in statement
    # the record source named in the fact
    assert "clay millennial booklet" in statement and "wiles chapter" in statement
    # the record's two sides (the iff form of the statement)
    assert "the L-product at s equal to one is zero if and only if there are infinitely many rational points" in statement
    # the derivation files it on the panel (the composition statement)
    comp = S16_THEOREMS["bsd-panel-satisfaction"]["statement"]
    assert "order zero of vanishing equals the rank zero" in comp
    assert "order one of vanishing equals the rank one" in comp


def test_offline_values_never_store_answers() -> None:
    """S16 brings NO new off-line value: expect.offline_watch is
    empty, the leading coefficient is named without its digits, and
    the carried 13.3586546916 never resurfaces in an S16 answer."""
    with open("bands/spec-e6.20.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    watch = ["13.3586546916", "0.3059997738"]
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        for w in watch:
            assert w not in str(v), f"off-line value {w!r} floated into an on-line answer"
    for v in list(FROZEN["walls_honest"].values()):
        for w in watch:
            assert w not in v, "a carried off-line witness must not move into an S16 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the SIX carry rows (P6: byte-identical to the seed store):
    # the S15 record-partial carry (height 83), the ramification
    # correction, the S14 L-partial carry, the S15 factor carry,
    # the W-S15 BSD-touch WALL, and the queue
    assert FROZEN["seam_carry_refs"] == ["S04:01", "S04:02", "S04:03", "S04:04", "S04:05", "S04:06"]
    # the carried wall row stays honest (P3 wall-carried)
    assert FROZEN["derived_table"]["S04:05"].startswith("needs_info: this band does not state the BSD")
    # the off-script kstbound standing check (the savant soil)
    assert FROZEN["offscript_carry"] == {"state the kstbound rule": "because two unit circles meet in at most two points the unit pair graph of a "
        "planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs "
        "at a constant times n to the three halves power"}
    # the seam crosscheck expected value
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"


def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]


def test_probe_grammar_classifies() -> None:
    # the full 51-surface map (det_classify is the referee)
    plain = {
        "S02:01": "s16-order", "S02:02": "s16-rank",
        "S02:05": "s16-order", "S02:06": "s16-order",
        "S02:09": "s16-rank", "S02:10": "s16-rank",
        "S02:11": "s16-selmer", "S02:12": "s16-selmer",
        "S02:13": "s16-torsion", "S02:14": "s16-gen",
        "S02:15": "s16-descend", "S02:16": "s16-descend",
        "S02:17": "derive",
        "S03:03": "derive", "S03:05": "s16-bsd", "S03:06": "s16-reach",
        "S03:07": "s16-consistent", "S03:08": "derive",
        "S03:09": "s16-sides", "S03:10": "s16-sides",
        "S03:11": "s16-selwall", "S03:12": "s16-selwall",
        "S03:13": "s16-lvalwall", "S03:14": "s16-panel",
        "S03:15": "s16-bandstate", "S03:17": "s16-uncond",
        "S04:01": "s15-recpartial", "S04:02": "s15-corr",
        "S04:03": "s14-lpar", "S04:04": "s15-factor",
        "S04:05": "s15-bsd-touch", "S04:06": "s12-queue",
        "S04:07": "s16-order", "S04:08": "s16-rank",
        "S04:09": "s16-bsd", "S04:10": "s16-reach",
        "S04:11": "s16-consistent", "S04:13": "s16-gen",
        "S04:14": "s16-sides", "S04:15": "s16-torsion",
        "S04:16": "s16-bandstate", "S04:17": "s16-order",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:03": "vanish-def",
        "S02:07": "rank-def",
        "S03:01": "statement-def",
        "S03:16": "bsd-panel-satisfaction",
        "S04:12": "reach-def",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", "s16-state", want), ref
    assertion_turns = ["S02:04", "S02:08", "S03:02", "S03:04"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what does the first panel member's L product hold at my line end?")[1]["mode"] == "s14-lpar"
    assert det_classify("what does the record L product of the second panel member hold at height 83?")[1]["mode"] == "s15-recpartial"
    assert det_classify("does this band state the BSD?")[1]["mode"] == "s15-bsd-touch"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("state the kstbound rule")[1]["mode"] == "lem-state"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: the summit's own state readout cites the summit
    # composition; the queue carry row cites the carried queue theorem
    assert FROZEN["theorem_allowed"] == {
        "S03:16": ["bsd-panel-satisfaction"],
        "S04:06": ["queue-declared"],
    }
    # the full sanctioned DAG: thirty-four theorem facts (the S15
    # thirty-three + the summit composition)
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 34
    assert "theorem:bsd-panel-satisfaction" in dag
    assert "theorem:bsd" not in dag, "the bare conj id must NOT exist (the summit is the declared record fact + the composition)"


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH
    assert SCRIPT_HASH == "4baa6bc6579d62fd"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:11": ["selmer", "line end 84"],
        "S03:12": ["selmer", "line end 84"],
        "S03:13": ["leading coefficient", "line end 84"],
        "S03:14": ["conductor", "line end 84"],
    }


def test_band_map_frozen_untouched() -> None:
    # the BSD island is research-adjacent: the frozen bands-map
    # (S10) stays untouched; e6.20 validates the map as-is against
    # the extended registry.
    from kainos.tutor.bands import BAND_MAP
    from kainos.tutor.e620 import CONCEPTS_E620

    domains = {d for b in BAND_MAP for d in b.domains}
    assert "bsd" not in domains, "the band map is frozen at S10 — no new band entries"
    assert len(CONCEPTS_E620) == 104  # the S15 100 + the four summit concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (the D-e6k family:
    # the missing-parts byte and the scaffold byte both show through
    # here as F turns; no ambiguous letters)
    assert FROZEN["domain_sequence"] == {2: "UUULSSULSSSSSSSSF", 3: "ULFLSSSTSSHHHHSSS", 4: "SSSSHSSSSSSSSSSSS"}
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"
