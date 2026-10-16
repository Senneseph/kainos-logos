# Phase 0 — Results (sign-off)

> Filled by [`action-steps/05-harness-ci.md`](../../../action-steps/05-harness-ci.md) — Phase 0 sign-off.

- **Date / commit:** 2026-08-20 · verified at parent `d23529d` (step 04) + this file's commit (`git log -1 --format=%h -- plan/30-phases/phase-0-foundation/results.md`)
- **Claim:** the substrate is sound, versioned, and inspectable.

| Exit criterion | Evidence (path / passing test) | Status |
|----------------|--------------------------------|--------|
| 1. Package installs, imports, CLI works | `pip install -e '.[dev]'` + `import kainos` + `kainos` CLI verified in-container on every gate run (117 tests green). `tests/test_scaffold.py` (packaging/entry-point), `tests/cli/test_cli.py::test_console_script_is_wired` (installed `kainos` script), full CLI coverage in `tests/cli/test_cli.py` | ✅ |
| 2. Assertions only (no bare edge; disputed pair preserved) | Bare-edge rejection: `tests/codex/test_models.py::test_missing_provenance_raises`, `::test_omitted_provenance_raises`, `::test_missing_source_raises`, `::test_schema_rejects_missing_provenance`, `::test_schema_rejects_missing_source`. Disputed pair: `tests/codex/test_store.py::test_disputed_pair_survives_in_both_stores[sqlite]` and `[memory]` (both sides returned; neither deleted) | ✅ |
| 3. Store parity (SQLite ≡ in-memory) | Entire parametrized suite `tests/codex/test_store.py` runs `[sqlite]`/`[memory]` — identical expectations, both pass. Byte-identical dumps: `tests/golden/test_golden.py::test_codex_dump_matches_golden[sqlite]` + `[memory]` | ✅ |
| 4. IR + codex schemas; validation; golden round-trip | `specs/codex.schema.json` + `specs/ir.schema.json` (kainos/codex/1, kainos/ir/1; closed shapes). Malformed IR rejected with schema path: `tests/ir/test_codec.py::test_missing_kind_raises_with_path` et al. Byte-stable goldens: `tests/golden/test_golden.py::test_ir_golden_round_trip_is_byte_stable`, `::test_golden_dump_file_is_itself_canonical`; `tests/ir/test_codec.py::test_bundled_schema_is_byte_identical_to_specs` | ✅ |
| 5. Harness runs + writes results with config | `results/dummy.json` + `results/dummy.md` (+ `SUMMARY.md` report) — config block `{"commit": "d23529d", "dataset_hash": null, "seed": 0}`; `tests/harness/test_runner.py` (registration, execution, reproducibility keys, persistence, reporting, resolution, phase selection, module entry) | ✅ |
| 6. CI green + this file signed | `.github/workflows/ci.yml` — container-first (ADR-0001/0010): `make image` → `make test` (pytest) → `make lint` → `make typecheck` → `make bench` (harness smoke). Local equivalent already run green: 117 passed, ruff clean, mypy clean (15 files). This file signed. | ✅ |

**Dummy experiment run** (`results/dummy.md`):

```
# Experiment results

| name | passed | value | threshold | evidence |
|------|--------|-------|-----------|----------|
| dummy | PASS | 1.0 | == 1.0 | `results/dummy.evidence.json` |
```

**Test counts:** `pytest --collect-only -q` → `117 tests collected in 0.49s` · `pytest -q` → `117 passed in 1.33s`

**Notes / deviations**
- `Result` carries one additive field beyond the plan-40 dataclass: `threshold: str | None = None` (the report table column needs it; the contract's five fields are unchanged and in order).
- `config.commit` resolves `KAINOS_GIT_COMMIT` (injected by the Makefile, so in-container runs carry the host's commit) > `git rev-parse` > `"unknown"`.

---
*Phase 0 is DONE. Next: `action-steps/06-regex-ir-emitter.md` (Phase 1).*
