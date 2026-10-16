"""Explicit, provenance-carrying promotion into the CODEX (ADR-0012, P3.17).

The anti-corruption rule (P12/X3): **nothing writes a workspace's content to
the CODEX except ``promote``**, and what it writes is deliberately weak —
``candidate`` assertions that must pass the ordinary verification/
consolidation path (Phase 2) before they can become ``established``. Working
memory never writes truth.

- ``promote(ws, ir_role, codex, observer)`` writes the named IR's
  relationships as candidate assertions with
  ``provenance.source = workspace_<id>`` (``derived=True``). Idempotent:
  re-promoting the same relationship is a no-op (deterministic assertion ids;
  the delta-merge discipline from step 19).
- ``lapse(ws, sink)`` handles expired/abandoned lifetimes: dump to
  results-class storage (regenerable) — **never** to the CODEX.
"""

from __future__ import annotations

import json
from pathlib import Path

from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    Provenance,
    Source,
    TermRef,
)
from kainos.codex.store import CodexStore
from kainos.workspace.workspace import WorkSpace

__all__ = ["lapse", "promote", "promoted_assertion_id"]


def promoted_assertion_id(ws_id: str, role: str, index: int) -> str:
    """Deterministic id: re-promotion of the same relationship resolves to
    the same assertion (idempotent no-op)."""

    return f"as_promoted_ws_{ws_id}_{role}_r{index}"


def promote(workspace: WorkSpace, ir_role: str, codex: CodexStore, observer: str) -> list[str]:
    """Write every relationship of ``workspace.irs[ir_role]`` to ``codex`` as
    a candidate assertion with provenance ``workspace_<id>``. Returns the
    assertion ids written (re-promotes of existing ids are returned but not
    rewritten — the store state is unchanged by them)."""

    owner = _find_role(workspace, ir_role)
    rels = owner.irs[ir_role].get("relationships", [])
    ids: list[str] = []
    for i, rel in enumerate(rels):
        aid = promoted_assertion_id(workspace.id, ir_role, i)  # provenance credits the ROOT
        if _exists(codex, aid):
            ids.append(aid)
            continue
        ctx = rel.get("context")
        codex.add(
            Assertion(
                id=aid,
                subject=TermRef(id=str(rel["subject"]), labels=[]),
                relation=TermRef(id=str(rel["relation"]), labels=[]),
                object=str(rel["object"]),
                status=EpistemicState.candidate,
                context=Context(data=dict(ctx)) if ctx else Context(),
                provenance=Provenance(
                    source=Source(uri=f"workspace_{workspace.id}", version="1"),
                    observer=observer,
                    derived=True,
                ),
            )
        )
        ids.append(aid)
    return ids


def _find_role(root: WorkSpace, role: str) -> WorkSpace:
    """BFS for the (unique) workspace in the tree holding ``role``. The role
    names an IR anywhere in the promoted tree; the promotion itself is
    credited to the root it was invoked on (``workspace_<root_id>``)."""

    queue = [root]
    owner: WorkSpace | None = None
    while queue:
        ws = queue.pop(0)
        if role in ws.irs:
            if owner is not None:
                raise ValueError(f"role is ambiguous (held by >1 workspace): {role}")
            owner = ws
        queue.extend(ws.children[cid] for cid in sorted(ws.children))
    if owner is None:
        raise KeyError(f"no IR with role in tree rooted at {root.id}: {role}")
    return owner


def _exists(codex: CodexStore, aid: str) -> bool:
    try:
        codex.get(aid)
    except KeyError:
        return False
    return True


def lapse(workspace: WorkSpace, sink: Path) -> Path:
    """Expired/abandoned lifetime handling: dump the workspace to results-
    class storage (a regenerable artifact) and leave the CODEX untouched.
    Returns the sink path written."""

    sink = Path(sink)
    sink.mkdir(parents=True, exist_ok=True)
    out = sink / f"workspace_{workspace.id}.json"
    out.write_text(json.dumps(workspace.dump(), indent=2, sort_keys=True) + "\n")
    return out
