"""IR codec tests (P0.05): boundary validation, round-trips, schema sync, CWD independence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kainos.ir import codec
from kainos.ir.codec import dump, load, validate
from kainos.ir.models import (
    Constraint,
    Entity,
    Goal,
    Hypothesis,
    Relationship,
    SemanticIR,
    UnresolvedRef,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN = REPO_ROOT / "tests" / "ir" / "golden" / "minimal.json"

FULL_IR = {
    "kind": "query",
    "goals": [{"id": "g1", "content": "find the capital"}],
    "entities": [
        {"id": "e-france", "type": "country", "labels": ["France"]},
        {"id": "e-paris", "type": "city"},
    ],
    "relationships": [
        {"subject": "e-france", "relation": "CAPITAL_OF", "object": "e-paris", "context": {"domain": "geography"}}
    ],
    "events": [{"t": 1}],
    "constraints": [{"kind": "unique", "value": 1}, {"kind": "must_hold"}],
    "unresolved": [{"id": "u1", "surface": "the dash thing", "candidates": ["dash", "hyphen"]}],
    "hypotheses": [{"id": "h1", "statement": "maybe", "confidence": 0.5}],
    "meta": {"ir": "kainos/ir/1", "source": "test"},
}


# ── happy path ─────────────────────────────────────────────────────────────


def test_valid_sample_loads():
    ir = load(FULL_IR)
    assert ir.kind == "query"
    assert isinstance(ir, SemanticIR)


def test_minimal_golden_loads_and_round_trips():
    x = json.loads(GOLDEN.read_text())
    assert dump(load(x)) == x


def test_round_trip_full_fixture():
    assert dump(load(FULL_IR)) == FULL_IR


def test_load_wraps_a_copy():
    """The wrapper owns its dict: mutating the input after load must not leak."""

    src = {"kind": "state", "entities": [{"id": "a"}]}
    ir = load(src)
    src["kind"] = "pattern"
    src["entities"].append({"id": "late-arriver"})
    assert dump(ir) == {"kind": "state", "entities": [{"id": "a"}]}


# ── validation rejects malformed IR, with the schema path ─────────────────


def test_missing_kind_raises_with_path():
    bad = dict(FULL_IR)
    del bad["kind"]
    with pytest.raises(ValueError, match=r"^IR invalid at \$") as ei:
        validate(bad)
    assert "kind" in str(ei.value)


def test_unknown_kind_value_raises():
    with pytest.raises(ValueError, match=r"\$\.kind"):
        validate({"kind": "riddle"})


def test_entity_missing_id_raises_with_path():
    with pytest.raises(ValueError, match=r"\.entities\[0\]"):
        validate({"kind": "state", "entities": [{"type": "city"}]})


def test_relationship_missing_object_raises_with_path():
    with pytest.raises(ValueError, match=r"\.relationships\[0\]"):
        validate({"kind": "state", "relationships": [{"subject": "a", "relation": "R"}]})


def test_unresolved_missing_surface_raises():
    with pytest.raises(ValueError, match=r"\$\.unresolved"):
        validate({"kind": "state", "unresolved": [{"id": "u1"}]})


def test_constraint_without_kind_raises():
    with pytest.raises(ValueError, match=r"\$\.constraints\[0\]"):
        validate({"kind": "state", "constraints": [{"value": 1}]})


def test_closed_top_level_rejects_extra_keys():
    # additionalProperties violations are reported at the parent path with the key named
    with pytest.raises(ValueError, match=r"^IR invalid at \$") as ei:
        validate({"kind": "state", "bogus": True})
    assert "bogus" in str(ei.value)


def test_load_rejects_non_dict():
    with pytest.raises(ValueError, match=r"^IR invalid at \$"):
        validate(["not", "an", "object"])


# ── bundling / CWD independence ────────────────────────────────────────────


def test_bundled_schema_is_byte_identical_to_specs():
    bundled = Path(codec.__file__).resolve().parent / "_schemas" / "ir.schema.json"
    assert bundled.read_bytes() == (REPO_ROOT / "specs" / "ir.schema.json").read_bytes()


def test_validate_does_not_depend_on_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # a directory with no specs/ — must still work
    load(FULL_IR)
    with pytest.raises(ValueError):
        validate({"kind": "riddle"})


# ── thin model round-trips ─────────────────────────────────────────────────


@pytest.mark.parametrize(
    "obj",
    [
        Entity(id="e1", type="city", labels=["Paris"]),
        Entity(id="e2"),
        Relationship(subject="a", relation="R", object="b", context={"k": "v"}),
        Relationship(subject="a", relation="R", object="b"),
        Constraint(kind="unique", value=1),
        Constraint(kind="must_hold"),
        UnresolvedRef(id="u1", surface="the dash thing", candidates=["dash"]),
        UnresolvedRef(id="u2", surface="thing"),
        Goal(id="g1", content="find the capital"),
        Hypothesis(id="h1", statement="maybe", confidence=0.5),
        Hypothesis(id="h2", statement="plain"),
    ],
    ids=[
        "entity-full",
        "entity-minimal",
        "rel-with-context",
        "rel-minimal",
        "constraint-with-value",
        "constraint-minimal",
        "unresolved-with-candidates",
        "unresolved-minimal",
        "goal",
        "hypothesis-with-confidence",
        "hypothesis-minimal",
    ],
)
def test_model_round_trip(obj):
    assert type(obj).from_dict(obj.to_dict()) == obj


def test_model_to_dict_output_is_schema_valid():
    ir = {
        "kind": "state",
        "entities": [Entity(id="e1", type="city").to_dict()],
        "relationships": [Relationship(subject="e1", relation="R", object="e2").to_dict()],
        "constraints": [Constraint(kind="unique", value=1).to_dict()],
        "unresolved": [UnresolvedRef(id="u1", surface="x").to_dict()],
        "goals": [Goal(id="g1", content="c").to_dict()],
        "hypotheses": [Hypothesis(id="h1", statement="s", confidence=0.1).to_dict()],
    }
    validate(ir)  # every to_dict shape the models emit must be schema-valid
