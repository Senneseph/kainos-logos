"""Planner: proof on achievables, NoValidPlan (gap + nearest prefix + trace)
on unachievable, and the P11 property — plans never name an undeclared
capability (hypothesis-driven)."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from kainos.codex.memory import InMemoryCodexStore
from kainos.projection.capabilities import load_capabilities, seed_capabilities
from kainos.projection.planner import NoValidPlan, Plan, plan


def _store():
    s = InMemoryCodexStore()
    seed_capabilities(s)
    return s


def test_achievable_goal_gives_valid_plan_with_proof():
    store = _store()
    r = plan(["knowledge_located", "artifact_available"], store)
    assert isinstance(r, Plan)
    assert r.steps == ["SEARCH_CODEX", "WRITE_TEXT"]
    # proof chain: each step's preconditions held before it; effects reach the goal
    state: set[str] = set()
    caps = load_capabilities(store)
    for entry in r.proof:
        cap = caps[entry["step"]]
        assert set(cap.preconditions) <= state, entry
        assert state | set(cap.effect) == set(entry["facts_after"])
        state = set(entry["facts_after"])
    assert {"knowledge_located", "artifact_available"} <= state
    assert r.terminal_state() >= {"knowledge_located", "artifact_available"}


def test_initial_context_used():
    store = _store()
    r = plan(["source_content"], store, initial=["source_referenced"])
    assert isinstance(r, Plan) and r.steps == ["READ_SOURCE"]
    r2 = plan(["source_content"], store)  # no context => unachievable
    assert isinstance(r2, NoValidPlan)


def test_unachievable_returns_no_valid_plan_with_gap():
    store = _store()
    r = plan(["image_capability"], store)
    assert isinstance(r, NoValidPlan)
    assert r.gap == "image_capability"  # the unmeetable fact, named
    # nearest prefix: every step precondition-satisfied + new fact, declared only
    declared = set(load_capabilities(store))
    assert all(s in declared for s in r.nearest_prefix)
    caps = load_capabilities(store)
    state: set[str] = set()
    for step in r.nearest_prefix:
        assert set(caps[step].preconditions) <= state
        assert set(caps[step].effect) - state
        state |= set(caps[step].effect)
    # the refusal is inspectable: the trace records rejected steps
    assert len(r.trace) > 0
    assert any(t.get("outcome") == "precondition_failed" for t in r.trace)
    assert "precondition_failed" in str(r.trace) or "budget" in str(r.trace)


def test_gap_is_an_unmeetable_fact():
    store = _store()
    r = plan(["image_capability", "knowledge_located"], store)
    # knowledge_located IS producible; the gap must name the unproducible one
    assert isinstance(r, NoValidPlan)
    assert r.gap == "image_capability"


def test_no_valid_plan_for_empty_capability_store():
    store = InMemoryCodexStore()  # nothing declared at all
    r = plan(["knowledge_located"], store)
    assert isinstance(r, NoValidPlan)
    assert r.gap == "knowledge_located"
    assert r.nearest_prefix == []


@given(
    goal=st.lists(st.sampled_from(
        ["knowledge_located", "artifact_available", "user_clarification",
         "source_content", "source_referenced", "image_capability"]),
        min_size=1, max_size=4).map(sorted),
    initial=st.lists(st.sampled_from(
        ["knowledge_located", "artifact_available", "user_clarification",
         "source_content", "source_referenced"]), min_size=0, max_size=3),
)
@settings(max_examples=120, deadline=None)
def test_plans_never_use_undeclared_capabilities(goal, initial):
    """P11 property: for ANY goal/initial over the seed capability set, the
    output (Plan steps OR NoValidPlan.nearest_prefix) names only declared
    capabilities — and a Plan's proof independently re-verifies."""

    store = _store()
    declared = set(load_capabilities(store))
    caps = load_capabilities(store)
    r = plan(list(goal), store, initial=list(set(initial)))
    if isinstance(r, Plan):
        assert set(r.steps) <= declared
        state: set[str] = set(initial)
        for entry in r.proof:
            assert set(caps[entry["step"]].preconditions) <= state
            state |= set(entry["facts_added"])
        assert set(goal) <= state
    else:
        assert set(r.nearest_prefix) <= declared
        state: set[str] = set(initial)
        for step in r.nearest_prefix:
            assert set(caps[step].preconditions) <= state
            state |= set(caps[step].effect)
