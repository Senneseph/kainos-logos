**Signed by:** step 05 / action P0.10 — fills `plan/30-phases/phase-0-foundation/results.md`.

Phase 0 is signed off when **all six** exit criteria are met (step 05 maps each to
evidence):

1. **Package** — `pip install -e '.[dev]'` + `import kainos` + `kainos` CLI entry
   all work; `make test/lint/typecheck` green. *(01, 04)*
2. **Assertions only** — the CODEX rejects a bare edge: missing `provenance`/
   `source` raises; a disputed pair survives with both sides returned. *(02,
   tests: `tests/codex/test_models.py`, `tests/codex/test_store.py`)*
3. **Store parity** — `SqliteCodexStore` and `InMemoryCodexStore` pass the same
   parametrized test suite. *(02)*
4. **IR discipline** — `specs/ir.schema.json` + `codex.schema.json` exist;
   `validate` rejects malformed IR with a schema path; golden round-trips are
   byte-stable. *(03, 04)*
5. **Harness** — a registered experiment runs, writes `results/*.md|json` with
   `seed`/`commit`/`dataset_hash` config, and renders a markdown report. *(05)*
6. **CI + sign-off** — `.github/workflows/ci.yml` runs pytest + lint + typecheck
   green; this phase's `results.md` is filled in. *(05)*

After sign-off: mark step 05 ✅ in `action-steps/README.md`; proceed to
`action-steps/06-regex-ir-emitter.md`.
