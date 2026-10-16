"""E1.1 runner tests (P1.09) — full-corpus parity, the harness registration,
and the failure path (a deliberately wrong expectation is reported, not hidden).
"""

from __future__ import annotations

import json

from kainos.harness.runner import REGISTRY, resolve
from kainos.regex.bench import (
    E1_1Experiment,
    corpus_hash,
    default_corpus_path,
    run_e1_1,
)

# ── the claim: 100% parity on the full corpus ──────────────────────────────


def test_e1_1_full_parity(tmp_path):
    report = run_e1_1(out_dir=tmp_path / "r")
    assert report["accuracy"] == 1.0
    assert len(report["per_item"]) == report["config"]["n_records"]
    assert all(item["ok"] for item in report["per_item"])
    for item in report["per_item"]:
        assert item["pcre"] == item["expected"]


def test_e1_1_writes_the_phase1_report(tmp_path):
    report = run_e1_1(out_dir=tmp_path)
    written = json.loads((tmp_path / "e1.1.json").read_text(encoding="utf-8"))
    assert written == report
    assert written["config"]["corpus_hash"] == corpus_hash(default_corpus_path())
    assert "seed" in written["config"]


def test_run_e1_1_is_deterministic(tmp_path):
    a = run_e1_1(out_dir=tmp_path / "a")
    b = run_e1_1(out_dir=tmp_path / "b")
    assert a == b


# ── failure path: mismatches are reported per item ─────────────────────────


def test_e1_1_reports_a_wrong_expectation(tmp_path):
    from kainos.regex.data import load_corpus

    records = load_corpus(default_corpus_path())
    broken = [dict(r) for r in records]
    broken[0]["expected_pcre"] = broken[0]["expected_pcre"] + "X"  # impossible suffix
    corpus = tmp_path / "broken.jsonl"
    corpus.write_text(
        "\n".join(
            json.dumps({k: r[k] for k in ("id", "description", "expected_pcre", "positive", "negative")})
            for r in broken
        )
        + "\n",
        encoding="utf-8",
    )
    report = run_e1_1(corpus_path=corpus, out_dir=tmp_path / "out")
    assert report["accuracy"] < 1.0
    bad = [i for i in report["per_item"] if not i["ok"]]
    assert len(bad) == 1
    assert bad[0]["note"] == "pcre mismatch"


# ── harness registration ───────────────────────────────────────────────────


def test_e1_1_registered_in_harness():
    exp = REGISTRY["e1.1"]
    assert isinstance(exp, E1_1Experiment)
    assert exp.threshold == "== 1.0"
    assert exp.name == "e1.1"
    assert resolve("e1.1") is exp
    # Phase selection sees it as Phase 1.
    from kainos.harness import runner as runner_mod

    assert any(e.name == "e1.1" for e in runner_mod.selected(phase=1))


def test_experiment_run_returns_result_contract(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # results/phase-1/e1.1.json lands in the sandbox
    result = E1_1Experiment().run()
    assert result.name == "e1.1"
    assert result.passed is (result.value == 1.0)
    assert result.value == 1.0
    assert str(result.evidence[0]) == "results/phase-1/e1.1.json"
    assert (tmp_path / "results/phase-1/e1.1.json").is_file()
    assert result.config["dataset_hash"]
    assert result.config["per_item"]
