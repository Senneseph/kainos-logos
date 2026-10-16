from __future__ import annotations

import hashlib
import json
import re as _re
from pathlib import Path

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S21,
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
    S19_LESSONS,
    S19_THEOREMS,
    S20_LESSONS,
    S20_THEOREMS,
    S21_LESSONS,
    S21_THEOREMS,
    Brainstem,
    det_classify,
)
from kainos.tutor.e624 import CONCEPTS_E624
from kainos.tutor.e625 import CONCEPTS_E625, FROZEN, SCRIPT_HASH
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime, load_store

MARKER = "under the condition of the Riemann hypothesis"
MARKER_VARIANT = "under the condition that"

S21_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S21_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS)
    + list(S13_LESSONS) + list(S14_LESSONS) + list(S15_LESSONS)
    + list(S16_LESSONS) + list(S17_LESSONS) + list(S18_LESSONS)
    + list(S19_LESSONS) + list(S20_LESSONS)
)


def test_new_concepts_prereqs_point_down() -> None:
    """S21 adds the two condition concepts; their prereqs point DOWN
    into the carried line (the conditional lot; the rh-scale and the
    factor-route of the S12 fundamentals)."""
    carried = tuple(c.id for c in CONCEPTS_E624)
    assert tuple(c.id for c in CONCEPTS_E625) == carried + tuple(c.id for c in CONCEPT_S21)
    existing = set(carried)
    for c in CONCEPT_S21:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S21}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id for c in CONCEPT_S21}
    assert by_id == {"hypothesis", "condition-line"}
    for c in CONCEPT_S21:
        assert c.band == "college-1"
        assert c.domain == "rh"
    by_id_map = {c.id: c for c in CONCEPT_S21}
    assert by_id_map["hypothesis"].prereqs == ("conditional",)
    assert by_id_map["condition-line"].prereqs == ("rh-scale", "factor-route")


