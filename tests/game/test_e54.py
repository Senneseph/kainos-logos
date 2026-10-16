"""E5.4 (T6 #166, M4 stretch) — the LLM-surface messaging arm: the
official (SKIP/canonical) arm's pins, the frozen X3 drop values, and
the experiment class (full 5/5 against the frozen control)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kainos.game.e54 import (
    CHECKS,
    GRAMMAR_SHA,  # noqa: F401  (re-exported for drift checks)
    E5_4Experiment,
    run_e5_4,
)


@pytest.fixture
def run(tmp_path: Path) -> dict:
    return run_e5_4(tmp_path, write=False)


def test_x1_the_twelve_e51_claims_survive(run: dict) -> None:
    c = run["checks"][0]
    assert c["name"] == "x1-e51-claims-survive-exactly" and c["passed"]
    claims = c["detail"]["e51_claims"]
    assert len(claims) == 12
    assert all(v is True for v in claims.values()), claims


def test_x2_seam_neutrality(run: dict) -> None:
    c = run["checks"][1]
    assert c["passed"]
    assert all(c["detail"]["stores_identical"].values())
    assert all(c["detail"]["stripped_hash_match"].values())


def test_x3_honest_drop_matches_the_frozen_control(run: dict) -> None:
    c = run["checks"][2]
    assert c["passed"]
    obs = c["detail"]["observed"]
    # the frozen prediction, verbatim: one dropped message flips the
    # detector (a cannot detect what b never said), erases a's only
    # belief about b, and still recovers the grid
    assert obs["drops_logged"] == 1
    assert obs["first_correct"] == {
        "round": 4,
        "by": "b",
        "target": "a",
        "object": "row3:door mine=c3 other=c4",
    }
    assert obs["a_beliefs_about_b"] == 0 and obs["b_beliefs_about_a"] == 1
    assert obs["recovery"] is True and obs["correct_cells"] == {"a": 20, "b": 20}
    assert obs["disputes"] == {"a": 0, "b": 2}
    assert obs == c["detail"]["expected"]  # == the frozen control, by X3's own pass
    # the dropped sentence is recorded verbatim in the artifact report
    drop = run["runs_drop_arm"]["e5.4-false-v1-drop"]
    assert drop["first_correct"]["by"] == "b"


def test_x4_seam_and_skip_record(run: dict) -> None:
    c = run["checks"][3]
    assert c["passed"]
    d = c["detail"]
    assert d["arm"] == {
        "codec": "canonical",
        "backend": "none",
        "note": d["arm"]["note"],
    }
    assert d["grammar_sha"].startswith("sha256:")
    assert (
        d["llm_seam"]["renderer"] == "llm:mock"
    )  # the typed seam over the shared Backend
    assert d["frozen_present"] is True, (
        "the official run requires the frozen derived constants"
    )


def test_x5_determinism(run: dict) -> None:
    c = run["checks"][4]
    assert c["passed"]
    # all six canonical runs re-ran bit-identically
    hashes = {k: v["determinism_hash"] for k, v in run["runs"].items()}
    assert len(hashes) == 6


def test_frozen_file_pins_the_matrix(run: dict) -> None:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        cand = base / "results" / "phase-5" / "e5.4-derived.json"
        if cand.exists():
            broken = json.loads(cand.read_text())
            break
    else:
        pytest.fail("e5.4-derived.json missing (the freeze must land with the build)")
    assert run["grammar_sha"] == broken["grammar_sha"]
    for k, h in broken["x1"]["run_hashes"].items():
        assert run["runs"][k]["determinism_hash"] == h, k


def test_experiment_class_full_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import os

    monkeypatch.setenv("KAINOS_RESULTS_DIR", str(tmp_path))
    r = E5_4Experiment().run()
    assert r.passed is True and r.value == 1.0 and CHECKS == 5
    assert r.config["arm"]["backend"] == "none"
    os.environ.pop("KAINOS_RESULTS_DIR", None)
