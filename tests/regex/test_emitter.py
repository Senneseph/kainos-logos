"""PCRE emitter tests (P1.02) — every rule of the spec §3 table (byte-exact),
both canonical examples, UnresolvedRef rejection.
"""

from __future__ import annotations

from typing import Any

import pytest

from kainos.regex.emitter import UnresolvedError, emit
from kainos.regex.ir import (
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
    Repeat,
    Sequence,
    UnresolvedRef,
)

D = ClassKind.digit

CASES: list[tuple[str, Node, str]] = [
    # Sequence: concatenated, unwrapped (the corrected rule).
    ("sequence-concat", Sequence([Literal("a"), Literal("b"), Literal("c")]), "abc"),
    ("empty-sequence", Sequence([]), ""),
    # Repeat: all seven quantifiers.
    ("repeat-one-or-more", Repeat(Class(D), Quantifier.one_or_more()), r"\d+"),
    ("repeat-zero-or-more", Repeat(Class(D), Quantifier.zero_or_more()), r"\d*"),
    ("repeat-optional", Repeat(Class(D), Quantifier.optional()), r"\d?"),
    ("repeat-exactly", Repeat(Class(D), Quantifier.exactly(3)), r"\d{3}"),
    ("repeat-at-least", Repeat(Class(D), Quantifier.at_least(2)), r"\d{2,}"),
    ("repeat-at-most", Repeat(Class(D), Quantifier.at_most(4)), r"\d{0,4}"),
    ("repeat-between", Repeat(Class(D), Quantifier.between(2, 5)), r"\d{2,5}"),
    # Class: all five kinds.
    ("class-digit", Class(ClassKind.digit), r"\d"),
    ("class-letter", Class(ClassKind.letter), "[A-Za-z]"),
    ("class-word", Class(ClassKind.word), r"\w"),
    ("class-whitespace", Class(ClassKind.whitespace), r"\s"),
    ("class-any", Class(ClassKind.any), "."),
    # Literal: escaping, per the spec's metachar list — and only that list.
    (
        "literal-metachars-escaped",
        Literal(".^$*+?()[]{}|"),
        "".join("\\" + c for c in r".^$*+?()[]{}|"),
    ),
    ("literal-unmetached", Literal("ab-19"), "ab-19"),
    # Anchor.
    ("anchor-start", Anchor(AnchorKind.start), "^"),
    ("anchor-end", Anchor(AnchorKind.end), "$"),
    # Alternative / Group / Flag.
    ("alternative", Alternative([Literal("foo"), Literal("bar")]), "(?:foo|bar)"),
    ("alternative-nested", Alternative([Literal("a"), Alternative([Literal("b"), Literal("c")])]), "(?:a|(?:b|c))"),
    ("group-literal", Group(Literal("ab")), "(?:ab)"),
    ("group-sequence", Group(Sequence([Literal("a"), Literal("b")])), "(?:ab)"),
    ("flag", Flag("case_insensitive"), "(?i)"),
    # Wrap guard: a quantifier over a multi-element sequence groups its body.
    ("repeat-of-sequence-wraps", Repeat(Sequence([Literal("a"), Literal("b")]), Quantifier.one_or_more()), r"(?:ab)+"),
]


@pytest.mark.parametrize(("name", "node", "expected"), CASES, ids=[c[0] for c in CASES])
def test_emitter_table_is_byte_exact(name, node, expected):
    assert emit(node) == expected


# ── canonical examples (spec §3; byte-exact, become goldens) ────────────────


def test_canonical_1_cat_digits():
    tree = Sequence([Literal("cat"), Repeat(Class(D), Quantifier.one_or_more())])
    assert emit(tree) == r"cat\d+"


def test_canonical_2_case_insensitive_phone_like():
    tree = Sequence(
        [
            Flag("case_insensitive"),
            Repeat(Class(D), Quantifier.exactly(3)),
            Literal("-"),
            Alternative([Literal("foo"), Literal("bar")]),
        ]
    )
    assert emit(tree) == r"(?i)\d{3}-(?:foo|bar)"


# ── rejection: the emitter never guesses ────────────────────────────────────


@pytest.mark.parametrize(
    ("name", "node"),
    [
        ("unresolved-bare", UnresolvedRef(surface="hyphen", candidates=["-"])),
        ("unresolved-no-candidates", UnresolvedRef(surface="the thing")),
        (
            "unresolved-in-sequence",
            Sequence([Literal("x"), UnresolvedRef(surface="dash", candidates=["-", "–"])]),
        ),
        (
            "unresolved-in-alternative",
            Alternative([Literal("a"), UnresolvedRef(surface="b")]),
        ),
    ],
    ids=["bare", "no-candidates", "in-sequence", "in-alternative"],
)
def test_emitting_unresolved_ref_raises(name, node):
    with pytest.raises(UnresolvedError):
        emit(node)


def test_unresolved_error_names_the_surface_and_candidates():
    with pytest.raises(UnresolvedError, match="hyphen") as exc:
        emit(UnresolvedRef(surface="hyphen", candidates=["-", "–"]))
    assert "-, –" in str(exc.value)


def test_unknown_flag_raises():
    with pytest.raises(ValueError, match="unknown flag"):
        emit(Flag("unicode"))


def test_emitter_output_is_pure_function_of_ast():
    """Same AST → same bytes, every time (determinism is the contract)."""

    tree = Sequence(
        [
            Flag("case_insensitive"),
            Repeat(Class(D), Quantifier.exactly(3)),
            Literal("-"),
            Alternative([Literal("foo"), Literal("bar")]),
        ]
    )
    first: Any = emit(tree)
    assert all(emit(tree) == first for _ in range(5))
