"""Dialect IR tests (P1.01) — generic↔dialect round-trip losslessness.

The contract: `from_ir(to_ir(x)) == x` (structurally), the document is valid
generic IR (kainos/ir/1), ids are deterministic, and single-node to_generic()
matches the entity mapping.
"""

from __future__ import annotations

from typing import Any

import pytest

from kainos.ir.codec import validate
from kainos.regex.ir import (
    DIALECT,
    Alternative,
    Anchor,
    AnchorKind,
    Class,
    ClassKind,
    Flag,
    Group,
    Literal,
    Node,
    Quantifier,
    QuantKind,
    Repeat,
    Sequence,
    UnresolvedRef,
    from_ir,
    to_ir,
)

TREE: list[tuple[str, Node]] = [
    ("literal", Literal("cat")),
    ("literal-metachars", Literal("a.b*c|d")),
    ("class-digit", Class(ClassKind.digit)),
    ("class-any", Class(ClassKind.any)),
    ("anchor-start", Anchor(AnchorKind.start)),
    ("anchor-end", Anchor(AnchorKind.end)),
    ("flag", Flag("case_insensitive")),
    ("repeat-simple", Repeat(Class(ClassKind.word), Quantifier.one_or_more())),
    ("repeat-exactly", Repeat(Literal("ab"), Quantifier.exactly(3))),
    ("repeat-between", Repeat(Class(ClassKind.digit), Quantifier.between(2, 4))),
    (
        "canonical-1",
        Sequence([Literal("cat"), Repeat(Class(ClassKind.digit), Quantifier.one_or_more())]),
    ),
    (
        "canonical-2",
        Sequence(
            [
                Flag("case_insensitive"),
                Repeat(Class(ClassKind.digit), Quantifier.exactly(3)),
                Literal("-"),
                Alternative([Literal("foo"), Literal("bar")]),
            ]
        ),
    ),
    ("sequence-unwrapped", Sequence([Literal("a"), Literal("b"), Literal("c")])),
    ("alternative", Alternative([Literal("foo"), Alternative([Literal("x"), Literal("y")]), Literal("bar")])),
    ("group-sequence", Group(Sequence([Literal("a"), Literal("b")]))),
    ("unresolved", UnresolvedRef(surface="hyphen", candidates=["-", "–"])),
    ("unresolved-no-candidates", UnresolvedRef(surface="the thing")),
    (
        "unresolved-in-sequence",
        Sequence([Literal("x"), UnresolvedRef(surface="dash", candidates=["-"]), Class(ClassKind.digit)]),
    ),
    ("repeat-of-alternative", Repeat(Alternative([Literal("a"), Literal("b")]), Quantifier.at_least(2))),
    ("nested-groups", Group(Sequence([Group(Literal("ab")), Repeat(Class(ClassKind.digit), Quantifier.optional())]))),
]


@pytest.mark.parametrize(("name", "tree"), TREE, ids=[t[0] for t in TREE])
def test_dialect_generic_round_trip_is_lossless(name, tree):
    doc = to_ir(tree)
    back = from_ir(doc)
    # Structural equality (ids excluded from comparison); round trip is idempotent.
    assert back == tree
    assert to_ir(back) == doc  # deterministic: rebuilt tree re-serializes identically


@pytest.mark.parametrize(("name", "tree"), TREE, ids=[t[0] for t in TREE])
def test_document_is_valid_generic_ir(name, tree):
    doc = to_ir(tree)
    validate(doc)  # must not raise — the dialect maps onto the generic boundary
    assert doc["kind"] == "pattern"
    assert doc["meta"] == {"dialect": DIALECT}


def test_ids_are_deterministic_preorder():
    doc = to_ir(
        Sequence(
            [
                Literal("cat"),
                Repeat(Class(ClassKind.digit), Quantifier.one_or_more()),
                UnresolvedRef(surface="hyphen"),
            ]
        )
    )
    assert [e["id"] for e in doc["entities"]] == ["e0", "e1", "e2", "e3"]  # pre-order
    assert [u["id"] for u in doc["unresolved"]] == ["u0"]
    # Edges in deterministic emission order (children before parents at each
    # level; from_ir re-sorts Sequence edges by position). Repeat edge carries
    # the quantifier in context.
    assert doc["relationships"] == [
        {"subject": "e0", "relation": "sequence", "object": "e1", "context": {"position": 0}},
        {"subject": "e2", "relation": "repeat", "object": "e3", "context": {"kind": "one_or_more"}},
        {"subject": "e0", "relation": "sequence", "object": "e2", "context": {"position": 1}},
        {"subject": "e0", "relation": "sequence", "object": "u0", "context": {"position": 2}},
    ]


