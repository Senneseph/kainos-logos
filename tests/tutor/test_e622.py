from __future__ import annotations

import hashlib
import json

from kainos.tutor.brainstem import (
    CONCEPT_S18,
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
    S18_BEDS,
    S18_LESSONS,
    S18_THEOREMS,
    Brainstem,
    _pnp_py_heaviest,
    _pnp_py_kill_trials,
    _pnp_py_pi_count,
    _pnp_py_pi_list,
    _pnp_py_pigeonhole,
    _pnp_py_scan_cost,
    _pnp_py_spf_cost,
    det_classify,
)
from kainos.tutor.e621 import CONCEPTS_E621
from kainos.tutor.e622 import CONCEPTS_E622, FROZEN, SCRIPT_HASH

S18_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S18_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS)
    + list(S13_LESSONS) + list(S14_LESSONS) + list(S15_LESSONS)
    + list(S16_LESSONS) + list(S17_LESSONS)
)


def test_new_concepts_prereqs_point_down() -> None:
    """S18 adds the four decidable-line concepts; prereqs point DOWN
    (the S11 soil: divides, scan-ledger; the band's own edges: the
    tamable machine over the decision question, the reduction over
    the decision question + the scan-ledger, the cost counter over
    the reduction + the scan-ledger)."""
    carried = tuple(c.id for c in CONCEPTS_E621)
    assert tuple(c.id for c in CONCEPTS_E622) == carried + (
        CONCEPT_S18[0].id, CONCEPT_S18[1].id, CONCEPT_S18[2].id, CONCEPT_S18[3].id,
    )
    existing = set(carried)
    for c in CONCEPT_S18:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S18}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id: c for c in CONCEPT_S18}
    assert by_id["decision-question"].prereqs == ("divides",)
    assert by_id["tamable-machine"].prereqs == ("decision-question",)
    assert by_id["reduction"].prereqs == ("decision-question", "scan-ledger")
    assert by_id["cost-counter"].prereqs == ("reduction", "scan-ledger")
    for c in CONCEPT_S18:
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
    for slug in S18_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S18_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for mod in (
        S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS, S10_THEOREMS,
        S11_THEOREMS, S12_THEOREMS, S13_THEOREMS, S14_THEOREMS, S15_THEOREMS,
        S16_THEOREMS, S17_THEOREMS,
    ):
        for m in mod.values():
            assert m["statement"] not in script_lines
    # the pre-lesson gaps run BEFORE the first teach (S2:01-02, then
    # the teach at S2:03 — two gaps, the S18 shape)
    assert FROZEN["script"][2][0] == "does the seven divide the eighty-four of record?"
    assert FROZEN["script"][2][1] == "state the question-def rule"
    assert (
        FROZEN["script"][2][2]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S18_LESSONS.items() if s == "question-def")
    )
    assert FROZEN["script"][3][0] == "how many primes lie at or below my line end of record?"
    # the one sanctioned composition, derived in-band on the strict
    # part set (the scaffold first names the short part)
    assert "derive line-pi-reduction from question-def and reduction-def" in script_lines
    assert "derive line-pi-reduction from question-def" in script_lines
    # the S17 soil carries (the island connects through the soil)
    assert "what is the statement of the beal island of record?" in script_lines


def test_frozen_shape() -> None:
    """The control #1 census (D-e6m: the mechanism spoke, never the
    hand)."""
    assert FROZEN["seed_total"] == 1641
    assert FROZEN["seed_identity"] == "e092ef1261ef7210"
    assert FROZEN["line_end_final"] == 84  # S18 writes NO successor facts
    assert FROZEN["new_facts"] == 5
    assert FROZEN["new_fact_ids"] == [
        "lemma:question-def",
        "lemma:tamable-def",
        "lemma:reduction-def",
        "lemma:cost-def",
        "theorem:line-pi-reduction",
    ]
    assert FROZEN["total_seam_facts"] == 133  # 117 lemma + 16 theorem (S17 128 + the FIVE)
    assert len(FROZEN["theorem_dag"]) == 37  # S6..S18
    assert len(FROZEN["walls_honest"]) == 2
    assert len(FROZEN["beds_exact"]) == 18
    assert len(FROZEN["derived_table"]) == 18  # the derive + the seventeen S4 rows (beds are beds_exact)
    assert len(FROZEN["pre_teach_gaps"]) == 8  # the eight pre-lesson gaps
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 1
    assert len(FROZEN["missing_parts_failure"]) == 0
    assert FROZEN["rederive"] is None
    assert len(FROZEN["seam_carry_refs"]) == 5
    assert FROZEN["final_total"] == 1698  # 1641 + 5 facts + 52 events (D-e6m(b))
    assert FROZEN["new_events"] == 52
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "UULSSSUULHHSUULSS"
    assert FROZEN["domain_sequence"][3] == "UULSSSFTSSSSSSSSS"
    assert FROZEN["domain_sequence"][4] == "SSHSSSSSSSSSSHSSS"


