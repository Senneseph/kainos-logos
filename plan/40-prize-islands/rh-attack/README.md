# RH Attack — operating system

Attack the Riemann Hypothesis **at its foundations** (primes, the series, the
1/2) before any exotic fields, using the store's four operations:

**add something / remove something / duplicate something / alter something.**

RH is fundamentally about primes and their distribution. Whether the
non-trivial zeros all sit on the line is a *side question* to the main
point — but the zeros are where the series "runs out", so they are the
working edge.

## The brief (owner, abridged)

- "Something must be missing with RH. Either the series is wrong, and needs
  something like the previous or next terms in relation to the current, or
  there's something we've missed."
- "What do we need about 1/2 for primes?" (7 = 3+1/2 + 3+1/2; primes as
  difference of two squares; splitting a prime evenly eventually reaches 1/2.)
- One progress report **per day**: work done + interesting findings.
- Read `RH-TRIAL-POINT.md` (starting intuitions) and `RH-DIRECTION.md`
  (the OPERATOR transcript to be tested, not believed).

## Honesty contract (store discipline, non-negotiable)

1. **No `theorem:riemann` is ever invented.** Discovery candidates only;
   the store speaks, not the hand.
2. Every claim in a report is labeled: **measured** / **theorem** /
   **conjecture** / **unmapped** / **falsified-with-computation**.
3. **Constants are computed or fetched, never recalled.** (Day-001 lesson:
   a "published N(10^4)=1423" turned out to be a memory error — the true
   value is 10142, RVM-verified.)
4. Honest walls are reported as results, not failures.
5. External claims (e.g. in RH-DIRECTION.md) are adjudicated by
   re-running the claimed simulation, not by reading its conclusion.

## File map

| path | role |
|---|---|
| `scripts/rh/sieve.py` | exact prime soil (sieve, von Mangoldt, psi, classes, twins, two-squares) |
| `scripts/rh/day001_primes.py` | Q1–Q6 prime-structure study (x ≤ 2e6, twins to 5e7) |
| `scripts/rh/day001_zeta.py` | full zeta layer from numpy: Lanczos logΓ, Euler–Maclaurin ζ, DLMF real Z(t), zero census, S3a–f experiments |
| `scripts/rh/zeta_core.py` | canonical shared zeta engine (extracted from day-001) + `selftest()`; day-002+ scripts import it |
| `scripts/rh/day002_mirror.py` | mirror invariant I(s) = \|ζ(s)\|²+\|ζ(1−s̄)\|² (M2/M3), β-layer leak test (M4), four-mirror orbit structure (M6) |
| `scripts/rh/mpmath_audit_beta.py` | dps-50 oracle for the β layer (rotation proof, first β zeros, I12 values) |
| `scripts/rh/day002_fibonacci_closeout.py` (+`_control.py`) | Fibonacci-vs-zeros close-out; phase-shifted band controls |
| `scripts/rh/zeta_core.py` `Z_rs` | validated Riemann–Siegel real-Z engine (2-term remainder; error 5e-6..3e-5 for t ≥ 4.5e4) |
| `scripts/rh/day003_mirror_scaling.py` | owner's mirror-scale question: M1 \|χ\|=1 on line, M2 off-line grid, M3 involutions (no chain), M4 gap = factorization property |
| `scripts/rh/day003_census_1e5.py` | T=1e5 zero census (RS walk + EM confirm + midpoint twin check + block deficit map) |
| `scripts/rh/day003_s_arg_mpmath.py` | independent dps-40 argument cross-check of the census (2K even-integer identity) |
| `scripts/rh/zeros_T100000.txt` | 138,065 zeros, 0 < γ ≤ 1e5 (float-precision base ≤ 1e4 + RS/EM tiers) |
| `scripts/rh/bench_cupy_numpy.py` | CuPy/ROCm (8060S gfx1151) vs numpy A/B benchmark for the RH workloads |
| `scripts/rh/day004_missing_terms.py` | σ-grid of the missing tail: \|ζ−P_N\| = N^{1−σ}/\|1−s\|, first order = −I (T1/T0 = 2.000 grid-wide) |
| `scripts/rh/day004_missing_terms_N.py` | N-profile of the missing tail (law check, second order ½N^{−s}, zero vs between rows) |
| `scripts/rh/day004_s_walk_gpu.py` | all-GPU S(t) walk (GPU port of Z_rs + vartheta; 0.5 s for 4.5 M pts) + S_t_walk_1e4_1e5_gpu.txt |
| `scripts/rh/day004b_onset.py` | zero-onset vs (t/N): C~\|I\| at t/N ≈ 2 (GPU; N=10⁵ rows >10⁵ flagged: EM cap, 6.3) |
| `scripts/rh/day004b_s_walk_1e6.py` | S-walk 1e5→1e6 dt=0.02 (diagnostic; **count is −38: missed twins** — see day-004 §6.2) |
| `scripts/rh/day004c_twinfix_walk.py` | corrected S-walk 1e5→1e6 dt=0.005 (N(1e6)=1,747,142; S(1e6)=−2.5086; 61 s) |
| `scripts/rh/day004d_twin0021.py` | nested dt=0.0025 re-walk: count stability (exact agreement = no residual twins) |
| `scripts/rh/day004f_twin_gap_map.py` | the 19 twin gaps in (1e5,1e6] (Z_rs-bisected + dip + mpmath sign probes) |
| `scripts/rh/day005_s_walk_1e7.py` | streaming S-walk 1e6→1e7, dt = 5e-4 (twin floor ≈ 9e-4 projected; per-decade stats, ~1.8e10 pts) |
| `scripts/rh/day005_law_chi5.py` | the χ₅ missing-term law: −A(N)N^{−s} + (2s/5)N^{−s−1} + O(N^{−s−2}); c(t) = \|2s/5\|;
| `scripts/rh/day005_band_density.py` | Fibonacci primitive-prime band density S(N) baseline (Zsigmondy exceptions {6, 12}) |
| `scripts/rh-ts/` | **all new code from day 5**: TypeScript, functional style (no for/if, while allowed, ternary branching, one function per file, descriptive names, lint after every edit — `npm run check` = strict tsc + eslint no-restricted-syntax; `npm test` = 32/32 node:test goldens). 15 one-function modules + `run-law-chi5.ts` (4/4 goldens PASS) + `run-band-density.ts` (7/7 PASS) cross-validated against python. Python = legacy verified instrument only. |

