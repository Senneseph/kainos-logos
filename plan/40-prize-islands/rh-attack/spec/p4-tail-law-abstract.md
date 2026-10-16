# P4 — ABSTRACT SPECIFICATION (what it is supposed to do, from RH-PROOF-OUTLINE.md)

*Not a status report. Not an error map. The target state, written as a
mathematical specification with a Lean 4.33.1 type-compatibility ledger.
Source: outline §4 + §9 row P4, cross-checked against §3, §8, §10 and the
measured record (`spec/onset-bridge-e7b1.md`, `scripts/rh/day004b_onset.py`).
Lean facts pinned against the official 4.33.1 docs
(`kainos-logos/references/official-lean4-docs/`, `LEAN4-4331-QUICKREF.md`)
and the pinned mathlib source (`.lake/packages/mathlib`).*

---

## 0. What P4 is FOR in the argument (outline §3, §4, §10)

The floor (§10, P8, the open wall) must say: **from the definition side
alone, the quantity W_n(t) is smaller than the detector scale
f(δ,t)·|K|, uniformly in t, with no zero-count input.** The definition
side must therefore be equipped with a zero-free quantity whose *size* is
rigorously bounded. P4 is that equipment:

- §4 defines the definition side: `P_n(s) = Σ_{k≤n} k^{−s}` (Euler sum),
  `I(n,s) = n^{1−s}/(1−s)` (first-term integral), and the missing tail
  `W_n(t)` = what remains of the Euler sum after stripping the first n
  terms *and* the first-term integral approximation.
- The measured law (15 points, N-independent, `spec/onset-bridge-e7b1.md`):
  `|W_n(t)|/|I(n,s)| ≈ ½·(t/n)`, four digits, onset window `t/n ≈ 1–2`.
- **P4 = that law as a theorem**: an explicit Euler–Maclaurin expansion
  of the tail of `Σ k^{−s}` with an *explicit computable remainder bound*,
  from which the ½·(t/n)-law follows as a corollary — no fit, no O-term
  left implicit.

P4 is the definition-side engine of the floor. Its output is a
**zero-free upper bound B_n(t) on |W_n(t)|** with every constant explicit.

## 0.5 SIGN CORRECTION (recorded before any port — P-0.9 class)

The outline's displayed definition line reads
`W_n(t) = ζ(½+it) − P_n(½+it) − I(n,½+it)`. The outline's *own* next
line (and the measured data) fix the sign: **the first-order term of the
tail `ζ − P_n` is `−I(n,s)`** (it is `∫_n^∞ x^{−s} dx = −n^{1−s}/(1−s)`
for Re(s) ∈ (0,1]·), since the tail must be stripped of `−I`, not `+I`).
The measurement confirms: `day004b_onset.py` computes
`C = |tail + I|` with `I = N^{1−s}/(1−s)` and labels it "second order
(after removing −I)". Therefore the strictified definition used below is

    W_n(t) := T_n(s) + I(n,s),   T_n(s) := Σ_{k>n} k^{−s}  (Re(s) > 0),

and `|W_n|/|I|` is the measured quantity (0.0500/0.1000/0.2509/0.5071/
1.0620 at t/n = 0.1/0.2/0.5/1/2). The outline's `− I` line is a
sign-typo against its own "first-order term is −I" sentence and against
all 15 data points; it is flagged for a doc pass (no behavior
consequence: the ratio |W_n|/|I| is stated for the data-consistent
quantity).

**Scoping decision (same no-ζ-in-the-core convention as B-3):** the Lean
core works with the tail *series* `T_n` — which converges for Re(s) > 0
(Dirichlet) and is the definition-side instrument itself. The
identification `T_n(s) = ζ(s) − P_n(s)` on the line is the **Riemann
1859 continuation identity** (the Dirichlet series sums to the
analytic continuation for Re(s) > 0) — a classical citation of the
definition side, exactly the role DLMF 25.2.12 plays in B-3. Mathlib's
`riemannZeta` (complex-differentiable, `zeta_eq_tsum_one_div_nat_cpow`
for `1 < re s`) is available for the `re > 1` anchor, but the
continuation-identity itself is *not in mathlib* and is NOT ported.

## 0.6 PUBLISHED SOLUTIONS (found online, day-017 — the owner's hunch was right)

Two prior formalizations exist; both are used rather than re-invented:

