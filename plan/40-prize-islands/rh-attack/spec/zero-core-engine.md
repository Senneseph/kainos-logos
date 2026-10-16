# SPEC — zero-core-engine (Riemann–Siegel Z(t), both languages)

PURPOSE. Evaluate Z(t) = e^{iϑ(t)} ζ(½+it) and count zeros (sign changes).
Two homeomorphic engines must agree: Python `scripts/rh/zeta_core.py`
(oracle side, hosts the dps mpmath cross-checks) and TypeScript
`scripts/rh-ts/src/rs-z-value-of-t.ts` (development side — new engine work
goes here per owner directive 2026-09-09: Python is DONE except where
mpmath dps precision is the whole point).

FORMULA (FORMULAS.md §2; read source DLMF 25.10.2/25.10.3).
Z = 2·Σ_{n≤N} cos(ϑ − t·ln n)/√n + (−1)^{N−1}[Re ψ(p)/u − ψ‴(p)/(96π²u³)],
N = ⌊(t/2π)^{½}⌋, p = (t/2π)^{½} − N, u = (t/2π)^{¼};
ϑ(t) = Im ln Γ(¼ + ½it) − ½t ln π;
ψ‴(p) = −Im[S]/h³ (complex-step, h = 1e-3; the Re[S] version was a
bug — day-007, caught by the TS port's γ₇ golden).

INVARIANTS / GOLDENS.
- zeta_core.selftest() gate on every entry point.
- Known-zero goldens: γ₇ = 40.91871901214749130, γ₁₀₀ = 236.524229…;
  Z(γ) ≈ 0 and sign-change structure (P-0.7).
- GPU-vs-host cross-check at 12 scattered points before any bulk run
  (tol 1e-6, float64).

VALIDITY MAP (MEASURED, day-009).
- t ≥ 1e5: twin-safe (error ~1e-8 ≪ |Z'|·dt). This is the certified zone.
- t in [1e4, 2e4]: NOT twin-safe: 38/20 missed flips on [1e4, 1.9e4]
  vs the certified zero list N(1.9e4) = 21,211 (engine error ~5e-4
  corrupts signs within ~3e-5 rad of a zero).
- t < 1e4: same class, worse. LOW-t sign-walk evidence from float64
  2-term is unreliable — use dps (frozen oracle) there.
- The 1.03e5 EM-cap defect (engine) was found day-4/5; the S(1e7) GPU
  chunk defect (one dead 256k-point tile, 246 missed flips) is a
  device-memory event, corrected by the running dt025 re-walk.

STATUS. Both engines current; selftest + goldens green; TS stack
39/39. Python engine frozen as oracle; no new features there.
