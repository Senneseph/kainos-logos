"""Shared explain logic (P0.04) — the inspectability spine (invariant #9).

Both store impls delegate their protocol ``explain`` method to :func:`explain`,
so SQLite and in-memory behavior can never diverge. Result shape:

- resolved node: ``{"id", "assertion", "provenance", "chain"}`` where each
  ``chain`` entry is either
  - another resolved node (same shape) for an existing evidence id,
  - ``{"id": I, "missing": true}`` for an unknown id (never raises),
  - ``{"id": I, "circular": true}`` for a cycle in the evidence graph,
  - ``{"id": I, "truncated": true}`` where the depth limit cut the recursion.

``depth`` (default 3) caps how many evidence levels are expanded below the
requested assertion.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:  # avoid a runtime import cycle (stores import this module)
    from kainos.codex.store import CodexStore

__all__ = ["DEFAULT_DEPTH", "explain"]

DEFAULT_DEPTH: Final = 3


def explain(store: CodexStore, id: str, depth: int = DEFAULT_DEPTH) -> dict[str, Any]:
    """Return the assertion dict + provenance + recursive, depth-limited evidence chain.

    Never raises for missing evidence — unknown ids render as
    ``{"id": I, "missing": true}`` (plan 10.1).
    """
    return _node(store, id, depth, frozenset())


def _node(store: CodexStore, id: str, depth_left: int, seen: frozenset[str]) -> dict[str, Any]:
    try:
        a = store.get(id)
    except KeyError:
        return {"id": id, "missing": True}
    if id in seen:
        return {"id": id, "circular": True}
    prov = a.provenance
    assert prov is not None  # invariant #1: no assertion exists without provenance
    node: dict[str, Any] = {
        "id": id,
        "assertion": a.to_dict(),
        "provenance": prov.to_dict(),
    }
    if depth_left > 0:
        node["chain"] = [_node(store, e, depth_left - 1, seen | {id}) for e in prov.evidence]
    else:
        node["chain"] = [{"id": e, "truncated": True} for e in prov.evidence]
    return node
