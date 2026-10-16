from __future__ import annotations

import hashlib
import json
import re as _re
from pathlib import Path

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S23,
    S23_LESSONS,
    S23_THEOREMS,
    Brainstem,
    det_classify,
)
from kainos.tutor.e626 import CONCEPTS_E626
from kainos.tutor.e627 import CONCEPTS_E627, FROZEN, SCRIPT_HASH
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime, load_store

MARKER = "under the condition of the Riemann hypothesis"
MARKER_VARIANT = "under the condition that"

S23_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S23_LESSONS.items()]


def test_new_concepts_prereqs_point_down() -> None:
    """S23 adds the two prime-proportion concepts; their prereqs
    point DOWN into the carried line (divides and first-divisor
    from the S11 soil, composite from the S5/S14 soil, the coprime
    pair itself for the fingerprint) — the gap lists are empty at
    band end: the soil is closed (the stage A D4 pre-reg)."""
    carried = tuple(c.id for c in CONCEPTS_E626)
    assert tuple(c.id for c in CONCEPTS_E627) == carried + tuple(c.id for c in CONCEPT_S23)
    existing = set(carried)
    for c in CONCEPT_S23:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S23}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id for c in CONCEPT_S23}
    assert by_id == {"coprime-pair", "prime-fingerprint"}
    for c in CONCEPT_S23:
        assert c.band == "college-1"
        assert c.domain == "arithmetic"
    by_id_map = {c.id: c for c in CONCEPT_S23}
    assert by_id_map["coprime-pair"].prereqs == ("divides", "first-divisor")
    assert by_id_map["prime-fingerprint"].prereqs == ("coprime-pair", "composite")


