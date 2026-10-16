from __future__ import annotations

import hashlib
import json
import re as _re
from pathlib import Path

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S31,
    S31_LESSONS,
    S31_THEOREMS,
    Brainstem,
    det_classify,
)
from kainos.tutor.e625 import CONCEPTS_E625
from kainos.tutor.e635 import CONCEPTS_E635, FROZEN, SCRIPT_HASH
from kainos.tutor.mastery import reset_concepts
from kainos.tutor.session import InfantRuntime, load_store

MARKER = "under the condition of the Riemann hypothesis"
MARKER_VARIANT = "under the condition that"

S31_LESSION_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S31_LESSONS.items()]


def test_new_concepts_prereqs_point_down() -> None:
    """S31 adds the two seeded-line concepts; their prereqs point DOWN
    into the carried line (the S14 soil: add-two-digit and
    mult-within-100; the S4 count-successor and the band's own
    seeded line)."""
    carried = tuple(c.id for c in CONCEPTS_E625)
    assert tuple(c.id for c in CONCEPTS_E635) == carried + tuple(c.id for c in CONCEPT_S31)
    existing = set(carried)
    for c in CONCEPT_S31:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S31}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id for c in CONCEPT_S31}
    assert by_id == {"seeded-line", "golden-seed"}
    for c in CONCEPT_S31:
        assert c.band == "college-1"
        assert c.domain == "arithmetic"
    by_id_map = {c.id: c for c in CONCEPT_S31}
    assert by_id_map["seeded-line"].prereqs == ("add-two-digit", "mult-within-100")
    assert by_id_map["golden-seed"].prereqs == ("seeded-line", "count-successor")


