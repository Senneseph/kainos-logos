"""In-memory implementation of ``CodexStore`` (P0.03) — for fast tests.

Behavior is required to be **identical** to :class:`SqliteCodexStore`
(Phase 0 exit criterion "store parity"); ``tests/codex/test_store.py`` enforces
this with both parametrized unit tests and a full scenario-diff between the two
implementations. Behavior contract: see
:meth:`kainos.codex.store.CodexStore` module docstring.
"""

from __future__ import annotations

import json
from dataclasses import replace

from kainos.codex.explain import explain as _explain
from kainos.codex.models import Assertion, Context, EpistemicState, TermRef

__all__ = ["InMemoryCodexStore"]


class InMemoryCodexStore:
    """Dict/list-backed CODEX store with the same contract as the SQLite one."""

    def __init__(self) -> None:
        self._terms: dict[str, TermRef] = {}
        self._assertions: dict[str, Assertion] = {}
        self._generation = 0

    @property
    def generation(self) -> int:
        # One increment per add; update_status routes through add.
        return self._generation

    # ── helpers ────────────────────────────────────────────────────────────

    def _upsert_term(self, t: TermRef) -> None:
        self._terms[t.id] = t

    def _term(self, term_id: str) -> TermRef:
        return self._terms.get(term_id, TermRef(id=term_id))

    def _fetch(self, id: str) -> Assertion | None:
        return self._assertions.get(id)

    def get(self, id: str) -> Assertion:
        a = self._fetch(id)
        if a is None:
            raise KeyError(f"unknown assertion id: {id}")
        return a

    # ── CodexStore ─────────────────────────────────────────────────────────

    def add(self, a: Assertion) -> str:
        self._upsert_term(a.subject)
        self._upsert_term(a.relation)
        if isinstance(a.object, TermRef):
            self._upsert_term(a.object)
        # Normalization parity with SQLite: an empty Interval (both bounds
        # open) is indistinguishable from no interval.
        if a.validity is not None and a.validity.from_ is None and a.validity.to is None:
            a = replace(a, validity=None)
        self._assertions[a.id] = a
        self._generation += 1
        return a.id

    def update_status(self, id: str, status: EpistemicState, evidence: list[str] | None = None) -> None:
        a = self.get(id)
        assert a.provenance is not None  # invariant #1: every stored assertion has it
        prov = a.provenance
        new_evidence = list(prov.evidence)
        for e in evidence or []:
            if e not in new_evidence:
                new_evidence.append(e)
        self.add(replace(a, status=status, provenance=replace(prov, evidence=new_evidence)))

    def _context_fragments(self, d: dict) -> list[str]:
        """Per-key JSON fragments a candidate context JSON must contain."""

        return [json.dumps(k) + ": " + json.dumps(d[k], sort_keys=True) for k in sorted(d)]

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
        status_e = None
        if status is not None:
            status_e = status.value if isinstance(status, EpistemicState) else EpistemicState(str(status)).value
        fragments = self._context_fragments(context_match) if context_match is not None else None
        out: list[Assertion] = []
        for a in self._assertions.values():
            if subject is not None and a.subject.id != subject:
                continue
            if relation is not None and a.relation.id != relation:
                continue
            if object is not None and a.object_id != object:
                continue
            if status is not None and a.status.value != status_e:
                continue
            if fragments is not None:
                stored = json.dumps(a.context.data, sort_keys=True)
                if not all(f in stored for f in fragments):
                    continue
            if time_at is not None:
                lo = a.validity.from_ if a.validity is not None else None
                hi = a.validity.to if a.validity is not None else None
                if (lo is not None and lo > time_at) or (hi is not None and hi < time_at):
                    continue
            out.append(a)
        return sorted(out, key=lambda a: a.id)

    def neighbors(self, term: str, depth: int = 1) -> list[Assertion]:
        if depth < 1:
            return []
        frontier: set[str] = {term}
        seen_terms: set[str] = {term}
        found: dict[str, Assertion] = {}
        for _ in range(depth):
            next_frontier: set[str] = set()
            for a in self._assertions.values():
                if a.subject.id in frontier or a.object_id in frontier:
                    found.setdefault(a.id, a)
                    for endpoint in (a.subject.id, a.object_id):
                        if endpoint not in seen_terms:
                            seen_terms.add(endpoint)
                            next_frontier.add(endpoint)
            frontier = next_frontier
            if not frontier:
                break
        return [found[k] for k in sorted(found)]

    def rotate(self, term: str) -> list[TermRef]:
        partners: set[str] = set()
        for a in self._assertions.values():
            if a.subject.id == term or a.object_id == term:
                for endpoint in (a.subject.id, a.object_id):
                    if endpoint != term:
                        partners.add(endpoint)
        return [self._term(t) for t in sorted(partners)]

    def coverage(self, term: str, context: Context | None = None) -> float:
        context_match = context.to_dict() if context is not None else None
        encountered: set[tuple[str, str]] = set()
        verified: set[tuple[str, str]] = set()
        for a in self.query(context_match=context_match):
            if a.subject.id == term:
                combo = (a.relation.id, a.object_id)
            elif a.object_id == term:
                combo = (a.relation.id, a.subject.id)
            else:
                continue
            encountered.add(combo)
            if a.provenance is not None and a.provenance.verified:
                verified.add(combo)
        if not encountered:
            return 0.0
        return len(verified) / len(encountered)

    def dump(self) -> dict:
        terms = [self._terms[t].to_dict() for t in sorted(self._terms)]
        assertions = [self._assertions[i].to_dict() for i in sorted(self._assertions)]
        return {"terms": terms, "assertions": assertions}

    def explain(self, id: str) -> dict:
        return _explain(self, id)
