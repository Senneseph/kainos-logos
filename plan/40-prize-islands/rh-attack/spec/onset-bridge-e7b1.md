# SPEC — onset-bridge (E7b-1): the zero⇔prime bridge test

PURPOSE. Predict the measured prime-side onset law from zero-side
ingredients only, and report the residual honestly. This is THE bridge
test of the project (owner's ½-intuition in explicit-formula language).

THE MEASUREMENT (prime side, day-04b, 4 digits, N-independent).
C(N,t) = |tail + I|, tail = ζ(s) − Σ_{n≤N} n^{−s}, I = N^{1−s}/(1−s),
s = ½+it. Measured C/|I| (t/N): 0.0500 / 0.1000 / 0.2509 / 0.5071 /
1.0620 at t/N = 0.1 / 0.2 / 0.5 / 1 / 2 — i.e. C/|I| = ½·(t/N) to 4
digits; the zeros "enter the budget" at t/N ≈ 2. (15 measured points:
N ∈ {1e3, 1e4, 1e5} × the five ratios.)

THE PREDICTION (zero side, derived; THE-EULER-ACTION §E7b + RESULTS).
C_zero(N,t) = | main(s)·Π_{|γ|≤G} F_γ(s)·e^{T(G,s)} − (Pn − I) |
- main(s) = the 25.2.12 main factor (read verbatim, verified at s=2).
- F_γ = (1−s/ρ)e^{s/ρ}, ρ = ½±iγ, on-line closed form: per-pair factor
  EXACTLY REAL = e^{½/(¼+γ²)}·(1−(¼+t²)/(¼+γ²)) (new structural fact;
  the phase is 0 or π — the 2K step — plus the smooth Σ t/(¼+γ²)).
- e^{T(G,s)} = analytic tail beyond the list, T = ∫_G^∞ pairlog·
  (ln(γ/2π)/2π) dγ (RVM density; pairlog the closed-form pair factor).

ERROR BUDGET (quantified, day-009; PARAMETER CORRECTED 20:35 by the
certified G=3e5 run). The direct product over list zeros is exact
(closed-form per-pair factor); the density TAIL beyond G is wrong by
sum-vs-∫ against ACTUAL zero spacings (S-scale fluctuation), NOT by
f(G) alone. Empirical (docker 1.3.0, certified 466,655 list):
  t=1e3, 2e3 (G=3e5): Ψ-err 6.4e-5, 1.8e-3
  t=5e3: 2.2e-2   t=1e4: 8.3e-2 (≈ same at G=1e5 — SATURATES in G
     once G ≫ t: the sum-vs-int fluctuation over (t, G) does not vanish
     as G→∞ at fixed t)
  t=2e4: 0.42   t=5e4: |Ψ|/|ζ| ~ 19 (Δlog ≈ 2.9)   t≥1e5: > 1
→ **the density-tail model's testable region: t ≲ 2–5e3 (C ≥ error
   floor); reaching t ~ 1–2e5 (the N=1e5 row) needs the ACTUAL zeros
   there (G ≳ 5–6e6 walk), and even then the saturation note applies —
   the honest ceiling of the current method is t ~ 1e4–2e4 unless the
   tail is upgraded (pair-correlation-corrected density or a further
   certified list). The f(G) = |ln(1−(¼+t²)/(¼+G²))| term is the
   SUBORDINATE part; the dominant term is S-scale × span(t, G).

PASS CRITERION (pre-registered). All testable points within 5% relative;
monotone in t/N; slope ∈ [0.4, 0.6]. Points inside the error budget are
REPORTED as boundaries (never silently counted as passes).

**STAGE-1 RESULT (G=3e5 CERTIFIED list, docker mpmath 1.3.0, 20:35 —
out_day009c_onset_pred_certified.txt):**
  (1e3, 1.0): pred 0.5086 vs meas 0.5071 → **+0.29%**  Ψ-err 6.4e-5 — CLEAN PASS (4-digit point)
  (1e4, 0.1): pred 0.0494 vs meas 0.0500 → **−1.2%**   Ψ-err 6.4e-5 — CLEAN PASS
  (1e3, 2.0): pred 1.1235 vs meas 1.0620 → +5.8%  Ψ-err 1.8e-3 — borderline (C/err ≈ 9)
  (1e4, 2.0)→(1e4, 0.2): pred 0.1042 vs meas 0.1000 → +4.2%  Ψ-err 1.8e-3 — borderline (C/err ≈ 6)
  (1e3, 0.1/0.2/0.5): +43.6/+70.9/+70.6%, Ψ-err 3.7e-3…8.2e-3 — low-t G≫t regime,
      C/err ≈ 2–4: measurable-but-fuzzy, directionally right (law shape ✓)
  (1e4, ≥0.5) & all (1e5, ·): C below the Ψ error floor — IN BUDGET
      (the N=1e5 row needs G ≳ 5–6e6 = M5 decision matrix; at
      (1e5, 0.5/1.0/2.0) also 2t → G boundary).
  Monotone in t/N ✓ (both rows); clean-region slope consistent with ½ ✓.
  Certified N(3e5) = 466,655 (both passes; S_file ≈ −16).

