"""Deterministic kernel tests (P1.03) — every clause template + quantifier and
class surface maps to the expected AST node; the lexicon-reference semantics are
exercised with (and without) a seeded CODEX.
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.lang.deterministic import DeterministicKernel, parse_regex_text, tokenize
from kainos.lang.kernel import Interpretation, LanguageKernel
from kainos.regex.emitter import emit
from kainos.regex.ir import (
    Alternative,
    Anchor,
    AnchorKind,
    Class,
    ClassKind,
    Flag,
    Group,
    Literal,
    Quantifier,
    Repeat,
    Sequence,
    UnresolvedRef,
)
from kainos.regex.lexicon import seed


@pytest.fixture()
def codex() -> InMemoryCodexStore:
    store = InMemoryCodexStore()
    seed(store)
    return store


@pytest.fixture()
def kernel(codex) -> DeterministicKernel:
    return DeterministicKernel(codex)


# ── tokenizer ───────────────────────────────────────────────────────────────


def test_tokenize_is_lowercase_whitespace_insensitive():
    assert tokenize("Three  Digits, THEN a HYPHEN") == [
        "three",
        "digits",
        ",",
        "then",
        "a",
        "hyphen",
    ]


# ── anchors / flags / literals / groups ─────────────────────────────────────


@pytest.mark.parametrize("text", ["beginning of string", "start of string"])
def test_anchor_start_surfaces(text, kernel):
    assert _tree_of(kernel, text) == Anchor(kind=AnchorKind.start)


def test_anchor_end(kernel):
    assert _tree_of(kernel, "end of string") == Anchor(kind=AnchorKind.end)


def test_flag(kernel):
    assert _tree_of(kernel, "ignoring case") == Flag("case_insensitive")


def test_literal_capture(kernel):
    assert _tree_of(kernel, "the literal foo") == Literal("foo")
    assert _tree_of(kernel, "the literal foo bar") == Literal("foo bar")
    assert (
        _tree_of(kernel, "the literal foo, then a digit")
        == Sequence([Literal("foo"), Class(ClassKind.digit)])
    )


def test_group(kernel):
    assert _tree_of(kernel, "a group of three digits") == Group(
        node=Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.exactly(3))
    )
    assert _tree_of(kernel, "a group of a digit") == Group(node=Class(ClassKind.digit))


# ── classes ─────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("text", ["a digit", "digits", "letters", "word", "a space", "spaces", "whitespace", "any", "anything"])
def test_class_surfaces(text, kernel):
    kind = {
        "a digit": ClassKind.digit,
        "digits": ClassKind.digit,
        "letters": ClassKind.letter,
        "word": ClassKind.word,
        "a space": ClassKind.whitespace,
        "spaces": ClassKind.whitespace,
        "whitespace": ClassKind.whitespace,
        "any": ClassKind.any,
        "anything": ClassKind.any,
    }[text]
    assert _tree_of(kernel, text) == Class(kind=kind)


# ── quantifiers (all seven, all surface forms) ──────────────────────────────


@pytest.mark.parametrize(
    ("text", "kind", "quant"),
    [
        ("one or more digits", ClassKind.digit, Quantifier.one_or_more()),
        ("zero or more digits", ClassKind.digit, Quantifier.zero_or_more()),
        ("optional digits", ClassKind.digit, Quantifier.optional()),
        ("optionally a digit", ClassKind.digit, Quantifier.optional()),
        ("maybe a digit", ClassKind.digit, Quantifier.optional()),
        ("exactly 3 digits", ClassKind.digit, Quantifier.exactly(3)),
        ("three digits", ClassKind.digit, Quantifier.exactly(3)),
        ("3 digits", ClassKind.digit, Quantifier.exactly(3)),
        ("at least 2 digits", ClassKind.digit, Quantifier.at_least(2)),
        ("at most 5 letters", ClassKind.letter, Quantifier.at_most(5)),
        ("between 2 and 5 digits", ClassKind.digit, Quantifier.between(2, 5)),
        ("from 2 to 5 digits", ClassKind.digit, Quantifier.between(2, 5)),
    ],
    ids=["one or more digits", "zero or more digits", "optional digits", "optionally a digit",
         "maybe a digit", "exactly 3 digits", "three digits", "3 digits", "at least 2 digits",
         "at most 5 letters", "between 2 and 5 digits", "from 2 to 5 digits"],
)
def test_quantifier_surfaces(text, kind, quant, kernel):
    assert _tree_of(kernel, text) == Repeat(node=Class(kind=kind), quantifier=quant)


# ── number-surface disambiguation (spec §1) ─────────────────────────────────


def test_number_bare_is_digit_class(kernel):
    assert _tree_of(kernel, "a number") == Class(ClassKind.digit)
    assert _tree_of(kernel, "numbers") == Class(ClassKind.digit)


def test_number_followed_by_standalone_numeral_is_literal(kernel):
    assert _tree_of(kernel, "number 5") == Literal("5")


def test_number_followed_by_numeral_word_is_ambiguous(kernel):
    tree = _tree_of(kernel, "number one")
    assert tree == UnresolvedRef(surface="number one", candidates=["digit_class", "numeric_literal"])


# ── reference terms ─────────────────────────────────────────────────────────


@pytest.mark.parametrize("text", ["thing", "the thing", "it", "that"])
def test_reference_terms_become_unresolved_refs(text, kernel):
    tree = _tree_of(kernel, text)
    assert isinstance(tree, UnresolvedRef)
    assert tree.surface == ("thing" if "thing" in text else text)
    assert "digit_class" in tree.candidates and "numeric_literal" in tree.candidates


# ── connectors / alternatives ───────────────────────────────────────────────


def test_sequence_connectors(kernel):
    seq = _tree_of(kernel, "a digit, then a letter, and a word")
    assert seq == Sequence([Class(ClassKind.digit), Class(ClassKind.letter), Class(ClassKind.word)])
    seq2 = _tree_of(kernel, "a digit followed by a letter")
    assert seq2 == Sequence([Class(ClassKind.digit), Class(ClassKind.letter)])


def test_either_or(kernel):
    tree = _tree_of(kernel, "either a digit or a letter")
    assert tree == Alternative([Class(ClassKind.digit), Class(ClassKind.letter)])


def test_bare_or_chain(kernel):
    tree = _tree_of(kernel, "a digit or a letter or a word")
    assert tree == Alternative(
        [Class(ClassKind.digit), Class(ClassKind.letter), Class(ClassKind.word)]
    )


# ── lexicon-reference semantics (the hyphen test) ───────────────────────────


def test_hyphen_comes_from_the_codex_not_the_parser(codex):
    """'three digits, then a hyphen' → Sequence[Repeat(digit, exactly(3)), Literal("-", raw=True)]
    — and the Literal (raw: CODEX-taught, emitted verbatim) exists ONLY because the CODEX says hyphen realizes "-"."""

    with_codex = _tree_of(DeterministicKernel(codex), "three digits, then a hyphen")
    expected = Sequence(
        [
            Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.exactly(3)),
            Literal("-", raw=True),
        ]
    )
    assert with_codex == expected
    assert _tree_of(DeterministicKernel(codex), "three digits, then a hyphen") == expected

    # No codex: the same text must NOT invent "-". It stays unresolved.
    no_codex = _tree_of(DeterministicKernel(), "three digits, then a hyphen")
    assert no_codex == Sequence(
        [
            Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.exactly(3)),
            UnresolvedRef(surface="hyphen", candidates=[]),
        ]
    )


def test_lexicon_ambiguity_yields_unresolved_ref_with_candidates(codex):
    # A second, competing realization makes the hit ambiguous.
    from kainos.codex.models import Assertion, Provenance, Source, TermRef

    dup = Assertion(
        id="lexicon-hyphen-dup",
        subject=TermRef(id="hyphen", kind="entity", labels=["hyphen"]),
        relation=TermRef(id="realizes_as", kind="relation", labels=["realizes as"]),
        object="–",
        polarity=True,
        confidence=0.5,
        provenance=Provenance(source=Source(uri="test"), observer="test"),
    )
    codex.add(dup)
    tree = _tree_of(DeterministicKernel(codex), "a hyphen")
    assert tree == UnresolvedRef(surface="hyphen", candidates=["-", "–"])


# ── the kernel contract (parse/realize/propose) ─────────────────────────────


def test_kernel_is_a_language_kernel(kernel):
    assert isinstance(kernel, LanguageKernel)


def test_parse_returns_interpretations(kernel):
    interps = kernel.parse("a digit")
    assert len(interps) == 1
    interp = interps[0]
    assert isinstance(interp, Interpretation)
    assert interp.ir == Class(ClassKind.digit)
    assert interp.score == 1.0
    assert interp.unresolved == []


def test_parse_reports_unresolved_surfaces(kernel):
    interp = kernel.parse("a digit, the thing")[0]
    assert interp.unresolved == ["thing"]


def test_realize_is_the_emitter(kernel):
    tree = _tree_of(kernel, "three digits, then a hyphen")
    assert kernel.realize(tree) == emit(tree) == r"\d{3}-"


def test_propose_is_empty_for_now(kernel):
    assert kernel.propose(Class(ClassKind.digit)) == []


def test_full_sentence_parse_then_realize(kernel):
    """The NL form of the canonical example, end to end: parse → realize,
    byte-exact against the spec §3 golden output."""

    text = "ignoring case, three digits, a hyphen, either the literal foo or the literal bar"
    interp = kernel.parse(text)[0]
    assert interp.unresolved == []
    assert kernel.realize(interp.ir) == r"(?i)\d{3}-(?:foo|bar)"


def test_parse_to_generic_ir_round_trips(kernel):
    """Parsed trees are plain dialect trees: they survive the P1.01 generic
    mapping (a later step runs the full resolver on these)."""

    from kainos.regex.ir import from_ir, to_ir

    tree = _tree_of(kernel, "three digits, then a hyphen")
    assert from_ir(to_ir(tree)) == tree


# ── structural errors (the parser never guesses) ────────────────────────────


@pytest.mark.parametrize(
    "text",
    ["", "or", "a digit or", "either a digit", "the literal", "the",
    "a digit, then", "a digit and", "followed by", "exactly 3"],
    ids=["empty", "dangling-or", "trailing-or", "either-without-or", "dangling-literal",
         "dangling-article", "trailing-comma-then", "trailing-and", "leading-connector", "bare-quantifier"],
)
def test_structurally_unparseable_raises(kernel, text):
    with pytest.raises(ValueError):
        kernel.parse(text)


def test_parse_is_pure_text_to_ast(kernel):
    """Same text → same tree, every time (determinism is the phase-1 contract)."""

    text = "ignoring case, three digits, a hyphen"
    first = kernel.parse(text)[0].ir
    assert all(kernel.parse(text)[0].ir == first for _ in range(5))
    # And the parser module function with a fixed lookup is a pure function.
    a = parse_regex_text(text, lambda w: Literal("X") if w == "hyphen" else UnresolvedRef(w))
    b = parse_regex_text(text, lambda w: Literal("X") if w == "hyphen" else UnresolvedRef(w))
    assert a == b


def _tree_of(kernel: DeterministicKernel, text: str):
    return kernel.parse(text)[0].ir
