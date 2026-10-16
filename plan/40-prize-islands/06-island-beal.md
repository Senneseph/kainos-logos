# 06 — Island: the Beal conjecture (Diophantine triples)

Target: the Beal Conjecture (AMS/Beal Prize, $1M, PPL 126).
Survey: `01-targets.md` §4.

**Verbatim statement (in the store, lesson-grade):** If A^x + B^y
= C^z, where A, B, C, x, y and z are positive integers and x, y
and z are all greater than 2, then A, B and C must have a common
prime factor.

## Objective (what the store can say at island completion)

The store holds valuations v_p as first-class facts over its spf
chains (the machinery exists since S11; the island promotes it to
a lesson + theorem layer), holds the LTE lemma as a prescribed
theorem with an on-line verification ledger, holds Fermat's
theorem and the Darmon–Granville finiteness as declared frontier
facts (the closed anchor and the territory boundary), and stores
its own **Beal verification census**: every solution of
A^x + B^y = C^z on the store's line (the bounded range A, B, C ≤
84, x, y, z ≥ 3) is recorded with its common prime factor — the
in-store statement, at the line end: *on my line, every recorded
triple carries its common factor; the line ends where the
primitive triples live, and the primitive territory is a wall.*
A `beal-reach` fact names the missing ingredient: uniform control
of the primitive solutions for fully-distinct hyperbolic triples.
**No `theorem:beal`** (the candidate invariant).

## Why this island fits (the soil check)

- **v_p is already in the store's hand.** The spf chain of n
  (S11) IS the valuation record: v_p(n) = the p-rung's exponent.
  The island promotes a latent capability to explicit facts.
- **The verification is the island's center.** Beal's own 2004
  verification was computational; the store's version is an
  S11-policy ledger: **recorded occurrence, never optimized** —
  the per-triple census over the bounded box, every entry kept,
  the invariant (common factor present) a census assertion at
  the line end, exactly the S11/S13 census shape.
