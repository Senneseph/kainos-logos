"""Sources vs analyses (ADR-0012, P3.16) — a document does not become knowledge.

``SOURCE`` (uri + hash + version) is one object; each analysis is a VERSIONED
IR referencing it. Analyses are **immutable + append-only**: re-analysis
never overwrites — it is a new version. "What did we conclude last time?" =
:func:`SourceRegistry.latest_analysis`. "Re-analyze for contradictions with
the current model" = a new ``add_analysis`` call (a workspace operation),
output versioned vN+1. If the source changes (hash differs), every analysis
that declared ``derived_from <source_id>`` is flagged stale (dependency
tracking).

Scope guard (Phase 3): local file sources only (uri + hash). No document
ingestion, no external fetches.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

__all__ = ["DERIVED_FROM", "AnalysisRecord", "SourceRef", "SourceRegistry"]

DERIVED_FROM = "derived_from"


@dataclass(frozen=True)
class SourceRef:
    uri: str
    hash: str
    version: int = 1


@dataclass(frozen=True)
class AnalysisRecord:
    source_id: str
    version: int
    ir: dict
    created_at: str


class SourceRegistry:
    """In-memory source+analysis ledger. Source ids are the SourceRef.uri."""

    def __init__(self) -> None:
        self._sources: dict[str, SourceRef] = {}
        self._analyses: dict[str, list[AnalysisRecord]] = {}

    def register(self, ref: SourceRef) -> None:
        if ref.uri in self._sources:
            raise ValueError(f"source already registered: {ref.uri}")
        self._sources[ref.uri] = ref
        self._analyses.setdefault(ref.uri, [])

    def source(self, source_id: str) -> SourceRef:
        return self._sources[source_id]

    def add_analysis(self, source_id: str, ir: dict, created_at: str) -> AnalysisRecord:
        """Append a NEW analysis version (vN+1). Analyses are immutable:
        earlier versions are never touched (verified by test)."""

        if source_id not in self._sources:
            raise KeyError(f"unknown source: {source_id}")
        version = len(self._analyses[source_id]) + 1
        rec = AnalysisRecord(source_id=source_id, version=version, ir=dict(ir), created_at=created_at)
        self._analyses[source_id].append(rec)
        return rec

    def analyses(self, source_id: str) -> list[AnalysisRecord]:
        return list(self._analyses.get(source_id, []))

    def latest_analysis(self, source_id: str) -> AnalysisRecord:
        recs = self._analyses[source_id]
        if not recs:
            raise KeyError(f"no analyses for source: {source_id}")
        return recs[-1]

    def stale_derivations(self, source_id: str, new_hash: str) -> list[str]:
        """The source's hash changed (or is being checked against a new one):
        every analysis that declared ``derived_from <source_id>`` is stale.
        Returns ``["source_id:version", ...]`` (sorted by version) — empty if
        the hash is unchanged or no analysis declared the dependency."""

        ref = self._sources[source_id]
        if new_hash == ref.hash:
            return []
        out = []
        for rec in self._analyses[source_id]:
            rels = rec.ir.get("relationships", [])
            if any(r.get("relation") == DERIVED_FROM and r.get("object") == source_id for r in rels):
                out.append(f"{source_id}:{rec.version}")
        return sorted(out)


def hash_file(path: Path | str) -> str:
    """SHA-256 of a local file (the Phase-3 source identity model)."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
