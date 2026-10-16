"""E3.3 end-to-end (fast, hermetic): the two-node bear story must PASS its
pre-registered threshold, deterministically."""

from __future__ import annotations

import json
from pathlib import Path

from kainos.exchange.bench import run_e3_3


def test_e33_passes_thresholds(tmp_path: Path):
    report = run_e3_3(out_dir=tmp_path)
    assert report["passed"] is True, report["threshold"]

    th = report["threshold"]
    assert th["new_context_term_ge_1"]
    assert th["both_values_retained_established"]
    assert th["distinct_contexts_ge_2"]
    assert th["disputed_count_zero"]
    assert th["no_averaging"]
    assert th["converged_identical_knowledge"]
    assert report["idempotent_remerge"] is True

    # the new context TERM is the one the plan's candidate list predicts first
    assert report["evidence"]["context_terms"] == {
        "node_arctic_winter": ["ctx:time:polar_bear"],
        "node_arctic_summer": ["ctx:time:polar_bear"],
    }

    for nr in report["per_node"].values():
        rec = nr["reconciliation"]
        assert rec["explained"] and rec["dimension"] == "time"
        assert rec["term_id"] == "ctx:time:polar_bear"
        assert rec["disputed_before"] == 4 and rec["disputed_after"] == 0
        assert nr["disputed"] == 0

    # both merge reports carried every incoming delta (no silent drops)
    for nr in report["per_node"].values():
        mr = nr["merge_report"]
        assert len(mr["merged"]) == 2 and len(mr["disputed"]) == 4


def test_e33_writes_results_files(tmp_path: Path):
    run_e3_3(out_dir=tmp_path)
    flat = tmp_path / "e3.3.json"
    phase = tmp_path / "phase-3" / "e3.3.json"
    assert flat.exists() and phase.exists()
    a = json.loads(flat.read_text())
    b = json.loads(phase.read_text())
    assert a == b
    assert (tmp_path / "e3.3.md").exists()


def test_e33_deterministic(tmp_path: Path):
    r1 = run_e3_3(out_dir=None)
    r2 = run_e3_3(out_dir=None)
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)


def test_experiment_class_passes():
    from dataclasses import fields  # noqa: F401 (shape check only)

    from kainos.exchange.bench import E3_3Experiment

    result = E3_3Experiment().run()
    assert result.passed
    assert result.name == "e3.3"
    assert result.value == 1.0  # one new context term
    assert result.config["converged"] is True
    assert result.config["new_context_terms"] == ["ctx:time:polar_bear"]
    assert result.evidence[0] == Path("results/phase-3/e3.3.json")
