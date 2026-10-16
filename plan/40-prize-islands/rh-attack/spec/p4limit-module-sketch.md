# P4Limit — LEAN MODULE SKETCH (what the M→∞ passage needs, before any code)

*Operational decomposition of the P4 spec (`p4-tail-law-abstract.md`) §T2–T4.
Not a status report; a shopping list with a dependency ledger. Green so far:
P4Em (1st order, verbatim port), P4Tail (per-period), P4Em2 (`em2_finite` +
`ico_sum_telescope`). This module = the M→∞ passage with explicit remainder
bounds, ending in the P4 statement (zero-free bound `B_n(t)`). The T5 float
gate is a separate module (P4Float), out of scope here.*

---

## 1. The exact mathematical content, atom by atom

Throughout: `s = ½ + i t` (t : ℝ, so Re s = ½, s ≠ 1, 1−s ≠ 0), `n : ℕ`,
`n ≥ 1`; `f(x) := (x : ℂ)^{−s}` on x > 0; `P_n = Σ_{k≤n} k^{−s}`;
`I(n,s) := n^{1−s}/(1−s)`; `W_n(s) := riemannZeta s − P_n s + I(n,s)`
(the spec §0.5 corrected sign). All constants explicit, zero-free.

**Atom L1 — derivatives of f (x ↦ (x:ℂ)^{−s}), x > 0:**
  f′(x) = −s·(x:ℂ)^{−s−1},   f″(x) = s(s+1)·(x:ℂ)^{−s−2}
Mechanical via the pinned `deriv_ofReal_cpow_const`
(Mathlib/Analysis/SpecialFunctions/Pow/Deriv.lean:306, per spec) applied
twice (c = −s, then c = −s−1; neither is 0, s = ½+it).
Dependency: verify the lemma's exact hypotheses at 4.33.1 (x ≠ 0 suffices
for our domain). **STATUS: local pin (mathlib), no online resource needed.**

**Atom L2 — the finite EM rearrangement (identity; all s with 1−s ≠ 0; every M ≥ n):**
  A(M,s) := Σ_{k≤M} k^{−s} − M^{1−s}/(1−s) + ½·M^{−s} + (s/12)·M^{−s−1}
           = P_n − I(n,s) − ½·n^{−s} + (s/12)·n^{−s−1}
             − ½·∫_n^M B̂₂({x})·s(s+1)·(x:ℂ)^{−s−2} dx          (L2)
where A(M,s) is the 2-subtracted running sum whose limit IS the continuation
(measured: A(M) − ζ at 1/√M rate).
Mechanical from `em2_finite` (green) + L1 + the antiderivative
`∫ x^{−s}dx = x^{1−s}/(1−s)` + ring-level rearrangement. EXACT, no limits,
no ζ.
Dependencies: antiderivative pin (cpow integral over ℝ → ℂ); periodic
Bernoulli `B̂₂(u) = B₂(u − ⌊u⌋)` as a local def; continuity/derivability
hypotheses for `em2_finite` instantiated at 𝕜 = ℂ (its statement is RCLike
generic — ℂ qualifies; needs the twice-differentiable proof, from L1).
**STATUS: assembly from green local pieces; the only genuinely new
statement in the module is its RHS integral form.**

**Atom L3 — absolute convergence of the kernel integral, Re s = ½:**
  ∫_n^∞ B̂₂({x})·f″(x) dx converges absolutely, and
  |f″(x)| = |s||s+1|·x^{−5/2}  (decreasing in x).
Consequence: `A(M,s)`'s RHS in (L2) has a limit as M → ∞, namely
  lim = P_n − I(n,s) − ½·n^{−s} + (s/12)·n^{−s−1} − ½·∫_n^∞ B̂₂({x}) f″(x) dx.
Hence the LHS (the 2-subtracted running sum) converges too — **by the
identity, not by any series argument** (the raw series diverges at σ = ½;
the abscissa is exactly 1 — spec §T1, computed day-017).
Dependencies: `intervalIntegral` over [n, ∞) for ℝ → ℂ (limit-of-finite
intervals), absolute convergence by comparison with ∫_n^∞ x^{−5/2}
(p-power integrability pin — standard mathlib).
**STATUS: standard mathlib machinery to be located; no research risk.**

