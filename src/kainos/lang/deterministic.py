"""Deterministic language kernel (P1.03) — restricted English → regex dialect AST.

A hand-written tokenizer + recursive-descent parser for the Phase 1 grammar
(`plan/30-phases/phase-1-regex/spec.md` §1 — the authoritative tables). The kernel
is the "language organ" (invariant #2): `text <-> IR` only, and it assigns **no
character values, ever**: class surfaces keep semantic class identity, and a bare
content word (`hyphen`, `dash`, …) is resolved at parse time by a **direct CODEX
lexicon lookup** (exact `realizes_as` hit → `Literal(realization)`; miss or
ambiguity → `UnresolvedRef`, which the step-08 resolver rotates or escalates).
"hyphen means `-`" lives in the CODEX (`kainos.regex.lexicon.seed`), not here.
"""

from __future__ import annotations

import re
from collections.abc import Callable

from kainos.codex.store import CodexStore
from kainos.lang.kernel import Interpretation
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
    Node,
    Quantifier,
    Repeat,
    Sequence,
    UnresolvedRef,
)

__all__ = ["DeterministicKernel", "parse_regex_text", "tokenize"]


# ── surfaces (spec §1) ──────────────────────────────────────────────────────

_NUM_WORDS: dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

_CLASS_SURFACES: dict[str, ClassKind] = {
    "digit": ClassKind.digit,
    "digits": ClassKind.digit,
    "letter": ClassKind.letter,
    "letters": ClassKind.letter,
    "word": ClassKind.word,
    "words": ClassKind.word,
    "whitespace": ClassKind.whitespace,
    "space": ClassKind.whitespace,
    "spaces": ClassKind.whitespace,
    "any": ClassKind.any,
    "anything": ClassKind.any,
}

_NUMBER_SURFACES: frozenset[str] = frozenset({"number", "numbers"})

_REFERENCE_SURFACES: frozenset[str] = frozenset({"thing", "it", "that"})
_REFERENCE_CANDIDATES: list[str] = ["digit_class", "numeric_literal"]

_CONNECTOR_TOKENS: frozenset[str] = frozenset({",", "then", "and", "or"})

_TOKEN_RE = re.compile(r"[a-z0-9]+|,|\S")


def tokenize(text: str) -> list[str]:
    """Lowercase, whitespace-insensitive: words, commas, and single other chars."""

    lowered = re.sub(r"\s+", " ", text.lower()).strip()
    return _TOKEN_RE.findall(lowered)


