from __future__ import annotations

import hashlib
import json

from kainos.tutor.brainstem import (
    CONCEPT_S19,
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
    S17_LESSONS,
    S17_THEOREMS,
    S18_LESSONS,
    S18_THEOREMS,
    S19_BEDS,
    S19_LESSONS,
    S19_THEOREMS,
    Brainstem,
    _pnp_py_parity_terms,
    _pnp_py_parity_verify,
    det_classify,
)
from kainos.tutor.e622 import CONCEPTS_E622
from kainos.tutor.e623 import CONCEPTS_E623, FROZEN, SCRIPT_HASH

S19_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S19_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS)
    + list(S13_LESSONS) + list(S14_LESSONS) + list(S15_LESSONS)
    + list(S16_LESSONS) + list(S17_LESSONS) + list(S18_LESSONS)
)


def test_new_concepts_prereqs_point_down() -> None:
    """S19 adds the four difficulty-line concepts; prereqs point DOWN
    (the S18 soil: the cost counter; the band's own edges: the np
    class over the p class + the cost counter, the summit over the
    np class, the size shadow over the summit + the np class)."""
    carried = tuple(c.id for c in CONCEPTS_E622)
    assert tuple(c.id for c in CONCEPTS_E623) == carried + (
        CONCEPT_S19[0].id, CONCEPT_S19[1].id, CONCEPT_S19[2].id, CONCEPT_S19[3].id,
    )
    existing = set(carried)
    for c in CONCEPT_S19:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S19}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id: c for c in CONCEPT_S19}
    assert by_id["class-p"].prereqs == ("cost-counter",)
    assert by_id["class-np"].prereqs == ("class-p", "cost-counter")
    assert by_id["pnp-summit"].prereqs == ("class-np",)
    assert by_id["size-shadow"].prereqs == ("pnp-summit", "class-np")
    for c in CONCEPT_S19:
        assert c.band == "college-1"
        assert c.domain == "pnp"


