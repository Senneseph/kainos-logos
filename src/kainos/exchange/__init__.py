"""Distributed CODEX exchange (Phase 3, design: plan/10-architecture/distributed-codex.md).

The exchange unit is a **semantic transaction** (assertion + provenance +
node identity + timestamp), merge is **idempotent** and **conflict-
preserving** (both sides stay, flagged, never averaged), and a
contradiction is resolved into a **new context TERM** — not blended.
Scope: local two-node exchange only (no transport, per the design doc).
"""

from kainos.exchange.protocol import AssertionDelta, MergeReport, merge
from kainos.exchange.reconciler import (
    CANDIDATE_DIMENSIONS,
    CONTEXT_KIND,
    DECLARES_CONTEXT,
    Reconciliation,
    context_term_id,
    reconcile,
)

__all__ = [
    "CANDIDATE_DIMENSIONS",
    "CONTEXT_KIND",
    "DECLARES_CONTEXT",
    "AssertionDelta",
    "MergeReport",
    "Reconciliation",
    "context_term_id",
    "merge",
    "reconcile",
]
