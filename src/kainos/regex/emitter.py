"""PCRE emitter (P1.02) — a dumb, deterministic rule-applier (spec §3, byte-exact).

Meaning lives in the CODEX (invariant #2); the emitter neither interprets nor
resolves. The one judgment call beyond the table: a `Repeat` whose child is a
multi-element `Sequence` wraps the body in `(?:…)` so the quantifier binds to the
whole sequence (without it, `Repeat(Sequence[a,b], one_or_more)` would emit `ab+`,
a different language). Everything else is the table, exactly.
`UnresolvedRef` has no PCRE — emitting one raises `UnresolvedError`; the resolver
(step 08) runs first and escalates rather than guessing.
"""

from __future__ import annotations

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

__all__ = ["UnresolvedError", "emit"]


class UnresolvedError(RuntimeError):
    """An UnresolvedRef reached the emitter. Never guess: resolve first (step 08)."""


_CLASS_OUTPUT: dict[ClassKind, str] = {
    ClassKind.digit: r"\d",
    ClassKind.letter: "[A-Za-z]",
    ClassKind.word: r"\w",
    ClassKind.whitespace: r"\s",
    ClassKind.any: ".",
}

_FLAG_CHARS: dict[str, str] = {"case_insensitive": "i"}

_METACHARS: frozenset[str] = frozenset(r"\.^$*+?()[]{}|")


def emit(node: Node) -> str:
    """Emit the PCRE for a dialect tree (raises UnresolvedError / ValueError on
    inputs with no faithful PCRE form)."""

    return _emit(node)


def _emit(n: Node) -> str:
    if isinstance(n, UnresolvedRef):
        candidates = ", ".join(n.candidates) or "none"
        raise UnresolvedError(
            f"cannot emit UnresolvedRef for {n.surface!r} — resolve it first (candidates: {candidates})"
        )
    if isinstance(n, Sequence):
        return "".join(_emit(el) for el in n.elements)  # concatenated, unwrapped (spec §3)
    if isinstance(n, Repeat):
        body = _emit(n.node)
        if isinstance(n.node, Sequence):
            body = f"(?:{body})"  # multi-element body: the quantifier must bind to the whole sequence
        return body + _quantifier(n.quantifier)
    if isinstance(n, Class):
        return _CLASS_OUTPUT[n.kind]
    if isinstance(n, Literal):
        if n.raw:
            # A raw literal is a regex fragment learned from the CODEX: pass
            # it through exactly as taught (no escaping).
            return n.text
        return "".join("\\" + c if c in _METACHARS else c for c in n.text)
    if isinstance(n, Anchor):
        return "^" if n.kind is AnchorKind.start else "$"
    if isinstance(n, Alternative):
        return "(?:" + "|".join(_emit(b) for b in n.branches) + ")"
    if isinstance(n, Group):
        return f"(?:{_emit(n.node)})"
    if isinstance(n, Flag):
        try:
            char = _FLAG_CHARS[n.name]
        except KeyError:
            raise ValueError(f"unknown flag {n.name!r} (known: {', '.join(sorted(_FLAG_CHARS))})") from None
        return f"(?{char})"
    raise TypeError(f"not a regex-dialect node: {type(n)!r}")


def _quantifier(q: Quantifier) -> str:
    match q.kind:
        case QuantKind.one_or_more:
            return "+"
        case QuantKind.zero_or_more:
            return "*"
        case QuantKind.optional:
            return "?"
        case QuantKind.exactly:
            return f"{{{q.n}}}"
        case QuantKind.at_least:
            return f"{{{q.n},}}"
        case QuantKind.at_most:
            return f"{{0,{q.n}}}"
        case QuantKind.between:
            return f"{{{q.a},{q.b}}}"
    raise AssertionError("unreachable quantifier kind")