def test_script_shape_and_teaching() -> None:
    """51 turns; the two teaches are the lesson phrases verbatim; no
    carried S4–S20 seam statement appears in the script (Stage-A)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S21_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S21_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for mod in (
        S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS, S10_THEOREMS,
        S11_THEOREMS, S12_THEOREMS, S13_THEOREMS, S14_THEOREMS, S15_THEOREMS,
        S16_THEOREMS, S17_THEOREMS, S18_THEOREMS, S19_THEOREMS, S20_THEOREMS,
    ):
        for m in mod.values():
            assert m["statement"] not in script_lines
    # the S02 rhythm: the queue carried first, then a concept's two
    # gaps run immediately before its teach, for both concepts
    assert FROZEN["script"][2][0] == "what is the queue above my line?"
    assert FROZEN["script"][2][5] == "can my line reason under the condition?"
    assert FROZEN["script"][2][6] == "state the hypothesis-def rule"
    assert (
        FROZEN["script"][2][7]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S21_LESSONS.items() if s == "hypothesis-def")
    )
    assert FROZEN["script"][2][10] == "what is my condition line, end to end, as my store holds it?"
    assert FROZEN["script"][2][11] == "state the condition-line-def rule"
    assert (
        FROZEN["script"][2][12]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S21_LESSONS.items() if s == "condition-line-def")
    )
    # the one sanctioned composition, derived in-band on the strict
    # part set (the scaffold names only the hypothesis part first)
    assert "derive condition-line-filed from hypothesis-def" in script_lines
    assert "derive condition-line-filed from hypothesis-def and condition-line-def" in script_lines
    # the carried condition surfaces stand in the script
    assert "what does the condition give for the error of the prime count?" in script_lines
    assert "does my line agree with the conditional root scale?" in script_lines
    assert "what is the statement of the riemann island of record?" in script_lines


def test_frozen_shape() -> None:
    """The control #1 census (the mechanism spoke, never the hand):
    1823 + 3 new facts + 45 new events = 1871; the S21 band writes
    NO successor facts (the line end stays 84)."""
    assert FROZEN["seed_total"] == 1823
    assert FROZEN["seed_identity"] == "e84381407e1dba64"
    assert FROZEN["line_end_final"] == 84  # S21 writes NO successor facts
    assert FROZEN["new_facts"] == 3
    assert FROZEN["new_fact_ids"] == [
        "lemma:hypothesis-def",
        "lemma:condition-line-def",
        "theorem:condition-line-filed",
    ]
    assert FROZEN["total_seam_facts"] == 146  # 106 lemma + 40 theorem (S20 143 + the THREE)
    assert len(FROZEN["theorem_dag"]) == 40  # S6..S21
    assert len(FROZEN["walls_honest"]) == 4  # each declared territory probed once
    assert len(FROZEN["beds_exact"]) == 16
    assert len(FROZEN["derived_table"]) == 17  # the 16 beds + the sanctioned derive
    assert len(FROZEN["pre_teach_gaps"]) == 4  # two pre-lesson gaps per concept
    assert len(FROZEN["teach_turns"]) == 2
    assert len(FROZEN["scaffold_failures"]) == 1
    assert len(FROZEN["missing_parts_failure"]) == 0
    assert FROZEN["rederive"] is None
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S02:03", "S02:04", "S02:05",
        "S03:01", "S03:02", "S03:03", "S03:04", "S03:05", "S03:06",
        "S03:07", "S03:08", "S03:09", "S03:10", "S03:11",
        "S04:01", "S04:02", "S04:05", "S04:06", "S04:07", "S04:08", "S04:16",
    ]
    assert FROZEN["final_total"] == 1871  # 1823 + 3 facts + 45 events
    assert FROZEN["new_events"] == 45
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "SSSSSUULSSUULSSSS"
    assert FROZEN["domain_sequence"][3] == "SSSSSSSSSSSFTSSHH"
    assert FROZEN["domain_sequence"][4] == "SSSSSSSSSSSSSHHSS"
    # the off-script standing check: the first lot of the queue
    assert list(FROZEN["offscript_carry"]) == ["the queue above my line, first lot, which?"]


def test_pre_s21_states_carry_e624_final() -> None:
    """The 120 carried concepts at their S20-final values (the live
    control census, excluding the two new concepts)."""
    pre = FROZEN["pre_s21_states"]
    assert len(pre) == 120
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S21}, "a NEW concept leaked into the pre-states"
    # the S20 soil the condition line stands on (the S20-final values)
    assert pre["weave"] == {"state": "stable", "correct": 8}
    assert pre["summit-shape"] == {"state": "practicing", "correct": 8}
    assert pre["shadow-form"] == {"state": "stable", "correct": 6}
    assert pre["boundary-form"] == {"state": "stable", "correct": 5}
    # the RH soil the condition line walks
    assert pre["riemann"] == {"state": "practicing", "correct": 14}
    assert pre["rh-scale"]["state"] == "practicing"
    assert pre["rh-relevance"]["state"] == "practicing"
    assert pre["factor-route"]["state"] == "practicing"
    assert pre["conditional"] == {"state": "practicing", "correct": 1}
    # the island summits the condition names
    assert pre["beal-summit"] == {"state": "stable", "correct": 7}
    assert pre["bsd-summit"] == {"state": "stable", "correct": 13}
    assert pre["pnp-summit"] == {"state": "stable", "correct": 7}
    assert pre["class-p"] == {"state": "stable", "correct": 4}
    assert pre["class-np"] == {"state": "stable", "correct": 5}
    # the S21 drill at the carried coordinates (control #1)
    assert FROZEN["pre_s21_drilled"] == {
        "conditional": 1,
        "factor-route": 7,
        "psi-eq": 1,
        "rh-relevance": 3,
        "rh-scale": 1,
        "riemann": 3,
        "shadow-form": 3,
    }
    # the two NEW concepts at their frozen band-end values: both
    # practicing, with their prereq gaps named in the mechanism's
    # order (NOT the Concept tuple order)
    assert FROZEN["mastery_expected"] == {
        "condition-line": {"correct": 9, "state": "practicing"},
        "hypothesis": {"correct": 5, "state": "practicing"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "condition-line": ["factor-route", "rh-scale"],
        "hypothesis": ["conditional"],
    }


def test_denylist_is_the_s9_44() -> None:
    # S21 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44


def test_conditional_marker_present() -> None:
    """The S21 facts are the CONDITIONAL band: every one of the three
    new facts carries the exact condition marker (the D-e6o(b) mirror
    inverts the S20 posture — S20's facts were marker-free, these
    must carry the marker); the census conserves: seed 3 exact + 1
    variant, final 6 exact + 1 variant (the variant is the
    conditional-def's own 'under the condition that' form,
    byte-identical across the band)."""
    hy, hyd = None, None
    for phrase, meta in S21_LESSONS.items():
        if meta[1] == "hypothesis-def":
            hy = phrase
        if meta[1] == "condition-line-def":
            hyd = phrase
    assert hy is not None and MARKER in hy
    assert hyd is not None and MARKER in hyd
    filed = S21_THEOREMS["condition-line-filed"]["statement"]
    assert MARKER in filed
    # the census on the seed and the final store (the store speaks)
    seed = load_store(Path(FROZEN["seed"]))
    seed_exact = [
        a.id for a in seed.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str) and MARKER in a.object
    ]
    assert seed_exact == ["lemma:rh-bound-scale", "lemma:rh-upf", "theorem:two-routes-one-guarantee"]
    seed_variant = [
        a.id for a in seed.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str)
        and MARKER not in a.object and MARKER_VARIANT in a.object
    ]
    assert seed_variant == ["lemma:conditional-def"]
    # and the seed facts are byte-identical in the FROZEN-derived band-end view
    fin = load_store(Path(FROZEN["seed"].replace("e6.24-run1", "e6.25-run1")))
    fin_exact = [
        a.id for a in fin.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str) and MARKER in a.object
    ]
    assert sorted(fin_exact) == sorted(seed_exact + FROZEN["new_fact_ids"])
    fin_variant = [
        a.id for a in fin.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str)
        and MARKER not in a.object and MARKER_VARIANT in a.object
    ]
    assert fin_variant == ["lemma:conditional-def"]
    assert fin.get("lemma:conditional-def").object == seed.get("lemma:conditional-def").object
    assert FROZEN["seed"].startswith("results/phase-6/e6.24-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S21_THEOREMS) == {"condition-line-filed"}
    assert S21_THEOREMS["condition-line-filed"]["parts"] == (
        "hypothesis-def",
        "condition-line-def",
    )
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:13": [
            "condition-line-filed",
            [
                "lemma:hypothesis-def",
                "lemma:condition-line-def",
            ],
        ],
    }
    # the honest-turn bytes: the scaffold names only the hypothesis
    # part (short the condition-line-def), before the sanctioned
    # derive puts the rule together on the exact set
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the condition-line-def before i can put it together" in FROZEN["scaffold_failures"]["S03:12"]


def test_walls_bytes() -> None:
    # the four declared territories, each probed once: S03:16
    # W-S21-1 (the condition itself), S03:17 W-S21-2 (the dropped
    # marker), S04:14 W-S21-4 (the declared queue), S04:15 W-S21-1
    # re-probed after the queue check
    wall_attrs = {
        "S03:16": Brainstem.W_S21_1,
        "S03:17": Brainstem.W_S21_2,
        "S04:14": Brainstem.W_S21_4,
        "S04:15": Brainstem.W_S21_1,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the no-new-decimals rule: the condition line names only values
    # the line's record already holds — no off-line digit string anywhere
    for _wall in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry an off-line digit string"
    assert "fills the line, not the condition" in Brainstem.W_S21_1
    assert "a conditional statement stripped of its marker is off the line" in Brainstem.W_S21_2
    assert "no new value past my line end enters the floor" in Brainstem.W_S21_3
    assert "no lot added" in Brainstem.W_S21_4
    # W-S21-3 (the register) is the declared fourth territory: it
    # stands on the Brainstem even though the band probes the other
    # three territories' neighbours in the script
    assert "the twenty gaps covered of the twenty-two" in Brainstem.W_S21_3
    # no honest-zero bytes (the S21 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The on-line bed rows re-derive from the STORE'S OWN WALKS
    (re-walked here independently of the brainstem's — the
    store-speaks rule)."""
    store = load_store(Path(FROZEN["seed"]))
    # (a) the marker census on the SEED's theorem facts: 13 line end
    # / 2 spot / 24 universal of 39 — the S02:16 bed stands on this
    e_n = s_n = n_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        assert isinstance(a.object, str)
        if "line end" in a.object:
            e_n += 1
        elif "at s = 2" in a.object:
            s_n += 1
        else:
            n_n += 1
    assert (e_n, s_n, n_n) == (13, 2, 24)
    assert "thirteen of my thirty-nine theorem facts close their scope at the line end" in FROZEN["beds_exact"]["S02:16"]
    assert "two close on the line's spot marker" in FROZEN["beds_exact"]["S02:16"]
    assert "twenty-four carry the universal form with no line end marker" in FROZEN["beds_exact"]["S02:16"]
    # (b) the census re-walked AFTER the band's own filing: 40
    # theorem facts, fourteen closing at the line end (the new filing
    # is the fourteenth line-end marker)
    assert "fourteen of my forty theorem facts close their scope at the line end" in FROZEN["beds_exact"]["S03:15"]
    assert "fourteen of my forty theorem facts close their scope at the line end" in FROZEN["beds_exact"]["S04:03"]
    assert "a form of the line is not a census of its end" in FROZEN["beds_exact"]["S03:15"]
    # (c) the STATE beds: the new facts' state readouts are the
    # lesson phrases and the filing statement VERBATIM (the
    # house-voice rule), re-anchored here against the brainstem
    # constants, not against FROZEN
    hy = next(p for p, m in S21_LESSONS.items() if m[1] == "hypothesis-def")
    line = next(p for p, m in S21_LESSONS.items() if m[1] == "condition-line-def")
    filed = S21_THEOREMS["condition-line-filed"]["statement"]
    assert FROZEN["beds_exact"]["S02:09"] == hy
    assert FROZEN["beds_exact"]["S04:09"] == hy
    assert FROZEN["beds_exact"]["S02:14"] == line
    assert FROZEN["beds_exact"]["S04:10"] == line
    assert FROZEN["beds_exact"]["S04:11"] == filed
    # (d) the USAGE beds (the hypothesis in action): a grounded yes
    # that carries the marker and closes at the numbered line end
    for ref in ("S02:10", "S02:17", "S04:12"):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("yes — to reason under the condition")
        assert MARKER in v
        assert v.endswith("at the line end 84")
        assert "assumed in the lot, never proved by it" in v
    # (e) the LINE beds (the condition line end to end): one line
    # from the assumption, each consequence keeping its marker
    for ref in ("S02:15", "S04:13"):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("one line from the assumption")
        assert MARKER in v
        assert v.endswith("at the line end 84")
        assert "each consequence keeping its marker" in v
    # (f) the FILING beds: the filing files the line, not the
    # condition — the condition stays open of record
    for ref in ("S03:14", "S04:04", "S04:17"):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("the line, not the condition")
        assert "assumed, never proved, believed, not known" in v
        assert v.endswith("at the line end 84")
    # the beds carry NO off-line digit strings of record
    for v in FROZEN["beds_exact"].values():
        assert not _re.search(r"\d{10,}", v)


