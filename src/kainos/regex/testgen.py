"""Test generator (P1.06) — seeded, deterministic example generation.

`generate(node, seed)` returns (positives, negatives) for a **resolved** dialect
tree: positives are concrete strings the pattern's language must contain
(quantifiers expanded to a few in-bounds lengths); negatives each violate one
constraint (wrong literal, wrong class, out-of-range count, broken anchor,
extra suffix) by mutating exactly one element of an otherwise-valid example.
Same tree + same seed → same examples (determinism is the contract; the judge
is what makes them mean anything).
"""

from __future__ import annotations

import itertools
import random

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
    QuantKind,
    Repeat,
    Sequence,
    UnresolvedRef,
)

__all__ = ["generate"]

# Concrete representative characters per class (positives instantiate with these).
CLASS_CHAR: dict[ClassKind, str] = {
    ClassKind.digit: "0",
    ClassKind.letter: "a",
    ClassKind.word: "a",
    ClassKind.whitespace: " ",
    ClassKind.any: "x",
}

# A character that does NOT belong to the class (one-constraint-violation mutations).
WRONG_CLASS_CHAR: dict[ClassKind, str] = {
    ClassKind.digit: "a",
    ClassKind.letter: "0",
    ClassKind.whitespace: "a",
    ClassKind.word: " ",
    ClassKind.any: "a",  # unused: `any` matches everything — no class-violation exists
}

_NEG_CAP = 6
_SAMPLE_CAP = 8


_RAW_META = frozenset(".^$*+?()[]{}|\\")


def _raw_inert_flags(n: Node) -> list[bool]:
    """For every raw literal in the tree: True when its text is inert (no
    regex metacharacters — its language is exactly that string)."""

    flags: list[bool] = []

    def walk(x: Node) -> None:
        if isinstance(x, Literal) and x.raw:
            flags.append(all(c not in _RAW_META for c in x.text))
        if isinstance(x, Sequence):
            for el in x.elements:
                walk(el)
        elif isinstance(x, Alternative):
            for b in x.branches:
                walk(b)
        elif isinstance(x, (Repeat, Group)):
            walk(x.node)

    walk(n)
    return flags


def generate(node: Node, seed: int = 0) -> tuple[list[str], list[str]]:
    """(positive examples, negative examples) for a resolved tree. Deterministic
    under a fixed seed. Raises ValueError for trees still containing an
    UnresolvedRef — the pipeline must not test what it cannot justify.

    CODEX-taught (raw) fragments: an inert raw literal (no metacharacters)
    has the one-word language of its own text and is sampled as such; when
    the tree's raw fragments are all non-inert, no examples are synthesized
    — their language is owned by their provenance (the teaching), and the
    judge verdict is vacuous rather than misleading."""

    if _has_unresolved(node):
        raise ValueError("cannot generate examples for a tree with unresolved references")
    flags = _raw_inert_flags(node)
    if flags and not any(flags):
        return [], []
    rng = random.Random(seed)
    positives = _samples(node, "", rng, force=None)[:_SAMPLE_CAP]
    negatives = _negatives(node, positives, rng)
    return positives, negatives


def _has_unresolved(node: Node) -> bool:
    if isinstance(node, UnresolvedRef):
        return True
    if isinstance(node, Sequence):
        return any(_has_unresolved(el) for el in node.elements)
    if isinstance(node, Alternative):
        return any(_has_unresolved(b) for b in node.branches)
    if isinstance(node, (Repeat, Group)):
        return _has_unresolved(node.node)
    return False


def _counts(q: Quantifier) -> list[int]:
    """A few in-bounds copy counts to instantiate the quantifier."""

    match q.kind:
        case QuantKind.one_or_more:
            return [1, 2]
        case QuantKind.zero_or_more:
            return [0, 2]
        case QuantKind.optional:
            return [0, 1]
        case QuantKind.exactly:
            return [q.n or 0]
        case QuantKind.at_least:
            n = q.n or 0
            return [n, n + 1]
        case QuantKind.at_most:
            return [0, q.n or 0]
        case QuantKind.between:
            return [q.a or 0, q.b or 0]


def _samples(n: Node, path: str, rng: random.Random, force: dict[str, int] | None) -> list[str]:
    """Concrete strings this node's sub-pattern can produce (bounded)."""

    if isinstance(n, Literal):
        if n.raw:
            # A raw fragment: only inert ones (no regex metacharacters) have
            # a one-word language — exactly their text. Non-inert fragments
            # (e.g. a taught \\d{3}-\\d{3}-\\d{4}) synthesize no samples.
            meta = frozenset(".^$*+?()[]{}|\\")
            return [n.text] if all(c not in meta for c in n.text) else []
        return [n.text]
    if isinstance(n, Class):
        return [CLASS_CHAR[n.kind]]
    if isinstance(n, (Anchor, Flag)):
        return [""]  # zero-width
    if isinstance(n, Group):
        return _samples(n.node, f"{path}.0", rng, force)
    if isinstance(n, Alternative):
        out: list[str] = []
        for i, b in enumerate(n.branches):
            out.extend(_samples(b, f"{path}.{i}", rng, force)[:2])
        return _dedupe(out)
    if isinstance(n, Sequence):
        lists = [_samples(el, f"{path}.{i}", rng, force)[:2] for i, el in enumerate(n.elements)]
        if any(not ls for ls in lists):
            return []
        product = list(itertools.product(*lists))
        if len(product) > 4:
            product = rng.sample(product, 4)
        return _dedupe(["".join(p) for p in product])
    if isinstance(n, Repeat):
        child = _samples(n.node, f"{path}.0", rng, force)
        if not child:
            return []
        s = child[0]
        k = force.get(path) if force is not None else None
        counts = [k] if k is not None else _counts(n.quantifier)
        return [s * k for k in counts]
    raise ValueError(f"cannot sample node {type(n)!r}")


