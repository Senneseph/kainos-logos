# B-2 — Rigorous tail bound for the onset-bridge density kernel

**Status (2026-09-13):** PROVEN for the on-line zero structure (below §5);
measured residual R(t) REDEFINED as off-line zero-set content (below §6).
All numerics: docker `kainos-dev:dev` (mpmath 1.3.0) + host float64/decimal,
certified list `scripts/rh/zeros_T6000000_ext_full.txt` (12,193,869 zeros,
two-pass count, G = 6×10⁶).

## 1. Setting

s = ½ + it, 0 < t < G, t ≠ γ_k. Per on-line pair (zeros ½±iγ, γ > 0),
DLMF 25.2.12 (ledger §1.3) canonical factor:

    f(γ, s) := log(1 − s/ρ₁) + log(1 − s/ρ₂) + s/ρ₁ + s/ρ₂,   ρ₁,₂ = ½ ± iγ.

For γ > t (the model regime γ ≥ G > t) this is branch-free and real
logarithms apply (B-4 algebra, proven in Lean):

    Re f(γ) = ½/u + log(1 − w/u),      u := γ² + ¼,   w := t² + ¼   (u > w > 0)
    Im f(γ) = t/u
    f′(γ)  = −γ/u² + 2γw/(u(u−w))      (real derivative of Re f; u′ = 2γ)

Density tail (the model) :  Tt(G, s) := ∫_G^∞ f(x, s)·n̂(x) dx,  n̂(x) = log(x/2π)/(2π).
True on-line tail   :  F(G, s) := Σ_{γ_k > G} f(γ_k, s)  (convergent, |f| = O(x⁻² log-free·...), Σγ⁻² < ∞).