def test_script_shape_and_teaching() -> None:
    """51 turns; the four teaches are the lesson phrases verbatim;
    no carried seam statement appears in the script (Stage-A)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S19_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S19_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for mod in (
        S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS, S10_THEOREMS,
        S11_THEOREMS, S12_THEOREMS, S13_THEOREMS, S14_THEOREMS, S15_THEOREMS,
        S16_THEOREMS, S17_THEOREMS, S18_THEOREMS,
    ):
        for m in mod.values():
            assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the first teach (S2:01-02, then
    # the teach at S2:03 — two gaps, the S19 shape)
    assert FROZEN["script"][2][0] == "is dividing a question in p on my line?"
    assert FROZEN["script"][2][1] == "state the p-class-def rule"
    assert (
        FROZEN["script"][2][2]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S19_LESSONS.items() if s == "p-class-def")
    )
    assert FROZEN["script"][3][0] == "how many terms does the smallest dnf of parity at four variables need?"
    # the one sanctioned composition, derived in-band on the strict
    # part set (the scaffold first names only the shadow part)
    assert "derive parity-blowup-filed from parity-shadow-def and np-class-def" in script_lines
    assert "derive parity-blowup-filed from parity-shadow-def" in script_lines
    # the S18 soil carries (the island connects through the soil)
    assert "state the line-pi-reduction rule" in script_lines
    assert "what is the statement of the beal island of record?" in script_lines


def test_frozen_shape() -> None:
    """The control #1 census (the mechanism spoke, never the hand —
    D-e6n: the pnp-summit mastery is six, the S4 letters shift by one
    against the pre-registration)."""
    assert FROZEN["seed_total"] == 1698
    assert FROZEN["seed_identity"] == "60851c661832f306"
    assert FROZEN["line_end_final"] == 84  # S19 writes NO successor facts
    assert FROZEN["new_facts"] == 5
    assert FROZEN["new_fact_ids"] == [
        "lemma:p-class-def",
        "lemma:np-class-def",
        "lemma:pnp-def",
        "lemma:parity-shadow-def",
        "theorem:parity-blowup-filed",
    ]
    assert FROZEN["total_seam_facts"] == 138  # 122 lemma + 16 theorem (S18 133 + the FIVE)
    assert len(FROZEN["theorem_dag"]) == 38  # S6..S19
    assert len(FROZEN["walls_honest"]) == 4
    assert len(FROZEN["beds_exact"]) == 16
    assert len(FROZEN["derived_table"]) == 18  # the derive + the seventeen S4 rows
    assert len(FROZEN["pre_teach_gaps"]) == 8  # the eight pre-lesson gaps
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 1
    assert len(FROZEN["missing_parts_failure"]) == 0
    assert FROZEN["rederive"] is None
    assert FROZEN["seam_carry_refs"] == ["S04:01", "S04:02", "S04:03", "S04:04", "S04:05", "S04:06", "S04:07"]
    assert FROZEN["final_total"] == 1756  # 1698 + 5 facts + 53 events (D-e6n(b))
    assert FROZEN["new_events"] == 53
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "UULSSUULSSSUULSSS"
    assert FROZEN["domain_sequence"][3] == "UULSSSSFTSSHHHHSS"
    assert FROZEN["domain_sequence"][4] == "SHSSHSSSSSSSSSSSH"


def test_pre_s19_states_carry_e622_final() -> None:
    """The 112 carried concepts at their S18-final values (the live
    control census, excluding the four new concepts — the e621
    convention, carried)."""
    pre = FROZEN["pre_s19_states"]
    assert len(pre) == 112
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S19}, "a NEW concept leaked into the pre-states"
    # the S18 decidable soil the difficulty line stands on
    assert pre["decision-question"] == {"state": "stable", "correct": 7}
    assert pre["tamable-machine"] == {"state": "stable", "correct": 4}
    assert pre["reduction"] == {"state": "stable", "correct": 9}
    assert pre["cost-counter"] == {"state": "stable", "correct": 10}
    # the S17 Beal soil as the S18 store held it
    assert pre["beal-summit"] == {"state": "stable", "correct": 5}
    assert pre["beal-census"] == {"state": "stable", "correct": 11}
    assert pre["l-correction"] == {"state": "stable", "correct": 10}
    assert pre["rh-relevance"]["state"] == "practicing"  # the store held it practicing (17 correct)
    # the S11 soil the whole track stands on
    assert pre["first-divisor"] == {"state": "stable", "correct": 36}
    assert pre["divides"] == {"state": "stable", "correct": 5}
    assert pre["scan-ledger"] == {"state": "stable", "correct": 12}
    # the S14/S16 BSD soil the island chain carries
    assert pre["curve-shadow"] == {"state": "stable", "correct": 12}
    assert pre["bsd-summit"] == {"state": "stable", "correct": 11}
    # the S17 valuation soil the Beal island closed on
    assert pre["valuation"] == {"state": "stable", "correct": 6}
    assert pre["lte-form"] == {"state": "stable", "correct": 7}
    # the S19 soil drill at the NEW coordinates (control #1: the S4
    # carries re-anchor the S18 line-pi/reduction rows, the S17 beal
    # and correction rows, and the S8 relevance row)
    assert FROZEN["pre_s19_drilled"] == {
        "beal-summit": 1,
        "bsd-summit": 1,
        "l-correction": 1,
        "reduction": 1,
        "rh-relevance": 1,
    }
    # the four NEW concepts at their frozen band-end values (all
    # stable: the four-correct-derivation rule held for each)
    assert FROZEN["mastery_expected"] == {
        "class-p": {"correct": 4, "prereq_gaps": [], "state": "stable"},
        "class-np": {"correct": 5, "prereq_gaps": [], "state": "stable"},
        "pnp-summit": {"correct": 6, "prereq_gaps": [], "state": "stable"},
        "size-shadow": {"correct": 11, "prereq_gaps": [], "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "class-p": [],
        "class-np": [],
        "pnp-summit": [],
        "size-shadow": [],
    }


def test_denylist_is_the_s9_44() -> None:
    # S19 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44


def test_unconditional_marker_absent() -> None:
    """The S19 facts are the unconditional difficulty band: none
    carries the RH marker; the uncond probe says so of record on the
    line."""
    marker = "under the condition of the Riemann hypothesis"
    for th in S19_THEOREMS.values():
        assert marker not in th["statement"]
    for phrase in S19_LESSONS:
        assert marker not in phrase
    # the seed is the official S18 store (e6.22 run 1)
    assert FROZEN["seed"].startswith("results/phase-6/e6.22-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S19_THEOREMS) == {"parity-blowup-filed"}
    assert S19_THEOREMS["parity-blowup-filed"]["parts"] == ("parity-shadow-def", "np-class-def")
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:09": ["parity-blowup-filed", ["parity-shadow-def", "np-class-def"]],
    }
    # the honest-turn bytes: the scaffold names the single short part
    # (the np-class-def), before the sanctioned derive puts the rule
    # together on the exact set
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the np-class-def" in FROZEN["scaffold_failures"]["S03:08"]


def test_walls_bytes() -> None:
    # the four walls are the Brainstem class attributes, byte-frozen:
    # S03:12 W-S19-1 (relativization), S03:13 W-S19-2 (algebrization),
    # S03:14 W-S19-3 (natural proofs), S03:15 W-S19-4 (AC0)
    wall_attrs = {
        "S03:12": Brainstem.W_S19_1,
        "S03:13": Brainstem.W_S19_2,
        "S03:14": Brainstem.W_S19_3,
        "S03:15": Brainstem.W_S19_4,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the no-new-decimals rule: the off-line territory is named at its
    # record place, never as a value of the line
    import re as _re
    for _wall in list(FROZEN["walls_honest"].values()) + [
        Brainstem.W_S19_1, Brainstem.W_S19_2, Brainstem.W_S19_3, Brainstem.W_S19_4,
    ]:
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry an off-line digit string"
    assert "baker-gill-solovay" in Brainstem.W_S19_1
    assert "aaronson-wigderson" in Brainstem.W_S19_2 and "chen-hu-ren" in Brainstem.W_S19_2
    assert "razborov-rudich" in Brainstem.W_S19_3
    assert "razborov-smolensky" in Brainstem.W_S19_4 and "shannon" in Brainstem.W_S19_4
    # no honest-zero bytes (the S19 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}
    # the S4 algebrization reprobe re-emits the SAME wall byte
    assert FROZEN["derived_table"]["S04:17"] == "needs_info: " + Brainstem.W_S19_2


def test_beds_match_the_python_reference() -> None:
    """The 16 on-line bed rows re-derive against the mechanism's own
    references (never hand-written values)."""
    # the PARITY CENSUS: the table of 2^(k-1), verified end-to-end by
    # the mechanism's own walk
    for k in range(1, 17):
        assert S19_BEDS["parity"][k] == 2 ** (k - 1) == _pnp_py_parity_terms(k), k
    assert S19_BEDS["rows16"] == 65536
    assert S19_BEDS["shannon16"] == 4096 == 2 ** 16 // 16
    _pnp_py_parity_verify(16)  # the structural census check, 1..16 (raises on mismatch)
    # the p answers (the S18 soil inside the S19 band)
    assert "yes — dividing is a p question on my line" in FROZEN["beds_exact"]["S02:04"]
    assert "one hundred ninety-two candidate steps" in FROZEN["beds_exact"]["S02:05"]
    # the census rows
    assert "eight of record" in FROZEN["beds_exact"]["S03:04"]
    assert "one hundred twenty-eight of record" in FROZEN["beds_exact"]["S03:05"]
    assert "five hundred twelve of record" in FROZEN["beds_exact"]["S03:06"]
    assert "exactly the same as the terms of its smallest dnf" in FROZEN["beds_exact"]["S03:07"]
    assert "thirty-two thousand seven hundred sixty-eight of record" in FROZEN["beds_exact"]["S03:10"]
    assert "the sixty-five thousand five thousand" not in FROZEN["beds_exact"]["S03:11"]
    assert "the sixty-five thousand five hundred thirty-six rows" in FROZEN["beds_exact"]["S03:11"]
    # the statement and the bandstate carry the island record
    assert "does p equal np" in FROZEN["beds_exact"]["S02:16"]
    assert "open of record" in FROZEN["beds_exact"]["S02:16"]
    assert "the three barriers of record" in FROZEN["beds_exact"]["S02:16"]
    assert "thirty-two thousand seven hundred sixty-eight" in FROZEN["beds_exact"]["S02:17"]
    assert "the three barriers of record" in FROZEN["beds_exact"]["S02:17"]
    # the composition bed: the census invariant inside the statement,
    # byte-identical at the S3 and S4 state turns (the theorem speaks
    # from the store at both)
    comp = S19_THEOREMS["parity-blowup-filed"]["statement"]
    assert FROZEN["derived_table"]["S03:09"] == comp  # the derive turn's byte
    assert FROZEN["beds_exact"]["S03:16"] == comp
    assert FROZEN["derived_table"]["S04:16"] == comp
    assert "thirty-two thousand seven hundred sixty-eight" in comp
    assert "at the line end eighty-four" in comp
    # the beds carry NO off-line digit strings of record
    import re as _re
    for v in FROZEN["beds_exact"].values():
        assert not _re.search(r"\d{10,}", v)


def test_lesson_phrases_are_house_voiced() -> None:
    """S19 is the island's SUMMIT band: the island statement itself
    enters as DECLARED RECORD in the summit lesson (never as a
    settled theorem). The S19 lessons are house-voiced on the line —
    and the theorem statement carries the census invariant AND the
    line end in number words."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S19_LESSONS.items()}
    # the p class: the bounded-cost settling pattern of the line
    assert "the questions my walk settles" in by_slug["p-class-def"]
    assert "at the line end eighty-four" in by_slug["p-class-def"]
    # the np class: the STORE'S OWN PATTERN (every fact is the
    # certificate of its own derivation path)
    assert "the store itself" in by_slug["np-class-def"]
    assert "at the line end eighty-four" in by_slug["np-class-def"]
    # the summit: the CMI record verbatim, declared open of record
    assert "does p equal np" in by_slug["pnp-def"]
    assert "open of record" in by_slug["pnp-def"]
    assert "the three barriers of record" in by_slug["pnp-def"]
    assert "at the line end eighty-four" in by_slug["pnp-def"]
    # the difficulty shadow: the named missing ingredient
    assert "two to the k-minus-1 terms" in by_slug["parity-shadow-def"]
    assert "the named missing ingredient" in by_slug["parity-shadow-def"]
    assert "at the line end eighty-four" in by_slug["parity-shadow-def"]
    # the file: the census invariant inside the statement
    comp = S19_THEOREMS["parity-blowup-filed"]["statement"]
    assert "thirty-two thousand seven hundred sixty-eight" in comp
    assert "at the line end eighty-four" in comp
    # NO island candidate is settled: the statement lives in the
    # declared-record lesson and the walls only — never as "p equals
    # np is a theorem" or any settled claim in the band material
    for text in list(S19_LESSONS) + [comp]:
        assert "p equals np is a theorem" not in text
        assert "p is not equal to np is a theorem" not in text