def test_pre_s18_states_carry_e621_final() -> None:
    """The 108 carried concepts at their S17-final values (the live
    control census, excluding the four new concepts — the e621
    convention, carried)."""
    pre = FROZEN["pre_s18_states"]
    assert len(pre) == 108
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S18}, "a NEW concept leaked into the pre-states"
    # the Beal soil as the S17 store held it
    assert pre["beal-summit"] == {"state": "stable", "correct": 4}
    assert pre["beal-census"] == {"state": "stable", "correct": 10}
    assert pre["l-correction"] == {"state": "stable", "correct": 9}
    assert pre["rh-relevance"]["state"] == "practicing"  # the store held it practicing (17 correct)
    # the S11 soil the decidable line stands on
    assert pre["first-divisor"] == {"state": "stable", "correct": 36}
    assert pre["divides"] == {"state": "stable", "correct": 5}
    assert pre["scan-ledger"] == {"state": "stable", "correct": 12}
    # the S17 valuation soil the Beal island closed on
    assert pre["valuation"] == {"state": "stable", "correct": 6}
    assert pre["lte-form"] == {"state": "stable", "correct": 7}
    # the S18 soil drill at the NEW coordinates (control #1: the S4
    # carries S04:01-02 + the S15 correction carry S04:04)
    assert FROZEN["pre_s18_drilled"] == {
        "beal-census": 1,
        "beal-summit": 1,
        "l-correction": 1,
    }
    # the four NEW concepts at their frozen band-end values (all
    # stable: the four-correct-derivation rule held for each)
    assert FROZEN["mastery_expected"] == {
        "decision-question": {"correct": 7, "prereq_gaps": [], "state": "stable"},
        "tamable-machine": {"correct": 4, "prereq_gaps": [], "state": "stable"},
        "reduction": {"correct": 9, "prereq_gaps": [], "state": "stable"},
        "cost-counter": {"correct": 10, "prereq_gaps": [], "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "decision-question": [],
        "tamable-machine": [],
        "reduction": [],
        "cost-counter": [],
    }


def test_denylist_is_the_s9_44() -> None:
    # S18 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44


def test_unconditional_marker_absent() -> None:
    """The S18 facts are the unconditional decidable band: none
    carries the RH marker; the uncond probe says so of record on the
    line."""
    marker = "under the condition of the Riemann hypothesis"
    for th in S18_THEOREMS.values():
        assert marker not in th["statement"]
    for phrase in S18_LESSONS:
        assert marker not in phrase
    # the seed is the official S17 store (e6.21 run 1)
    assert FROZEN["seed"].startswith("results/phase-6/e6.21-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S18_THEOREMS) == {"line-pi-reduction"}
    assert S18_THEOREMS["line-pi-reduction"]["parts"] == ("question-def", "reduction-def")
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:08": ["line-pi-reduction", ["question-def", "reduction-def"]],
    }
    # the honest-turn bytes: the scaffold names the single short part
    # (the named-set short the required-set before the rule can be
    # put together); the S18 band has no missing-parts probe
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the reduction-def" in FROZEN["scaffold_failures"]["S03:07"]


def test_walls_bytes() -> None:
    # the two walls are the Brainstem class attributes, byte-frozen:
    # S02:10 W-S18-1 (the halting problem), S02:11 W-S18-2 (the
    # machine universe)
    wall_attrs = {
        "S02:10": Brainstem.W_S18_1,
        "S02:11": Brainstem.W_S18_2,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the no-new-decimals rule: the off-line territory is named at its
    # record place, never as a value of the line
    import re as _re
    for _wall in list(FROZEN["walls_honest"].values()) + [Brainstem.W_S18_1, Brainstem.W_S18_2]:
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry an off-line digit string"
    assert "turing" in Brainstem.W_S18_1
    assert "infinite tape" in Brainstem.W_S18_2
    # no honest-zero bytes (the S18 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The 18 on-line beds re-derive against the mechanism's own
    references (never hand-written values)."""
    # the PI CENSUS: twenty-three primes, the first-divisor list
    assert _pnp_py_pi_count(84) == 23
    assert _pnp_py_pi_list(84) == S18_BEDS["primes"]
    assert len(S18_BEDS["primes"]) == 23
    assert S18_BEDS["pi"] == 23
    # the DECISION table: the seven divides, the thirteen does not,
    # the two and three divide, the seventeen does not
    assert S18_BEDS["decision"] == {
        "seven": True, "thirteen": False, "two": True, "three": True, "seventeen": False,
    }
    # the COST CENSUS: the whole-line scan, the heaviest query, the
    # spot rows, the kill-trials
    assert _pnp_py_scan_cost(84) == 192 == S18_BEDS["scan_cost"]
    assert _pnp_py_heaviest(84) == (83, 8) == tuple(S18_BEDS["heaviest"])
    for n, c in S18_BEDS["cost_spot"].items():
        assert _pnp_py_spf_cost(n) == c, n
    assert tuple(S18_BEDS["kill_trials"]) == (
        _pnp_py_kill_trials(84, False), _pnp_py_kill_trials(84, True),
    ) == (95, 87)
    # the PIGEONHOLE: n = 1..10 rows, zero violations each
    for n in range(1, 11):
        total, violations = _pnp_py_pigeonhole(n)
        assert S18_BEDS["pigeonhole"][n] == (total, 0) == S18_BEDS["pigeonhole"][n]
        assert violations == 0
    # the bed bytes name the records (the house wording)
    assert "one hundred ninety-two candidate steps of record" in FROZEN["beds_exact"]["S02:16"]
    assert "eighty-three" in FROZEN["beds_exact"]["S02:17"]
    assert "eight candidate steps of record" in FROZEN["beds_exact"]["S02:17"]
    assert "twenty-three of record" in FROZEN["beds_exact"]["S03:04"]
    assert "ninety-five candidate steps over the composites" in FROZEN["beds_exact"]["S03:05"]
    assert "eighty-seven with the prime candidates alone" in FROZEN["beds_exact"]["S03:05"]
    assert "zero — the walk's loop never runs over the two" in FROZEN["beds_exact"]["S03:10"]
    assert "zero violations of record" in FROZEN["beds_exact"]["S03:17"]
    # the composition bed: the census invariant inside the statement
    assert "twenty-three of them" in FROZEN["beds_exact"]["S03:13"]
    assert "one hundred ninety-two candidate steps" in FROZEN["beds_exact"]["S03:13"]
    assert "at the line end eighty-four" in FROZEN["beds_exact"]["S03:13"]


def test_lesson_phrases_are_house_voiced() -> None:
    """S18 is the island's FOUNDATION band: the island statement
    itself enters only at the S19 summit (declared record). The S18
    lessons are house-voiced on the line — and the theorem statement
    carries the census invariant AND the line end in number words."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S18_LESSONS.items()}
    # the decision question (the line's yes/no pattern)
    assert "a yes/no question about objects on my line" in by_slug["question-def"]
    assert "at the line end eighty-four" in by_slug["question-def"]
    # the tamable machine: the DESIGN FACT, walled inside the lesson
    assert "design fact" in by_slug["tamable-def"]
    assert "infinite tape" in by_slug["tamable-def"]
    assert "at the line end eighty-four" in by_slug["tamable-def"]
    # the reduction: the prime-count question re-expressed
    assert "a mapping of question a to question b" in by_slug["reduction-def"]
    assert "at the line end eighty-four" in by_slug["reduction-def"]
    # the cost counter: the ledger of the decision walks
    assert "one hundred ninety-two candidate steps" in by_slug["cost-def"]
    assert "at the line end eighty-four" in by_slug["cost-def"]
    # the composition: the census invariant inside the statement
    comp = S18_THEOREMS["line-pi-reduction"]["statement"]
    assert "twenty-three" in comp
    assert "one hundred ninety-two" in comp
    assert "at the line end eighty-four" in comp
    # NO island candidate language is settled: no "p equals np"
    # anywhere in the S18 band material
    for text in list(S18_LESSONS) + [comp]:
        assert "p equals np" not in text
        assert "p is not equal to np" not in text


def test_offline_values_never_store_answers() -> None:
    """S18 brings NO new off-line value: expect.offline_watch is
    empty, and no off-line digit string floats into an on-line
    answer, a bed, or a wall (the off-line territory is named at its
    record place)."""
    with open("bands/spec-e6.22.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    import re as _re
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"an off-line digit string floated into an on-line answer: {str(v)[:60]!r}"
    for v in list(FROZEN["walls_honest"].values()):
        assert not _re.search(r"\d{10,}", v), "an off-line digit string must not live in an S18 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the FIVE carry rows (P6: byte-identical to the seed store):
    # the Beal statement carry, the Beal census carry, the S17
    # primitive-wall carry, the S15 ramification correction, and the
    # queue
    assert FROZEN["seam_carry_refs"] == ["S04:01", "S04:02", "S04:03", "S04:04", "S04:05"]
    # the carried wall row stays honest (P3 wall-carried): the S17
    # Beal primitive wall (W-S17-1)
    assert FROZEN["derived_table"]["S04:03"].startswith("needs_info: the wall is the primitive territory itself")
    # the off-script standing check: the S17 summit rule, byte-
    # identical to the store's own theorem statement
    assert FROZEN["offscript_carry"] == {
        "state the beal-line-satisfaction rule": S17_THEOREMS["beal-line-satisfaction"]["statement"]
    }
    # the seam crosscheck expected value
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"


def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]


def test_probe_grammar_classifies() -> None:
    # the full 51-surface map (det_classify is the referee)
    plain = {
        "S02:01": "s18-dec", "S02:04": "s18-dec", "S02:05": "s18-dec",
        "S02:06": "s18-ph", "S02:07": "s18-halt",
        "S02:10": "s18-halt", "S02:11": "s18-machine",
        "S02:12": "s18-tam",
        "S02:16": "s18-scan", "S02:17": "s18-heavy",
        "S03:01": "s18-pi", "S03:04": "s18-pi",
        "S03:05": "s18-kill",
        "S03:06": "s18-costspot", "S03:09": "s18-costspot", "S03:10": "s18-costspot", "S03:11": "s18-costspot",
        "S03:12": "s18-bandstate", "S03:14": "s18-uncond",
        "S03:15": "s18-dec", "S03:16": "s18-dec", "S03:17": "s18-ph",
        "S04:01": "s17-beal", "S04:02": "s17-census", "S04:03": "s17-prim",
        "S04:04": "s15-corr", "S04:05": "s12-queue",
        "S04:06": "s18-tam", "S04:07": "s18-tam", "S04:08": "s18-tam",
        "S04:09": "s18-pi", "S04:10": "s18-scan", "S04:11": "s18-heavy",
        "S04:12": "s18-kill", "S04:13": "s18-ph", "S04:14": "s18-halt",
        "S04:16": "s18-bandstate", "S04:17": "s18-uncond",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:02": "question-def",
        "S02:08": "tamable-def",
        "S02:14": "cost-def",
        "S03:02": "reduction-def",
        "S03:13": "line-pi-reduction",
        "S04:15": "line-pi-reduction",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", "s18-state", want), ref
    derive_turns = {
        "S03:07": "derive",
        "S03:08": "derive",
    }
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    assertion_turns = ["S02:03", "S02:09", "S02:15", "S03:03"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the summit fact of the island?")[1]["mode"] == "s16-bsd"
    assert det_classify("what is the statement of the beal island of record?")[1]["mode"] == "s17-beal"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("state the beal-line-satisfaction rule")[1]["mode"] == "s17-state"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: the line-pi-reduction state readouts cite the
    # band's own composition; the queue carry row cites the carried
    # queue theorem
    assert FROZEN["theorem_allowed"] == {
        "S03:13": ["line-pi-reduction"],
        "S04:05": ["queue-declared"],
        "S04:15": ["line-pi-reduction"],
    }
    # the full sanctioned DAG: thirty-seven theorem facts (the S17
    # thirty-six + line-pi-reduction)
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 37
    assert "theorem:line-pi-reduction" in dag
    assert "theorem:beal-line-satisfaction" in dag  # the S17 summit stays in the DAG
    assert "theorem:beal" not in dag, "the bare Beal conj id must NOT exist (the S17 invariant holds)"
    assert "theorem:bsd" not in dag, "the bare BSD conj id stayed gone (the S16 invariant holds)"
    assert "theorem:p-vs-np" not in dag, "the bare island candidate id must NOT exist (the P vs NP question stays open of record)"


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH
    assert SCRIPT_HASH == "823c2b05dcd3f0e3"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S02:10": ["turing", "line end 84"],
        "S02:11": ["machine universe", "line end 84"],
    }


def test_band_map_frozen_untouched() -> None:
    # the P vs NP island is research-adjacent: the frozen bands-map
    # (S10) stays untouched; e6.22 validates the map as-is against
    # the extended registry.
    from kainos.tutor.bands import BAND_MAP

    domains = {d for b in BAND_MAP for d in b.domains}
    assert "pnp" not in domains, "the band map is frozen at S10 — no new band entries"
    assert len(CONCEPTS_E622) == 112  # the S17 108 + the four decidable-line concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (the D-e6m family: the
    # scaffold byte names the single short part — it shows through as
    # an F turn; no ambiguous letters)
    assert FROZEN["domain_sequence"] == {
        2: "UULSSSUULHHSUULSS",
        3: "UULSSSFTSSSSSSSSS",
        4: "SSHSSSSSSSSSSHSSS",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"
