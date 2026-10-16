"""E4.1 harness integration: bench report, experiment class, registration."""

from __future__ import annotations

import json
from pathlib import Path

from kainos.harness.runner import REGISTRY, resolve, selected
from kainos.puzzle.bench import E4_1Experiment, run_e4_1


def test_bench_report_all_checks_pass(tmp_path: Path) -> None:
    report = run_e4_1(out_dir=tmp_path)
    assert report["passed"] is True
    assert report["checks"] == 14
    assert report["checks_passed"] == 14
    full = tmp_path / "phase-4" / "e4.1.json"
    assert full.exists()
    data = json.loads(full.read_text())
    assert data["passed"] is True
    assert data["checks_passed"] == 14
    assert data["arms"]["F"]["status"] == "SKIPPED"  # no Ollama in tests
    assert data["arms"]["A"]["status"] == "solved"
    assert data["arms"]["C"]["n_solutions"] == 2
    assert [c["clue"] for c in data["arms"]["D"]["certificate"]] == [9, 16]
    assert data["arms"]["E"]["status"] == "solved"


def test_experiment_class_returns_passing_result(tmp_path: Path) -> None:
    run_e4_1(out_dir=tmp_path)
    result = E4_1Experiment().run()
    assert result.name == "e4.1"
    assert result.passed is True
    assert result.value == 1.0
    assert result.threshold is None or "14/14" in result.threshold
    assert result.config["checks_passed"] == 14
    assert result.config["arm_f_status"] == "SKIPPED"


def test_registration_and_phase_selection() -> None:
    assert "e4.1" in REGISTRY
    assert resolve("e4.1").name == "e4.1"
    # short names are the part after the FIRST dot ("1") — ambiguous across
    # phases by design (e1.1/e2.1/e3.1/e4.1); the exact key is what commands use
    assert [e.name for e in selected(phase=4)] == ["e4.1"]


def test_experiment_contract_fields() -> None:
    exp = E4_1Experiment()
    assert exp.name == "e4.1"
    assert exp.hypothesis
    assert exp.metric
    assert exp.threshold
