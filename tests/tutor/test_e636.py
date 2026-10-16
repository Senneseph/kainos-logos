from __future__ import annotations

import hashlib
import json
import re as _re
from pathlib import Path

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S32,
    S32_LESSONS,
    S32_THEOREMS,
    Brainstem,
    det_classify,
)
from kainos.tutor.e635 import CONCEPTS_E635
from kainos.tutor.e636 import CONCEPTS_E636, FROZEN, SCRIPT_HASH
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime, load_store

MARKER = "under the condition of the Riemann hypothesis"
MARKER_VARIANT = "under the condition that"

S32_LESSION_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S32_LESSONS.items()]


def test_new_concepts_prereqs_point_down() -> None:
    """S32 adds the two seed-census concepts; their prereqs point DOWN
    into the carried line (the S4 count-successor, the S5 mod4
    split's territory, and the S31 seeded line — the seed period
    stands on the line the store already holds; the off-line seed
    stands on the line AND the period, so the gap lists are empty
    at band end: the soil is closed, D4 pre-reg)."""
    carried = tuple(c.id for c in CONCEPTS_E635)
    assert tuple(c.id for c in CONCEPTS_E636) == carried + tuple(c.id for c in CONCEPT_S32)
    existing = set(carried)
    for c in CONCEPT_S32:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S32}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id for c in CONCEPT_S32}
    assert by_id == {"seed-period", "off-line-seed"}
    for c in CONCEPT_S32:
        assert c.band == "college-1"
        assert c.domain == "arithmetic"
    by_id_map = {c.id: c for c in CONCEPT_S32}
    assert by_id_map["seed-period"].prereqs == ("seeded-line", "mod4-split", "count-successor")
    assert by_id_map["off-line-seed"].prereqs == ("seeded-line", "seed-period")