GPU scripts run under `~/venvs/cupy/bin/cupy_py` (cuPy 14.2.0 ROCm wheel +
LD_LIBRARY_PATH wrapper; system python untouched).
| `scripts/rh/mpmath_audit.py` | independent verification of the census (mpmath dps 50/80, pinned container) |
| `scripts/rh/out_*.txt` | canonical outputs (committed; re-runnable) |
| `plan/40-prize-islands/rh-attack/day-NNN.md` | daily reports |

## How to run

```bash
cd scripts/rh
python3 day001_primes.py    # ~30 s  (host python3, numpy only)
python3 day001_zeta.py      # ~90 s  (writes zeros_T10000.txt)
python3 day002_mirror.py             # ~3 s
python3 day002_fibonacci_closeout.py # ~1 s (needs zeros_T10000.txt)
python3 day003_mirror_scaling.py     # ~3 s
python3 day003_census_1e5.py         # ~5 min  (writes zeros_T100000.txt)
docker run --rm -i -v "$PWD":/work kainos-dev:dev \
  sh -c "pip -q install mpmath && cd /work && python3 day003_s_arg_mpmath.py"
docker run --rm -i -v "$PWD":/work kainos-dev:dev \
  sh -c "pip -q install mpmath && cd /work && python3 mpmath_audit.py"
docker run --rm -i -v "$PWD":/work kainos-dev:dev \
  sh -c "pip -q install mpmath && cd /work && python3 mpmath_audit_beta.py"
# verified day-4b pattern (no -v: host /tmp not mounted; pipe a standalone script via stdin):
docker run --rm -i kainos-dev:dev python3 - < /tmp/mpmath_check.py
# GPU walks (from scripts/rh):
~/venvs/cupy/bin/cupy_py day004c_twinfix_walk.py   # ~61 s
~/venvs/cupy/bin/cupy_py day004d_twin0021.py       # ~2 min (dt=0.0025 stability)
python3 day004f_twin_gap_map.py                    # ~1 min (19 twin gaps, CPU Z_rs)
~/venvs/cupy/bin/cupy_py day004b_onset.py          # ~2 s (onset t/N table)
```

