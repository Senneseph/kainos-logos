"""kainos.game — multi-agent games over CODEX (Phase 5 / T1 kernel, T5 audit).

The kernel: view-isolated agents (the isolation is structural — an agent
can only PERCEIVE the facts of its own view), a budgeted/asserted
channel carrying :class:`~kainos.exchange.protocol.AssertionDelta`
messages, a deterministic round scheduler, and the ToM store-audit
harness (:func:`~kainos.game.audit.tom_audit`) that reads the agents'
CODEX stores white-box.

Design notes: ``plan/10-architecture/multi-agent-games.md``.
"""

from kainos.game.actions import Action, Commit, Pass, Reveal, Say, capability_for
from kainos.game.agent import (
    Agent,
    Rejection,
    StepFn,
    belief_assertion,
    fact_delta_for,
    fact_value,
)
from kainos.game.audit import AuditReport, beliefs_about, tom_audit
from kainos.game.channel import Channel, ChannelEvent
from kainos.game.demo import run_demo_games
from kainos.game.scheduler import Game
from kainos.game.spec import ChannelSpec, GameSpec

__all__ = [
    "Action",
    "Agent",
    "AuditReport",
    "Channel",
    "ChannelEvent",
    "ChannelSpec",
    "Commit",
    "Game",
    "GameSpec",
    "Pass",
    "Rejection",
    "Reveal",
    "Say",
    "StepFn",
    "belief_assertion",
    "beliefs_about",
    "capability_for",
    "fact_delta_for",
    "fact_value",
    "run_demo_games",
    "tom_audit",
]
