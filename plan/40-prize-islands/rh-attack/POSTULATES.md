# The Postulates (working hypotheses, labeled evidence)

Operating rule: a **postulate** here is a precisely stated, *falsifiable*
hypothesis with (a) the measured/classical evidence that motivates it, and
(b) one or more named experiments that would kill it. Nothing here is a
theorem. Labels used throughout: **MEASURED** (this project, engine +
verification trail in `scripts/`), **CLASSICAL** (textbook, cited),
**INFERRED** (interpretation of measured data), **PREDICTED** (untested
consequence of a postulate).

---

## P-W — the Width Postulate (missing tails are cell-width expansions)

**Setup.** Let χ be a nontrivial Dirichlet character mod q; let
A(x) = Σ_{n≤x} χ(n) (the *band cumulative*: a zero-mean periodic step
function, period q); r := N mod q; P(r) := Σ_{j=1..r} χ(j).

**P-W.1 (the expansion).** The missing tail

    T_χ(N, s) := Σ_{n>N} χ(n) n^{−s},   s = σ + it, σ > 0

has an asymptotic expansion in N^{−1},

    T_χ(N, s) = −P(r) N^{−s} + s·M₁(r,χ) N^{−s−1} + s(s+1)·M₂(r,χ) N^{−s−2} + ⋯

where the M_k are **rational coefficients depending only on the period
cell geometry (χ, q, r)** — the Euler–Maclaurin / Abel–Poisson moments of
the cell integral ∫_N^∞ A(x)x^{−s−1}dx. Equivalently: *every series-side
term of a periodic missing tail is a finite computation from the period
cells; the s-dependence is a falling factorial of weight k.* The ζ case
(χ ≡ 1, mean 1) is the same expansion starting one order higher with the
pole (mean)·N^{1−s}/(1−s) — our Day-4 missing-term law.

**Evidence.**
- **MEASURED (χ₅, k = 0 and 1, all five phases):** D(r) = −P(r) to
  1e-8..1e-12 and M₁(r) = +2/5 (r ∈ {0,1,4}), −3/5 (r ∈ {2,3}) at 7–9
  digits, t = 1..1000, two independent stacks (float64 TS block-form vs
  dps-40 mpmath Hurwitz-ζ oracle; 22/22 cross-checks; N-convergence to
  1e6 now measured directly: c_r(N)/s → M₁ with drift A·N^{−1.000±0.001}).
  The t = 1000 "drift" of Day-5 is explained by this N⁻¹ convergence, not a
  law breakdown. (day-005 §8, day-006 §1.)
- **MEASURED (χ₁₃, k = 0, all thirteen phases):** D(r) = −P(r) to
  1e-7..1e-12 (18 phases total across q = 5 and 13 — the band identity is
  universal in q so far). **M₁ for the P(r) = 0 phases (r = 0,2,6,10,12):
  integers 2, 1, −3, 1, 2** (4+ digits, dps-45, 5-point exact-elimination
  fit). M₁ for the P(r) ≠ 0 phases: PENDING a clean convergence run (see
  the 3-term trap below) — the day-5 convention value is the quantity to
  quote: c_r(N) := (T + P(r)N^{−s})N^{s+1} → s·M₁(r).
- **MEASURED (ζ, pole + k = 1):** N^{1−σ}/|1−s| and −½N^{−s} exact
  (Day-4, 3–5 digits, CPU = GPU); and the onset curve C/|I| = ½·(t/N) to 4
  digits for t/N = 0.1, 0.2, 0.5 — the coefficient of the half-term is
  itself measured, and onset "t/N ≈ 2" is exactly ½·t = N where the
  half-term catches the pole term.
- **THE UNIFICATION (measured in all three lines above):** the ζ half-term
  −½N^{−s} and the χ₅/χ₁₃ M₁-terms are the *same object* — the first
  cell-width moment of the tail. Mean-1 series (ζ) start with the pole
  (mean)·N^{1−s}/(1−s); mean-0 series (nontrivial χ) start at the band
  −P(r)N^{−s}; in both cases the next term is s times a rational
  cell-moment, and **the ½ of the half-term is M₁(ζ) = −1/2, the same role
  as 2/5, −3/5 (χ₅) and the χ₁₃ integers.** One ladder, two entry points.
