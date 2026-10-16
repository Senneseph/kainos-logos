"""E6.4 — phrasology (D-e6i): the mechanism (phrasings as store facts,
grammar-first intake, honest unknowns, the correction pair) and the
full-run pins (from the frozen control; the official run must
reproduce these EXACTLY)."""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.tutor.brainstem import (
    CANON_TEMPLATES,
    REL_PHRASING,
    Brainstem,
    det_classify,
)
from kainos.tutor.e64 import FROZEN, SCRIPT_HASH, E6_4Experiment, run_e6_4


@pytest.fixture
def bs():
    b = Brainstem(codex=InMemoryCodexStore())
    b._set_session(1)  # house pattern: the runtime boots before turning
    return b


def _phrasings(bs):
    return [a for a in bs._codex.query(relation=REL_PHRASING)]


def test_teach_classify_and_fact(bs):
    k, slots = det_classify('the phrasing "what is the sum of {a} and {b}?" is the same as "{a} + {b} is what?"')
    assert k == "assertion"
    assert slots["new"] == "what is the sum of {a} and {b}?"
    r = bs.turn('the phrasing "what is the sum of {a} and {b}?" is the same as "{a} + {b} is what?"')
    assert r.kind == "assertion"
    for n in range(1, 14):  # seed the line 0..13 (capability = store data)
        bs.turn(f"after {n - 1} comes {n}")
    ps = bs.turn("what is the sum of 6 and 7?")
    assert ps.kind == "question"
    assert str(ps.response_ir["parse_source"]).startswith("lexicon:phrasing:")
    assert ps.response_ir["answer"] == "13"
    g = bs.turn("6 + 7 is what?")  # the canonical form: grammar stays first
    assert g.response_ir["parse_source"] == "grammar"
    assert g.response_ir["answer"] == "13"
    assert len(_phrasings(bs)) == 1  # one fact, not duplicated per use


def test_teach_line_without_numbers_still_teaches(bs):
    """the lesson-family template carries no digits — it must still be
    a teach (a numeric-only guard would have died here)."""
    line = 'the phrasing "the number after {a} is {b}" is the same as "after {a} comes {b}"'
    k, slots = det_classify(line)
    assert k == "assertion" and slots["new"] == "the number after {a} is {b}"
    # the canonical lesson template is named by its POLICY slot names
    # (a, b) — the mapping names declare the canonical slot each surface
    # position fills
    assert "after {a} comes {b}" in dict(CANON_TEMPLATES).values()


def test_invalid_mapping_rejected_honestly(bs):
    r = bs.turn('the phrasing "what is the sum of {a} and {b}?" is the same as "what do the digits mean?"')
    assert r.kind == "ambiguous"
    assert not r.memory_diff
    r = bs.turn('the phrasing "what is the sum of {a} and {c}?" is the same as "{a} + {b} is what?"')
    assert r.kind == "ambiguous"
    assert not r.memory_diff
    assert _phrasings(bs) == []


def test_honest_unknown_then_parsed(bs):
    for n in range(7):  # seed the line 0..7 (capability = store data)
        bs.turn(f"after {n} comes {n + 1}")
    u = bs.turn("how many fingers do hand 3 and hand 4 have?")
    assert u.kind == "ambiguous"
    assert "teach me the mapping" in u.response_text
    assert not u.memory_diff
    bs.turn('the phrasing "how many fingers do hand {a} and hand {b} have?" is the same as "{a} + {b} is what?"')
    p = bs.turn("how many fingers do hand 3 and hand 4 have?")
    assert p.kind == "question" and p.response_ir["answer"] == "7"


def test_wrong_mapping_then_correction(bs):
    bs.turn("subtraction is walking backward")  # the sub capability (store data)
    bs.turn("comparison is walking the line")  # the cmp capability
    for n in range(1, 18):  # the line 0..17
        bs.turn(f"after {n - 1} comes {n}")
    bs.turn('the phrasing "is {a} bigger than {b}?" is the same as "{a} - {b} is what?"')
    w = bs.turn("is 17 bigger than 9?")
    assert w.response_ir["answer"] == "8"  # the wrong mapping answers the subtraction
    c = bs.turn('no — that was a mistake; the phrasing "is {a} bigger than {b}?" is the same as "is {a} larger than {b}?"')
    assert c.kind == "correction"
    a = bs.turn("is 17 bigger than 9?")
    assert str(a.response_ir["answer"]).startswith("yes")
    phr = _phrasings(bs)
    open_facts = [x for x in phr if x.status == EpistemicState.established and x.subject.id.startswith("phr:") and (x.validity is None or x.validity.to is None)]
    obsolete = [x for x in phr if x.status == EpistemicState.obsolete and x.subject.id.startswith("phr:")]
    assert len(open_facts) == 1  # single current claimant (D-e6c)
    assert len(obsolete) == 1  # the wrong one is KEPT, closed
    assert all(x.validity is not None and x.validity.to is not None for x in obsolete)  # validity ended
    assert not [x for x in phr if x.status == EpistemicState.disputed]  # none left open
    replacement = open_facts[0].id
    assert replacement in obsolete[0].provenance.evidence  # the superseded fact links its replacement


def test_lesson_family_composes_with_line(bs):
    bs.turn("after 70 comes 71")  # a seed fact beyond the line I build below
    bs.turn('the phrasing "the number after {a} is {b}" is the same as "after {a} comes {b}"')
    p = bs.turn("the number after 55 is 56")
    assert p.kind == "assertion"
    assert str(p.response_ir.get("ack") or "").startswith("after 55")


def test_full_run_pins(tmp_path):
    rep = run_e6_4(tmp_path)
    assert rep["passed"] == 8 and rep["value"] == 1.0
    turns = rep["turns"]
    assert len(turns) == 42
    assert sorted(r for r, t in turns.items() if t["kind"] == "ambiguous") == ["S02:01", "S02:02", "S02:13", "S03:09", "S04:09"]
    assert turns["S02:04"]["response_ir"]["answer"] == "13"
    assert turns["S02:15"]["response_ir"]["answer"] == "8"
    assert turns["S03:08"]["response_ir"]["uncertainty_state"] == "needs_info"
    assert FROZEN["total_turns"] == 42
    assert isinstance(SCRIPT_HASH, str) and len(SCRIPT_HASH) == 16


def test_experiment_class_runs(tmp_path):
    import os

    e = E6_4Experiment()
    old = os.environ.get("KAINOS_RESULTS_DIR")
    os.environ["KAINOS_RESULTS_DIR"] = str(tmp_path)
    try:
        r = e.run()
    finally:
        if old is None:
            os.environ.pop("KAINOS_RESULTS_DIR", None)
        else:
            os.environ["KAINOS_RESULTS_DIR"] = old
    assert r.passed is True and r.value == 1.0
