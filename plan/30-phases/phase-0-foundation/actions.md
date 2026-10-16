# Phase 0 — Actions (P0.01–P0.10)

| ID | Action | Directive |
|----|--------|-----------|
| P0.01 | Repo scaffold: Docker image, package, Makefile, gitignore, README | [`../../../action-steps/01-scaffold.md`](../../../action-steps/01-scaffold.md) |
| P0.02 | CODEX data model (assertion dataclasses, mandatory provenance) | [`../../../action-steps/02-codex-model-store.md`](../../../action-steps/02-codex-model-store.md) |
| P0.03 | `CodexStore` protocol + SQLite + in-memory implementations | same as P0.02 |
| P0.04 | `explain(id)` evidence chains wired into both stores | [`../../../action-steps/03-codex-explain-ir.md`](../../../action-steps/03-codex-explain-ir.md) |
| P0.05 | Semantic IR schema + codec + validation | same as P0.04 |
| P0.06 | Golden-file serialization tests | [`../../../action-steps/04-golden-cli.md`](../../../action-steps/04-golden-cli.md) |
| P0.07 | `kainos` CLI (codex add/query/explain/dump, ir validate) | same as P0.06 |
| P0.08 | Experiment harness (runner, registry, result files, report) | [`../../../action-steps/05-harness-ci.md`](../../../action-steps/05-harness-ci.md) |
| P0.09 | CI pipeline (pytest + typecheck + lint in-container) | same as P0.08 |
| P0.10 | Phase 0 sign-off (`results.md`) | same as P0.08 |
