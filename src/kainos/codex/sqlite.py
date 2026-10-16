"""SQLite implementation of ``CodexStore`` (P0.03) — the default durable store.

DDL per action-step 02 §4. Two storage conventions beyond the bare columns:

- ``assertions.object`` stores the object ``json.dumps``-encoded — a JSON
  string for str objects, a JSON object for TermRefs — so both shapes are
  recoverable and matchable via JSON1 without a schema fork.
- ``terms`` holds term metadata; the ``evidence`` table mirrors
  ``provenance.evidence`` and is kept in sync on every write (it is the join
  table step 03's evidence chains will lean on).

Behavior contract (shared with ``InMemoryCodexStore``): see
:meth:`kainos.codex.store.CodexStore` module docstring. In particular,
``context GLOB`` with escaped per-key fragments implements exactly the
canonical-JSON fragment-subset rule; GLOB is case-sensitive by default.
"""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import replace
from typing import Any, Self

from kainos.codex.explain import explain as _explain
from kainos.codex.models import Assertion, Context, EpistemicState, TermRef

__all__ = ["SqliteCodexStore"]

_DDL = """
CREATE TABLE IF NOT EXISTS terms (id TEXT PRIMARY KEY, kind TEXT, labels TEXT /*JSON*/);
CREATE TABLE IF NOT EXISTS assertions (
  id TEXT PRIMARY KEY, subject TEXT, relation TEXT, object TEXT,
  polarity INTEGER, context TEXT /*JSON*/, validity_from TEXT, validity_to TEXT,
  confidence REAL, status TEXT, provenance TEXT /*JSON*/, exception TEXT
);
CREATE TABLE IF NOT EXISTS evidence (assertion_id TEXT, evidence_id TEXT);
CREATE INDEX IF NOT EXISTS idx_subj ON assertions(subject, relation, object);
CREATE INDEX IF NOT EXISTS idx_rel  ON assertions(relation);
CREATE INDEX IF NOT EXISTS idx_stat ON assertions(status);
"""

# The object's term id whether the column holds a JSON object (TermRef) or a
# JSON string (raw str): `{"id": ...}` yields its id; a JSON string yields itself.
_OBJ_ID = "CASE WHEN json_type(object) = 'object' THEN json_extract(object, '$.id') ELSE json_extract(object, '$') END"


def _glob_escape(pattern: str) -> str:
    """Escape GLOB metacharacters so the pattern matches a literal substring."""

    return "".join(f"[{ch}]" if ch in "*?[" else ch for ch in pattern)