def _dedupe(items: list[str]) -> list[str]:
    out: list[str] = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


# ── negatives: violate exactly one constraint ──────────────────────────────


def _negatives(root: Node, positives: list[str], rng: random.Random) -> list[str]:
    negatives: list[str] = []

    def add(s: str) -> None:
        if s and s not in positives and s not in negatives and len(negatives) < _NEG_CAP:
            negatives.append(s)

    base = next((p for p in positives if p), positives[0] if positives else "")

    def swap_once(s: str, old: str, new: str) -> str | None:
        if not old or new == old:
            return None
        idx = s.find(old)
        return None if idx < 0 else s[:idx] + new + s[idx + len(old):]

    def other_char(c: str) -> str:
        return "a" if c != "a" else "0"

    def walk(n: Node, path: str) -> None:
        if isinstance(n, Literal) and n.text:
            mutated = swap_once(base, n.text[:1], other_char(n.text[:1]))
            if mutated:
                add(mutated)
        if isinstance(n, Class) and n.kind is not ClassKind.any:
            mutated = swap_once(base, CLASS_CHAR[n.kind], WRONG_CLASS_CHAR[n.kind])
            if mutated:
                add(mutated)
        if isinstance(n, Repeat):
            k_bad = _bad_count(n.quantifier)
            if k_bad is not None:
                forced = _samples(root, "", rng, force={path: k_bad})
                if forced:
                    add(forced[0])
        if isinstance(n, Anchor):
            # break the anchor: an anchor-anchored pattern must fail with a stray edge char.
            add("z" + base) if n.kind is AnchorKind.start else add(base + "z")
        for i, child in _children(n):
            walk(child, f"{path}.{i}")

    walk(root, "")

    if not negatives:
        if base and not _ends_wild(root):
            # No structural constraint found: an extra suffix must break full-match.
            add(base + "z")
        else:
            # No usable base (e.g. the only positives are empty): a single
            # wrong-class character violates any concrete class constraint.
            c = _first_class_excluding_any(root)
            if c is not None:
                add(WRONG_CLASS_CHAR[c])
    return negatives


def _first_class_excluding_any(n: Node) -> ClassKind | None:
    if isinstance(n, Class):
        return None if n.kind is ClassKind.any else n.kind
    if isinstance(n, Sequence):
        for el in n.elements:
            k = _first_class_excluding_any(el)
            if k is not None:
                return k
        return None
    if isinstance(n, Alternative):
        for b in n.branches:
            k = _first_class_excluding_any(b)
            if k is not None:
                return k
        return None
    if isinstance(n, (Repeat, Group)):
        return _first_class_excluding_any(n.node)
    return None


def _children(n: Node) -> list[tuple[str, Node]]:
    if isinstance(n, Sequence):
        return [(str(i), el) for i, el in enumerate(n.elements)]
    if isinstance(n, Alternative):
        return [(str(i), b) for i, b in enumerate(n.branches)]
    if isinstance(n, (Repeat, Group)):
        return [("0", n.node)]
    return []


def _bad_count(q: Quantifier) -> int | None:
    """An out-of-bounds copy count (None when the quantifier is unbounded)."""

    match q.kind:
        case QuantKind.exactly | QuantKind.at_most:
            return (q.n or 0) + 1
        case QuantKind.at_least:
            return max(0, (q.n or 0) - 1)
        case QuantKind.between:
            return (q.b or 0) + 1
        case QuantKind.one_or_more:
            return 0
        case _:
            return None


def _ends_wild(n: Node) -> bool:
    """True when the pattern's tail matches ANY extra suffix, so an
    'extra suffix' negative would actually (wrongly) match."""

    n = _tail(n)
    if isinstance(n, Class) and n.kind is ClassKind.any:
        return True
    if isinstance(n, Repeat):
        return (
            n.quantifier.kind in (QuantKind.one_or_more, QuantKind.zero_or_more)
            and _contains_any(n.node)
        )
    return False


def _tail(n: Node) -> Node:
    while True:
        if isinstance(n, Group):
            n = n.node
        elif isinstance(n, Sequence) and n.elements:
            n = n.elements[-1]
        else:
            return n


def _contains_any(n: Node) -> bool:
    if isinstance(n, Class):
        return n.kind is ClassKind.any
    if isinstance(n, Sequence):
        return any(_contains_any(el) for el in n.elements)
    if isinstance(n, Alternative):
        return any(_contains_any(b) for b in n.branches)
    if isinstance(n, (Repeat, Group)):
        return _contains_any(n.node)
    return False