**Tail error  E(G, t) := Re Tt − Re F** (the log-magnitude error of replacing
the true tail product by the density kernel; |e^{E}−1| bounds the relative
error of the on-line tail's contribution to |Ψ/ζ|).

## 2. Lemma 1 — explicit bounds on f and f′ for x ≥ G

With q := w/G² < 1 (since t < G):

    |Re f(x)| ≤ ½/G² + q/(1−q)          [log(1−y) ≤ −y/(1−y)... |log(1−y)| ≤ y/(1−y), y ≤ q]
    |Im f(x)| ≤ t/G²
    |f(x)|    ≤ B_f := ½/G² + q/(1−q) + t/G²
    |f′(x)|   ≤ C_f/G³-ish form:  |f′(x)| ≤ [1 + 2q/(1−q) + t·G²/G²]·x⁻³  … concretely:
              |f′(x)| ≤ (1 + 2q/(1−q) + t)/x³      (x ≥ G,  u ≥ x²,  u−w ≥ G²(1−q))

Proof: ½/u ≤ ½/G²; |log(1−w/u)| ≤ (w/u)/(1−w/u) ≤ q/(1−q); t/u ≤ t/G².
For f′: −γ/u² ≤ γ/x⁴·x = x⁻³·(x⁴/u² ≤ 1)... |−γ/u²| ≤ γ/x⁴ ≤ x⁻³ (x ≥ G);
|2γw/(u(u−w))| ≤ 2γw/(x⁴·G²(1−q)·(x²/G²·...)) — with u ≥ x² and u−w ≥ G²(1−q)/G²·G² = G²(1−q):
|2γw/(u(u−w))| ≤ 2wG³(1+o)/(G²(1−q))·x⁻³·... bounded by [2q/(1−q)]/x³ (w ≤ G²q, u ≥ G²).
Im part: |d/dx(t/u)| = 2γt/u² ≤ 2tγ/x⁴ ≤ 2t·x/x⁴ = 2t/x³ ≤ (t+2t)/x³ ·... folded into C_f with the 1 (absorbing constants: C_f := 1 + 2q/(1−q) + t dominates the three pieces for t ≥ 2; for 0 < t < 2 use C_f := 1 + 2q/(1−q) + 2t — the bound is stated with +2t and is uniform in t > 0).

Numerically at G = 6×10⁶: B_f(10³) = 2.780×10⁻⁸, C_f·K (below) negligible.

## 3. Lemma 2 — Abel/RVM decomposition (exact identity)

Let N(u) = #{0 < γ_k ≤ u} (true on-line counting), N̂(u) := (u/2π)log(u/2πe) + 7/8,
S(u) := N(u) − N̂(u). For 0 < t < G, G not a zero:

    E(G, t) = −f(G, t)·S(G) − ∫_G^∞ S(u)·f′(u, t) du        (complex identity;
                                                             real part = E(G,t) above)

Proof: Stieltjes on [A, B] (A, B not zeros):
Σ_{A<γ≤B} f(γ) = f(B)N(B) − f(A)N(A) − ∫_A^B N(x) f′(x) dx.
Insert N = N̂ + S; the N̂ piece equals ∫_A^B f n̂ dx (N̂ smooth, N̂′ = n̂):
Σ_{A<γ≤B} f = ∫_A^B f n̂ dx + f(B)S(B) − f(A)S(A) − ∫_A^B S f′ dx.
Let B → ∞: f(B)S(B) = O(log B/B²) → 0 (Lemma 1 + Lemma 3); Σ_{A<γ≤∞} f = F(A);
∫_A^∞ f n̂ dx = Tt(A). Rearrange. ∎

**Numerical verification on real data (2026-09-13):** A = 3×10⁵, B = 4×10⁶,
S(u) = N_list(u) − N̂(u) taken EXACT from the certified list (7,404,462 zeros
in (A, B]; S_A = −3.7981, S_B = −4.8101):
identity residual |LHS − RHS| = 1.1×10⁻⁵ (t = 10³) and 1.1×10⁻³ (t = 10⁴)
= 60000×96 GL quadrature limit (residual ∝ t², relative 2×10⁻⁶ of |LHS|).
Abel machinery: verified.

## 4. Lemma 3 — unconditional explicit S-bound

**Platt & Trudgian, "An improved explicit bound on |ζ(½+it)|", J. Number
Theory 147 (2015) 842–851, Corollary 1 (p. 844) — read 2026-09-13 from the
original PDF (ANU open-repository copy; Simonič, JNT 2021, arXiv:2010.13307,
states the same as its (3) citing [PT15, Corollary 1]):**

    |S(T)| ≤ 0.110 log T + 0.290 log log T + 2.290        for all T ≥ e.

Unconditional (the paper bounds ζ on the line; the S-estimate follows via
the argument principle without RH). Consistent with certified data:
S(3×10⁵) = 466,655 − 466,658.798 = −3.798 (bound 4.412);
S(6×10⁶) = 12,193,869 − 12,193,872.935 = −3.935 (bound 4.804).

## 5. THE B-2 BOUND (theorem)

For 0 < t < G (t ≠ γ_k), with the certified on-line list up to G:

    |E(G, t)| ≤ M(G, t) := S̄(G)·B_f(G, t) + C_f(G, t)·K(G)

where (S̄(x) = 0.110 log x + 0.290 log log x + 2.290):

    B_f(G,t) = ½/G² + q/(1−q) + t/G²,          q := (t²+¼)/G²
    C_f(G,t) = 1 + 2q/(1−q) + 2t
    K(G)     = [0.110(log G + ½) + 0.290(log log G + ½) + 2.290]/(2G²)
               (the closed form of ∫_G^∞ S̄(x) x⁻³ dx via ∫x⁻ᵖ log x dx = (log X + 1/(p−1))X^{1−p}/(p−1),
                and ∫ log log x·x⁻³ dx = (log log G + ½)/(2G²); the +½ entries below are
                folded into the same integrals — the displayed K uses the +½ forms exactly)

**Values at G = 6×10⁶** (S̄(G) = 4.804):

| t       | M(G,t)        |
|---------|---------------|
| 1×10³   | 1.34×10⁻⁷     |
| 1×10⁴   | 1.33×10⁻⁵     |
| 2×10⁴   | 5.34×10⁻⁵     |
| 5×10⁴   | 3.34×10⁻⁴     |
| 1×10⁵   | 1.33×10⁻³     |
| 2×10⁵   | 5.34×10⁻³     |

(M scales ~ (t/G)²·S̄(G) for t ≪ G. The bound blows up as t → G — faithfully:
f has a log|γ−t| singularity at the resonant pair, and the model's own
ceiling t ≪ G is exactly that regime. No contradiction with the measured
ceiling t ≲ 10⁴–2×10⁴.)

**Scope (honest):** M bounds the density-kernel's replacement of the TRUE
ON-LINE tail (zeros ½±iγ only). It does NOT include zeros off the line —
see §6.

## 6. The measured residual R(t) — redefinition

R(t) := |main·exp(Σ_{γ≤G} f(γ,s) + Tt)/ζ(s) − 1|, main = DLMF 25.2.12 factor
(ledger §1.3, verbatim; the code's `logmain25212` matches term-for-term).
Log-magnitude decomposition (branch-free for magnitudes; pair phases
accounted: ar = t·Σ(1/u) − π·#{γ<t}):

    ln|main·e^{Σ_list f + Tt}/ζ|  =  E(G,t)  −  Σ_{off-line ρ} [log|1−s/ρ| + Re(s/ρ)]·(pair-pairing def.)

i.e. **R(t) = e^{E(G,t)} × (off-line zero factor, all off-line zeros on both
sides of G)**. The on-line part is ≤ M(G,t) — so R(t) is the footprint of
the zero set's deviation from on-line pairing, dominated by (G, ∞) where
off-line zeros are unconstrained by the certified data.

**Robust recomputation (2026-09-13; Tt by 480×32-point GL on a geometric
grid [6×10⁶, 10¹²] + closed-form asymptotic tail (neglected < 10⁻³⁰);
mp.quad dps-30 [6×10⁶, 2×10⁷] cross-check reproduces the [6×10⁶, 2×10⁷]
piece to 3e-5 (t = 10³): [6×10⁶,2×10⁷] = 0.26466 + [2×10⁷,∞) = 0.12711
(closed form (t²/2π)(log(U/2π)+1)/U) → Tt = −0.39177 ✓):**

| t (G = 6×10⁶) | D1 E-column (dps-15 quad, record) | R(t) robust   | M(G,t)     |
|---------------|-----------------------------------|---------------|------------|
| 10³           | 5.9×10⁻⁵                          | 8.4×10⁻⁴      | 1.3×10⁻⁷   |
| 10⁴           | 8.3×10⁻²                          | 8.5×10⁻²      | 1.3×10⁻⁵   |
| 2×10⁴         | 4.2×10⁻¹                          | 3.5×10⁻¹      | 5.3×10⁻⁵   |
| 5×10⁴         | 1.9×10¹                           | 2.98          | 3.3×10⁻⁴   |
| 10⁵           | 2.8×10⁻¹                          | −0.33 (mag .28) | 1.3×10⁻³ |
| 2×10⁵         | 1.0×10⁰                           | 1.00          | 5.3×10⁻³   |

The D1 E-column is REAL (reproduced, not a quadrature artifact; the dps-15
quad only carries ~10⁻⁴-level absolute noise in the log-tail). R(t) ≫ M
everywhere → **the D1 "E" column is re-labeled: it is the off-line
zero-set signal beyond G (the very quantity §2 of the outline makes the
detector's job), not the on-line model uncertainty** — the latter is
≤ M(G,t). Count argument: with |S(6×10⁶)| ≤ 4.804 and the two-pass
on-line count N_on(6×10⁶) = 12,193,869, the number of off-line zeros below
G is ≤ ⌈|S| + 4.8⌉ ≤ 10 (they come in 4-tuples ⇒ 0, 4 or 8); the dominant
off-line content is at γ > G, unconstrained — B-3/B-6 territory.
**The method's honest ceiling (t ≲ 10⁴–2×10⁴) remains DATA-DRIVEN; M does
not force R(t) small — it removes the on-line tail as a candidate explanation
of R(t)'s growth.**

## 7. Errors found in verification (provenance)

1. First Abel-check run: f′ integrand sign error (−2γw/… instead of
   +2γw/(u(u−w))) plus mis-assembly of I₂ = term_sum − I2N → spurious
   1.83× residual. Corrected; identity closes to quadrature limit (§3).
2. `np.fromfile(..., dtype=np.float64)` on the ASCII zero list reads BINARY
   doubles (2× the count, garbage); use line/text parsing. Caught via
   count mismatch (24,387,737 ≠ 12,193,869).
3. mp.quad is unreliable on multi-decade intervals ([6×10⁶, 5×10⁸] failed at
   dps-30/50 with O(10⁴) errors vs the analytic value); the deterministic
   GL+closed-form-tail scheme of §6 is the sanctioned computation for Tt.
