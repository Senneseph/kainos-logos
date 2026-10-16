"""T1 game kernel — spec (data, not code) and the shared-view model.

Per ``plan/10-architecture/multi-agent-games.md``: a game is
``GameSpec`` = players + a fact state + per-agent VIEWS (private/shared)
+ channel policy + round count + turn order. VIEW ISOLATION IS A
STRUCTURAL INVARIANT: the only path from world facts to an agent is
``views[agent]`` (enforced in :mod:`kainos.game.agent`; there is no API
surface that exposes another agent's private facts — pinned by
negative-control tests, E3.7 style).
"""

from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ["ChannelSpec", "GameSpec"]


@dataclass(frozen=True)
class ChannelSpec:
    """Channel policy.

    - ``budget_per_round``: max deltas a player may SEND per round
      (Say + Reveal combined). An action that would exceed the remaining
      budget is rejected whole (all-or-nothing, recorded in the
      transcript) — never partially delivered.
    - ``corruption``: probability in [0, 1] that a delivered fact-value
      assertion is replaced by a DIFFERENT value of the same domain (the
      lying/noisy-channel model). Applied deterministically through the
      game seed; every corruption is recorded with its original value.
      0.0 = honest channel (the E5.1/E5.2 baselines start there).
    """

    budget_per_round: int = 2
    corruption: float = 0.0

    def __post_init__(self) -> None:
        if self.budget_per_round < 0:
            raise ValueError("budget_per_round must be >= 0")
        if not 0.0 <= self.corruption <= 1.0:
            raise ValueError("corruption must be in [0, 1]")


@dataclass(frozen=True)
class GameSpec:
    """The whole game as data. New game = new spec; the kernel never
    changes (the multi-agent analog of the phase-4 ``PuzzleSpec``).

    - ``state``: every fact of the world, ``fact_id -> value``. Facts
      visible to no agent are ambient (legal; they simply never surface).
    - ``views``: ``player -> fact ids it may perceive``. The SHARED view
      is the intersection; everything else for a player is PRIVATE.
    """

    name: str
    players: tuple[str, ...]
    state: dict[str, str]
    views: dict[str, frozenset[str]]
    channel: ChannelSpec = field(default_factory=ChannelSpec)
    rounds: int = 3
    turn_order: tuple[str, ...] | None = None  # default: players in order
    #: Declared per-player perception distortions (episode data): the
    #: planted-wrong shared layer of E5.1 is EXACTLY this — a data-level
    #: declaration that player p perceives certain IN-VIEW facts with a
    #: value different from the world state. Scope is never affected
    #: (validation: overridden facts must be inside the player's view),
    #: so the structural view-isolation invariant is untouched.
    perception_overrides: dict[str, dict[str, str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.players:
            raise ValueError("a game needs at least one player")
        if len(set(self.players)) != len(self.players):
            raise ValueError("players must be distinct")
        if self.rounds < 1:
            raise ValueError("rounds must be >= 1")
        for p, v in self.views.items():
            if p not in self.players:
                raise ValueError(f"view for unknown player {p!r}")
            unknown = v - set(self.state)
            if unknown:
                raise ValueError(f"view of {p!r} references unknown facts: {sorted(unknown)}")
        missing = set(self.players) - set(self.views)
        if missing:
            raise ValueError(f"players without a view: {sorted(missing)}")
        for p, ov in self.perception_overrides.items():
            if p not in self.players:
                raise ValueError(f"perception override for unknown player {p!r}")
            outside = set(ov) - self.views[p]
            if outside:
                raise ValueError(
                    f"perception override of {p!r} reaches OUTSIDE its view "
                    f"{sorted(outside)} — scope is never a perception issue"
                )
            unknown_ov = set(ov) - set(self.state)
            if unknown_ov:
                raise ValueError(f"perception override of {p!r} names unknown facts: {sorted(unknown_ov)}")
        order = self.turn_order or self.players
        if sorted(order) != sorted(self.players):
            raise ValueError("turn_order must be a permutation of players")

    def turn(self) -> tuple[str, ...]:
        return self.turn_order or self.players

    def shared_view(self) -> frozenset[str]:
        """Facts every player can see (the shared layer)."""

        inter = frozenset(self.views[self.players[0]])
        for p in self.players[1:]:
            inter = inter & self.views[p]
        return inter

    def private_view(self, player: str) -> frozenset[str]:
        """Facts ONLY this player can see."""

        return self.views[player] - self.shared_view()
