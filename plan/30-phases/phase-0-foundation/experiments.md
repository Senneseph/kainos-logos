# Phase 0 — Experiments

Phase 0 has one "experiment" (the substrate soundness gate) plus the harness
self-test. The real falsifiable experiments begin in Phase 1.

## E0.1 — Substrate soundness & inspectability

- **Hypothesis:** The CODEX store faithfully represents assertions (provenance,
  context, time, status, EXCEPTION) and every stored assertion is fully
  inspectable/dumpable, with no data loss through add→query→dump.
- **Metric:** round-trip fidelity = 100% of assertions present and field-identical
  after add → query → dump → reload; plus a binary "explain shows provenance +
  evidence chain" check.
- **Threshold:** fidelity == 1.0 and explain check == pass.
- **Evidence:** `tests/codex/test_store.py`, `tests/codex/test_explain.py`,
  golden files.

## E0.2 — Harness self-test

- **Hypothesis:** The experiment harness can run a named experiment and render its
  result table to `results.md`.
- **Metric:** dummy experiment `passed == True`.
- **Threshold:** `kainos experiment run --name dummy` exit code 0 and `results/dummy.md`
  contains the metric.
- **Evidence:** `results/dummy.md`.

Both must pass before Phase 1 begins.
