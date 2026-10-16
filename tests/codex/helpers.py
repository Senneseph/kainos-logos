"""Shared builders for CODEX tests (kept out of the test modules on purpose)."""

from __future__ import annotations

from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    ExceptionState,
    Interval,
    Provenance,
    Source,
    TermRef,
)


def make_term(term_id: str, kind: str = "concept", labels: list[str] | None = None) -> TermRef:
    return TermRef(id=term_id, kind=kind, labels=labels or [])


def make_source(uri: str = "https://example.org/facts/v1") -> Source:
    return Source(
        uri=uri,
        media_type="text/markdown",
        version="1",
        hash="sha256:deadbeef",
        retrieved_at="2026-08-20T00:00:00Z",
        authority="https://example.org",
    )


def make_provenance(
    uri: str = "https://example.org/facts/v1",
    observer: str = "tester",
    derived: bool = False,
    verified: bool = False,
    evidence: list[str] | None = None,
) -> Provenance:
    return Provenance(
        source=make_source(uri),
        observer=observer,
        derived=derived,
        verified=verified,
        evidence=evidence or [],
    )


def make_assertion(
    a_id: str,
    subject: str,
    relation: str,
    object: TermRef | str,
    polarity: bool = True,
    context: dict | None = None,
    validity: Interval | None = None,
    confidence: float = 1.0,
    status: EpistemicState = EpistemicState.candidate,
    provenance: Provenance | None = None,
    exception: ExceptionState | None = None,
) -> Assertion:
    return Assertion(
        id=a_id,
        subject=make_term(subject),
        relation=make_term(relation, kind="relation"),
        object=object,
        polarity=polarity,
        context=Context(data=context or {}),
        validity=validity,
        confidence=confidence,
        status=status,
        provenance=provenance if provenance is not None else make_provenance(),
        exception=exception,
    )


def full_assertion() -> Assertion:
    """An assertion exercising every field (used for round-trip + parity)."""

    return Assertion(
        id="a-full",
        subject=make_term("France", kind="entity", labels=["France", "French Republic"]),
        relation=make_term("CAPITAL_OF", kind="relation", labels=["capital of"]),
        object=make_term("Paris", kind="entity", labels=["Paris"]),
        polarity=False,
        context=Context(data={"domain": "geography", "country_code": "FR"}),
        validity=Interval(from_="2024-01-01", to="2025-01-01"),
        confidence=0.9,
        status=EpistemicState.established,
        provenance=make_provenance(derived=True, verified=True, evidence=["e-1"]),
        exception=ExceptionState.unverified,
    )