def test_lesson_phrases_are_house_voiced() -> None:
    """S21 is the condition line: the assumption enters as a status
    surface (believed, not known) and the marker travels in every
    consequence. The S21 lessons are house-voiced on the line — and
    the theorem statement carries the marker AND the line end."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S21_LESSONS.items()}
    # the hypothesis: the condition as a usable assumption
    assert MARKER in by_slug["hypothesis-def"]
    assert "assumed in the lot, never proved by it" in by_slug["hypothesis-def"]
    assert "a conditional lot read without its condition is a misread this store punishes" in by_slug["hypothesis-def"]
    assert "at the line end eighty-four" in by_slug["hypothesis-def"]
    # the condition line: one line from the assumption
    assert MARKER in by_slug["condition-line-def"]
    assert "each consequence keeping its marker" in by_slug["condition-line-def"]
    assert "at the line end eighty-four" in by_slug["condition-line-def"]
    # the file: the marker AND the line end in number words
    comp = S21_THEOREMS["condition-line-filed"]["statement"]
    assert MARKER in comp
    assert "the marker travels in every consequence" in comp
    assert "assumed, never proved, at the line end eighty-four" in comp
    # NO island candidate is settled: the statements stay open of
    # record in the band material — never a settled claim
    for text in list(S21_LESSONS) + [comp]:
        assert "p equals np is a theorem" not in text
        assert "the riemann hypothesis is true" not in text
        assert "beal's conjecture is true" not in text
        assert "the condition is proved" not in text


def test_offline_values_never_store_answers() -> None:
    """S21 brings NO new off-line value: expect.offline_watch is
    empty, and no off-line digit string floats into an on-line
    answer, a bed, or a wall (the condition line names only values
    the line's record already holds)."""
    with open("bands/spec-e6.25.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"an off-line digit string floated into an on-line answer: {str(v)[:60]!r}"
    for v in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", v), "an off-line digit string must not live in an S21 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the 23 carry rows (P6: byte-identical to the seed store):
    # the queue and its first lot, the four condition givings, the
    # agreement and the two roads, the scale/ledger/mroot/selved/
    # reachscale reads, the two state readouts, and the riemann
    # summit carried twice
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S02:03", "S02:04", "S02:05",
        "S03:01", "S03:02", "S03:03", "S03:04", "S03:05", "S03:06",
        "S03:07", "S03:08", "S03:09", "S03:10", "S03:11",
        "S04:01", "S04:02", "S04:05", "S04:06", "S04:07", "S04:08", "S04:16",
    ]
    # the off-script standing check: the first lot of the queue,
    # byte-identical to the store's own declared record (the
    # condition line is the first of the four declared lots — the
    # band adds no lot, it fills lot one)
    store = load_store(Path(FROZEN["seed"]))
    queue_fact = store.get("theorem:queue-declared")
    queue_byte = queue_fact.object if isinstance(queue_fact.object, str) else str(queue_fact.object)
    assert "the condition line" in queue_byte
    first_lot = FROZEN["offscript_carry"]["the queue above my line, first lot, which?"]
    assert first_lot.startswith("the condition line — the condition-closers made teachable")
    assert first_lot.endswith("with the conditional consequences as drills")
    # the riemann summit carry byte: re-derived here on a single
    # boot over the SEED store (no band turn may drift it) — the
    # statement verbatim + the open status
    import tempfile

    reset_concepts()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "codeX-S01.json").write_bytes(Path(FROZEN["seed"]).read_bytes())
        rt = InfantRuntime(root, concepts=CONCEPTS_E625)
        rt.boot(2)
        res = rt.turn("what is the statement of the riemann island of record?")
    conj = store.get("conjecture:riemann")
    want = (
        f"the statement of the riemann island, as my store holds it: {conj.object} — "
        f"declared of record, open of record: believed, not known, at the line end 84"
    )
    assert res.response_ir.get("answer") == want
    # the seam crosscheck expected value
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"


