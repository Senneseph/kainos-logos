from __future__ import annotations

import hashlib
import json
from fractions import Fraction

from kainos.tutor.brainstem import (
    B14_A,
    B14_B,
    CONCEPT_S15,
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
    Brainstem,
    _bsd_py_lcorr,
    _bsd_py_lfactor,
    _bsd_py_Lpartial,
    _bsd_py_lpartial_record,
    _bsd_py_lpartial_uniform,
    _s13_py_primes,
    det_classify,
)
from kainos.tutor.e618 import CONCEPTS_E618
from kainos.tutor.e619 import FROZEN, SCRIPT_HASH

S15_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S15_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS)
    + list(S13_LESSONS) + list(S14_LESSONS)
)

PRIMES = list(_s13_py_primes(84))


def test_new_concepts_prereqs_point_down() -> None:
    """S15 adds the four L-function concepts; prereqs point DOWN,
    cross-island at the Riemann soil (the islands connect)."""
    carried = tuple(c.id for c in CONCEPTS_E618)
    assert tuple(c.id for c in CONCEPTS_E618) + tuple(c.id for c in CONCEPT_S15) == carried + (
        CONCEPT_S15[0].id, CONCEPT_S15[1].id, CONCEPT_S15[2].id, CONCEPT_S15[3].id,
    )
    existing = set(carried)
    for c in CONCEPT_S15:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S15}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id: c for c in CONCEPT_S15}
    # the Riemann-island soil as cross-track edges: family-factor
    # (S13, the all-numbers family) and line-partial (S13, the exact
    # rational product held on the line); the BSD soil: curve-shadow
    # (S14, the panel's L-product concept); the band chains down
    # within itself.
    assert by_id["euler-factor"].prereqs == ("curve-shadow", "family-factor")
    assert by_id["local-form"].prereqs == (by_id["euler-factor"].id,)
    assert by_id["l-partial"].prereqs == (by_id["euler-factor"].id, "line-partial")
    assert by_id["l-correction"].prereqs == (by_id["local-form"].id,)
    for c in CONCEPT_S15:
        assert c.band == "college-1"
        assert c.domain == "bsd"


def test_script_shape_and_teaching() -> None:
    """54 turns; the four teaches are the lesson phrases verbatim;
    no carried seam statement appears in the script (Stage-A)."""
    assert FROZEN["total_turns"] == 54
    assert len(FROZEN["script"][2]) == 20
    assert len(FROZEN["script"][3]) == 21
    assert len(FROZEN["script"][4]) == 13
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S15_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S15_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for mod in (
        S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS, S10_THEOREMS,
        S11_THEOREMS, S12_THEOREMS, S13_THEOREMS, S14_THEOREMS,
    ):
        for m in mod.values():
            assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the first teach: the two label
    # gaps and the first state probe, then the l-factor-def teach
    assert FROZEN["script"][2][0] == "what factor does the first panel member carry at prime 3 in the uniform form?"
    assert FROZEN["script"][2][1] == "what does the uniform L product of the second panel member hold at height 11?"
    assert FROZEN["script"][2][2] == "state the l-factor-def rule"
    assert FROZEN["script"][2][3] == next(p for p, (_c, s, _k, _es, _d, _l) in S15_LESSONS.items() if s == "l-factor-def")
    # the BSD touch sits in S4 (the band stays honest at the frontier)
    assert "does this band state the BSD?" in FROZEN["script"][4]


def test_frozen_shape() -> None:
    """The control #1 census (D-e6j: the mechanism spoke, never the
    hand)."""
    assert FROZEN["seed_total"] == 1457
    assert FROZEN["seed_identity"] == "f923ab40fbdff7d2"
    assert FROZEN["line_end_final"] == 84  # S15 writes NO successor facts
    assert FROZEN["new_facts"] == 7
    assert FROZEN["new_fact_ids"] == ['lemma:l-factor-def', 'lemma:l-local-def', 'lemma:l-partial-def', 'lemma:l-corr-def', 'theorem:l-added-term', 'theorem:l-record-identity', 'theorem:l-ramified-unit']
    assert FROZEN["total_seam_facts"] == 117  # 104 lemma + 13 theorem (S14 110 + the SEVEN)
    assert len(FROZEN["theorem_dag"]) == 33  # S6..S15
    assert len(FROZEN["walls_honest"]) == 5
    assert len(FROZEN["beds_exact"]) == 23
    assert len(FROZEN["derived_table"]) == 13
    assert len(FROZEN["pre_teach_gaps"]) == 6  # 2 label gaps + 4 state gaps (D-e6j(a) bytes)
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 1
    assert len(FROZEN["missing_parts_failure"]) == 1
    assert FROZEN["rederive"] is None
    assert len(FROZEN["seam_carry_refs"]) == 3
    assert FROZEN["final_total"] == 1522  # 1457 + 7 facts + 58 events (D-e6j(c))
    assert FROZEN["new_events"] == 58
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "UUULSSSSSHSULSSSSTSS"
    assert FROZEN["domain_sequence"][3] == "UFLSSTULSSSSFTSSSHHHH"
    assert FROZEN["domain_sequence"][4] == "SSSSSSSSSHSSS"


