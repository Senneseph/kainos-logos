"""T1 kernel demos — the loop, proven end to end.

Two 2-player, 4-round scripted games over the shared kernel:

1. ``shared-view`` (the clean sharing case): disjoint private views +
   one shared fact; each agent shares its own cell (round 2), re-shares
   it (round 3 — exercises idempotent re-merge), then COMMITS the other
   agent's cell learned from the transcript (round 4). While learning,
   each stores a first-order belief about what the other said (the
   audited mental model). Expected: both commits correct, zero
   violations, zero view leaks, idempotent duplicates recorded.

2. ``contradiction-talk`` (the dispute probe): same grid, but agent b
   starts from a WRONG prior about a's cell, says it (round 2), learns
   the truth from a's honest share (round 3), and corrects itself
   publicly (round 3). Agent a's store must then hold BOTH the wrong
   and the right claim as a DISPUTED pair — cross-linked, never
   averaged (A5 at the social scale) — and a's audit must show the
   deception recorded (one incorrect belief) with zero violations
   (everything was backed by actual speech).

Both are deterministic (seed 1, fixed policies, no wall clock); the
official run writes ``results/phase-5/<game>.json``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from kainos.game.actions import Commit, Pass, Say
from kainos.game.agent import (
    Agent,
    StepFn,
    belief_assertion,
    fact_delta_for,
    fact_value,
)
from kainos.game.scheduler import Game
from kainos.game.spec import ChannelSpec, GameSpec

__all__ = ["CONTRADICTION_SPEC", "SHARED_SPEC", "run_demo_games"]

_STATE: dict[str, str] = {
    "s:shared_goal": "clear_the_ford",
    "pa:a_cell": "convoy_route_a",
    "pb:b_cell": "convoy_route_b",
}
_VIEWS: dict[str, frozenset[str]] = {
    "a": frozenset({"s:shared_goal", "pa:a_cell"}),
    "b": frozenset({"s:shared_goal", "pb:b_cell"}),
}
_CHANNEL = ChannelSpec(budget_per_round=2, corruption=0.0)

SHARED_SPEC = GameSpec("shared-view", ("a", "b"), dict(_STATE), dict(_VIEWS), _CHANNEL, rounds=4)

#: b's wrong prior in the contradiction game (the seeded false rumor).
_WRONG_PRIOR = "convoy_route_z"

CONTRADICTION_SPEC = GameSpec("contradiction-talk", ("a", "b"), dict(_STATE), dict(_VIEWS), _CHANNEL, rounds=4)


def _other_speech(agent: Agent, other: str) -> list:
    """Fact assertions in this agent's store that came from the other."""

    out = []
    for x in agent.codex.query():
        if x.subject.id.startswith("fact:") and x.relation.id == "is" and (
            x.provenance is not None and x.provenance.source is not None and x.provenance.source.uri == f"agent:{other}"
        ):
            out.append(x)
    return out


def _store_beliefs(agent: Agent, other: str) -> None:
    """First-order model maintenance: for every fact the other has
    asserted, keep a SUPPORTED belief assertion (self-derived, evidence =
    the received assertion's id). Already-stored beliefs are a no-op
    (deterministic ids). Beliefs keep the RAW value in ``fact:<id>=<v>``
    form — the agent's model of speech, distinct from the property-form
    world-model facts."""

    for x in _other_speech(agent, other):
        fid = x.subject.id[len("fact:") :]
        value = fact_value(x.object_id)
        if value is None:
            continue
        belief = belief_assertion(
            self_id=agent.player_id,
            other=other,
            fact_id=fid,
            value=value,
            source_uri=f"agent:{agent.player_id}",
            evidence=(x.id,),
        )
        try:
            agent.codex.get(belief.id)
        except KeyError:
            agent.remember(belief)


def _learned_value(agent: Agent, other: str, fact_id: str) -> str | None:
    """The value the other agent asserted for a fact (latest speech)."""

    values = [fact_value(x.object_id) for x in _other_speech(agent, other) if x.subject.id == f"fact:{fact_id}"]
    values = [v for v in values if v is not None]
    return values[-1] if values else None