class SqliteCodexStore:
    """SQLite-backed CODEX store. ``path=None`` gives an in-memory database."""

    def __init__(self, path: str | os.PathLike[str] | None = None) -> None:
        self._conn = sqlite3.connect(":memory:" if path is None else os.fspath(path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_DDL)
        self._generation = 0

    @property
    def generation(self) -> int:
        # One increment per add; update_status routes through add.
        return self._generation

    # ── lifecycle ──────────────────────────────────────────────────────────

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # ── term helpers ───────────────────────────────────────────────────────

    def _upsert_term(self, t: TermRef) -> None:
        self._conn.execute(
            "INSERT INTO terms(id, kind, labels) VALUES(?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET kind = excluded.kind, labels = excluded.labels",
            (t.id, t.kind, json.dumps(t.labels)),
        )

    def _term(self, term_id: str) -> TermRef:
        row = self._conn.execute("SELECT kind, labels FROM terms WHERE id = ?", (term_id,)).fetchone()
        if row is None:
            return TermRef(id=term_id)
        return TermRef(id=term_id, kind=row["kind"], labels=json.loads(row["labels"]))

    def _row_to_assertion(self, r: sqlite3.Row) -> Assertion:
        raw_obj = json.loads(r["object"])
        validity = r["validity_from"] if (r["validity_from"] is not None or r["validity_to"] is not None) else None
        return Assertion.from_dict(
            {
                "id": r["id"],
                "subject": self._term(r["subject"]).to_dict(),
                "relation": self._term(r["relation"]).to_dict(),
                "object": raw_obj,
                "polarity": bool(r["polarity"]),
                "context": json.loads(r["context"]),
                "validity": {"from": r["validity_from"], "to": r["validity_to"]} if validity is not None else None,
                "confidence": r["confidence"],
                "status": r["status"],
                "provenance": json.loads(r["provenance"]),
                "exception": r["exception"],
            }
        )

    def _fetch(self, id: str) -> sqlite3.Row | None:
        return self._conn.execute("SELECT * FROM assertions WHERE id = ?", (id,)).fetchone()

    def get(self, id: str) -> Assertion:
        row = self._fetch(id)
        if row is None:
            raise KeyError(f"unknown assertion id: {id}")
        return self._row_to_assertion(row)

    # ── CodexStore ─────────────────────────────────────────────────────────

    def add(self, a: Assertion) -> str:
        self._upsert_term(a.subject)
        self._upsert_term(a.relation)
        if isinstance(a.object, TermRef):
            self._upsert_term(a.object)
        d = a.to_dict()
        validity = d["validity"]
        self._conn.execute(
            "INSERT INTO assertions(id, subject, relation, object, polarity, context, "
            "validity_from, validity_to, confidence, status, provenance, exception) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET subject = excluded.subject, relation = excluded.relation, "
            "object = excluded.object, polarity = excluded.polarity, context = excluded.context, "
            "validity_from = excluded.validity_from, validity_to = excluded.validity_to, "
            "confidence = excluded.confidence, status = excluded.status, provenance = excluded.provenance, "
            "exception = excluded.exception",
            (
                a.id,
                a.subject.id,
                a.relation.id,
                json.dumps(d["object"]),
                int(a.polarity),
                json.dumps(d["context"], sort_keys=True),
                validity["from"] if validity is not None else None,
                validity["to"] if validity is not None else None,
                a.confidence,
                a.status.value,
                json.dumps(d["provenance"]),
                d["exception"],
            ),
        )
        prov = a.provenance
        assert prov is not None  # invariant #1: no assertion exists without provenance
        self._conn.execute("DELETE FROM evidence WHERE assertion_id = ?", (a.id,))
        self._conn.executemany(
            "INSERT INTO evidence(assertion_id, evidence_id) VALUES(?, ?)",
            [(a.id, e) for e in prov.evidence],
        )
        self._conn.commit()
        self._generation += 1
        return a.id

    def update_status(self, id: str, status: EpistemicState, evidence: list[str] | None = None) -> None:
        a = self.get(id)
        prov = a.provenance
        assert prov is not None  # invariant #1: every stored assertion has it
        new_evidence = list(prov.evidence)
        for e in evidence or []:
            if e not in new_evidence:
                new_evidence.append(e)
        self.add(replace(a, status=status, provenance=replace(prov, evidence=new_evidence)))

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
        where: list[str] = []
        params: list[Any] = []
        if subject is not None:
            where.append("subject = ?")
            params.append(subject)
        if relation is not None:
            where.append("relation = ?")
            params.append(relation)
        if object is not None:
            where.append(f"({_OBJ_ID}) = ?")
            params.append(object)
        if status is not None:
            where.append("status = ?")
            params.append(status.value if isinstance(status, EpistemicState) else EpistemicState(str(status)).value)
        if context_match is not None:
            for k in sorted(context_match):
                fragment = json.dumps(k) + ": " + json.dumps(context_match[k], sort_keys=True)
                where.append("context GLOB ?")
                params.append("*" + _glob_escape(fragment) + "*")
        if time_at is not None:
            where.append("(validity_from IS NULL OR validity_from <= ?) AND (validity_to IS NULL OR validity_to >= ?)")
            params.extend((time_at, time_at))
        sql = "SELECT * FROM assertions"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY id"
        return [self._row_to_assertion(r) for r in self._conn.execute(sql, params).fetchall()]

    def neighbors(self, term: str, depth: int = 1) -> list[Assertion]:
        if depth < 1:
            return []
        frontier: set[str] = {term}
        seen_terms: set[str] = {term}
        found: dict[str, Assertion] = {}
        for _ in range(depth):
            next_frontier: set[str] = set()
            marks = ", ".join("?" * len(frontier))
            sql = f"SELECT * FROM assertions WHERE subject IN ({marks}) OR ({_OBJ_ID}) IN ({marks})"
            for r in self._conn.execute(sql, [*frontier, *frontier]).fetchall():
                a = self._row_to_assertion(r)
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
        sql = f"SELECT * FROM assertions WHERE subject = ? OR ({_OBJ_ID}) = ?"
        for r in self._conn.execute(sql, (term, term)).fetchall():
            a = self._row_to_assertion(r)
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
        terms = [self._term(r["id"]).to_dict() for r in self._conn.execute("SELECT id FROM terms ORDER BY id")]
        assertions = [
            self._row_to_assertion(r).to_dict() for r in self._conn.execute("SELECT * FROM assertions ORDER BY id")
        ]
        return {"terms": terms, "assertions": assertions}

    def explain(self, id: str) -> dict:
        return _explain(self, id)
