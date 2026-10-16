# READS (verbatim, no recall): Riemann 1859 explicit formula + GS25 zero-sum machinery

Captured 2026-09-09 for E7b (P-E.3). These are the two verbatim anchors for
the zero side of the recognition map.

## 1. Riemann 1859 — the explicit formula, VERBATIM (Wilkins translation)

Source: https://www.maths.tcd.ie/pub/HistMath/People/Riemann/Zeta/EZeta.pdf
(D. R. Wilkins, "On the Number of Prime Numbers less than a Given Quantity",
preliminary version December 1998; PDF also at claymath.org, local copy
/tmp/pi-web-pdf/ezeta.md).

Setup (p. 5): Riemann defines the counting function with the half-jump
convention:

> "Let F(x) be equal to this number when x is not exactly equal to a prime
> number; but let it be greater by 1/2 when x is a prime number, so that,
> for any x at which there is a jump in the value in F(x),
> F(x) = (F(x+0) + F(x−0))/2."

> "If in the identity log ζ(s) = −Σ log(1 − p^{−s}) = Σ p^{−s} + 1/2 Σ p^{−2s}
> + 1/3 Σ p^{−3s} + ... one now replaces p^{−s} by s∫_p^∞ x^{−s−1} dx,
> p^{−2s} by s∫_{p^2}^∞ x^{−s−1} dx, ... one obtains
> **log ζ(s)/s = ∫_1^∞ f(x) x^{−s−1} dx**,
> if one denotes F(x) + 1/2 F(x^{1/2}) + 1/3 F(x^{1/3}) + ... by f(x)."

**THE EXPLICIT FORMULA (p. 9, verbatim):**

> "Through the insertion of these values in the expression for f(x) one
> obtains
> **f(x) = Li(x) − Σ_α ( Li(x^{1/2+αi}) + Li(x^{1/2−αi}) )
>           + ∫_x^∞ dx / ((x²−1) ln x) + log ξ(0)**,
> if in Σ_α one substitutes for α all positive roots (or roots having a
> positive real part) of the equation ξ(α) = 0, ordered by their
> magnitude."

Recovery of F (p. 9, verbatim): "From f(x) one obtains F(x) by inversion of
the relation f(x) = Σ (1/n) F(x^{1/n}), to obtain the equation
**F(x) = Σ_m (−1)^{μ_m} f(x^{1/m})**, in which one substitutes for m the
series consisting of those natural numbers that are not divisible by any
square other than 1, and in which μ denotes the number of prime factors of m."

**THE PRIME-DENSITY zero kernel (p. 9, verbatim) — the E7b anchor:**

> "If one restricts Σ_α to a finite number of terms, then the derivative of
> the expression for f(x) or, up to a part diminishing very rapidly with
> growing x,
> **1/ln x − 2 Σ_α x^{−1/2} cos(α ln x) / ln x**
> gives an approximating expression for the density of the prime number +
> half the density of the squares of the prime numbers + a third of the
> density of the cubes of the prime numbers etc. at the magnitude x."

Reading notes (labels: interpretation):
- Modern form of the same formula: F-type counting
  `x − Σ_ρ Li(x^ρ) − ln(2π) − ½ ln(1 − x^{−2})` (the ∫_x^∞ dx/((x²−1)ln x)
  term and log ξ(0) = ½ln(2π) repackage into ln(2π) + ½ln(1−x^{−2}));
  verify the constant identity dps-40 before using (do not assume).
- The zero kernel per conjugate pair: **amplitude x^{−1/2}/ln x,
  oscillation cos(γ ln x), coefficient 2** — the x^{−1/2} is exactly the
  unit-amplitude σ = ½ signature that our onset measurement
  (|N^{ρ−s}| = 1 at σ = ½) reads. Riemann 1859 wrote the zero side of the
  action in 1859; our onset C/|I| = ½·(t/N) is the moment that kernel
  becomes visible in the tail budget.
- Riemann's α = our γ (roots of ξ(α)=0, α real = RH claim "all roots real").

## 2. GS25 — Goldston–Suriajaya, arXiv:2603.28104 (30 Mar 2026)

"Zeta Zeros in a Narrow Vertical Box". Full text saved locally:
/tmp/pi-web-pdf/zeta-zeros-in-a-narrow-vertical-box.md (copy to repo? no —
cite arXiv; the note is 7 pp public).