def test_offline_values_never_store_answers() -> None:
    """S19 brings NO new off-line value: expect.offline_watch is
    empty, and no off-line digit string floats into an on-line
    answer, a bed, or a wall (the off-line territory is named at its
    record place — the shannon bound sits NAMED AT ITS SCALE inside
    the wall, in number words)."""
    with open("bands/spec-e6.23.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    import re as _re
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"an off-line digit string floated into an on-line answer: {str(v)[:60]!r}"
    for v in list(FROZEN["walls_honest"].values()):
        assert not _re.search(r"\d{10,}", v), "an off-line digit string must not live in an S19 wall"
    # the AC0 wall names shannon in number words, never as a value
    assert "four thousand ninety-six" in Brainstem.W_S19_4
    assert "4096" not in Brainstem.W_S19_4


def test_seam_carry_and_semantic_seam() -> None:
    # the SEVEN carry rows (P6: byte-identical to the seed store):
    # the S18 line-pi rule, the S8 halting wall, the S17 beal
    # statement, the S16 bsd summit, the S17 primitive wall, the S15
    # ramification correction, and the S12 queue
    assert FROZEN["seam_carry_refs"] == ["S04:01", "S04:02", "S04:03", "S04:04", "S04:05", "S04:06", "S04:07"]
    # the carried wall rows stay honest (P3 wall-carried): the S8
    # halting wall (W-S18-1) and the S17 Beal primitive wall (W-S17-1)
    assert FROZEN["derived_table"]["S04:02"].startswith("needs_info: the wall is the halting territory")
    assert FROZEN["derived_table"]["S04:05"].startswith("needs_info: the wall is the primitive territory itself")
    # the off-script standing check: the S18 line-pi reduction rule,
    # byte-identical to the store's own theorem statement
    assert FROZEN["offscript_carry"] == {
        "state the line-pi-reduction rule": S18_THEOREMS["line-pi-reduction"]["statement"]
    }
    # and the in-run S04:01 row says the SAME bytes (the semantic seam
    # is closed both ways)
    assert FROZEN["derived_table"]["S04:01"] == S18_THEOREMS["line-pi-reduction"]["statement"]
    # the statement carries from the S2 session byte-identical
    assert FROZEN["derived_table"]["S04:12"] == FROZEN["beds_exact"]["S02:16"]
    # the seam crosscheck expected value
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"


def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]


