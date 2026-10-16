"""WORKSPACE containers — recursion, fork isolation, dump/load round-trip."""

from __future__ import annotations

import json

from kainos.workspace.workspace import Lifetime, WorkSpace


def _tree() -> WorkSpace:
    grand = WorkSpace(id="W3", label="grandchild")
    grand.add_ir({"kind": "state", "relationships": [{"subject": "s", "relation": "decides_transport", "object": "route_x"}]}, "decision")
    mid = WorkSpace(id="W2", label="child")
    mid.add_ir({"kind": "state", "relationships": [{"subject": "s", "relation": "r1", "object": "o1"}]}, "other")
    mid.add_child(grand)
    root = WorkSpace(id="W1", label="root")
    root.add_child(mid)
    return root


def test_query_reaches_grandchild_recursion_depth_2() -> None:
    root = _tree()
    rows = root.query("transport")
    assert len(rows) == 1
    assert rows[0]["workspace"] == "W3"
    assert rows[0]["relation"] == "decides_transport"
    assert rows[0]["object"] == "route_x"
    # the decision is in a GRANDCHILD — recursion depth 2 from the root
    assert len(root.children["W2"].children) == 1


def test_query_predicate_matches_any_field_and_string_or_callable() -> None:
    root = _tree()
    assert len(root.query("route_x")) == 1  # object
    assert len(root.query("decides_transport")) == 1  # relation
    call = root.query(lambda s, r, o: r == "r1")
    assert [x["workspace"] for x in call] == ["W2"]


def test_query_is_deterministic_sorted_rows() -> None:
    root = _tree()
    a = root.query(lambda s, r, o: True)
    b = root.query(lambda s, r, o: True)
    assert a == b
    assert a == sorted(a, key=lambda r: (r["workspace"], r["role"], r["index"]))


def test_fork_is_mutation_isolated_both_ways() -> None:
    root = _tree()
    fork = root.fork("W1_fork")
    # revise inside the fork
    fork.children["W2"].children["W3"].add_ir(
        {"kind": "state", "relationships": [{"subject": "s", "relation": "decides_transport", "object": "route_y"}]}, "decision"
    )
    assert fork.query("decides_transport")[0]["object"] == "route_y"
    assert root.query("decides_transport")[0]["object"] == "route_x"  # original untouched
    # and back: an edit to the original never leaks into the fork
    root.children["W2"].add_ir({"kind": "state", "relationships": [{"subject": "s", "relation": "new_rel", "object": "o"}]}, "extra")
    assert "new_rel" not in str(fork.query(lambda s, r, o: True))
    assert fork.id == "W1_fork" and fork.parent is None
    assert root.parent is None and root.id == "W1"


def test_dump_load_roundtrip_lossless_and_deterministic() -> None:
    root = _tree()
    d1 = root.dump()
    d2 = root.dump()
    assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)
    back = WorkSpace.load(d1)
    assert back.dump() == d1
    assert back.query("transport")[0]["object"] == "route_x"
    # parent wiring survived the round-trip
    assert back.children["W2"].parent is back
    assert back.children["W2"].children["W3"].parent is back.children["W2"]
    assert back.parent is None


def test_lifetimes_and_role_replace() -> None:
    ws = WorkSpace(id="A", label="a", lifetime=Lifetime.EPHEMERAL)
    assert Lifetime.PROJECT.value == "project"
    ws.add_ir({"kind": "state", "relationships": []}, "r")
    ws.add_ir({"kind": "state", "relationships": [{"subject": "x", "relation": "y", "object": "z"}]}, "r")  # revision replaces
    assert len(ws.irs["r"]["relationships"]) == 1
    dup = WorkSpace(id="B", label="b")
    root = WorkSpace(id="R", label="root")
    root.add_child(dup)
    try:
        root.add_child(WorkSpace(id="B", label="other"))
        assert False, "expected ValueError on duplicate child id"
    except ValueError:
        pass
