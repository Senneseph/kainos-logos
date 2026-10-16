"""T1 game kernel — the action contract.

Four actions, each gated by a DECLARED capability (P11 discipline:
capabilities are data the agent carries; an action requiring an
undeclared capability is rejected with a NAMED GAP and never executed —
the same honesty contract as E3.6's planner). Sharing in this kernel is
an EXPLICIT act (Reveal/Say over the channel), never a leak.

(Staging note, recorded on #161: T1 declares capabilities as a frozen
set on the agent; at T2/T3 — where game policy lives in the CODEX per
the spec's reuse plan — the ToM ablation becomes a one-line STORE
operation as the multi-agent spec prescribes.)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from kainos.exchange.protocol import AssertionDelta

__all__ = [
    "ALL_CAPABILITIES",
    "Action",
    "Commit",
    "Correct",
    "Pass",
    "Reveal",
    "Say",
    "capability_for",
]

#: The full capability set (the demo games start here; games may restrict).
ALL_CAPABILITIES: frozenset[str] = frozenset(
    {
        "send_message",
        "reveal_private",
        "commit",
        "pass",
        "assert_about_other",  # gate on Correct (the false-belief probe assertion)
    }
)


@dataclass(frozen=True)
class Say:
    """Send structured assertions. ``receiver`` = another player id, or
    ``"shared"`` for the shared scope (delivered to every other player).
    Payloads are step-19 ``AssertionDelta``s (schema-validated,
    provenance-carrying) — the exchange protocol IS the message medium."""

    receiver: str
    deltas: tuple[AssertionDelta, ...]


@dataclass(frozen=True)
class Reveal:
    """Explicitly make own PRIVATE facts public on the shared scope.
    Fact ids must be private to the acting agent (kernel-checked); the
    values travel as broadcast assertion deltas (same channel, same
    budget, same corruption semantics as Say)."""

    fact_ids: tuple[str, ...]


@dataclass(frozen=True)
class Correct:
    """An explicit correction assertion ABOUT another agent's model of a
    shared fact — the signature false-belief probe assertion ("your row 3
    is wrong: you read the door at c2, I read c4"). Carried as a
    self-sourced assertion delta (subject ``agent:<target>``, relation
    ``corrects``) so it rides the same attribution/budget/corruption
    machinery as all speech. Requires capability ``assert_about_other``
    — V0 (the ToM ablation) lacks the slot, so the kernel rejects a
    forced attempt with a NAMED GAP: the probe is structurally clean."""

    target: str
    fact_id: str
    deltas: tuple[AssertionDelta, ...]


@dataclass(frozen=True)
class Commit:
    """Bind an agent's final answer/stance. Multiple commits are legal;
    the LAST one wins and all are recorded in the transcript."""

    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Pass:
    """Take no action this turn (always allowed)."""


Action = Say | Reveal | Commit | Correct | Pass


def capability_for(action: Action) -> str:
    """The capability required to perform an action."""

    if isinstance(action, Say):
        return "send_message"
    if isinstance(action, Reveal):
        return "reveal_private"
    if isinstance(action, Correct):
        return "assert_about_other"
    if isinstance(action, Commit):
        return "commit"
    if isinstance(action, Pass):
        return "pass"
    raise TypeError(f"unknown action {action!r}")


def action_kind(action: Action) -> str:
    """Stable name for transcripts/reports."""

    return {Say: "say", Reveal: "reveal", Commit: "commit", Correct: "correct", Pass: "pass"}[type(action)]