def test_probe_grammar_classifies() -> None:
    # the full 51-surface map (det_classify is the referee)
    plain = {
        "S02:01": "s19-p", "S02:04": "s19-p", "S02:05": "s19-p",
        "S02:06": "s19-np", "S02:09": "s19-np", "S02:10": "s19-np", "S02:11": "s19-settle",
        "S02:12": "s19-summit", "S02:15": "s19-summit", "S02:16": "s19-statement", "S02:17": "s19-bandstate",
        "S03:01": "s19-parity", "S03:04": "s19-parity", "S03:05": "s19-parity", "S03:06": "s19-parity",
        "S03:07": "s19-parcnf", "S03:10": "s19-parity", "S03:11": "s19-settle16",
        "S03:12": "s19-rel", "S03:13": "s19-alg", "S03:14": "s19-natp", "S03:15": "s19-ac0",
        "S03:17": "s19-unc",
        "S04:01": "s18-state", "S04:02": "s18-halt", "S04:03": "s17-beal", "S04:04": "s16-bsd",
        "S04:05": "s17-prim", "S04:06": "s15-corr", "S04:07": "s12-queue",
        "S04:08": "s19-p", "S04:09": "s19-p", "S04:10": "s19-np", "S04:11": "s19-np",
        "S04:12": "s19-statement", "S04:13": "s19-summit",
        "S04:14": "s19-parity", "S04:15": "s19-parity",
        "S04:17": "s19-alg",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:02": "p-class-def",
        "S02:07": "np-class-def",
        "S02:13": "pnp-def",
        "S03:02": "parity-shadow-def",
        "S03:16": "parity-blowup-filed",
        "S04:16": "parity-blowup-filed",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", "s19-state", want), ref
    derive_turns = {
        "S03:08": "derive",
        "S03:09": "derive",
    }
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    assertion_turns = ["S02:03", "S02:08", "S02:14", "S03:03"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the summit fact of the island?")[1]["mode"] == "s16-bsd"
    assert det_classify("what is the statement of the beal island of record?")[1]["mode"] == "s17-beal"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("state the line-pi-reduction rule")[1]["mode"] == "s18-state"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: the parity state readouts cite the band's own
    # file; the line-pi carry row cites the S18 theorem; the queue
    # carry row cites the carried queue theorem
    assert FROZEN["theorem_allowed"] == {
        "S03:16": ["parity-blowup-filed"],
        "S04:01": ["line-pi-reduction"],
        "S04:07": ["queue-declared"],
        "S04:16": ["parity-blowup-filed"],
    }
    # the full sanctioned DAG: thirty-eight theorem facts (the S18
    # thirty-seven + parity-blowup-filed)
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 38
    assert "theorem:parity-blowup-filed" in dag
    assert "theorem:line-pi-reduction" in dag  # the S18 soil stays in the DAG
    assert "theorem:beal-line-satisfaction" in dag  # the S17 summit stays in the DAG
    assert "theorem:beal" not in dag, "the bare Beal conj id must NOT exist (the S17 invariant holds)"
    assert "theorem:bsd" not in dag, "the bare BSD conj id stayed gone (the S16 invariant holds)"
    assert "theorem:p-vs-np" not in dag, "the bare island candidate id must NOT exist (the P vs NP question stays open of record)"


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH
    assert SCRIPT_HASH == "96431ed8bedf0121"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:12": ["baker-gill-solovay", "line end 84"],
        "S03:13": ["aaronson-wigderson", "chen-hu-ren", "line end 84"],
        "S03:14": ["razborov-rudich", "line end 84"],
        "S03:15": ["razborov-smolensky", "hastsad", "shannon", "line end 84"],
    }


def test_band_map_frozen_untouched() -> None:
    # the P vs NP island is research-adjacent: the frozen bands-map
    # (S10) stays untouched; e6.23 validates the map as-is against
    # the extended registry.
    from kainos.tutor.bands import BAND_MAP

    domains = {d for b in BAND_MAP for d in b.domains}
    assert "pnp" not in domains, "the band map is frozen at S10 — no new band entries"
    assert len(CONCEPTS_E623) == 116  # the S18 112 + the four difficulty-line concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (D-e6n: the pnp-summit
    # mastery is six, not five — the uncond probe settles on the
    # summit concept too; the S4 letters shift by one against the
    # pre-registration)
    assert FROZEN["domain_sequence"] == {
        2: "UULSSUULSSSUULSSS",
        3: "UULSSSSFTSSHHHHSS",
        4: "SHSSHSSSSSSSSSSSH",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"
