"""Contradiction -> missing dimension (P3.07, plan/10-architecture/distributed-codex.md).

The distributed form of the single-node Phase 2 mechanism
(`kainos.q20.learn.detect_dimension` — E2.5, ``dim:hibernates``): a
contradiction (``X`` vs ``not-X`` about the same thing) is evidence of a
MISSING context dimension, so the reconciler enumerates the candidate
dimensions — ``time, location, role, modality, context`` (the plan's fixed
list, in this order) — and asks: under which added dimension can both
sides be true?

Operational test for "D explains both sides of a conflicting group":

- specific D (``time`` / ``location`` / ``role`` / ``modality``): every pair
  of sides with DIFFERENT values must carry DIFFERENT ``D`` values in their
  context data (and the key must be present on both sides of each pair — an
  absent key does not distinguish);
- ``context`` (the catch-all candidate, tried LAST): the conflicting sides'
  context data differ in at least one key (there is some contextual fact
  separating them, even if un-named).

If a dimension explains the group, a NEW context TERM ``ctx:<D>:<subject>``
is created and declared as KNOWLEDGE (``<subject> --declares_context-->
ctx:D:subject`` — the term is addressable, never a code comment) and every
side is re-expressed under its own context (``context.data`` gains
``context_term`` + ``dimension``) with ``exception=requires_context``;
disputed sides are re-established — the contradiction is EXPLAINED, not
hidden (the E2.5 precedent). If NO candidate explains the group, the sides
are left ``disputed`` and nothing is invented.

**No averaging, ever:** the reconciler only touches ``context`` /
``status`` / ``exception``; objects and polarities are byte-preserved
(invariant #6).
"""

from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from typing import Any

from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    ExceptionState,
    Provenance,
    Source,
    TermRef,
)
from kainos.codex.store import CodexStore
from kainos.exchange.protocol import aspect_of, full_value

__all__ = [
    "CANDIDATE_DIMENSIONS",
    "CONTEXT_KIND",
    "DECLARES_CONTEXT",
    "Reconciliation",
    "context_term_id",
    "reconcile",
]

# The plan's fixed candidate list, tried in order; "context" is the
# catch-all and must be last (a specific dimension is a stronger finding).
CANDIDATE_DIMENSIONS: tuple[str, ...] = ("time", "location", "role", "modality", "context")

DECLARES_CONTEXT = "declares_context"
CONTEXT_KIND = "context"


def context_term_id(dimension: str, subject_id: str) -> str:
    return f"ctx:{dimension}:{subject_id}"


@dataclass
class Reconciliation:
    """The outcome of reconciling one (subject, relation) fact family.

    ``explained`` is True only when some candidate dimension separated the
    conflicting sides and the re-expression happened; otherwise the group is
    left exactly as found (disputed), which is an honest outcome (P8)."""

    subject: str
    relation: str
    explained: bool
    dimension: str | None = None
    term_id: str | None = None
    declaration_id: str | None = None
    reexpressed: list[str] = field(default_factory=list)
    disputed_before: int = 0
    disputed_after: int = 0
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "relation": self.relation,
            "explained": self.explained,
            "dimension": self.dimension,
            "term_id": self.term_id,
            "declaration_id": self.declaration_id,
            "reexpressed": list(self.reexpressed),
            "disputed_before": self.disputed_before,
            "disputed_after": self.disputed_after,
            "note": self.note,
        }


def _conflicting_group(store: CodexStore, subject: str, relation: str) -> list[Assertion]:
    """All assertions of (subject, relation) with a contested aspect: same
    aspect key, >= 2 distinct full values. Only epistemically live states
    count (candidate/established/disputed — the directive's 'conflicting
    established' includes the merge's output: a conflict that merge already
    flagged disputed is the same contradiction, now carrying the flag)."""

    by_aspect: dict[str, list[Assertion]] = {}
    for a in store.query(subject=subject, relation=relation):
        if a.status not in (EpistemicState.candidate, EpistemicState.established, EpistemicState.disputed):
            continue
        by_aspect.setdefault(aspect_of(a), []).append(a)
    best: list[Assertion] = []
    for group in by_aspect.values():
        if len({full_value(a) for a in group}) >= 2 and len(group) > len(best):
            best = group  # ALL instances of every value — each must be re-expressed
    return best


