# FORMULAS.md — master formula ledger (the no-recall rule, enforced)

**Discipline (the no-recall rule; owner directive, 2026-09-07; companion
rule in POSTULATES P-0 item 8 = named constants):** every formula
used in this project must exist in this file BEFORE it is used, with its
label and source. If a formula is not here: read it from the primary
source (verbatim, with the page/section noted), add it here with its
label, only then use it. Training-memory recall is a forbidden source for
zero-side / engine / measured formulas. This file is the safe place; the
primary-source READS it cites are the ground it stands on.

Labels:
- **VERBATIM** — quoted from the primary source (file/section noted).
- **MEASURED** — our own output: value(s) + precision + producing file.
- **DERIVED** — derived in-project: the derivation file is named.
- **CLASSICAL** — standard theorem/identity (author/work named).
- **READ-PENDING** — needed, not yet read from the primary source. The
  read must happen before first use, then this entry is replaced by the
  verbatim text.

---

## 1. External, verbatim

### 1.1 Riemann 1859 (Wilkins translation; full read: READS-1859-GS25.md §1; local copy /tmp/pi-web-pdf/ezeta.md)

VERBATIM — the prime-density zero kernel (p. 9), **the E7b anchor**:

> "If one restricts Σ_α to a finite number of terms, then the derivative
> of the expression for f(x) or, up to a part diminishing very rapidly
> with growing x,
> **1/ln x − 2 Σ_α x^{−1/2} cos(α ln x) / ln x**
> gives an approximating expression for the density of the prime number +
> half the density of the squares of the prime numbers + a third of the
> density of the cubes of the prime numbers etc. at the magnitude x."

Per conjugate pair — the single-zero density kernel: **amplitude
x^{−1/2}/ln x, oscillation cos(γ ln x), coefficient 2**; α (Riemann's
root of ξ(iα)=0) = iγ, i.e. ρ = ½ + iγ (RH: all roots real).
(Reading note, INTERPRETATION: the x^{−1/2} is the σ = ½ unit-amplitude
signature our onset measurement reads; Riemann wrote the zero side of the
action in 1859.)

VERBATIM — the explicit formula (p. 9) and the F(x) = Σ_m (−1)^{μ_m}
f(x^{1/m}) definition: see READS-1859-GS25.md §1 (full quote preserved
there; not duplicated here to keep one copy of the verbatim text).

Modern F-type form used for the constant check (INTERPRETATION; the
constant identity must be verified dps-40 before first use — not yet
verified, do not assume): `x − Σ_ρ Li(x^ρ) − ln(2π) − ½ ln(1 − x^{−2})`.

### 1.2 GS25 — Goldston–Suriajaya, arXiv:2603.28104 (full read: READS-1859-GS25.md §2)

