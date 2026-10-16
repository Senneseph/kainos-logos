"""Semantic IR models (P0.05) — thin constructs over the validated dict.

``specs/ir.schema.json`` (``kainos/ir/1``) is the source of truth; these
dataclasses are convenience constructors whose ``to_dict`` output is always
schema-valid. ``SemanticIR`` is a deliberately thin wrapper: validation lives
in :mod:`kainos.ir.codec`, and the wrapper's dict round-trips exactly
(``dump(load(x)) == x``).

``goals`` / ``events`` / ``hypotheses`` are free-form per the schema; the
:class:`Goal` / :class:`Hypothesis` classes are minimal conveniences for the
shapes Phase 1–2 actually emit, not extra constraints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "Constraint",
    "Entity",
    "Goal",
    "Hypothesis",
    "Relationship",
    "SemanticIR",
    "UnresolvedRef",
]


@dataclass(frozen=True)
class SemanticIR:
    """A validated IR dict (``kainos/ir/1``). The schema is the source of truth."""

    data: dict

    @property
    def kind(self) -> str:
        return self.data["kind"]

    def to_dict(self) -> dict:
        return self.data

    @classmethod
    def from_dict(cls, d: dict) -> SemanticIR:
        return cls(data=d)


@dataclass(frozen=True)
class Entity:
    id: str
    type: str | None = None
    labels: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"id": self.id}
        if self.type is not None:
            d["type"] = self.type
        d["labels"] = list(self.labels)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Entity:
        return cls(id=d["id"], type=d.get("type"), labels=list(d.get("labels", ())))


@dataclass(frozen=True)
class Relationship:
    subject: str
    relation: str
    object: str
    context: dict | None = None

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"subject": self.subject, "relation": self.relation, "object": self.object}
        if self.context is not None:
            d["context"] = dict(self.context)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Relationship:
        ctx = d.get("context")
        return cls(subject=d["subject"], relation=d["relation"], object=d["object"], context=dict(ctx) if ctx else None)


@dataclass(frozen=True)
class Constraint:
    kind: str
    value: Any = None

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"kind": self.kind}
        if self.value is not None:
            d["value"] = self.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Constraint:
        return cls(kind=d["kind"], value=d.get("value"))


@dataclass(frozen=True)
class UnresolvedRef:
    """How language signals "I can't commit to a meaning" — the bridge to EXCEPTION territory."""

    id: str
    surface: str
    candidates: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"id": self.id, "surface": self.surface, "candidates": list(self.candidates)}

    @classmethod
    def from_dict(cls, d: dict) -> UnresolvedRef:
        return cls(id=d["id"], surface=d["surface"], candidates=list(d.get("candidates", ())))


@dataclass(frozen=True)
class Goal:
    """Minimal convenience — ``goals[]`` is free-form per ``kainos/ir/1``."""

    id: str
    content: str

    def to_dict(self) -> dict:
        return {"id": self.id, "content": self.content}

    @classmethod
    def from_dict(cls, d: dict) -> Goal:
        return cls(id=d["id"], content=d["content"])


@dataclass(frozen=True)
class Hypothesis:
    """Minimal convenience — ``hypotheses[]`` is free-form per ``kainos/ir/1``."""

    id: str
    statement: str
    confidence: float | None = None

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"id": self.id, "statement": self.statement}
        if self.confidence is not None:
            d["confidence"] = self.confidence
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Hypothesis:
        return cls(id=d["id"], statement=d["statement"], confidence=d.get("confidence"))
