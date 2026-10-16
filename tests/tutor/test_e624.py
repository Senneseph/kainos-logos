from __future__ import annotations

import hashlib
import json
import re as _re
from pathlib import Path

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S20,
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
    Brainstem,
    det_classify,
)
from kainos.tutor.e623 import CONCEPTS_E623
from kainos.tutor.e624 import CONCEPTS_E624, FROZEN, SCRIPT_HASH
from kainos.tutor.session import load_store

S20_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S20_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS)
    + list(S13_LESSONS) + list(S14_LESSONS) + list(S15_LESSONS)
    + list(S16_LESSONS) + list(S17_LESSONS) + list(S18_LESSONS) + list(S19_LESSONS)
)


def test_new_concepts_prereqs_point_down() -> None:
    """S20 adds the four weaving concepts; prereqs point DOWN into the
    carried islands (the beal soil: divides / the scan-ledger; the
    summit concepts: riemann / bsd-summit / beal-summit / pnp-summit;
    the forms: curve-shadow / lte-form / size-shadow / class-np and
    beal-census / tamable-machine / pnp-summit)."""
    carried = tuple(c.id for c in CONCEPTS_E623)
    assert tuple(c.id for c in CONCEPTS_E624) == carried + tuple(c.id for c in CONCEPT_S20)
    existing = set(carried)
    for c in CONCEPT_S20:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S20}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id: c for c in CONCEPT_S20}
    assert by_id["weave"].prereqs == ("divides", "first-divisor", "scan-ledger", "beal-census", "reduction")
    assert by_id["summit-shape"].prereqs == ("riemann", "bsd-summit", "beal-summit", "pnp-summit")
    assert by_id["shadow-form"].prereqs == ("curve-shadow", "lte-form", "size-shadow", "class-np")
    assert by_id["boundary-form"].prereqs == ("beal-census", "tamable-machine", "pnp-summit")
    for c in CONCEPT_S20:
        assert c.band == "college-1"
        assert c.domain == "weave"


def test_script_shape_and_teaching() -> None:
    """51 turns; the four teaches are the lesson phrases verbatim; no
    carried S4–S19 seam statement appears in the script (Stage-A)."""
    assert FROZEN["total_turns"] == 51
    assert len(FROZEN["script"][2]) == 17
    assert len(FROZEN["script"][3]) == 17
    assert len(FROZEN["script"][4]) == 17
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S20_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S20_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for mod in (
        S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS, S10_THEOREMS,
        S11_THEOREMS, S12_THEOREMS, S13_THEOREMS, S14_THEOREMS, S15_THEOREMS,
        S16_THEOREMS, S17_THEOREMS, S18_THEOREMS, S19_THEOREMS,
    ):
        for m in mod.values():
            assert m["statement"] not in script_lines
    # the S02 rhythm: the four island summits carried first, then a
    # concept's two gaps run immediately before its teach
    assert FROZEN["script"][2][4] == "what soil do my islands share, as my prereq graph of record holds it?"
    assert FROZEN["script"][2][5] == "state the weave-def rule"
    assert (
        FROZEN["script"][2][6]
        == next(p for p, (_c, s, _k, _es, _d, _l) in S20_LESSONS.items() if s == "weave-def")
    )
    assert FROZEN["script"][3][0] == "what holds once for the four island summits, as my store walks it?"
    # the one sanctioned composition, derived in-band on the strict
    # part set (the scaffold first names only the soil + shape parts)
    assert (
        "derive summit-shape-filed from weave-def, summit-shape-def, shadow-form-def and boundary-form-def"
        in script_lines
    )
    assert "derive summit-shape-filed from weave-def and summit-shape-def" in script_lines
    # the four island summit surfaces carried from their bands
    assert "what is the statement of the riemann island of record?" in script_lines
    assert "what is the summit fact of the island?" in script_lines
    assert "what is the statement of the beal island of record?" in script_lines
    assert "what is the statement of the pnp island of record?" in script_lines