## Report contract (daily)

The daily cadence is scheduled: `crontab -l` → `0 7 * * *` runs
`scripts/rh/daily_report.sh` (headless `pi -p` session, 07:00 local), which
do's the queue item, files the next `day-NNN.md`, and commits the rh paths.
Log: `scripts/rh/cron.log`.


Each `day-NNN.md` must contain:
1. **What was built/measured** (with the exact numbers from `out_*.txt`).
2. **Verdicts** on the claims under test (RH-DIRECTION.md, RH-TRIAL-POINT.md,
   or the day's hypothesis) — each True-with-name-of-real-object /
   Falsified-with-computation / Unmapped-wall.
3. **Interesting findings** (the owner gets the interesting things first).
4. **The named missing ingredient** in store language (rh-reach vocabulary:
   "zero control in the critical strip"; criterion-gap: x·e^{−c√log x}
   vs. required x^{1/2+ε}).
5. **The exact next question** and the next-day queue.

## Current state (end of Day 005, 2026-09-09)

- **All new code is now TypeScript** (`scripts/rh-ts/`): functional style
  (no `for`/`if`, `while` allowed, ternary branching, one function per file,
  lint after every edit — `npm run check` = strict tsc + eslint
  no-restricted-syntax; `npm test` = 32/32 node:test goldens). Python is
  retained only as the legacy verified instrument (engines, data producers,
  mpmath verifier). The day-4 python draft's bug class (silent arithmetic)
  produced a 7-bug census on first TS draft — each caught by the gates
  before composition; two recurred *from the python* (fib base case +
  pair-slot), which is why goldens are computed, not copied.
- **χ₅ missing-term law (fusion bridge), measured in both stacks:**
  Σ_{n>N} χ₅(n)n^{-s} = −A(N)N^{-s} + (2s/5)N^{-s-1} + O(N^{-s-2}); the
  pole integral becomes a bounded discrete band-residue (A = 5-periodic
  residue); per-decade raw decay 10^{1.5}; c(t) = |2s/5| to ~1% for
  t ≤ 1000. TS re-measurement: 4/4 cross-checks PASS vs python, 0.5 s.
- **Band density (both stacks, 7/7 cross-checks PASS, 1.3 s):** B(n) = Σ
  1/q over primitive prime divisors of F_n (bigint pipeline: fast doubling,
  trial+Pollard-rho, exact order via F_n mod q); S(10) = 0.702846,
  S(100) = 1.265391; Zsigmondy B(6)=B(12)=0; fit S ~ N^{0.2529} over
  n ≤ 100 (sub-logarithmic power, not saturated in range). Degenerate
  primes {2, 5} excluded from the order criterion (5 ramifies, 2 degenerates).
- **Onset curve re-verified (N=1e5 column, EM cap 1.2M):** t/N scaling to
  4 digits below t/N = 2; **N-dependence appears exactly at the t/N ≈ 2
  bend** (1.062 at N ≤ 1e4 vs 1.473 at N = 1e5); above it r → 1, C/|I| ~
  160–180 with C ~ (t/N)^{-0.6±0.1}; jump to 7980 at t/N = 50 (next
  regime, probably EM-side floor).
- **S(1e7) walk:** dt = 5e-4 (≈2× the projected twin floor), 1.8e10
  point-evaluations, streaming per-decade stats; RUNNING at report time —
  numbers + dt/2 stability re-walk land in this file/README on completion.
- (Earlier state retained: S(1e6) corrected N = 1,747,142, S(1e6) =
  −2.5086, 2K = −2 at 5e5 and 1e6; twin-floor protocol; EM-cap defect;
  CuPy on the 8060S, 12.5×–1240×; N(1e5) = 138,065 verified.)
- **Day-006 queue:** S(1e7) dt/2 re-walk + 2K(1e7) dps-40 (1e7 and 5e6);
  S-growth-over-three-decades statement; band baseline to n = 10³–10⁴ in
  TS; χ₅ O(N^{-s-2}) remainder quantified (c(1000) drift), χ₁₃ check;
  TS CPU port of the 2-term RS engine as a verified reference instrument.
