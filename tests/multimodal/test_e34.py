"""E3.4 end-to-end — cross-modal corroboration + consolidation in the CODEX."""

from __future__ import annotations

import json
from pathlib import Path

from kainos.harness.runner import REGISTRY, Result
from kainos.multimodal.bench import E3_4Experiment, run_e3_4


def test_e3_4_report_meets_the_threshold(tmp_path: Path) -> None:
    r = run_e3_4(out_dir=tmp_path)
    assert r["passed"] is True
    # one abstract pattern recognized across modalities:
    assert r["pattern_matched_cross_modal"] is True
    pt, pv = r["patterns"]["text"], r["patterns"]["vision"]
    assert pt["pattern"] == pv["pattern"] == "TRANSFER"
    assert pt["object"] == pv["object"] == "box"
    assert pt["actor"] == "john" and pv["actor"] is None  # modality-specific knowledge
    assert pt["from"] is None and pt["to"] is None
    assert pv["from"] == "(0.0,0.0,0.0)" and pv["to"] == "(4.0,4.0,4.0)"
    # one entity consolidated from >=2 modalities:
    assert r["entity_consolidated"] is True
    assert r["consolidated_entities"] == ["box"]
    cons = r["consolidation"]["box"]
    assert cons["modalities"] == ["modality_synthetic_vision", "modality_text"]
    assert len(cons["assertion_ids"]) == 2


def test_e3_4_writes_result_file_and_is_deterministic(tmp_path: Path) -> None:
    a = run_e3_4(out_dir=tmp_path / "a")
    b = run_e3_4(out_dir=tmp_path / "b")
    out = tmp_path / "a" / "phase-3" / "e3.4.json"
    assert out.exists()
    assert json.loads(out.read_text()) == a
    assert a == b
    assert (tmp_path / "a" / "phase-3" / "e3.4.json").read_bytes() == (
        tmp_path / "b" / "phase-3" / "e3.4.json"
    ).read_bytes()


def test_e3_4_experiment_class_and_registry() -> None:
    assert "e3.4" in REGISTRY
    exp = E3_4Experiment()
    assert exp.name == "e3.4"
    assert isinstance(exp.hypothesis, str) and isinstance(exp.metric, str)
    res = exp.run()
    assert isinstance(res, Result)
    assert res.passed is True and res.value == 1.0
    assert res.config["pattern_matched"] is True
    assert res.config["consolidated_entities"] == ["box"]
