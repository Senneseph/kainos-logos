"""Merge semantics (P3.06): idempotent, conflict-preserving, provenance-faithful."""

from __future__ import annotations

import json

import pytest

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

SUBJ = "polar_bear"


def _assertion(aid: str, value: str, *, node: str, established: bool = True, context: dict | None = None) -> Assertion:
    return Assertion(
        id=aid,
        subject=TermRef(id=SUBJ, labels=[SUBJ]),
        relation=TermRef(id="has_property", labels=[]),
        object=f"hibernates={value}",
        status=EpistemicState.established if established else EpistemicState.candidate,
        context=Context(data=dict(context or {})),
        provenance=Provenance(
            source=Source(uri=f"games:{node}", version="1"),
            observer=node,
        ),
    )


def _delta(a: Assertion, node: str, ts: str = "2026-08-21T00:00:00+00:00") -> AssertionDelta:
    return AssertionDelta(assertion=a, node_id=node, timestamp=ts)


def test_conflict_preserves_both_sides_and_flags_disputed():
    store = InMemoryCodexStore()
    store.add(_assertion("as_local_1", "no", node="node_b"))
    report = merge(store, [_delta(_assertion("as_remote_1", "yes", node="node_a"), "node_a")])

    # both sides remain, both disputed, cross-linked evidence
    local = store.get("as_local_1")
    remote = store.get("as_remote_1")
    assert local.status == EpistemicState.disputed
    assert remote.status == EpistemicState.disputed
    assert "as_remote_1" in local.provenance.evidence
    assert "as_local_1" in remote.provenance.evidence  # cross-linked, both directions
    # objects untouched — no averaging
    assert local.object == "hibernates=no"
    assert remote.object == "hibernates=yes"
    assert report.disputed == [["as_remote_1", "as_local_1"]]
    assert report.conflicts_preserved == 2


def test_merge_is_idempotent():
    store = InMemoryCodexStore()
    store.add(_assertion("as_local_1", "no", node="node_b"))
    d = _delta(_assertion("as_remote_1", "yes", node="node_a"), "node_a")
    first = merge(store, [d])
    before = len(store.query())
    second = merge(store, [d])

    assert first.merged == ["as_remote_1"]
    assert second.merged == []
    assert second.duplicates == ["as_remote_1"]
    assert len(store.query()) == before  # re-merge is a no-op
    # statuses survive the no-op, unchanged
    assert store.get("as_remote_1").status == EpistemicState.disputed
    assert store.get("as_local_1").status == EpistemicState.disputed


def test_provenance_preserved_through_merge():
    store = InMemoryCodexStore()
    d = _delta(_assertion("as_remote_1", "yes", node="node_a"), "node_a")
    merge(store, [d])
    merged = store.get("as_remote_1")
    assert merged.provenance.observer == "node_a"
    assert merged.provenance.source.uri == "games:node_a"


def test_non_conflicting_addition_passes_through():
    store = InMemoryCodexStore()
    other = Assertion(
        id="as_remote_2",
        subject=TermRef(id="orca", labels=["orca"]),
        relation=TermRef(id="has_property", labels=[]),
        object="migrates=yes",
        status=EpistemicState.established,
        provenance=Provenance(source=Source(uri="games:node_a", version="1"), observer="node_a"),
    )
    report = merge(store, [_delta(other, "node_a")])
    assert report.merged == ["as_remote_2"]
    assert report.disputed == []
    assert store.get("as_remote_2").status == EpistemicState.established


def test_same_value_different_id_is_not_a_conflict():
    store = InMemoryCodexStore()
    store.add(_assertion("as_local_1", "no", node="node_b"))
    d = _delta(_assertion("as_remote_1", "no", node="node_a"), "node_a")  # corroborating side
    report = merge(store, [d])
    assert report.disputed == []
    assert store.get("as_remote_1").status == EpistemicState.established


def test_same_aspect_isolation():
    """Different aspects of the same fact are not conflicts (hibernates vs diet)."""

    store = InMemoryCodexStore()
    store.add(
        Assertion(
            id="as_local_1",
            subject=TermRef(id=SUBJ, labels=[]),
            relation=TermRef(id="has_property", labels=[]),
            object="diet=seals",
            status=EpistemicState.established,
            provenance=Provenance(source=Source(uri="games:node_b", version="1"), observer="node_b"),
        )
    )
    d = _delta(_assertion("as_remote_1", "yes", node="node_a"), "node_a")
    report = merge(store, [d])
    assert report.disputed == []


@pytest.mark.parametrize("bad_delta", [
    {"assertion": {}, "node_id": "n", "timestamp": "2026-08-21T00:00:00+00:00"},  # assertion missing required
    {"assertion": None, "node_id": "n", "timestamp": "2026-08-21T00:00:00+00:00"},
    {"node_id": "n", "timestamp": "2026-08-21T00:00:00+00:00"},  # assertion key missing
    {"assertion": None, "node_id": "n"},  # timestamp missing
    {"assertion": None, "node_id": "n", "timestamp": "yesterday"},  # not ISO-8601
])
def test_delta_contract_rejects_bad_shapes(bad_delta):
    with pytest.raises(ValueError):
        AssertionDelta.from_dict(bad_delta)


def test_delta_json_roundtrip():
    a = _assertion("as_remote_1", "yes", node="node_a", context={"time": "winter"})
    d = _delta(a, "node_a")
    payload = json.loads(json.dumps(d.to_dict()))
    back = AssertionDelta.from_dict(payload)
    assert back.assertion.to_dict() == a.to_dict()
    assert back.node_id == "node_a"
    assert back.timestamp == d.timestamp
