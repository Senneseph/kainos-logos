# PROMPT M2 — TS port of the onset pipeline (development side)

CONTEXT.
- spec/onset-bridge-e7b1.md (what it computes + error budget)
- spec/zero-core-engine.md (the TS home of Z(t), ϑ, the selftest gate)
- Python reference: scripts/rh/day009_e7b2_onset_pred.py + its output
  (out_day009_e7b2_onset_pred.txt) — the goldens, per P-0.3/P-0.7.
- TS stack: scripts/rh-ts/ (39/33… 39/39 tests; npm run check).

WHY TS. Owner directive 2026-09-09: new development in TypeScript;
Python frozen as oracle. Float64 is SUFFICIENT here: the ±2e6-log-
unit cancellation lives in log-space accumulators (la, ar, T) whose
float64 error ~1e-9 in log units ≪ the 1e-3 test budget; the final
exp() sees O(1-20) arguments. (If any point needs better, that point
goes back to the frozen mpmath oracle — don't bignum-port.)

MODULES (one file each, rh-ts/src + test).
- pair-factor-of.ts — the EXACT on-line pair factor
  e^{½/(¼+γ²)}·(1−(¼+t²)/(¼+γ²)) (real) + its log (branch: sign →
  phase 0/π). Test: closed form vs the complex-product value
  (1−s/ρ)e^{s/ρ}·(1−s/(1−ρ))e^{s/(1−ρ)} at 8 random (t,γ), 1e-12.
- zero-product-log.ts — (la, ar) accumulation over the zero list (both
  signs), log-space; streaming (chunks) to bound memory. Test: at
  s=2 (ℜ>1) product→ζ convergence to 1.4e-11 at G=1e5 (the verified
  classical anchor).
- tail-integral.ts — ∫_G^∞ pairlog·(ln(γ/2π)/2π) dγ, composite
  Simpson / Gauss on a fixed γ-grid in log-spaced intervals
  (no scipy; the integrand is smooth & monotone-decay beyond 2t).
  Test: tail(3e5, t=1e4) vs the mpmath quad value (recorded oracle),
  1e-6 relative.
- onset-predict.ts — C_zero/|I| for the 15 measured points (N, t/N).
  Test: goldens = the Python mpmath first run (1e3 line to 1e-6;
  points inside its error budget: tolerance = the budget, not 1e-6 —
  encode the budget in the test).

ENGINE. Reuse rh-ts/src/rs-z-value-of-t.ts (Z, ϑ) for the |ζ|
reference and the Ψ-error channel; the partial sums Pn and I are
plain float64 (N ≤ 1e5).

DONE WHEN. npm run check clean; npm test green including the s=2
convergence golden and the 15-point golden table; the TS output for
the testable points matches the Python oracle within 5e-4 relative.
OUT OF SCOPE. dps/bignum (frozen oracle owns that), the G=1e6+ lists.