def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]


def test_probe_grammar_classifies() -> None:
    # the full 51-surface map (det_classify is the referee)
    plain = {
        "S02:01": "s12-queue",
        "S02:02": "s12-queue-lot",
        "S02:03": "s12-condgive",
        "S02:04": "s12-condgive",
        "S02:05": "s20-rhsummit",
        "S02:10": "s21-hypo",
        "S02:15": "s21-line",
        "S02:16": "s20-marker",
        "S02:17": "s21-hypo",
        "S03:01": "s12-condgive",
        "S03:02": "s12-condgive",
        "S03:03": "s12-agree",
        "S03:04": "s12-uncond",
        "S03:05": "s12-roads-how",
        "S03:06": "s12-roads-cond",
        "S03:07": "s12-scalecount",
        "S03:08": "s12-mlab",
        "S03:09": "s12-mroot",
        "S03:10": "s12-selved",
        "S03:11": "s12-reachscale",
        "S03:14": "s21-filing",
        "S03:15": "s20-marker",
        "S03:16": "s21-w1",
        "S03:17": "s21-w2",
        "S04:01": "s12-queue",
        "S04:02": "s12-queue-lot",
        "S04:03": "s20-marker",
        "S04:04": "s21-filing",
        "S04:05": "s12-state",
        "S04:06": "s12-state",
        "S04:07": "s9-state",
        "S04:08": "s9-state",
        "S04:12": "s21-hypo",
        "S04:13": "s21-line",
        "S04:14": "s21-w4",
        "S04:15": "s21-w1",
        "S04:16": "s20-rhsummit",
        "S04:17": "s21-filing",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:06": "s21-hypo",
        "S02:07": "s21-state",
        "S02:09": "s21-state",
        "S02:11": "s21-line",
        "S02:12": "s21-state",
        "S02:14": "s21-state",
        "S04:09": "s21-state",
        "S04:10": "s21-state",
        "S04:11": "s21-state",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    state_slugs = {
        "S02:07": "hypothesis-def",
        "S02:09": "hypothesis-def",
        "S02:12": "condition-line-def",
        "S02:14": "condition-line-def",
        "S04:09": "hypothesis-def",
        "S04:10": "condition-line-def",
        "S04:11": "condition-line-filed",
    }
    for ref, slug in state_slugs.items():
        _kind, slots = det_classify(_surface(ref))
        assert slots.get("slug") == slug, f"{ref}: {slots} != {slug}"
    derive_turns = {"S03:12": "derive", "S03:13": "derive"}
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
        assert slots.get("target") == "condition-line-filed", ref
    assertion_turns = ["S02:08", "S02:13"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("what is the statement of the riemann island of record?")[1]["mode"] == "s20-rhsummit"
    assert det_classify("state the rh-reach rule")[1]["mode"] == "s9-state"
    assert det_classify("does my line agree with the conditional root scale?")[1]["mode"] == "s12-agree"
    assert det_classify("the queue above my line, fifth lot, which?")[1]["lot"] == "fifth"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: the queue carries cite the declared queue
    # theorem, the carried condition reads cite the S9/S12 theorems
    # of the line, and the band's own filing is cited by the state
    # readouts and the filing probes
    assert FROZEN["theorem_allowed"] == {
        "S02:01": ["queue-declared"],
        "S02:02": ["queue-declared"],
        "S03:03": ["gap-scale-agreement"],
        "S03:04": ["spf-chain"],
        "S03:05": ["two-routes-one-guarantee"],
        "S03:06": ["two-routes-one-guarantee"],
        "S03:11": ["rh-reach"],
        "S03:14": ["condition-line-filed"],
        "S04:01": ["queue-declared"],
        "S04:02": ["queue-declared"],
        "S04:04": ["condition-line-filed"],
        "S04:07": ["criterion-gap"],
        "S04:08": ["rh-reach"],
        "S04:11": ["condition-line-filed"],
        "S04:17": ["condition-line-filed"],
    }
    # the full sanctioned DAG: forty theorem facts (the S20
    # thirty-nine + condition-line-filed); NO bare island candidate id
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 40
    assert "theorem:condition-line-filed" in dag
    assert "theorem:summit-shape-filed" in dag  # the S20 filing stays in the DAG
    assert "theorem:parity-blowup-filed" in dag  # the S19 soil stays in the DAG
    assert "theorem:line-pi-reduction" in dag  # the S18 soil stays in the DAG
    assert "theorem:queue-declared" in dag  # the S12 declared queue stays in the DAG
    assert "theorem:beal" not in dag, "the bare Beal conj id must NOT exist (the S17 invariant holds)"
    assert "theorem:bsd" not in dag, "the bare BSD conj id stayed gone (the S16 invariant holds)"
    assert "theorem:p-vs-np" not in dag, "the P vs NP island question stays open of record"
    assert "theorem:p-eq-np" not in dag, "the P vs NP island question stays open of record"
    assert "theorem:riemann" not in dag, "the RH island candidate stays open of record"


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH
    assert SCRIPT_HASH == "cdecc888aa781b26"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:16": ["fills the line", "not the condition", "line end 84"],
        "S03:17": ["dropped marker", "misread this store punishes", "line end 84"],
        "S04:14": ["declared queue", "no lot added", "line end 84"],
        "S04:15": ["fills the line", "not the condition", "line end 84"],
    }


def test_band_map_domain_carried() -> None:
    # the condition line lives in the carried RH domain (S10 band
    # map, frozen): no new domain enters the registry
    from kainos.tutor.bands import BAND_MAP

    domains = {d for b in BAND_MAP for d in b.domains}
    assert "rh" in domains, "rh is a band-map domain of record"
    assert "rh" in {c.domain for c in CONCEPTS_E624}, "rh is already in the S20 registry"
    assert {c.domain for c in CONCEPT_S21} == {"rh"}, "no NEW domain enters the S21 registry"
    assert len(CONCEPTS_E625) == 122  # the S20 120 + the two condition concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (1871 final: no carry
    # dedupes net new this band — the four new carry surfaces all
    # drill fresh)
    assert FROZEN["domain_sequence"] == {
        2: "SSSSSUULSSUULSSSS",
        3: "SSSSSSSSSSSFTSSHH",
        4: "SSSSSSSSSSSSSHHSS",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"


def test_discovery_candidate_invariant_full_width() -> None:
    """The D8 gate at FULL width (the condition line must not settle
    an island): no bare island theorem id may exist in the seed
    store — the four candidates stay open of record (the store
    speaks, not the hand)."""
    store = load_store(Path(FROZEN["seed"]))
    ids = {a.id for a in store.query() if a.id}
    for bare in ("theorem:riemann", "theorem:bsd", "theorem:beal", "theorem:p-vs-np", "theorem:p-eq-np"):
        assert bare not in ids, f"{bare}: a bare island theorem fact exists in the seed store"
    # and the riemann conj is still open with its declared source
    conj = store.get("conjecture:riemann")
    assert conj.context.data.get("conjecture_status") == "open"
    assert conj.context.data.get("source_role") == "declared-source"
    # the InMemoryCodexStore import is exercised (the loader seam)
    assert isinstance(store, InMemoryCodexStore)
