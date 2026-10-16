"""T1 kernel — spec validation (the game-as-data contract)."""

from __future__ import annotations

import pytest

from kainos.game.spec import ChannelSpec, GameSpec

BASE_STATE = {"f1": "x", "f2": "y", "f3": "z"}


def make_spec(**kw) -> GameSpec:
    views = kw.pop("views", {"a": frozenset({"f1", "f2"}), "b": frozenset({"f2", "f3"})})
    return GameSpec(
        name=kw.pop("name", "t-spec"),
        players=kw.pop("players", ("a", "b")),
        state=kw.pop("state", dict(BASE_STATE)),
        views=views,
        **kw,
    )


def test_valid_spec_round_trips() -> None:
    s = make_spec(rounds=4)
    assert s.turn() == ("a", "b")
    assert s.shared_view() == frozenset({"f2"})
    assert s.private_view("a") == frozenset({"f1"})
    assert s.private_view("b") == frozenset({"f3"})


def test_view_referencing_unknown_fact_rejected() -> None:
    with pytest.raises(ValueError, match="unknown facts"):
        make_spec(views={"a": frozenset({"f1", "nope"}), "b": frozenset({"f2"})})


def test_player_without_view_rejected() -> None:
    with pytest.raises(ValueError, match="without a view"):
        make_spec(views={"a": frozenset({"f1"})})


def test_turn_order_must_be_permutation() -> None:
    with pytest.raises(ValueError, match="permutation"):
        make_spec(turn_order=("a", "a"))
    s = make_spec(turn_order=("b", "a"))
    assert s.turn() == ("b", "a")


def test_channel_validation() -> None:
    with pytest.raises(ValueError, match="budget"):
        make_spec(channel=ChannelSpec(budget_per_round=-1))
    with pytest.raises(ValueError, match="corruption"):
        make_spec(channel=ChannelSpec(corruption=1.5))
    assert make_spec(channel=ChannelSpec(corruption=1.0)).channel.corruption == 1.0


def test_at_least_one_player_and_round() -> None:
    with pytest.raises(ValueError, match="at least one player"):
        make_spec(players=(), views={})
    with pytest.raises(ValueError, match="rounds"):
        make_spec(rounds=0)