VERBATIM core (as recorded there):
- Pair object: **F(α,T) := Σ_{ρ,ρ'} T^{α(ρ−ρ')} W(ρ−ρ')**,
  **W(u) := 4/(4 − u²)** (Montgomery's kernel; over pairs of full zeros,
  no RH).
- **Unconditional Montgomery theorem (BGSTB24, (6.3)):** F(α,T) =
  ((1+o(1)) T^{−2α} log T + α + o(1)) · T/(2π) · log T, uniformly
  0 ≤ α ≤ 1 — without RH.
- Close-pair bound (GM87 Lemma 9, (5.1)): Σ_{|γ'−γ| ≤ h} 1 ≪ (1 + h log T)·(T log T)/T…
  (diagonal term ≤ (C+o(1)) T/(2π log T) for absolute C ≫ 2 unconditionally).
- **Theorem 2 (reduction):** if Σ_{ρ,ρ': γ=γ'} 1 ≤ (C+o(1)) T/(2π log T)
  then the proportion of zeros simple AND on the line ≥ 2 − C
  (companions (3−C)/2, (4−C)/3).
- **Theorem 1 (GS25):** zeros in narrow box |σ − ½| < b(T)/log T, b → 0
  ⇒ C = 4/3 ⇒ **≥ 2/3 simple and on the line** (Fejér-kernel proof,
  (7.1)–(8.2)).

Prior-art percentages (READS §2, verbatim from the note): Levinson 1974
34.74% simple+on-line; PRZZ20 41.7% on-line / 40.7% simple+on-line; the
Claude/2026 result 67.25% / 83.625% (b = 0.001, Tsang-family kernel,
BGSTB25 Thm 2). See also EXTERNAL-2026-claude-rh.md.

CONFLATION RULE (P-0): the GS object is a PAIR-correlation sum with
kernel W(u); our measured onset C is a SINGLE-zero object. E7b uses the
Riemann-1859 kernel; never the GS kernel (question "is W the two-zero
shadow of the single-zero action kernel?" is post-E7b).

### 1.3 DLMF and other standard references

- DLMF 25.10.2 (argument of ζ): `ϑ(t) ≡ ph Γ(¼ + ½ it) − ½ t ln π` — READ
  (25.10(i): ph = principal value, chosen to make Z(t) real). This is
  NOT the RVM main term — do not conflate (the walk's θ_walk/π and the
  RVM main differ by exactly 1: §2.3).
- **DLMF 25.10 (Zeros) — READ 2026-09-09 (full section, dlmf.nist.gov/
  25.10).** VERBATIM core (also recorded in READS-1859-GS25.md §3):
  - RH statement: all nontrivial zeros lie on the critical line ℜs = ½;
    zero-free ℜs ≥ 1 (Hadamard / de la Vallée Poussin 1896, PNT);
    trivial zeros −2n; none for ℜs ≤ 0 except trivial; critical-strip
    zeros symmetric about the real axis and the line.
  - 25.10.1: `Z(t) ≡ e^{iϑ(t)} ζ(½+it)` real, vanishes at the zeros;
    zeros separated by Z sign changes; Z changes sign infinitely often.
  - **25.10.3 (Riemann–Siegel, source Titchmarsh (4.17.4)):**
    `Z(t) = 2 Σ_{n=1}^{m} cos(ϑ(t) − t ln n)/n^{1/2} + R(t)`,
    `m = ⌊(t/2π)^{1/2}⌋` (radical dropped by text extraction; matches
    the engine and its validation), `R(t) = O(t^{−1/4})`, an
    asymptotic series ("Riemann also developed a technique for
    determining further terms").
  - DLMF prior art: first 10,000,000,000 zeros on the line (van de
    Lune et al. 1986); "More than 41% of all the zeros … on the
    critical line" (Bui et al. 2011 = PRZZ20).
  - Note: 25.10 refers to N(T) (Riemann's counting method) and to
    comparing it with Z sign changes, but prints no N(T) = … formula.
- **DLMF 25.11 (READ 2026-09-09): 25.11 is the HURWITZ zeta function —
  NOT “the explicit formula for the counting path”** (the plan's
  section number was a recall error — exactly what the ledger
  discipline is for). What is actually there, VERBATIM:
  - **25.11.5 (Euler–Maclaurin, source Apostol (25), p. 269):**
    `ζ(s,a) = Σ_{n=0}^{N} 1/(n+a)^s + (N+a)^{1−s}/(s−1)
              − s ∫_N^∞ {x}/(x+a)^{s+1} dx`,  s ≠ 1, ℜs > 0, a > 0.
    ⇒ the cell tail = `(N+a)^{1−s}/(s−1) − s ∫_N^∞ {x}/(x+a)^{s+1} dx`:
    the sawtooth {x} is the width. This is the classical home of the
    project's width (missing-term) law: the M₁ moment is the leading
    sawtooth-integral term — P-W now has a read classical reference,
    not only the measured tables.
- **RVM main term:** main(T) = (T/2π)(ln(T/2π) − 1) + 7/8 — CLASSICAL
  (Riemann–von Mangoldt; Titchmarsh (4.1) family — the DLMF prints the
  comparison N(T) vs sign changes under Riemann's method, not the
  closed form). MEASURED consistency: θ_walk/π = main − 1 to 1e-7
  (day-003); that measurement, not the text, is the certificate.
- **DLMF 25.2.11 (READ 2026-09-09, raw TeX): the Euler PRIME product**
  `ζ(s) = Π_p p^{−s}` — the ledger's "25.2.11 = product over zeros" was
  a section-number error; 25.2.11 = primes, 25.2.12 = zeros (both now
  read).
- **DLMF 25.2.12 (product over zeros) — READ 2026-09-09, raw TeX
  verbatim + numerically verified** (day009 check, out file):
  `ζ(s) = (2π)^s e^{−(1+γ_E/2)s} / [2(s−1)Γ(½s+1)] · Π_ρ (1−s/ρ)e^{s/ρ}`
  (ρ over ℜρ > 0; γ_E = Euler). Per-zero factor = genus-1 canonical
  E₁(s/ρ); the e^{s/ρ} factor is load-bearing (convergence). Verified:
  at a zero |main·Π−ζ| → 2.4e-11 (1500 zeros), Im[e^{iϑ}main·Π] → 0
  (Z-reality through the product).
- **Platt & Trudgian, J. Number Theory 147 (2015) 842–851, Corollary 1
  (p. 844) — READ 2026-09-13 from the original PDF (ANU open repository;
  cross-checked via Simonič, JNT 2021, arXiv:2010.13307 eq. (3))**: the
  Riemann–von Mangoldt remainder S(T) = N(T) − [(T/2π)log(T/2πe) + 7/8],
  N(T) = #{nontrivial ρ: 0 < ℑρ ≤ T}:
  `|S(T)| ≤ 0.110 log T + 0.290 log log T + 2.290,  T ≥ e` (unconditional.
  Consistent with our certified counts: S(3×10⁵) = −3.798 (bound 4.412);
  S(6×10⁶) = −3.935 (bound 4.804). Used as S̄ in the B-2 bound.
- **RVM two-sided N(T) estimate — the admissibility source (25ab,
  2026-09-16; CITED in `S4G.s4g_admissible`)**: the Lean admissibility
  chain uses the conservative constant set
  `|N(T) − (T/2π)log(T/(2πe))| ≤ 0.137 log T + 0.443 log log T + 4.4`
  (Backlund-form; in use since the day-025 REV2 design;
  N_rvm_low(x) := (x/2π)(log(x/2π) − 1) − (137/1000)log x −
  (443/1000)log log x − 44/10; PINNED ratio 3.24335400 at T0² = 1.21×10¹⁰,
  min 3.24203321 on [1.2×10¹⁰, 10⁴⁰] —
  day025_gapw_constants.py [4]).  VERIFIED CURRENT BEST (owner online
  check, 2026-09-15): **Bellotti–Fiori, arXiv:2412.15470 v2 (accepted
  Math. Comp.)**: for T ≥ e,
  `|N(T) − (T/2π)log(T/(2πe))| ≤ 0.10076 log T + 0.24460 log log T
  + 8.08344` — strictly sharper (prior best: Hasanalizade–Shen–Wong
  0.1038/0.2573/9.3675).  The admissibility chain closes with ratio
  ≥ 3.24 under either constant set, so the sharper set is a future
  tightening, not a requirement.  Checked, not the competitor:
  arXiv:2402.04272 (PNT ψ-formula error term).  FORMALIZED 25ac+:
  `S4G.N_rvm_low_bf` + `S4G.s4g_admissible_bf` (Lean, exact rationals
  10076/100000, 24460/100000, 808344/100000; same chain as the
  Backlund theorem; dps-50 certificate day026_admissibility_bf.py,
  ALL PASS — ratio 3.24335400295 @ T0², x-floor margin 2.6e9×).
  Bibliographic note:
  the 0.137/0.443/4.4 set is CITED as in use; a first-hand read of the
  original Backlund paper remains a pending store item.
- **DLMF 25.4.1 (functional equation) — READ 2026-09-09, raw TeX
  verbatim:** `ζ(1−s) = 2(2π)^{−s} cos(½πs) Γ(s) ζ(s)`.
- The zero kernel for E7b: the PRIMARY SOURCE is Riemann 1859 p. 9
  (§1.1 verbatim). DLMF ch. 25 carries the product form (25.2.12) and
  the R–S formula (25.10.3), not the density kernel: the kernel is
  Riemann's own.

---

## 2. Original formulas — MEASURED (value + precision + file)

### 2.1 Exact identities

**E7a — the Euler action identity** (EXACT, dps-50, 5/5 PASS; file
`scripts/rh/day006_e7a_action_identity.py`, raw `out_day006_euler_action_identity.txt`;
statement THE-EULER-ACTION.md §1). For a sequence a(n), partial sums
A(m) = Σ_{j≤m} a(j), any s, integers N < M:

```
Σ_{n=N+1}^{M} a(n) n^{−s}  =  A(M) M^{−s} − A(N) N^{−s}
    +  Σ_{m=N}^{M−1} A(m) [ m^{−s} − (m+1)^{−s} ]
```

(edge flux + rolling interior; exact finite sums, no asymptotics;
verified χ₅ paths and generic random ±1 paths at complex s).

**D = −P (two-cut consistency, the width-law certificate):** with
N₁ the first cut of the exact M₁ extraction,
`D(r) := tail(N₁)·N₁^s − s·M₁(r)/N₁  =  −P(r)` — MEASURED to 1e-10 at
every phase for q = 5, 13 (E2-exact, 18/18), q = 17 (17/17), and at
q = 24, 28, 56 (day-008). Files: `day006_e2_exact_m1.py`,
`day006_chi17_exact.py`, `day008_flatten_cusp.py` (+ raw outputs).

**Mirror & zero-sum & antipode (P-W laws)** — MEASURED, dps-35/40:
- `M₁(r) = M₁(−r mod q)` — q = 5, 13 (1e-10), 17 (3.1e-13), 24 (1.5e-12),
  28 (2.9e-12), 56 (6.7e-11).
- `Σ_r M₁(r) = 0` — q = 5, 13, 17 (1.6e-17), 24 (1.2e-12), 28 (3.5e-12),
  56 (1.2e-10).
- **Antipode sign flip (even moduli):** `M₁(r + q/2) = −M₁(r)` —
  τ₁₂ (9.6e-15 raw; 4.0 in the centered F₂₄ version is the non-
  multiplicative contrast), χ₂₄ (2.2e-13), χ₅₆ (9.7e-12). τ₁₂ table
  {2,2,1,0,−1,−2,−2,−2,−1,0,1,2} (dps-35, `day006_cyclotomic_12_24.py`).
- Integer-valuedness: q = 5 {2/5,2/5,−3/5,−3/5,2/5}; q = 13 {2,2,1,1,0,
  −2,−3,−3,−2,0,1,1,2}; q = 17 (all integers, 2.6e-9); q = 24 (8.4e-9),
  28 (1.5e-8), 56 (1.6e-7).
- t-independence: M₁(t=3) = M₁(t=10) to 1e-10 (q = 5, 13, 17).

### 2.2 The width (missing-term) law and the onset

**Width law (P-W):** the residue-cell tail at s = ½+it,
`tail_q(r; N) := Σ_{n>N, n≡r (mod q)} n^{−s}`, has the exact serial
(asymptotic-order) form

```
tail = P(r) N^{−s} + s·M₁(r) N^{−s−1} + s(s+1) M₂(r) N^{−s−2} + …
```

with P(r) the band-cumulative (exact path) and M_k (r) the Lebesgue-
width cell moments, functions of (r, χ, q) only. The M₁ rung is MEASURED
EXACTLY (three-cut extrapolation, no fitting — the 3-term trap is a
discipline rule: a 3-power-term fit once returned 7/5 where the truth is
2/5 at residual 1e-9). Convergence is in the cut, not a fit.

**Onset (P-Z, MEASURED):** the zero-oscillation C(t,N) of the ζ-tail at
s = ½+it has onset scale N ≈ t/2: **C/|I| = ½·(t/N) to 4 digits**
(day-04b, t/N crossing 1 at t/N ≈ 2; "zeros enter the budget at
t/N ≈ 2"). Files: `day004b_onset.py` + raw onset columns.

### 2.3 Count-side formulas (the walk certificate stack)

**S conventions (LOCKED, day-003/004b, verified to 1e-7):**
- main(T) := (T/2π)(ln(T/2π) − 1) + 7/8 (CLASSICAL, §1.3).
- θ_walk/π := (T/2π)(ln(T/2π) − 1) − 1/8  =  main(T) − 1 (EXACT, 1e-7).
- **S_file(T) := N(T) − θ_walk/π  =  N − main + 1** (walk convention).
- Textbook S(T) := N(T) − main(T) = S_file − 1.
- Locked: N(10⁵)=138,065, S_file = −2.558419306; N(10⁶)=1,747,142,
  S_file = −2.508632116; per-decade max|S| ∈ {4.55…4.67} (1e4–1e7 GPU
  walk, defective 10⁷ line replaced by re-walk — in progress).

**2K identity (MEASURED, dps; per-height shadow — NOT conserved):**
`2K(T) := (N(T) − main(T) + 1) − Arg ζ(½+iT)/π` with Arg the PRINCIPAL
argument of ζ (NOT the vartheta/continuous argument). Measured: −2 at
T ∈ {10⁵, 5×10⁵, 10⁶} (±6.6e-8, dps-40); 2K(γ₁₃₈,₀₆₆ ∓ 0.25) =
−2.9999999 (dps floor). **Drift (day-007, measured ≈ −3 rad⁻¹ on
zero-free intervals):** d(main)/dt ≈ ln(T/2π)/(2π) ≈ 1.54/rad and the
continuous-argument rate give d(2K)/dt ≈ −(1.54 + 1.54) — 2K drifts; a
simple on-line zero's jump cancels the drift (parity conserved mod 2
per crossing). Valid use: parity at each certified height (even =
consistent with no off-line zero below it). Certificates of record:
the S-envelope + twin-floor walk + E7b zero-term test — 2K is a shadow.

**Twin-floor rule (hard, day-003/004):** a flip-count walk at spacing dt
certifies counts only while dt < min-gap(t) in the window (floor ≈ 0.003
at 1e5–1e6, projected ≈ 9e-4 at 1e7); the certificate is the dt vs dt/2
stability re-walk (exact flip agreement), not a 2K parity. Measured
reliability: exactly 1 dead GPU chunk (256,000-point tile) in ~70,000,
≈128-rad counting blackout near t ≈ 1.06e6 (GPU walk 1e6→1e7), = 246
missed flips; detected because the flat-|S| ≈ 247 plateau is itself the
alarm; corrected N/S(10⁷) pending the re-walks.

### 2.4 Engine formulas (float64 instrument, patched 2026-09-09)

**Z_rs — 2-term Riemann–Siegel + corrected remainder (MEASURED accuracy;
file `scripts/rh/zeta_core.py`, TS port `rh-ts/src/rs-z-value-of-t.ts`,
8 goldens max diff 8.7e-10):**
```
sq = √(t/(2π));  N = ⌊sq⌋;  p = sq − N;  u = √sq;  θ = vartheta(t)
Z(t) = 2 Σ_{n=1}^{N} cos(θ − t·ln n)/√n
       + (−1)^{N−1} [ Re ψ(p)/u − ψ‴(p)/(96 π² u³) ]
```
**ψ‴ by complex step (DAY-007 FIX — the engine defect):** with
`S = Σ_{k=0}^{3} (−1)^{3−k} C(3,k) ψ(p + i k h)`, h = 1e-3, the Taylor
expansion is `S = (ih)³ ψ‴ − 1.5 h⁴ ψ⁗ + 1.25 i h⁵ ψ‴‴‴ + …`, hence
**ψ‴(p) = −Im[S]/h³** (O(h²) error ≈ 1e-6·ψ‴‴‴; verified against
mpmath `mp.diff` at 3 p-values; file `day007_psid3_fix_check.py`).
The legacy `Re[S]/h³` was an O(h·ψ⁗) residual (35× off, sign-wrong at a
p) — the port-against-known-zeros rule (P-0 addendum 7) is what caught it.
Accuracy: 2e-9…1e-8 at t ≥ 4.5e4 (float64 floor); ~5e-4 at t ≈ 41 is the
intrinsic 2-term O(u^{−5}) RS floor, NOT an engine defect.

**vartheta (dps, DLMF 25.10.2 form):** `θ(t) = Im ln Γ(¼ + it/2) − (t/2) ln π`
(Lanczos ns = 50 in the TS port; rel 6.9e-16 vs dps).

**dps evaluation floor (MEASURED, day-007):** |Z(γ_exact)| ≈ 1.5e-6 at
t ≈ 10⁵ (bisection stalls at interval ~1e-7 with |Z'| ≈ 15.6) — this is
the achievable mpmath dps-50 certification level at these heights, not
1e-45.

### 2.5 Flattening / 24-structure (2026-09-09, from the measured M₁ tables;
files `day008_flatten_cusp.py` + raw)

**The flattening (DERIVED from measured tables, shape-level float64):**
`w(r) := M₁(r) e^{2π i r / q}` — the closed loop of the cell.
- **Antipodal coincidence (even moduli):** w(r + q/2) = w(r) to 1.2e-15
  (τ₁₂), 2.2e-13 (χ₂₄), 4.4e-13 (τ₂₈), 9.7e-12 (χ₅₆) — the sign flip
  and the π-angle rotation cancel: the 24-cell object is ONE closed
  curve traced twice.
- **Cusp exactly at the quadrant cells** (r = q/4, 3q/4) in every grid.
- **Corner law (MEASURED, four-grid sequence):** the angle the two
  neighbours of a cusp cell subtend at the center =
  **180° − 720°/q**: 120.00° (q=12), 150.00° (q=24), 154.29° (q=28),
  167.14° (q=56) — exact to the printed digit; monotone to 180° ⇒ the
  continuum cusp is an OPEN smooth passage (a circle crossing the
  origin), not a pinched cardioid cusp (→ 0°).
- **Limaçon parameter** ρ = a + b cos(φ−φ₀): |a/b| = 0.0425, 0.0649,
  0.1720, 0.2504 — the circle end (|a/b| = 0), not the cardioid end
  (1). Circle fits (center, R, origin-gap, max-dev): q=12 (1.1098, 0),
  1.078, gap 0.0318, dev 0.188; q=24 (3.0006, 0), 3.0051, gap 0.0045
  (0.15% of R), dev 0.192 (3.2%); q=28 gap 0.3627 dev 0.268;
  q=56 gap 1.7906 dev 1.374 (M₁-staircase plateaus bow the arc).
- **Skew:** zero in all four multiplicative cells (M₁ strictly real);
  F₂₄ (non-multiplicative): common mass at arg 92.86° (≈93° global
  tilt), front/back residual 42 > shape scale 28 (open two-petal).

**F₂₄ raw cell (MEASURED, exact, no approximation):** front =
[1,1,2,3,5,8,1,9,10,7,5,0], back = [5,5,10,3,1,4,5,9,2,11,1,0];
**back − front ≡ 4·[1,1,2,0,2,2,1,0,1,1,2,0] (mod 12)** — halves
identical mod 4 (the quadrant part), the slide is a mod-3 shift.
Cell sum 108, mean 9/2 (code-verified). M₁ (dps-40, 6-cut LS, per-phase
guard 1e-6): all 24 = common mass (−17,470 ± 349,150i) + per-phase ≤ ~40;
antipode diff 42 (≈99% front/back identity — NOT the τ₁₂ sign flip).
**Two cell classes, two front-back laws** (multiplicative = antipode
sign flip; non-multiplicative = near-identity + mod-3 slide).

### 2.7 B-5 CORE exact ratio (FILLED 2026-09-10; PROVEN in Lean 2026-09-11)

For s = ½+it (t > 0, t ≠ γ), the 25.2.12 canonical factors
F_ρ(s) = (1 − s/ρ)·e^{s/ρ}, P_on = F_{½+iγ}·F_{½−iγ} (the B-4 pair),
P_off = ∏_{ρ∈{½+δ±iγ, ½−δ±iγ}} F_ρ, R(s,δ) = P_off/P_on:

  ω_δ := (1+2δ)/((½+δ)²+γ²) + (1−2δ)/((½−δ)²+γ²) − 1/(¼+γ²) ∈ ℝ,

  **R(s,δ) = (¼+γ²)((γ−t)²+δ²)((γ+t)²+δ²)
              / ((γ²−t²)((½+δ)²+γ²)((½−δ)²+γ²)) · e^{s·ω_δ}**   (T1)

Real signed prefactor × pure constant-rate phase; the sign flip of
(γ²−t²) at t = γ is the ONLY branch. `b5Ratio`/`b5Abs`/`b5NoffPos`/
`b5PrefSign` + the polynomial identity of the off-line numerator
((t²−γ²)² + 2δ²(t²+γ²) + δ⁴ — all-positive coefficients, no δ > 0
zero-window) are PROVEN in
`scripts/rh-lean/RhAttack/B5.lean` (Lean 4.33.1 stable + Mathlib 4.33.1;
def bodies carry the flat monomial form ¼±δ+δ²+γ² of (½±δ)²+γ²).
Verification: Python dps-30 (out_day010_b5core_check.txt, worst
|formula−direct| 5.978×10⁻²⁶, 12 configs) + Lean float64 12/12 cross-check
in `Main.lean` (day-012). Home: outline [B-5 CORE].

### 2.8 B-2 tail bound M(G,t) (DERIVED + PROVEN 2026-09-13; spec:
`spec/b2-tail-bound.md`)

On-line tail error of the density kernel, s = ½+it, 0 < t < G, t ≠ γ_k,
Re f(x) = ½/u + log(1−w/u), u = x²+¼, w = t²+¼ (γ > t; B-4 algebra):

  **E(G,t) = Re∫_G^∞ f n̂ dx − Σ_{γ_k>G} Re f(γ_k) = −Re f(G)·S(G) − ∫_G^∞ S(x) Re f′(x) dx**
  (exact; Abel + N = N̂ + S; verified on 7.4M real list zeros,
  (3×10⁵, 4×10⁶], at quadrature limit 1.1×10⁻⁵ / 1.1×10⁻³ for t = 10³/10⁴)

  ⇒  **|E(G,t)| ≤ M(G,t) := S̄(G)·B_f(G,t) + C_f(G,t)·K(G)**,
  q := (t²+¼)/G²,  S̄(x) = 0.110 ln x + 0.290 ln ln x + 2.290:
    B_f = ½/G² + q/(1−q) + t/G²,
    C_f = 1 + 2q/(1−q) + 2t,
    K(G) = [0.110(ln G+½) + 0.290(ln ln G+½) + 2.290]/(2G²)
           (= ∫_G^∞ S̄ x⁻³ dx, closed form from ∫x⁻ᵖ ln x dx and ∫ln ln x·x⁻³ dx).
  Values G = 6×10⁶ (S̄ = 4.804): M(10³)=1.3×10⁻⁷, M(10⁴)=1.3×10⁻⁵,
  M(2×10⁴)=5.3×10⁻⁵, M(5×10⁴)=3.3×10⁻⁴, M(10⁵)=1.3×10⁻³, M(2×10⁵)=5.3×10⁻³.
  The full D1 model residual R(t) = |main·e^{Σ_list f + Tt}/ζ − 1| exceeds
  M at every t (robust recompute: 8.4×10⁻⁴ … 2.98 … −8.0): the excess is
  the OFF-LINE zero-set factor beyond G (spec §6) — the §2 detector's
  signal, not kernel uncertainty. Home: outline [B-2].

### 2.6 Other measured constants

- **χ₅ drift exponent:** −1.00052 ± 0.001 (day-005/006 cross-phase
  coupling run).
- **Fibonacci band density:** S(N) ~ N^{0.24–0.25}; B(6) = B(12) = 0
  (day-005 band runs).
- **Fibonacci cell sums:** B(6) = B(12) = 0; F₂₄ mean 9/2 (§2.5).
- **E2-exact tables (dps-35, 1e-10):** χ₅ M₁ {2/5, 2/5, −3/5, −3/5, 2/5};
  χ₁₃ M₁ {2, 2, 1, 1, 0, −2, −3, −3, −2, 0, 1, 1, 2} (THE-EULER-ACTION.md
  §4b; files + raw).
- **Crown-jewel first output:** γ₁₃₈,₀₆₆ = 100000.74372338832472451031208038330078125
  (dps-50 bisection, |Z| floor 1.5e-6, Z' = −15.581, S_file(γ) =
  −2.703628652; float finder agrees to 1e-7; files `day007_zero_at_dps.py`,
  `rh-ts/src/zero-at.ts`).

---

## 3. Derived, awaiting full execution

**E7b — the zero-side kernel (DERIVED + VERIFIED 2026-09-09; two
route findings; destination THE-EULER-ACTION.md §E7b; day-009 §2-4).**

**Route a — product space (CONVERGENT, VERIFIED).** From 25.2.12,
per-zero canonical factor E(s/ρ) = (1−s/ρ)e^{s/ρ}; RH lift
1−s/ρ = i(γ−t)/(½+iγ). On-line closed form (per list-entry γ, both
conjugates):

```
|E|²_γ = (t²+γ²)² e^{(tγ+1/4)/(1/4+γ²)} / (1/4+γ²)
E_γ    = i(γ−t)/(½+iγ) · e^{(1/4+tγ)/(1/4+γ²)}     (+ conjugate)
phase_γ(t) = (π/2 − atan2(γ, 1/2)) + (t−γ)/(2(1/4+γ²))  [+π lift at t=γ]
```

Component-verified at dps-50 (day009_e7b1_f/d): per-factor arg slope
(t−γ)/(2(¼+γ²)) to 1e-12; jump exactly π at t = γ (the 2K
convention); full-product arg slope, zero-free, = mpmath ζ slope to
5e-7 rad/rad (t = 14000). **In ℜs > 1 the formula is numerically
true**: at s = 2 the product converges 3.88e-8 (100) → 1.6e-10
(12000) → 1.4e-11 (all) → 0.0 (500000, tail absorbed).
**Strip limitation (HONEST):** the product MAGNITUDE at ½+it needs
G ~ t² tail zeros (|tail| ~ exp(c·t²/G)); at t = 14000, G = 12000:
off-by 5.5e1450 in magnitude. The PHASE is unaffected. Any strip
AMPLITUDE claim needs the analytic tail correction
T(G,s) = ∫_G^∞ pairlog(γ,s)·(ln(γ/2π)/(2π))·dγ (closed-form
integrand; day009_e7b2 uses it to ~1e-3 in log units).

**Route b — x-space 1859 kernel (DIVERGENT — recorded finding).** The
Abel transform of k_ρ(x) = −2x^{−1/2}cos(γ ln x)/ln x against
(x−N)x^{−s}, ℜs = ½, carries a 1/ln x tail: ~ 2N^{1/2}/ln N, not
integrable. The 1859 zero-density kernel does NOT reproduce the ζ-tail
zero-side in the strip; its "+ smooth" remainder is load-bearing. Not
a defect to patch: the 1859 kernel stays the prime-counting object;
the zero-side ζ-tail object is the product-space kernel above. The
derived-but-divergent Abel integral K(N,½+it,ρ) = −2∫_N^∞ cos(γ ln x)
(1−N/x)x^{−it}dx/ln x is kept here as the counter-example that fixed
the route choice.

**E7b-1 target (RE-FRAMED, day-009 §4; STAGE-1 COMPLETE 20:35).** The
S-level bridge attempt (G=12000 S_cand) is a RVM consistency check (the
S walk counts zeros; S_cand drifts by the zero-density term itself) —
SUPERSEDED, see scripts/rh/day009_e7b1_h_final.py header. The real
zero⇔prime bridge is the ONSET law: measured (day-04b, 4 digits,
N-independent) C/|I| = ½·(t/N) for C = |tail+I|, tail = ζ−Pn,
I = N^{1−s}/(1−s). Zero-side prediction: |main·Π_{|γ|≤G}·e^{T(G,s)} −
(Pn−I)| / |I| at the 15 measured (N, t/N) points.
**STAGE-1 (G=3e5, CERTIFIED list N(3e5)=466,655, docker mpmath 1.3.0,
out_day009c_onset_pred_certified.txt):** CLEAN PASS (1e3, 1.0) +0.29%
and (1e4, 0.1) −1.2% (Ψ-err 6.4e-5); in-budget borderline (1e3, 2.0)
+5.8%, (1e4, 0.2) +4.2%; (1e4, ≥0.5) and all (1e5, ·) below the
zero-side error floor (C < |Ψ-error|·|ζ|) — reported as boundaries,
NOT failures. Error model (corrected 20:35, spec/onset-bridge-e7b1.md):
tail error SATURATES in G once G ≫ t (7.8e-2 @G=1e5 ≈ 8.3e-2 @G=3e5,
t=1e4) — sum-vs-∫ against actual zero spacings (S-scale), not f(G).
Honest ceiling of the density-tail method: t ~ 1e4–2e4; the N=1e5 row
needs the actual zeros up to G ≳ 5–6e6 (M5 decision matrix, on
demand). PASS/FAIL framing (pre-registered): testable points within 5%
+ monotone + slope ∈ [0.4, 0.6] (met in the clean region); FAIL =
non-explicit-formula content (new to us). **ENVIRONMENT (P-0.9, 20:35):
mpmath 1.4.1 (host) mp.quad tail defect (real part +0.003 @t=1e3 → Ψ
2.995e-3 vs true 2.292e-5) — docker 1.3.0 is the verified onset
environment; host 1.4.1 no tail quads.**

---

## 4. Classical identities used (author named)

- Riemann–von Mangoldt main term: main(T) = (T/2π)(ln(T/2π) − 1) + 7/8.
- vartheta: DLMF 25.10.2 (§1.3).
- Γ(½) = √π (Euler) — the (−½)! = √π entry of P-G (owner census).
- W(u) = 4/(4−u²) (Montgomery pair kernel) — used ONLY in the external
  comparison section, never inside our single-zero computations.
- Quadratic reciprocity residue rules for the Kronecker (2/n), (3/n),
  (7/n) tables (computed from definition in `day008_flatten_cusp.py`,
  assert-checked; (7/n) has conductor 28 since 7 ≡ 3 mod 4; 48 is NOT a
  fundamental discriminant: (48/n) = (12/n)).
- Zero-set structural facts (B-0, structural — no numeric constants):
  (a) ζ > 0 on (0,1) ⇒ no off-line zero with Re < 0 in that strip
  (citation pending, outline F-0.1); (b) trivial zeros are negative
  even integers (F-0.2); (c) non-real zeros come in 4-tuples
  {ρ, 1−ρ, ρ̄, 1−ρ̄} (F-0.3); (d) HFE Re ρ = ½ ⇔ Re(1−ρ̄) = ½ and the
  conjugate-pair map ι(ρ) = 1−ρ̄ is a fixed-point-free involution on
  the off-line zeros (F-0.4 — the heart of the even-jump argument);
  (e) RVM ⇒ finite counting slices (F-0.5). Used in Lean purely as the
  `ZeroSet` axioms of `scripts/rh-lean/RhAttack/B0.lean` — B-0 is pure
  Finset counting, so it consumes NO numeric formulas from this ledger.

## 5. Index — formula → home file

| formula | home |
|---|---|
| E7a action identity | THE-EULER-ACTION.md §1 + out_day006_euler_action_identity.txt |
| width law / M₁ tables | THE-EULER-ACTION.md §4b + rh-missing-tail results/width-ladder-tables.md |
| onset C/|I| = ½·t/N | day-004b + results/certified-zero-survey.md |
| 2K / S / main / twin-floor | POSTULATES.md P-0 + results/certified-zero-survey.md |
| Z_rs / ψ‴ / vartheta / floors | scripts/rh/zeta_core.py + day-007 check |
| flattening / 24-structure | day-008 + results/width-ladder-tables.md §11 |
| 1859 / GS25 verbatim | READS-1859-GS25.md |
| B-0 structural facts (ZeroSet axioms) | scripts/rh-lean/RhAttack/B0.lean + day-011 §4d |
| B-5 CORE ratio R(s,δ) + ω_δ (§2.7) | outline [B-5 CORE] + day-012 + scripts/rh-lean/RhAttack/B5.lean |
| B-2 tail bound M(G,t) (§2.8) + S̄ (Platt–Trudgian Cor 1, §1.3) | spec/b2-tail-bound.md + day-013 |
| Claude-2026 prior art | EXTERNAL-2026-claude-rh.md |