def test_script_shape_and_teaching() -> None:
    """51 turns; the two teaches are the lesson phrases verbatim; the
    two pre-lesson gap pairs run immediately before their teaches; the
    sanctioned derive names the strict part set (the scaffold first
    names only the seeded-line part)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S31_LESSION_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S31_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    assert S31_THEOREMS["seeded-line-filed"]["statement"] not in script_lines
    # the S02 rhythm: the queue carried first, then each concept's two
    # concept/rule gaps run immediately before its teach
    assert FROZEN["script"][2][0] == "what is the queue above my line?"
    assert FROZEN["script"][2][2] == "what is my seeded line, end to end, as my store holds it?"
    assert FROZEN["script"][2][3] == "state the seeded-line-def rule"
    assert (
        FROZEN["script"][2][4]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S31_LESSONS.items() if s == "seeded-line-def")
    )
    assert FROZEN["script"][2][7] == "what is the golden seed line, end to end, as my store holds it?"
    assert FROZEN["script"][2][8] == "state the golden-seed-def rule"
    assert (
        FROZEN["script"][2][9]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S31_LESSONS.items() if s == "golden-seed-def")
    )
    # the one sanctioned composition: scaffold (short the golden part),
    # then the derive on the exact set
    assert "derive seeded-line-filed from seeded-line-def" in script_lines
    assert "derive seeded-line-filed from seeded-line-def and golden-seed-def" in script_lines
    # the carried queue surfaces stand in the script
    assert "what is the queue above my line?" in script_lines
    assert "the queue above my line, first lot, which?" in script_lines


def test_frozen_shape() -> None:
    """The control census (the mechanism spoke, never the hand):
    1871 + 3 new facts + 47 new events = 1921; the S31 band writes
    NO successor facts (the line end stays 84)."""
    assert FROZEN["seed_total"] == 1871
    assert FROZEN["seed_identity"] == "77e07edf42292f88"
    assert FROZEN["line_end_final"] == 84  # S31 writes NO successor facts
    assert FROZEN["new_facts"] == 3
    assert FROZEN["new_fact_ids"] == [
        "lemma:seeded-line-def",
        "lemma:golden-seed-def",
        "theorem:seeded-line-filed",
    ]
    assert FROZEN["total_seam_facts"] == 149  # 107 lemma + 41 theorem (S21 146 + the THREE)
    assert len(FROZEN["theorem_dag"]) == 41  # S6..S31
    assert len(FROZEN["walls_honest"]) == 5  # the three declared territories, re-probed on S04
    assert len(FROZEN["beds_exact"]) == 32
    assert len(FROZEN["derived_table"]) == 33  # the 32 beds + the sanctioned derive
    assert len(FROZEN["pre_teach_gaps"]) == 4  # a concept gap + a rule gap per concept
    assert FROZEN["teach_turns"] == {
        "S02:05": "lemma:seeded-line-def",
        "S02:10": "lemma:golden-seed-def",
    }
    assert len(FROZEN["scaffold_failures"]) == 1
    assert FROZEN["missing_parts_failure"] == {}
    assert FROZEN["rederive"] is None
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S03:01", "S03:02", "S04:01", "S04:02",
    ]
    assert FROZEN["final_total"] == 1921  # 1871 + 3 facts + 47 events
    assert FROZEN["new_events"] == 47
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "SSUULSSUULSSSSSSS"
    assert FROZEN["domain_sequence"][3] == "SSSSSSSSFTSSSHHSS"
    assert FROZEN["domain_sequence"][4] == "SSSSSSSSSSSSHHHSS"
    # the off-script standing check: the first lot of the queue
    assert list(FROZEN["offscript_carry"]) == ["the queue above my line, first lot, which?"]


def test_pre_s31_states_carry_e625_final() -> None:
    """The 122 carried concepts at their S21-final values (the live
    control census, excluding the two new concepts)."""
    pre = FROZEN["pre_s31_states"]
    assert len(pre) == 122
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S31}, "a NEW concept leaked into the pre-states"
    # the S20/S21 soil carried unchanged-or-improved
    assert pre["weave"] == {"state": "stable", "correct": 8}
    assert pre["summit-shape"] == {"state": "practicing", "correct": 8}
    assert pre["shadow-form"] == {"state": "stable", "correct": 9}
    assert pre["boundary-form"] == {"state": "stable", "correct": 5}
    # the RH line carried through the condition band
    assert pre["riemann"] == {"state": "practicing", "correct": 17}
    assert pre["rh-scale"]["state"] == "practicing"
    assert pre["rh-relevance"]["state"] == "practicing"
    assert pre["factor-route"]["state"] == "practicing"
    assert pre["conditional"] == {"state": "practicing", "correct": 2}
    # the island summits the queue declared
    assert pre["beal-summit"] == {"state": "stable", "correct": 7}
    assert pre["bsd-summit"] == {"state": "stable", "correct": 13}
    assert pre["pnp-summit"] == {"state": "stable", "correct": 7}
    assert pre["class-p"] == {"state": "stable", "correct": 4}
    assert pre["class-np"] == {"state": "stable", "correct": 5}
    # the S14 soil the seeded line stands on: ALL STABLE
    assert pre["add-two-digit"] == {"state": "stable", "correct": 11}
    assert pre["mult-within-100"] == {"state": "stable", "correct": 9}
    assert pre["count-successor"] == {"state": "stable", "correct": 14}
    # the S31 drill at the carried coordinates (control #1)
    assert FROZEN["pre_s31_drilled"] == {
        "rh-relevance": 2,
        "shadow-form": 2,
    }
    # the two NEW concepts at their frozen band-end values: both
    # STABLE with EMPTY prereq-gap lists (their soil is closed)
    assert FROZEN["mastery_expected"] == {
        "golden-seed": {"correct": 15, "state": "stable"},
        "seeded-line": {"correct": 14, "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "golden-seed": [],
        "seeded-line": [],
    }


def test_unconditional_band_marker_census() -> None:
    """The D-e6q mirror inverts the S21 posture: this is the
    UNCONDITIONAL band. Every one of the three new facts carries NO
    condition marker; the census conserves at seed AND final
    (six exact + one variant — the four S12 marker facts keep
    theirs, the variant is conditional-def's own form,
    byte-identical across the band)."""
    for phrase in S31_LESSONS:
        assert MARKER not in phrase, "an S31 lesson carries the condition marker"
        assert MARKER_VARIANT not in phrase
    filed = S31_THEOREMS["seeded-line-filed"]["statement"]
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
    fin = load_store(Path(FROZEN["seed"].replace("e6.25-run1", "e6.35-run1")))
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
    assert FROZEN["seed"].startswith("results/phase-6/e6.25-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S31_THEOREMS) == {"seeded-line-filed"}
    assert S31_THEOREMS["seeded-line-filed"]["parts"] == (
        "seeded-line-def",
        "golden-seed-def",
    )
    assert S31_THEOREMS["seeded-line-filed"]["concept"] == "golden-seed"
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:10": [
            "seeded-line-filed",
            [
                "lemma:seeded-line-def",
                "lemma:golden-seed-def",
            ],
        ],
    }
    # the honest-turn bytes: the scaffold names only the seeded-line
    # part (short the golden-seed-def), before the sanctioned derive
    # puts the rule together on the exact set
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the golden-seed-def before i can put it together" in FROZEN["scaffold_failures"]["S03:09"]


def test_walls_bytes() -> None:
    # the three declared territories: W_S31_1 (the off-line
    # constants) probed at S03:14 and re-probed at S04:13,
    # W_S31_2 (the seed law) at S03:15 and S04:14, and
    # W_S31_3 (the ratio limit) at S04:15
    wall_attrs = {
        "S03:14": Brainstem.W_S31_1,
        "S03:15": Brainstem.W_S31_2,
        "S04:13": Brainstem.W_S31_1,
        "S04:14": Brainstem.W_S31_2,
        "S04:15": Brainstem.W_S31_3,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the no-new-decimals rule: the walls name positions and the
    # equation, never a digit string of record
    for _wall in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry an off-line digit string"
    assert "pi stands off the line between the three and the four" in Brainstem.W_S31_1
    assert "declared, not filed" in Brainstem.W_S31_1
    assert "not a seeded line, it is the line's own shadow" in Brainstem.W_S31_2
    assert "no landing value is filed" in Brainstem.W_S31_3
    # the walls carry the position claims, spelled (three and the
    # four, two and the three, one and the two)
    assert "named by position and by the equation x squared equals x plus one" in Brainstem.W_S31_1
    # no honest-zero bytes (the S31 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The on-line bed rows re-derive from the STORE'S OWN WALKS
    (re-walked here independently of the brainstem's — the
    store-speaks rule)."""
    store = load_store(Path(FROZEN["seed"]))
    # (a) the line-end marker census on the SEED's theorem facts:
    # 14 line end / 2 spot / 24 universal of 40 — the S02:16 and
    # S03:08 pre-census beds stand on this
    e_n = s_n = n_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        assert isinstance(a.object, str)
        if "line end" in a.object:
            e_n += 1
        elif "at s = 2" in a.object:
            s_n += 1
        else:
            n_n += 1
    assert (e_n, s_n, n_n) == (14, 2, 24)
    for ref in ("S02:16", "S03:08"):
        assert "fourteen of my forty" in FROZEN["beds_exact"][ref], ref
        assert "two close on the line's spot marker" in FROZEN["beds_exact"][ref]
        assert "twenty-four carry the universal form with no line end marker" in FROZEN["beds_exact"][ref]
    # (b) the census re-walked AFTER the band's own filing: 41
    # theorem facts, fifteen closing at the line end (the new filing
    # is the fifteenth line-end marker)
    for ref in ("S03:13", "S04:03"):
        assert "fifteen of my forty-one theorem facts close their scope at the line end" in FROZEN["beds_exact"][ref], ref
        assert "a form of the line is not a census of its end" in FROZEN["beds_exact"][ref]
    # (c) the STATE beds: the new facts' state readouts are the
    # lesson phrases and the filing statement VERBATIM (the
    # house-voice rule), re-anchored here against the brainstem
    # constants, not against FROZEN
    sl = next(p for p, (_c, s, _k, _es, _d, _l) in S31_LESSONS.items() if s == "seeded-line-def")
    gs = next(p for p, (_c, s, _k, _es, _d, _l) in S31_LESSONS.items() if s == "golden-seed-def")
    filed = S31_THEOREMS["seeded-line-filed"]["statement"]
    assert FROZEN["beds_exact"]["S02:06"] == sl
    assert FROZEN["beds_exact"]["S04:05"] == sl
    assert FROZEN["beds_exact"]["S02:11"] == gs
    assert FROZEN["beds_exact"]["S04:06"] == gs
    assert FROZEN["beds_exact"]["S03:12"] == filed
    assert FROZEN["beds_exact"]["S04:07"] == filed
    # (d) the FILING beds: the filing files the line, not the
    # constants — the constants stay off the floor
    for ref in ("S03:11", "S04:04", "S04:17"):
        v = FROZEN["beds_exact"][ref]
        assert v.startswith("the line, not the constants"), ref
        assert "never by a digit" in v, ref
        assert v.endswith("at the line end 84"), ref
    # the beds carry NO off-line digit strings of record
    for v in FROZEN["beds_exact"].values():
        assert not _re.search(r"\d{10,}", v)


