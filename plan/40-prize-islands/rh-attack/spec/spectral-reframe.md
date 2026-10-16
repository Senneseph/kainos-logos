# SPEC — the spectral reframe (eigen-value route) of the open theorem

Status: **speculation / narrowing note** (day-023, owner-requested). Not a
proof artifact — lives in the working tree per the repo-split rule. The
proof repository (`rh-missing-tail`) is unaffected. Companion: the pre-
project song `A_SPECTRAL_SOLUTION.md` (owner: its spectral imagery is its
own provenance, not a claim about this work; no edits).

## 0. What the route is (citations verified day-023, web)

- **Nyman–Beurling / Baez–Duarte**: RH ⟺ step functions {λ/x − λ{1/x}}
  total in L²(0,1) (equivalently the Baez–Duarte set total in a Hardy
  space). Survey: arXiv math/0607733. Quantitative refinement (arXiv
  math/9910055): ∏_ρ(1 − 1/ρ) (over off-line ρ) is the NORM OF THE
  PROJECTION of 1 to that span — a measurable norm, our flavor.
- **Zeros-as-spectrum constructions**: Connes-type operator whose
  spectrum IS the non-trivial zeros, with the explicit formula recovered
  as a character formula (arXiv math/0412277); Berry–Keating H = xp
  (Phys. Rev. Lett. 118, 130201) with broken PT-symmetry.
- **Spectral flow** (arXiv 2406.01828, 2024): crossing-parity of the
  zero-heights as levels of a family; S-matrix from the Euler product.

The song's verse 3 ("if the operator stayed Hermitian, its frequencies
couldn't stray") is Hilbert–Pólya stated as music: reality of the
spectrum ⟺ self-adjointness (spectral theorem).

## 1. The exact map: our pieces ↔ their spectral referents

| Our piece | Spectral referent |
|---|---|
| 1859 kernel K(s; G) (log form) | spectral generating function (Fredholm-determinant shape: log K = Tr log(I − A)) |
| Riemann–von Mangoldt | Weyl law (spectral counting function) |
| S(t) | oscillatory remainder of the Weyl law (phase of the counting function) |
| definition side Pₙ + I(n,s) | geometric side: a truncated trace = aliasing (trapezoidal-rule) expansion of the smooth part |
| detector R(s,δ) (B5 closed form) | spectral-perturbation signature: move one eigenvalue off the real axis by δ → log-spectral function changes by exactly R − 1 |
| no-dead-window (b5NoffPositive) | no trace-invisible perturbation (Newton-identity rigidity, made infinite) |
| C1a pole facts | the signature DIVERGES at the eigenvalue's own spectral parameter (strongest non-invisibility) |
| P8 floor Wₙ + M(G,t) | trace-noise floor of the un-perturbed expansion (EM aliasing wire + zero-density tail wire) |
| P9 closure | the squeeze: geometric-side observable change < minimal spectral signature ⇒ no off-line mass |
| 2K even (Route B) | spectral flow mod 2 (crossing parity); twins = degeneracy events; dt₂ twin floor = measured degeneracy floor |
| PinCensus (c_k pins) | values of the same spectral product P(s) at the trivial points — an independent spectral census |

## 2. THE NARROWING — the open theorem as a two-constant inequality

> **P1.2 = uniform trace-rigidity of the explicit formula:**
>
>     N(t) < f_min(t)   for all t,
>
> - `f_min(t)` = the minimal off-line spectral signature. Near: ≥ 0.998·|K|
>   (PINNED; and ∞ at own height — C1a). Far: (t/γ)²·|K| (A4.1,
>   LEAN-PROVEN). δ-uniform: all-positive-coefficient δ-polynomial
>   (B5, LEAN-PROVEN).
> - `N(t)` = the zero-free definition-side trace noise: the EM
>   aliasing (P4Limit L5 bound, the n-side) + the zero-density tail
>   wire M(G,t) (B3Sbar `b3BoundExplicit`), as wired by P8Floor
>   A4.3 (`p8_residual_wired`).

**State of the two constants (day-023):**
- `f_min`: mostly machine-proven already. The spectral route explains
  why B5's no-dead-window is deep (Newton-identity fact), and C1a
  sharpens it to ∞ at own height.