def _explained_by(sides: list[Assertion], dimension: str) -> bool:
    """Does ``dimension`` separate the sides? (See module docstring for the
    operational test.)"""

    if dimension == "context":
        # the catch-all: some contextual fact (any key) separates the sides
        sigs = {json.dumps(s.context.data, sort_keys=True) for s in sides}
        return len(sigs) >= 2
    for i in range(len(sides)):
        for j in range(i + 1, len(sides)):
            a, b = sides[i], sides[j]
            if full_value(a) == full_value(b):
                continue  # same value on both sides: D is not tested between them
            va = a.context.data.get(dimension)
            vb = b.context.data.get(dimension)
            if va is None or vb is None or va == vb:
                return False
    return True


def _declare_term(store: CodexStore, term: TermRef, decl_id: str, subject: TermRef) -> None:
    """Declare the context term as KNOWLEDGE: a first-class assertion, visible
    to the reasoner (the E2.5 ``declares_dimension`` pattern, generalized)."""

    if store.query(relation=DECLARES_CONTEXT, subject=subject.id, object=term.id):
        return
    prov = Provenance(
        source=Source(uri=f"reconciliation:{term.id}", version="1"),
        observer="reconciler",
        derived=True,
        verified=True,
    )
    store.add(
        Assertion(
            id=decl_id,
            subject=subject,
            relation=TermRef(id=DECLARES_CONTEXT, labels=["declares context"]),
            object=term,
            status=EpistemicState.established,
            provenance=prov,
        )
    )


def reconcile(store: CodexStore, subject: str, relation: str) -> Reconciliation:
    """Reconcile the (single) most-contested aspect of (subject, relation).

    Returns a :class:`Reconciliation`: either an explained group (new context
    TERM, both sides re-expressed and re-established) or an honest
    "unexplained" (sides left disputed, nothing invented).
    """

    sides = _conflicting_group(store, subject, relation)
    subject_term = TermRef(id=subject, labels=[subject])
    disputed_before = sum(1 for s in sides if s.status == EpistemicState.disputed)
    if not sides:
        return Reconciliation(subject=subject, relation=relation, explained=False, note="no conflicting group")

    dimension = next((d for d in CANDIDATE_DIMENSIONS if _explained_by(sides, d)), None)
    if dimension is None:
        return Reconciliation(
            subject=subject,
            relation=relation,
            explained=False,
            disputed_before=disputed_before,
            disputed_after=disputed_before,
            note="no candidate dimension explains both sides; the group stays disputed (nothing invented)",
        )

    term_idv = context_term_id(dimension, subject)
    term = TermRef(id=term_idv, labels=[f"{subject} ({dimension} context)"], kind=CONTEXT_KIND)
    decl_id = f"as_declares_context_{dimension}_{subject}"
    _declare_term(store, term, decl_id, subject_term)

    reexpressed: list[str] = []
    for s in sides:
        current = store.get(s.id)
        new_context = Context(
            data={**current.context.data, "context_term": term_idv, "dimension": dimension}
        )
        status = current.status
        if current.status == EpistemicState.disputed:
            status = EpistemicState.established  # explained, not hidden (E2.5 precedent)
        store.add(
            dataclasses.replace(current, context=new_context, status=status, exception=ExceptionState.requires_context)
        )
        reexpressed.append(s.id)

    live = [a for a in store.query(subject=subject, relation=relation) if a.status == EpistemicState.disputed]
    return Reconciliation(
        subject=subject,
        relation=relation,
        explained=True,
        dimension=dimension,
        term_id=term_idv,
        declaration_id=decl_id if store.query(relation=DECLARES_CONTEXT, subject=subject, object=term_idv) else None,
        reexpressed=reexpressed,
        disputed_before=disputed_before,
        disputed_after=len(live),
        note=f"dimension '{dimension}' explains all sides; term {term_idv} created; both sides retained under distinct contexts (no averaging)",
    )