def test_frozen_shape() -> None:
    """The control #1 census (the mechanism spoke, never the hand —
    D-e6o(a): the final total is 1823, one below the pre-registration
    of 1824; the S04:07 queue-carry event dedupes against the S19
    seed's S04:07 event id, writing zero net new assertions)."""
    assert FROZEN["seed_total"] == 1756
    assert FROZEN["seed_identity"] == "627f6165fc5f3507"
    assert FROZEN["line_end_final"] == 84  # S20 writes NO successor facts
    assert FROZEN["new_facts"] == 5
    assert FROZEN["new_fact_ids"] == [
        "lemma:weave-def",
        "lemma:shadow-form-def",
        "lemma:boundary-form-def",
        "lemma:summit-shape-def",
        "theorem:summit-shape-filed",
    ]
    assert FROZEN["total_seam_facts"] == 143  # 104 lemma + 39 theorem (S19 138 + the FIVE)
    assert len(FROZEN["theorem_dag"]) == 39  # S6..S20
    assert len(FROZEN["walls_honest"]) == 5
    assert len(FROZEN["beds_exact"]) == 10
    assert len(FROZEN["derived_table"]) == 29  # the non-carry, non-wall derived rows (beds included)
    assert len(FROZEN["pre_teach_gaps"]) == 8  # the eight pre-lesson gaps
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 1
    assert len(FROZEN["missing_parts_failure"]) == 0
    assert FROZEN["rederive"] is None
    assert FROZEN["seam_carry_refs"] == ["S02:02", "S02:03", "S04:07", "S04:17"]
    assert FROZEN["final_total"] == 1823  # 1756 + 5 facts + 62 events (D-e6o(a))
    assert FROZEN["new_events"] == 62
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1)
    assert FROZEN["domain_sequence"][2] == "SSSSUULSSUULSSUUL"
    assert FROZEN["domain_sequence"][3] == "UULSSSSFTSHHHHSSS"
    assert FROZEN["domain_sequence"][4] == "SSSSSSSSSSSSSHSSS"
    # the off-script standing check: the queue (the weaving adds no
    # lot to the declared queue)
    assert list(FROZEN["offscript_carry"]) == ["what is the queue above my line?"]


def test_pre_s20_states_carry_e623_final() -> None:
    """The 116 carried concepts at their S19-final values (the live
    control census, excluding the four new concepts)."""
    pre = FROZEN["pre_s20_states"]
    assert len(pre) == 116
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S20}, "a NEW concept leaked into the pre-states"
    # the S19 soil the weaving line stands on (the S19-final values)
    assert pre["class-p"] == {"state": "stable", "correct": 4}
    assert pre["class-np"] == {"state": "stable", "correct": 5}
    assert pre["pnp-summit"] == {"state": "stable", "correct": 6}
    assert pre["size-shadow"] == {"state": "stable", "correct": 11}
    # the S11/S18 soil the weave walks
    assert pre["divides"] == {"state": "stable", "correct": 5}
    assert pre["first-divisor"] == {"state": "stable", "correct": 36}
    assert pre["scan-ledger"] == {"state": "stable", "correct": 12}
    assert pre["decision-question"] == {"state": "stable", "correct": 7}
    assert pre["reduction"] == {"state": "stable", "correct": 10}
    assert pre["cost-counter"] == {"state": "stable", "correct": 10}
    # the island summits the shape stands on
    assert pre["beal-summit"] == {"state": "stable", "correct": 6}
    assert pre["beal-census"] == {"state": "stable", "correct": 11}
    assert pre["bsd-summit"] == {"state": "stable", "correct": 12}
    assert pre["riemann"] == {"state": "practicing", "correct": 13}  # the shape's declared gap
    assert pre["rh-relevance"]["state"] == "practicing"
    # the form soils
    assert pre["curve-shadow"] == {"state": "stable", "correct": 12}
    assert pre["lte-form"] == {"state": "stable", "correct": 7}
    assert pre["tamable-machine"] == {"state": "stable", "correct": 4}
    # the S20 drill at the NEW carry coordinates (control #1: the
    # four island summit carries + the Beal census carry; the queue
    # carry's event dedupes against the S19 seed's S04:07 event id and
    # drills nothing new)
    assert FROZEN["pre_s20_drilled"] == {
        "beal-census": 1,
        "beal-summit": 1,
        "bsd-summit": 1,
        "pnp-summit": 1,
        "riemann": 1,
    }
    # the four NEW concepts at their frozen band-end values: three
    # stable, and the summit-shape practicing with its declared gap
    # [riemann] (the shape holds while its riemann instance waits on
    # the condition chain — the gap is named, not hidden)
    assert FROZEN["mastery_expected"] == {
        "weave": {"correct": 8, "state": "stable"},
        "summit-shape": {"correct": 8, "state": "practicing"},
        "shadow-form": {"correct": 6, "state": "stable"},
        "boundary-form": {"correct": 5, "state": "stable"},
    }
    assert FROZEN["expected_prereq_gaps"] == {
        "weave": [],
        "summit-shape": ["riemann"],
        "shadow-form": [],
        "boundary-form": [],
    }


