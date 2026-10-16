"""WORKSPACE containers — recursive, lifetime-scoped memory (ADR-0012, P12, P3.15).

Memory is recursively addressable structure, not a bigger context window:
a WORKSPACE is a bounded, named, lifetime-scoped container of Intermediate
Representations (Semantic IR dicts) and child workspaces. "What did we
decide about transportation?" is a graph query over workspace IRs at any
depth — never a reprocessing of the conversation that produced them.

Rules (ADR-0012, non-negotiable):
- Content does NOT migrate automatically across lifetimes. Promotion is a
  separate, explicit, provenance-carrying operation (see ``promote.py``);
  expired content is dumped to results-class storage or discarded (``lapse``),
  never silently written to the CODEX.
- Un-promoted content is invisible to the CODEX by construction (P12; the
  E3.7 negative control).
"""

from __future__ import annotations

import copy
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

__all__ = ["Lifetime", "WorkSpace", "query_result_key"]


class Lifetime(str, Enum):
    EPHEMERAL = "ephemeral"
    SESSION = "session"
    PROJECT = "project"
    LONG_TERM = "long_term"  # the CODEX — reachable only via explicit promotion


def query_result_key(r: dict[str, Any]) -> tuple[str, str, int]:
    """Deterministic ordering of query results: by workspace id, role, then
    relationship position (BFS order is stable; sorting removes ambiguity)."""

    return (r["workspace"], r["role"], r["index"])


@dataclass
class WorkSpace:
    """A bounded container of IRs + child workspaces. ``irs`` maps a role
    name (e.g. ``"transport_decision"``) to one Semantic IR dict — a role
    holds the workspace's current IR for that concern (re-recording a role
    replaces it: that is how a decision gets revised)."""

    id: str
    label: str
    lifetime: Lifetime = Lifetime.SESSION
    parent: WorkSpace | None = None
    irs: dict[str, dict] = field(default_factory=dict)
    children: dict[str, WorkSpace] = field(default_factory=dict)

    # ── construction ─────────────────────────────────────────────────────

    def add_ir(self, ir: dict, role: str) -> None:
        """Store an IR (dict, ``kainos/ir/1`` shape) under ``role``.
        Re-adding a role REPLACES its IR (the revision workflow)."""

        if not isinstance(ir, dict):
            raise TypeError("an IR is a dict (Semantic IR per kainos/ir/1)")
        self.irs[role] = copy.deepcopy(ir)

    def add_child(self, child: WorkSpace) -> None:
        if child.id in self.children:
            raise ValueError(f"child id already present: {child.id}")
        child.parent = self
        self.children[child.id] = child

    # ── queryability ─────────────────────────────────────────────────────

    def query(self, predicate: Callable[[str, str, str], bool] | str) -> list[dict]:
        """BFS over this workspace and ALL descendants. For every relationship
        in every contained IR, test the predicate against (subject, relation,
        object). A string predicate is a case-sensitive substring match on
        ANY of the three fields. Results: one row per matched relationship:
        ``{workspace, role, index, subject, relation, object}``, sorted by
        (workspace, role, index) — deterministic.

        A decision stored in a grandchild is found from the project root:
        this is the whole point (query, don't reprocess)."""

        if isinstance(predicate, str):
            needle = predicate

            def predicate(s: str, r: str, o: str) -> bool:
                return needle in s or needle in r or needle in o

        out: list[dict] = []

        def visit(ws: WorkSpace) -> None:
            for role in sorted(ws.irs):
                rels = ws.irs[role].get("relationships", [])
                for i, rel in enumerate(rels):
                    s, r, o = str(rel.get("subject", "")), str(rel.get("relation", "")), str(rel.get("object", ""))
                    if predicate(s, r, o):
                        out.append(
                            {
                                "workspace": ws.id,
                                "role": role,
                                "index": i,
                                "subject": s,
                                "relation": r,
                                "object": o,
                            }
                        )
            for cid in sorted(ws.children):
                visit(ws.children[cid])

        visit(self)
        return sorted(out, key=query_result_key)

    # ── fork / persistence ──────────────────────────────────────────────

    def fork(self, new_id: str) -> WorkSpace:
        """Deep copy of this workspace subtree, rooted at a NEW id with no
        parent (fork-then-revise is the workflow). Mutations on either side
        never leak to the other (verified by test)."""

        def clone(ws: WorkSpace, new_ws_id: str | None) -> WorkSpace:
            c = WorkSpace(
                id=new_ws_id if new_ws_id is not None else ws.id,
                label=ws.label,
                lifetime=ws.lifetime,
                parent=None,  # re-wired below
                irs=copy.deepcopy(ws.irs),
            )
            for cid in sorted(ws.children):
                c.add_child(clone(ws.children[cid], None))
            return c

        f = clone(self, new_id)
        # re-wire parent pointers within the fork (add_child did it; the root
        # stays parentless by construction)
        return f

    def dump(self) -> dict:
        """Deterministic dict form (sorted keys where it matters); the
        JSON ``json.dumps(dump(), sort_keys=True)`` is byte-stable — this is
        how a session restarts (P12: workspaces are JSON, they ride the
        existing codec)."""

        def d(ws: WorkSpace) -> dict:
            return {
                "id": ws.id,
                "label": ws.label,
                "lifetime": ws.lifetime.value,
                "parent": ws.parent.id if ws.parent else None,
                "irs": {role: ws.irs[role] for role in sorted(ws.irs)},
                "children": [c for c in (d(ws.children[cid]) for cid in sorted(ws.children))],
            }

        return d(self)

    @staticmethod
    def load(data: dict) -> WorkSpace:
        """Inverse of :meth:`dump` (tree, parent re-wired)."""

        def build(node: dict) -> WorkSpace:
            ws = WorkSpace(id=node["id"], label=node["label"], lifetime=Lifetime(node["lifetime"]), irs=node.get("irs", {}))
            for cnode in node.get("children", []):
                ws.add_child(build(cnode))  # add_child re-wires child.parent
            return ws

        return build(data)