- `N(t)`: the whole open content. The route identifies the SHAPE of the
  missing bound: an **aliasing bound on the t side** — N(t) must be
  controlled jointly by both wires (the EM band at n AND the tail at G)
  being simultaneously below f_min at the same height. This is why t/B
  (not t alone) is the true variable, and why the 1×10⁷ repair walk
  (day-023, running) IS the noise-floor measurement for the uniform
  theorem.

## 3. Concrete deliverables

1. **Name the theorem** (done in §2): P1.2 = uniform trace-rigidity
   (N < f_min ∀t). A wall gets a name, two named constants, a known
   lower bound on one. Proof attempts can target the two sides
   separately and meet in the middle.
2. **One-lemma Lean gap (candidate for the next P9-side commit):** the
   *self-signature pole* corollary — "an off-line eigenvalue produces a
   divergent log-signature at its own spectral parameter." C1a proves
   the pole mass is positive finite (p9_poff_own_height_pos) and the
   kernel change is exact; the ∞-statement (R → ∞ at t = g) is a
   one-line corollary not yet written as a theorem.
3. **Route B restated as spectral flow + degeneracy floor:** 2K even ∀t
   = crossing-parity conservation. Under continuous deformation,
   crossings are conserved, so the theorem reduces to (i) parity at a
   reference height (CERTIFIED: 2K(10⁷) even, day-014) + (ii) a
   degeneracy floor (twin events cannot annihilate parity). The dt₂
   protocol measures (ii): min gap 0.0023 on (10⁵, 6×10⁶] (day-023
   re-measure) = the first degeneracy-floor datum for Route B.

## 4. The honest wall

This is a REFRAMING, not a bypass. Hilbert–Pólya-style constructions
exist precisely because "build the self-adjoint operator" is itself as
hard as RH — the reality of the spectrum is the content, not the
construction. What the route buys: the name of P1.2, the shape of the
missing bound (t-side aliasing), and the Route B degeneracy-floor
program — all pointing at our EXISTING measurements (the 10⁷ walk,
the twin floors, the Xval pin) rather than at new ones.

## 5. BSY-1: the k = 1 pin, resolved and measured (day-023)

The parked "Baez–Duarte projection norm vs PinCensus P(s)" speculation
resolves to a named theorem and a measured certificate.