- M₁ is rational **to measurement precision** for every measured instance
  (χ₅: /5; χ₁₃ P=0 phases: integers). Exact rational form: PREDICTED,
  code-computation pending.

**Day-006 second-order measurement (χ₅ r = 1, t = 10, 7-point N from
1e4 to 1e6, dps-45):**

    c_r(N)/s  =  M₁(r) + (0.6 + 0.4i)·(t/N) + O(N^{−2})
              =  2/5 + (3/5)(t/N) + i·(2/5)(t/N) + O(N^{−2})

  exponent = −1.0005 ± 0.001, A = 4.021 (4 digits). The N⁻¹ drift is
  **t-linear and moment-weighted**: the **imaginary** part carries M₁(r)
  itself (2/5) and the **real** part carries the *other phase-group's*
  moment (3/5 = |M₁(group B)|) — a first measured instance of cross-phase
  moment coupling. Weight structure PREDICTED by P-W.1 survives (term k
  ∝ polynomial in s of degree k+1): k = 0 measured at degree 1 (∝ s, 9
  digits), k = 1 measured ∝ t (4 digits, one phase).

**The 3-term trap (honest wall, measured):** a 3-power-term extrapolation
(T ~ DN^{−s} + EN^{−s−1} + FN^{−s−2}) fitted on 5 cuts in [5e4, 1e5] with a
single rotating Fz-phase **mis-models the remainder**: for χ₅ it returns
E₁/s = 7/5 instead of the true 2/5 (and E₃/s = −18/5 instead of −3/5) on
every P(r) ≠ 0 phase, while being exact on the P(r) = 0 phases — D-residual
1e-9 *at the fit points*, off by 1.0 in E at N = 1e4. The remainder is not
a single F·e^{−it ln N}/N per phase. **Rule: never quote E from a 3-term
extrapolation; converge c_r(N) directly (or fit the drift, which has a
clean single exponent).** (All P(r) = 0 phases are safe either way.)

**Falsifiers.**
- **P-W.2 (generality in q).** Fix χ₁₃ (odd q, different period shape):
  (a) the measured M₁ table (float64, N grid per phase) equals the
  dps-40 cell-moment oracle at **all 13 phases** within convergence
  tolerance; (b) the table values are rational × s with denominators
  dividing a small multiple of 13; (c) phases related by multiplication by
  units of (Z/13Z)× carry a structured relation in M₁ (the orbit law is to
  be *read off the measurement*, not assumed). A single phase missing the
  rational-moment structure refutes P-W.1 as stated.
- **P-W.3 (second order; the onset bend).** The per-phase O(N^{−s−2})
  coefficient is also a rational moment × s(s+1); **and** for ζ the
  measured onset-bend N-dependence (C/|I| = 1.062 at N ≤ 1e4 vs 1.473 at
  N = 1e5, t/N = 2) is *reproduced* by the k = 2 cell term. If the bend
  has N-dependence that no rational moment can match, the series side
  carries hidden zero content at order 2 — the separation postulate (P-Z)
  fails earlier than predicted.
- **P-W.4 (non-multiplicative cells: F mod 12, period 24).** The Fibonacci
  residue sequence (period 24, **MEASURED** lift sum 108, mean 9/2, period
  closes) has the same expansion *with a pole*:
  T(N,s) = (9/2)N^{1−s}/(1−s) + B(r)N^{−s} + s·M₁₂₄(r,…)N^{−s−1} + ⋯ —
  the 24-phase band table B and moment table are measurable; P-W predicts
  the same weight structure for a non-multiplicative periodic cell
  function. (The owner's "12-/24-adic periods as Lebesgue widths" question
  is P-W applied to F mod 12.)
- **P-W.5 (the zero-side boundary).** The cell-side expansion is exact at
  every order *as a function of the period data alone*; zero content of
  L(s,χ) is unique remainder beyond the cell scale — **MEASURED** for ζ at
  the onset ½·t = N (zero-oscillation term ≍ band term); **PREDICTED** for
  χ₅ to first appear at order k = 2.