def test_denylist_is_the_s9_44() -> None:
    # S20 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44


def test_unconditional_marker_absent() -> None:
    """The S20 facts are the unconditional weaving band: none carries
    the RH marker (the island questions stand open of record, never as
    premises); the seed is the official S19 store (e6.23 run 1)."""
    marker = "under the condition of the Riemann hypothesis"
    for th in S20_THEOREMS.values():
        assert marker not in th["statement"]
    for phrase in S20_LESSONS:
        assert marker not in phrase
    assert FROZEN["seed"].startswith("results/phase-6/e6.23-run1/") and FROZEN["seed"].endswith("codeX-S04.json")


def test_compositions_sanctioned() -> None:
    assert set(S20_THEOREMS) == {"summit-shape-filed"}
    assert S20_THEOREMS["summit-shape-filed"]["parts"] == (
        "weave-def",
        "summit-shape-def",
        "shadow-form-def",
        "boundary-form-def",
    )
    # the frozen derive turn carries the SAME sanctioned part set
    assert FROZEN["derive_successes"] == {
        "S03:09": [
            "summit-shape-filed",
            [
                "lemma:weave-def",
                "lemma:summit-shape-def",
                "lemma:shadow-form-def",
                "lemma:boundary-form-def",
            ],
        ],
    }
    # the honest-turn bytes: the scaffold names the two short parts
    # (the shadow-form-def AND the boundary-form-def), before the
    # sanctioned derive puts the rule together on the exact set
    assert FROZEN["missing_parts_failure"] == {}
    assert "short the shadow-form-def and the boundary-form-def" in FROZEN["scaffold_failures"]["S03:08"]