**Atom L4 — the OP family (the two remainder-bound lemmas; the analytical
heart of the module; ℝ → ℝ valued; h : ℝ → ℝ decreasing, h → 0, and
h(x) = O(x^{−5/2})-summable on [n,∞)):**
  OP1 (crude, fallback):  |∫_n^∞ B̂₂({x}) h(x) dx| ≤ (2·sup|B̂₂|)·h(n) = h(n)/3.
      period split; ∫₀¹ B̂₂ = 0 lets each period be rewritten against the
      constant h(n+j); |Δ_j| ≤ h(n+j) − h(n+j+1); telescope.
  OP2 (shipped, refined):  |∫_n^∞ B̂₂({x}) h(x) dx| ≤ (max_{[0,1]}|B₃|/3)·h(n)
      = (√3/108)·h(n).
      Δ_j(u) = ∫₀ᵘ (−h′)(n+j+v) dv; Fubini on [0,1]² (finite intervals);
      ∫ᵤ¹ B̂₂ du = −B₃(u)/3 (B₃(1) = 0); |B₃| ≤ √3/36 — closed form,
      attained at (3±√3)/6; √3/36 < 1/20 via norm_num; telescope.
Apply with h = |f″| (or componentwise to Re f″ / Im f″):
  |−½∫_n^∞ B̂₂ f″| ≤ ½·(√3/108)·|s|(|s|+1)·n^{−5/2} = (√3/216)|s|(|s|+1)n^{−5/2}.
Dependencies: Fubini on the finite [0,1]² (standard); the B₃-maximum lemma
(one local lemma: `max |B₃| on [0,1] = √3/36`, calculus + norm_num);
telescoping sums (pattern already used in `ico_sum_telescope`).
**STATUS: CANDIDATES FOR ONLINE REUSE (AFP `Euler_MacLaurin` bound form,
published proofs of the B₃-kernel EM remainder) — LEAN PROOF IS FALLBACK
per owner directive. Cross-check the constants against a published
source; do not just trust our derivation.**

**Atom L5 — the cited 1859 identity + the P4 statement (composition root):**
  [CITED, not Lean-proved — the B-3 no-ζ-identity convention, spec §0.5/§T1,
   role of DLMF 25.2.12; numerically verified day-017 at the 1/√M rate:]
      lim_{M→∞} A(M, ½+it) = riemannZeta (½ + it).
  Combined with (L2)+(L3) this is EXACTLY the strict identity
      W_n(s) = −½·n^{−s} + (s/12)·n^{−s−1} − ½·∫_n^∞ B̂₂({x}) f″(x) dx   (P4-id)
  where W_n is defined via `riemannZeta` (the ζ-anchor at Re s > 1,
  `zeta_eq_tsum_one_div_nat_cpow`, is the only ζ-touching fact, and it is
  available in mathlib — pin to confirm).
  **THE P4 STATEMENT (zero-free explicit bound, zero-free, computable):**
      |W_n(t)| ≤ B_n(t) := ½·n^{−1/2} + (|s|/12)·n^{−3/2}
                      + (√3/216)·|s|(|s|+1)·n^{−5/2},    s = ½+it,
  by triangle inequality on (P4-id) with OP2: the first two terms are exact
  magnitudes (|n^{−s}| = n^{−1/2}, |n^{−s−1}| = n^{−3/2}); the third is
  OP2. Every constant explicit; nothing implicit or fitted.
  **The T4 corollary (the strictified measured law):** with |I| = n^{1/2}/|s|:
      |W_n|/|I| ≤ (|s|/2)/n + (t²+¼)/(12·n²) + (√3/216)·(t²+¼)·(|s|+1)/n³
  — pure division algebra from the statement; the measured 15-point table
  (0.0500 … 1.0620) is checked against these discs by the P4Float gate (T5),
  not here.

## 2. Dependency ledger (look for vs invent) — UPDATED after research (day-019 turn)

