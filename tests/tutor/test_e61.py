"""E6.1 — the attended pilot, end-to-end.

Runs the frozen 30-turn script through the full Brainstem/InfantRuntime
(twice, byte-identity) and pins the FROZEN derived constants from
plan/30-phases/phase-6-tutor/experiments.md — this is the pre-registered
contract: the official run must reproduce these exactly.
"""

from __future__ import annotations

import pytest

from kainos.tutor.bench import CHECKS, FROZEN, run_e6_1


@pytest.fixture(scope="module")
def rep(tmp_path_factory):
    out = tmp_path_factory.mktemp("phase-6")
    return run_e6_1(out)


def test_eight_of_eight(rep):
    assert rep["checks_passed"] == CHECKS == 8
    assert all(c["pass"] for c in rep["checks"].values())
    # the failure detail must be empty too (pass with residue is not a pass)
    for name, c in rep["checks"].items():
        for key in ("violations", "replay_violations", "open_disputes_at_end", "duplicate_claimants", "fabrication_events", "unbacked_grounded"):
            if key in c:
                assert c[key] in ([], {}), (name, key, c[key])


def test_turn_count_is_frozen(rep):
    assert rep["checks"]["c1_contract_valid"]["turns_validated"] == FROZEN["turn_count"] == 30


def test_trajectory_matches_frozen_table(rep):
    assert rep["checks"]["c2_learning"]["trajectory"] == FROZEN["trajectory"]
    assert rep["checks"]["c2_learning"]["proof_events"] == 11


def test_conflict_pairs_are_the_frozen_pairs(rep):
    pairs = rep["checks"]["c4_correction_discipline"]["pairs"]
    assert [(p["superseded"], p["replacement"]) for p in pairs] == [
        ("cs-fS0204:2->5", "cs-fS0103:2->3"),
        ("cs-fS0403:3->9", "cs-fS0104:3->4"),
    ]
    assert rep["checks"]["c4_correction_discipline"]["open_disputes_at_end"] == []
    assert rep["checks"]["c4_correction_discipline"]["duplicate_claimants"] == {}


def test_honest_answers_are_frozen_words(rep):
    answers = rep["checks"]["c3_no_fabrication"]["s3_probe_answers"]
    assert answers["7 + 8 is what?"] == "needs_info: i cannot chain successor facts far enough for 7 + 8"
    assert answers["4 + 9 is what?"] == "needs_info: i cannot chain successor facts far enough for 4 + 9"
    assert answers["what comes after 40?"] == "needs_info: i have no established fact for what comes after 40"


def test_persistence_pairs_bit_equal(rep):
    pairs = rep["checks"]["c5_persistence"]["pairs"]
    assert all(p["bit_equal"] for p in pairs)
    assert pairs[0]["trace"] == ["cs-fS0103:2->3", "cs-fS0104:3->4", "cs-fS0105:4->5"]


def test_attention_is_exactly_the_frozen_event(rep):
    att = rep["checks"]["c7_determinism"]["attention"]
    assert len(att) == 1
    assert att[0]["turn"] == "S04:03" and att[0]["type"] == "repeated-conflict"
    assert rep["checks"]["c7_determinism"]["byte_identical_run1_run2"] is True
    assert rep["checks"]["c7_determinism"]["fabrication_events"] == []


def test_final_shape_constants(rep):
    d = rep["derived"]
    assert d["final_assertions"] == 45
    assert d["script_hash"] == "d3a409a8495dbfa9"
    assert [r["turns"] for r in d["per_session"]] == [14, 6, 6, 4]
    assert [r["codex_total"] for r in d["per_session"]] == [27, 34, 39, 45]
    assert [r["restored"] for r in d["per_session"]] == [False, True, True, True]


def test_seam_behaviour_is_frozen(rep):
    seam = rep["checks"]["c8_surface_arm"]["seam"]
    assert seam["llm_used_and_identical"] and seam["disagreement_falls_back_recorded"]
    assert seam["phrase_fallback_identical"] and seam["irs_identical_across_arms"]
    assert seam["fallback_events"] == 2 and seam["llm_events"] == 6
    # official arm is the deterministic one (no Ollama in the hermetic run)
    assert rep["checks"]["c8_surface_arm"]["official_arm"].startswith("det")
