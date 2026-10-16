# 10.1 — CODEX (persistent semantic substrate)

Design summary. The normative build spec is `../../action-steps/02-codex-model-store.md`
and `../../action-steps/03-codex-explain-ir.md`; the machine-readable schema is
`specs/codex.schema.json` (emitted by step 02) — if this page and the schema disagree,
the schema wins and this page is stale.

## Why "assertions, not facts" (invariant #1)

The store never holds bare edges. Every knowledge unit is an **Assertion**: a
relationship wrapped in the metadata that makes it evaluable:

```
Assertion
├── subject:    TermRef
├── relation:   TermRef
├── object:     TermRef | str
├── polarity:   bool          (negation is data, not a separate relation)
├── context:    Context       (free-form JSON; relationships indexed by context)
├── validity:   Interval?     (valid_from/valid_to; null = open-ended)
├── confidence: float ∈ [0,1]
├── status:     EpistemicState
├── provenance: Provenance    (MANDATORY — missing source ⇒ TypeError)
│                ├── source: Source (uri, media_type, version, hash, retrieved_at, authority)
│                ├── observer: str
│                └── derived / verified / evidence: [ids]
└── exception:  ExceptionState?  (boundary marker; see glossary)
```

Consequences that tests must enforce:

- No store accepts an `Assertion` without non-null `provenance.source` (ADR-0008).
- Conflicting assertions (e.g. `CAPITAL_OF(France,Paris)` / `CAPITAL_OF(France,Lyon)`)
  are **both stored** with their status — never averaged (invariant #6, P6).
- `explain(id)` returns the assertion plus its recursive evidence chain — the
  inspectability spine (invariant #9). A missing evidence id renders as
  `{"id": ..., "missing": true}`, never an exception.

## Store protocol

`CodexStore` (add / update_status / query / neighbors / rotate / coverage / dump /
explain) with two implementations required to behave identically:
`SqliteCodexStore` (default, durable) and `InMemoryCodexStore` (tests). All Phase 0–2
store logic is exercised against **both** via parametrized tests.

- `rotate(term)`: return the term's neighborhood — the "rotation" primitive that
  resolves vague references ("the dash thing") through semantic proximity.
- `coverage(term, context)`: `verified_combinations / encountered_combinations` —
  the quantitative "how well do we understand this term" signal behind the growth
  dashboard (Phase 2, E2.2).

## What is intentionally NOT here

- No reasoner logic (see `phases` docs; resolution lives in the domain packages).
- No graph-DB engine. SQLite-behind-an-interface first (ADR-0002); a graph-DB port is
  a Phase 3+ concern only if traversal cost demands it. Distribution via semantic
  deltas is separate: `distributed-codex.md`.
