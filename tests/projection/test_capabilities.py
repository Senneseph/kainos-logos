"""Capabilities are CODEX assertions (P11): round-trip, removal by
obsoletizing, provenance visible — no side effects anywhere."""

from __future__ import annotations

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.projection.capabilities import (
    DEFAULT_CAPABILITIES,
    Capability,
    load_capabilities,
    obsoletize_capability,
    seed_capabilities,
)


def test_seed_load_roundtrip():
    store = InMemoryCodexStore()
    seed_capabilities(store)
    caps = load_capabilities(store)
    assert set(caps) == {c.name for c in DEFAULT_CAPABILITIES}
    for c in DEFAULT_CAPABILITIES:
        assert caps[c.name] == c


def test_no_image_capability_in_seed():
    """E3.6's honest-refusal test depends on the absence of an image
    capability — pin that absence explicitly (X1)."""

    store = InMemoryCodexStore()
    seed_capabilities(store)
    caps = load_capabilities(store)
    assert not any("IMAGE" in n or "GENERATE" in n for n in caps)
    producers_of_image_cap = [c for c in caps.values() if "image_capability" in c.effect]
    assert producers_of_image_cap == []


def test_adding_a_capability_is_a_store_operation():
    """Declaring a NEW capability requires no code change: it is a
    Capability + an assertion add (P11)."""

    store = InMemoryCodexStore()
    seed_capabilities(store)
    assert "FETCH_TEXT" not in load_capabilities(store)
    for a in Capability(name="FETCH_TEXT", preconditions=(), effect=("artifact_available",), cost=2.0).to_assertions():
        store.add(a)
    assert "FETCH_TEXT" in load_capabilities(store)


def test_removal_is_obsoletize_and_changes_planning():
    from kainos.projection.planner import NoValidPlan, Plan, plan

    store = InMemoryCodexStore()
    seed_capabilities(store)
    ok = plan(["artifact_available"], store)
    assert isinstance(ok, Plan) and "WRITE_TEXT" in ok.steps

    obsoletize_capability(store, "WRITE_TEXT")
    after = plan(["artifact_available"], store)
    # without WRITE_TEXT nothing produces artifact_available => NoValidPlan
    assert isinstance(after, NoValidPlan)
    # the obsoleted capability's rows are non-established
    for a in store.query(subject="WRITE_TEXT", relation="has_property"):
        assert a.status == EpistemicState.obsolete


def test_provenance_visible_on_capability_rows():
    store = InMemoryCodexStore()
    seed_capabilities(store)
    a = store.query(subject="SEARCH_CODEX", relation="has_property")[0]
    assert a.provenance is not None
    assert a.provenance.source.uri == "capability_seed"
    assert a.status == EpistemicState.established


def test_unknown_capability_name_rejected():
    store = InMemoryCodexStore()
    try:
        seed_capabilities(store, ["NOT_A_CAPABILITY"])
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_seeding_is_idempotent():
    store = InMemoryCodexStore()
    seed_capabilities(store)
    n1 = len(store.query())
    seed_capabilities(store)  # upserts — no duplicates
    assert len(store.query()) == n1
    assert len(load_capabilities(store)) == len(DEFAULT_CAPABILITIES)
