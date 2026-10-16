"""CODEX — the persistent semantic substrate (assertions, not facts).

Phase 0 contents: data model (:mod:`kainos.codex.models`), the store protocol
(:mod:`~kainos.codex.store.CodexStore`), the shared explain logic
(:mod:`kainos.codex.explain`), and the two behavior-identical implementations
(:class:`~kainos.codex.sqlite.SqliteCodexStore`, default, and
:class:`~kainos.codex.memory.InMemoryCodexStore`). Contract:
``specs/codex.schema.json`` (``kainos/codex/1``).
"""

from kainos.codex.explain import explain
from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    ExceptionState,
    Interval,
    Provenance,
    Source,
    TermRef,
)
from kainos.codex.sqlite import SqliteCodexStore
from kainos.codex.store import CodexStore

__all__ = [
    "Assertion",
    "CodexStore",
    "Context",
    "EpistemicState",
    "ExceptionState",
    "InMemoryCodexStore",
    "Interval",
    "Provenance",
    "Source",
    "SqliteCodexStore",
    "TermRef",
    "explain",
]