def test_script_shape_and_teaching() -> None:
    """51 turns; the two teaches are the lesson phrases verbatim;
    the two pre-lesson gap pairs run immediately before their
    teaches; the four carries open the S02; the sanctioned derive
    names the strict two-part set (the scaffold first names only
    the coprime-pair part)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S23_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S23_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    assert S23_THEOREMS["fingerprint-filed"]["statement"] not in script_lines
    # the S02 rhythm: the four carries open, then each concept's two
    # gaps run immediately before its teach (the coprime pair, then
    # the prime fingerprint)
    assert FROZEN["script"][2][0] == "state the spf-def rule"
    assert FROZEN["script"][2][1] == "what is the divides rule, end to end, as my store holds it?"
    assert FROZEN["script"][2][2] == "what is the decision question, end to end, as my store holds it?"
    assert FROZEN["script"][2][3] == "what does the proportion filing settle of record?"
    assert FROZEN["script"][2][4] == "what is the coprime pair, end to end, as my store holds it?"
    assert FROZEN["script"][2][5] == "state the coprime-pair-def rule"
    assert (
        FROZEN["script"][2][6]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S23_LESSONS.items() if s == "coprime-pair-def")
    )
    assert FROZEN["script"][2][8] == "what is the prime fingerprint, end to end, as my store holds it?"
    assert FROZEN["script"][2][9] == "state the prime-fingerprint-def rule"
    assert (
        FROZEN["script"][2][10]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S23_LESSONS.items() if s == "prime-fingerprint-def")
    )
    # the one sanctioned composition: scaffold (short the
    # prime-fingerprint part), then the derive on the exact
    # two-part set
    assert "derive fingerprint-filed from coprime-pair-def" in script_lines
    assert "derive fingerprint-filed from coprime-pair-def and prime-fingerprint-def" in script_lines


def test_frozen_shape() -> None:
    """The control census (the mechanism spoke, never the hand):
    2021 + 3 new facts + 50 new events = 2074 (the store-global
    event ids dedupe across bands — the control's own census,
    never the hand's, D-e6u(a)); the S23 band writes NO successor
    facts (the line end stays 84)."""
    assert FROZEN["seed_total"] == 2021
    assert FROZEN["seed_identity"] == "c5eee97dcd92a636"
    assert FROZEN["line_end_final"] == 84  # S23 writes NO successor facts
    assert FROZEN["new_facts"] == 3
    assert FROZEN["new_fact_ids"] == [
        "lemma:coprime-pair-def",
        "lemma:prime-fingerprint-def",
        "theorem:fingerprint-filed",
    ]
    assert FROZEN["total_seam_facts"] == 158  # 114 lemma + 44 theorem (S22 155 + the THREE)
    assert len(FROZEN["theorem_dag"]) == 44  # S6..S21 + S31 + S32 + S22 + S23
    assert len(FROZEN["walls_honest"]) == 5  # the declared territories: W_S23_1 twice, W_S23_2, W_S23_3, + the carried 0:0 re-probe (W_S22_1)
    assert len(FROZEN["beds_exact"]) == 29
    assert len(FROZEN["derived_table"]) == 30  # the 29 beds + the sanctioned derive
    assert len(FROZEN["pre_teach_gaps"]) == 4  # a concept gap + a rule gap per concept
    assert FROZEN["teach_turns"] == {
        "S02:07": "lemma:coprime-pair-def",
        "S02:11": "lemma:prime-fingerprint-def",
    }
    assert len(FROZEN["scaffold_failures"]) == 1
    assert FROZEN["missing_parts_failure"] == {}
    assert FROZEN["rederive"] is None
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S02:03", "S02:04", "S03:01", "S03:02",
        "S04:01", "S04:02", "S04:16",
    ]
    assert FROZEN["final_total"] == 2074  # 2021 + 3 facts + 50 events
    assert FROZEN["new_events"] == 50
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "SSSSUULSUULSSSSSS"
    assert FROZEN["domain_sequence"][3] == "SSSSSSSSSSSSSFTSH"
    assert FROZEN["domain_sequence"][4] == "SSHHHHSSSSSSSSSSS"
    # the off-script standing probe (D-e6u(b)/(c))
    assert list(FROZEN["offscript_carry"]) == ["what is the first proportion where the parts are primes above two?"]


def test_pre_s23_states_carry_e626_final() -> None:
    """The 128 carried concepts at their S22-final values (the live
    control census, excluding the two new concepts)."""
    pre = FROZEN["pre_s23_states"]
    assert len(pre) == 128
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S23}, "a NEW concept leaked into the pre-states"
    # the S11/soil carried unchanged-or-improved
    assert pre["divides"] == {"state": "stable", "correct": 8}
    assert pre["first-divisor"] == {"state": "stable", "correct": 36}
    assert pre["composite"] == {"state": "stable", "correct": 7}
    assert pre["decision-question"] == {"state": "stable", "correct": 10}
    assert pre["line-partial"] == {"state": "stable", "correct": 11}
    assert pre["mult-within-100"] == {"state": "stable", "correct": 9}
    # the S22 final carried through the prime-proportion band
    assert pre["proportion"] == {"state": "stable", "correct": 8}
    assert pre["fraction"] == {"state": "stable", "correct": 18}
    assert pre["seed-period"] == {"state": "stable", "correct": 17}
    assert pre["off-line-seed"] == {"state": "stable", "correct": 8}
    assert pre["seeded-line"] == {"state": "stable", "correct": 14}
    assert pre["golden-seed"] == {"state": "stable", "correct": 16}
    # the S23 drill at the carried coordinates (control #1): the
    # carries re-fire at the S23 coordinates (the first-divisor x6,
    # the divides rule x4, the decision question x3, the proportion
    # filing x4 — the marker census probe credits the S6
    # shadow-form ground)
    assert FROZEN["pre_s23_drilled"] == {
        "decision-question": 1,
        "divides": 2,
        "first-divisor": 2,
        "proportion": 1,
        "shadow-form": 1,
    }
    # the two NEW concepts at their frozen band-end values: both
    # STABLE with EMPTY prereq-gap lists (their soil is closed)
    assert FROZEN["mastery_expected"] == {
        "coprime-pair": {"correct": 6, "state": "stable"},
        "prime-fingerprint": {"correct": 23, "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "coprime-pair": [],
        "prime-fingerprint": [],
    }


def test_unconditional_band_marker_census() -> None:
    """The S23 band is the UNCONDITIONAL band (the S20 posture,
    carried through S22): every one of the three new facts carries
    NO condition marker; the census conserves at seed AND final
    (six exact + one variant — the four S12 marker facts keep
    theirs, the variant is conditional-def's own form,
    byte-identical across the band)."""
    for phrase in S23_LESSONS:
        assert MARKER not in phrase, "an S23 lesson carries the condition marker"
        assert MARKER_VARIANT not in phrase
    filed = S23_THEOREMS["fingerprint-filed"]["statement"]
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
    fin = load_store(Path("results/phase-6/e6.27-run1/codeX-S04.json"))
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
    assert FROZEN["seed"].startswith("results/phase-6/e6.26-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    # the band owns exactly its concept lessons + the theorem fact:
    # the filing's sanctioned part set is the strict two-part set
    # from the two relationship lessons (the pair and its
    # fingerprint)
    assert set(S23_THEOREMS) == {"fingerprint-filed"}
    assert S23_THEOREMS["fingerprint-filed"]["parts"] == (
        "coprime-pair-def",
        "prime-fingerprint-def",
    )
    assert S23_THEOREMS["fingerprint-filed"]["concept"] == "prime-fingerprint"
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:15": [
            "fingerprint-filed",
            [
                "lemma:coprime-pair-def",
                "lemma:prime-fingerprint-def",
            ],
        ],
    }
    # the honest-turn bytes: the scaffold names only the coprime-
    # pair part (short the prime-fingerprint-def), before the
    # sanctioned derive puts the rule together on the exact set
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the prime-fingerprint-def before i can put it together" in FROZEN["scaffold_failures"]["S03:14"]


def test_walls_bytes() -> None:
    # the declared territories: W_S23_1 (the pair past the line
    # end) probed at S03:17 and re-probed at S04:04, W_S23_2 (the
    # never-reduced discipline) at S04:05, W_S23_3 (the colliding
    # fingerprint) at S04:06 — the 0:0 evenness re-declaration
    # rides the carried W_S22_1 wall byte at S04:03 (the S20
    # re-probe pattern)
    wall_attrs = {
        "S03:17": Brainstem.W_S23_1,
        "S04:03": Brainstem.W_S22_1,
        "S04:04": Brainstem.W_S23_1,
        "S04:05": Brainstem.W_S23_2,
        "S04:06": Brainstem.W_S23_3,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # no digit string of record enters the walls
    for _wall in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry a digit string of record"
    assert "the eighty-three by the seventy-nine is the last prime pair on my line" in Brainstem.W_S23_1
    assert "the pair with the eighty-nine is off the floor" in Brainstem.W_S23_1
    assert "a proportion of two distinct primes never reduces" in Brainstem.W_S23_2
    assert "a proportion that reduces is not a proportion of two distinct primes" in Brainstem.W_S23_2
    assert "two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced proportions" in Brainstem.W_S23_3
    assert "a second pair claiming the first pair's proportion is a misread" in Brainstem.W_S23_3
    assert "zero to zero is the evenness of the two empty parts" in FROZEN["walls_honest"]["S04:03"]
    assert "the value and the relation are two jobs" in FROZEN["walls_honest"]["S04:03"]
    # no honest-zero bytes (the S23 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The on-line bed rows re-derive from the STORE'S OWN WALKS
    (re-walked here independently of the brainstem's — the
    store-speaks rule)."""
    store = load_store(Path(FROZEN["seed"]))
    # (a) the line-end marker census on the SEED's theorem facts:
    # 17 line end / 2 spot / 24 universal of 43 (the S22 final)
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
    assert (e_n, s_n, n_n) == (17, 2, 24)
    assert th_n == 43
    # (b) the census re-walked AFTER the band's own filing: 44
    # theorem facts, eighteen closing at the line end (the new
    # filing is the eighteenth line-end marker)
    assert "eighteen of my forty-four theorem facts close their scope at the line end" in FROZEN["beds_exact"]["S04:17"]
    # (c) the STATE beds: the new facts' state readouts are the
    # lesson phrases and the filing statement VERBATIM (the
    # house-voice rule), re-anchored here against the brainstem
    # constants, not against FROZEN
    copr = next(p for p, (_c, s, _k, _es, _d, _l) in S23_LESSONS.items() if s == "coprime-pair-def")
    fp = next(p for p, (_c, s, _k, _es, _d, _l) in S23_LESSONS.items() if s == "prime-fingerprint-def")
    filed = S23_THEOREMS["fingerprint-filed"]["statement"]
    assert FROZEN["beds_exact"]["S02:08"] == copr
    assert FROZEN["beds_exact"]["S02:12"] == fp
    assert FROZEN["beds_exact"]["S04:09"] == copr
    assert FROZEN["beds_exact"]["S04:10"] == fp
    assert FROZEN["beds_exact"]["S04:11"] == filed
    # (d) the CO-PRIME beds: the four tests, re-walked
    assert FROZEN["beds_exact"]["S02:13"].startswith("two and three: a coprime pair outright")
    assert FROZEN["beds_exact"]["S02:14"].startswith("four and six: not a coprime pair — they share the part two")
    assert FROZEN["beds_exact"]["S02:15"].startswith("no — a proportion of two distinct primes never reduces")
    assert FROZEN["beds_exact"]["S02:16"].startswith("two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced")
    assert FROZEN["beds_exact"]["S02:17"].startswith("the seven-step chain is the ceiling")
    # (e) the CHAIN beds: the six divisions, each in both
    # languages — one division, two faces (divmod re-run)
    assert FROZEN["beds_exact"]["S03:03"].startswith("seven over three is two and one third")
    assert "seven is two times three plus one, one division in either word" in FROZEN["beds_exact"]["S03:03"]
    assert FROZEN["beds_exact"]["S03:04"].startswith("seven mod three is one")
    assert FROZEN["beds_exact"]["S03:05"].startswith("twenty-nine over eleven is two and seven elevenths")
    assert FROZEN["beds_exact"]["S03:06"].startswith("twenty-nine mod eleven is seven")
    assert "twenty-nine is two times eleven plus seven" in FROZEN["beds_exact"]["S03:06"]
    assert FROZEN["beds_exact"]["S03:07"].startswith("twenty-nine over forty-seven is the value under one")
    assert "the value under one" in FROZEN["beds_exact"]["S03:07"]
    assert FROZEN["beds_exact"]["S03:08"].startswith("the first reduction step of twenty-nine to forty-seven")
    assert "forty-seven is one times twenty-nine plus eighteen" in FROZEN["beds_exact"]["S03:08"]
    assert FROZEN["beds_exact"]["S03:09"].startswith("eighty-three over seventy-nine is one and four seventy-ninths")
    assert FROZEN["beds_exact"]["S03:10"].startswith("eighty-three mod two is one")
    assert FROZEN["beds_exact"]["S03:11"].startswith("seventy-one over seven is ten and one seventh")
    # the S04 re-walks: the same divisions, byte-identical
    assert FROZEN["beds_exact"]["S04:13"] == FROZEN["beds_exact"]["S03:07"]
    assert FROZEN["beds_exact"]["S04:14"] == FROZEN["beds_exact"]["S03:10"]
    # (f) the FILING beds: the pair and its fingerprint, filed of
    # record, at the line end
    for ref in ("S03:16", "S04:12"):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("the prime proportion, filed of record"), ref
        assert v.endswith("at the line end 84"), ref
    # the coprime-pair re-test at the S04 close
    assert FROZEN["beds_exact"]["S04:15"].startswith("forty-one and seventy-one: a coprime pair")
    # (g) the CEILING beds: the four tied pairs, re-counted
    for ref in ("S03:12", "S04:08"):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("the seven-step chain is the ceiling"), ref
        assert "twenty-nine by forty-seven, twenty-nine by seventy-nine" in v
        assert "forty-one by sixty-seven" in v
        assert "forty-one by seventy-one" in v
    # the beds carry NO digit strings of record
    for v in FROZEN["beds_exact"].values():
        assert not _re.search(r"\d{10,}", v), f"an off-line digit string floated into a bed: {str(v)[:60]!r}"


def test_lesson_phrases_are_house_voiced() -> None:
    """S23 is the prime proportion: the pair is its own reduced
    proportion, the fingerprint reads the line, the seven-step
    chain is the ceiling. The S23 lessons are house-voiced on the
    line — and the theorem statement closes at the spelled line
    end."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S23_LESSONS.items()}
    # the coprime pair: the shared-part test, the prime-outright
    # case, the no-reduction discipline
    assert "a coprime pair is a pair of parts of my line that share no part above one" in by_slug["coprime-pair-def"]
    assert "a prime's first divisor is itself, so the shared part would have to divide both primes and be none of them" in by_slug["coprime-pair-def"]
    assert "two distinct primes are a coprime pair outright" in by_slug["coprime-pair-def"]
    assert "and a coprime pair needs no reduction: its proportion is already in lowest terms" in by_slug["coprime-pair-def"]
    assert "at the line end eighty-four" in by_slug["coprime-pair-def"]
    # the prime fingerprint: the pair is the proportion
    assert "the proportion of two distinct primes is the fingerprint of the pair" in by_slug["prime-fingerprint-def"]
    assert "the two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced proportions" in by_slug["prime-fingerprint-def"]
    assert "no two pairs alike" in by_slug["prime-fingerprint-def"]
    assert "at the line end eighty-four" in by_slug["prime-fingerprint-def"]
    # the file: the fingerprint of record, at the spelled line end
    comp = S23_THEOREMS["fingerprint-filed"]["statement"]
    assert "filed of record" in comp
    assert "two hundred and fifty-three pairs, two hundred and fifty-three proportions, no collisions on my line" in comp
    assert "filed on the line, at the line end eighty-four" in comp
    # NO island candidate is settled: the statements stay open of
    # record in the band material — never a settled claim
    for text in list(S23_LESSONS) + [comp]:
        assert "p equals np is a theorem" not in text
        assert "the riemann hypothesis is true" not in text
        assert "beal's conjecture is true" not in text
        assert "pi equals" not in text


def test_offline_values_never_store_answers() -> None:
    """S23 brings NO new line fact and NO 0/0 value: expect.offline_
    watch is empty, no digit string of record floats into an on-line
    answer, a bed, or a wall, and NO stored fact values zero over
    zero (the evenness is a declaration, never a value)."""
    with open("bands/spec-e6.27.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"a digit string of record floated into an on-line answer: {str(v)[:60]!r}"
    for v in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", v), "a digit string of record must not live in an S23 wall"
    # the 0/0 discipline: no stored fact may VALUE zero over zero —
    # every 0/0 mention in the final store is a DECLARATION of
    # evenness / of no value
    fin = load_store(Path("results/phase-6/e6.27-run1/codeX-S04.json"))
    for a in fin.query():
        obj = a.object if isinstance(a.object, str) else ""
        if "0/0" in obj or "zero over zero" in obj.lower() or "zero to zero" in obj.lower():
            assert "holds no value" in obj or "never valued" in obj or "no value" in obj, (
                f"{a.id} VALUES zero over zero: {obj[:80]!r}"
            )


def test_seam_carry_and_semantic_seam() -> None:
    # the nine carry rows (P6: byte-identical to the seed store):
    # the four carries in the S02 opening block, the two in each
    # later session, and the telescope carry that closes the S04
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S02:03", "S02:04", "S03:01", "S03:02",
        "S04:01", "S04:02", "S04:16",
    ]
    # the off-script standing probe (D-e6u(b): three to five, the
    # first proportion whose parts are primes above two; D-e6u(c):
    # expect_derived=false — on the SEED-ONLY runtime it is the
    # typed honest gap, never a derived claim)
    with open("bands/spec-e6.27.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    off = spec["offscript"][0]
    assert off["question"] == "what is the first proportion where the parts are primes above two?"
    assert off["expect_derived"] is False
    assert FROZEN["offscript_carry"]["what is the first proportion where the parts are primes above two?"] is None
    # the riemann summit carry byte: re-derived here on a single
    # boot over the SEED store (no band turn may drift it) — the
    # statement verbatim + the open status
    import tempfile

    reset_concepts()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "codeX-S01.json").write_bytes(Path(FROZEN["seed"]).read_bytes())
        rt = InfantRuntime(root, concepts=CONCEPTS_E627)
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
    # S23 probe surfaces classify into the S23 modes (the census
    # re-fires the carried s20-marker mode at S04:17); the carried
    # surfaces keep their modes
    plain = {
        "S02:02": "s22-carry-divides",
        "S02:03": "s22-carry-question",
        "S02:04": "s22-filing",
        "S02:05": "s23-cop",
        "S02:13": "s23-coprime",
        "S02:14": "s23-coprime",
        "S02:15": "s23-neverred",
        "S02:16": "s23-census",
        "S02:17": "s23-ceiling",
        "S03:02": "s22-carry-divides",
        "S03:03": "s23-chain-frac",
        "S03:04": "s23-chain-mod",
        "S03:05": "s23-chain-frac",
        "S03:06": "s23-chain-mod",
        "S03:07": "s23-chain-frac",
        "S03:08": "s23-chain-mod",
        "S03:09": "s23-chain-frac",
        "S03:10": "s23-chain-mod",
        "S03:11": "s23-chain-frac",
        "S03:12": "s23-ceiling",
        "S03:13": "s23-census",
        "S03:16": "s23-filing",
        "S03:17": "s23-w1",
        "S04:02": "s22-carry-question",
        "S04:03": "s22-w1",
        "S04:04": "s23-w1",
        "S04:05": "s23-w2",
        "S04:06": "s23-w3",
        "S04:07": "s23-census",
        "S04:08": "s23-ceiling",
        "S04:13": "s23-chain-frac",
        "S04:14": "s23-chain-mod",
        "S04:15": "s23-coprime",
        "S04:16": "s22-carry-telescope",
        "S04:17": "s20-marker",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    # the carried S11 state surfaces (the first-divisor rule, read
    # back at the S23 coordinates)
    state_modes = {
        "S02:01": "s11-state",
        "S02:06": "s23-state",
        "S02:08": "s23-state",
        "S02:10": "s23-state",
        "S02:12": "s23-state",
        "S03:01": "s11-state",
        "S04:01": "s11-state",
        "S04:09": "s23-state",
        "S04:10": "s23-state",
        "S04:11": "s23-state",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    state_slugs = {
        "S02:01": "spf-def",
        "S03:01": "spf-def",
        "S04:01": "spf-def",
        "S02:06": "coprime-pair-def",
        "S02:08": "coprime-pair-def",
        "S02:10": "prime-fingerprint-def",
        "S02:12": "prime-fingerprint-def",
        "S04:09": "coprime-pair-def",
        "S04:10": "prime-fingerprint-def",
        "S04:11": "fingerprint-filed",
    }
    for ref, slug in state_slugs.items():
        _kind, slots = det_classify(_surface(ref))
        assert slots.get("slug") == slug, f"{ref}: {slots} != {slug}"
    derive_turns = {"S03:14": "derive", "S03:15": "derive"}
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
        assert slots.get("target") == "fingerprint-filed", ref
    assertion_turns = ["S02:07", "S02:11"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the proportion, end to end, as my store holds it?")[1]["mode"] == "s22-prop"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set (the mechanism grounded the band's own filing
    # under the FILING probe and the STATE echo rows that ground
    # it; the proportion-filing carry cites the S22 theorem; the
    # telescope carry cites the S13 theorem — the frozen set is
    # the mechanism's, never the hand's)
    assert FROZEN["theorem_allowed"] == {
        "S02:04": ["proportion-filed"],
        "S03:16": ["fingerprint-filed"],
        "S04:11": ["fingerprint-filed"],
        "S04:12": ["fingerprint-filed"],
        "S04:16": ["telescope-line"],
    }
    # the full sanctioned DAG: forty-four theorem facts (the S22
    # forty-three + fingerprint-filed); NO bare island candidate id
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 44
    assert "theorem:fingerprint-filed" in dag
    assert "theorem:proportion-filed" in dag  # the S22 filing stays in the DAG
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
    assert SCRIPT_HASH == "c6c662b4dc24ec6d"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:17": [
            "eighty-three by the seventy-nine is the last prime pair on my line",
            "the eighty-nine my line already declared off-line",
            "at the line end 84",
        ],
        "S04:03": [
            "zero to zero is the evenness of the two empty parts",
            "the part you count with is zero parts",
            "the value and the relation are two jobs",
            "at the line end 84",
        ],
        "S04:04": [
            "eighty-three by the seventy-nine is the last prime pair on my line",
            "the eighty-nine my line already declared off-line",
            "at the line end 84",
        ],
        "S04:05": [
            "a proportion of two distinct primes never reduces",
            "a proportion that reduces is not a proportion of two distinct primes",
            "at the line end 84",
        ],
        "S04:06": [
            "two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced proportions",
            "a second pair claiming the first pair's proportion is a misread",
            "at the line end 84",
        ],
    }


def test_band_map_domain_carried() -> None:
    # the prime proportion lives in the carried ARITHMETIC domain:
    # no NEW domain enters the registry
    carried_domains = {c.domain for c in CONCEPTS_E626}
    assert "arithmetic" in carried_domains, "arithmetic is already in the S22 registry"
    assert {c.domain for c in CONCEPT_S23} == {"arithmetic"}, "no NEW domain enters the S23 registry"
    assert {c.domain for c in CONCEPT_S23} <= carried_domains, "the S23 domains are carried, not new"
    assert len(CONCEPTS_E627) == 130  # the S22 128 + the two prime-proportion concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (2074 final: 51 turns,
    # 5 inert gap turns, 50 mechanism-counted events — the
    # control's own census, never the hand's, D-e6u(a))
    assert FROZEN["domain_sequence"] == {
        2: "SSSSUULSUULSSSSSS",
        3: "SSSSSSSSSSSSSFTSH",
        4: "SSHHHHSSSSSSSSSSS",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"


def test_discovery_candidate_invariant_full_width() -> None:
    """The D8 gate at FULL width (the prime proportion must not
    settle an island): no bare island theorem id may exist in the
    seed store — the four candidates stay open of record (the
    store speaks, not the hand)."""
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
