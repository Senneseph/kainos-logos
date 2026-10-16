"""Reconciler semantics (P3.07): contradiction -> new context TERM (not averaging)."""

from __future__ import annotations

import json

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    Provenance,
    Source,
    TermRef,
)
from kainos.exchange.protocol import AssertionDelta, merge
from kainos.exchange.reconciler import CANDIDATE_DIMENSIONS, reconcile

SUBJ = "polar_bear"


def _provenance(node: str) -> Provenance:
    return Provenance(source=Source(uri=f"games:{node}", version="1"), observer=node)


def _a(aid: str, value: str, node: str, context: dict, status=EpistemicState.disputed) -> Assertion:
    return Assertion(
        id=aid,
        subject=TermRef(id=SUBJ, labels=[SUBJ]),
        relation=TermRef(id="has_property", labels=[]),
        object=f"hibernates={value}",
        status=status,
        context=Context(data=context),
        provenance=_provenance(node),
    )


def _disputed_pair(store: InMemoryCodexStore, ctx_a: dict, ctx_b: dict) -> None:
    d1 = AssertionDelta(_a("as_a1", "yes", "node_a", ctx_a), "node_a", "2026-08-21T00:00:00+00:00")
    store.add(_a("as_b1", "no", "node_b", ctx_b, status=EpistemicState.established))
    merge(store, [d1])
    # both sides now disputed via merge's conflict path
    assert store.get("as_a1").status == EpistemicState.disputed
    assert store.get("as_b1").status == EpistemicState.disputed


def test_time_dimension_explains_and_creates_context_term():
    store = InMemoryCodexStore()
    _disputed_pair(store, {"time": "winter"}, {"time": "summer"})
    r = reconcile(store, SUBJ, "has_property")

    assert r.explained
    assert r.dimension == "time"
    assert r.term_id == "ctx:time:polar_bear"
    # the TERM exists in the store's term table, declared as knowledge
    terms = {t["id"]: t for t in store.dump()["terms"]}
    assert "ctx:time:polar_bear" in terms
    assert terms["ctx:time:polar_bear"]["kind"] == "context"
    decls = store.query(relation="declares_context", subject=SUBJ)
    assert len(decls) == 1 and decls[0].status == EpistemicState.established
    # both sides re-established, under DISTINCT contexts, values preserved (no averaging)
    a, b = store.get("as_a1"), store.get("as_b1")
    assert a.status == EpistemicState.established and b.status == EpistemicState.established
    assert a.object == "hibernates=yes" and b.object == "hibernates=no"
    ca = json.dumps(a.context.data, sort_keys=True)
    cb = json.dumps(b.context.data, sort_keys=True)
    assert ca != cb
    assert a.context.data.get("context_term") == "ctx:time:polar_bear"
    assert b.context.data.get("time") == "summer"
    assert a.context.data.get("time") == "winter"
    # disputed -> 0
    assert r.disputed_after == 0
    left = [x for x in store.query(subject=SUBJ, relation="has_property") if x.status == EpistemicState.disputed]
    assert left == []


def test_unexplained_group_stays_disputed_and_invents_nothing():
    store = InMemoryCodexStore()
    _disputed_pair(store, {}, {})  # identical (empty) contexts: nothing distinguishes
    r = reconcile(store, SUBJ, "has_property")
    assert not r.explained
    assert r.term_id is None
    for tid in ("ctx:time:polar_bear", "ctx:location:polar_bear", "ctx:context:polar_bear"):
        assert tid not in {t["id"] for t in store.dump()["terms"]}
    assert store.get("as_a1").status == EpistemicState.disputed
    assert store.get("as_b1").status == EpistemicState.disputed
    # no averaged third value
    vals = {x.object for x in store.query(subject=SUBJ, relation="has_property")}
    assert vals == {"hibernates=yes", "hibernates=no"}


def test_specific_dimensions_prefer_over_catchall():
    """A specific dimension (location) found before the catch-all 'context'."""

    store = InMemoryCodexStore()
    _disputed_pair(store, {"location": "den"}, {"location": "ice"})
    r = reconcile(store, SUBJ, "has_property")
    assert r.explained and r.dimension == "location"
    assert r.term_id == "ctx:location:polar_bear"


def test_context_catchall_covers_unnamed_context_facts():
    store = InMemoryCodexStore()
    _disputed_pair(store, {"observed_by": "field_team_1"}, {"observed_by": "field_team_2"})
    r = reconcile(store, SUBJ, "has_property")
    assert r.explained and r.dimension == "context"
    assert r.term_id == "ctx:context:polar_bear"


def test_reconcile_is_idempotent():
    store = InMemoryCodexStore()
    _disputed_pair(store, {"time": "winter"}, {"time": "summer"})
    r1 = reconcile(store, SUBJ, "has_property")

    def state() -> dict:
        return {
            a.id: (a.status.value, json.dumps(a.context.data, sort_keys=True))
            for a in store.query(subject=SUBJ, relation="has_property")
        }

    s1 = state()
    r2 = reconcile(store, SUBJ, "has_property")
    # the term is the same, declared exactly once, and the store state is stable
    assert r2.term_id == r1.term_id == "ctx:time:polar_bear"
    assert state() == s1
    decls = store.query(relation="declares_context", subject=SUBJ)
    assert len(decls) == 1


def test_candidate_list_matches_plan():
    assert tuple(CANDIDATE_DIMENSIONS) == ("time", "location", "role", "modality", "context")


def test_no_conflict_group_is_a_noop():
    store = InMemoryCodexStore()
    store.add(_a("as_a1", "yes", "node_a", {"time": "winter"}, status=EpistemicState.established))
    r = reconcile(store, SUBJ, "has_property")
    assert not r.explained and r.note == "no conflicting group"
    assert r.term_id is None
