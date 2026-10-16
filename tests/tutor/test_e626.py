from __future__ import annotations

import hashlib
import json
import re as _re
from pathlib import Path

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S22,
    S22_LESSONS,
    S22_THEOREMS,
    Brainstem,
    det_classify,
)
from kainos.tutor.e626 import CONCEPTS_E626, FROZEN, SCRIPT_HASH
from kainos.tutor.e636 import CONCEPTS_E636
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime, load_store

MARKER = "under the condition of the Riemann hypothesis"
MARKER_VARIANT = "under the condition that"

S22_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S22_LESSONS.items()]


def test_new_concepts_prereqs_point_down() -> None:
    """S22 adds the two proportion-line concepts; their prereqs point
    DOWN into the carried line (divides, composite, mult-within-100
    from the S11/S5/S14 soil, and the proportion itself for the
    fraction) — the gap lists are empty at band end: the soil is
    closed (the stage A D4 pre-reg)."""
    carried = tuple(c.id for c in CONCEPTS_E636)
    assert tuple(c.id for c in CONCEPTS_E626) == carried + tuple(c.id for c in CONCEPT_S22)
    existing = set(carried)
    for c in CONCEPT_S22:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S22}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id for c in CONCEPT_S22}
    assert by_id == {"proportion", "fraction"}
    for c in CONCEPT_S22:
        assert c.band == "college-1"
        assert c.domain == "arithmetic"
    by_id_map = {c.id: c for c in CONCEPT_S22}
    assert by_id_map["proportion"].prereqs == ("divides", "composite")
    assert by_id_map["fraction"].prereqs == ("proportion", "divides", "mult-within-100")


