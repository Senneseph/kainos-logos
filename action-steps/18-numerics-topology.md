# Action Step 18 — φ numerics + Fibonacci topology (GATED, P3.03–P3.05)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

Two **isolated, benchmark-gated** experiments: φ-exponent numerics and Fibonacci
topology. Each is *adopt or reject* — never merged into core unless it wins.

## Prerequisites

- [ ] Phases 0–1 complete (core is stable). This step must not change core behavior.

## Background

The document's φ/Fibonacci ideas are explicitly speculative (ADR-0006). They live
behind a `Numerics` strategy seam so they can be tested without risking the CODEX.
This step builds the seam + the benchmarks; the results are reported as adopt/reject.

## Steps

### 1. `src/kainos/numerics/base.py`

`Numerics` protocol: `encode(x)->int`, `decode(i)->float`, `compare(a,b)`,
`accumulate(list)->float`. `FloatNumerics` = identity pass-through (the default; core
must behave identically with it).

### 2. `src/kainos/numerics/phi.py` — `PhiNumerics`

- Represent a strength as `s·φ^n` (sign bit + φ-exponent).
- `multiply` = exponent add (`φ^a·φ^b = φ^(a+b)`); `accumulate` uses Fibonacci
  normalization (`φ^(n+2) = φ^(n+1)+φ^n` as a local rewrite).
- Tests in `tests/numerics/` mirroring `src/kainos/numerics/` explicitly (G8):
  `test_base.py` (protocol + `FloatNumerics` identity) and `test_phi.py`
  (`encode/decode` round-trips to a stated tolerance, `multiply` = exponent add,
  Fibonacci normalization correctness).

### 3. `benchmarks/phi/` — E3.5

MAC-like + histogram-of-powers kernels comparing `PhiNumerics` vs FP8/INT8 on
**error-per-op** and **ops-per-result** at matched bit budget. → `results/phase-3/e3.5.json`
with a verdict field `adopt|reject` + a written margin.

### 4. `benchmarks/topology/` — E3.2

Toy supervised task; compare `X_{n+2} = f(X_{n+1}) + X_n` residual recurrence and/or a
Fibonacci width schedule vs. same-budget MLP, ≥3 seeds. → `results/phase-3/e3.2.json`
with `adopt|reject` + variance.

### 5. Guard

Regression test `tests/numerics/test_seam_neutral.py`: with `FloatNumerics`
(default), the full Phase 1 pipeline still passes E1.1 (proves the seam didn't
change core). This test runs in CI like any other unit test.

## Verification

```bash
kainos experiment run --name e3.5 && kainos experiment run --name e3.2 \
  && pytest tests/numerics -q
```

Expect: `e3.5.json` and `e3.2.json` contain explicit `adopt|reject` verdicts; the
`tests/numerics/` suite (including `test_seam_neutral.py`) is green.

## Done when

- [ ] `Numerics` seam + `FloatNumerics` + `PhiNumerics` exist and unit-tested
- [ ] E3.5 (φ) and E3.2 (topology) report explicit adopt/reject with a margin
- [ ] core regression green (seam is inert by default)

## If stuck

`plan/10-architecture/phi-numerics.md`, `plan/30-phases/phase-3-generalization/experiments.md` → E3.2/E3.5.