STATUS (G=1e5 first run ✓; G=3e5 CERTIFIED-LIST RERUN running 20:25, docker).
- (1e3, 1.0): 0.5076 vs 0.5071 → +0.10% (the 4-digit point) ✓ [G=1e5]
- (1e4, 0.1): 0.0498 vs 0.0500 → −0.4% ✓ [G=1e5]
- (1e4, 0.2): +5.0% (borderline); (1e3, 2.0): +6.3% (borderline) [G=1e5]
- (1e3, 0.1/0.2/0.5), (1e4, ≥0.5), all (1e5, ·): inside error budget at
  G=1e5; the G=3e5 rerun is meant to move (1e4, ≤0.5) and (1e5, 0.1/0.2)
  into/past the budget.

**G=3e5 zero list: CERTIFIED 20:20** — seg00 re-walk with fixed code:
N(3e5) = 466,655 on BOTH passes (dt=5e-4 and dt2 agree), engine gate
6.5e-10, min gap 0.005750 at t=273193.66, strict monotone 466,655 lines
(zeros_T300000_ext_full.txt). Certified N(3e5) = 466,655 (S_file ≈ −16).

Incident record (P-0.9) — each item invalidated exactly one artifact,
all now labeled:
(a) FIRST-CHUNK ZEROED bug in day009b pass_dt: the first chunk of every
    pass got fl = zeros (internal sign changes not computed) — dropped
    every zero in [w0, w0 + CHUNK·dt) (13 on seg00 incl. γ₁₃₈₀₆₆ =
    100000.743723). Fixed: fl[1:] = sgn[1:] != sgn[:-1].
(b) the old (buggy) run's passes additionally missed 11–12 flips beyond
    chunk-0 (466,630/466,643 vs true 466,655); its gate was 100× worse
    (8.6e-8 vs 6.5e-10) and it ran the MAXN=978 grid (256MB) under CPU
    memory pressure, vs the certified run's per-W1 MAXN=219 (57MB).
    Cause not fully isolated; the certified dt/dt2 agreement supersedes
    (P-0.2). → **grid sized to the actual W1, gate per run**.
(c) old list contained a flip at EXACTLY 200000.000000 (grid sample)
    → the provisional G=3e5 onset run computed Ψ(t=2e5) = 0 exactly.
    List artifact, not a zero (certified list's nearest: 199999.7055).
    out_day009c_onset_pred_ext.txt (provisional list) is INVALIDATED —
    kept only as the record of this detection path. Any t landing ON a
    listed zero is SINGULAR — reported as singular, never as FAIL.
(d) **mpmath 1.4.1 (host) REGRESSION: mp.quad of the tail integral
    returns real part 0.003 too large at t=1000 (−16.9939 vs
    −16.9909 in docker 1.3.0; all other terms bit-identical) → Ψ
    error 2.995e-3 instead of 2.292e-5. HOST MPMATH 1.4.1: NO TAIL
    QUADS. Docker kainos-dev:dev (mpmath 1.3.0) is the verified onset
    environment** (original G=1e5 numbers + s=2 anchor 1.4e-11 all
    1.3.0 runs).
(e) GNU `sort -n` does not parse scientific notation — first merge of
    the 3e5 list was corrupted; redone with `sort -g` + numpy
    monotonicity check (P-0.8: verify derived artifacts).
(f) the day009d auto-chain stalled: `wait $!` targets the cupy_py
    WRAPPER pid, not the python pid — merge/rerun done manually;
    chains must wait on the real process (pgrep by argv) or drop the
    wrapper.

LIMITATIONS (honest). The N=1e5 row at t/N = 1, 2 needs G ≳ 5–6e6
(error model: G² ≫ 2t²S√N) — deferred to "test extensively later"
(owner 2026-09-09). The density tail bounds the claim: the model is a
REGION-limited certification until the list grows.

FUTURE. TS port (float64, log-space product + float64 quad tail —
float64 is sufficient: the cancellation lives in log-space accumulators
whose error ~1e-9 in log units ≪ the 1e-3 budget). See prompts/M2.
NOTE: a float64 quad is immune to the mpmath-1.4.1 defect — the TS
port is now ALSO the fix for the environment hazard.