| Atom | Need | Local (pinned/green) | Online (found) | Invention (fallback) |
|------|------|---------------------|-----------------|----------------------|
| L1 | cpow real-arg derivs ×2 | `Complex.deriv_ofReal_cpow_const {x : ℝ} (hx : x ≠ 0) (hc : c ≠ 0)` (Analysis/SpecialFunctions/Pow/Deriv.lean:303 — exact, hypotheses are just x ≠ 0, c ≠ 0 ✓) | — | hypothesis juggling only |
| L2 | antiderivative x^{−s} on ℝ→ℂ; B̂₂; C² proof of f | IBP family: `MeasureTheory/Integral/IntervalIntegral/IntegrationByParts.lean` (full: deriv_mul/mul_deriv/smul variants + comp variants); P4Em.lean already uses `integral_mul_deriv_eq_deriv_mul` — PROVEN pattern; B̂₂ = `RhAttack.P4Tail.B2` (green, reuse via import, P4Em2 precedent); additivity `sum_integral_adjacent_intervals_Ico` (used) | — | the L2 identity assembly (mechanical) |
| L3 | ∞-interval kernel integral, abs convergence | `MeasureTheory/Integral/IntervalIntegral/Periodic.lean` (found): `intervalIntegral_add_zsmul_eq`, `sInf_add_zsmul_le_integral_of_pos`, `integral_le_sSup_add_zsmul_of_pos`, `tendsto_atTop_intervalIntegral_of_pos` — periodic-primitive machinery, the exact shape of the tail-limit argument; comparison integrability (standard names, pin at draft time) | — | comparison proof (standard) |
| L4 | OP1/OP2 period-split bounds; max B₃ = √3/36 | `Periodic.lean` as structural template; `Polynomial.bernoulli` + `deriv_bernoulli_add_one` (Bₖ₊₁′ = (k+1)Bₖ — the B₃/3 antiderivative fact); `ico_sum_telescope` pattern | AFP `Euler_MacLaurin` (sup-pbernpoly bound shape); DLMF 25.2.9 (published B̃₃-kernel counterpart of the same remainder) | **the OP lemmas themselves** (~15 + ~25 lines); max-B₃ lemma (constant computed, see §5) |
| L5 | cited continuation identity; algebra | `zeta_eq_tsum_one_div_nat_cpow {s} (hs : 1 < re s)` (LSeries/RiemannZeta.lean:207) + `riemannZeta := hurwitzZetaEven 0` (:121) | **DLMF 25.2.8** (citable: ℜs > 0, Apostol Thm 12.21) + Tao 2010 expository | — (citation + division algebra) |

## 3. Research checklist (this turn — online BEFORE any Lean)

1. **EM with Bernoulli remainder, formalized**: Lean 4 (mathlib / zeta-23-lean
   / other repos), Isabelle AFP `Euler_MacLaurin` (statement shape of the
   bound — for cross-checking OP1/OP2 constants and route), Coq.
2. **The A(M) → ζ continuation identity** (2-subtracted sums → analytic
   continuation, Re s = ½): published form we can cite precisely in the
   header (DLMF 25.2.12? Titchmarsh Ch. IV? — name + page for the header).
3. **max_{[0,1]} |B₃| = √3/36**: published occurrence of the constant
   (EM third-order remainder literature) to cross-check our closed form.
4. **mathlib 4.33.1 stock** (local docs per goal methodology): exact
   statements of `riemannZeta` + tsum lemma; `summable`/Dirichlet for
   re>1 series; `intervalIntegral` infinite-interval + AtTop convergence
   APIs; p-power integrability; `deriv_ofReal_cpow_const` hypotheses.

## 4. Constraints carried into the module (store discipline)

- No ζ-identity in Lean at Re s = ½ beyond the cited 1859 line (B-3
  convention); the re>1 anchor is the only ζ-touching fact.
- No Float↔ℝ coercion; the T5 float gate stays a separate object.
- Every constant computed or cross-checked against a published source
  (√3/36, h(n)/3, 1/12, √3/216) — never recalled.
- Atomic files (`RhAttack/P4Limit.lean` or split L4 into its own file if it
  grows), uniform headers, zero sorry, git per green atom.
- OP1 first, as the fallback; OP2 shipped once green (spec §T3).

## 5. Research log (day-019 turn — owner directive: sketch → research → Lean as FALLBACK)

### Online resources found (borrow / cross-check, don't reinvent)

