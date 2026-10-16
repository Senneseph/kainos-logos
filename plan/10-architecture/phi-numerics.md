# 10.3 — φ/Fibonacci numerics (isolated, benchmark-gated)

> **Status: EXPERIMENTAL. Gated by ADR-0006.** This capability is *never* a dependency
> of the CODEX schema or the Phase 0–2 pipeline. It is a standalone experiment with an
> explicit adopt/reject verdict (E3.5 numerics, E3.2 topology).

## The idea (from PROJECT_OVERVIEW)

Represent magnitudes as `sign · φ^n` (φ = the golden ratio). Two identities do the work:

- **Multiplication → exponent addition:** `φ^a · φ^b = φ^(a+b)` — a MAC becomes
  "add exponents, XOR signs, accumulate, normalize" instead of a floating-point multiply.
- **Fibonacci carry normalization:** `φ^(n+2) = φ^(n+1) + φ^n` — two adjacent magnitude
  levels sum to exactly the next level. Accumulation reduces by *local rewrites* of a
  digit string, the Fibonacci/Zeckendorf structure of φ-positional numbers.

The hypothesis is **not** "φ beats binary." It is: at a matched bit budget, the
representation may be *more computationally efficient than numerically efficient* —
the killer metric is **useful neural computation per bit-operation**, not bits per
number.

## The seam

`kainos.numerics` exposes a `Numerics` protocol:

```
Numerics: encode(x) -> int ; decode(i) -> float ; compare(a, b) ; accumulate(list) -> float
FloatNumerics   — identity pass-through (DEFAULT; core must behave identically)
PhiNumerics     — s·φ^n encode/decode, exponent-add multiply, Fibonacci normalization
```

Core code only touches the protocol. `FloatNumerics` is the default, and a regression
test proves the Phase 1 pipeline passes E1.1 unchanged under it (the seam is inert by
default).

## Benchmarks (action-step 18)

| Experiment | Compares | Metrics | Verdict |
|------------|----------|---------|---------|
| E3.5 φ numerics | `PhiNumerics` MAC/histogram kernels vs FP8/INT8 at matched bit budget | error-per-op, ops-per-result | `adopt` / `reject` + margin |
| E3.2 topology | `X_{n+2} = f(X_{n+1}) + X_n` residual recurrence and/or Fibonacci width schedule vs same-budget MLP, ≥3 seeds | task accuracy, variance | `adopt` / `reject` + margin |

## The gate rule

Unless the benchmark wins by a stated margin, the verdict is **reject** and the result
is recorded in `plan/30-phases/phase-3-generalization/results.md` + an ADR. A reject is
a success of the method, not a failure of the project (P8).

## Why keep it at all

The overview conversation rates φ/Fibonacci the highest of all the speculative ideas
(★★★★★) *and* explicitly warns against assuming superiority — which is exactly what the
gate encodes. The shared recurrence (`φ^(n+2)=φ^(n+1)+φ^n` numerically,
`F_{n+2}=F_{n+1}+F_n` topologically) is a genuinely unusual property of this scale
system; it deserves one clean, cheap test before it's dismissed or promoted.