Machinery (verbatim core, §6–§7):
- Pair-correlation object:
  **F(α,T) := Σ_{ρ,ρ'} T^{α(ρ−ρ')} W(ρ−ρ')**,
  **W(u) := 4/(4 − u²)** (Montgomery's kernel, now over pairs of full
  zeros, no RH).
- **Unconditional Montgomery theorem (BGSTB24, cited as (6.3)):**
  F(α,T) = ((1+o(1)) T^{−2α} log T + α + o(1)) · T/(2π) · log T,
  uniformly 0 ≤ α ≤ 1 — WITHOUT RH (the RH version (6.4) is a special case).
- Unconditional close-pair bound (GM87 Lemma 9, (5.1)):
  Σ_{|γ'−γ| ≤ h} 1 ≪ (1 + h log T)·T log T / T...
  (in particular the diagonal (γ=γ') term ≤ (C+o(1)) T/(2π log T) for some
  absolute C, much larger than 2 unconditionally).
- **Theorem 2 (reduction):** if the diagonal two-zero sum satisfies
  Σ_{ρ,ρ': γ=γ'} 1 ≤ (C+o(1)) T/(2π log T), then the proportion of zeros
  which are simple AND on the line is **≥ 2 − C** (plus companion bounds
  (3−C)/2 and (4−C)/3).
- **Theorem 1 (this note):** assuming all zeros with T < γ ≤ 2T lie in the
  narrow box |σ − ½| < b(T)/log T, b(T) → 0, then C = 4/3 ⇒ **≥ 2/3
  simple and on the line** — proved by Fejér-kernel alone (no Tsang
  kernel, following Montgomery closely; the proof closes at the
  sin(½(γ−γ')logT)/(½(γ−γ')logT)² sum = (4/3+o(1))T log T / (2π)·(T log T)
  normalization, (7.1)–(8.2)).
- Context from the note: previous unconditional records: Levinson 1974
  34.74% simple+on-line; **PRZZ20 41.7% on-line / 40.7% simple+on-line
  (= the 5/12 ≈ 41.67% "41%" the owner remembered, in its 2020 form)**;
  the Claude/2026 result (67.25% / 83.625%) uses b = 0.001 with the
  optimized (Tsang-family) kernel per BGSTB25 Theorem 2.

Reading note (label: interpretation): the GS school's zero-side object is a
**PAIR-correlation sum with kernel W(ρ−ρ') = 4/(4−(ρ−ρ')²)**; our measured
onset C is a **SINGLE-zero** object (the explicit formula above). The
recognition map must not conflate them: E7b uses the Riemann-1859 kernels;
GS25 is the proportion school (complementary, EXTERNAL-2026-claude-rh.md).
One structural remark worth testing later: W(u) = 4/(4−u²) is a
Meromorphic-inversion kernel (poles at u = ±2) — the same
"inversion = mirror" shape as our action's weight field; whether the pair
kernel is the two-zero shadow of the single-zero action kernel is a
question for after E7b (do not conflate before then).

## 3. E7b design (from these reads, labels: plan)

Observed (measured): C(t, N) = zero-oscillation in the ζ-tail at s = ½+it,
onset scale N ≈ t/2 (C/|I| = ½ t/N to 4 digits, Day-04b).
Predictor (from 1859, regularized Abel from the density kernel):
C_pred(t, N) = Σ_{ρ: γ near t} [single-zero kernel(K=N, s=½+it, ρ)] + smooth.
Single-zero kernel: derived (not recalled) by Abel-transforming Riemann's
density kernel x^{−1/2}cos(γ ln x)/ln x against the weight (x−N)_+ x^{−s}
— the derivation goes in THE-EULER-ACTION.md §E7b when executed.
Data: our zero list (138,065 zeros ≤ 1e5) + the measured C from the
Day-04b onset columns (N = 1e4..1e5, t/N = 2).
PASS = nearest zero dominates with the derived coefficient (agreement to
the measured 4-digit level); FAIL = non-explicit-formula content (new for
us). Cost: O(number of t-points × zeros within O(1) of t) — minutes.

---

## 3. DLMF ch. 25 READ (2026-09-09, dlmf.nist.gov — full sections fetched)

**§25.10 Zeros — read (full section).**

- §25.10(i) Distribution — RH, VERBATIM (paraphrase-marked only where the
  page text is quoted in full): "The _Riemann hypothesis_ states that all
  nontrivial zeros lie on [the critical] line [ℜs = ½]." Zero-free:
  ℜs > 1 (product representation (25.2.11)); ℜs = 1 (Hadamard 1896;
  de la Vallée Poussin 1896a,b — the PNT proofs); functional equation
  ⇒ trivial zeros ζ(−2n); ζ(s) ≠ 0 for ℜs ≤ 0 except trivial; in the
  critical strip 0 < ℜs < 1: infinitely many zeros, "distributed
  symmetrically about the real axis and about the critical line".
- 25.10.1: `Z(t) ≡ exp(iϑ(t))·ζ(½+it)` — the real-valued function used
  for counts on the line; |Z| = |ζ(½+it)|; "Z(t) vanishes at the zeros
  of ζ(½+it), which can be separated by observing sign changes of Z(t).
  Because Z(t) changes sign infinitely often, ζ(½+it) has infinitely
  many zeros with t real."
- 25.10.2: `ϑ(t) ≡ ph Γ(¼ + ½it) − ½ t ln π`, "is chosen to make Z(t)
  real, and ph Γ(¼ + ½it) assumes its principal value." (This is the
  ϑ — do not conflate with the RVM main constant; see FORMULAS.md §2.3,
  where the walk identity θ_walk/π = main − 1 is the measured
  certificate.)
- §25.10(ii) Riemann–Siegel Formula — VERBATIM framing: "Riemann
  developed a method for counting the total number N(T) of zeros of
  ζ(s) in that portion of the critical strip with 0 < t < T. By
  comparing N(T) with the number of sign changes of Z(t) we can decide
  whether ζ(s) has any zeros off the line in this region. Sign changes
  of Z(t) are determined by multiplying (25.9.3) by exp(iϑ(t)) to
  obtain the _Riemann–Siegel formula_:"
  - **25.10.3:** `Z(t) = 2 Σ_{n=1}^{m} cos(ϑ(t) − t ln n) / n^{1/2}
    + R(t)`, `m = ⌊(t/2π)^{1/2}⌋` (source: Titchmarsh (1986b),
    (4.17.4), p. 89; erratum v1.1.4 added the m constraint; the radical
    is dropped by the page's text extraction — engine + validation
    confirm the square-root form).
  - "where R(t) = O(t^{−1/4}) as t → ∞. The error term R(t) can be
    expressed as an asymptotic series that begins [image] Riemann also
    developed a technique for determining further terms."
  - Prior art on the page: "the first ten billion zeros … are on the
    critical line (van de Lune et al. 1986)"; "More than 41% of all the
    zeros in the critical strip lie on the critical line (Bui et al.
    2011)" [Bui et al. 2011 = PRZZ20 in our files].
  - **DLMF 25.10 prints no N(T) = θ(T) + S(T) + 1-style closed form.**
    It names Riemann's counting method and the comparison with Z sign
    changes; the closed form lives in the classical monograph literature
    (Titchmarsh (4.1) family). Our engine's S conventions are
    measurement-certified (FORMULAS.md §2.3), not text-transcribed.

**§25.11 Hurwitz Zeta Function — read (2026-09-09). CORRECTION:** the
E7b plan's reference to "DLMF 25.11, the explicit formula for the
counting path's zero content" was a section-number recall error. 25.11
is the Hurwitz zeta function (ζ(s,a) = Σ_{n=0}^∞ 1/(n+a)^s etc.). Ch. 25
carries no "explicit formula" section at all (contents read: 25.1–25.21,
no such section; the zero kernel's PRIMARY source remains Riemann 1859
p. 9, §1 above).

What 25.11 DOES give us (VERBATIM, recorded — directly relevant):
- **25.11.5 (Euler–Maclaurin; source Apostol (1976), (25), p. 269):**
  `ζ(s,a) = Σ_{n=0}^{N} 1/(n+a)^s + (N+a)^{1−s}/(s−1) − s ∫_N^∞
  {x}/(x+a)^{s+1} dx`, s ≠ 1, ℜs > 0, a > 0, N = 0,1,2,3,…
  ⇒ the residual tail past the partial sum is a bounded-function
  ({x} = fractional part = the "width") integral with a 1/(x+a) power
  kernel. This is the classical home of the project's width law:
  expanding (x+a)^{−s−1} at N, the leading sawtooth integrals produce
  exactly the P, M₁, M₂, … rung structure the M₁ machinery measures
  (P-W in POSTULATES.md; tables in the repo). The measured tables are
  the discrete exact version; 25.11.5 is the continuous classical one.

**Read status for E7b (all gates now cleared):**
- zero density kernel (single zero, amplitude, oscillation, coefficient):
  Riemann 1859 p. 9 — VERBATIM, §1.
- Z, ϑ, sign-change counting, R–S formula + O(t^{−1/4}) remainder:
  DLMF 25.10.1–25.10.3 — VERBATIM, above.
- width-law classical home (sawtooth/width EM representation):
  DLMF 25.11.5 — VERBATIM, above.
- GS pair object F(α,T) + W(u) + unconditional Montgomery theorem +
  narrow-box Theorem 1 + reduction Theorem 2: GS25 — VERBATIM, §2.
- What is NOT read and NOT needed for E7b execution: nothing remaining
  on the E7b gate. (The Titchmarsh (4.17.4) text itself, and the full
  (25.11.5)-family for L-functions (DLMF 25.15), remain optional
  extras.)

**§25.2 (iv) Infinite Products + §25.4 — READ (2026-09-09, raw .tex
endpoints — the most verbatim form DLMF provides).**

- **25.2.11 (TeX verbatim):** `\zeta(s)=\prod_p (1-p^{-s})^{-1}` — the
  Euler product (Apostol 1976, p. 231; A&S 23.2.2). This is the (25.2.11)
  that §25.10(i) cites for "ζ(s) ≠ 0 for ℜs > 1" — via the primes, not
  the zeros.
- **25.2.12 (TeX verbatim) — the product over zeros, primary form:**

  ```tex
  \zeta(s) = (2\pi)^s e^{-s-(\gamma s/2)} / [2 (s-1) \Gamma(\tfrac12 s + 1)]
             \cdot \prod_{\rho} (1 - s/\rho) e^{s/\rho}
  ```

  product over the zeros ρ with ℜρ > 0 (HTML note); γ = Euler's
  constant; Γ(½s+1) zero-encodes the trivial zeros; (s−1) the pole.
  **The per-zero factor is E₁(s/ρ) = (1−s/ρ)e^{s/ρ} — genus-1
  canonical; the e^{s/ρ} factor is load-bearing (not a phase
  decoration): its magnitude e^{Re(s/ρ)} is O(1)–exponential away from
  the zero and is what makes the product converge.**
- **25.4.1 (TeX verbatim) — the functional equation:**
  `\zeta(1-s) = 2 (2\pi)^{-s} \cos(\tfrac12 \pi s) \Gamma(s) \zeta(s)`.

**NUMERIC VERIFICATION of 25.2.12 (engine-first, before any use) —
`scripts/rh/day009_dlmf_252_12_check.py`, raw
`out_day009_dlmf_252_12_check.txt` (docker mpmath dps-30):**
- product built over BOTH signs (ℜ>0 means ½+iγ and ½−iγ for our
  certified on-line list);
- at the zero t = 14.134725142: |main·Π − ζ|: 5.4e-11 (n=500) →
  3.3e-11 (n=1000) → 2.4e-11 (n=1500) — convergent;
- at t = 10: |main·Π − ζ|: 0.896 (n=50) → 0.116 (n=1000) → 0.070 (n=2000)
  — slow off-zero convergence (active zeros γ ≤ O(t), tail ~ t²/γ²);
- at t = 100: |…| = 2.7e5 (n=500) → 3.6e3 (n=1000) → 6.1e2 (n=1500) —
  converging but requires n ≫ t² (≈ 1.5e4 zeros for 1e-3);
- DLMF 25.10.1–2 cross-check: Im[e^{iϑ(t)}·main·Π] → 0 (Z real):
  0.01996 (n=500) → 0.008871 (n=1500) at t = 10 — ϑ(t) (25.10.2)
  verified as the main phase through the zero product itself.

**Design consequence for the E7b execution (recorded):** the direct read
sum Σ_γ (canonical pair factors) at t is fully covered by our 1e5 zero
list only for t up to ≈ 1e4–2e4 (need γ_max ≈ 5–10·t for the arg to
converge to ~1e-2 in S). Beyond that (t → 1e5), the same sum is
computable with the crown-jewel zero-finder (γ_n computed on demand) or
with the RVM-density tail correction. The 4-digit onset test lives in
t ≤ 2e4 anyway (onset columns N = 1e4..1e5 at t/N = 2 ⇒ t = 2N up to
2e5… — the t ≤ 2e4 slice is the first fully-covered slice; extend with
the zero-finder).
