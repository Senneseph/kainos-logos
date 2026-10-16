"""Structured creativity (X2): T=0 deterministic single plan; T>0 over
3 seeds yields >= 3 distinct valid plans, all constraint-valid, trace
records (branch, temperature, seed); and the pruning invariant — a branch
violating an established negative fact is removed before selection."""

from __future__ import annotations

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState, Provenance, Source, TermRef
from kainos.projection.capabilities import (
    Capability,
    load_capabilities,
    seed_capabilities,
)
from kainos.projection.creative import traverse
from kainos.projection.planner import verify_proof

GOAL = ["artifact_available"]


def _store():
    s = InMemoryCodexStore()
    seed_capabilities(s)
    for a in Capability(name="FETCH_TEXT", preconditions=(), effect=("artifact_available",), cost=2.0).to_assertions():
        s.add(a)
    return s


def _reverify(p, store, goal):
    caps = load_capabilities(store)
    state: set[str] = set()
    for entry in verify_proof(p.steps, caps, set()):
        assert set(caps[entry["step"]].preconditions) <= state
        state |= set(entry["facts_added"])
    assert set(goal) <= state, f"plan {p.steps} does not reach the goal"
    return all(s in caps for s in p.steps)


def test_t0_is_deterministic_single_plan():
    store = _store()
    a = traverse(GOAL, store, 0.0, seed=7, k=3)
    b = traverse(GOAL, store, 0.0, seed=7, k=3)
    c = traverse(GOAL, store, 0.0, seed=99, k=3)  # seed irrelevant at T=0
    assert len(a) == 1 and [tuple(p.steps) for p in a] == [tuple(p.steps) for p in b]
    assert [tuple(p.steps) for p in c] == [tuple(p.steps) for p in a]
    _reverify(a[0], store, GOAL)


def test_t_positive_yields_three_distinct_valid_plans_over_three_seeds():
    store = _store()
    seen: set[tuple[str, ...]] = set()
    for seed in (7, 8, 9):
        for p in traverse(GOAL, store, 0.5, seed=seed, k=3):
            seen.add(tuple(p.steps))
            _reverify(p, store, GOAL)  # every sampled plan is constraint-valid
            trace_entries = [t for t in p.trace if "branch" in t]
            assert trace_entries, "every creative plan must record its choice"
            for t in trace_entries:
                assert "temperature" in t and "seed" in t and "score_inputs" in t
    assert len(seen) >= 3, f"spread over 3 seeds: only {seen}"


def test_pruning_invariant_established_negative_fact_removes_branch():
    """A capability whose effect contradicts an established `fact=no`
    assertion may never appear in a sampled plan (X2 hard constraint)."""

    store = _store()
    # declare an image capability...
    for a in Capability(name="EMIT_IMAGE", preconditions=(), effect=("image_capability",), cost=0.5).to_assertions():
        store.add(a)
    # ...and mark image_capability established-NO in the CODEX
    store.add(
        Assertion(
            id="as_neg_image",
            subject=TermRef(id="world", labels=["world"]),
            relation=TermRef(id="has_property", labels=["has property"]),
            object="image_capability=no",
            status=EpistemicState.established,
            provenance=Provenance(source=Source(uri="world_state", version="1"), observer="world_state"),
        )
    )
    # the ONLY plan reaching [image_capability] violates the established fact
    plans = traverse(["image_capability"], store, 2.0, seed=7, k=5)
    assert plans == []  # honest empty set — never a fact-violating plan
    # ...and without the established negative fact, the branch is valid
    store2 = _store()
    for a in Capability(name="EMIT_IMAGE", preconditions=(), effect=("image_capability",), cost=0.5).to_assertions():
        store2.add(a)
    plans2 = traverse(["image_capability"], store2, 0.0, seed=7, k=3)
    assert len(plans2) == 1 and plans2[0].steps == ["EMIT_IMAGE"]
    _reverify(plans2[0], store2, ["image_capability"])


def test_pruned_branches_are_recorded_in_the_audit_trace():
    store = _store()
    for a in Capability(name="EMIT_IMAGE", preconditions=(), effect=("image_capability",), cost=0.5).to_assertions():
        store.add(a)
    store.add(
        Assertion(
            id="as_neg_image",
            subject=TermRef(id="world", labels=["world"]),
            relation=TermRef(id="has_property", labels=["has property"]),
            object="image_capability=no",
            status=EpistemicState.established,
            provenance=Provenance(source=Source(uri="world_state", version="1"), observer="world_state"),
        )
    )
    # goal [artifact_available]: legal plans exist (via FETCH_TEXT /
    # SEARCH+WRITE) while EMIT_IMAGE-shaped branches (e.g. [EMIT_IMAGE,
    # FETCH_TEXT]) reach it too — but violate the established fact, so they
    # are pruned and recorded
    plans = traverse(["artifact_available"], store, 0.0, seed=7, k=3)
    assert plans, "legal plans exist, so traversal must not be empty"
    for p in plans:
        assert "EMIT_IMAGE" not in p.steps
    audit = [t for t in plans[0].trace if t.get("kind") == "pruned_fact_violation"]
    assert audit and any("image_capability" in t["violated"] for t in audit)


def test_no_valid_plans_means_empty_not_fabricated():
    store = _store()
    plans = traverse(["totally_unproducible_fact"], store, 1.0, seed=7, k=3)
    assert plans == []


def test_negative_facts_only_count_when_established():
    """Obsolete `fact=no` rows do not prune (the constraint set is the
    store's ESTABLISHED knowledge)."""

    store = _store()
    for a in Capability(name="EMIT_IMAGE", preconditions=(), effect=("image_capability",), cost=0.5).to_assertions():
        store.add(a)
    store.add(
        Assertion(
            id="as_neg_image",
            subject=TermRef(id="world", labels=["world"]),
            relation=TermRef(id="has_property", labels=["has property"]),
            object="image_capability=no",
            status=EpistemicState.obsolete,  # retired knowledge: no constraint
            provenance=Provenance(source=Source(uri="world_state", version="1"), observer="world_state"),
        )
    )
    plans = traverse(["image_capability"], store, 0.0, seed=7, k=3)
    assert len(plans) == 1 and plans[0].steps == ["EMIT_IMAGE"]
