"""Model tests (action-step 02 §6): round-trip, non-nullability, clamping, schema parity."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import pytest

from kainos.codex.models import (
    Assertion,
    EpistemicState,
    ExceptionState,
    Interval,
    TermRef,
)
from tests.codex.helpers import (
    full_assertion,
    make_assertion,
)

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "specs" / "codex.schema.json"

EXPECTED_KEY_ORDER = [
    "id",
    "subject",
    "relation",
    "object",
    "polarity",
    "context",
    "validity",
    "confidence",
    "status",
    "provenance",
    "exception",
]


@pytest.fixture(scope="module")
def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


# ── round trips ────────────────────────────────────────────────────────────


def test_roundtrip_full_assertion():
    a = full_assertion()
    assert Assertion.from_dict(a.to_dict()) == a


def test_roundtrip_minimal_assertion():
    a = make_assertion("a-min", "France", "CAPITAL_OF", "Paris")
    assert Assertion.from_dict(a.to_dict()) == a


def test_roundtrip_preserves_str_object_and_exceptions():
    a = make_assertion(
        "a-neg",
        "France",
        "CAPITAL_OF",
        "Paris",
        polarity=False,
        validity=Interval(from_="2024-01-01"),
        status=EpistemicState.disputed,
        exception=ExceptionState.conflicting,
    )
    assert Assertion.from_dict(a.to_dict()) == a


def test_to_dict_is_deterministic():
    a = full_assertion()
    d1, d2 = a.to_dict(), copy.deepcopy(a.to_dict())
    assert json.dumps(d1, sort_keys=False) == json.dumps(d2, sort_keys=False)
    assert list(d1.keys()) == EXPECTED_KEY_ORDER


# ── non-nullable provenance (invariant #1, ADR-0008) ───────────────────────


def test_missing_provenance_raises():
    # Constructed directly (not via the helper): None must be rejected by __post_init__.
    with pytest.raises(TypeError):
        Assertion(id="a-x", subject=TermRef(id="S"), relation=TermRef(id="R"), object="O", provenance=None)


def test_omitted_provenance_raises():
    with pytest.raises(TypeError):
        Assertion(id="a-x", subject=TermRef(id="S"), relation=TermRef(id="R"), object="O")


def test_missing_source_raises():
    from kainos.codex.models import Provenance

    with pytest.raises(TypeError):
        Assertion(
            id="a-x",
            subject=TermRef(id="S"),
            relation=TermRef(id="R"),
            object="O",
            provenance=Provenance(source=None, observer="observer"),
        )


def test_confidence_clamps_high():
    a = make_assertion("a-c1", "S", "R", "O", confidence=1.5)
    assert a.confidence == 1.0


def test_confidence_clamps_low():
    a = make_assertion("a-c2", "S", "R", "O", confidence=-0.5)
    assert a.confidence == 0.0


def test_confidence_survives_roundtrip_after_clamp():
    a = make_assertion("a-c3", "S", "R", "O", confidence=42)
    assert Assertion.from_dict(a.to_dict()) == a
    assert Assertion.from_dict(a.to_dict()).confidence == 1.0


# ── model ⇄ schema parity (G1) ─────────────────────────────────────────────


def _all_to_dict_fixtures() -> list[dict]:
    return [
        full_assertion().to_dict(),
        make_assertion("a-min", "France", "CAPITAL_OF", "Paris").to_dict(),
        make_assertion(
            "a-exc",
            "S",
            "R",
            "O",
            exception=ExceptionState.impossible,
            validity=Interval(from_="2024-01-01", to="2025-01-01"),
        ).to_dict(),
    ]


def test_every_to_dict_output_validates_against_schema(schema):
    for d in _all_to_dict_fixtures():
        jsonschema.validate(d, schema)  # raises on first violation


def test_schema_rejects_missing_provenance(schema):
    d = full_assertion().to_dict()
    del d["provenance"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(d, schema)


def test_schema_rejects_missing_source(schema):
    d = full_assertion().to_dict()
    d["provenance"]["source"] = None
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(d, schema)


def test_schema_rejects_unknown_status(schema):
    d = full_assertion().to_dict()
    d["status"] = "certain"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(d, schema)


def test_schema_rejects_out_of_range_confidence(schema):
    d = full_assertion().to_dict()
    d["confidence"] = 2.0
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(d, schema)


def test_schema_rejects_extra_fields(schema):
    d = full_assertion().to_dict()
    d["extra"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(d, schema)
