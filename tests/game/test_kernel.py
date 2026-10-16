"""T1 kernel — scheduler: determinism, budget, corruption, and the
view-isolation negative control (E3.7 style: the leak CAN be detected)."""

from __future__ import annotations

import json

from kainos.game.actions import Pass, Say
from kainos.game.agent import Agent, fact_delta_for
from kainos.game.demo import _build_shared
from kainos.game.scheduler import Game
from kainos.game.spec import ChannelSpec, GameSpec

SPEC = GameSpec("t-kernel", ("a", "b"), {"fa": "1", "fb": "2", "fs": "s"},
                {"a": frozenset({"fa", "fs"}), "b": frozenset({"fb", "fs"})},
                ChannelSpec(budget_per_round=4, corruption=0.0),
                rounds=3)


def silent_game(budget: int = 4, corruption: float = 0.0) -> Game:
    spec = GameSpec(
        "t-kernel2", ("a", "b"), {"fa": "1", "fb": "2", "fs": "s"},
        {"a": frozenset({"fa", "fs"}), "b": frozenset({"fb", "fs"})},
        ChannelSpec(budget_per_round=budget, corruption=corruption),
        rounds=3,
    )
    agents = {p: Agent(p, spec, lambda view, r, t: Pass()) for p in spec.players}
    return Game(spec, agents, seed=7)


def test_two_identical_runs_are_bit_identical() -> None:
    r1 = _build_shared().run(write=False)
    r2 = _build_shared().run(write=False)
    assert r1 == r2
    assert r1["determinism_hash"] == r2["determinism_hash"]
    canonical = json.dumps(
        {k: v for k, v in r1.items() if k != "determinism_hash"}, indent=2, sort_keys=True, ensure_ascii=False
    )
    import hashlib

    assert r1["determinism_hash"] == "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()


def test_budget_is_all_or_nothing() -> None:
    """Two deltas when one remains in the round budget: the WHOLE action
    is rejected (no partial delivery), recorded as budget_reject."""

    def two_sends(view, round_no, transcript):
        if round_no != 1:
            return Pass()
        deltas = tuple(
            fact_delta_for("say", "a", "fa", view["fa"], 1, i, "t-kernel")
            for i in range(2)
        )
        return Say("shared", deltas)

    spec = GameSpec(
        "t-budget", ("a", "b"), {"fa": "1", "fb": "2"},
        {"a": frozenset({"fa"}), "b": frozenset({"fb"})},
        ChannelSpec(budget_per_round=1, corruption=0.0),
        rounds=2,
    )
    a = Agent("a", spec, two_sends)
    b = Agent("b", spec, lambda view, r, t: Pass())
    game = Game(spec, {"a": a, "b": b}, seed=1)
    report = game.run(write=False)
    rejects = [e for e in report["channel"]["events"] if e["kind"] == "budget_reject"]
    assert len(rejects) == 1 and rejects[0]["actor"] == "a"
    assert report["agents"]["a"]["rejections"] == []  # budget is a channel fact, not a policy rejection
    # nothing partial: b's inbox never received one of the two
    assert report["channel"]["sent_totals"]["a"] == 0


def test_corruption_is_seeded_and_recorded_with_originals() -> None:
    """corruption=1.0: every fact-value delta is replaced by a different
    value of the same domain, deterministically, with the original
    recorded (the transcript stays auditable)."""

    spec = GameSpec(
        "t-noise", ("a", "b"), {"fa": "1", "fb": "2"},
        {"a": frozenset({"fa"}), "b": frozenset({"fb"})},
        ChannelSpec(budget_per_round=4, corruption=1.0),
        rounds=2,
    )

    def noisemaker(p: str):
        key = "fa" if p == "a" else "fb"

        def step(view: dict[str, str], round_no: int, transcript: list) -> object:
            if round_no != 1:
                return Pass()
            return Say("shared", (fact_delta_for("say", p, key, view[key], 1, 0, "t-noise"),))

        return step

    mk = lambda: {p: Agent(p, spec, noisemaker(p)) for p in spec.players}
    r1 = Game(spec, mk(), seed=42).run(write=False)
    r2 = Game(spec, mk(), seed=42).run(write=False)
    assert r1 == r2, "same seed must give the same corruptions"
    events = [e for e in r1["channel"]["events"] if e["kind"] == "corruption"]
    assert events, "corruption=1.0 must corrupt every fact delta"
    for e in events:
        assert e["detail"]["original"].startswith("value=")
        assert e["detail"]["transmitted"] != e["detail"]["original"]


def test_leaky_agent_is_caught_by_the_negative_control() -> None:
    """The isolation check is not vacuous: an agent that leaks a hidden
    fact in perceive() is flagged in the report (E3.7 discipline)."""

    class LeakyAgent(Agent):
        def perceive(self) -> dict[str, str]:
            out = super().perceive()
            # the bug: a hidden (other) fact leaks into the visible slice
            hidden = [f for f in self._spec.state if f not in self._spec.views[self.player_id]]
            if hidden:
                out[hidden[0]] = self._spec.state[hidden[0]]
            return out

    spec = GameSpec(
        "t-leak", ("a", "b"), {"fa": "1", "fb": "2"},
        {"a": frozenset({"fa"}), "b": frozenset({"fb"})},
        ChannelSpec(budget_per_round=4), rounds=2,
    )
    agents = {p: (LeakyAgent(p, spec, lambda view, r, t: Pass()) if p == "a" else Agent(p, spec, lambda view, r, t: Pass())) for p in spec.players}
    report = Game(spec, agents, seed=1).run(write=False)
    assert report["negative_control"]["view_leaks"] == 2  # one per round, round 1 and 2
    assert report["negative_control"]["checked_turns"] == 4


def test_leak_count_is_zero_for_the_stock_kernel() -> None:
    for builder in (_build_shared(),):
        report = builder.run(write=False)
        assert report["negative_control"]["view_leaks"] == 0
        assert report["negative_control"]["checked_turns"] == 8


def test_unknown_receiver_is_recorded_not_fatal() -> None:
    def to_ghost(view, round_no, transcript):
        if round_no != 1:
            return Pass()
        return Say("ghost", (fact_delta_for("say", "a", "fa", view["fa"], 1, 0, "t-ghost"),))

    spec = GameSpec(
        "t-ghost", ("a", "b"), {"fa": "1", "fb": "2"},
        {"a": frozenset({"fa"}), "b": frozenset({"fb"})},
        ChannelSpec(budget_per_round=4), rounds=2,
    )
    a = Agent("a", spec, to_ghost)
    b = Agent("b", spec, lambda view, r, t: Pass())
    report = Game(spec, {"a": a, "b": b}, seed=1).run(write=False)
    ghost = [e for e in report["transcript"] if e.get("error", "").startswith("unknown receiver")]
    assert len(ghost) == 1 and ghost[0]["actor"] == "a"
    assert report["channel"]["bad_receivers"][0]["receiver"] == "ghost"


def test_silent_game_runs_and_hash_is_stable() -> None:
    r1 = silent_game().run(write=False)
    r2 = silent_game().run(write=False)
    assert r1["determinism_hash"] == r2["determinism_hash"]
    assert r1["scores"] == {"n_commits": 0}
