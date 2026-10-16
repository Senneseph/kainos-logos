"""T1 kernel — the agent: structural view isolation, capability gating,
speech attribution, and self-sourced storage."""

from __future__ import annotations

from kainos.codex.models import Assertion, Provenance, Source, TermRef
from kainos.game.actions import (
    ALL_CAPABILITIES,
    Commit,
    Pass,
    Reveal,
    Say,
    capability_for,
)
from kainos.game.agent import Agent, fact_delta_for
from kainos.game.spec import ChannelSpec, GameSpec

SPEC = GameSpec("t-agent", ("a", "b"), {"fa": "1", "fb": "2", "fs": "s"},
                {"a": frozenset({"fa", "fs"}), "b": frozenset({"fb", "fs"})},
                ChannelSpec(budget_per_round=4, corruption=0.0),
                rounds=3)


def agent(player: str = "a", caps: frozenset[str] | None = None, step=None) -> Agent:
    return Agent(player, SPEC, step or (lambda view, r, t: Pass()), capabilities=caps or ALL_CAPABILITIES)


# ── structural view isolation ─────────────────────────────────────────


def test_perceive_returns_exactly_the_visible_slice() -> None:
    a = agent()
    assert a.perceive() == {"fa": "1", "fs": "s"}
    a_b = agent("b")
    assert a_b.perceive() == {"fb": "2", "fs": "s"}
    # the private fact is absent from the OTHER agent's world surface
    assert "fb" not in a.perceive()
    assert "fa" not in a_b.perceive()


def test_the_agent_holds_no_copy_of_the_full_state() -> None:
    """Structural invariant, white-box: apart from perceive(), the agent
    keeps no copy of the full state (there is nothing to leak) — the spec
    is referenced, never copied into agent state."""

    a = agent()
    full = {"fa", "fb", "fs"}
    for name, value in vars(a).items():
        assert not (
            isinstance(value, dict) and set(value) == full
        ), f"agent attribute {name!r} holds a copy of the full state"
    assert a._spec is SPEC


# ── capability gating (named-gap rejection, never guessed) ────────────


def test_undeclared_capability_rejects_with_named_gap() -> None:
    a = agent(caps=ALL_CAPABILITIES - {"commit"}, step=lambda view, r, t: Commit({"x": 1}))
    action, rej = a.act_on(1, [])
    assert isinstance(action, Pass)
    assert rej is not None and "commit" in rej.reason and "not declared" in rej.reason
    assert a.rejections[-1].action == "Commit"


def test_capability_table_covers_all_actions() -> None:
    assert capability_for(Pass()) == "pass"
    assert capability_for(Commit({})) == "commit"
    assert capability_for(Reveal(("f",))) == "reveal_private"
    assert capability_for(Say("b", ())) == "send_message"


# ── speech attribution (the kernel enforces, it does not trust) ───────


def test_forged_speech_rejected() -> None:
    """An agent whose policy speaks with ANOTHER agent's attribution is
    rejected — the kernel checks node + source + observer itself."""

    def forgery(view, round_no, transcript):
        delta = fact_delta_for("say", "b", "fa", "1", 1, 0, "t-agent")  # b's delta
        return Say("shared", (delta,))

    a = agent(step=forgery)
    action, rej = a.act_on(1, [])
    assert isinstance(action, Pass)
    assert rej is not None and "node" in rej.reason


def test_self_sourced_speech_admitted() -> None:
    def honest(view, round_no, transcript):
        delta = fact_delta_for("say", "a", "fa", view["fa"], round_no, 0, "t-agent")
        return Say("shared", (delta,))

    a = agent(step=honest)
    action, rej = a.act_on(1, [])
    assert isinstance(action, Say) and rej is None


def test_reveal_only_allows_private_layer() -> None:
    def bad_reveal(view, round_no, transcript):
        return Reveal(("fs",))  # fs is SHARED, not a's private layer

    a = agent(step=bad_reveal)
    action, rej = a.act_on(1, [])
    assert isinstance(action, Pass)
    assert rej is not None and "non-private" in rej.reason


def test_reveal_allows_own_private_fact() -> None:
    def ok_reveal(view, round_no, transcript):
        return Reveal(("fa",))

    a = agent(step=ok_reveal)
    action, rej = a.act_on(1, [])
    assert isinstance(action, Reveal) and rej is None


# ── self-sourced storage discipline ───────────────────────────────────


def test_remember_requires_self_sourced_provenance() -> None:
    a = agent()
    foreign = Assertion(
        id="t-forged",
        subject=TermRef(id="x"),
        relation=TermRef(id="is"),
        object="y",
        provenance=Provenance(
            source=Source(uri="agent:b"), observer="b",
        ),
    )
    try:
        a.remember(foreign)
        raise AssertionError("storing a foreign-sourced assertion must raise")
    except ValueError as e:
        assert "self-sourced" in str(e)
