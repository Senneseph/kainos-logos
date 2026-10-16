"""E3.7 end-to-end — the anti-corruption experiment (X3, P12)."""

from __future__ import annotations

import json
from pathlib import Path

from kainos.harness.runner import REGISTRY, Result
from kainos.workspace.bench import E3_7Experiment, run_e3_7


def test_e3_7_official_report_passes_all_checks(tmp_path: Path) -> None:
    r = run_e3_7(out_dir=tmp_path)
    assert r["passed"] is True
    assert r["query_accuracy"] == 1.0
    assert r["recursion_depth"] >= 2  # the grandchild's decision, from the root
    assert r["fork_isolation"] is True
    assert r["negative_control_passed"] is True  # the mandatory control, IN the report
    p = r["promotion"]
    assert p["assertion_count"] == 1
    assert all(v == "candidate" for v in p["status"].values())
    assert all(v == "workspace_PROJECT_GAME_fork" for v in p["source"].values())
    sv = r["source_versioning"]
    assert sv["analyses"] == 2 and sv["latest_version"] == 2
    assert sv["v1_immutable_after_v2"] is True
    assert sv["stale_on_hash_change"] and sv["stale_on_same_hash"] == []
    assert r["checks_passed"] == r["checks"]


def test_e3_7_writes_result_file(tmp_path: Path) -> None:
    r = run_e3_7(out_dir=tmp_path)
    out = tmp_path / "phase-3" / "e3.7.json"
    assert out.exists()
    data = json.loads(out.read_text())
    assert data == r
    assert "negative_control_passed" in data  # the spec: in the result file
    assert "config" in data and isinstance(data["config"]["commit"], str)


def test_e3_7_is_byte_deterministic(tmp_path: Path) -> None:
    a = run_e3_7(out_dir=tmp_path / "a")
    b = run_e3_7(out_dir=tmp_path / "b")
    ba = (tmp_path / "a" / "phase-3" / "e3.7.json").read_bytes()
    bb = (tmp_path / "b" / "phase-3" / "e3.7.json").read_bytes()
    assert a == b
    assert ba == bb  # byte-stable report (fixed script, fixed timestamps, no RNG)


def test_e3_7_experiment_class_and_registry() -> None:
    assert "e3.7" in REGISTRY
    exp = E3_7Experiment()
    assert exp.name == "e3.7"
    assert isinstance(exp.hypothesis, str) and isinstance(exp.metric, str)
    assert "negative control" in exp.metric
    res = exp.run()  # note: exp.run() raw — the runner fills commit/threshold
    assert isinstance(res, Result)
    assert res.passed is True and res.value == 1.0
    assert isinstance(exp.threshold, str)
    assert res.config["negative_control_passed"] is True
