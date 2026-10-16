"""Promotion discipline — candidate-only, provenance, idempotence,
invisibility of un-promoted content (the P12 anti-corruption rule)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.workspace.promote import _find_role, lapse, promote
from kainos.workspace.workspace import Lifetime, WorkSpace


def _workspace() -> WorkSpace:
    child = WorkSpace(id="C1", label="child")
    child.add_ir(
        {"kind": "state", "relationships": [{"subject": "plan", "relation": "decides_thing", "object": "alpha"}]},
        "the_thing",
    )
    other = WorkSpace(id="C2", label="never promoted")
    other.add_ir(
        {"kind": "state", "relationships": [{"subject": "plan", "relation": "secret_detail", "object": "omega"}]},
        "the_secret",
    )
    root = WorkSpace(id="ROOT_WS", label="root", lifetime=Lifetime.PROJECT)
    root.add_child(child)
    root.add_child(other)
    return root


def test_promote_writes_candidates_only_with_workspace_provenance() -> None:
    root = _workspace()
    codex = InMemoryCodexStore()
    ids = promote(root, "the_thing", codex, observer="tester")
    assert ids == ["as_promoted_ws_ROOT_WS_the_thing_r0"]
    a = codex.get(ids[0])
    assert a.status == EpistemicState.candidate  # NOT established — never skips the path
    assert a.provenance.source.uri == "workspace_ROOT_WS"
    assert a.provenance.derived is True
    assert a.provenance.observer == "tester"
    assert a.object == "alpha"


def test_promote_is_idempotent() -> None:
    root = _workspace()
    codex = InMemoryCodexStore()
    first = promote(root, "the_thing", codex, observer="t1")
    second = promote(root, "the_thing", codex, observer="t2")
    assert first == second
    assert len(codex.query(relation="decides_thing")) == 1  # no duplicate assertions
    # the original observer survives (no rewriting)
    assert codex.get(first[0]).provenance.observer == "t1"


def test_unpromoted_content_invisible_to_codex_negative_control() -> None:
    root = _workspace()
    codex = InMemoryCodexStore()
    promote(root, "the_thing", codex, observer="t")
    # the sibling workspace's IR was NEVER promoted:
    assert codex.query(relation="secret_detail") == []
    assert codex.query(object="omega") == []
    # and nothing can be established out of thin air:
    assert codex.query(status=EpistemicState.established) == []


def test_promote_role_resolution_and_errors() -> None:
    root = _workspace()
    codex = InMemoryCodexStore()
    # role lives in a CHILD — resolved by recursive lookup, provenance still the root
    ids = promote(root, "the_thing", codex, observer="t")
    assert codex.get(ids[0]).provenance.source.uri == "workspace_ROOT_WS"
    with pytest.raises(KeyError):
        promote(root, "does_not_exist", codex, observer="t")

    # ambiguous role (two workspaces hold it) is rejected, not silently merged
    w = WorkSpace(id="AMB", label="amb")
    w.add_ir({"kind": "state", "relationships": [{"subject": "a", "relation": "rel", "object": "b"}]}, "dup")
    c1 = WorkSpace(id="D1", label="d1")
    c1.add_ir({"kind": "state", "relationships": [{"subject": "a", "relation": "rel", "object": "b"}]}, "dup")
    w.add_child(c1)
    with pytest.raises(ValueError):
        _find_role(w, "dup")


def test_lapse_dumps_to_sink_never_to_codex(tmp_path: Path) -> None:
    root = _workspace()
    codex = InMemoryCodexStore()
    sink = tmp_path / "lapsed"
    out = lapse(root, sink)
    assert out == sink / "workspace_ROOT_WS.json"
    assert out.exists()
    # the CODEX is untouched by a lapse — nothing leaked:
    assert codex.query(relation="decides_thing") == []
    assert codex.query(relation="secret_detail") == []
    # the dumped workspace round-trips (regenerable storage, P12)
    data = json.loads(out.read_text())
    back = WorkSpace.load(data)
    assert set(back.children) == {"C1", "C2"}
    assert back.lifetime is Lifetime.PROJECT
