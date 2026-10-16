"""CODEX data model (P0.02) — assertions, not facts (invariant #1).

Every :class:`Assertion` is a relation wrapped in the metadata that makes it
evaluable: provenance (MANDATORY — no bare-edge path, ADR-0008), context,
validity interval, confidence, epistemic status, and an optional EXCEPTION
marker. Contradicting assertions are preserved, never averaged (#6).

Contract: ``specs/codex.schema.json`` (``kainos/codex/1``) is the structural
mirror of these classes. The dataclasses are the implementation source of
truth; the JSON schema is the contract. Any field change is *breaking* and
requires a schema version bump + ADR.

Note on the directive's field list: `Assertion.provenance` and
`Provenance.source` are typed ``Optional`` (default ``None``) so the
"non-nullable" rules can be enforced in ``__post_init__`` as specified —
constructing without them raises ``TypeError``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

__all__ = [
    "Assertion",
    "Context",
    "EpistemicState",
    "ExceptionState",
    "Interval",
    "Provenance",
    "Source",
    "TermRef",
]


class EpistemicState(str, Enum):
    """An assertion's epistemic status (vocabulary in 00-CONTEXT.md)."""

    candidate = "candidate"
    established = "established"
    disputed = "disputed"
    obsolete = "obsolete"
    hypothesis = "hypothesis"
    ambiguous = "ambiguous"
    contradicted = "contradicted"
    inapplicable = "inapplicable"


class ExceptionState(str, Enum):
    """EXCEPTION boundary state (invariant #5: EXCEPTION != impossible)."""

    unseen = "unseen"
    unresolved = "unresolved"
    ambiguous = "ambiguous"
    conflicting = "conflicting"
    unverified = "unverified"
    requires_context = "requires_context"
    impossible = "impossible"


@dataclass(frozen=True)
class TermRef:
    """An independently addressable semantic node (invariant #4)."""

    id: str
    kind: str = "concept"
    labels: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"id": self.id, "kind": self.kind, "labels": list(self.labels)}

    @classmethod
    def from_dict(cls, d: dict) -> TermRef:
        return cls(id=d["id"], kind=d.get("kind", "concept"), labels=list(d.get("labels", ())))


@dataclass(frozen=True)
class Context:
    """Free-form, JSON-serializable context (relationships indexed by context)."""

    data: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return dict(self.data)

    @classmethod
    def from_dict(cls, d: dict | None) -> Context:
        return Context(data=dict(d or {}))


@dataclass(frozen=True)
class Interval:
    """Validity range; ``None`` bounds are open-ended. ISO-8601 date strings.

    The JSON key is ``"from"`` (schema contract); the Python attribute is
    ``from_`` because ``from`` is a reserved word.
    """

    from_: str | None = None
    to: str | None = None

    def to_dict(self) -> dict:
        return {"from": self.from_, "to": self.to}

    @classmethod
    def from_dict(cls, d: dict) -> Interval:
        return Interval(from_=d.get("from"), to=d.get("to"))


@dataclass(frozen=True)
class Source:
    """The origin an assertion was drawn from (never a bare edge, ADR-0008)."""

    uri: str
    media_type: str | None = None
    version: str | None = None
    hash: str | None = None
    retrieved_at: str | None = None
    authority: str | None = None

    def to_dict(self) -> dict:
        return {
            "uri": self.uri,
            "media_type": self.media_type,
            "version": self.version,
            "hash": self.hash,
            "retrieved_at": self.retrieved_at,
            "authority": self.authority,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Source:
        return cls(
            uri=d["uri"],
            media_type=d.get("media_type"),
            version=d.get("version"),
            hash=d.get("hash"),
            retrieved_at=d.get("retrieved_at"),
            authority=d.get("authority"),
        )


@dataclass(frozen=True)
class Provenance:
    """Mandatory wrapper: which source, who observed, what evidence backs it."""

    source: Source | None
    observer: str
    derived: bool = False
    verified: bool = False
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "source": self.source.to_dict() if self.source is not None else None,
            "observer": self.observer,
            "derived": self.derived,
            "verified": self.verified,
            "evidence": list(self.evidence),
        }

    @classmethod
    def from_dict(cls, d: dict) -> Provenance:
        src = d.get("source")
        return cls(
            source=Source.from_dict(src) if isinstance(src, dict) else src,
            observer=d["observer"],
            derived=d.get("derived", False),
            verified=d.get("verified", False),
            evidence=list(d.get("evidence", ())),
        )


@dataclass(frozen=True)
class Assertion:
    """The atomic CODEX unit: a relation wrapped in mandatory metadata (#1)."""

    id: str
    subject: TermRef
    relation: TermRef
    object: TermRef | str
    polarity: bool = True
    context: Context = field(default_factory=Context)
    validity: Interval | None = None
    confidence: float = 1.0
    status: EpistemicState = EpistemicState.candidate
    provenance: Provenance | None = None
    exception: ExceptionState | None = None

    def __post_init__(self) -> None:
        # Non-nullable (invariant #1): no bare-edge path (ADR-0008).
        if self.provenance is None:
            raise TypeError("Assertion.provenance is mandatory (no bare-edge path, ADR-0008)")
        if self.provenance.source is None:  # pyright: reportOptionalMemberAccess
            raise TypeError("Assertion.provenance.source is mandatory (ADR-0008)")
        # Confidence clamped to [0, 1].
        object.__setattr__(self, "confidence", max(0.0, min(1.0, float(self.confidence))))

    @property
    def object_id(self) -> str:
        """The object's term id whether it is a :class:`TermRef` or a raw string."""

        return self.object if isinstance(self.object, str) else self.object.id

    def to_dict(self) -> dict:
        """Deterministic (field-ordered) dict form; exact ``from_dict`` inverse."""

        return {
            "id": self.id,
            "subject": self.subject.to_dict(),
            "relation": self.relation.to_dict(),
            "object": self.object.to_dict() if isinstance(self.object, TermRef) else self.object,
            "polarity": self.polarity,
            "context": self.context.to_dict(),
            "validity": self.validity.to_dict() if self.validity is not None else None,
            "confidence": self.confidence,
            "status": self.status.value,
            "provenance": self.provenance.to_dict() if self.provenance is not None else None,
            "exception": self.exception.value if self.exception is not None else None,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Assertion:
        obj = d["object"]
        return cls(
            id=d["id"],
            subject=TermRef.from_dict(d["subject"]),
            relation=TermRef.from_dict(d["relation"]),
            object=obj if isinstance(obj, str) else TermRef.from_dict(obj),
            polarity=d.get("polarity", True),
            context=Context.from_dict(d.get("context")),
            validity=Interval.from_dict(d["validity"]) if d.get("validity") is not None else None,
            confidence=d.get("confidence", 1.0),
            status=EpistemicState(d.get("status", "candidate")),
            provenance=Provenance.from_dict(d["provenance"]) if d.get("provenance") is not None else None,
            exception=ExceptionState(d["exception"]) if d.get("exception") is not None else None,
        )
