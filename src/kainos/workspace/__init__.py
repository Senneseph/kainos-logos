"""Recursive workspace memory (Phase 3, ADR-0012; claim X3).

WORKSPACE containers — bounded, lifetime-scoped, nestable, queryable,
forkable, JSON-round-trippable — plus explicit provenance-carrying promotion
into the CODEX and versioned source/analysis separation. The anti-corruption
invariant (P12): un-promoted workspace content is invisible to the CODEX,
and only verified candidates ever enter it.
"""

from kainos.workspace.promote import lapse, promote, promoted_assertion_id
from kainos.workspace.source import (
    DERIVED_FROM,
    AnalysisRecord,
    SourceRef,
    SourceRegistry,
    hash_file,
)
from kainos.workspace.workspace import Lifetime, WorkSpace, query_result_key

__all__ = [
    "DERIVED_FROM",
    "AnalysisRecord",
    "Lifetime",
    "SourceRef",
    "SourceRegistry",
    "WorkSpace",
    "hash_file",
    "lapse",
    "promote",
    "promoted_assertion_id",
    "query_result_key",
]