1. **Lean, first-order EM (PORT).** Alex Kontorovich's
   `PrimeNumberTheoremAnd/EulerMaclaurin.lean` (a PNT proof in Lean;
   v4.32.2 — one release before our 4.33.1 pin; the zeta-23-lean fork
   carries it verbatim). It proves, for `𝕜 : RCLike` (ℝ **or ℂ** ✓):

       ∑ k ∈ Ioc ⌊a⌋ ⌊b⌋, f k = f a·B̂₁(a) − f b·B̂₁(b) + ∫_a^b f
                              + ∫_a^b f′(t)·B̂₁(t) dt

   (exact `B1 x := x − ⌊x⌋₊ − ½`, `|B1| ≤ ½`), derived from
   `Mathlib.NumberTheory.AbelSummation.sum_mul_eq_sub_sub_integral_mul`
   — **verified present in the pinned 4.33.1 mathlib**
   (`AbelSummation.lean:129`); `module`/`grind`/`fun_prop` all exist at
   4.33.1. Ported verbatim as `RhAttack/P4Em.lean` (Atom-1), with the
   provenance header (their own convention) and minimal changes only if
   4.33.1 requires them.

2. **Isabelle/HOL, full even-Bernoulli form (CROSS-CHECK).** AFP entry
   `Euler_MacLaurin`: `euler_maclaurin_strong_int'` (open half-line,
   even-Bernoulli form, remainder
   `EM_remainder n = (−1)^{n+1}/n! ∫ pbernpoly(n,·)·f^{(n)}`) with the
   bound `‖EM_remainder‖ ≤ (sup ‖pbernpoly n‖ / n!) · g(x)` for a
   dominating `g → 0`. This is exactly the OP1 shape of §T3 — the
   published cross-check for the remainder bound. (Not ported: different
   proof assistant; used to verify constants, per the no-guess rule.)

**What no published source provides (the local derivation):** the
**second-order form** (the `−(s/12)·n^{−s−1}` term + `B̂₂-f″` remainder)
at `Re s = ½`. Upstream has only first order; AFP states it generically
but is not Lean. Atom-2 derives it locally from the pinned Abel
machinery + the ported first-order lemma (finite `N` first, exact;
`N → ∞` after, using `f, f′, f″ → 0`). The kernel-construction detail
is settled IN the atom (one edit → re-run → observe); the target
identity below is what the atom must produce.

## 1. The mathematical content, theorem by theorem

Throughout: `s = (1/2 : ℂ) + it` with `t : ℝ` (so Re(s) = ½ > 0, s ≠ 1),
`n : ℕ`, `n ≥ 1`. All constants explicit.

### T1 — definitions and the domain of convergence

- `P_n(s) := (∑ k in Finset.Icc 1 n, (1 : ℂ) / (k : ℂ) ^ s)` (finite;
  `(k : ℂ) ≠ 0` on the support).
- `I(n,s) := (n : ℂ) ^ (1 - s) / (1 - s)` — well-defined: `1 - s = 1/2 - it`
  has modulus `√(t² + ¼) > 0`, never zero.
- `T_n(s) := ∑' (k : ℕ), (if k ≤ n then 0 else (1 : ℂ)/(k : ℂ)^s)` —
  the tail as a tsum. **Domain claim (corrected, day-017, computed):**
  the Dirichlet series for ζ has abscissa of convergence exactly 1 —
  `T_n` is summable for **Re(s) > 1 only**; for Re(s) ≤ 1 it DIVENGES
  (at σ = ½ the terms are k^{−1/2}·k^{−it}, magnitude not summable;
  the slow chirp k^{−it} gives only logarithmic/sublinear cancellation —
  verified: `Σ_{k≤2e5} k^{−1/2−1000i}` partial sums stay O(1) at 2e5
  by sublinear growth, no convergence). Therefore, at the line
  (σ = ½) the missing tail is defined **through the analytically
  continued ζ** (mathlib `riemannZeta` — a zero-free object: no zero
  list, no Riemann–Siegel in the statement):

      W_n(s) := (riemannZeta s − P_n(s)) + I(n,s),   s = ½ + it.

  The EM identity for W_n at σ = ½ is then the **Riemann 1859 formula**:
  the finite exact EM (Atom-2, valid for all s) + `M → ∞`, whose limit
  defines the continuation — cited, per the B-3 no-ζ-identity-convention
  (DLMF 25.2.12's role). **Verified numerically (computed, not
  recalled):** at s = ½+1000i, N = 1000 the 2-subtracted partial sums
  `A(M) := Σ_{k≤M}k^{−s} − M^{1−s}/(1−s) + ½M^{−s} + (s/12)M^{−s−1}`
  converge to mpmath-`zeta(s)` with `|A(M)−ζ|` ≈ 0.0316/0.0100/0.00316
  at M = 10³/10⁴/10⁵ (exactly 1/√M rate — the M^{−1/2} tail of the
  chirp), and the full identity `W_n = −½n^{−s} + (s/12)n^{−s−1} −
  ½∫_n^∞ B̂₂f″` holds to 3.7e-5 (float64 per-period quadrature).