- **P-W.6 (front/back = antipodal structure; even moduli; Day-007).** The
  first even modulus, τ₁₂ (primitive real Dirichlet, 12 = 2×4×3), gives the
  measured structure: **(a)** antipode **M₁(r + q/2) = −M₁(r)** (front ↔
  back = sign flip) at 1e-10..1e-14, with the character itself carrying it
  (τ₁₂(r+6) = −τ₁₂(r) on its support); **(b)** mirror M₁(r) = M₁(−r) at
  6.5e-14; **(c)** trace Σ_r M₁(r) = 0 at 3.3e-14; **(d)** quadrant orbits
  (r, r+3, r+6, r+9) decompose into antipode sign-flip pairs, each orbit
  summing to 0. In 2×4×3 language: 2 = sign flip, 4 = zero-sum quadrant
  orbit, 3 = number of orbits. *Measured at q = 12 only*; the extension to
  all even moduli is the falsifier (τ₂₀/τ₂₈ queued). Non-multiplicative
  cells organize front/back differently: F₂₄ (fib-mod-12, mean-centered)
  has back = front + a 4-quadrant modular offset (halves identical mod 4,
  the slide is mod 3) in the raw cell, and in M₁ the halves agree to ~99%
  (max antipode diff 42 vs common mass 3.5e5, dps-40 6-cut fit, relative
  guard 1e-6) — **front/back = near-identity, not sign flip.** Two cell
  classes, two front-back laws.

---

## P-G — the Half Postulate (one ½, many homes)

**Statement.** Every ½ that has appeared in this attack (measured or
classical) is an instance of a single mechanism: **½ is the measure of a
half-cell (half-endpoint/half-width) or the fixed point of a self-operation
(self-mirror / self-composition).**

**The census (as of Day-005):**
1. **Critical line** σ = ½: fixed point of the ζ functional-equation
   involution; **MEASURED** isometric pairing |χ| = 1 on the line (Day-3 M1).
2. **√N price**: the convergence price N^{1−σ} becomes √N on the line —
   the half-exponent; **MEASURED** (Day-4, 3–5 digits).
3. **The half-term** −½N^{−s}: the half-endpoint (trapezoid) of the
   missing-tail trapezoid rule; **MEASURED** as a coefficient via the onset
   curve C/|I| = ½(t/N) to 4 digits (Day-4/5).
4. **(−½)! = √π**: fixed point (s = ½) of the gamma mirror Γ(s)Γ(1−s) =
   π/sin πs; the pairing constant π split half-and-half across the mirror;
   the exact twin of home 1 (CLASSICAL, owner-carried).
