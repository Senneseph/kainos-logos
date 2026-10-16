"""Session runtime (T3): boot/restore/lapse over the persistent CODEX.

The pilot's lifecycle discipline: strictly sequential sessions, restored
CODEX over an EMPTY workspace, logged lapses, and — the point of it all —
learning surviving the restart.
"""

from __future__ import annotations

import json

import pytest

from kainos.tutor.session import (
    InfantRuntime,
    codex_dump_path,
    deterministic_bytes,
    session_report_path,
)


def _boot_and_teach(rt: InfantRuntime, session: int, turns: list[str]) -> dict:
    rt.boot(session)
    for t in turns:
        rt.turn(t)
    return rt.lapse().to_dict()


def test_first_session_starts_fresh(tmp_path):
    rt = InfantRuntime(tmp_path)
    rep = _boot_and_teach(rt, 1, ["after 0 comes 1"])
    assert rep["restored"] is False
    assert rep["workspace_empty_at_boot"] is True
    assert len(rep["turns"]) == 1


def test_second_session_restores_and_stays_empty_at_boot(tmp_path):
    rt = InfantRuntime(tmp_path)
    _boot_and_teach(rt, 1, ["after 0 comes 1", "after 1 comes 2"])
    rep2 = _boot_and_teach(rt, 2, ["what comes after 1?"])
    assert rep2["restored"] is True
    assert rep2["workspace_empty_at_boot"] is True
    turn = rep2["turns"][0]
    assert turn["kind"] == "question"
    assert turn["response_ir"]["answer"] == "2"  # learned in S1, answered in S2


def test_learning_survives_restart_byte_equal(tmp_path):
    rt = InfantRuntime(tmp_path)
    rt.boot(1)
    for n in range(5):
        rt.turn(f"after {n} comes {n + 1}")
    a1 = rt.turn("2 + 3 is what?")
    rt.lapse()
    rt.boot(2)
    a2 = rt.turn("2 + 3 is what?")
    # ANSWERED turns carry no turn stamp in their grounded IR — the proof
    # chain cites the (persistent) fact ids, so the S2 turn is bit-equal.
    for k in ("kind", "slots", "response_ir", "response_text", "grounded"):
        assert a1.to_dict()[k] == a2.to_dict()[k], k
    assert a2.response_ir["answer"] == "5"


def test_sessions_are_strictly_sequential(tmp_path):
    rt = InfantRuntime(tmp_path)
    with pytest.raises((RuntimeError, ValueError)):
        rt.boot(1)
        rt.boot(1)  # no lapse in between
    rt.lapse()
    with pytest.raises(ValueError):
        rt.boot(1)  # replaying history is refused


def test_missing_dump_is_an_error_not_a_fresh_store(tmp_path):

    rt = InfantRuntime(tmp_path)
    _boot_and_teach(rt, 1, ["after 0 comes 1"])
    # remove the S1 dump: S2 must fail loudly, not silently start fresh
    codex_dump_path(tmp_path, 1).unlink()
    with pytest.raises(FileNotFoundError):
        rt.boot(2)


def test_persisted_files_are_byte_stable(tmp_path):
    def run_once(root):
        rt = InfantRuntime(root)
        _boot_and_teach(rt, 1, ["after 0 comes 1", "after 1 comes 2", "what comes after 1?"])

    run_once(tmp_path / "a")
    run_once(tmp_path / "b")
    for name in ("codeX-S01.json", "session-S01.json"):
        left = (tmp_path / "a" / name).read_bytes()
        right = (tmp_path / "b" / name).read_bytes()
        assert left == right
    # the report is valid JSON with the frozen shape
    rep = json.loads(session_report_path(tmp_path / "a", 1).read_text())
    assert set(rep) >= {"session", "restored", "turns", "mastery", "attention", "codex", "workspace", "arm"}
    assert deterministic_bytes(rep)  # round-trips through the deterministic serializer


def test_lapse_report_records_mastery_and_added(tmp_path):
    rt = InfantRuntime(tmp_path)
    rep = _boot_and_teach(rt, 1, ["after 0 comes 1", "what comes after 0?"])
    assert rep["mastery"]["count-successor"]["state"] == "practicing"
    assert rep["codex"]["total"] > 0
    assert any("lesson" in e for e in rep["turns"][0]["events"])
    assert rep["arm"] == {"llm_events": 0, "fallback_events": 0}