- The **ζ-anchor lemma** (the only statement touching `riemannZeta`):
  for `1 < re s`, `riemannZeta s = (∑' k, (1:ℂ)/(k:ℂ)^s)` (mathlib,
  `zeta_eq_tsum_one_div_nat_cpow`), hence for such s, `T_n s =
  riemannZeta s − P_n s`. For `re s = ½` the identification is the cited
  1859 identity (header + outline, not a Lean claim).

### T2 — the first-order identity (the measured "first-order owns the tail")

For Re(s) > 0, s ≠ 1, n ≥ 1 — **verified at σ = 1.5 (convergent series,
3.2e-7) AND at σ = ½ (continuation, 3.7e-5), computed day-017**:

    T_n(s) + I(n,s) = −(1/2)·n^{−s} + (s/12)·n^{−s−1} + R_{n,1}(s)

with the **PLUS** sign on the `(s/12)` term (corrected day-017 from the
draft's `−(s/12)` — pinned by the s = 1.5 numerical check: the minus
form misses by 7.3e-4 ≫ the 7.9e-5 bound; the plus form hits to 3.2e-7
inside the 7.9e-5 bound) and `R_{n,1}(s) = −½∫_n^∞ B̂₂({x})·f″(x) dx`
(the m=1 remainder; the sign of `R` is pinned in Atom-2 by the same
route). At σ > 1 `T_n` is the convergent tail; at σ = ½ the identity
IS the 1859 formula in W-form (T1). The first-order term of the raw
tail `ζ − P_n` is `−I` — after stripping it, `−½ n^{−s}` is what the
floor must see. This is the exact content of the measured
"r = 2.000 means tail = −I exactly" fingerprint.

### T3 — the explicit Euler–Maclaurin remainder (the P4 crown)

For `f(x) = (x:ℂ)^{−s}` (Re s = ½ > 0), the **second-order EM identity**
(Atom-2, derived in Lean from the pinned Abel machinery, finite exact
`N`-form first, then `N → ∞`):

    T_n(s) = n^{1−s}/(s−1) − ½·n^{−s} + (s/12)·n^{−s−1} + R_{n,1}(s),
    R_{n,1}(s) = −(1/2)·∫_n^∞ B̂₂({x})·f″(x) dx,

