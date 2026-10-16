# Phase 0 — Foundation

**Goal:** the substrate — CODEX model + store, versioned Semantic IR, golden
serialization, CLI, experiment harness, CI. No intelligence yet; nothing in this phase
"thinks". Everything later phases touch must be stable, inspectable, and versioned.

**Scope:** action-steps 01–05 (`P0.01`–`P0.10`). **Out of scope:** any domain logic
(regex, 20Q), any model training, anything GPU (ADR-0010: CPU-only in-container).

## Exit criteria (the six; step 05 maps each to evidence)

1. **Package** — `pip install -e '.[dev]'` + `import kainos` + `kainos` CLI entry
   all work; `make test/lint/typecheck` green. *(01, 04)*
2. **Assertions only** — the CODEX rejects a bare edge: missing `provenance`/`source`
   raises; a disputed pair survives with both sides returned. *(02, test:
   `tests/codex/test_models.py`, `tests/codex/test_store.py`)*
3. **Store parity** — `SqliteCodexStore` and `InMemoryCodexStore` pass the same
   parametrized test suite. *(02)*
4. **IR discipline** — `specs/ir.schema.json` + `codex.schema.json` exist; `validate`
   rejects malformed IR with a schema path; golden round-trips are byte-stable. *(03, 04)*
5. **Harness** — a registered experiment runs, writes `results/*.md|json` with
   `seed`/`commit`/`dataset_hash` config, and renders a markdown report. *(05)*
6. **CI + sign-off** — `.github/workflows/ci.yml` runs pytest + lint + typecheck green;
   this phase's `results.md` is filled in. *(05)*

## Actions

See [`actions.md`](actions.md). Sign-off: [`results.md`](results.md) (filled by step 05).

## Risks / notes

- The schema (`codex.schema.json`, `ir.schema.json`) is the contract. Any field change
  is a *breaking* change needing a schema version bump + ADR, because phases 1–2 data
  will be stored against it.
- `data/codex.sqlite` is the CLI's runtime DB — gitignored; it is **not** part of the
  committed substrate (see `../../90-appendices/repo-layout.md`).
