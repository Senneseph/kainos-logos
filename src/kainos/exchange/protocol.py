"""Semantic-transaction exchange protocol for distributed CODEX (P3.06,
plan/10-architecture/distributed-codex.md).

Principles implemented here (see the design doc):

1. **The exchange unit is a semantic transaction, never a raw mutation:**
   an :class:`AssertionDelta` is an `Assertion` (with its mandatory
   provenance — ADR-0008) plus the sender's `node_id` and an ISO-8601
   `timestamp`. The wire shape is a documented JSON contract
   (`specs/assertion_delta.schema.json`) and every boundary (``from_dict``)
   validates against it, like the IR codec does for IR.
2. **Merge preserves conflict (invariant #6).** When an incoming assertion
   conflicts with what the target already holds (same subject + relation +
   aspect, different value), BOTH sides remain — flagged ``disputed`` with
   cross-linked evidence. Averaging/blending never happens: the merge only
   ever touches status/evidence, never ``object``/``polarity``.
3. **Merge is idempotent:** re-merging a delta whose assertion id the target
   already holds is a no-op (counted as a duplicate).

Scope guard (design doc): no transport, no replication protocol — two local
stores exchange deltas through this module; the protocol is the deliverable.
"""

from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]  # no py.typed shipped; stubs would need a lockfile pin (IR-codec pattern)

from kainos.codex.models import Assertion, EpistemicState, ExceptionState
from kainos.codex.store import CodexStore

__all__ = ["AssertionDelta", "MergeReport", "aspect_of", "conflict_pairs", "full_value", "merge", "schema_path"]

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "specs" / "assertion_delta.schema.json"


def schema_path() -> Path:
    return SCHEMA_PATH


_DELTA_VALIDATOR: Any = None


def _validator():
    """Draft 2020-12 validator for the delta contract (the boundary check of
    the IR-codec pattern). The contract is self-contained (house style:
    internal $refs only) — the assertion level mirrors ``kainos/codex/1``."""

    global _DELTA_VALIDATOR
    if _DELTA_VALIDATOR is None:
        _DELTA_VALIDATOR = jsonschema.Draft202012Validator(json.loads(SCHEMA_PATH.read_text()))
    return _DELTA_VALIDATOR


# ── the semantic transaction ────────────────────────────────────────────────


@dataclass(frozen=True)
class AssertionDelta:
    """One unit of exchange: an assertion + who said it + when (ISO-8601)."""

    assertion: Assertion
    node_id: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "assertion": self.assertion.to_dict(),
            "node_id": self.node_id,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> AssertionDelta:
        """Parse + validate against the JSON contract (boundary check, the
        IR-codec pattern). Raises ``ValueError`` on schema violation."""

        try:
            _validator().validate(d)
        except jsonschema.ValidationError as e:
            raise ValueError(f"AssertionDelta does not match the contract: {e.message}") from e
        return cls(
            assertion=Assertion.from_dict(d["assertion"]),
            node_id=d["node_id"],
            timestamp=d["timestamp"],
        )


# ── conflict semantics (mirrors the Phase 2 verification logic) ────────────


def aspect_of(a: Assertion) -> str:
    """The assertion's ASPECT: what two assertions are 'about' the same thing.

    - string object (property-style, ``"hibernates=yes"``): the key before ``=``;
    - term object: the term id (plus relation already scoped by the caller).

    Same aspect + different full value = a contradiction (X vs not-X).
    """

    if isinstance(a.object, str):
        return a.object.split("=", 1)[0] if "=" in a.object else a.object
    return a.object.id


def full_value(a: Assertion) -> str:
    """The assertion's full value: aspect + value + polarity (is_a-style
    polarity differences ARE value differences — a 'no' is the negation)."""

    base = a.object if isinstance(a.object, str) else a.object.id
    if a.relation.id == "is_a" and not isinstance(a.object, str):
        return base + (":yes" if a.polarity else ":no")
    if a.polarity is False:
        return base + ":no"
    return base


def conflict_pairs(a: Assertion, b: Assertion) -> bool:
    """True iff the two assertions are the same fact with different values
    (same subject, same relation, same aspect, different full value)."""

    if a.subject.id != b.subject.id or a.relation.id != b.relation.id:
        return False
    if aspect_of(a) != aspect_of(b):
        return False
    return full_value(a) != full_value(b)


# ── merge ──────────────────────────────────────────────────────────────────


@dataclass
class MergeReport:
    """What a merge did (evidence, P9): every delta resolved as exactly one of
    merged / duplicate / disputed; the disputed list names both sides."""

    node_ids: list[str] = field(default_factory=list)
    merged: list[str] = field(default_factory=list)  # ids added (new to the target)
    duplicates: list[str] = field(default_factory=list)  # ids already present (no-op)
    disputed: list[list[str]] = field(default_factory=list)  # [incoming, existing] pairs
    conflicts_preserved: int = 0  # sides of conflicts kept (both — never one)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_ids": list(self.node_ids),
            "merged": list(self.merged),
            "duplicates": list(self.duplicates),
            "disputed": [list(p) for p in self.disputed],
            "conflicts_preserved": self.conflicts_preserved,
        }


def merge(target: CodexStore, deltas: list[AssertionDelta]) -> MergeReport:
    """Merge semantic transactions into ``target`` (idempotent, conflict-preserving).

    Per delta, in order:
      - id already in target -> duplicate (no-op, the receiver's current state
        of that assertion wins — evidence already flowed);
      - conflicts with one or more stored siblings (same aspect) -> the
        incoming assertion is stored as ``disputed`` and EVERY conflicting
        sibling is set ``disputed`` with cross-linked evidence (invariant #6:
        both sides stay; the sender's status never overrides the receiver's
        store — each node derives its epistemic state from identical evidence);
      - otherwise -> added as-is (its status travels with the transaction).
    Only status/evidence are ever modified; objects and polarities are never
    touched (no averaging, invariant #6).
    """

    report = MergeReport()
    for delta in deltas:
        a = delta.assertion
        if delta.node_id not in report.node_ids:
            report.node_ids.append(delta.node_id)
        try:
            target.get(a.id)
        except KeyError:
            pass
        else:
            report.duplicates.append(a.id)
            continue

        siblings = target.query(subject=a.subject.id, relation=a.relation.id)
        # (the incoming assertion is not in the target yet)
        clashing = [s for s in siblings if aspect_of(s) == aspect_of(a) and full_value(s) != full_value(a)]
        if clashing:
            report.conflicts_preserved += 1 + len(clashing)
            incoming = dataclasses.replace(a, status=EpistemicState.disputed, exception=ExceptionState.conflicting)
            assert incoming.provenance is not None  # invariant #1: every assertion has provenance
            prov = dataclasses.replace(
                incoming.provenance,
                evidence=list(dict.fromkeys(list(incoming.provenance.evidence) + [c.id for c in clashing])),
            )
            incoming = dataclasses.replace(incoming, provenance=prov)
        else:
            incoming = a
        target.add(incoming)
        report.merged.append(a.id)
        for s in clashing:
            target.update_status(s.id, EpistemicState.disputed, evidence=[a.id])
            current = target.get(s.id)
            target.add(dataclasses.replace(current, exception=ExceptionState.conflicting))
            # ^ status + cross-linked evidence set by update_status; the
            #   exception mark matches the Phase 2 conflict semantics
            report.disputed.append([a.id, s.id])
    return report