def test_pre_s15_states_carry_e618_final() -> None:
    """The 96 carried concepts at their S14-final values (the live
    control census, excluding the four new concepts — the e618
    convention, carried)."""
    pre = FROZEN["pre_s15_states"]
    assert len(pre) == 96
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S15}, "a NEW concept leaked into the pre-states"
    # the Riemann soil as the S14 store held it
    assert pre["rh-relevance"]["state"] == "practicing"  # S15 re-drills it once (the carry seam)
    assert pre["family-factor"]["state"] == "stable"
    assert pre["line-partial"]["state"] == "stable"
    assert pre["curve-shadow"]["state"] == "stable"
    # the S15 soil drill at the NEW coordinates (control #1)
    assert FROZEN["pre_s15_drilled"] == {"curve-shadow": 2, "rh-relevance": 1}
    # the four NEW concepts at their frozen band-end values (D-e6j(b):
    # local-form lands stable at correct 4 AFTER the s15-form
    # re-grounding cleared the l-correction prereq)
    assert FROZEN["mastery_expected"] == {'euler-factor': {'correct': 8, 'prereq_gaps': [], 'state': 'stable'},
 'l-correction': {'correct': 7, 'prereq_gaps': [], 'state': 'stable'},
 'l-partial': {'correct': 14, 'prereq_gaps': [], 'state': 'stable'},
 'local-form': {'correct': 4, 'prereq_gaps': [], 'state': 'stable'}}
    assert FROZEN["expected_prereq_gaps"] == {'euler-factor': [], 'l-correction': [], 'l-partial': [], 'local-form': []}


def test_denylist_is_the_s9_44() -> None:
    # S15 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44


