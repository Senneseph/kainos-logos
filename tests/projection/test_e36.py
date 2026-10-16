"""E3.6 end-to-end (fast, hermetic): the full battery passes its
pre-registered threshold deterministically."""

from __future__ import annotations

from pathlib import Path

from kainos.projection.bench import E3_6Experiment, run_e3_6


def test_e36_rates_and_policy():
    r = run_e3_6(out_dir=None)
    assert r["passed"] is True
    assert r["goal_achievable_validity"] == 1.0
    assert r["honest_refusal_rate"] == 1.0
    assert r["clarification_policy"]["high_stakes"] == "ask"
    assert r["clarification_policy"]["low_stakes"] == "default"
    assert r["clarification_policy"]["policy_ok"] is True
    assert r["clarification_policy"]["applied_default"] == "artifact_available=SEARCH_CODEX|WRITE_TEXT"


def test_e36_creativity_block():
    r = run_e3_6(out_dir=None)
    c = r["creativity"]
    assert c["t0_greedy_deterministic"] is True
    assert len(c["t0_plans"]) == 1
    assert c["spread_met"] is True and c["all_valid"] is True
    assert c["traces_record_temperature_and_seed"] is True
    assert c["distinct_plans"]  # at least the spread floor (2)
    assert len(c["per_seed"]) == 3


def test_e36_gap_and_refusal_details():
    r = run_e3_6(out_dir=None)
    g3 = r["per_goal"]["PRODUCE_IMAGE"]
    assert g3["refusal_ok"] is True
    assert g3["gap"] == "image_capability"
    assert g3["trace_size"] > 0
    assert g3["contract"]["valid"] is True and g3["contract"]["violations"] == []


def test_e36_writes_files(tmp_path: Path):
    run_e3_6(out_dir=tmp_path)
    assert (tmp_path / "e3.6.json").exists()
    assert (tmp_path / "phase-3" / "e3.6.json").exists()
    assert (tmp_path / "e3.6.md").exists()


def test_e36_deterministic():
    import json

    a = json.dumps(run_e3_6(out_dir=None), sort_keys=True)
    b = json.dumps(run_e3_6(out_dir=None), sort_keys=True)
    assert a == b


def test_experiment_class():
    res = E3_6Experiment().run()
    assert res.passed
    assert res.value == 1.0
    assert res.config["validity"] == 1.0 and res.config["refusal"] == 1.0
    assert res.evidence[0] == Path("results/phase-3/e3.6.json")
