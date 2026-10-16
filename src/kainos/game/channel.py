"""T1 game kernel — the scoped, budgeted, (optionally) corrupting channel.

Messages are step-19 ``AssertionDelta``s (idempotent merge semantics,
provenance mandatory). Delivery is synchronous but OBSERVATION is
deferred to the receiver's next round (round semantics: talk in round n
is seen at round n+1's observe step — no within-round ordering bias).
Corruption is deterministic (seeded) and fully recorded: what changed
from what. The channel never touches the players' CODEXes directly — it
only fills inboxes; the CODEX is each agent's own store.
"""

from __future__ import annotations

import dataclasses
import random
from dataclasses import dataclass

from kainos.codex.models import (
    Assertion,  # noqa: F401 (type clarity for _maybe_corrupt)
)
from kainos.exchange.protocol import AssertionDelta

__all__ = ["Channel", "ChannelEvent"]


@dataclass
class ChannelEvent:
    """One recorded channel event (budget rejection or corruption)."""

    kind: str  # "budget_reject" | "corruption"
    round: int
    actor: str
    detail: dict


class Channel:
    """The game's message medium (shared + private scopes).

    - budget: ``budget_per_round`` deltas per player per round (Say +
      Reveal combined); an action exceeding the remaining budget is
      rejected whole (all-or-nothing, recorded).
    - corruption: with probability ``corruption`` (applied DETERMINISTIC
      through the game seed), a delivered fact-value assertion's object
      is replaced by a different value of the same domain — the
      lying/noisy-channel model. Every corruption is recorded with its
      original value, so transcripts stay auditable.
    """

    def __init__(
        self,
        players: tuple[str, ...],
        budget_per_round: int,
        corruption: float,
        rng: random.Random,
        values: tuple[str, ...],
    ) -> None:
        self._inboxes: dict[str, list[AssertionDelta]] = {p: [] for p in players}
        self._sent_this_round: dict[str, int] = {p: 0 for p in players}
        self._totals: dict[str, int] = {p: 0 for p in players}
        self._budget = budget_per_round
        self._corruption = corruption
        self._rng = rng
        self._values = values
        self.events: list[ChannelEvent] = []

    # ── round bookkeeping ────────────────────────────────────────────────

    def new_round(self) -> None:
        """Start a fresh round: per-round send budgets reset."""

        for p in self._sent_this_round:
            self._sent_this_round[p] = 0

    def budget_left(self, player: str) -> int:
        return self._budget - self._sent_this_round[player]

    # ── delivery ─────────────────────────────────────────────────────────

    def deliver(self, round_no: int, sender: str, receiver: str, deltas: tuple[AssertionDelta, ...]) -> bool:
        """Deliver one action's deltas. Returns True on delivery; False
        (with a recorded ``budget_reject`` event) when the action would
        exceed the sender's remaining round budget — all-or-nothing."""

        n = len(deltas)
        if n > self.budget_left(sender):
            self.events.append(
                ChannelEvent(
                    "budget_reject",
                    round_no,
                    sender,
                    {"receiver": receiver, "attempted": n, "budget_left": self.budget_left(sender)},
                )
            )
            return False
        self._sent_this_round[sender] += n
        self._totals[sender] += n
        recipients = [p for p in self._inboxes if p != sender] if receiver == "shared" else [receiver]
        for r in recipients:
            for d in deltas:
                self._inboxes[r].append(self._maybe_corrupt(round_no, sender, d))
        return True

    def _maybe_corrupt(self, round_no: int, sender: str, d: AssertionDelta) -> AssertionDelta:
        a = d.assertion
        if (
            isinstance(a.object, str)
            and a.object in self._values
            and self._corruption > 0.0
            and self._rng.random() < self._corruption
        ):
            alternatives = sorted(v for v in self._values if v != a.object)
            if alternatives:
                tampered = self._rng.choice(alternatives)
                na = dataclasses.replace(a, object=tampered)
                self.events.append(
                    ChannelEvent(
                        "corruption",
                        round_no,
                        sender,
                        {"assertion": a.id, "original": a.object, "transmitted": tampered},
                    )
                )
                return AssertionDelta(assertion=na, node_id=d.node_id, timestamp=d.timestamp)
        return d

    def take_inbox(self, player: str) -> list[AssertionDelta]:
        """Drain one player's inbox (order-preserving)."""

        out = self._inboxes[player]
        self._inboxes[player] = []
        return out

    def sent_totals(self) -> dict[str, int]:
        return dict(self._totals)