def test_script_shape_and_teaching() -> None:
    """51 turns; the two teaches are the lesson phrases verbatim; the
    two pre-lesson gap pairs run immediately before their teaches;
    the sanctioned derive names the strict two-part set (the
    scaffold first names only the seed-period part)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S32_LESSION_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S32_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    assert S32_THEOREMS["seed-census-filed"]["statement"] not in script_lines
    # the S02 rhythm: the queue carried first, then each concept's two
    # gaps run immediately before its teach (the seed period, then the
    # off-line seed)
    assert FROZEN["script"][2][0] == "what is the queue above my line?"
    assert FROZEN["script"][2][1] == "the queue above my line, first lot, which?"
    assert FROZEN["script"][2][2] == "what is my seed period, end to end, as my store holds it?"
    assert FROZEN["script"][2][3] == "state the seed-period-def rule"
    assert (
        FROZEN["script"][2][4]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S32_LESSONS.items() if s == "seed-period-def")
    )
    assert FROZEN["script"][2][8] == "what are the off-line seeds, end to end, as my store holds it?"
    assert FROZEN["script"][2][9] == "state the off-line-seed-def rule"
    assert (
        FROZEN["script"][2][10]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S32_LESSONS.items() if s == "off-line-seed-def")
    )
    # the one sanctioned composition: scaffold (short the off-line
    # part), then the derive on the exact two-part set
    assert "derive seed-census-filed from seed-period-def" in script_lines
    assert "derive seed-census-filed from seed-period-def and off-line-seed-def" in script_lines
    # the carried queue surfaces stand in the script
    assert "what is the queue above my line?" in script_lines
    assert "the queue above my line, first lot, which?" in script_lines


def test_frozen_shape() -> None:
    """The control census (the mechanism spoke, never the hand):
    1921 + 3 new facts + 42 new events = 1966 (the store-global
    event ids dedupe across bands — D-e6s: the control's own
    census, never the hand's); the S32 band writes NO successor
    facts (the line end stays 84)."""
    assert FROZEN["seed_total"] == 1921
    assert FROZEN["seed_identity"] == "898a7c52e43391b6"
    assert FROZEN["line_end_final"] == 84  # S32 writes NO successor facts
    assert FROZEN["new_facts"] == 3
    assert FROZEN["new_fact_ids"] == [
        "lemma:seed-period-def",
        "lemma:off-line-seed-def",
        "theorem:seed-census-filed",
    ]
    assert FROZEN["total_seam_facts"] == 152  # 110 lemma + 42 theorem (S31 149 + the THREE)
    assert len(FROZEN["theorem_dag"]) == 42  # S6..S32
    assert len(FROZEN["walls_honest"]) == 6  # the three declared territories, re-probed on S04
    assert len(FROZEN["beds_exact"]) == 31
    assert len(FROZEN["derived_table"]) == 32  # the 31 beds + the sanctioned derive
    assert len(FROZEN["pre_teach_gaps"]) == 4  # a concept gap + a rule gap per concept
    assert FROZEN["teach_turns"] == {
        "S02:05": "lemma:seed-period-def",
        "S02:11": "lemma:off-line-seed-def",
    }
    assert len(FROZEN["scaffold_failures"]) == 1
    assert FROZEN["missing_parts_failure"] == {}
    assert FROZEN["rederive"] is None
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S03:01", "S03:02", "S04:01", "S04:02",
    ]
    assert FROZEN["final_total"] == 1966  # 1921 + 3 facts + 42 events (D-e6s dedupe)
    assert FROZEN["new_events"] == 42
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "SSUULSSSUULSSSSSS"
    assert FROZEN["domain_sequence"][3] == "SSSSSSSSFTSSSHHHS"
    assert FROZEN["domain_sequence"][4] == "SSSSSSSSSSSSHHHSS"
    # the off-script standing check: the first lot of the queue
    assert list(FROZEN["offscript_carry"]) == ["the queue above my line, first lot, which?"]


def test_pre_s32_states_carry_e635_final() -> None:
    """The 124 carried concepts at their S31-final values (the live
    control census, excluding the two new concepts)."""
    pre = FROZEN["pre_s32_states"]
    assert len(pre) == 124
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S32}, "a NEW concept leaked into the pre-states"
    # the S20/S21 soil carried unchanged-or-improved
    assert pre["weave"] == {"state": "stable", "correct": 8}
    assert pre["summit-shape"] == {"state": "practicing", "correct": 8}
    assert pre["shadow-form"] == {"state": "stable", "correct": 11}
    assert pre["boundary-form"] == {"state": "stable", "correct": 5}
    # the RH line carried through the condition band
    assert pre["riemann"] == {"state": "practicing", "correct": 17}
    assert pre["rh-scale"] == {"state": "practicing", "correct": 24}
    assert pre["rh-relevance"] == {"state": "practicing", "correct": 23}
    assert pre["factor-route"] == {"state": "practicing", "correct": 19}
    assert pre["conditional"] == {"state": "practicing", "correct": 2}
    # the island summits the queue declared
    assert pre["beal-summit"] == {"state": "stable", "correct": 7}
    assert pre["bsd-summit"] == {"state": "stable", "correct": 13}
    assert pre["pnp-summit"] == {"state": "stable", "correct": 7}
    assert pre["class-p"] == {"state": "stable", "correct": 4}
    assert pre["class-np"] == {"state": "stable", "correct": 5}
    # the S14 soil: ALL STABLE
    assert pre["add-two-digit"] == {"state": "stable", "correct": 11}
    assert pre["mult-within-100"] == {"state": "stable", "correct": 9}
    assert pre["count-successor"] == {"state": "stable", "correct": 14}
    # the S31 seeded line carried through the seed-census band
    assert pre["seeded-line"] == {"state": "stable", "correct": 14}
    assert pre["golden-seed"] == {"state": "stable", "correct": 15}
    # the S32 drill at the carried coordinates (control #1): the
    # lucas re-walk fires the golden seed once; the post census at
    # the shadow form
    assert FROZEN["pre_s32_drilled"] == {
        "golden-seed": 1,
        "shadow-form": 1,
    }
    # the two NEW concepts at their frozen band-end values: both
    # STABLE with EMPTY prereq-gap lists (their soil is closed)
    assert FROZEN["mastery_expected"] == {
        "off-line-seed": {"correct": 8, "state": "stable"},
        "seed-period": {"correct": 17, "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "off-line-seed": [],
        "seed-period": [],
    }


def test_unconditional_band_marker_census() -> None:
    """The S32 band is the UNCONDITIONAL band (the S20 posture,
    carried through S31): every one of the three new facts carries
    NO condition marker; the census conserves at seed AND final
    (six exact + one variant — the four S12 marker facts keep
    theirs, the variant is conditional-def's own form,
    byte-identical across the band)."""
    for phrase in S32_LESSONS:
        assert MARKER not in phrase, "an S32 lesson carries the condition marker"
        assert MARKER_VARIANT not in phrase
    filed = S32_THEOREMS["seed-census-filed"]["statement"]
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
    fin = load_store(Path(FROZEN["seed"].replace("e6.35-run1", "e6.36-run1")))
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
    assert FROZEN["seed"].startswith("results/phase-6/e6.35-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    # the D-e6s(a) form: the frozen c0 contract admits a band owning
    # exactly its concept lessons + the theorem facts — the six
    # record clauses stand FOLDED in the two lessons, the filing's
    # sanctioned part set is the strict two-part set, never the
    # pre-registered three-part set (the record clauses are not
    # store facts of the band)
    assert set(S32_THEOREMS) == {"seed-census-filed"}
    assert S32_THEOREMS["seed-census-filed"]["parts"] == (
        "seed-period-def",
        "off-line-seed-def",
    )
    assert S32_THEOREMS["seed-census-filed"]["concept"] == "seed-period"
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:10": [
            "seed-census-filed",
            [
                "lemma:seed-period-def",
                "lemma:off-line-seed-def",
            ],
        ],
    }
    # the honest-turn bytes: the scaffold names only the seed-period
    # part (short the off-line-seed-def), before the sanctioned
    # derive puts the rule together on the exact set
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the off-line-seed-def before i can put it together" in FROZEN["scaffold_failures"]["S03:09"]


def test_walls_bytes() -> None:
    # the three declared territories: W_S32_1 (the off-line
    # residue) probed at S03:14 and re-probed at S04:13,
    # W_S32_2 (the no-repeat of the value story) at S03:15 and
    # S04:14, W_S32_3 (the golden collapse) at S03:16 and S04:15
    wall_attrs = {
        "S03:14": Brainstem.W_S32_1,
        "S03:15": Brainstem.W_S32_2,
        "S03:16": Brainstem.W_S32_3,
        "S04:13": Brainstem.W_S32_1,
        "S04:14": Brainstem.W_S32_2,
        "S04:15": Brainstem.W_S32_3,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the no-new-decimals rule: the walls name positions and the
    # story, never a digit string of record
    for _wall in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry an off-line digit string"
    assert "pi, e, and the golden seed stand off my line" in Brainstem.W_S32_1
    assert "the floor asks the residue question only of what stands on it" in Brainstem.W_S32_1
    assert "a line seeded by a seed of two or more never repeats a value" in Brainstem.W_S32_2
    assert "the period of the value story is declared none" in Brainstem.W_S32_2
    assert "that multiplier never one" in Brainstem.W_S32_3
    assert "its nearest approach to the one its own reciprocal" in Brainstem.W_S32_3
    # no honest-zero bytes (the S32 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The on-line bed rows re-derive from the STORE'S OWN WALKS
    (re-walked here independently of the brainstem's — the
    store-speaks rule)."""
    store = load_store(Path(FROZEN["seed"]))
    # (a) the line-end marker census on the SEED's theorem facts:
    # 15 line end / 2 spot / 24 universal of 41 (the S31 final:
    # 14 + the seeded-line filing) — the S02:17 and S03:08
    # pre-census beds stand on this
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
    assert (e_n, s_n, n_n) == (15, 2, 24)
    assert th_n == 41
    for ref in ("S02:17", "S03:08"):
        assert "fifteen of my forty-one theorem facts close their scope at the line end" in FROZEN["beds_exact"][ref], ref
        assert "two close on the line's spot marker" in FROZEN["beds_exact"][ref]
    # (b) the census re-walked AFTER the band's own filing: 42
    # theorem facts, sixteen closing at the line end (the new filing
    # is the sixteenth line-end marker)
    for ref in ("S03:13", "S04:03"):
        assert "sixteen of my forty-two theorem facts close their scope at the line end" in FROZEN["beds_exact"][ref], ref
    # (c) the STATE beds: the new facts' state readouts are the
    # lesson phrases and the filing statement VERBATIM (the
    # house-voice rule), re-anchored here against the brainstem
    # constants, not against FROZEN
    sp = next(p for p, (_c, s, _k, _es, _d, _l) in S32_LESSONS.items() if s == "seed-period-def")
    ol = next(p for p, (_c, s, _k, _es, _d, _l) in S32_LESSONS.items() if s == "off-line-seed-def")
    filed = S32_THEOREMS["seed-census-filed"]["statement"]
    assert FROZEN["beds_exact"]["S02:06"] == sp
    assert FROZEN["beds_exact"]["S04:05"] == sp
    assert FROZEN["beds_exact"]["S02:12"] == ol
    assert FROZEN["beds_exact"]["S04:06"] == ol
    assert FROZEN["beds_exact"]["S03:12"] == filed
    assert FROZEN["beds_exact"]["S04:07"] == filed
    # (d) the value-story beds: the constant story and the page's
    # numbers, all standing off the floor
    assert "no — a seed of two or more never repeats a value" in FROZEN["beds_exact"]["S02:13"]
    assert "my sum line walks even, odd, odd" in FROZEN["beds_exact"]["S02:14"]
    assert "divides the term at the sixth, the eight, four times" in FROZEN["beds_exact"]["S02:15"]
    assert "the seeds three mod five carry their period at a fifth of the pisano count" in FROZEN["beds_exact"]["S02:16"]
    assert "the fibonacci sequence the page names" in FROZEN["beds_exact"]["S03:03"]
    assert "the lucas numbers" in FROZEN["beds_exact"]["S03:05"]
    assert "sign turned when n is even and kept when n is odd" in FROZEN["beds_exact"]["S03:06"]
    assert "the fibonacci sequence the page holds" in FROZEN["beds_exact"]["S03:07"]
    # (e) the FILING beds: the census, not the census gaps — the
    # constants stay off the floor
    for ref in ("S03:11", "S04:04"):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("the census, not the census gaps"), ref
        assert v.endswith("at the line end 84"), ref
    # the beds carry NO off-line digit strings of record
    for v in FROZEN["beds_exact"].values():
        assert not _re.search(r"\d{10,}", v), f"a bed must not carry an off-line digit string: {str(v)[:60]!r}"


def test_lesson_phrases_are_house_voiced() -> None:
    """S32 is the seed census: the line's residue story and the
    value story of the constants off the floor, in the page's own
    wordings (the owner's 2026-08-28 directive). The S32 lessons
    are house-voiced on the line — and the theorem statement
    closes at the spelled line end."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S32_LESSONS.items()}
    # the seed period: the skeleton's own paisano count, the class
    # three shadow, the parity rotation, the law of my sums
    # dividing
    assert "on the skeleton's own cycle" in by_slug["seed-period-def"]
    assert "at exactly the pisano count" in by_slug["seed-period-def"]
    assert "a fifth of the pisano count" in by_slug["seed-period-def"]
    assert "the parity of my seeded lines" in by_slug["seed-period-def"]
    assert "the law of my sums dividing" in by_slug["seed-period-def"]
    assert "zero violations" in by_slug["seed-period-def"]
    assert "at the line end eighty-four" in by_slug["seed-period-def"]
    # the off-line seed: the constants by name and role, never by a
    # digit; the page's names woven in
    assert "pi, e, and the golden seed" in by_slug["off-line-seed-def"]
    assert "the golden ratio the page names, its letter phi" in by_slug["off-line-seed-def"]
    assert "never by a digit" in by_slug["off-line-seed-def"]
    assert "the lucas numbers the page names" in by_slug["off-line-seed-def"]
    assert "the fibonacci sequence the page names" in by_slug["off-line-seed-def"]
    assert "the one divided by my eighty-nine" in by_slug["off-line-seed-def"]
    assert "declared, not filed" in by_slug["off-line-seed-def"]
    assert "at the line end eighty-four" in by_slug["off-line-seed-def"]
    # the file: the census, not the census gaps, at the spelled line
    # end
    comp = S32_THEOREMS["seed-census-filed"]["statement"]
    assert "filed of record" in comp
    assert "the strict two-part set" not in comp  # the form lives in the record, not the fact
    assert "filed on the line, at the line end eighty-four" in comp
    # NO island candidate is settled: the statements stay open of
    # record in the band material — never a settled claim
    for text in list(S32_LESSONS) + [comp]:
        assert "p equals np is a theorem" not in text
        assert "the riemann hypothesis is true" not in text
        assert "beal's conjecture is true" not in text
        assert "pi equals" not in text


def test_offline_values_never_store_answers() -> None:
    """S32 brings NO new off-line value: expect.offline_watch is
    empty, and no off-line digit string floats into an on-line
    answer, a bed, or a wall (the one over eighty-nine is a
    decimal shadow of the CEILING, declared, never filed — the
    ceiling itself, the eighty-nine, is line content)."""
    with open("bands/spec-e6.36.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"an off-line digit string floated into an on-line answer: {str(v)[:60]!r}"
    for v in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", v), "an off-line digit string must not live in an S32 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the six carry rows (P6: byte-identical to the seed store):
    # the queue and its first lot, each session's opening pair
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S03:01", "S03:02", "S04:01", "S04:02",
    ]
    # the off-script standing check: the first lot of the queue,
    # byte-identical to the store's own declared record (the queue
    # stands untouched — the course adds no lot)
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
        rt = InfantRuntime(root, concepts=CONCEPTS_E636)
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
    # the full 51-surface map (det_classify is the referee): the
    # thirty-six new S32 probe surfaces classify into the S32
    # modes (the census re-fires the carried s20-marker mode); the
    # carried queue surfaces keep their S12 modes
    plain = {
        "S02:01": "s12-queue",
        "S02:02": "s12-queue-lot",
        "S02:03": "s32-period",
        "S02:07": "s32-pisano8",
        "S02:08": "s32-pisano12",
        "S02:09": "s32-offline",
        "S02:13": "s32-value",
        "S02:14": "s32-parity",
        "S02:15": "s32-divides",
        "S02:16": "s32-shadow5",
        "S02:17": "s20-marker",
        "S03:01": "s12-queue",
        "S03:02": "s12-queue-lot",
        "S03:03": "s32-pagenames",
        "S03:04": "s32-goldenpower",
        "S03:05": "s32-lucas",
        "S03:06": "s32-belowzero",
        "S03:07": "s32-recip89",
        "S03:08": "s20-marker",
        "S03:11": "s32-filing",
        "S03:13": "s20-marker",
        "S03:14": "s32-w1",
        "S03:15": "s32-w2",
        "S03:16": "s32-w3",
        "S03:17": "s32-shadow5",
        "S04:01": "s12-queue",
        "S04:02": "s12-queue-lot",
        "S04:03": "s20-marker",
        "S04:04": "s32-filing",
        "S04:08": "s32-pisano8",
        "S04:09": "s32-value",
        "S04:10": "s32-lucas",
        "S04:11": "s32-pagenames",
        "S04:12": "s32-shadow5",
        "S04:13": "s32-w1",
        "S04:14": "s32-w2",
        "S04:15": "s32-w3",
        "S04:16": "s32-parity",
        "S04:17": "s32-divides",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:04": "s32-state",
        "S02:06": "s32-state",
        "S02:10": "s32-state",
        "S02:12": "s32-state",
        "S03:12": "s32-state",
        "S04:05": "s32-state",
        "S04:06": "s32-state",
        "S04:07": "s32-state",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    state_slugs = {
        "S02:04": "seed-period-def",
        "S02:06": "seed-period-def",
        "S02:10": "off-line-seed-def",
        "S02:12": "off-line-seed-def",
        "S03:12": "seed-census-filed",
        "S04:05": "seed-period-def",
        "S04:06": "off-line-seed-def",
        "S04:07": "seed-census-filed",
    }
    for ref, slug in state_slugs.items():
        _kind, slots = det_classify(_surface(ref))
        assert slots.get("slug") == slug, f"{ref}: {slots} != {slug}"
    derive_turns = {"S03:09": "derive", "S03:10": "derive"}
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
        assert slots.get("target") == "seed-census-filed", ref
    assertion_turns = ["S02:05", "S02:11"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("the queue above my line, first lot, which?")[1]["lot"] == "first"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set (the mechanism grounded the band's own filing
    # under both STATE echo rows and the FILING probes — the
    # frozen set is the mechanism's, never the hand's): the queue
    # carries cite the declared queue theorem, and
    # seed-census-filed is cited by the state readouts and the
    # filing probes (the four turns that ground it)
    assert FROZEN["theorem_allowed"] == {
        "S02:01": ["queue-declared"],
        "S02:02": ["queue-declared"],
        "S03:01": ["queue-declared"],
        "S03:02": ["queue-declared"],
        "S03:11": ["seed-census-filed"],
        "S03:12": ["seed-census-filed"],
        "S04:01": ["queue-declared"],
        "S04:02": ["queue-declared"],
        "S04:04": ["seed-census-filed"],
        "S04:07": ["seed-census-filed"],
    }
    # the full sanctioned DAG: forty-two theorem facts (the S31
    # forty-one + seed-census-filed); NO bare island candidate id
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 42
    assert "theorem:seed-census-filed" in dag
    assert "theorem:seeded-line-filed" in dag  # the S31 filing stays in the DAG
    assert "theorem:condition-line-filed" in dag  # the S21 filing stays in the DAG
    assert "theorem:summit-shape-filed" in dag  # the S20 filing stays in the DAG
    assert "theorem:queue-declared" in dag  # the S12 declared queue stays in the DAG
    assert "theorem:beal" not in dag, "the bare Beal conj id must NOT exist (the S17 invariant holds)"
    assert "theorem:bsd" not in dag, "the bare BSD conj id stayed gone (the S16 invariant holds)"
    assert "theorem:p-vs-np" not in dag, "the P vs NP island question stays open of record"
    assert "theorem:p-eq-np" not in dag, "the P vs NP island question stays open of record"
    assert "theorem:riemann" not in dag, "the RH island candidate stays open of record"


def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH
    assert SCRIPT_HASH == "8c511586bbab22fc"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:14": [
            "pi, e, and the golden seed stand off my line",
            "the floor asks the residue question only of what stands on it",
            "a misreading the floor's own declaration refutes",
            "at the line end 84",
        ],
        "S03:15": [
            "a line seeded by a seed of two or more never repeats a value",
            "the seed-one line shares its one at the start and outgrows after",
            "at the line end 84",
            "the period of the value story is declared none",
        ],
        "S03:16": [
            "that multiplier never one",
            "its nearest approach to the one its own reciprocal",
            "at the line end 84",
            "a repeat claimed",
        ],
        "S04:13": [
            "pi, e, and the golden seed stand off my line",
            "the floor asks the residue question only of what stands on it",
            "a misreading the floor's own declaration refutes",
            "at the line end 84",
        ],
        "S04:14": [
            "a line seeded by a seed of two or more never repeats a value",
            "the seed-one line shares its one at the start and outgrows after",
            "at the line end 84",
            "the period of the value story is declared none",
        ],
        "S04:15": [
            "that multiplier never one",
            "its nearest approach to the one its own reciprocal",
            "at the line end 84",
            "a repeat claimed",
        ],
    }


def test_band_map_domain_carried() -> None:
    # the seed census lives in the carried ARITHMETIC domain (the
    # S14/S5 sum-line territory, the D-e6q(d) discipline carried):
    # no NEW domain enters the registry
    carried_domains = {c.domain for c in CONCEPTS_E635}
    assert "arithmetic" in carried_domains, "arithmetic is already in the S31 registry"
    assert {c.domain for c in CONCEPT_S32} == {"arithmetic"}, "no NEW domain enters the S32 registry"
    assert {c.domain for c in CONCEPT_S32} <= carried_domains, "the S32 domains are carried, not new"
    assert len(CONCEPTS_E636) == 126  # the S31 124 + the two seed-census concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (1966 final: 51 turns,
    # 4 inert gap turns, 42 mechanism-counted events after the
    # store-global event-id dedupe — D-e6s, the control's own
    # census, never the hand's -5 against the naive 47)
    assert FROZEN["domain_sequence"] == {
        2: "SSUULSSSUULSSSSSS",
        3: "SSSSSSSSFTSSSHHHS",
        4: "SSSSSSSSSSSSHHHSS",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"


def test_discovery_candidate_invariant_full_width() -> None:
    """The D8 gate at FULL width (the seed census must not settle an
    island): no bare island theorem id may exist in the seed store —
    the four candidates stay open of record (the store speaks, not
    the hand)."""
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