def test_single_node_to_generic_shapes():
    assert Literal("cat").to_generic("e0") == {"id": "e0", "type": "Literal", "labels": ["cat"]}
    assert Class(ClassKind.digit).to_generic("e1") == {"id": "e1", "type": "Class", "labels": ["digit"]}
    assert Anchor(AnchorKind.end).to_generic("e2") == {"id": "e2", "type": "Anchor", "labels": ["end"]}
    assert Flag("case_insensitive").to_generic("e3") == {"id": "e3", "type": "Flag", "labels": ["case_insensitive"]}
    assert Sequence([Literal("a")]).to_generic("e4") == {"id": "e4", "type": "Sequence"}
    assert Repeat(Literal("a"), Quantifier.optional()).to_generic("e5") == {"id": "e5", "type": "Repeat"}
    assert Alternative([Literal("a")]).to_generic("e6") == {"id": "e6", "type": "Alternative"}
    assert Group(Literal("a")).to_generic("e7") == {"id": "e7", "type": "Group"}
    assert UnresolvedRef("hyphen", ["-"]).to_generic("u0") == {"id": "u0", "surface": "hyphen", "candidates": ["-"]}
    # A bare node without an identity cannot name itself.
    with pytest.raises(ValueError, match="no id"):
        Literal("x").to_generic()
    # Identity set on the node is honored.
    assert Literal("x", id="e9").to_generic() == {"id": "e9", "type": "Literal", "labels": ["x"]}


def test_quantifier_dict_round_trip():
    cases = [
        Quantifier.one_or_more(),
        Quantifier.zero_or_more(),
        Quantifier.optional(),
        Quantifier.exactly(3),
        Quantifier.at_least(2),
        Quantifier.at_most(4),
        Quantifier.between(2, 5),
    ]
    for q in cases:
        assert Quantifier.from_dict(q.to_dict()) == q


def test_quantifier_kinds_are_the_spec_family():
    assert {k.value for k in QuantKind} == {
        "one_or_more",
        "zero_or_more",
        "optional",
        "exactly",
        "at_least",
        "at_most",
        "between",
    }


# ── from_ir rejection behavior ──────────────────────────────────────────────


def test_from_ir_empty_doc_is_invalid():
    with pytest.raises(ValueError, match="kainos/ir|invalid"):
        from_ir({})


def test_from_ir_rejects_non_pattern_kind():
    with pytest.raises(ValueError, match="not a pattern document"):
        from_ir({"kind": "state", "entities": [{"id": "e0", "type": "Literal", "labels": ["x"]}]})


def test_from_ir_rejects_dangling_object():
    doc = to_ir(Sequence([Literal("a"), Literal("b")]))
    doc["relationships"][0]["object"] = "ghost"
    with pytest.raises(ValueError, match="dangling relationship object"):
        from_ir(doc)


def test_from_ir_rejects_multiple_roots():
    doc = to_ir(Literal("a"))
    doc["entities"].append({"id": "e9", "type": "Literal", "labels": ["b"]})
    with pytest.raises(ValueError, match="exactly one root"):
        from_ir(doc)


def test_from_ir_rejects_unknown_type():
    doc: dict[str, Any] = {"kind": "pattern", "entities": [{"id": "e0", "type": "Wormhole"}]}
    with pytest.raises(ValueError, match="unknown dialect node type"):
        from_ir(doc)


def test_from_ir_rejects_cycle():
    # A cycle reachable from the root: e0 → e1 ⇄ e2.
    doc: dict[str, Any] = {
        "kind": "pattern",
        "entities": [
            {"id": "e0", "type": "Sequence"},
            {"id": "e1", "type": "Group"},
            {"id": "e2", "type": "Group"},
        ],
        "relationships": [
            {"subject": "e0", "relation": "sequence", "object": "e1", "context": {"position": 0}},
            {"subject": "e1", "relation": "group", "object": "e2"},
            {"subject": "e2", "relation": "group", "object": "e1"},
        ],
    }
    with pytest.raises(ValueError, match="cyclic dialect document"):
        from_ir(doc)


def test_from_ir_rejects_rootless_cycle():
    # A cycle with no entry point has zero roots — rejected before traversal.
    doc: dict[str, Any] = {
        "kind": "pattern",
        "entities": [
            {"id": "e0", "type": "Group"},
            {"id": "e1", "type": "Group"},
        ],
        "relationships": [
            {"subject": "e0", "relation": "group", "object": "e1"},
            {"subject": "e1", "relation": "group", "object": "e0"},
        ],
    }
    with pytest.raises(ValueError, match="exactly one root"):
        from_ir(doc)


def test_from_ir_rejects_bad_repeat_edges():
    doc: dict[str, Any] = {
        "kind": "pattern",
        "entities": [{"id": "e0", "type": "Repeat"}],
    }
    with pytest.raises(ValueError, match="exactly one repeat edge"):
        from_ir(doc)