def _num(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    return _NUM_WORDS.get(token)


# ── recursive descent ───────────────────────────────────────────────────────
#
# expr   := seq (or seq)*                         # alternatives bind loosest
# seq    := atom (connector atom)*                # "," "then" "and" "followed by"
# atom   := anchor | flag | either … or | group of … | the literal … |
#           reference | (quant?) class | content-word (lexicon ref)


def parse_regex_text(text: str, lookup: Callable[[str], Node] | None = None) -> Node:
    """Parse a restricted-English regex description into a dialect tree.

    `lookup` resolves a bare content word to a node (the kernel supplies the
    CODEX lexicon lookup); `None` means "no lexicon available" — such words
    become `UnresolvedRef` with no candidates.

    Raises ValueError on structurally unparseable text (dangling connectors,
    trailing garbage) — the parser never guesses character values.
    """

    tokens = tokenize(text)
    if not tokens:
        raise ValueError("empty text")
    node, i = _expr(tokens, 0, lookup)
    if i != len(tokens):
        raise ValueError(f"unparsed trailing tokens: {' '.join(tokens[i:])!r}")
    return node


def _expr(tokens: list[str], i: int, lookup: Callable[[str], Node] | None) -> tuple[Node, int]:
    left, i = _seq(tokens, i, lookup)
    if i < len(tokens) and tokens[i] == "or":
        branches = [left]
        while i < len(tokens) and tokens[i] == "or":
            i += 1
            right, i = _seq(tokens, i, lookup)
            branches.append(right)
        if len(branches) == 1:  # "or" at the end
            raise ValueError("dangling 'or'")
        return Alternative(branches=branches), i
    return left, i


def _is_connector(tokens: list[str], i: int) -> bool:
    if i >= len(tokens):
        return False
    if tokens[i] in (",", "then", "and"):
        return True
    return tokens[i] == "followed" and i + 1 < len(tokens) and tokens[i + 1] == "by"


def _skip_connector(tokens: list[str], i: int) -> int:
    if tokens[i] == "followed":
        return i + 2
    return i + 1


def _seq(tokens: list[str], i: int, lookup: Callable[[str], Node] | None) -> tuple[Node, int]:
    first, i = _atom(tokens, i, lookup)
    elements: list[Node] = [first]
    while i < len(tokens) and _is_connector(tokens, i):
        # A run of connectors (", then") is one logical continuation.
        while i < len(tokens) and _is_connector(tokens, i):
            i = _skip_connector(tokens, i)
        if i >= len(tokens):
            raise ValueError("dangling connector at end of text")
        el, i = _atom(tokens, i, lookup)
        elements.append(el)
    if len(elements) == 1:
        return first, i
    return Sequence(elements=elements), i


def _atom(
    tokens: list[str], i: int, lookup: Callable[[str], Node] | None
) -> tuple[Node, int]:
    if i >= len(tokens):
        raise ValueError("unexpected end of text (dangling connector?)")
    t = tokens[i]

    # Structural tokens that cannot start an atom.
    if t in (",", "then", "and", "followed", "by"):
        raise ValueError(f"cannot parse: {t!r} cannot start a clause")
    if t == "or":
        raise ValueError("dangling 'or'")

    # Anchors.
    if t in ("beginning", "start") and _starts_with(tokens, i, (t, "of", "string")):
        return Anchor(kind=AnchorKind.start), i + 3
    if _starts_with(tokens, i, ("end", "of", "string")):
        return Anchor(kind=AnchorKind.end), i + 3

    # Flag.
    if _starts_with(tokens, i, ("ignoring", "case")):
        return Flag("case_insensitive"), i + 2

    # Either … or … (the whole alternative is the atom).
    if t == "either":
        node, j = _expr(tokens, i + 1, lookup)
        if not isinstance(node, Alternative):
            raise ValueError("'either' requires 'or'")
        return node, j

    # Articles introduce a clause.
    if t in ("a", "an", "the"):
        return _atom_after_article(tokens, i, lookup)

    # Quantifier (+ class) — an article may sit between the two ("maybe a digit").
    q, j = _quantifier(tokens, i)
    if q is not None and j < len(tokens) and tokens[j] in ("a", "an", "the"):
        j += 1
    cls, k = _class_surface(tokens, j)
    if q is not None and cls is None:
        raise ValueError(f"quantifier {q.to_dict()!r} has no class to apply to")
    if cls is not None:
        return (Repeat(node=cls, quantifier=q) if q is not None else cls), k

    # Bare class surface (no quantifier).
    cls, j = _class_surface(tokens, i)
    if cls is not None:
        return cls, j

    # Reference terms (bare).
    if t in _REFERENCE_SURFACES:
        return UnresolvedRef(surface=t, candidates=list(_REFERENCE_CANDIDATES)), i + 1

    # Vague reference with a content word: "<word> thing" (e.g. "the dash
    # thing") — the parser assigns no value; the candidate is the content word
    # so the resolver can rotate it in the CODEX.
    if i + 1 < len(tokens) and tokens[i + 1] == "thing":
        return UnresolvedRef(surface=f"{t} thing", candidates=[t]), i + 2

    # Content word: direct CODEX lexicon lookup (never a hard-coded value).
    # When the single word has no lexicon entry, try the maximal run of
    # content words as one reference phrase (e.g. "American phone number")
    # so the resolver can find a multi-word CODEX term.
    if lookup is not None:
        node = lookup(t)
        if not isinstance(node, UnresolvedRef):
            return node, i + 1
        j = i
        while j < len(tokens) and _is_content_word(tokens, j):
            j += 1
        if j > i + 1:
            phrase = " ".join(tokens[i:j])
            return UnresolvedRef(surface=phrase, candidates=[tokens[i], phrase]), j
    node = lookup(t) if lookup is not None else UnresolvedRef(surface=t, candidates=[])
    return node, i + 1


_RUN_STOP_WORDS = frozenset(
    {
        "a", "an", "the", "either", "or", "thing", "literal", "group",
        "optional", "optionally", "maybe", "exactly", "at", "least", "most",
        "between", "from", "to", "more", "beginning", "start", "end", "of",
        "string", "ignoring", "case", "followed", "by",
    }
    | set(_CLASS_SURFACES)
    | _REFERENCE_SURFACES
    | set(_NUM_WORDS)
    | set(_CONNECTOR_TOKENS)
)


def _number_disambiguated(tokens: list[str], i: int) -> bool:
    """True when the 'number' at i is the grammar's number surface ('number 5',
    'number one') rather than an ordinary noun ("phone number")."""

    nxt = i + 1
    return nxt < len(tokens) and (
        tokens[nxt].isdigit() or _NUM_WORDS.get(tokens[nxt]) is not None
    )


def _is_content_word(tokens: list[str], i: int) -> bool:
    """True when tokens[i] can extend a reference-phrase run. Anything the
    grammar itself parses (article, connector, anchor, flag, quantifier word,
    class surface, reference word, 'thing/it/that', literal/group, numeral,
    digit) stops the run — except 'number(s)' mid-phrase: it stops only when
    it is the grammar's disambiguated surface (followed by a numeral)."""

    t = tokens[i]
    if t in _RUN_STOP_WORDS or t.isdigit():
        return False
    if _is_connector(tokens, i):
        return False
    if t in _NUMBER_SURFACES:
        return not _number_disambiguated(tokens, i)
    return True


def _atom_after_article(
    tokens: list[str], i: int, lookup: Callable[[str], Node] | None
) -> tuple[Node, int]:
    article = tokens[i]
    j = i + 1
    if j >= len(tokens):
        raise ValueError(f"dangling article {article!r}")
    t = tokens[j]
    if article == "the" and t == "literal":
        return _literal_capture(tokens, j + 1)
    if t in _REFERENCE_SURFACES:
        return UnresolvedRef(surface=t, candidates=list(_REFERENCE_CANDIDATES)), j + 1
    if t == "group" and j + 1 < len(tokens) and tokens[j + 1] == "of":
        node, k = _expr(tokens, j + 2, lookup)
        return Group(node=node), k
    # "a/an" + clause: skip the article, parse the clause.
    return _atom(tokens, j, lookup)


def _literal_capture(tokens: list[str], i: int) -> tuple[Node, int]:
    """'the literal <text>' — <text> runs to the next connector or end of text."""

    start = i
    while i < len(tokens) and tokens[i] not in _CONNECTOR_TOKENS and not _is_connector(tokens, i):
        i += 1
    if i == start:
        raise ValueError("dangling 'the literal' (no text)")
    text = " ".join(tokens[start:i])
    return Literal(text=text), i


def _starts_with(tokens: list[str], i: int, prefix: tuple[str, ...]) -> bool:
    return tuple(tokens[i : i + len(prefix)]) == prefix


def _quantifier(tokens: list[str], i: int) -> tuple[Quantifier | None, int]:
    if _starts_with(tokens, i, ("one", "or", "more")):
        return Quantifier.one_or_more(), i + 3
    if _starts_with(tokens, i, ("zero", "or", "more")):
        return Quantifier.zero_or_more(), i + 3
    if tokens[i] in ("optional", "optionally", "maybe"):
        return Quantifier.optional(), i + 1
    if tokens[i] == "exactly" and (n := _num(tokens[i + 1] if i + 1 < len(tokens) else "")) is not None:
        return Quantifier.exactly(n), i + 2
    if _starts_with(tokens, i, ("at", "least")):
        n = _num(tokens[i + 2]) if i + 2 < len(tokens) else None
        if n is not None:
            return Quantifier.at_least(n), i + 3
    if _starts_with(tokens, i, ("at", "most")):
        n = _num(tokens[i + 2]) if i + 2 < len(tokens) else None
        if n is not None:
            return Quantifier.at_most(n), i + 3
    if tokens[i] == "between" and i + 3 < len(tokens) and tokens[i + 2] == "and":
        a, b = _num(tokens[i + 1]), _num(tokens[i + 3])
        if a is not None and b is not None:
            return Quantifier.between(a, b), i + 4
    if tokens[i] == "from" and i + 3 < len(tokens) and tokens[i + 2] == "to":
        a, b = _num(tokens[i + 1]), _num(tokens[i + 3])
        if a is not None and b is not None:
            return Quantifier.between(a, b), i + 4
    # Bare numeral → exactly(n)  ("three digits", "3 digits") — spec §1.
    n = _num(tokens[i])
    if n is not None:
        return Quantifier.exactly(n), i + 1
    return None, i


def _class_surface(tokens: list[str], i: int) -> tuple[Node | None, int]:
    """A class surface at tokens[i] (after any already-consumed article). Returns
    (None, i) when it is not one. 'number(s)' gets the spec disambiguation."""

    if i >= len(tokens):
        return None, i
    t = tokens[i]
    if t in _NUMBER_SURFACES:
        nxt = i + 1
        if nxt < len(tokens):
            if tokens[nxt].isdigit():
                # "number 5" — a standalone numeral: the literal value.
                return Literal(text=tokens[nxt]), nxt + 1
            num_word = _NUM_WORDS.get(tokens[nxt])
            if num_word is not None:
                # "number one" — both readings live → genuinely ambiguous.
                return UnresolvedRef(
                    surface=f"{t} {tokens[nxt]}",
                    candidates=list(_REFERENCE_CANDIDATES),
                ), nxt + 1
        return Class(kind=ClassKind.digit), i + 1
    if t in _CLASS_SURFACES:
        return Class(kind=_CLASS_SURFACES[t]), i + 1
    return None, i


# ── the kernel ──────────────────────────────────────────────────────────────


def _unresolved_surfaces(node: Node) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()

    def walk(n: Node) -> None:
        if isinstance(n, UnresolvedRef) and n.surface not in seen:
            seen.add(n.surface)
            out.append(n.surface)
        if isinstance(n, Sequence):
            for el in n.elements:
                walk(el)
        elif isinstance(n, Alternative):
            for b in n.branches:
                walk(b)
        elif isinstance(n, (Repeat, Group)):
            walk(n.node)

    walk(node)
    return out


class DeterministicKernel:
    """Phase 1 language kernel: restricted English <-> regex dialect AST.

    With a `codex`, bare content words resolve through the seeded lexicon
    (`kainos.regex.lexicon.seed`) at parse time; without one they stay
    `UnresolvedRef`. The parser itself contains no character values.
    """

    def __init__(self, codex: CodexStore | None = None) -> None:
        self._codex = codex

    def _lookup(self, word: str) -> Node:
        assert self._codex is not None  # only called when a codex is present
        hits = self._codex.query(subject=word, relation="realizes_as")
        realizations = sorted({a.object_id for a in hits})
        if len(realizations) == 1:
            # A CODEX realization is a taught regex fragment (raw), not
            # literal text — the emitter must not escape it.
            return Literal(text=realizations[0], raw=True)
        if len(realizations) > 1:  # ambiguous hit → let the resolver rotate
            return UnresolvedRef(surface=word, candidates=realizations)
        return UnresolvedRef(surface=word, candidates=[])  # miss → resolver / escalation

    # -- LanguageKernel protocol -------------------------------------------

    def parse(self, text: str, context: dict | None = None) -> list[Interpretation]:
        """One deterministic reading (score 1.0); raises ValueError when the text
        is structurally unparseable."""

        tree = parse_regex_text(text, self._lookup if self._codex is not None else None)
        return [Interpretation(ir=tree, score=1.0, unresolved=_unresolved_surfaces(tree))]

    def realize(self, ir: object, style: str | None = None) -> str:
        """Deterministic realization: the step-06 PCRE emitter (the `style` hook
        is reserved for later surfaces)."""

        if not isinstance(ir, Node):
            raise TypeError(f"realize() expects a regex dialect Node, got {type(ir)!r}")
        return emit(ir)

    def propose(self, ir: object) -> list[dict]:
        """No proposals yet — the step-08 reasoner proposes; this contract slot
        stays empty on purpose."""
        return []