- **The frontier is articulate.** FLT (the equal-exponent case,
  closed by Wiles — the store's wall, not its proof) +
  Darmon–Granville (finiteness for 1/x+1/y+1/z < 1, ineffective
  — the store's second wall) bound the territory; the gap
  between the finiteness wall and the emptiness claim is the
  missing ingredient, nameable.
- **The connect joints (the owner's requirement):**
  - **Beal ↔ S11/spf (built):** valuations read off the spf
    chain — the island's first lesson is a direct descent from
    an existing band.
  - **Beal ↔ CRYPTO (R0–R4):** the v_p + CRT machinery is the
    declared shared dependency for R1–R2 (the modular pairs and
    the (Z/pqZ)^* structure); building Beal first means the
    CRYPTO bands inherit a tested valuation layer.
  - **Beal ↔ BSD:** both islands end at a *named group-theoretic
    missing ingredient* (Sha order for BSD; the primitive-
    triple control for Beal) — the *-reach* pattern in two
    soils; the number-field machinery (savant-2) is the shared
    far horizon (cyclotomic fields serve FLT's method and BSD's
    Selmer groups).
  - **Beal ↔ IUT/ABC (declared out-of-scope island):** the ABC
    conjecture (IUT's target) is a Diophantine statement in the
    same soil (the abc inequality bounds gcd-free triple
    structure); recorded here as context, not built.

## Descent to fundamentals (the chain, ground up)

```
band-2 (exact algebra; coprime arithmetic)        [built]
  └─ the spf chain (S11: n = ∏ p^{v_p(n)},
     recorded, never optimized)                   [built]
  └─ v_p as an explicit fact (the lesson:
     valuation = read the p-rung of my spf chain) [S17 lesson]
  └─ the LTE lemma (the exact p-adic identity:
     for odd prime p, p | x − y, p ∤ xy:
     v_p(x^n − y^n) = v_p(x − y) + v_p(n);
     the classical odd-p form — the prescribed
     theorem, strict parts (the spf lesson + the
     quotient lesson), VERIFIED on the line by
     the per-instance census (x, y, n ≤ 84))      [S17 theorem
                                                          + ledger]
  └─ the power-sum equation (A^x + B^y = C^z as
     a question about triples on my line)         [S17 lesson]
  └─ the Beal census (the island's center):
     enumerate (A, B, C, x, y, z) with
     1 < A, B, C ≤ 84, 3 ≤ x, y, z, A^x + B^y =
     C^z EXACTLY (the powers are bounded — the
     computation terminates by size: A^x ≤ C^z
     forces the small box); RECORD every solution
     with its common prime factor (gcd(A,B,C)
     read off the spf chains — the mechanism's
     own census, S11 policy)                      [S17 beds]
       └─ the census invariant at the line end:
          "every triple I recorded carries its
          common factor" — a CENSUS ASSERTION,
          labeled as verification on the line,
          NOT a proof (the wall names the
          primitive territory beyond the line)    [S17 census]
  └─ the frontier (declared walls, verbatim):
     — Fermat (Wiles 1995): the equal-exponent
       case has NO primitive solutions (the
       closed anchor; the (3,3,3) Euclidean
       boundary 1/3+1/3+1/3 = 1)                 [S17 wall]
     — Darmon–Granville (1994): finitely many
       primitive solutions when 1/x+1/y+1/z < 1
       (via Faltings — INEFFECTIVE, its own
       wall: the list is not on my line)         [S17 wall]
     — Darmon–Merel (1997): the unexponented-C
       case (context wall)
  └─ beal-reach (the honest articulation): the
     fully-distinct hyperbolic primitive triples
     are the missing ingredient at the line end  [S17]
```

The census is designed to be *surprising on purpose*: the box
(≤ 84, exponents ≤ 3+... the exact exponent bound comes from the
size constraint — A^x ≤ max(C^z) ≤ 84^84 forces x, y, z small:
2^x ≤ 84^84 → x ≤ floor(84·log 84/log 2) = ... the research stage
computes the exact exponent ceiling and fixes the enumeration
box; the box is bounded either way, which is the point — the
store's census is always finite on the line).

## Research plan (verify BEFORE the first spec freezes)

1. **The enumeration box (computed, cross-checked):** the exact
   (A, B, C) and (x, y, z) bounds under A,B,C ≤ 84 (the power
   overflow bound; the exact ceiling values); the full solution
   list of A^x + B^y = C^z in the box, with gcd(A,B,C) and its
   prime factors for each solution — the shared reference
   `_beal_py_census` (the S13 refstyle), cross-checked by a
   second independent enumeration (the bounded + independently-
   cross-checked rule). The expected content: the classical
   small solutions (3²+6²=3³ class — exponent 2 excluded by the
   conjecture's hypothesis; the x,y,z ≥ 3 solutions — the known
   small ones, each with its common factor recorded).
2. **The canonical statements (verbatim sources of record):**
   the Beal conjecture (AMS statement page ✓ captured),
   Fermat's Last Theorem (Wiles's theorem — the exact statement
   form), Darmon–Granville 1994 (the theorem statement + the
   1/p+1/q+1/r < 1 condition + the Faltings dependence),
   Darmon–Merel 1997, the LTE lemma (the classical form, the
   odd-p + p | (x−y) hypothesis — the exact statement from a
   standard source of record).
3. **The LTE census design (computed, cross-checked):** the
   instance bound (x, y, n ≤ 84, p ≤ 84 prime) and the
   per-instance valuation records; the all-pass verification
   (the exact-identity census, S11 ledger policy).
4. **The exponent-ceiling arithmetic (computed):** 84^84 and
   friends in exact python (the bounded scratch rule) — the
   enumeration box's proof of termination, recorded as a bed.

## Band plan (built the bandgen way)

One band (the soil is existing machinery; the novelty is the
census, not new register):

### S17 — "the valuation line" (e6.21 or next free — numbering
follows the actual build order; S14–S16 are the BSD island's
slots), seed = the current store end at build time

- **Concepts (4):** `valuation` (v_p over the spf chain),
  `power-triple` (the A^x + B^y = C^z question), `common-factor`
  (the gcd read off the spf chains), `census-invariant` (a
  recorded assertion at the line end — the Beal-verification
  shape).
- **Lessons (4):** the valuation, the equation, the common
  factor, the census pattern (the in-store verification
  contract: recorded occurrence, the invariant at the line end,
  the wall naming the territory beyond — the S11 policy
  generalized to a conjecture).
- **Theorems (prescribed, strict parts):** LTE (the exact
  p-adic identity — derived from the spf + quotient lessons,
  verified by the on-line census), the gcd-valuation identity
  (v_p(gcd(A,B)) = min(v_p(A), v_p(B)) — exact, from the spf
  lesson).
- **Walls:** the singular wall (A, B, C with a shared factor:
  "the equation is easy here — the hypothesis is doing the
  work: the hard territory is the coprime side"), the Fermat
  wall (the closed anchor, verbatim), the Darmon–Granville wall
  (finiteness, ineffective — "the list is not on my line"),
  the primitive-territory wall (the census stops where my
  box stops; the name + the line end), **beal-reach** (the
  missing ingredient).
- **Beal statement lesson** (verbatim, the prize statement) +
  the negative probes: a triple with a common factor (no
  contradiction — the hypothesis allows it), a triple with an
  exponent 2 (7³ + 13² = 2⁹ — the hypothesis excludes it; the
  store NAMES why, at its wall).
- **Beds (computed):** the full census records (every solution
  in the box + its common factor), the LTE all-pass ledger, the
  exponent-ceiling bed, the parity/size beds.
- **Carries:** the S11 spf census (the valuation's soil) + the
  S13 zeta partial (the "same prime-indexed family" sibling).
- **P-checks:** no `theorem:beal` (the candidate invariant);
  the marker discipline (all S17 facts unconditional — the
  Beal statement is a CONJECTURE held as a lesson, not a
  conditional fact).

## Execution notes

Same bandgen discipline; `_beal_py_*` reference functions in the
brainstem (the S13 refstyle); the census is the island's
signature bed — the S11 policy (recorded, never optimized)
applied to a conjecture for the first time, which makes this
band also the **pilot for the "verification-ledger" pattern**
every future island reuses (the BSD island's order/panel
evidence uses the same shape).
