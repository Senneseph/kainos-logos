"""kainos.regex — the regex dialect: Semantic-IR AST, PCRE emitter, CODEX lexicon
(step 07), resolver (step 08)."""

from __future__ import annotations

from kainos.regex.emitter import UnresolvedError, emit
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

__all__ = [
    "DIALECT",
    "Alternative",
    "Anchor",
    "AnchorKind",
    "Class",
    "ClassKind",
    "Flag",
    "Group",
    "Literal",
    "Node",
    "QuantKind",
    "Quantifier",
    "Repeat",
    "Sequence",
    "UnresolvedError",
    "UnresolvedRef",
    "emit",
    "from_ir",
    "to_ir",
]
