"""Response contracts: each of the seven kinds passes its exemplar IR and
fails a missing-field variant; unknown kinds pass through unconstrained."""

from __future__ import annotations

import pytest

from kainos.projection.contract import CONTRACTS, response_contract, validate_response

EXEMPLARS = {
    "request": {"plan": ["SEARCH_CODEX", "WRITE_TEXT"], "result": "regex emitted", "trace": ["step1"]},
    "question": {"answer": "yes", "evidence": ["as_a1"], "uncertainty_state": "established"},
    "command": {"action": "WRITE_TEXT", "resulting_state": ["artifact_available"]},
    "assertion": {"ack": True, "provenance": {"source": "games:g1"}, "epistemic_state": "established"},
    "correction": {"superseded": "hibernates=yes", "replacement": "hibernates=no"},
    "impossible": {"gap": "image_capability", "nearest_plan": ["SEARCH_CODEX", "WRITE_TEXT"]},
    "ambiguous": {"clarifying_question": "Which route?", "candidates": [["FETCH_TEXT"], ["SEARCH_CODEX", "WRITE_TEXT"]]},
}


@pytest.mark.parametrize("kind", sorted(CONTRACTS))
def test_exemplar_passes(kind):
    ok, violations = validate_response(EXEMPLARS[kind], kind)
    assert ok, violations


@pytest.mark.parametrize("kind", sorted(CONTRACTS))
def test_missing_field_fails(kind):
    ir = dict(EXEMPLARS[kind])
    key = next(iter(ir))
    del ir[key]
    ok, violations = validate_response(ir, kind)
    assert not ok
    assert any(key in v for v in violations)


def test_unknown_kind_is_pass_through():
    assert response_contract("freeform") is None
    ok, violations = validate_response({"anything": 1}, "freeform")
    assert ok and violations == []


def test_impossible_requires_gap_and_nearest_plan():
    ok, _ = validate_response({"gap": "image_capability", "nearest_plan": ["WRITE_TEXT"]}, "impossible")
    assert ok
    ok, _ = validate_response({"gap": "image_capability"}, "impossible")  # no nearest plan
    assert not ok


def test_ambiguous_caps_candidates_at_two():
    ir = {"clarifying_question": "Which?", "candidates": [1, 2, 3]}
    ok, violations = validate_response(ir, "ambiguous")
    assert not ok and any("1-2" in v for v in violations)


def test_correction_requires_both_distinct():
    ok, _ = validate_response({"superseded": "a=1", "replacement": "a=2"}, "correction")
    assert ok
    ok, violations = validate_response({"superseded": "a=1", "replacement": "a=1"}, "correction")
    assert not ok and any("differ" in v for v in violations)
    ok, _ = validate_response({"superseded": "a=1"}, "correction")
    assert not ok