**Theorem (cited, sources read day-023).**
- Burnol (Contemp. Math. 287, 23-26, 2001, "A note on Nyman\u2019s
equivalent formulation of the RH", arXiv math/9910055), Thm 1.2:
  ‖P(**1**)‖ = ∏_{Re ρ > 1/2} |(1−ρ)/ρ| (multiplicities; P = the
  orthogonal projection onto the Nyman–Beurling subspace NB of
  L²((0,1))).
- Balazard–Saias–Yor ("Notes sur la fonction ζ de Riemann, 2", Adv.
  Math. 143 (1999) 284-287): s = 1 specialization of the factorization
  (s−1)ζ(s)/s = E(s)·B(s) (E = on-line factor fixed by the boundary
  modulus = **our bridge factor** at s = 1; B = the Blaschke product
  over the off-line zeros; single-pair B-factor = the B5 ratio
  quotient):

    I = (1/2π) ∫_{Re w = 1/2} log|ζ(w)| / |w|² |dw|
      = (1/π) ∫_0^∞ log|Z(t)| / (1/4 + t²) dt
      = Σ_{Re ρ > 1/2} log|ρ/(1−ρ)|   (each term ≥ 0)

    I = 0  ⟺  no off-line zeros  ⟺  RH.

  Sensitivity: one off-line pair at height γ, distance δ, adds
  ≈ 2δ/γ² — the t⁻² species of the PinCensus, but δ-WEIGHTED (the
  count part is absent: the BSY sum sees the DISPLACEMENT, not the
  count). Relation to our pin at s₀ = −2 (k = 1): the pin signature =
  count part (−4k/t, d-blind, absorbed by the Hadamard identity) +
  d-sensitive part (4kδ/t², buried under truncation); BSY-I is the
  k = 1 d-sensitive REMAINDER with the truncation eliminated by the
  exact integral. The pin family is now complete: {count: PinCensus
  k = 1,2,3,5,10; δ: BSY-I}.

**Measurement (day-023; `scripts/rh/day023_bsy1.py` →
`scripts/rh/out_day023_bsy1.txt`, 147 s, 12-way CPU):**
- I[0, 10⁶] = **+1.594668050404×10⁻⁶** — RH-consistent at the stated
  error level 2.1768×10⁻⁵ (quadrature 2×10⁻⁵ + audited tail 1.77×10⁻⁶).
- Audits (all PASS): list-driven cell census = **1,747,142 = the
  certified N(10⁶) exactly** (the quadrature independently counts all
  the zeros); engine sign-flip at every list zero 1,747,129/1,747,129
  (the 13 scalar-band zeros covered by the dps-30 spot checks, 196/200
  at 1.45×10⁻⁶ worst — the expected log-amplification of the 5×10⁻⁸
  engine error at small |Z|); convexity envelope audited, not recalled.
- **Certificate: excludes off-line pairs with Σ 2δ/γ² > 6.5×10⁻⁵
  (3-σ). e^I − 1 = 1.59×10⁻⁶ = the B(1) Blaschke-norm defect (= 1 −
  ‖P(1)‖ to first order) on the measured band.**
- Independence: no zero walk, no S/2K parity, no N(t) count enters the
  integrand — only log|ζ(½+it)| on the line. It is the fourth
  instrument species now running in parallel: {S/2K parity, walk
  count, PinCensus count, BSY-I δ}.
- Sharpening (day-024 candidate, after the 10⁷ walk frees cores):
  extend T to 10⁷ (tail → ~3×10⁻⁷, band-D Δ to 0.125 → quadrature
  → ~5×10⁻⁶) ⇒ error level ~10⁻⁵ ⇒ certificate Σ 2δ/γ² > 3×10⁻⁵·...
  the δ-sensitive census reaches the PinCensus depth with a δ instead
  of a count in the numerator.

## 7. The F₁ / absolute-geometry reading (day-023: worth as a LENS, not as an execution route)

The Weil-conjecture analogy (RH for function fields — Deligne via the
cohomological machinery Grothendieck built; the dream of Spec Z as a
"curve over F₁" so that a Lefschetz trace formula gives RH the same
way) is the program of Connes/Consani/Lozetti/Lorscheid/Soulé/
Schaeffer et al. State of the art, checked day-023 (NOT recalled):

- Connes–Consani–Moscovici, **"Zeta spectral triples"** (arXiv
  2511.22755, 2025; EMS book series 2025): self-adjoint operators
  D_log^{(λ,N)} (rank-one perturbations of the scaling-operator triple)
  "whose spectra coincide" with the zeros — a PROPOSED STRATEGY;
  the self-adjointness is the content, relative to spectral
  assumptions (the usual Hilbert–Pólya wall).
- Connes–Consani–Moscovici, **"Schemes over F₁ and zeta functions"**
  (Compositio Math. 2025): the real counting function N(q) of the
  hypothetical C = Spec Z over F₁, zeta = the COMPLETE Riemann zeta;
  a functorial F₁-scheme theory reconciling Soulé and Deitmar (Kato
  monoid geometry). OBJECT-MKING: progress, and no RH.
- Connes, **"An essay on the Riemann Hypothesis"** (alainconnes.org):
  "a geometric framework... allowing us to transpose several of the
  key ingredients of the geometric proof of RH for function fields... **It
  is yet unclear if this is the right set-up for the final
  Riemann–Roch step**" — the most authoritative line on the wall.
- Connes–Consani, **"The Weil proof and the geometry of the adeles
  class space"** (arXiv math/0703392): the explicit dictionary between
  Weil's proof (curves, divisors, Riemann–Roch, Frobenius) and the
  adelic class space — the reading instrument below.
- Lorscheid, **blueprints** (arXiv 1103.1745 et seq.): a real
  F₁-scheme theory (Kato–Deitmar–CC reconciled), zeta functional
  equations for F₁-schemes — scheme theory without RH.

**Judgment: NOT an execution route for us.** (i) The wall is
object-construction, not a missing theorem: the absolute point / F₁-
schemes are not yet in usable form, and the field's own leader says
the Riemann–Roch set-up is unproven — our methodology (spec → Lean →
compute) runs on existing objects; F₁ geometry's epistemic state is
"machinery missing", not "one theorem missing". (ii) Even the best
active attempt (CC–M spectral triples, 2025) is a strategy whose
self-adjointness is the hypothesis. (iii) Cost: re-deriving a decade
of frontier work at sub-frontier level, with no reachable endpoint
this year. **Track, don't do**: if a closed Riemann–Roch identity /
intersection theory for the arithmetic surface Spec Z × Spec Z lands
(Compositio 2025 is the direction), P1.2 may collapse to a
verification step — literature-watch item, not our work.

**Worth as a lens — three formalized items.**

**(a) Our closure is already in Deligne's shape.** The function-field
proof: eigenvalues appear in the Lefschetz TRACE; the SAME eigenvalues
are bounded by the NORM side (Riemann–Roch = positivity of the
intersection form); the squeeze = trace side demands an eigenvalue
exist, norm side bounds it. Ours:
| Weil/Deligne | Our argument |
|---|---|
| Lefschetz trace (eigenvalue appearance) | zero side: the kernel / B-s Blaschke product / B5 ratio R |
| norm side (Riemann–Roch, intersection form) | definition side: Wₙ aliasing + M(G,t) tail wire (p8_B, p8_residual_wired) |
| eigenvalue magnitude bound \|λ\| = q^{1/2} | f_min(t) (0.998\|K\| near; (t/γ)²\|K\| far; ∞ at own height — C1a) |
| the squeeze (trace vs norm) | C5/C5b: N(t) < f_min(t) — the two-constant theorem IS the arithmetic form of "norm side < minimal eigenvalue signature" |

**(b) The missing object has a name now: our Riemann–Roch identity.**
In Deligne's world the norm side is an IDENTITY (the RR sum is a
degree of an effective divisor — positive, exact). Our norm side is
identity + ERROR (the EM wire + the M wire). **P1.2 is exactly the
question of whether that error is controllable by the minimal
eigenvalue signature** — i.e. P1.2 is our "standard conjectures"
item (Grothendieck's RR-for-cycles, the content Grothendieck listed
as unproven arithmetic-geometric machinery). The F₁ program is the
project of making that Riemann–Roch exact; we do not build it, but
naming the gap this way is the narrowing.