def test_lesson_phrases_are_house_voiced() -> None:
    """S31 is the seeded line: the constants stay off the floor,
    named by position and by the equation, never by a digit. The
    S31 lessons are house-voiced on the line — and the theorem
    statement closes at the spelled line end."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S31_LESSONS.items()}
    # the seeded line: the sum law + the skeleton reading + the shifts
    assert "seed one and c under the sum rule" in by_slug["seeded-line-def"]
    assert "no other seed standing on my line a shift" in by_slug["seeded-line-def"]
    assert "at the line end eighty-four" in by_slug["seeded-line-def"]
    # the golden seed: off the line, named by the equation, never by a
    # digit; its line its own power
    assert "stands off the line between the one and the two" in by_slug["golden-seed-def"]
    assert "x squared equals x plus one" in by_slug["golden-seed-def"]
    assert "never by a digit" in by_slug["golden-seed-def"]
    assert "at the line end eighty-four" in by_slug["golden-seed-def"]
    # the file: the line, not the constants, at the spelled line end
    comp = S31_THEOREMS["seeded-line-filed"]["statement"]
    assert "filed of record" in comp
    assert "named by position and by the equation, never by a digit" in comp
    assert "at the line end eighty-four" in comp
    # NO island candidate is settled: the statements stay open of
    # record in the band material — never a settled claim
    for text in list(S31_LESSONS) + [comp]:
        assert "p equals np is a theorem" not in text
        assert "the riemann hypothesis is true" not in text
        assert "beal's conjecture is true" not in text
        assert "pi equals" not in text


def test_offline_values_never_store_answers() -> None:
    """S31 brings NO new off-line value: expect.offline_watch is
    empty, and no off-line digit string floats into an on-line
    answer, a bed, or a wall (the seeded line names only values the
    line's record already holds)."""
    with open("bands/spec-e6.35.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"an off-line digit string floated into an on-line answer: {str(v)[:60]!r}"
    for v in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", v), "an off-line digit string must not live in an S31 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the six carry rows (P6: byte-identical to the seed store):
    # the queue and its first lot, each session's opening pair
    assert FROZEN["seam_carry_refs"] == [
        "S02:01", "S02:02", "S03:01", "S03:02", "S04:01", "S04:02",
    ]
    # the off-script standing check: the first lot of the queue,
    # byte-identical to the store's own declared record (the
    # seeded line is the course of the queue, the lot stays declared)
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
        rt = InfantRuntime(root, concepts=CONCEPTS_E635)
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
    # sixteen new S31 drill surfaces classify into the thirteen S31
    # modes; the carried queue surfaces keep their S12 modes
    plain = {
        "S02:01": "s12-queue",
        "S02:02": "s12-queue-lot",
        "S02:03": "s31-seeded",
        "S02:07": "s31-seeded",
        "S02:08": "s31-golden",
        "S02:12": "s31-golden",
        "S02:13": "s31-sumline",
        "S02:14": "s31-shift",
        "S02:15": "s31-cassini",
        "S02:16": "s20-marker",
        "S02:17": "s31-seeded",
        "S03:01": "s12-queue",
        "S03:02": "s12-queue-lot",
        "S03:03": "s31-ratio",
        "S03:04": "s31-goldenwalk",
        "S03:05": "s31-silence",
        "S03:06": "s31-shift",
        "S03:07": "s31-cassini",
        "S03:08": "s20-marker",
        "S03:11": "s31-filing",
        "S03:13": "s20-marker",
        "S03:14": "s31-w1",
        "S03:15": "s31-w2",
        "S03:16": "s31-seeded",
        "S03:17": "s31-golden",
        "S04:01": "s12-queue",
        "S04:02": "s12-queue-lot",
        "S04:03": "s20-marker",
        "S04:04": "s31-filing",
        "S04:08": "s31-seeded",
        "S04:09": "s31-golden",
        "S04:10": "s31-sumline",
        "S04:11": "s31-shift",
        "S04:12": "s31-cassini",
        "S04:13": "s31-w1",
        "S04:14": "s31-w2",
        "S04:15": "s31-w3",
        "S04:16": "s31-golden",
        "S04:17": "s31-filing",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:04": "s31-state",
        "S02:06": "s31-state",
        "S02:09": "s31-state",
        "S02:11": "s31-state",
        "S03:12": "s31-state",
        "S04:05": "s31-state",
        "S04:06": "s31-state",
        "S04:07": "s31-state",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
    state_slugs = {
        "S02:04": "seeded-line-def",
        "S02:06": "seeded-line-def",
        "S02:09": "golden-seed-def",
        "S02:11": "golden-seed-def",
        "S03:12": "seeded-line-filed",
        "S04:05": "seeded-line-def",
        "S04:06": "golden-seed-def",
        "S04:07": "seeded-line-filed",
    }
    for ref, slug in state_slugs.items():
        _kind, slots = det_classify(_surface(ref))
        assert slots.get("slug") == slug, f"{ref}: {slots} != {slug}"
    derive_turns = {"S03:09": "derive", "S03:10": "derive"}
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
        assert slots.get("target") == "seeded-line-filed", ref
    assertion_turns = ["S02:05", "S02:10"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("the queue above my line, first lot, which?")[1]["lot"] == "first"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set (D-e6q(c): the mechanism grounded the band's own
    # filing under both STATE echo rows and the FILING probes — the
    # frozen set is the mechanism's, never the hand's): the queue
    # carries cite the declared queue theorem, and seeded-line-filed
    # is cited by the state readouts and the filing probes
    assert FROZEN["theorem_allowed"] == {
        "S02:01": ["queue-declared"],
        "S02:02": ["queue-declared"],
        "S03:01": ["queue-declared"],
        "S03:02": ["queue-declared"],
        "S03:11": ["seeded-line-filed"],
        "S03:12": ["seeded-line-filed"],
        "S04:01": ["queue-declared"],
        "S04:02": ["queue-declared"],
        "S04:04": ["seeded-line-filed"],
        "S04:07": ["seeded-line-filed"],
        "S04:17": ["seeded-line-filed"],
    }
    # the full sanctioned DAG: forty-one theorem facts (the S21
    # forty + seeded-line-filed); NO bare island candidate id
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 41
    assert "theorem:seeded-line-filed" in dag
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
    assert SCRIPT_HASH == "22c2b8552be72285"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:14": [
            "pi stands off the line between the three and the four",
            "named by position and by the equation",
            "at the line end 84",
            "declared, not filed",
        ],
        "S03:15": [
            "only at seed one and c under the sum law",
            "not a seeded line",
            "at the line end 84",
        ],
        "S04:13": [
            "pi stands off the line between the three and the four",
            "named by position and by the equation",
            "at the line end 84",
            "declared, not filed",
        ],
        "S04:14": [
            "only at seed one and c under the sum law",
            "not a seeded line",
            "at the line end 84",
        ],
        "S04:15": [
            "no landing value is filed",
            "named by the equation alone",
            "at the line end 84",
        ],
    }


def test_band_map_domain_carried() -> None:
    # the seeded line lives in the carried ARITHMETIC domain (the
    # S14/S5 sum-line territory - D-e6q(d): the splice once wrote a fresh
    # 'soil' domain; the registry carries arithmetic): no NEW domain
    # enters the registry
    carried_domains = {c.domain for c in CONCEPTS_E625}
    assert "arithmetic" in carried_domains, "arithmetic is already in the S21 registry"
    assert {c.domain for c in CONCEPT_S31} == {"arithmetic"}, "no NEW domain enters the S31 registry"
    assert {c.domain for c in CONCEPT_S31} <= carried_domains, "the S31 domains are carried, not new"
    assert len(CONCEPTS_E635) == 124  # the S21 122 + the two seeded-line concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (1921 final: the teach
    # turns store facts, not events — 51 turns, 4 inert gap turns,
    # 47 mechanism-counted events, drift -4, D-e6q(b))
    assert FROZEN["domain_sequence"] == {
        2: "SSUULSSUULSSSSSSS",
        3: "SSSSSSSSFTSSSHHSS",
        4: "SSSSSSSSSSSSHHHSS",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"


def test_discovery_candidate_invariant_full_width() -> None:
    """The D8 gate at FULL width (the seeded line must not settle an
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