1. **DLMF 25.2.8** (dlmf.nist.gov/25.2#E8) — **the published CITATION for the
   A(M)→ζ continuation itself**:  ζ(s) = Σ_{k=1}^N k^{−s} + N^{1−s}/(s−1)
   − s∫_N^∞ (x−⌊x⌋)x^{−(s+1)} dx,  **ℜs > 0**, N = 1,2,3,…
   (Apostol 1976 Thm 12.21 p. 269, via a=1, N↦N−1; A&S 23.2.9).
   Also gives W_n = −s∫_n^∞ {x} x^{−s−1} dx directly (sawtooth kernel) —
   the IBP-chain start of our second-order form.
2. **DLMF 25.2.9, n = 1** (A&S 23.2.3) — **the published second-order form**:
   ζ(s) = Σ_{k=1}^N k^{−s} + N^{1−s}/(s−1) − ½N^{−s} + (s/12)N^{−s−1}
          − (s(s+1)(s+2)/6) ∫_N^∞ B̃₃(x) x^{−(s+3)} dx,   ℜs > −2,
   B̃ₓ = periodic Bernoulli function (DLMF §24.2(iii)).
   → Published counterpart of our T3/P4-id: SAME head terms (−½N^{−s},
   (s/12)N^{−s−1} — the s/12 sign now pinned by a published statement too,
   in addition to day-017 numerics).
3. **Tao, “The Euler-Maclaurin formula, Bernoulli numbers, the zeta function,
   and real-variable analytic continuation” (2010-04-10)** — expository
   derivation of exactly this continuation route with explicit remainders;
   secondary citation for the header.
4. **Isabelle AFP `Euler_MacLaurin`** (isa-afp.org) — EM to Banach-valued f,
   textbook + Concrete-Mathematics variants; remainder bound = sup-norm of
   pbernpoly × domination by g→0 → structural cross-check of the OP1/OP2
   bound shape (sup|kernel|·h(n) — ours refines it, spec §0.6/§T3).
5. **anthropics/zeta-23-lean** (commit 3635e748) — `Zeta23/FromPNTPlus/
   EulerMaclaurin.lean` (already ported = our P4Em) + `Mertens.lean`; PR
   #1367 “Upstream first-order Euler-Maclaurin to Mathlib” confirms mathlib
   carries the polynomial `bernoulliFun` but the periodic family and EM
   remainder-lemmas are NOT upstreamed → local invention of L4 is the gap,
   as the spec said.

### Local mathlib 4.33.1 pins (grep-verified this turn, exact names)

- ζ-anchor (T1): `zeta_eq_tsum_one_div_nat_cpow {s : ℂ} (hs : 1 < re s)`
  (LSeries/RiemannZeta.lean:207); `riemannZeta := hurwitzZetaEven 0` (:121).
- IBP: `MeasureTheory/Integral/IntervalIntegral/IntegrationByParts.lean`
  (full family, incl. smul/RCLike and comp variants); our green P4Em.lean
  already calls `intervalIntegral.integral_mul_deriv_eq_deriv_mul`.
- Periodic integrals: `IntervalIntegral/Periodic.lean` (NEW find) —
  `intervalIntegral_add_zsmul_eq` (∫ over n periods = n·∫ one period),
  `sInf/sSup_add_zsmul_le/integral_of_pos` (primitive bounded by
  X + ⌊t/T⌋·Y — the OP bound shape), `tendsto_atTop_intervalIntegral_of_pos`.
- Bernoulli: `Polynomial.bernoulli : ℕ → ℚ[X]`, `bernoulliFun : ℕ → ℝ → ℝ`
  (ZetaValues.lean:48) with simp facts (`bernoulli_one : X − 2⁻¹`,
  `bernoulliFun_two = X²−X+1/6`), `derivative_bernoulli_add_one` (Bₖ₊₁′ =
  (k+1)Bₖ → B₃/3 antideriv of B̂₂ per period), endpoint facts.
  Periodic B̂ₖ NOT in mathlib → reuse `RhAttack.P4Tail.B2` (green).
- Fubini: `MeasureTheory/Integral/Prod.lean` (exact lemma at draft time).
- Max B₃: not in mathlib → local lemma. **Computed this turn** (script
  `/tmp/p4limit_crosscheck.py`): grid max of |B₃| on [0,1] =
  0.048112522432 = √3/36 to 14 digits, attained at (3−√3)/6 = 0.2113248654.

### Numerical cross-check (computed, not recalled)

n = 100, s = ½ + 10i (t/n = 0.1 — a measured-point setting, measured ratio
0.0500; mpmath 50 dps target; float64 per-period Gauss–Legendre, no kinks
inside a period, J = 120 000 periods):

- |W_target|/|I| = **0.050028** — reproduces the measured law (½·t/n) ✓
- (A) OUR route −½∫B̂₂f″:   |W_target − W_A| = **3.2e-16**
- (B) DLMF 25.2.9 form −(s(s+1)(s+2)/6)∫B̃₃x^{−s−3}: |W_target − W_B| = **3.1e-16**
- **|W_A − W_B| = 3.5e-18** → the two remainders are THE SAME IDENTITY to
  machine precision.

Verdict: the P4 statement's analytic content is externally verified against
the published DLMF/Apostol family + high-precision zeta. What remains to be
INVENTED in Lean is only the *proofs* (L2 assembly, L3 convergence, L4
OP1/OP2, L5 algebra) — every dependency now pinned or templated.

### Next action (pending owner GO — no Lean written this turn, per directive)

Draft `RhAttack/P4Limit.lean`: atom L1 (derivs) → L2 (finite identity)
→ L3 (abs convergence) → L4 (OP1 first, fallback; then OP2) → L5 (P4
statement + T4 corollary), one green commit per atom.

---

## 6. L4 ABSTRACT SPEC (post numeric-refutation turn — the operative spec)

**Method (owner directive): spec → online → numerics → Lean.**
Before writing L4 Lean, the constant in the §1 L5 draft (3rd P4 term
`(√3/216)|s||s+1|·n^{−5/2}`) was numerically tested by an honest
**per-period** summation (`∑_{j≥n} ∫₀¹ B₂̂(u) s(s+1)(j+u)^{−s−2} du`;
a naive single-`quad` over `[n, n+2·10⁵]` gave garbage — 10⁵ unit-scale
features — and had to be discarded).

**NUMERICAL REFUTATION (computed 2026-09-13; script /tmp/l4_check2.py):**
R(s,n) := |∫_n^∞ B̂₂ f″| / (n^{−5/2}|s||s+1|) — the §1-draft constant is
√3/108 = 0.01604 (against the integral; ½ for the W-term).
- t=50, n=10: R = 0.03057 > 0.01604 — **the §1-draft P4 3rd-term constant
  is FALSE.** Same at t=100, n=10 (R = 0.0728).
- The |s+2|-carrying candidates hold at all 15 grid points (t ∈ {0,2,10,
  50,100} × n ∈ {10,100,1000}):
  - (IBP route)  √3/270·|s+2|  — min margin R/candidate = 0.095
  - (MVT route)   7/60·|s+2|   — 15/15 as well, far looser
→ **The P4 statement (L5) must carry an |s+2| factor.** Amended P4
statement:
  |W_n(½+it)| ≤ ½·n^{−1/2} + (|s|/12)·n^{−3/2}
              + (√3/540)·|s(s+1)(s+2)|·n^{−5/2}      (P4-bnd, amended)
(the last = ½ · (√3/270)|s(s+1)(s+2)|n^{−5/2} from A3 below).
The first two terms are unchanged (exact magnitudes). The amended bound
still strictly contains the measured 15-point ratios (0.0500…1.0620);
tightness to be re-verified by the P4Float gate.

**max|B₃| — computed, not recalled:** max_{u∈[0,1]}|B₃(u)| = √3/36 =
0.0481125224324688…, attained at u = (3−√3)/6 (max) and (3+√3)/6 (min);
checked to 50 digits + 20000-point grid.

**The L4 atoms (final):**
- **A0 — the B₃ kernel + basic facts** (local def, mirrors P4Tail.B2;
  mathlib's `bernoulliFun`/`bernoulliFun_two` (ZetaValues.lean) is the
  same polynomial family — used for cross-check only, per the P4 no-ζ-
  core + P4Tail local-kernel convention):
    `B3 x := (x−⌊x⌋₊)³ − (3/2)(x−⌊x⌋₊)² + (1/2)(x−⌊x⌋₊)` (ℝ → ℝ).
  Facts (all by ring/norm_num on the fractional part): B3poly 0 = 0,
  B3poly 1 = 0; `(d/du)B3poly u = 3·B2poly u` (with B2poly = u²−u+1/6 =
  P4Tail's per-period polynomial); ∫₀¹B2poly = 0, ∫₀¹B3poly = 0
  (antiderivatives — `beroulliFun`/`integral_bernoulliFun_eq_zero`
  corroborate); `max |B3poly| = √3/36` (calculus: critical points of
  B3poly' = 3u²−3u+1/2 are (3±√3)/6; value at (3−√3)/6 = √3/36 —
  norm_num + `Real.sqrt` algebra, cross-checked above).
- **A1 — OP1 (crude, fallback)** — h : ℝ → ℝ decreasing, 0 ≤ h, h → 0,
  n : ℕ ≥ 1:  |∫_n^∞ B̂₂({x}) h(x) dx| ≤ (1/3)·h(n).
  Proof: per-period, ∫₀¹B₂̂ = 0 ⇒ period-j = ∫₀¹B₂̂(u)(h(n+j+u) − h(n+j))du;
  |·| ≤ 2·sup|B₂|·(h(n+j) − h(n+j+1)) = (1/3)(h(n+j) − h(n+j+1)); the
  finite sum telescopes; pass M→∞ with `intervalIntegral_tendsto_*`.
- **A2 — OP2 (refined, real decreasing h)** — same h + h absolutely
  continuous with h′ ≤ 0, ∫|h′| < ∞:
  |∫_n^∞ B̂₂({x}) h(x) dx| ≤ (√3/108)·h(n)  ( = (max|B₃|/3)·h(n) ).
  Proof (sketch §1's OP2, now pinned): Δ_j(u) := ∫₀ᵘ −h′(n+j+v)dv;
  IBP with B3poly/3 on [0,1] (B3poly(0) = B3poly(1) = 0 kills boundary
  terms): period-j = (1/3)∫₀¹ B3poly(u)·(−h′(n+j+u))du;
  |·| ≤ (sup|B3|/3)(h(n+j) − h(n+j+1)); telescope.
- **A3 — OP2c (complex decaying exponential — the atom P4 actually uses)**:
  s : ℂ, Re s > −1, s ∉ {−1, −2}, n : ℕ ≥ 1:
    |∫_n^∞ B̂₂({x})·(x:ℂ)^{−s−2} dx| ≤ (√3/270)·|s+2|·n^{−5/2}.
  Proof: per-period IBP with B3poly/3 (boundary terms vanish since
  B3poly(0) = B3poly(1) = 0); = (1/3)∫_n^∞ B3̂({x})·(s+2)·(x:ℂ)^{−s−3} dx;
  triangle: ≤ (sup|B3|/3)·|s+2|·∫_n^∞ x^{−(Re s)−3}dx =
  (√3/108)·|s+2|·n^{−Re s − 2}/(Re s + 2) — at Re s = ½:
  (√3/108)·|s+2|·(2/5)·n^{−5/2} = (√3/270)|s+2|n^{−5/2}.
  (The general-σ statement keeps the `n^{−Re s − 2}/(Re s + 2)` shape —
  Lean-able without specializing the exponent — then a σ = ½ corollary.)
  Numerics: 15/15 grid points, min margin 0.095 (t=50, n=10).
- Apply to P4 (L5): |−½∫ B̂₂ f″| ≤ ½·|s(s+1)|·(√3/270)|s+2|n^{−5/2}
  = (√3/540)|s(s+1)(s+2)|n^{−5/2} — (P4-bnd) above.

**Published cross-checks (online-first, this turn):**
- Boas, "Euler's summation formula" (users.cecs.anu.edu.au/~bdm/eulermac.pdf)
  Thm 1: |R_m| ≤ (2|B_{2m}|/(2m)!))∫|f^{(2m)}| — the crude |B₂̂|-sup form;
  OP1/OP2 are its monotonicity refinements (the standard sharpening).
- Tao 2010 (EM / Bernoulli / ζ post) — same B₂̂-kernel remainder shape.
- DLMF 24.2(iii) periodic Bernoulli functions B̃ₙ.
- mathlib4 (local 4.33.1, `NumberTheory/ZetaValues.lean`): `bernoulliFun`,
  `bernoulliFun_two` (= the B2 polynomial), `hasDerivAt_bernoulliFun`
  (B₃′ = 3B₂), `antideriv_bernoulliFun` (B₃/3 primitive of B₂),
  `integral_bernoulliFun_eq_zero` (∫₀¹B₃ = 0) — cross-check only;
  **no** `periodized_bernoulli` in 4.33.1 (newer-mathlib-only), and the
  P4 line keeps its P4Tail local-kernel convention.

**Dependencies (all local/green or pinned):** intervalIntegral IBP
(`intervalIntegral_mul_deriv_eq_deriv_mul` — P4Em precedent);
`ico_sum_telescope` (P4Em2); `integrableOn_Ioi_cpow_of_lt` +
`Complex.norm_cpow_eq_rpow_re_of_pos` (L3); `intervalIntegral_tendsto_*`
(L3); `abs_B2_le` (P4Tail); the M→∞ passage pattern of L3.

---

## 7. L5 ABSTRACT SPEC (2026-09-13 — post-L4, online-researched pins)

**Method (owner directive): spec → online → numerics → Lean.** All names below
were looked up online (mathlib4 master sources, fetched and read) and then
`#print`-verified against the pinned local mathlib (4.33.1). The tsum
machinery is **`to_additive`-generated** (the additive names are not greppable
as `theorem` lines — the multiplicative originals live in
`InfiniteSum/NatInt.lean` / `Defs.lean`).

**The statement (P4-bnd, amended per §6 — the |s+2|-carrying form):**
for s = ½+it, n ≥ 1:
```
|W_n(s)| ≤ ½·n^{−1/2} + (|s|/12)·n^{−3/2} + (√3/540)·‖s(s+1)(s+2)‖·n^{−5/2}
```
with `W_n(s) := riemannZeta s − P_n s + I(n,s)` (P_n = ∑_{k≤n} k^{−s},
I(n,s) = n^{1−s}/(1−s)); the T4 corollary `|W_n|/|I| ≤ (|s|/2)/n +
(t²+¼)/(12n²) + (√3/540)·(t²+¼)(|s|+1)·… /n^…` by division
(|I| = n^{1/2}/|s| at s = ½+it). The third term: ½·‖s(s+1)‖·(√3/270)·
‖s+2‖·n^{−5/2} — L4.4's `p4_f2_tail_bound` verbatim (f″ = s(s+1)x^{−s−2}).

**L5 atoms (composition from GREEN pieces + the pinned tsum layer):**

- **L5.a — `p4_Tn_Tendsto` (Tendsto language, no tsum):** for Re s > 1,
  `Tendsto (fun m : ℕ => ∑ k ∈ Finset.Ioc n m, (k:ℂ)^{−s}) atTop (𝓝 A)`
  where `A := −(n:ℂ)^{1−s}/(1−s) − ½(n:ℂ)^{−s} + (s/12)(n:ℂ)^{−s−1}
  − ½ s(s+1) ∫_{Ioi n} (B2 x:ℂ)(x:ℂ)^{−s−2} dx`. Proof: pointwise
  `∑_{Ioc n m} = (m^{1−s}−n^{1−s})/(1−s) + ½(m^{−s}−n^{−s}) +
  (1/12)(−s m^{−s−1} + s n^{−s−1}) − ½ s(s+1) ∫_n^m B₂ x x^{−s−2}` from
  **`em2_finite` (GREEN, P4Em2)** + `p4_integral_closed` (L2, GREEN) + L1
  derivatives (GREEN) + L1 `on_Icc` smoothness; then Tendsto-calculus with:
  * decay `(m:ℂ)^r → 0` (Re r < 0): via
    `Complex.norm_cpow_eq_rpow_re_of_pos` + `Real.rpow_neg` +
    `tendsto_rpow_atTop` (0 < y → x^y → ∞) + `tendsto_inv_atTop_zero` +
    `tendsto_natCast_atTop_atTop (R := ℝ)`;
  * kernel: **`p4_kernel_tendsto` (L3, GREEN)** composed with natCast.
- **L5.b — `p4_zeta_split` (the ζ→tail decomposition, Re s > 1):**
  `riemannZeta s − ∑ k ∈ range n, 1/((k+1):ℂ)^s = ∑' i, 1/((n+1+i):ℂ)^s`.
  Pinned: **`zeta_eq_tsum_one_div_nat_cpow {s} (hs : 1 < s.re) :
  riemannZeta s = ∑' (n : ℕ), 1 / ↑n ^ s`** (LSeries/RiemannZeta.lean:207;
  verified `#print`) + **`Summable.sum_add_tsum_nat_add (k : ℕ)
  (h : Summable f) : ∑ i ∈ range k, f i + ∑' i, f (i+k) = ∑' i, f i`**
  (to_additive of `Multipliable.prod_mul_tprod_nat_add`, NatInt.lean:233;
  **protected** — use dot notation) + summability
  **`Complex.summable_one_div_nat_cpow : Summable (fun n => 1/(n:ℂ)^p)
  ↔ 1 < p.re`** (PSeriesComplex.lean, David Loeffler; local ✓) +
  shift invariance `summable_nat_add_iff`.
- **L5.c — `p4_Tn_eq` (the passage):** `∑' i, 1/((n+1+i):ℂ)^s = A` by
  **`Summable.tendsto_sum_tsum_nat (h : Summable f) : Tendsto (fun n =>
  ∑ i ∈ range n, f i) atTop (𝓝 ∑' i, f i)`** (to_additive of
  `Multipliable.tendsto_prod_tprod_nat`, NatInt.lean:56; note the name
  pattern prod→sum per word: `tendsto_sum_tsum_nat`, NOT
  `tendsto_tsum_nat`) + L5.a via the reindex
  `∑_{i ∈ range m} 1/((n+1+i):ℂ)^s = ∑_{k ∈ Ioc n (n+m)} (k:ℂ)^{−s}` +
  `tendsto_nhds_unique` — no HasSum construction needed at all.
  (The `HasSum` def, for reference: `HasSum f a L := Tendsto (fun s :
  Finset β => ∑ b ∈ s, f b) (unconditional β).filter (𝓝 a)`;
  `HasSum.tsum_eq`, `Summable.hasSum` — to_additive of the HasProd
  family in InfiniteSum/Defs.lean; not needed on this route.)
- **L5.d — `p4_identity` (P4-id, Re s > 1):**
  `riemannZeta s − ∑ k ∈ range n, 1/((k+1):ℂ)^s + (n:ℂ)^{1−s}/(1−s) =
  −½(n:ℂ)^{−s} + (s/12)(n:ℂ)^{−s−1} − ½ ∫_{Ioi n} (B2 x:ℂ)
  ((s(s+1) : ℂ) · (x:ℂ)^{−s−2}) dx` — transitivity over L5.b + L5.c − L5.a
  (the `+I` cancels the `−I = −n^{1−s}/(1−s)` first-order term — the
  §0.5 sign correction, machine-checked).
- **L5.e — `p4_T4_bound` (the P4 statement, s = ½+it):** the Re s > 1
  identity extended to Re s = ½ is **[CITED: DLMF 25.2.8 /
  Apostol Thm 12.21 — the EM tail identity holds by analytic continuation
  on Re s > 0 (ζ−P_n+I meromorphic, RHS entire on {Re s > −1}\{−1,−2};
  agreement on Re s > 1 ⇒ equality on 0 < Re s < 1]; numerically verified
  day-017 at the 1/√M rate]** — stated with the citation in the docstring
  (the B-3 no-ζ-identity convention; the LEAN-proven core is L5.a–d at
  Re s > 1). The bound then follows by triangle inequality:
  `‖(n:ℂ)^{−s}‖ = n^{−1/2}` (`Complex.norm_cpow_eq_rpow_re_of_pos`),
  `‖(n:ℂ)^{−s−1}‖ = n^{−3/2}`, `‖∫ B₂ f″‖ ≤ (√3/270)‖s+2‖ n^{−5/2}`
  (**`p4_f2_tail_bound`, L4.4, GREEN**), `‖s(s+1)‖‖s+2‖ = ‖s(s+1)(s+2)‖`
  (`norm_mul`).
- **L5.f — `p4_T4_ratio` (the T4 corollary):** `|W_n|/|I| ≤ (|s|/2)/n +
  (|s|²)/(12n²) + (√3/540)|s(s+1)(s+2)| n^{−5/2} / (n^{1/2}/|s|)` —
  division algebra (`norm_div`, `abs_re` arithmetic), stated at s = ½+it
  with |I| = n^{1/2}/|s| (`‖(1−s)‖ = |s|` at Re s = ½: 1−s = ½−it).

**Order of attack (owner: one at a time):** L5.a (biggest — the Tendsto
assembly) → L5.b → L5.c → L5.d → L5.e → L5.f; one green commit per atom
(or per two tightly-coupled atoms).

**Honesty file:** the Re s = ½ bridge (L5.e's continuation step) is
CITED, not Lean-proved — the no-ζ-identity convention of P4/spec §0.5.
Everything else is machine-lean: the identity (Re s > 1), every constant,
the bound, the ratio.