def _make_shared_policy(agent_ref: Callable[[], Agent], player: str, other: str, my_fact: str, their_fact: str) -> StepFn:
    game_name = SHARED_SPEC.name

    def step(view: dict[str, str], round_no: int, transcript: list[dict[str, Any]]) -> Any:
        agent = agent_ref()
        _store_beliefs(agent, other)
        if round_no == 1:
            return Pass()
        if round_no in (2, 3):  # share (2) + re-share (3: idempotency check)
            delta = fact_delta_for("say", player, my_fact, view[my_fact], round_no, 0, game_name)
            return Say("shared", (delta,))
        value = _learned_value(agent, other, their_fact)
        if value is None:
            return Pass()  # honestly: cannot commit what one has not learned
        return Commit({"their_cell": value, "their_fact": their_fact})

    return step


def _make_contradiction_policy(
    agent_ref: Callable[[], Agent],
    player: str,
    other: str,
    my_fact: str,
    their_fact: str,
    game_name: str = CONTRADICTION_SPEC.name,
) -> StepFn:
    """b's script (player == 'b'): wrong prior at r2, correction + own
    share at r3, commit at r4. a's script (player == 'a'): honest share
    at r2, pass at r3 (absorbing b's wrong claim), commit at r4."""

    def step(view: dict[str, str], round_no: int, transcript: list[dict[str, Any]]) -> Any:
        agent = agent_ref()
        _store_beliefs(agent, other)
        if round_no == 1:
            return Pass()
        if round_no == 2:
            if player == "b":
                # the seeded false rumor about a's cell (an attributed,
                # checkable claim — the kernel records it, the store
                # preserves its later contradiction)
                delta = fact_delta_for("say", "b", "pa:a_cell", _WRONG_PRIOR, round_no, 0, game_name)
                return Say("shared", (delta,))
            return Say("shared", (fact_delta_for("say", "a", my_fact, view[my_fact], round_no, 0, game_name),))
        if round_no == 3:
            if player == "b":
                truth = _learned_value(agent, "a", "pa:a_cell")
                deltas = []
                if truth is not None and truth != _WRONG_PRIOR:
                    deltas.append(fact_delta_for("say", "b", "pa:a_cell", truth, round_no, 0, game_name))
                deltas.append(fact_delta_for("say", "b", my_fact, view[my_fact], round_no, 1, game_name))
                return Say("shared", tuple(deltas))
            return Pass()
        value = _learned_value(agent, other, their_fact)
        if value is None:
            return Pass()
        return Commit({"their_cell": value, "their_fact": their_fact})

    return step


def _score(commits: dict[str, dict[str, Any]], game: Game) -> dict[str, Any]:
    st = game.spec.state
    a = commits.get("a", {})
    b = commits.get("b", {})
    a_ok = a.get("their_cell") == st["pb:b_cell"] and a.get("their_fact") == "pb:b_cell"
    b_ok = b.get("their_cell") == st["pa:a_cell"] and b.get("their_fact") == "pa:a_cell"
    return {"a_correct": a_ok, "b_correct": b_ok, "score": 1.0 if (a_ok and b_ok) else 0.0}


def _build_shared() -> Game:
    spec = SHARED_SPEC
    holders: dict[str, Agent] = {}

    def mk(player: str, other: str, my_fact: str, their_fact: str) -> Agent:
        step = _make_shared_policy(lambda: holders[player], player, other, my_fact, their_fact)
        a = Agent(player, spec, step)
        holders[player] = a
        return a

    return Game(spec, {"a": mk("a", "b", "pa:a_cell", "pb:b_cell"), "b": mk("b", "a", "pb:b_cell", "pa:a_cell")}, seed=1, scorer=_score)


def _build_contradiction() -> Game:
    spec = CONTRADICTION_SPEC
    holders: dict[str, Agent] = {}

    def mk(player: str, other: str, my_fact: str, their_fact: str) -> Agent:
        step = _make_contradiction_policy(lambda: holders[player], player, other, my_fact, their_fact)
        a = Agent(player, spec, step)
        holders[player] = a
        return a

    return Game(spec, {"a": mk("a", "b", "pa:a_cell", "pb:b_cell"), "b": mk("b", "a", "pb:b_cell", "pa:a_cell")}, seed=1, scorer=_score)


def run_demo_games(out_dir: Any = None, write: bool = True) -> dict[str, dict[str, Any]]:
    """Run both kernel demos; with ``write`` their reports go to
    ``<results root>/phase-5/<game>.json`` (results-hygiene rule)."""

    reports: dict[str, dict[str, Any]] = {}
    for game in (_build_shared(), _build_contradiction()):
        reports[game.spec.name] = game.run(write=write, out_dir=out_dir)
    return reports
