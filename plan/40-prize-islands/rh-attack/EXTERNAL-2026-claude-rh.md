# EXTERNAL: the 2026-08 Anthropic/Claude Riemann-zeros result (prior art + contrast)

Recorded 2026-09-09 (owner pointed it out: "improved the provable
proportion from ~41% to ~60%"). Verified against primary sources the same
day. **We do NOT follow their trail — but we read it, and we position
ourselves against it.**

## What they proved

**Paper:** "More than two thirds of the zeros of the Riemann zeta
function lie on the critical line" — arXiv 2608.13637 (2026-08-02),
cleaner version arXiv 2609.02882 (2026-09-02); Anthropic release note:
anthropic.com/research/riemann-zeta.

- Unconditional: **≥ 2/3 (0.6725 with an optimised test family) of the
  non-trivial zeros in (T, 2T] are simple AND on the critical line**, and
  **≥ 5/6 (0.83625) are distinct**, as T → ∞ (liminf / (1−o(1))).
- Previous unconditional records: **5/12 = 41.67%** simple-and-on-line
  (this is the "~41%" figure) and **0.6603** distinct.
- Lineage of the result (the whole school, unchanged): Selberg 1942
  (positive proportion) → Levinson 1974 (1/3) → Conrey 1989 (40% simple)
  → records 5/12 + 0.6603 → this work.
- Method (from the abstracts): a **direct generalization of Montgomery's
  1973 deduction** (2/3 of zeros simple, *assuming* RH) — made
  unconditional by replacing "RH" with an explicit **estimate for a
  double sum over the zeros** (their 2025 note "Zeta Zeros in a Narrow
  Vertical Box", arXiv 2603.28104: "RH can be replaced with a general
  estimate for a double sum over zeros"), plus an **optimised test-family
  ("Montgomery–Taylor window")**. Self-described: "new, conceptually
  simpler, unconditional proof".
- Process (per the release note / press): argument **discovered and
  written by Claude** (unreleased research version), problem posed and
  guided by Jarred Sumner; **verified by Brian Conrey and Dan Goldston**
  (the two record-holders of the old bound) plus internal mathematicians;
  shipped with a **sorry-free Lean 4 formalisation**. RH itself: untouched
  (SciAm, 2026-08: "math's most famous problem is no closer to being
  solved").

## What it is, structurally

- A **global proportion theorem**: a liminf statement over ALL zeros in
  (T, 2T] as T → ∞. Statistical; says nothing about any individual zero,
  any individual t, any prime, any finite range.
- A **moment / test-family method**: the whole 50-year Conrey–Goldston
  school (positivity of a quadratic form in zero data + explicit
  zero-side estimates). The AI's contribution is *reorganization +
  optimization of known machinery*: finding where an explicit double-sum
  estimate replaces the RH assumption, and tuning the test family.
- No missing-tail analysis, no Euler–Maclaurin cell structure, no
  S-walks, no finite-range certificates, no primes.

## What it is NOT (and why "they didn't take the reductionist path"
holds)

- No local, per-scale structure: our program measures the *missing tail
  at each (t, N)* with explicit orders; theirs integrates over the whole
  decade asymptotically.
- No counterexample machine: our walk *finds* an off-line pair if one
  exists in walked range (2K jump + S anomaly + localizable pair); a
  proportion bound can never find one — 32.75% of zeros could be
  off-line forever and their theorem would still hold.
- No finite-range absolute: we hold "NO off-line pair below 10⁶"
  (100%, certified, 1.75·10⁶ zeros) — a species of statement their
  method cannot produce.

## Complementary, not competing

| | their theorem | our certificates |
|---|---|---|
| range | all T → ∞ (liminf) | [0, 10⁶] absolute → 10⁷ pending |
| guarantee | 67.25% of zeros good | 100% of zeros good (in range) |
| species | theorem (unconditional) | verified computation (dt/2 + dps) |
| counterexamples | cannot find any | finds them if in range |

Both can be true simultaneously, and they are.

## Consequences for our program (actionable)

1. **READ before E5** (the zero-side identification): the paper + the
   GS25 note (arXiv 2603.28104). E5 puts the classical explicit
   zero-side sum in missing-tail language; their double-sum-over-zeros
   estimate is adjacent machinery — we position against it, not past it.
2. **Calibration of the "known-but-reorganized" status**: their biggest
   RH-adjacent advance of the year is a *reorganization + optimization
   + formal verification of 40-year-old known tools*. That validates the
   reductionist-reorganization strategy the owner insists on: the value
   was in the joints, not in new axioms.
3. Our prior-art map for the structure layer (measured 2026-09-09):
   - RS remainder / "onset at N ≈ √(t/2π)" landscape: Berry 1995 (RS
     expansion, high orders, divergent, terms decrease until r* ≈ 2πt);
     **Trudgian 2011 I/II** (Math. Comp.: *sharp rigorous bounds for the
     first ten remainder terms on the line* — and the resulting
     algorithm is the one inside **mpmath**, which our oracle literally
     runs). → the *qualitative onset* = known; our 4-digit measurement
     (C/|I| = ½·t/N, bend N-dependence 1.062 → 1.473) is a sharper
     re-measurement of that landscape, interpreted as ½-term/catch-up.
   - Character tail expansions: **Berndt 1975** ("Character analogues of
     the Poisson and Euler–Maclaurin summation formulas", J. Number
     Theory 7(4):413–445): generalized Bernoulli polynomials = period
     cell integrals. → the *framework* behind P-W's M₁ = known; the
     specific two-valued χ₅ table {2/5, −3/5}, the χ₁₃ integer row, and
     the cross-phase drift coupling (Re: other group's moment, Im: own)
     are instances we measured, not found in the literature surveyed.
   - Our genuinely new objects (as of this audit): (a) the unification
     statement (the ζ half-term −½N^{−s} = M₁(ζ) of the same cell-width
     ladder as the χ moments); (b) the Half Postulate census; (c) the
     P-W/P-Z separation with a *measured* onset scale; (d) the
     instrument: twin-floor S-walks at 10⁷ scale with the GPU-reliability
     model and the defect-catch protocol.
4. **The Lean 4 formalisation exists and is public.** Our postulates
   (P-W P-G P-Z) will need exactly this discipline at the theorem stage:
   measure → conjecture → formal statement → (eventually) machine-checked
   proof. Note it now.

Sources (accessed 2026-09-09):
- arxiv.org/abs/2609.02882 · arxiv.org/html/2608.13637v1, v2
- anthropic.com/research/riemann-zeta (+ anthropic CDN PDFs of both)
- doi.org/10.48550/arxiv.2603.28104 (GS25 narrow-vertical-box)
- scientificamerican.com "No, Anthropic's AI didn't just solve math's
  hardest problem" (2026-08)
- temperaturezero.com 2026-08-11 (record-lineage detail: 5/12, 0.6603)
- royalsocietypublishing.org/doi/10.1098/rspa.1995.0093 (Berry 1995)
- doi.org/10.1090/s0025-5718-2010-02426-3 (Trudgian 2011)
- sciencedirect sciencedirect 0022314X75900451 (Berndt 1975)
