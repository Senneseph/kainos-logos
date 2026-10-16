# 40 — Testing

How every architectural claim becomes a reproducible, CI-gated experiment.

| File | Content |
|------|---------|
| [`harness.md`](harness.md) | The experiment-runner contract (how a claim becomes a result). |
| [`metrics.md`](metrics.md) | The full metric vocabulary, defined once. |
| [`benchmarks.md`](benchmarks.md) | The benchmark registry (E0.1 … E3.5). |

## Testing philosophy (P8: measure, don't argue)

1. Every claim is an **experiment** with a hypothesis, a metric, a threshold, and an
   evidence file — never "seems to work".
2. **Unit tests** gate correctness of substrate (CODEX, IR, kernel, emitter).
3. **Experiments** gate claims (compositionality, persistence, uncertainty, growth).
4. **Golden files** gate serialization stability.
5. **Baselines** are mandatory whenever we claim an improvement (random questioner,
   direct emitter, stateless learner, conventional model).

## The test pyramid (Phase 0 → 3)

```
experiments (claims)          ← few, high-value, CI + manual report
   └ integration (pipelines)  ← phase-level
      └ unit (models/store)   ← many, fast
         └ golden (snapshots) ← serialization
```

## CI gates

- `pytest` (unit + integration + golden) — must be green.
- `make typecheck` (mypy strict) — must be clean.
- `make lint` (ruff) — must be clean.
- `make bench` — experiments; results written to `results/`, not necessarily
  re-run on every commit (slow ones are marked and run on a schedule/PR label).