(`n^{1−s}/(s−1) = −I`; the `−(1/2)` is pinned by the day-017 numerics,
±checked by Atom-2's IBP sign convention).

so that, after stripping `−I` (the first-order term, T2) — **signs
verified numerically day-017 at σ = 1.5 (3.2e-7) and σ = ½ (3.7e-5)**:

    W_n(s) = −½·n^{−s} + (s/12)·n^{−s−1} + R_{n,1}(s),
    R_{n,1}(s) = −(1/2)·∫_n^∞ B̂₂({x})·f″(x) dx,

(The first-order identity — `T_n = −I − ½n^{−s} + ∫ B̂₁·f′` — is a
direct corollary of the PORTED Atom-1 lemma; the second order adds the
`B̂₂` kernel.)

**The remainder route (OP lemmas): proven in Lean atoms BEFORE use
(P-0.9 class — constants derived, not cited), cross-checked against the
AFP published bound form of §0.6:**

    Lemma OP1 (one-period, crude).  h : ℝ → ℝ decreasing, h → 0:
    |∫_n^∞ B̂₂({x}) h(x) dx| ≤ (2·sup|B̂₂|)·h(n) = h(n)/3.
      [integer-period split; ∫₀¹ B̂₂ = 0 ⟹ each period rewrites against
       the constant h(n+j); |Δ_j| ≤ h(n+j)−h(n+j+1); telescope. ~12
       lines.]  (AFP analogue: sup-pbernpoly bound, D = 2·sup|B̂₂|.)

    Lemma OP2 (second moment, refined).  Same hypotheses:
    |∫_n^∞ B̂₂({x}) h(x) dx| ≤ (max_{[0,1]}|B₃| / 3)·h(n) = (√3/108)·h(n).
      [Δ_j(u) = h(n+j)−h(n+j+u) = ∫₀ᵘ (−h′)(n+j+v) dv; swap order:
       ∫₀¹ B̂₂(u)Δ_j(u) du = ∫₀¹ (−h′)(n+j+v)·(∫ᵤ¹ B̂₂ du) dv, and
       ∫ᵤ¹ B̂₂ du = −B₃(u)/3 (B₃(1) = 0); |B₃(u)| ≤ max|B₃| = √3/36, a
       closed form — at the critical point v₀ = (3−√3)/6, v₀(1−v₀) = 1/6
       exactly and B₃(v₀) = (1/6)·(−√3/6); √3/36 < 1/20 via norm_num;
       telescopes as in OP1.] (Beyond the AFP bound — sharpens it.)

Apply to Re/Im of `f″` with `h = |f″| = ‖s‖(‖s‖+1)·x^{−5/2}`
(decreasing ✓, `‖s‖ = √(t²+¼)`):

    |R_{n,1}(s)| ≤ (1/2)·(√3/108)·‖s‖·(‖s‖+1)·n^{−5/2}
                 = (√3/216)·‖s‖·(‖s‖+1)·n^{−5/2}.            (OP2-bound)

Stability-first: **OP1 is the first atom proven and the fallback**
(constant `1/6` on `‖s‖(‖s‖+1)n^{−5/2}`); the shipped theorem uses
OP2 once it is green, since at the onset window `t/n = 2` the OP1 width
is ~5× the measured deviation while OP2 is ~4×.

**The stated P4 output** — zero-free explicit upper bound for the floor
(P8), `s = ½+it`, `n ≥ 1`, `‖s‖ = √(t²+¼)`:

    |W_n(t)| ≤ B_n(t) := ½·n^{−1/2} + (‖s‖/12)·n^{−3/2}
                   + (√3/216)·‖s‖·(‖s‖+1)·n^{−5/2},

triangle inequality on the three-term EM form, every factor explicit,
zero-free, computable. Asymptotically `B_n(t) = ½n^{−1/2}(1 + O(t²/n²))`
where the `O`-factor IS the explicit second/third term; nothing implicit.

### T4 — the ½·(t/n) law as a corollary (the strictified measured law)

From T2+T3, `|I(n,s)| = n^{1/2}/‖s‖`, `|n^{−s}| = n^{−1/2}`, `‖s‖ =
√(t²+¼)`; the ratio is trapped (triangle inequality, no phase
assumption) in

    ½·‖s‖/n  ±  err(t,n),

    err(t,n) = (t²+¼)/(12·n²) + (√3/216)·(t²+¼)·(‖s‖+1)/n³,

(the OP2-bound `‖s‖`-magnitudes divided by `|I| = n^{1/2}/‖s‖`, fully
explicit). The corollary — **checked numerically in the gate (T5), not
assumed** — is the interval containment of the five measured ratios at
all three N:

    0.0500, 0.1000, 0.2509, 0.5071, 1.0620
        ∈ [½‖s‖/n − err, ½‖s‖/n + err]

at `n ∈ {10³, 10⁴, 10⁵}` × `t/n ∈ {0.1, 0.2, 0.5, 1, 2}`. Hand-verified widths (to be machine-checked in the gate): t/n = 0.1 →
±0.09%; 0.2 → ±0.34%; 0.5 → ±2.2%; 1 → ±9.1%; 2 → ±40% — containing the
measured deviations (≤ 0.4%, 0.4%, 0.7%, 1.4%, 6.2%). N-independence: the
residual n-dependence of the interval beyond `t/n` is the explicit
`1/n`-terms (≤ 0.9% at the onset window), below the ≤ 6% measured
spread. The phase of the `(s/12)`-term is NOT assumed — the theorem
states the disk the data sit inside; phase tracking is a post-green
sharpening. The 15-point gate (T5) is the numeric witness.

### T5 — the A/B float layer (cross-check gate, not part of the claim)

A `P4Float` mirror (float64, no Float↔ℝ coercion) reproduces:
(i) the EM ratio `|W_n|/|I|` at the 15 measured points within the
measured spread; (ii) the n-independence (the three N-rows agree to
≤ 6% as measured); (iii) the explicit bound `B_n(t)` is *above* the
numerically computed `|W_n|` at those points (the theorem is
self-satisfying: the bound beats the value, exactly the B-5 pattern).
Prints PASS/FAIL, wired into `Main.main` after a green full build.

**Numerical hazard (P-0.9, recorded day-017):** the `B̂₂·f″` integral
has a kink at EVERY integer — mpmath `quad` on `[N, ∞)` (or even a
finite `[N, M]`) misintegrates it (observed: a 0.0135 error at
(σ=½, t=1000, N=1000) and an outright 1e63 explosion on per-period
`[0,1]` sub-intervals). The gate must integrate **per unit interval**
(Gauss–Legendre on each `[j, j+1)`, where `B̂₂` is a polynomial — smooth,
no kink inside): verified this way to 3.7e-5 against mpmath-`zeta`.
The Lean side has no such hazard (the integrals are theorem-level;
the float mirror is the only numeric consumer).

## 2. The type system of P4, and why each type is 4.33.1-compatible

- **s, P_n, I, T_n, W_n : ℂ.** mathlib `Complex` throughout. `riemannZeta : ℂ → ℂ` exists (pinned: `Mathlib/NumberTheory/LSeries/RiemannZeta.lean`, `def riemannZeta := hurwitzZetaEven 0`, `zeta_eq_tsum_one_div_nat_cpow` for `1 < re s`). The core (T2–T4) is **ζ-free by design** (series-based, re s = ½).
- **The tail tsum** is over ℕ with an `if k ≤ n` cutoff (zero on the
  finite head) — so `T_n` is a single tsum, and
  `T_n = (∑' k, (1:ℂ)/(k:ℂ)^s) − P_n` is available by tsum linearity
  once summability of the full series is established (which requires
  re s > 1; for re s = ½ the tsum `∑' (if k≤n then 0 else ...)` is
  *itself* summable by Dirichlet, and this is the actual object).
- **The Abel machinery (Atom-1/Atom-2 dependency):**
  `Mathlib.NumberTheory.AbelSummation.sum_mul_eq_sub_sub_integral_mul`
  — **verified present in the pinned 4.33.1 mathlib** (`AbelSummation.lean
  :129`), the exact theorem the upstream Kontorovich first-order EM file
  is built on (§0.6). The port compiles against it unmodified (Atom-1
  will confirm; syntax elements used — `module`, `@[expose]`, `grind`,
  `fun_prop` — all exist at 4.33.1).
- **Derivatives of `x ↦ (x:ℂ)^(−s)` on ℝ\{0}:** pinned at
  `Mathlib/Analysis/SpecialFunctions/Pow/Deriv.lean:306` —
  `Complex.deriv_ofReal_cpow_const {x : ℝ} (hx : x ≠ 0) (hc : c ≠ 0) :
  deriv (fun x : ℝ => (x : ℂ) ^ c) x = c * x ^ (c - 1)`. The iterates
  `f^{(2m)}` follow by repeated `deriv` (each is a scalar multiple of
  `(x:ℂ)^(−s−2m)`).
- **The remainder integral** is over `[n, ∞)` of a complex-valued
  function on ℝ: `intervalIntegral` (ℝ → ℂ, a normed ℝ-vector space) —
  same API B-3 used (ℝ-valued); the ℂ-valued variant is available
  (PROBE-1: confirm `.intervalIntegral` for ℝ→ℂ at 4.33.1).
- **Bernoulli:** `bernoulli (n : ℕ) : ℚ` and the polynomials
  `bernoulli (n : ℕ) : ℚ[X]` (pinned: `Mathlib/NumberTheory/Bernoulli.lean`,
  `Mathlib/NumberTheory/BernoulliPolynomials.lean`). `B̂_{2m}` = the
  periodic Bernoulli function (private def: `x ↦ bernoulli (2*m) |>.eval (x - ⌊x⌋)` in ℚ/ℝ).
- **The bound `E_m(s)·n^{...}`** reuses B-3's atoms (positivity,
  `norm_num`, `field_simp`, the `div_le_iff₀`/`monotone_div` pins).
- **No Float↔ℝ coercion** in the float layer (T5), per the B-3/B-5
  established rule: the float mirror is a *separate* object with its own
  `ℝ → Float` (or `Float`) implementation, not a coercion of the core.

## 3. What counts as P4 COMPLETE

1. `RhAttack.P4` (or the named piece) is green: T1–T4 proven, all
   constants explicit, no implicit O-terms, no `sorry`.
2. The ζ-anchor lemma (T1) is proven for re s > 1; the re s = ½ identity
   is cited (header + outline) as the 1859 continuation identity.
3. The A/B gate (T5) runs and prints PASS/FAIL in `lake exe rhattack`,
   wired after a green full build.
4. The sign correction (§0.5) is recorded in the file header and flagged
   in the outline for a doc pass.
5. Probes (N9+) keep compiling (2-line headers; failures in comments).
6. The explicit bound `B_n(t)` is the *stated output* of the file, named
   and documented as the input to the floor (P8).
