"""Shared explain (P0.04) — the module function, exercised against BOTH stores.

Directive scenarios: B is evidence for A -> explain(A) includes B in its chain;
a missing evidence id never raises. Plus depth-limiting, cycles, and the
store-method wiring (both impls must delegate to the same logic).
"""

from __future__ import annotations

import pytest

from kainos.codex.explain import DEFAULT_DEPTH, explain
from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.codex.sqlite import SqliteCodexStore
from tests.codex.helpers import make_assertion, make_provenance

STORE_IMPLS = [SqliteCodexStore, InMemoryCodexStore]
STORE_IDS = ["sqlite", "memory"]


@pytest.fixture(params=STORE_IMPLS, ids=STORE_IDS)
def store(request) -> SqliteCodexStore | InMemoryCodexStore:
    impl = request.param
    s: SqliteCodexStore | InMemoryCodexStore = (
        SqliteCodexStore(":memory:") if impl is SqliteCodexStore else InMemoryCodexStore()
    )
    yield s
    if isinstance(s, SqliteCodexStore):
        s.close()


def test_explain_includes_evidence_in_chain(store):
    store.add(make_assertion("B", "S-B", "R-B", "O-B", status=EpistemicState.established))
    store.add(make_assertion("A", "S-A", "R-A", "O-A", provenance=make_provenance(evidence=["B"])))

    ex = explain(store, "A")
    assert ex["id"] == "A"
    assert ex["assertion"]["id"] == "A"
    assert ex["provenance"]["evidence"] == ["B"]
    assert [e["id"] for e in ex["chain"]] == ["B"]
    assert ex["chain"][0]["assertion"]["id"] == "B"
    assert ex["chain"][0]["chain"] == []  # B has no evidence of its own


def test_explain_missing_evidence_does_not_raise(store):
    store.add(make_assertion("A", "S-A", "R-A", "O-A", provenance=make_provenance(evidence=["ghost"])))
    ex = explain(store, "A")
    assert ex["chain"] == [{"id": "ghost", "missing": True}]


def test_explain_unknown_top_level_renders_missing(store):
    assert explain(store, "nope") == {"id": "nope", "missing": True}


def test_explain_depth_limit_truncates(store):
    # A -> B -> C -> D (four hops)
    store.add(make_assertion("D", "S-D", "R", "O-D"))
    store.add(make_assertion("C", "S-C", "R", "O-C", provenance=make_provenance(evidence=["D"])))
    store.add(make_assertion("B", "S-B", "R", "O-B", provenance=make_provenance(evidence=["C"])))
    store.add(make_assertion("A", "S-A", "R", "O-A", provenance=make_provenance(evidence=["B"])))

    ex = explain(store, "A", depth=2)
    assert ex["chain"][0]["id"] == "B"
    assert ex["chain"][0]["chain"][0]["id"] == "C"
    assert ex["chain"][0]["chain"][0]["chain"] == [{"id": "D", "truncated": True}]

    # The default depth (3) expands one hop further: D is fully resolved.
    ex3 = explain(store, "A", depth=DEFAULT_DEPTH)
    assert ex3["chain"][0]["chain"][0]["chain"][0]["assertion"]["id"] == "D"


def test_explain_cycle_terminates(store):
    store.add(make_assertion("X", "S-X", "R", "O-X", provenance=make_provenance(evidence=["Y"])))
    store.add(make_assertion("Y", "S-Y", "R", "O-Y", provenance=make_provenance(evidence=["X"])))
    ex = explain(store, "X")
    assert ex["chain"][0]["id"] == "Y"
    assert ex["chain"][0]["chain"] == [{"id": "X", "circular": True}]


def test_store_method_delegates_to_shared_explain(store):
    store.add(make_assertion("A", "S-A", "R-A", "O-A", provenance=make_provenance(evidence=["ghost"])))
    assert store.explain("A") == explain(store, "A")
    # The module function is depth-parameterized; the store method is the default.
    assert store.explain("A") == explain(store, "A", depth=DEFAULT_DEPTH)


def test_get_unknown_raises_keyerror(store):
    with pytest.raises(KeyError):
        store.get("nope")