def test_walls_bytes() -> None:
    # the four declared territories (five honest rows: W-S20-1 is
    # re-probed at S04:14): S03:11 W-S20-1 (the filed shape),
    # S03:12 W-S20-2 (the declared queue), S03:13 W-S20-3 (the
    # register of the line), S03:14 W-S20-4 (the voice of the store)
    wall_attrs = {
        "S03:11": Brainstem.W_S20_1,
        "S03:12": Brainstem.W_S20_2,
        "S03:13": Brainstem.W_S20_3,
        "S03:14": Brainstem.W_S20_4,
        "S04:14": Brainstem.W_S20_1,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for ref, _wall in FROZEN["walls_honest"].items():
        assert "line end 84" in _wall, f"{ref}: every wall names the line end"
    # the no-new-decimals rule: the weaving names only values the
    # line's record already holds — no off-line digit string anywhere
    for _wall in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", _wall), "a wall must not carry an off-line digit string"
    assert "summit-shape filing fills the shape, not the statements" in Brainstem.W_S20_1
    assert "fifth lot is not in the queue" in Brainstem.W_S20_2
    assert "register of my weaving line is the line itself" in Brainstem.W_S20_3
    assert "the store speaks, not the hand" in Brainstem.W_S20_4
    # no honest-zero bytes (the S20 band has no zero-touch probes)
    assert FROZEN["honest_zero_bytes"] == {}


def test_beds_match_the_python_reference() -> None:
    """The ten on-line bed rows re-derive from the STORE'S OWN WALKS
    (re-walked here independently of the brainstem's — the
    D-e6n(b) rule: the store speaks, not the hand)."""
    store = load_store(Path(FROZEN["seed"]))
    # (a) the SOIL: the beal chain and the difficulty chain share
    # exactly {divides, scan-ledger}
    pre = {}
    for a in store.query(context_match={"kind": "prereq"}):
        pre.setdefault(a.context.data.get("concept"), set()).add(a.object_id)
    beal = pre["beal-census"] | pre["beal-summit"] | pre["valuation"]
    diff = pre["decision-question"] | pre["reduction"] | pre["cost-counter"]
    assert beal & diff == {"divides", "scan-ledger"}
    # (b) the NODE: the one walk under all three ledgers
    assert pre["beal-census"] & pre["reduction"] & pre["cost-counter"] == {"scan-ledger"}
    # (c) the MARKER CENSUS: the seed's 38 theorem facts at 12/2/24;
    # the band's own filing is the thirteenth line-end marker
    e_n = s_n = n_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        assert isinstance(a.object, str)
        if "line end" in a.object:
            e_n += 1
        elif "at s = 2" in a.object:
            s_n += 1
        else:
            n_n += 1
    assert (e_n, s_n, n_n) == (12, 2, 24)
    assert "line end eighty-four" in S20_THEOREMS["summit-shape-filed"]["statement"]
    # the beds carry the re-derived bytes
    assert "my islands share the soil of my line itself" in FROZEN["beds_exact"]["S02:08"]
    assert "divides question roots both" in FROZEN["beds_exact"]["S02:08"]
    assert "the scan-ledger walk stands under the beal census, the reduction, and the cost counter" in FROZEN["beds_exact"]["S02:08"]
    assert "the scan-ledger walk of record" in FROZEN["beds_exact"]["S02:09"]
    assert "the one walk that stands under the beal census" in FROZEN["beds_exact"]["S02:09"]
    assert "one shape of record" in FROZEN["beds_exact"]["S03:04"]
    assert "zero of the four" in FROZEN["beds_exact"]["S03:05"]
    assert "the riemann as its conjecture of 1859 (believed, not known)" in FROZEN["beds_exact"]["S03:05"]
    assert "the check of a fact on my line is the walk of its own derivation path" in FROZEN["beds_exact"]["S02:13"]
    assert "twelve of my thirty-eight theorem facts" in FROZEN["beds_exact"]["S02:14"]
    assert "thirteen of my thirty-nine theorem facts" in FROZEN["beds_exact"]["S03:10"]
    assert "twenty-four carry the universal form" in FROZEN["beds_exact"]["S02:14"]
    assert "a form of the line is not a census of its end" in FROZEN["beds_exact"]["S02:14"]
    assert "a wall of my band is a fact of record of the boundary form" in FROZEN["beds_exact"]["S03:06"]
    assert "no theorem of any record settles the p versus np question" in FROZEN["beds_exact"]["S03:07"]
    # the carried summit statements carry byte-identical (the pnp
    # statement bed: the declared record language, never a theorem)
    assert "does p equal np" in FROZEN["beds_exact"]["S02:04"]
    assert "open of record" in FROZEN["beds_exact"]["S02:04"]
    # the beds carry NO off-line digit strings of record
    for v in FROZEN["beds_exact"].values():
        assert not _re.search(r"\d{10,}", v)


def test_lesson_phrases_are_house_voiced() -> None:
    """S20 is the connecting work: the four relationships enter as
    walks of the store's own facts. The S20 lessons are house-voiced
    on the line — and the theorem statement carries the shape
    invariant AND the line end (the filing fills the shape, not the
    statements)."""
    by_slug = {s: p for p, (_c, s, _k, _es, _d, _l) in S20_LESSONS.items()}
    # the weave: the cross-island joints as edges of the graph
    assert "the cross-island joints are already edges" in by_slug["weave-def"]
    assert "the divides question roots both" in by_slug["weave-def"]
    assert "at the line end eighty-four" in by_slug["weave-def"]
    # the summit shape: the fourfold shape of record
    assert "the same fourfold shape of record" in by_slug["summit-shape-def"]
    assert "the missing ingredient named, or the statement open of record" in by_slug["summit-shape-def"]
    assert "at the line end eighty-four" in by_slug["summit-shape-def"]
    # the shadow form: the store's own pattern (verification on the
    # line, the paths as the certificates)
    assert "my proof form is verification on the line" in by_slug["shadow-form-def"]
    assert "the check of a fact is the walk of its path, and it ends" in by_slug["shadow-form-def"]
    assert "at the line end eighty-four" in by_slug["shadow-form-def"]
    # the boundary form: walls and declared absences as one kind
    assert "a wall and a declared absence are one kind of fact of record" in by_slug["boundary-form-def"]
    assert "nowhere past it" in by_slug["boundary-form-def"]
    assert "at the line end eighty-four" in by_slug["boundary-form-def"]
    # the file: the shape invariant AND the line end in number words
    comp = S20_THEOREMS["summit-shape-filed"]["statement"]
    assert "the filing fills the shape, not the statements" in comp
    assert "at the line end eighty-four" in comp
    # NO island candidate is settled: the statements stay open of
    # record in the band material — never "p equals np is a theorem"
    # or any settled claim
    for text in list(S20_LESSONS) + [comp]:
        assert "p equals np is a theorem" not in text
        assert "the riemann hypothesis is true" not in text
        assert "beal's conjecture is true" not in text


def test_offline_values_never_store_answers() -> None:
    """S20 brings NO new off-line value: expect.offline_watch is
    empty, and no off-line digit string floats into an on-line
    answer, a bed, or a wall (the weaving names only values the
    line's record already holds)."""
    with open("bands/spec-e6.24.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    assert spec["expect"]["offline_watch"] == []
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        assert not _re.search(r"\d{10,}", str(v)), f"an off-line digit string floated into an on-line answer: {str(v)[:60]!r}"
    for v in FROZEN["walls_honest"].values():
        assert not _re.search(r"\d{10,}", v), "an off-line digit string must not live in an S20 wall"


def test_seam_carry_and_semantic_seam() -> None:
    # the FOUR carry rows (P6: byte-identical to the seed store):
    # the BSD summit carry, the Beal statement carry, the queue
    # (off-script standing check), and the Beal census carry
    assert FROZEN["seam_carry_refs"] == ["S02:02", "S02:03", "S04:07", "S04:17"]
    # the off-script standing check: the queue, byte-identical to the
    # store's own theorem statement (the weaving adds no lot — the
    # mechanism answers queue-declared's object verbatim)
    store = load_store(Path(FROZEN["seed"]))
    queue_fact = store.get("theorem:queue-declared")
    queue_byte = queue_fact.object if isinstance(queue_fact.object, str) else str(queue_fact.object)
    assert FROZEN["offscript_carry"] == {"what is the queue above my line?": queue_byte}
    # the queue byte is the S12 declared record: four lots, no fifth
    assert "carries exactly four lots, in declared order" in queue_byte
    assert "a fifth lot is not in the queue" in queue_byte
    # the riemann summit carry byte (the new S20 surface probing the
    # seed's declared-source conj): the statement verbatim + the open
    # status
    conj = store.get("conjecture:riemann")
    assert FROZEN["derived_table"]["S02:01"] == (
        f"the statement of the riemann island, as my store holds it: {conj.object} — "
        f"declared of record, open of record: believed, not known, at the line end 84"
    )
    # the statement carries from the S2 session byte-identical
    assert FROZEN["derived_table"]["S02:04"] == FROZEN["beds_exact"]["S02:04"]
    # the seam crosscheck expected value
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"


def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]


def test_probe_grammar_classifies() -> None:
    # the full 51-surface map (det_classify is the referee)
    plain = {
        "S02:01": "s20-rhsummit",
        "S02:02": "s16-bsd",
        "S02:03": "s17-beal",
        "S02:04": "s19-statement",
        "S02:05": "s20-soil",
        "S02:08": "s20-soil",
        "S02:09": "s20-node",
        "S02:10": "s20-form",
        "S02:13": "s20-form",
        "S02:14": "s20-marker",
        "S02:15": "s20-wallkind",
        "S03:01": "s20-shape",
        "S03:04": "s20-shape",
        "S03:05": "s20-open",
        "S03:06": "s20-wallkind",
        "S03:07": "s20-absence",
        "S03:10": "s20-marker",
        "S03:11": "s20-w1",
        "S03:12": "s20-w2",
        "S03:13": "s20-w3",
        "S03:14": "s20-w4",
        "S03:16": "s20-unc",
        "S03:17": "s20-open",
        "S04:01": "s20-soil",
        "S04:02": "s20-node",
        "S04:03": "s20-shape",
        "S04:04": "s20-open",
        "S04:05": "s20-form",
        "S04:06": "s20-marker",
        "S04:07": "s12-queue",
        "S04:08": "s20-wallkind",
        "S04:09": "s20-absence",
        "S04:14": "s20-w1",
        "S04:15": "s20-weavestate",
        "S04:16": "s20-unc",
        "S04:17": "s17-census",
    }
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {
        "S02:06": "weave-def",
        "S02:11": "shadow-form-def",
        "S02:16": "boundary-form-def",
        "S03:02": "summit-shape-def",
        "S03:15": "summit-shape-filed",
        "S04:10": "weave-def",
        "S04:11": "shadow-form-def",
        "S04:12": "boundary-form-def",
        "S04:13": "summit-shape-def",
    }
    for ref, want in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", "s20-state", want), ref
    derive_turns = {"S03:08": "derive", "S03:09": "derive"}
    for ref, want in derive_turns.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question" and slots.get("mode") == want, f"{ref}: {kind} {slots}"
        assert slots.get("target") == "summit-shape-filed", ref
    assertion_turns = ["S02:07", "S02:12", "S02:17", "S03:03"]
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what is the summit fact of the island?")[1]["mode"] == "s16-bsd"
    assert det_classify("what is the statement of the beal island of record?")[1]["mode"] == "s17-beal"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("what is the statement of the pnp island of record?")[1]["mode"] == "s19-statement"
    assert det_classify("state the line-pi-reduction rule")[1]["mode"] == "s18-state"
    assert det_classify("is dividing a question in p on my line?")[1]["mode"] == "s19-p"
    assert det_classify("what lives in the relativization territory?")[1]["mode"] == "s19-rel"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: the state readouts and the bandstate cite the
    # band's own file; the queue carry cites the carried queue
    # theorem
    assert FROZEN["theorem_allowed"] == {
        "S03:15": ["summit-shape-filed"],
        "S04:07": ["queue-declared"],
        "S04:15": ["summit-shape-filed"],
    }
    # the full sanctioned DAG: thirty-nine theorem facts (the S19
    # thirty-eight + summit-shape-filed); NO bare island candidate id
    dag = set(FROZEN["theorem_dag"])
    assert len(dag) == 39
    assert "theorem:summit-shape-filed" in dag
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
    assert SCRIPT_HASH == "2674472b8229aef5"


def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {
        "S03:11": ["summit-shape filing", "open of record", "line end 84"],
        "S03:12": ["fifth lot is not in the queue", "line end 84"],
        "S03:13": ["register of my weaving line is the line itself", "line end 84"],
        "S03:14": ["the store speaks, not the hand", "line end 84"],
        "S04:14": ["summit-shape filing", "open of record", "line end 84"],
    }


def test_band_map_frozen_untouched() -> None:
    # the weaving band is connecting work, not a new prize band: the
    # frozen bands-map (S10) stays untouched; e6.24 validates the
    # map as-is against the extended registry.
    from kainos.tutor.bands import BAND_MAP

    domains = {d for b in BAND_MAP for d in b.domains}
    assert "weave" not in domains, "the band map is frozen at S10 — no new band entries"
    assert "weave" not in {c.domain for c in CONCEPTS_E623}, "the weaving domain is NEW to this band"
    assert len(CONCEPTS_E624) == 120  # the S19 116 + the four weaving concepts


def test_domain_sequences_are_control_one() -> None:
    # freeze the control #1 strings verbatim (D-e6o(a): the final
    # total is 1823, one below the pre-registration of 1824 — the
    # S04:07 queue-carry event dedupes against the S19 seed's
    # S04:07 event id)
    assert FROZEN["domain_sequence"] == {
        2: "SSSSUULSSUULSSUUL",
        3: "UULSSSSFTSHHHHSSS",
        4: "SSSSSSSSSSSSSHSSS",
    }
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"


def test_discovery_candidate_invariant_full_width() -> None:
    """The D8 gate at FULL width (the connecting work must not settle
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