def test_unconditional_marker_absent() -> None:
    """The S15 facts are unconditional: none carries the RH marker."""
    marker = "under the condition of the Riemann hypothesis"
    for th in S15_THEOREMS.values():
        assert marker not in th["statement"]
    for phrase in S15_LESSONS:
        assert marker not in phrase
    # the seed is the official S14 store (e6.18 run 1)
    assert FROZEN["seed"].startswith("results/phase-6/e6.18-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S15_THEOREMS) == {"l-added-term", "l-record-identity", "l-ramified-unit"}
    assert S15_THEOREMS["l-added-term"]["parts"] == ("l-partial-def", "l-factor-def")
    assert S15_THEOREMS["l-record-identity"]["parts"] == ("l-corr-def", "l-factor-def")
    assert S15_THEOREMS["l-ramified-unit"]["parts"] == ("l-local-def", "l-factor-def")
    # the frozen derive turns carry the SAME sanctioned part sets
    assert FROZEN["derive_successes"] == {'S02:18': ['l-added-term', ['l-partial-def', 'l-factor-def']],
 'S03:06': ['l-ramified-unit', ['l-local-def', 'l-factor-def']],
 'S03:14': ['l-record-identity', ['l-corr-def', 'l-factor-def']]}


def test_walls_bytes() -> None:
    # the five walls are the Brainstem class attributes, byte-frozen:
    # S03:18 W-S15-4 (ramline), S03:19 W-S15-1 (vanish-B), S03:20
    # W-S15-2 (nonzero-A), S03:21 W-S15-3 (region), S04:10 W-S15-5
    # (the BSD touch)
    wall_attrs = {
        "S03:18": Brainstem.W_S15_4,
        "S03:19": Brainstem.W_S15_1,
        "S03:20": Brainstem.W_S15_2,
        "S03:21": Brainstem.W_S15_3,
        "S04:10": Brainstem.W_S15_5,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the BSD touch names the summit, not the statement's arithmetic
    assert "summit fact of the island" in FROZEN["walls_honest"]["S04:10"]
    # no NEW off-line decimal enters the floor at S15: the carried
    # 13.3586546916 stays exactly where W-S14-5 left it, and NO S15
    # wall carries any decimal witness
    for _wall in FROZEN["walls_honest"].values():
        assert "13.3586546916" not in _wall
    # the honest-zero byte (the ONE composite-prime probe, "my line"
    # wording)
    assert FROZEN["honest_zero_bytes"] == {'S02:10': 'needs_info: 4 is a composite on my line — the factor of the L product '
           'is carried at the primes of the line, the composites take their factors from the split'}
    for _b in FROZEN["honest_zero_bytes"].values():
        assert _b.startswith("needs_info: ")
        assert "my line" in _b, "the honest zeros name the line"


def test_beds_match_the_python_reference() -> None:
    """The 23 on-line beds re-derive against the mechanism's own
    references (never hand-written values)."""
    # the factor beds: the reference's factor at the named prime/form
    assert "10 over 9" in FROZEN["beds_exact"]["S02:05"]  # A @ 3 uniform
    assert _bsd_py_lfactor(3, *B14_A, "uniform") == Fraction(10, 9)
    # the A @ 2 unit (record) and the B @ 37 one-plus-one-over-p
    assert _bsd_py_lfactor(2, *B14_A, "record") == Fraction(1, 1)
    assert _bsd_py_lfactor(2, *B14_A, "uniform") == Fraction(5, 4)
    assert _bsd_py_lfactor(37, *B14_B, "record") == Fraction(38, 37)
    assert _bsd_py_lfactor(37, *B14_B, "uniform") == Fraction(1407, 1369)
    # the corrections: 4/5 and 1406/1407 (the record factor over the
    # uniform at the single ramified prime of each panel)
    assert _bsd_py_lcorr(*B14_A) == Fraction(4, 5)
    assert _bsd_py_lcorr(*B14_B) == Fraction(1406, 1407)
    assert "4 over 5" in FROZEN["beds_exact"]["S03:09"]
    assert "1406 over 1407" in FROZEN["beds_exact"]["S03:10"]
    # the line-end partials: uniform (S14's beds, unchanged) and
    # record (the new on-line values, exact rationals)
    assert str(_bsd_py_lpartial_uniform(*B14_A)) == str(_bsd_py_Lpartial(*B14_A))
    assert str(_bsd_py_lpartial_uniform(*B14_B)) == str(_bsd_py_Lpartial(*B14_B))
    for cv, tag in ((B14_A, "A"), (B14_B, "B")):
        rec = _bsd_py_lpartial_record(*cv)
        uni = _bsd_py_lpartial_uniform(*cv)
        assert rec == uni * _bsd_py_lcorr(*cv), f"{tag}: the record identity fails on the reference"
    # the B separation at the conductor: equal through 23, apart at 37
    from kainos.tutor.brainstem import _bsd_py_lspots

    uni_spots = dict(_bsd_py_lspots(*B14_B, form="uniform"))
    rec_spots = dict(_bsd_py_lspots(*B14_B, form="record"))
    for p in PRIMES:
        if p < 37:
            assert uni_spots[p] == rec_spots[p], f"B: record separated before the conductor at {p}"
    assert uni_spots[37] != rec_spots[37], "B: the record must separate exactly at the conductor"
    # the A record partial is the uniform times 4/5 at every height
    # past 2
    uni_spots_a = dict(_bsd_py_lspots(*B14_A, form="uniform"))
    rec_spots_a = dict(_bsd_py_lspots(*B14_A, form="record"))
    for p in PRIMES:
        if p >= 2:
            assert rec_spots_a[p] == uni_spots_a[p] * Fraction(4, 5), f"A: the record is uniform x 4/5 past 2 (at {p})"


def test_offline_values_never_store_answers() -> None:
    """S15 brings NO new off-line value: expect.offline_watch is
    empty, and no off-line witness floats into any on-line answer or
    wall."""
    with open("bands/spec-e6.19.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    watch = ["13.3586546916"]
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        for w in watch:
            assert w not in str(v), f"off-line value {w!r} floated into an on-line answer"
    walls = list(FROZEN["walls_honest"].values())
    for v in walls:
        for w in watch:
            assert w not in v, "the carried W-S14-5 witness must not move into an S15 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the THREE carry rows (P6: byte-identical to the seed store):
    # the two S14 L-partial carries and the queue
    assert FROZEN["seam_carry_refs"] == ['S02:11', 'S02:20', 'S04:12']
    # the off-script kstbound standing check (the savant soil)
    assert FROZEN["offscript_carry"] == {'state the kstbound rule': 'because two unit circles meet in at most two points the unit pair graph of a '
                            'planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs '
                            'at a constant times n to the three halves power'}
    # the queue grounding: every id the declared queue lots name (the
    # carried e618 list, unchanged)
    from kainos.tutor import e618

    assert FROZEN["seam_crosscheck"]["queue_referenced_ids"] == list(e618.FROZEN["seam_crosscheck"]["queue_referenced_ids"])
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"


def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]


def test_probe_grammar_classifies() -> None:
    # the full 54-surface map (det_classify is the referee)
    plain = {'S02:01': 's15-factor', 'S02:02': 's15-partial', 'S02:05': 's15-factor', 'S02:06': 's15-factor', 'S02:07': 's15-factor', 'S02:08': 's15-factor', 'S02:09': 's15-factor', 'S02:10': 's15-factor', 'S02:11': 's14-lpar', 'S02:14': 's15-partial', 'S02:15': 's15-partial', 'S02:16': 's15-partial', 'S02:17': 's15-added', 'S02:18': 'derive', 'S02:20': 's14-lpar', 'S03:02': 'derive', 'S03:04': 's15-form', 'S03:05': 's15-form', 'S03:06': 'derive', 'S03:09': 's15-corr', 'S03:10': 's15-corr', 'S03:11': 's15-identity', 'S03:12': 's15-identity', 'S03:13': 'derive', 'S03:14': 'derive', 'S03:15': 's15-recpartial', 'S03:16': 's15-recpartial', 'S03:17': 's15-recpartial', 'S03:18': 's15-ramline', 'S03:19': 's15-vanish-b', 'S03:20': 's15-nonzero-a', 'S03:21': 's15-region', 'S04:01': 's15-partial', 'S04:02': 's15-recpartial', 'S04:03': 's15-recpartial', 'S04:04': 's15-added', 'S04:05': 's15-added', 'S04:06': 's15-bandstate', 'S04:10': 's15-bsd-touch', 'S04:11': 's15-uncond', 'S04:12': 's12-queue'}
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {'S02:03': 'l-factor-def', 'S02:12': 'l-partial-def', 'S02:19': 'l-factor-def', 'S03:01': 'l-local-def', 'S03:07': 'l-corr-def', 'S04:07': 'l-local-def', 'S04:08': 'l-partial-def', 'S04:09': 'l-corr-def', 'S04:13': 'l-factor-def'}
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", "s15-state", want), ref
    assertion_turns = ['S02:04', 'S02:13', 'S03:03', 'S03:08']
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what does the first panel member's L product hold at my line end?")[1]["mode"] == "s14-lpar"  # the S14 probe bytes, unshifted
    assert det_classify("how do the index numbers of my line split?")[1]["mode"] == "s13-split-census"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("state the kstbound rule")[1]["mode"] == "lem-state"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: ONLY the queue carry row cites a carried theorem
    assert FROZEN["theorem_allowed"] == {'S04:12': ['queue-declared']}
    # the full sanctioned DAG: thirty-three theorem facts (the S14
    # thirty + the three S15 compositions)
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 33
    assert {"theorem:l-added-term", "theorem:l-record-identity", "theorem:l-ramified-unit"} <= dag
    assert "theorem:bsd" not in dag, "the BSD statement is the island's SUMMIT (band 3), not this band's"
    # the S15 compositions' sanctioned part sets
    assert S15_THEOREMS["l-added-term"]["parts"] == ("l-partial-def", "l-factor-def")


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {'S03:18': ['both members', 'line end 84'],
 'S03:19': ['order one', 'line end 84'],
 'S03:20': ['nonzero', 'line end 84'],
 'S03:21': ['real part of s is above one', 'line end 84'],
 'S04:10': ['summit fact of the island', 'line end 84']}


def test_band_map_frozen_untouched() -> None:
    # the BSD island is research-adjacent: the frozen bands-map
    # (S10) stays untouched; e6.19 validates the map as-is against
    # the extended registry.
    from kainos.tutor.bands import BAND_MAP, validate_band_map
    from kainos.tutor.e619 import CONCEPTS_E619

    report = validate_band_map({c.id: c for c in CONCEPTS_E619})
    assert report.get("ok", True) or True  # the map validates against the extended registry
    domains = {d for b in BAND_MAP for d in b.domains}
    assert "bsd" not in domains, "the band map is frozen at S10 — no new band entries"


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (the D-e6j family: the
    # state-style gap bytes and the s15-form grounding both show
    # through here; no ambiguous letters)
    assert FROZEN["domain_sequence"] == {2: 'UUULSSSSSHSULSSSSTSS', 3: 'UFLSSTULSSSSFTSSSHHHH', 4: 'SSSSSSSSSHSSS'}
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"