**(c) The concrete part of the geometric program is ALREADY
measured: BSY-1.** The analytic skeleton of the CC adelic-class-space
program (the H² Hardy-space face — Nyman–Beurling/Baez–Duarte, the
space their "Weil proof dictionary" maps divisors/Riemann–Roch to)
carries exactly the object Burnol measured day-023:
‖P(1)‖ = |B(1)|, the projection norm = the Blaschke product over the
off-line zeros = e^{−I} (I = the BSY integral). **We have measured the
s = 1 concrete content of the geometric program** (I = +1.59×10⁻⁶,
RH-consistent at 2.2×10⁻⁵, §5): the pin family {count: PinCensus,
δ: BSY-I} is the arithmetic that the CC–M dictionary would produce
for its H² face, and it runs on our existing engines.

One-line synthesis: **the F₁ route is the same argument we have, in
its most ambitious dress — our two-constant theorem is the Hodge-index
question of that picture, BSY-1 its measured s = 1 norm, and the
missing Riemann–Roch identity is P1.2.** The lens sharpens the
architecture (confirmed Deligne-shape), names the gap (RR identity),
and explains why the B5/C1a "no trace-invisible eigenvalue" machinery
is deep (it is the semisimplicity Deligne's positivity replaces).

## 8. Open speculation (parked, pre-registered if pursued)

- **The t-side aliasing lemma (P1.2 half-b)**: state N(t) ≤ C(t/B)^a ·
  (EM wire + tail wire) with EXPLICIT a, C — and check the measured
  erosion curves (day-022b/c upper-band outputs) for the aliasing
  exponent. The measured P1.1c/d/E statistics are already the
  experimental input.