def test_script_shape_and_teaching() -> None:
    """51 turns; the two teaches are the lesson phrases verbatim; the
    two pre-lesson gap pairs run immediately before their teaches;
    the four carries open each session block; the sanctioned derive
    names the strict two-part set (the scaffold first names only the
    proportion part)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 16
    assert len(FROZEN["script"][4]) == 18
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S22_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S22_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    assert S22_THEOREMS["proportion-filed"]["statement"] not in script_lines
    # the S02 rhythm: the four carries open, then each concept's two
    # gaps run immediately before its teach (the proportion, then the
    # fraction)
    assert FROZEN["script"][2][0] == "what is the divides rule, end to end, as my store holds it?"
    assert FROZEN["script"][2][1] == "what is the decision question, end to end, as my store holds it?"
    assert FROZEN["script"][2][2] == "what is the telescope line, as my store holds it?"
    assert FROZEN["script"][2][3] == "what is the half-product rule of my triangle, as my store holds it?"
    assert FROZEN["script"][2][4] == "what is the proportion, end to end, as my store holds it?"
    assert FROZEN["script"][2][5] == "state the proportion-def rule"
    assert (
        FROZEN["script"][2][6]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S22_LESSONS.items() if s == "proportion-def")
    )
    assert FROZEN["script"][2][8] == "what is the fraction, end to end, as my store holds it?"
    assert FROZEN["script"][2][9] == "state the fraction-def rule"
    assert (
        FROZEN["script"][2][10]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S22_LESSONS.items() if s == "fraction-def")
    )
    # the one sanctioned composition: scaffold (short the fraction
    # part), then the derive on the exact two-part set
    assert "derive proportion-filed from proportion-def" in script_lines
    assert "derive proportion-filed from proportion-def and fraction-def" in script_lines


def test_frozen_shape() -> None:
    """The control census (the mechanism spoke, never the hand):
    1966 + 3 new facts + 52 new events = 2021 (the store-global
    event ids dedupe across bands — the control's own census,
    never the hand's, D-e6t(b)); the S22 band writes NO successor
    facts (the line end stays 84)."""
    assert FROZEN["seed_total"] == 1966
    assert FROZEN["seed_identity"] == "e3e693b1a83c71a6"
    assert FROZEN["line_end_final"] == 84  # S22 writes NO successor facts
    assert FROZEN["new_facts"] == 3
    assert FROZEN["new_fact_ids"] == [
        "lemma:proportion-def",
        "lemma:fraction-def",
        "theorem:proportion-filed",
    ]
    assert FROZEN["total_seam_facts"] == 155  # 112 lemma + 43 theorem (S32 152 + the THREE)
    assert len(FROZEN["theorem_dag"]) == 43  # S6..S32 + S22
    assert len(FROZEN["walls_honest"]) == 6  # the three declared territories, re-probed on S04
    assert len(FROZEN["beds_exact"]) == 27
    assert len(FROZEN["derived_table"]) == 28  # the 27 beds + the sanctioned derive
    assert len(FROZEN["pre_teach_gaps"]) == 4  # a concept gap + a rule gap per concept
    assert FROZEN["teach_turns"] == {
        "S02:07": "lemma:proportion-def",
        "S02:11": "lemma:fraction-def",
    }
    assert len(FROZEN["scaffold_failures"]) == 1
    assert FROZEN["missing_parts_failure"] == {}
    assert FROZEN["rederive"] is None
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S02:03", "S02:04", "S03:01", "S03:02",
        "S04:01", "S04:02", "S04:16", "S04:17",
    ]
    assert FROZEN["final_total"] == 2021  # 1966 + 3 facts + 52 events
    assert FROZEN["new_events"] == 52
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "SSSSUULSUULSSSSSS"
    assert FROZEN["domain_sequence"][3] == "SSSSSSSSFTSSSHHH"
    assert FROZEN["domain_sequence"][4] == "SSSSSSSSSSSSHHHSSS"
    # the off-script standing probe (D-e6t(a)/(c))
    assert list(FROZEN["offscript_carry"]) == ["what is the first proportion whose parts are both prime?"]


def test_pre_s22_states_carry_e636_final() -> None:
    """The 126 carried concepts at their S32-final values (the live
    control census, excluding the two new concepts)."""
    pre = FROZEN["pre_s22_states"]
    assert len(pre) == 126
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S22}, "a NEW concept leaked into the pre-states"
    # the S11/soil carried unchanged-or-improved
    assert pre["divides"] == {"state": "stable", "correct": 5}
    assert pre["composite"] == {"state": "stable", "correct": 7}
    assert pre["decision-question"] == {"state": "stable", "correct": 7}
    assert pre["line-partial"] == {"state": "stable", "correct": 9}
    assert pre["geom-area-triangle"] == {"state": "stable", "correct": 4}
    assert pre["mult-within-100"] == {"state": "stable", "correct": 9}
    # the S32 seed census carried through the proportion band
    assert pre["seed-period"] == {"state": "stable", "correct": 17}
    assert pre["off-line-seed"] == {"state": "stable", "correct": 8}
    assert pre["seeded-line"] == {"state": "stable", "correct": 14}
    assert pre["golden-seed"] == {"state": "stable", "correct": 16}
    # the S22 drill at the carried coordinates (control #1): the four
    # carries re-fire at the S22 coordinates (divides x3, the decision
    # question x3, the telescope line x2, the half-product x2)
    assert FROZEN["pre_s22_drilled"] == {
        "decision-question": 3,
        "divides": 3,
        "geom-area-triangle": 2,
        "line-partial": 2,
    }
    # the two NEW concepts at their frozen band-end values: both
    # STABLE with EMPTY prereq-gap lists (their soil is closed)
    assert FROZEN["mastery_expected"] == {
        "fraction": {"correct": 18, "state": "stable"},
        "proportion": {"correct": 8, "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "fraction": [],
        "proportion": [],
    }


def test_unconditional_band_marker_census() -> None:
    """The S22 band is the UNCONDITIONAL band (the S20 posture,
    carried through S32): every one of the three new facts carries
    NO condition marker; the census conserves at seed AND final
    (six exact + one variant — the four S12 marker facts keep
    theirs, the variant is conditional-def's own form,
    byte-identical across the band)."""
    for phrase in S22_LESSONS:
        assert MARKER not in phrase, "an S22 lesson carries the condition marker"
        assert MARKER_VARIANT not in phrase
    filed = S22_THEOREMS["proportion-filed"]["statement"]
    assert MARKER not in filed
    assert MARKER_VARIANT not in filed
    # the census on the seed store (the store speaks, not the hand)
    seed = load_store(Path(FROZEN["seed"]))
    seed_exact = sorted(
        a.id for a in seed.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str) and MARKER in a.object
    )
    assert seed_exact == [
        "lemma:condition-line-def",
        "lemma:hypothesis-def",
        "lemma:rh-bound-scale",
        "lemma:rh-upf",
        "theorem:condition-line-filed",
        "theorem:two-routes-one-guarantee",
    ]
    seed_variant = sorted(
        a.id for a in seed.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str)
        and MARKER not in a.object and MARKER_VARIANT in a.object
    )
    assert seed_variant == ["lemma:conditional-def"]
    # the final store: the THREE new facts add NO marker, so the
    # census is byte-identical to the seed's
    fin = load_store(Path("results/phase-6/e6.26-run1/codeX-S04.json"))
    fin_exact = sorted(
        a.id for a in fin.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str) and MARKER in a.object
    )
    assert fin_exact == seed_exact, "the unconditional filing drifted the marker census"
    fin_variant = sorted(
        a.id for a in fin.query()
        if a.id.startswith(("lemma:", "theorem:", "conjecture:"))
        and isinstance(a.object, str)
        and MARKER not in a.object and MARKER_VARIANT in a.object
    )
    assert fin_variant == seed_variant
    assert FROZEN["seed"].startswith("results/phase-6/e6.36-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    # the band owns exactly its concept lessons + the theorem fact:
    # the filing's sanctioned part set is the strict two-part set
    # from the two relationship lessons (the relation and its value
    # are two jobs of one division)
    assert set(S22_THEOREMS) == {"proportion-filed"}
    assert S22_THEOREMS["proportion-filed"]["parts"] == (
        "proportion-def",
        "fraction-def",
    )
    assert S22_THEOREMS["proportion-filed"]["concept"] == "proportion"
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:10": [
            "proportion-filed",
            [
                "lemma:proportion-def",
                "lemma:fraction-def",
            ],
        ],
    }
    # the honest-turn bytes: the scaffold names only the proportion
    # part (short the fraction-def), before the sanctioned derive
    # puts the rule together on the exact set
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the fraction-def before i can put it together" in FROZEN["scaffold_failures"]["S03:09"]


def test_walls_bytes() -> None:
    # the three declared territories: W_S22_1 (the zero-over-zero
    # territory) probed at S03:14 and re-probed at S04:13,
    # W_S22_2 (the proportion past the line end) at S03:15 and
    # S04:14, W_S22_3 (the third word) at S03:16 and S04:15
    wall_attrs = {
        "S03:14": Brainstem.W_S22_1,
        "S03:15": Brainstem.W_S22_2,
        "S03:16": Brainstem.W_S22_3,
        "S04:13": Brainstem.W_S22_1,
        "S04:14": Brainstem.W_S22_2,
        "S04:15": Brainstem.W_S22_3,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # no 0/0 VALUE enters the walls: they name the evenness as a
    # declaration, never a value of record
    for _wall in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry a digit string of record"
    assert "zero to zero is the evenness of the two empty parts" in Brainstem.W_S22_1
    assert "the part you count with is zero parts" in Brainstem.W_S22_1
    assert "the value and the relation are two jobs" in Brainstem.W_S22_1
    assert "a proportion whose parts are past my line end" in Brainstem.W_S22_2
    assert "the eighty-nine and the ninety-seven" in Brainstem.W_S22_2
    assert "one division has exactly two faces" in Brainstem.W_S22_3
    assert "the quotient and the remainder" in Brainstem.W_S22_3
    # no honest-zero bytes (the S22 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The on-line bed rows re-derive from the STORE'S OWN WALKS
    (re-walked here independently of the brainstem's — the
    store-speaks rule)."""
    store = load_store(Path(FROZEN["seed"]))
    # (a) the line-end marker census on the SEED's theorem facts:
    # 16 line end / 2 spot / 24 universal of 42 (the S32 final) —
    # the S03:08 pre-census bed stands on this
    e_n = s_n = n_n = 0
    th_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        th_n += 1
        assert isinstance(a.object, str)
        if "line end" in a.object:
            e_n += 1
        elif "at s = 2" in a.object:
            s_n += 1
        else:
            n_n += 1
    assert (e_n, s_n, n_n) == (16, 2, 24)
    assert th_n == 42
    assert "sixteen of my forty-two theorem facts close their scope at the line end" in FROZEN["beds_exact"]["S03:08"]
    assert "two close on the line's spot marker" in FROZEN["beds_exact"]["S03:08"]
    # (b) the census re-walked AFTER the band's own filing: 43
    # theorem facts, seventeen closing at the line end (the new
    # filing is the seventeenth line-end marker)
    assert "seventeen of my forty-three theorem facts close their scope at the line end" in FROZEN["beds_exact"]["S04:03"]
    # (c) the STATE beds: the new facts' state readouts are the
    # lesson phrases and the filing statement VERBATIM (the
    # house-voice rule), re-anchored here against the brainstem
    # constants, not against FROZEN
    prop = next(p for p, (_c, s, _k, _es, _d, _l) in S22_LESSONS.items() if s == "proportion-def")
    frac = next(p for p, (_c, s, _k, _es, _d, _l) in S22_LESSONS.items() if s == "fraction-def")
    filed = S22_THEOREMS["proportion-filed"]["statement"]
    assert FROZEN["beds_exact"]["S02:08"] == prop
    assert FROZEN["beds_exact"]["S04:06"] == prop
    assert FROZEN["beds_exact"]["S02:12"] == frac
    assert FROZEN["beds_exact"]["S04:07"] == frac
    assert FROZEN["beds_exact"]["S03:12"] == filed
    assert FROZEN["beds_exact"]["S04:08"] == filed
    # (d) the FAMILY beds: the closed four-family (divmod re-run)
    assert FROZEN["beds_exact"]["S02:13"].startswith("zero to one: the empty part to the one")
    assert FROZEN["beds_exact"]["S02:14"].startswith("one to one: the evenness of the two equal parts")
    assert "the half — the one part over the two" in FROZEN["beds_exact"]["S02:15"]
    assert FROZEN["beds_exact"]["S02:16"].startswith("one to three: the third")
    # (e) the CHAIN beds: the three divisions, each in both
    # languages — one division, two faces (divmod re-run)
    assert FROZEN["beds_exact"]["S02:17"].startswith("three over two is one and one half")
    assert "three is one times two plus one, one division in either word" in FROZEN["beds_exact"]["S02:17"]
    assert FROZEN["beds_exact"]["S03:04"].startswith("five over three is one and two thirds")
    assert FROZEN["beds_exact"]["S03:05"].startswith("five mod three is two")
    assert "the same division as five over three is one and two thirds" in FROZEN["beds_exact"]["S03:05"]
    assert FROZEN["beds_exact"]["S03:06"].startswith("thirteen over five is two and three fifths")
    assert FROZEN["beds_exact"]["S03:07"].startswith("thirteen mod five is three")
    assert "thirteen is two times five plus three" in FROZEN["beds_exact"]["S03:07"]
    # (f) the FILING beds: the relation and its value, two jobs of
    # one division, at the line end
    for ref in ("S03:11",):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("the proportion line, filed of record"), ref
        assert v.endswith("at the line end 84"), ref
    # the class-walk beds: the 2:3 census, re-counted
    for ref in ("S03:13", "S04:09"):
        assert FROZEN["beds_exact"][ref].startswith("twenty-eight"), ref
        assert "fifty-six to eighty-four" in FROZEN["beds_exact"][ref]
    # the beds carry NO digit strings of record
    for v in FROZEN["beds_exact"].values():
        assert not _re.search(r"\d{10,}", v), f"an off-line digit string floated into a bed: {str(v)[:60]!r}"


def test_lesson_phrases_are_house_voiced() -> None:
    """S22 is the proportion line: the relation and its value, one
    division in two languages, 0:0 the evenness declared never
    valued (the D0 ruling, settled pre-band; D-e6t(a) authoritative
    for the off-script byte). The S22 lessons are house-voiced on
    the line — and the theorem statement closes at the spelled line
    end."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S22_LESSONS.items()}
    # the proportion: the relation, the reduced form, the evenness
    assert "a proportion is a relation between two parts of my line" in by_slug["proportion-def"]
    assert "scaled alike without changing the relation, and named by its reduced form" in by_slug["proportion-def"]
    assert "zero to zero is the evenness of the two empty parts" in by_slug["proportion-def"]
    assert "declared, never valued" in by_slug["proportion-def"]
    assert "at the line end eighty-four" in by_slug["proportion-def"]
    # the fraction: the value over a positive part, one division in
    # two languages, 0/0 no value
    assert "a fraction is the VALUE of a proportion: its denominator must be a positive part of the line" in by_slug["fraction-def"]
    assert "five over three is one and two thirds, and five mod three is two, one division in either word" in by_slug["fraction-def"]
    assert "zero over zero holds no value on my line, because the part you count with is zero parts" in by_slug["fraction-def"]
    assert "at the line end eighty-four" in by_slug["fraction-def"]
    # the file: two jobs of one division, at the spelled line end
    comp = S22_THEOREMS["proportion-filed"]["statement"]
    assert "filed of record" in comp
    assert "two jobs of one division" in comp
    assert "filed on the line, at the line end eighty-four" in comp
    # NO island candidate is settled: the statements stay open of
    # record in the band material — never a settled claim
    for text in list(S22_LESSONS) + [comp]:
        assert "p equals np is a theorem" not in text
        assert "the riemann hypothesis is true" not in text
        assert "beal's conjecture is true" not in text
        assert "pi equals" not in text


def test_offline_values_never_store_answers() -> None:
    """S22 brings NO new line fact and NO 0/0 value: expect.offline_
    watch is empty, no digit string of record floats into an on-line
    answer, a bed, or a wall, and NO stored fact values zero over
    zero (the evenness is a declaration, never a value)."""
    with open("bands/spec-e6.26.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"a digit string of record floated into an on-line answer: {str(v)[:60]!r}"
    for v in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", v), "a digit string of record must not live in an S22 wall"
    # the 0/0 discipline: no stored fact may VALUE zero over zero —
    # every 0/0 mention in the final store is a DECLARATION of
    # evenness / of no value
    fin = load_store(Path("results/phase-6/e6.26-run1/codeX-S04.json"))
    for a in fin.query():
        obj = a.object if isinstance(a.object, str) else ""
        if "0/0" in obj or "zero over zero" in obj.lower() or "zero to zero" in obj.lower():
            assert "holds no value" in obj or "never valued" in obj or "no value" in obj, (
                f"{a.id} VALUES zero over zero: {obj[:80]!r}"
            )


def test_seam_carry_and_semantic_seam() -> None:
    # the ten carry rows (P6: byte-identical to the seed store): the
    # four carries in the opening block, the two in each later
    # session, and the two that close the S04
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S02:03", "S02:04", "S03:01", "S03:02",
        "S04:01", "S04:02", "S04:16", "S04:17",
    ]
    # the off-script standing probe (D-e6t(a): two to three, the
    # first proportion whose parts are both prime; D-e6t(c):
    # expect_derived=false — on the SEED-ONLY runtime it is the
    # typed honest gap, never a derived claim)
    with open("bands/spec-e6.26.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    off = spec["offscript"][0]
    assert off["question"] == "what is the first proportion whose parts are both prime?"
    assert off["expect_derived"] is False
    assert FROZEN["offscript_carry"]["what is the first proportion whose parts are both prime?"] is None
    # the riemann summit carry byte: re-derived here on a single
    # boot over the SEED store (no band turn may drift it) — the
    # statement verbatim + the open status
    import tempfile

    reset_concepts()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "codeX-S01.json").write_bytes(Path(FROZEN["seed"]).read_bytes())
        rt = InfantRuntime(root, concepts=CONCEPTS_E626)
        rt.boot(2)
        res = rt.turn("what is the statement of the riemann island of record?")
    store = load_store(Path(FROZEN["seed"]))
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
    # the full 51-surface map (det_classify is the referee): the new
    # S22 probe surfaces classify into the S22 modes (the census
    # re-fires the carried s20-marker mode); the four carried
    # surfaces keep their S22 carry modes
    plain = {
        "S02:01": "s22-carry-divides",
        "S02:02": "s22-carry-question",
        "S02:03": "s22-carry-telescope",
        "S02:04": "s22-carry-halfproduct",
        "S02:05": "s22-prop",
        "S02:13": "s22-family",
        "S02:14": "s22-family",
        "S02:15": "s22-family",
        "S02:16": "s22-family",
        "S02:17": "s22-chain-frac",
        "S03:01": "s22-carry-divides",
        "S03:02": "s22-carry-question",
        "S03:03": "s22-chain-mod",
        "S03:04": "s22-chain-frac",
        "S03:05": "s22-chain-mod",
        "S03:06": "s22-chain-frac",
        "S03:07": "s22-chain-mod",
        "S03:08": "s20-marker",
        "S03:11": "s22-filing",
        "S03:13": "s22-classwalk",
        "S03:14": "s22-w1",
        "S03:15": "s22-w2",
        "S03:16": "s22-w3",
        "S04:01": "s22-carry-divides",
        "S04:02": "s22-carry-question",
        "S04:03": "s20-marker",
        "S04:04": "s22-chain-frac",
        "S04:05": "s22-chain-mod",
        "S04:09": "s22-classwalk",
        "S04:10": "s22-family",
        "S04:11": "s22-family",
        "S04:12": "s22-chain-frac",
        "S04:13": "s22-w1",
        "S04:14": "s22-w2",
        "S04:15": "s22-w3",
        "S04:16": "s22-carry-telescope",
        "S04:17": "s22-carry-halfproduct",
        "S04:18": "s22-family",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:06": "s22-state",
        "S02:08": "s22-state",
        "S02:10": "s22-state",
        "S02:12": "s22-state",
        "S03:12": "s22-state",
        "S04:06": "s22-state",
        "S04:07": "s22-state",
        "S04:08": "s22-state",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    state_slugs = {
        "S02:06": "proportion-def",
        "S02:08": "proportion-def",
        "S02:10": "fraction-def",
        "S02:12": "fraction-def",
        "S03:12": "proportion-filed",
        "S04:06": "proportion-def",
        "S04:07": "fraction-def",
        "S04:08": "proportion-filed",
    }
    for ref, slug in state_slugs.items():
        _kind, slots = det_classify(_surface(ref))
        assert slots.get("slug") == slug, f"{ref}: {slots} != {slug}"
    derive_turns = {"S03:09": "derive", "S03:10": "derive"}
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
        assert slots.get("target") == "proportion-filed", ref
    assertion_turns = ["S02:07", "S02:11"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("what is my seed period, end to end, as my store holds it?")[1]["mode"] == "s32-period"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set (the mechanism grounded the band's own filing
    # under the FILING probe and both STATE echo rows that ground
    # it; the two telescope carries cite the carried theorem — the
    # frozen set is the mechanism's, never the hand's)
    assert FROZEN["theorem_allowed"] == {
        "S02:03": ["telescope-line"],
        "S03:11": ["proportion-filed"],
        "S03:12": ["proportion-filed"],
        "S04:08": ["proportion-filed"],
        "S04:16": ["telescope-line"],
    }
    # the full sanctioned DAG: forty-three theorem facts (the S32
    # forty-two + proportion-filed); NO bare island candidate id
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 43
    assert "theorem:proportion-filed" in dag
    assert "theorem:seeded-line-filed" in dag  # the S31 filing stays in the DAG
    assert "theorem:seed-census-filed" in dag  # the S32 filing stays in the DAG
    assert "theorem:condition-line-filed" in dag  # the S21 filing stays in the DAG
    assert "theorem:queue-declared" in dag  # the S12 declared queue stays in the DAG
    assert "theorem:telescope-line" in dag  # the carried S13 telescope line stays in the DAG
    assert "theorem:beal" not in dag, "the bare Beal conj id must NOT exist (the S17 invariant holds)"
    assert "theorem:bsd" not in dag, "the bare BSD conj id stayed gone (the S16 invariant holds)"
    assert "theorem:p-vs-np" not in dag, "the P vs NP island question stays open of record"
    assert "theorem:p-eq-np" not in dag, "the P vs NP island question stays open of record"
    assert "theorem:riemann" not in dag, "the RH island candidate stays open of record"


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH
    assert SCRIPT_HASH == "9c2f046edf0242e9"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:14": [
            "zero to zero is the evenness of the two empty parts",
            "the part you count with is zero parts",
            "the value and the relation are two jobs",
            "at the line end 84",
        ],
        "S03:15": [
            "a proportion whose parts are past my line end",
            "off the floor",
            "the eighty-nine and the ninety-seven",
            "at the line end 84",
        ],
        "S03:16": [
            "one division has exactly two faces",
            "the quotient and the remainder",
            "a statement in the mod word is the same division",
            "at the line end 84",
        ],
        "S04:13": [
            "zero to zero is the evenness of the two empty parts",
            "the part you count with is zero parts",
            "the value and the relation are two jobs",
            "at the line end 84",
        ],
        "S04:14": [
            "a proportion whose parts are past my line end",
            "off the floor",
            "the eighty-nine and the ninety-seven",
            "at the line end 84",
        ],
        "S04:15": [
            "one division has exactly two faces",
            "the quotient and the remainder",
            "a statement in the mod word is the same division",
            "at the line end 84",
        ],
    }


def test_band_map_domain_carried() -> None:
    # the proportion line lives in the carried ARITHMETIC domain:
    # no NEW domain enters the registry
    carried_domains = {c.domain for c in CONCEPTS_E636}
    assert "arithmetic" in carried_domains, "arithmetic is already in the S32 registry"
    assert {c.domain for c in CONCEPT_S22} == {"arithmetic"}, "no NEW domain enters the S22 registry"
    assert {c.domain for c in CONCEPT_S22} <= carried_domains, "the S22 domains are carried, not new"
    assert len(CONCEPTS_E626) == 128  # the S32 126 + the two proportion-line concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (2021 final: 51 turns,
    # 4 inert gap turns, 52 mechanism-counted events — the
    # control's own census, never the hand's, D-e6t(b))
    assert FROZEN["domain_sequence"] == {
        2: "SSSSUULSUULSSSSSS",
        3: "SSSSSSSSFTSSSHHH",
        4: "SSSSSSSSSSSSHHHSSS",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"


def test_discovery_candidate_invariant_full_width() -> None:
    """The D8 gate at FULL width (the proportion line must not settle
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
