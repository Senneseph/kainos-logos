# Action Step 02 — CODEX data model + store (P0.02–P0.03)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

The CODEX persistence layer: assertion dataclasses (with mandatory provenance) and a
store interface with a SQLite implementation + an in-memory implementation.

## Prerequisites

- [ ] Step 01 done (`import kainos` works).

## Background

The CODEX stores **assertions, not facts** (invariant #1). Every assertion carries
`source`, `context`, `status`, provenance, and (optionally) a validity interval and
EXCEPTION state. There is **no bare-edge path**. This is the substrate every later
phase depends on — get the model exactly right now.

## Steps

### 1. `src/kainos/codex/models.py`

Frozen dataclasses:

- `TermRef(id: str, kind: str = "concept", labels: list[str] = field(default_factory=list))`
- `Context(data: dict)` — free-form but JSON-serializable
- `Interval(from: str | None, to: str | None)` — validity range
- `Source(uri: str, media_type: str | None = None, version: str | None = None,
  hash: str | None = None, retrieved_at: str | None = None, authority: str | None = None)`
- `EpistemicState(str, Enum)`: `candidate, established, disputed, obsolete,
  hypothesis, ambiguous, contradicted, inapplicable`
- `ExceptionState(str, Enum)`: `unseen, unresolved, ambiguous, conflicting,
  unverified, requires_context, impossible`
- `Provenance(source: Source, observer: str, derived: bool = False,
  verified: bool = False, evidence: list[str] = field(default_factory=list))`
- `Assertion(id: str, subject: TermRef, relation: TermRef, object: TermRef | str,
  polarity: bool = True, context: Context = field(default_factory=Context),
  validity: Interval | None = None, confidence: float = 1.0,
  status: EpistemicState = EpistemicState.candidate, provenance: Provenance,
  exception: ExceptionState | None = None)`

Rules to implement in `__post_init__`:
- **Non-nullable** (invariant #1): raise `TypeError` if `provenance` is missing and if
  `provenance.source` is missing. (`context` and `status` have defaults, so only
  `provenance`/`source` are strictly enforced.)
- `confidence` clamped to `[0.0, 1.0]`.
- `to_dict()` / `from_dict()` round-trip exactly (deterministic key order).

### 2. `specs/codex.schema.json` (G1)

JSON Schema (draft 2020-12) named `kainos/codex/1` — the structural mirror of the
model above:

- `Assertion` required: `id`, `subject`, `relation`, `object`, `status`, `provenance`
  — `provenance` itself requires `source` (with `source.uri`) and `observer`
  (ADR-0008: no bare-edge escape hatch, enforced *by schema* too).
- Optional: `polarity`, `context`, `validity` (`from`/`to`), `confidence`,
  `exception` (enum: `unseen, unresolved, ambiguous, conflicting, unverified,
  requires_context, impossible`).
- The dataclasses remain the implementation source of truth; the schema is the
  *contract*. Add a parity test: every `to_dict()` output in the model test suite
  validates against `specs/codex.schema.json`.

### 3. `src/kainos/codex/store.py`

`CodexStore` protocol (methods, no logic):

```python
class CodexStore(Protocol):
    def add(self, a: Assertion) -> str: ...
    def update_status(self, id: str, status: EpistemicState,
                      evidence: list[str] | None = None) -> None: ...
    def query(self, *, subject: str | None = None, relation: str | None = None,
              object: str | None = None, status: EpistemicState | None = None,
              context_match: dict | None = None, time_at: str | None = None) -> list[Assertion]: ...
    def neighbors(self, term: str, depth: int = 1) -> list[Assertion]: ...
    def rotate(self, term: str) -> list[TermRef]: ...
    def coverage(self, term: str, context: Context | None = None) -> float: ...
    def dump(self) -> dict: ...
    def explain(self, id: str) -> dict: ...
```

### 4. `src/kainos/codex/sqlite.py` — `SqliteCodexStore`

SQLite schema:

```sql
CREATE TABLE terms (id TEXT PRIMARY KEY, kind TEXT, labels TEXT /*JSON*/);
CREATE TABLE assertions (
  id TEXT PRIMARY KEY, subject TEXT, relation TEXT, object TEXT,
  polarity INTEGER, context TEXT /*JSON*/, validity_from TEXT, validity_to TEXT,
  confidence REAL, status TEXT, provenance TEXT /*JSON*/, exception TEXT
);
CREATE TABLE evidence (assertion_id TEXT, evidence_id TEXT);
CREATE INDEX idx_subj ON assertions(subject, relation, object);
CREATE INDEX idx_rel  ON assertions(relation);
CREATE INDEX idx_stat ON assertions(status);
```

- `add` upserts the term rows and inserts the assertion (serialized via `to_dict`).
- `query` builds a parameterized `WHERE` from the provided filters; `context_match`
  is a substring/`LIKE` match over the context JSON; `time_at` checks
  `validity_from <= t <= validity_to` (inclusive, null = open-ended).
- `dump` returns `{"terms": [...], "assertions": [...]}` with deterministic ordering.

### 5. `src/kainos/codex/memory.py` — `InMemoryCodexStore`

Same protocol, backed by dicts/lists (for fast tests). Keep behavior identical to the
SQLite impl for `query`/`neighbors`/`coverage`.

### 6. Tests

`tests/codex/test_models.py`:
- construct a full assertion → `to_dict` → `from_dict` → equal.
- missing `provenance` raises `TypeError`; missing `source` raises `TypeError`.
- `confidence` clamps to `[0,1]`.
- every `to_dict()` output validates against `specs/codex.schema.json` (parity).

`tests/codex/test_store.py` (run against BOTH impls via `pytest.mark.parametrize`
over `[SqliteCodexStore, InMemoryCodexStore]`):
- add two assertions, `query(relation=...)` returns both.
- add a **disputed pair** (`CAPITAL_OF(France,Paris)` and
  `CAPITAL_OF(France,Lyon)`), query returns **both** (invariant #6: no averaging).

## Verification

```bash
pytest tests/codex -q
```

Expect: all green, including the disputed-pair assertion surviving in both stores.

## Done when

- [ ] `models.py`, `store.py`, `sqlite.py`, `memory.py` exist
- [ ] `specs/codex.schema.json` exists; model ⇄ schema parity test green
- [ ] `pytest tests/codex -q` green
- [ ] disputed pair survives (both returned) in both impls
- [ ] non-nullable provenance enforced (missing source raises)

## If stuck

`plan/10-architecture/codex.md` (data model), `plan/30-phases/phase-0-foundation/actions.md` → P0.02–P0.03.
