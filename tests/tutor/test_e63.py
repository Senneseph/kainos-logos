"""E6.3 — the un-attended loop (T5 #155): author policy, the LLM seam,
the analysis arm, the attention inbox, and the full-run pins (from the
official control; the official run must reproduce these EXACTLY)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import det_classify
from kainos.tutor.loop import FROZEN, author_decision, run_loop


@pytest.fixture
def frozen(monkeypatch):
    """Monkeypatch the loop's config dict (restored after the test)."""

    saved = dict(FROZEN)
    yield FROZEN
    FROZEN.clear()
    FROZEN.update(saved)


class _SeqAuthor:
    """A deterministic LLM author: first N lines are garbage (to
    exercise the bounded retry/drop), then it says the successor
    lesson for the line end it sees in the context — or a drill once
    the line reaches the cap."""

    name = "seq-author"

    def __init__(self, garbage: int = 2) -> None:
        self.garbage = garbage
        self.calls = 0

    def line(self, context: str) -> str:
        self.calls += 1
        if self.calls <= self.garbage:
            return "blah"  # unparseable on purpose
        m = re.search(r"the number line ends at (\d+)", context)
        n = int(m.group(1)) if m else 0
        if n < FROZEN["line_cap"] and f"after {n} comes {n + 1}" not in context:
            return f"after {n} comes {n + 1}"
        return "1 + 1 is what?"


class _DetLineAuthor:
    """A deterministic LLM author: line is a pure function of the
    context (no hidden state) — the determinism a real stateless
    backend would give, so the LLM-arm run is byte-identical too."""

    def line(self, context: str) -> str:
        m = re.search(r"the number line ends at (\d+)", context)
        if m is None:
            return "1 + 1 is what?"
        n = int(m.group(1))
        if n < FROZEN["line_cap"]:
            return f"after {n} comes {n + 1}"
        return "1 + 1 is what?"


class _StallAuthor:
    """An LLM author that hammers one UNLEARNED drill (honest gaps)."""

    def line(self, context: str) -> str:
        return "14 - 1 is what?"


class _WrongLessonAuthor:
    """An LLM author that teaches a WRONG successor on turn 2 (a
    genuine conflict; the dispute/attention discipline must handle
    it, and the inbox must file — never post — the ticket)."""

    name = "wrong-lesson-author"

    def __init__(self) -> None:
        self.calls = 0

    def line(self, context: str) -> str:
        self.calls += 1
        if self.calls == 1:
            return "after 0 comes 1"
        if self.calls == 2:
            return "after 1 comes 2"
        if self.calls == 3:
            return "after 1 comes 3"  # a DIFFERENT value for the existing fact 1 -> 2
        m = re.search(r"the number line ends at (\d+)", context)
        n = int(m.group(1)) if m else 2
        if n < FROZEN["line_cap"]:
            return f"after {n} comes {n + 1}"
        return "1 + 1 is what?"


def test_author_policy_first_line_and_cap(frozen: dict) -> None:
    frozen.update({"line_cap": 5, "sessions_max": 1, "turns_per_session": 12})
    store = InMemoryCodexStore()
    d = author_decision(store, 1)
    assert d == {"kind": "lesson-succ", "surface": "after 0 comes 1", "concept": "count-successor", "reason": d["reason"]}
    # grow the line to the cap with the policy's own decisions
    import tempfile

    from kainos.tutor.session import InfantRuntime

    with tempfile.TemporaryDirectory() as td:
        rt = InfantRuntime(Path(td))
        rt.boot(1)
        for _ in range(5):
            rt.turn(author_decision(rt.final_store(), 1)["surface"])
        d = author_decision(rt.final_store(), 1)
        assert d["kind"] != "lesson-succ"  # the cap is a hard stop for lessons
        assert _line_end_view(rt.final_store()) == 5


def _line_end_view(store) -> int:
    end = 0
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        sid, oid = a.subject.id, a.object_id
        if sid.startswith("count-successor:succ-of(") and oid.startswith("count-successor:num(") and (a.validity is None or a.validity.to is None):
            end = max(end, int(oid[len("count-successor:num(") : -1]))
    return end


def test_canonical_forms_cover_the_frozen_grammar() -> None:
    from kainos.tutor.loop import _canonical_form

    cases = {
        "after 3 comes 4": "after 3 comes 4",
        "after 12 comes 14": "after 12 comes 14",  # the FORM is frozen; the VALUE is the store's business
        "what comes after 9?": "what comes after 9?",
        "11 + 4 is what?": "11 + 4 is what?",
        "8 - 3 is what?": "8 - 3 is what?",
        "6 * 7 is what?": "6 * 7 is what?",
        "is 25 larger than 6?": "is 25 larger than 6?",
        "subtraction is walking backward": "subtraction is walking backward",
    }
    for line, want in cases.items():
        c = det_classify(line)
        assert _canonical_form(c) == want, line
    assert _canonical_form(det_classify("please recite the gettysburg address")) is None


def test_llm_seam_deterministic_author_is_byte_identical(frozen: dict, tmp_path: Path) -> None:
    """With a deterministic (context-function) LLM author — what a
    stateless real backend is — the whole LLM-arm run is
    byte-identical (the seam is neutral: determinism is a property of
    (loop, author), not of the det arm alone)."""

    frozen.update({"line_cap": 8, "sessions_max": 2, "turns_per_session": 14})
    rep = run_loop(tmp_path / "e63detllm", author=_DetLineAuthor())
    assert rep["arm"]["author"] == "llm" and rep["arm"]["llm_arm"] == "llm"
    kinds = {r["author_kind"] for srow in rep["sessions"] for r in srow["records"]}
    assert kinds == {"llm-line"}
    assert rep["run2_identical"]["identical"] is True
    assert rep["arm"]["llm_dropped"] == []


