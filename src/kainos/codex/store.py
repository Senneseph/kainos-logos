"""CodexStore protocol (P0.03) — methods, no logic.

Two implementations must behave **identically** (Phase 0 exit criterion
"store parity"): :class:`kainos.codex.sqlite.SqliteCodexStore` (default,
durable) and :class:`kainos.codex.memory.InMemoryCodexStore` (fast tests).
All Phase 0–2 store logic is exercised against both via parametrized tests.

Shared behavior contract (both impls, see their docstrings for details):

- ``query`` filters AND-combine; results are ordered by assertion id.
- ``object=X`` matches a str object equal to X **or** a TermRef with id == X.
- ``context_match``: case-sensitive substring match on the canonical
  (``json.dumps(sort_keys=True)``) JSON of the stored context — every query key
  ``k`` requires the fragment ``json.dumps(k) + ": " + json.dumps(v, sort_keys=True)``
  to occur in it; i.e. a one-level key/value subset (the directive's
  "substring/LIKE match over the context JSON", made multi-key safe).
- ``time_at`` uses inclusive bounds: ``validity_from <= t <= validity_to``;
  an absent/empty bound is open-ended (ISO-8601 strings compare correctly).
- ``neighbors`` expands over subject/object endpoints (a relation is an edge
  label, not a co-occurring term); an empty ``Interval`` normalizes to no
  interval in the store.
- ``explain(id)`` (wired to :func:`kainos.codex.explain.explain`) returns
  ``{"id", "assertion", "provenance", "chain"}`` and never raises: unknown ids
  render as ``{"id": I, "missing": true}``, cycles as ``{"id": I, "circular": true}``.
"""

from __future__ import annotations

from typing import Protocol

from kainos.codex.models import Assertion, Context, EpistemicState, TermRef

__all__ = ["CodexStore"]


class CodexStore(Protocol):
    """The single store interface for the CODEX (ADR-0002: SQLite behind it)."""

    @property
    def generation(self) -> int:
        """Monotonic mutation counter (0 = pristine). One increment per
        ``add``/``update_status`` — a read-only snapshot tag saying "which facts
        currently hold", so caches keyed on stored facts (M1 specialization
        cache) can invalidate themselves when the store mutates."""
        ...

    def add(self, a: Assertion) -> str:
        """Store the assertion (upsert on id; upserts its term rows). Returns the id."""
        ...

    def get(self, id: str) -> Assertion:
        """Fetch one assertion by id; raises ``KeyError`` if unknown."""
        ...

    def update_status(self, id: str, status: EpistemicState, evidence: list[str] | None = None) -> None:
        """Set an assertion's epistemic status; append evidence ids (deduped, order kept)."""
        ...

    def query(
        self,
        *,
        subject: str | None = None,
        relation: str | None = None,
        object: str | None = None,
        status: EpistemicState | None = None,
        context_match: dict | None = None,
        time_at: str | None = None,
    ) -> list[Assertion]:
        """All assertions matching every provided filter, ordered by id (see module docstring)."""
        ...

    def neighbors(self, term: str, depth: int = 1) -> list[Assertion]:
        """Assertions within graph distance ``depth`` of ``term`` (subject/object edges)."""
        ...

    def rotate(self, term: str) -> list[TermRef]:
        """The term's neighborhood: distinct partner terms of its direct assertions, sorted by id."""
        ...

    def coverage(self, term: str, context: Context | None = None) -> float:
        """``verified_combinations / encountered_combinations`` for the term; 0.0 if none.

        A *combination* is a (relation id, partner id) pair over assertions
        involving the term (optionally restricted to matching context). A
        combination is *verified* when some assertion backing it has
        ``provenance.verified`` true. (Plan 10.1: the "how well do we
        understand this term" signal behind the Phase 2 growth dashboard.)
        """
        ...

    def dump(self) -> dict:
        """``{"terms": [...], "assertions": [...]}`` with deterministic (id) ordering."""
        ...

    def explain(self, id: str) -> dict:
        """The assertion plus its (recursive) evidence chain; never raises (see module docstring)."""
        ...

    # The protocol's get/explain are shared with the step-04 CLI and the
    # inspectability tests; step 05 (harness) is the next additive change.