5. **The tower's half-attractor**: x^{x^{x⋯}} = ½ uniquely at x = 1/4
   (4^{−½} = ½; W-exact via u·e^u = ln 4 → u = ln 2); the tower's
   existence range [e^{−e}, e^{1/e}] is bounded by |f'| = 1 at the
   attractor — a merge (e^{−e}, two fixed points fuse) and a sign-flip
   (e^{1/e}, f' = −1, period doubling); CLASSICAL, owner-carried. Note the
   merge/flip pair is structurally our hidden-twin / flip-walk pair.
6. **(p±1)/2**: the square-difference bookkeeping p = ((p+1)/2)² −
   ((p−1)/2)² — ½ first visible in the prime bookkeeping (Day-2 level).

**Conjectural glue (INFERRED, unproven).** In the width-expansion language,
"half" always enters as the weight-1 moment of a half-width cell: the ½ in
home 3 is *the M₁ coefficient of the trapezoid cell*; the ½ in homes 1 and
4 are the mirror's fixed point. When the closed-form cell-moment formulas
land (P-W.2/P-W.3), check whether ½ appears in M₁(r,χ) for **every** q —
if it does, the six homes collapse to one measured mechanism.

---

## P-Z — the Separation Postulate (series side vs zero side)

**Statement.** In the missing-tail asymptotics of an L-series at
s = ½ + it, the two contents *separate by scale*:

- the **series side** (cell/width terms, P-W) is exactly computable from
  the period data alone, at every order;
- the **zero side** (the actual zero structure of L(s,χ)) is the unique
  non-computable-from-cells content and enters first, as an oscillatory
  remainder, at the scale where the cell terms and the zero-oscillation
  become comparable.

**Evidence / status.** For ζ: **MEASURED** — the zero side's first
appearance is the onset band at ½·t = N (C/|I| = 1, 4 digits; the N-
dependence at the bend is the next cell order, P-W.3). For χ₅: the series
side is clean through order k = 1 at all phases up to t = 1000 (**MEASU-
RED**); first zero-side signature **PREDICTED** at order k = 2.

**Corollary (the counting program, labeled).** While the zero side stays
below the cell scale, the on-line count and the total-zero
Riemann–von Mangoldt count agree. **MEASURED:** 2K = −2 (even, O(1)) at
t = 5×10⁵ and 10⁶ (dps-40) → *no room for even one off-line pair below
10⁶*; the S(10⁷) walk + 2K(10⁷) extends this to 10⁷ (in progress).

**Falsifier.** Any phase/order where the measured remainder deviates
from the rational cell-moment prediction by more than the convergence
tolerance *before* the predicted scale — i.e., zero content leaking into
the series side early — refutes P-Z (and with it, the counting corollary's
interpretation, though never its arithmetic).

---

## P-A — Action and Rolling (analogy layer, labeled 2026-09-09)

Owner-proposed physics images, audited against the measurements. Rule:
"action" is used only for a written functional with a named stationary
point; "rolling" only for an explicit phase trajectory. What survives the
audit:

**A1 (least-action frontier — MEASURED, via classical optimality).** The
Riemann–Siegel approximation is an asymptotic series whose omitted error
is stationary (least term) at N ≈ √(t/2π): a true stationarity statement
(Berry 1995; Trudgian 2011 rigorous bounds — the mpmath engine uses it).
Our measured onset (zero-oscillation term ≍ cell/band term, C/|I| =
½·(t/N) crossing 1 at t/N = 2) **is the boundary of that optimal-truncation
region**: the approximation is laziest at its optimal order, and the onset
is exactly where its laziness runs out and zero content appears. The ½ in
½·t = N is the boundary-cell (square) weight. Reading: *least action lives
on the approximation (the truncation), not on the primes* — the primes are
the fixed landscape; the action is on the lens. (The PNT itself has the
family's known home: density 1/log x = minimum-constraint / maximum-
entropy placement, the Cramér model — one line of the owner's sentence,
already classical.)

**A2 (the oscilloscope circle — MEASURED).** The complex trajectory
c_r(N) is a **decaying rotating spiral converging to s·M₁(r)**:
c_r(N)/s = M₁ + (0.6+0.4i)·t/N + O(N⁻²) with the e^{−2it ln N} rotation —
a circle "lying down but spinning" whose radius decays 1/N. The day-006
"3-term trap" was the oscilloscope's classic artifact: fitting a single
rotation component to multi-component motion.

**A3 (tautochrone — MEASURED, strongest form).** Tautochrone = equal
arrival time independent of release point. Measured analog: the
convergence EXONENT of the missing tail to its cell floor is
**phase-universal: −1.0005 ± 0.001** (χ₅ r=1, 7-point fit; same O(N⁻¹)
across all five phases, two stacks). Release from any phase arrives at
s·M₁ at the same rate; only the amplitude differs (the brachistochrone
axis — untested).

**A4 (rolling cycle / oloid — PREDICTED, falsifiable: E6).** The cycloid
is a circle rolling on a line; the analog is the **phase trace M₁(r) as
the period rolls** (r = 0..q−1): a closed polygonal trace whose jumps are
the cell values (a q-gon rolling trace). **First measured invariant (χ₅):
Σ_r M₁(r) = 3·(2/5) + 2·(−3/5) = 0 exactly — the rolling trace closes with
a zero centroid height** (flat-rolling, the oloid's constant-height
property). **E6**: measure the F₂₄ 24-phase trace (the E4 table) and test
the rolling invariants (sum/mean, variance, enclosed area, constant height
under roll). If the non-multiplicative cell also closes with an invariant
centroid, the rolling law is universal over periodic cell functions. The
"three cylinders" = the three ladders (ζ mean-1, χ zero-mean multiplicative,
F₂₄ non-multiplicative) sharing one cross-section = P-W's generality claim.

**What does not carry (stated, per discipline):** the primes/zeros do not
roll, move, or minimize — they are the fixed set; every "action/rolling"
statement in this project is about the *approximation's* trajectory in
complex phase space. A literal zero-side action exists in the known
**Berry–Keating** program (1999: zeros as energy levels of a Hermitian
quantum Hamiltonian — the action is there by quantum mechanics); our onset
can be read as the **semi-classical turning point** where the quantum (zero)
part of the missing tail becomes visible in the cell (WKB) approximation —
**INTERPRETATION, untested**; read that literature before E5, position
against it.

---

## P-E — the Euler Action Identity (VERIFIED EXACT 2026-09-09)

Full document: THE-EULER-ACTION.md. The original Euler problem (Dirichlet
sum from the series side) is exactly a flat 1D action:

    Σ_{n=N+1}^{M} a(n) n^{−s} = A(M)M^{−s} − A(N)N^{−s} + s ∫_N^M A(u) u^{−s−1} du
    (A(u) = Σ_{n≤u} a(n);  EXACT for every step path, every s — E7a,
     dps-50 residuals 1e-51..1e-53, periodic and random paths)

Consequences (labeled):
- THE ACTION IS CLOSED (total differential) ⇒ every path is stationary ⇒
  the series-side laws (D=−P, the width ladder) are UNIVERSAL by
  construction; they cannot see zeros or t at order 0.
- Recognition map: D=−P = edge flux; M₁/M₂ = exact interior action of the
  period cells (E2 Hurwitz form = its exact evaluation); ½ = boundary
  action of the smooth path at the edge (the square); onset ½·t = N =
  edge-action vs zero-interior-action budget crossing; Z(t) = interior
  action of the explicit-formula path at optimal truncation.
- P-Z (Separation) = the **exact/remainder decomposition of this action**:
  exact part = period data (computed at every order); remainder = zero
  content of the path (unique, enters at the measured onset).
- KNOWN part: Abel/Stieltjes identity, explicit formula, Berry optimal
  truncation. NEW part: flatness-as-universality, the recognition map, the
  budget-crossing onset reading, E7a/E7b.
- Falsifier P-E.1: any case where the finite identity fails above dps
  (none found; 5/5). P-E.2: E2 Hurwitz closed form vs infinity-limit serial
  form at full dps. **STATUS (2026-09-09): P-E.2 PASS at 1e-10, 18/18
  phases (χ₅+χ₁₃), exact form, zero fits — see THE-EULER-ACTION.md §4b.**
  Full χ₁₃ M₁ table: {2,2,1,1,0,−2,−3,−3,−2,0,1,1,2} (all integers).
  New measured symmetries: M₁(r)=M₁(−r mod q) ∀r; Σ_r M₁(r)=0 at q=5,13
  (rolling zero-centroid trace); M₁ t-independent to 1e-10.
  P-E.3 (the big one): E7b — the measured zero oscillation C at onset
  decomposes spectrally over the zero list with the Riemann-1859 kernel
  (READS-1859-GS25.md; DLMF ch.25 does NOT contain the explicit formula —
  checked), nearest zero dominant.
  **STATUS (2026-09-09): read gate complete (1859 p.9, 25.10, 25.11.5,
  25.2.11 = PRIME product, 25.2.12 = zero product — the ledger had the
  sections swapped; 25.4.1).** **The zero-space (1859 x-kernel) route is
  DIVERGENT (recorded finding, not a defect): the correct kernel is the
  closed-form product-space one (derived + component-verified, day-009
  §2).** **25.2.12 verified at s=2 (convergence 1.4e-11 + tail = 0.0;
  formula numerically true).** S-level bridge attempt (G=12000) is a RVM
  consistency check, not the bridge — the S walk is zero-side bookkeeping.
  **E7b-1 := onset-law prediction** (zero-side 25.2.12 + analytic tail vs
  the 15 measured day-04b onset points, 4-digit law C/|I| = ½·(t/N),
  N-independent): **first run COMPLETE (day-009 §6, out_day009_e7b2_*.txt)**
  — region-limited PASS with an error budget: (1e4, 0.1) −0.4%, (1e3, 1.0)
  +0.10% (the 4-digit point), (1e4, 0.2) +5.0%, (1e3, 2.0) +6.3%
  borderline; all other points inside the quantified tail-density error
  channel O(f(G)·S_osc) (localization: G=5e4→1.2e-2, G=1e5→7.8e-2, dps-30
  no change). The N=1e5 row needs zeros ABOVE 1e5: the 1e5→3e5 GPU
  extension walk is the next input (P-0.8-compliant script).
- WALL: exactness holds for bounded (mean-zero) paths; the ζ case (A = u)
  is the regularized version — pole + half-term = regularized edge action.

---

## P-0 — the Discipline (operating postulates, already standing)

1. **Constants are computed, never recalled.** (Two incidents this project:
   the F₂₄ lift sum 118 → verified 108; the M113 "43-digit prime" →
   composite.)
2. **Every count is a resolution-limited measurement:** dt < twin-floor(t)
   plus a dt/2 stability re-walk; 2K is a parity check only, never a count
   verifier (the Day-4 −38 lesson: an even error passes the mod-2 check).
   **Addendum (day-009): the 2-term float64 engine is twin-safe only for
   t ≳ 1e5 (O(u^{−5}) ~ 5e-4 at t ~ 1e4 → 38-20 missed flips on
   [1e4, 1.9e4] vs the certified zero list N(1.9e4) = 21,211). LOW-t
   sign-walk evidence from the float64 2-term engine is unreliable; use
   dps below 1e5. The day-003/004 CPU file S_t_walk_1e4_1e5.txt is
   DEFECTIVE (dt=0.1 > twin floor below ~2e4) — the dps-40 spot
   certifications (S(1e5), S(1e6), 2K) that don't use that file are
   unaffected.**
3. **Every measurement ships with two engines** (independent summation
   order or independent arithmetic, e.g. float64 TS vs dps-40 mpmath) and
   a named tolerance.
4. **Projections use measured per-evaluation cost at the target scale** —
   not at the calibration scale (the S(1e7) rate dropped 3.75 → 1.2
   Mpts/s as cos-argument scale grew).
5. **2K is a per-height shadow, not a conserved certificate (Day-007
correction).** 2K(T) = (N − main + 1) − argζ/π drifts on zero-free
intervals at ≈ −(ṁain + continuous Ṡ) ≈ −3.0/rad and cancels exactly at
simple on-line zeros; its *parity at a certified height* (even = consistent
with no off-line zero below that height) is the valid use, and it stands
as a reading at 1e5/5e5 — but it is NOT a quantity conserved between
heights, and it is a shadow of the S-envelope + twin-floor count + E5 zero-
term test, which are the certificates of record.
6. **CPU walk jobs: single-threaded BLAS, captured output (Day-007).**
   `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1` on every
   walk launch (a 16-thread OpenBLAS pool costs ~1–5 ms per small dot and
   turned a 5-minute re-walk into a 3.5-hour stall with TIME > ELAPSED as
   the symptom), and the output file in the same command line (a re-launch
   that printed to /dev/null lost its capture and had to be redone).
7. **A port is a free re-audit (Day-007).** Porting Z(t) to TS put the
   engine at a known zero (γ₇) for the first time; the golden set then
   caught a ψ‴ defect (Re vs Im complex-step part; 35× / wrong-sign
   derivative; ~1e-4 zero-location offset at small t) that three days of
   oracle comparisons had not, because no test ever evaluated the engine
   AT a zero. Every engine port must include at least one known-zero
   golden.
8. **Named constants, no magic numbers (owner's hygiene regimen,
   Day-009 evening).** Every special value (window edges, step sizes,
   precisions, tolerances, sample counts, conductors) is a NAMED
   module-level constant, written once, and every code path refers to the
   name — never to a literal or a recomputation of it. Every long-running
   job ECHOES its resolved constants and the derived grid invariants
   (n_samples, t_end = W0 + n_samples·dt must equal W1 to < dt/2,
   expected wall time from the measured per-evaluation cost) in its first
   output lines and ASSERTS them before spending a second of compute; a
   mismatch aborts. Incident record (the motive): the day-009 zero-walk
   extension was launched over a window estimated 1000× too small in the
   sizing arithmetic (the window is 5.9e6 rad wide, not 5.9e3), so a job
   intended to run ~10 min was actually a ~5-day job at 2.36e10 samples —
   killed at hour 1 by the timeout, but a startup echo asserting
   t_end == W1 and n_samples == (W1−W0)/dt would have aborted it in
   seconds. Companion rule: **derived quantities are recomputed from the
   named constants, never typed** (n_samples from (W1−W0)/DT, never a
   hand-typed integer).
9. **A result is only valid for the code+data state that made it
   (owner directive, Day-009 evening).** If a bug or a defective input is
   found in a script or a file, every earlier result that depended on it
   is INVALID until re-run on the fixed state — and the re-run happens
   before the fixed code is cited anywhere (journal, ledger, repo), with
   a "re-run on <fix>" line. No stale numbers may remain in the record as
   if current. Incident record (the motive, same session): (a) the
   onset-prediction script shipped without the product phase `ar
   (lnPsi = logmain + la only) — the first run was garbage and the fixed
   version was the one cited (OK only because the +13000% error was
   visible); (b) the S-level bridge attempt (G=12000 S_cand) ran on the
   CPU S-walk file [1e4,1e5] that was LATER flagged defective (dt=0.1 >
   twin floor) and was never re-run after the flag — its drift
   diagnosis partially rests on contaminated data; (c) the defective
   file S_t_walk_1e4_1p9e4_gpu_dt00025.txt (36M rows) was written by a
   version of the re-walk whose engine was already known to be
   twin-unsafe below 1e5 — it exists on disk and in the last commit as a
   landmine. Companion: every cited result line carries its provenance
   (script at the revision that made it + input file); "re-run" is part
   of the fix, not a follow-up. Owner framing: this is the
   self-sabotage loop (find bug → don't re-run → confused by stale
   results) and it is now a discipline violation, not bad luck.

---

### Status of the postulates (2026-09-09, evening)

| postulate | strongest evidence | next falsifier |
|---|---|---|
| P-W.1 | D = −P 18 phases (q=5,13); M₁: χ₅ 9 digits 2 stacks; χ₁₃ integers at 5 phases; drift = (3/5+2i/5 i)t/N at χ₅ r=1 | clean χ₁₃ M₁ table (all 13 phases); M₂ per phase |
| P-W.3 | ζ onset bend N-dependence, 4 digits | same as above (the drift *is* the k=1-in-c term) |
| P-W.4 | F₂₄ mean 9/2 verified (108/24) | F₂₄ tail first two terms |
| P-G | six homes + the M₁ = −½ unification | ½-in-M₁ for every q |
| P-Z | 2K = −2 at 5e5 & 1e6 (per-height readings; Day-007 drift correction: not conserved between heights); onset ½·t = N | **CLOSED (day-014, M3)**: re-walks landed — +244 direct count (246 falsified); N(1e7) = 21,136,121, S(1e7) = −3.2057 (dps-45), 2K(1e7) = −2; off-line pair exclusion 10⁶ → **10⁷** |
| P-W.6 | τ₁₂ antipode sign-flip + mirror + zero trace (q=12); F₂₄ front/back near-identity (dps-40) | τ₂₀/τ₂₈ (even); q=17 odd-modulus M₁ table (running) |

Day-006 lesson shipped as P-0 addendum: **phases live in the cuts** — every
N in a convergence run must be ≡ r (mod q); two of three day-006 runs were
invalidated by float-truncated cut lists (86399 ≡ 4 mod 5) and by mixed
residues mod 13. Check residues before arithmetic.