def test_llm_seam_bounded_retry_drops(frozen: dict, tmp_path: Path) -> None:
    """A flaky author: garbage lines are retried ONCE (E3.1 — no
    rescue loops) and then dropped + logged; the loop continues with
    whatever it can say."""

    frozen.update({"line_cap": 8, "sessions_max": 2, "turns_per_session": 14})
    rep = run_loop(tmp_path / "e63flaky", author=_SeqAuthor(garbage=2))
    assert rep["arm"]["author"] == "llm"
    assert len(rep["arm"]["llm_dropped"]) == 1, "one bounded drop attempt (2 garbage lines, 1 retry)"
    assert "twice" in rep["arm"]["llm_dropped"][0]["note"]
    assert all(d["author_line"] == "dropped" for d in rep["arm"]["llm_dropped"])


def test_wrong_llm_lesson_files_a_dispute_ticket_never_posts(frozen: dict, tmp_path: Path) -> None:
    frozen.update({"line_cap": 8, "sessions_max": 2, "turns_per_session": 6})
    rep = run_loop(tmp_path / "e63wrong", author=_WrongLessonAuthor())
    assert rep["tickets"], "a wrong lesson is a genuine conflict — the inbox must file"
    for t in rep["tickets"]:
        assert t["dedup_key"].startswith(("dispute:", "stalled:"))
        assert t["posted"] is False
        assert t["assignee"] == FROZEN["owner_assignee"]
    keys = [t["dedup_key"] for t in rep["tickets"]]
    assert len(keys) == len(set(keys)), "dedup must hold"
    assert rep["posted"] == []


def test_unfixable_stall_files_the_persist_trigger(frozen: dict, tmp_path: Path) -> None:
    frozen.update({"line_cap": 5, "sessions_max": 4, "turns_per_session": 6, "stalled_sessions": 3, "stalled_gaps": 4})
    rep = run_loop(tmp_path / "e63stall", author=_StallAuthor())
    assert rep["convergence"]["converged"] is False
    stalled_seen = [srow["diagnosis"]["stalled"] for srow in rep["sessions"]]
    assert any("sub-within-30" in s for s in stalled_seen), "the hammered unlearned concept must register as stalled"
    keys = {t["dedup_key"] for t in rep["tickets"]}
    assert "stalled:sub-within-30" in keys, "the second consecutive stall files the trigger"
    # the fix could not be applied (no grounded drill for an unlearned
    # capability) — that is recorded, and it is what makes the stall
    # unresolvable in-loop (D-e6h).
    fix_rows = [srow["diagnosis"]["fix"] for srow in rep["sessions"] if srow["diagnosis"]["fix"]]
    assert fix_rows and all(f["action"] == "re-expose" for f in fix_rows)


def test_full_run_pins_the_official_control(tmp_path: Path) -> None:
    """The full det run (97 turns over 3 sessions) with the frozen pins
    from the official control; the official run reproduces these."""

    rep = run_loop(tmp_path / "e63full")
    assert rep["convergence"] == {"converged": True, "converged_at_session": 3}
    assert rep["final_store"] == {"total": 182, "line_end": 70, "open_disputes": [], "beyond_cap": []}
    assert rep["tickets"] == [] and rep["posted"] == []
    assert rep["run2_identical"]["identical"] is True
    assert len(rep["run2_identical"]["files"]) == 7  # 3 codeX + 3 session + loop-report
    n_turns = [len(srow["records"]) for srow in rep["sessions"]]
    assert n_turns == [40, 40, 17]
    states3 = rep["sessions"][2]["diagnosis"]["concepts"]
    assert all(v["state"] == "stable" for v in states3.values())
    assert len(states3) == 6
    # the line-first order: S1 is 40 successor lessons, S2 reaches the cap
    s1 = rep["sessions"][0]["records"]
    assert all(r["author_kind"] == "lesson-succ" for r in s1)
    s1_end = rep["sessions"][0]["diagnosis"]["line_end"]
    s2_end = rep["sessions"][1]["diagnosis"]["line_end"]
    assert (s1_end, s2_end) == (40, 70)


def test_ticket_payload_shape(frozen: dict) -> None:
    from kainos.tutor.loop import _ticket_payload

    trig = {"kind": "open-dispute", "dedup_key": "dispute:cs-x", "severity": "high", "evidence": ["S02:04", "cs-x"]}
    p = _ticket_payload(trig, 2, Path("results/phase-6/e6.3-run1"))
    assert p["assignee"] == "Jesse Miller" and p["project"] == "Kainos-Logos"
    assert p["posted"] is False
    assert "S02" in p["subject"] or "dispute" in p["subject"]


def test_experiment_class_passes_the_full_run(tmp_path: Path) -> None:
    # the experiment class runs under the default out dir honouring the
    # env; point it at tmp via the env for this test.
    import os

    os.environ["KAINOS_RESULTS_DIR"] = str(tmp_path)
    try:
        from kainos.tutor.loop import CHECKS, E6_3Experiment

        r = E6_3Experiment().run()
        assert r.passed is True and r.value == 1.0 and CHECKS == 7
    finally:
        os.environ.pop("KAINOS_RESULTS_DIR", None)
