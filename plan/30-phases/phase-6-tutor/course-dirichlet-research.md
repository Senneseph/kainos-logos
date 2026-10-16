# DIRICHLET COURSE — RESEARCH (pre-registered, 2026-08-27)

Owner-directed (recorded in the course ledger, 2026-08-27):
prepare a course on the arblib Dirichlet L-function module —
`https://arblib.org/acb_dirichlet.html`. Grounded in the
store's OWN BYTES (the S21 final store
`results/phase-6/e6.25-run1/codeX-S04.json`, 1871
assertions, identity `77e07edf42292f88`, line 0..84) plus
computation verified 2026-08-27 (mpmath 1.4.1, 45–60 digits)
against that seed. The store speaks, not the hand.

## D1 — The owner's brief (as given)

> prepare a course on this:
> https://arblib.org/acb_dirichlet.html

The module (re-fetched and read in full, 2026-08-27) covers,
in its own sections: Dirichlet L-functions and the trivial
character as zeta; roots of unity and character groups
(including the Conrey DFT `f̂(χ) = Σ χ̄(x) f(x)` and Conrey's
isomorphism G → Ĝ); the Riemann xi functional equation;
Riemann–Siegel; Hurwitz L-decomposition; Stieltjes,
Gauss-sum and Jacobi-sum methods (naive/factor/order-2/
theta versions; the Gauss-route identity
J_q(a,b)G_q(ab) = G_q(a)G_q(b) "this assumes ab is
primitive"); theta series with FE
`t θ(a,t) = ε(χ) θ(1/a,1/t)`; root numbers with FE
`(q/π)^{(s+p)/2} Γ((s+p)/2) L(s,χ) = ε(χ) (q/π)^{(1−s+p)/2}
Γ((1−s+p)/2) L(1−s, χ̄)`; Hardy's Z function "`Z(t) =
e^{iθ(t)}L(1/2+it)` which is real for real t" ("Currently,
these methods require chi to be a primitive character");
Gram points ("the unique solution in [7,∞) of θ(g_n) = πn";
"only the Gram points corresponding to the Riemann zeta
function are supported, and both G and chi must be set to
NULL"); `zeta_nzeros` ("computes the number of zeros (counted
with multiplicity) of ζ(s) in the region 0 < Im(s) ≤ t");
Turing's method (Rosser's rule: "if Rosser's rule holds for
at least B consecutive Gram blocks whose union is
[g_n, g_p), then N(g_n) ≤ n+1 and N(g_p) ≥ p+1"); Platt's
method ("this function has the same zeros as ζ(1/2+it), and
is real for t by the functional equation"); the Hurwitz
decomposition `L(s,χ) = q^{−s} Σ_{k=1}^{q} χ(k) ζ(s, k/q)`;
the Euler-product inversion `1/L(s,χ) = Π_p(1 − χ(p)p^{−s})
= Σ μ(k)χ(k)/k^s` (finite for re(s) ≥ 2); the principal-
character pole ("removing the pole with residue Σ χ(k) =
φ(q)/q at s = 1"); and the module's own note "Note that the
alternating character (1,-1) itself is not a Dirichlet
character."

## D0 — Scope ruling

- THREE bands (one course = a small track):
  **S28 = E6.32 "the character line"**, **S29 = E6.33 "the
  Gauss line"**, **S30 = E6.34 "the zero census"** — the 56th,
  57th and 58th experiments. Reserved session slots after
  S27 = E6.31 (the primes-and-squares course, pre-registered).
  Build order is the owner's call; each band seeds from the
  final store of its predecessor in the chain.
- This is a NEW owner-directed track over a declared source
  module. It is NOT a lot of the declared FUNDAMENTALS
  queue: `theorem:queue-declared` stays byte-intact — lot 3
  ("the zero count at height T") KEEPS ITS SLOT: this course
  teaches the counting machinery as DECLARED-MODULE facts of
  record, it does not consume the lot (no lot-band, no fifth
  lot, P5 on the gate). And NOT a new island.
- **The GRH ruling (settled BEFORE any band):** the module
  states no hypothesis for L(s,χ) at all. The course does
  NOT file any generalization of `conjecture:riemann`: the
  conjecture stays zeta's, byte-identical, an open status
  surface never a premise; W-S30-3 punishes the misreading.
- **Seed rule (house, proportions pattern):** if the owner
  routes this course next, S28 seeds from the S21 final
  (1871, `77e07edf42292f88`); if the owner builds S22–S27
  first, S28 seeds from the S27 final. Every claim in this
  research is verified against the S21 final and is
  self-standing — S22–S27 only ADD facts and never move any
  S21-final byte (subset discipline), so the pre-reg stands
  on either seed; the control re-referees on the actual seed
  at freeze.
- **On-line/off-line ruling (settled BEFORE any band):** the
  line is 0..84. On-line: integer censuses (φ(q) counts,
  group sizes, periods, the zero count twenty-two), named
  rationals (the residues φ(q)/q — 8/15 at fifteen, 2/7 at
  the line end), named radicals (i√3, 2i, √5, 2√2, 2√3),
  and the declared names (Turing, Platt, Gram, Rosser).
  Off-line (walls/beds only, declared "a numerical check,
  not proof" — the store's own `lemma:num-zeros` pattern):
  zero heights (the two neighbors straddling eighty-four:
  82.910380854086, 84.735492980517), L-value decimals (the
  Catalan value of L(2,χ₄) to twenty digits, the s = 1
  constants), Gram-point values, sample Z-values. NO NEW
  DECIMALS enter the floor; the register discipline is
  policed by P0 + P5 + P6, and the per-band walls name each
  off-line value with the line end.

## D2 — Grounded census (the seed's own bytes + verified math)

### (a) Soil the store already holds (probe-verified; mastery
states from the S21 seed side, frozen in E6.25's FROZEN
`pre_s21_states`, 79 stable / 41 practicing, K = 4)

| concept | state | correct | the byte (abridged) |
|---------|-------|---------|---------------------|
| `zeta-series` | **stable** | 7 | "the zeta function is the sum over all n of n to the power minus s, and it converges when the real part of s is greater than one — the root of the track" |
| `euler-factor` | **stable** | 9 | the Euler-factor soil (primes as the atoms of zeta) |
| `zeta-cont` | practicing | 3 | "continues to a meromorphic function on the whole plane; its only singularity is a simple pole at s = 1 with residue 1" |
| `func-eq` | practicing | 14 | "xi(s) equals xi(1 minus s) — the functional equation, the symmetry every zero reflection and zero count rides on" |
| `trivial-zeros` | practicing | — | "zeta is exactly zero at every negative even integer … zeroed by the sine factor" |
| `num-zeros` | established byte | — | "the first nontrivial zero of zeta is at height 14.1347, to four decimals — the next three at 21.0221, 25.0109 and 30.4249 … a numerical check, not a proof" — CITED-UNTOUCHED |
| `rv-count` | practicing | 10 | "the riemann-von mangoldt counting formula … the census the hypothesis would complete" |
| `s-of-t` | practicing | 3 | "the sharp counting formula … S of T is 1 over pi times the argument of zeta on the critical line" |
| `st-eq` | practicing | 3 | "the Riemann hypothesis is equivalent to S of T being little-o of log T" |
| `hardy-line` | practicing | 5 | Hardy's theorem: infinitely many line zeros |
| `zero-density` / `zero-free` / `mean-square` | practicing | 4 / 13 / — | the zero-count neighborhood (S12 frontier) |
| `divides` / `composite` / `first-divisor` | **stable** | 5 / 7 / 36 | the line's elementary soil (pre-req candidates) |
| `mult-within-100` / `add-two-digit` / `count-successor` | **stable** | 9 / 11 / 14 | the drill soil (pre-req candidates) |
| `mod4-split` | **stable** | 10 | "the line splits at four" (pre-req candidate — character values ride on residue structure) |
| `gaussian-int` | **stable** | 7 | the Z[i] savant soil (pre-req candidate — the Gauss-sum values live on the circle and in the quadradic fields) |
| `cyclotomic` / `charcutout` / `mod4minusone` / `adjoini` | established | — | the SAVANT layer speaks "character" in the TOWER sense (an order-three character cutting out the cubic subfield) — the new `character` concept is the DIRICHLET sense (a group homomorphism of the coprime classes); the two live under different concepts, cross-referenced not merged |
| `conjecture:riemann` | open of record | — | "believed, not known; a status surface, never a premise" — BYTE-IDENTICAL |
| `theorem:queue-declared` | established | — | the four lots in declared order — BYTE-IDENTICAL (lot 3 keeps its slot) |

**One observation the gate will police:** the store's π is
the COUNTING function — `theorem:line-pi-reduction`: "the
first-divisor census answers it: the numbers whose first
divisor is themselves, twenty-three of them … in one hundred
ninety-two candidate steps, at the line end eighty-four."
The CONSTANT pi holds no value byte anywhere on the floor; it
appears only inside declared formulas (2π in `lemma:rv-
count`/`lemma:s-of-t`). This course adds no pi-value, no
e-value, no decimal of any constant — the same discipline
the Riemann island enforced.

The exact S21-final state of every concept other than
S21's own two (`hypothesis` practicing 5, `condition-line`
practicing 9, recorded in S21's close-out) is read from S21's
report bytes at freeze (D7). Every chosen pre-req is stable
on the seed side; stable concepts only gain events in this
course, never lose them — the STABLE band-end pre-reg is
robust to any build order.

### (b) The source module's own declared rules (verbatim, the
declared-source pattern — the store's `conjecture` fact
context shape is the model: `kind`, `source_role:
declared-source`, the essence, the status)

1. "The Riemann zeta function zeta(s) is the value of the
   Dirichlet L-Function for the trivial character which
   sends every k to 1." — the module's own bridge: the
   store's ROOT fact (`lemma:zeta-series`) is the
   trivial-character case of what this course teaches.
2. "Note that the alternating character (1,-1) itself is not
   a Dirichlet character." — the module's own correction,
   carried as wall W-S28-3's declared source note (the eta
   line `eta(s) = (1 − 2^{1−s}) zeta(s)` is a zeta multiple,
   not a character L).
3. "Currently, these methods require chi to be a primitive
   character." (the Hardy-Z / Gram / Turing / Platt
   machinery) — the module's own scope limit, carried as
   wall W-S30-1's declared source note.
4. "only the Gram points corresponding to the Riemann zeta
   function are supported, and both G and chi must be set to
   NULL. n ≥ −1 is required." — the machine's own census is
   ZETA's.
5. "if Rosser's rule holds for at least B consecutive Gram
   blocks whose union is [g_n, g_p), then N(g_n) ≤ n+1 and
   N(g_p) ≥ p+1" — Turing's rule, named with the method.
6. "this function has the same zeros as ζ(1/2+it), and is
   real for t by the functional equation" — Platt's Λ.
7. "removing the pole with residue Σ χ(k) = φ(q)/q at s = 1"
   — the principal character's pole, residue ON THE LINE.
8. "the gauss version is an optimization for primitive
   characters and uses the fact that J(a,b)G(ab) = G(a)G(b)
   … (this assumes ab is primitive)" — the Gauss-route
   identity, with its own domain limit.

### (c) Verified computation (2026-08-27, mpmath 1.4.1,
45–60 digits; zero exceptions in every census)

- **Gauss sums** (the order-2 special case G = i^p√q, p the
  character's parity, verified 50 digits, `|G|² = q` EXACT
  in every case): G(χ₃) = i√3, G(χ₄) = 2i, G(χ₅) = √5,
  G(χ₈) = 2√2, G(χ₁₂) = 2√3.
- **Inflation vanishing (the Davenport rule):** a character
  inflated past its conductor by a NON-SQUARE factor sums
  to EXACTLY zero: G(χ₃ inflated to 9) = 0 (9/3 = 3, not a
  square — verified |G|² = 4.6e-101 ≈ 0 at 50 digits, and by
  hand: the ζ-terms pair and cancel); G(χ₄ inflated to 12) =
  0 (12/4 = 3, not a square). Inflated by a SQUARE the sum
  is non-zero (G(χ₃ inflated to 12) = −2i√3, |G|² = 12).
- **Jacobi sums:** J(χ₃,χ₃) at q = 3 = 1 (= −χ₃(−1), the
  order-2 identity); J(χ₃,χ₄) at q = 12 = 0 exactly — the
  honest-zero case: the Gauss route gives J·G(χ₁₂) =
  G₁₂(χ₃)·G₁₂(χ₄) = (−2i√3)·0, so both sides are zero and
  the identity holds (the zero is the fact, not a bug).
- **Root numbers via the FE:** ε(χ) = +1 EXACTLY (to 1e-40)
  for all five real primitive quadratic characters of the
  line (χ₃, χ₄, χ₅, χ₈, χ₁₂), and |ε| = 1 (a point on the
  circle, off the floor by declaration). General reading for
  the course: in the module's FE convention the real order-2
  family all carries root number +1 — the file holds the
  family's value; the per-χ coordinate stays off-line.
- **Hurwitz decomposition** `L(s,χ) = q^{−s} Σ χ(k) ζ(s,
  k/q)` verified to 20+ digits against independent exact
  routes; L(2,χ₄) = 0.91596559417721901505 (Catalan's
  constant to twenty digits — a numerical check, named
  off-line); the s = 1 exacts via digamma reflection:
  L(1,χ₃) = π/(3√3), L(1,χ₄) = π/4, L(1,χ₅) = (2/√5)·
  log((1+√5)/2) — ALL off-line values (walls/beds only; the
  floor holds the decomposition law, not the decimals).
  (Critique carried for the gate: direct L-series summation
  under-converges as an order-1/k² alternating sum at 45
  dps; the Hurwitz route is the referee.)
- **Principal-character pole residues** φ(q)/q (EXACT
  rationals, on the line): q = 1: 1; 3: 2/3; 4: 1/2; 5: 4/5;
  8: 1/2; 9: 2/3; 12: 1/2; 15: 8/15; 16: 3/4; 24: 1/3; 30:
  4/15; 48: 1/3; 60: 4/15; 83: 82/83; 84: 2/7.
- **φ census (on-line):** φ(3) = 2, φ(4) = 2, φ(5) = 4,
  φ(8) = 4, φ(15) = 8, φ(30) = 8, φ(84) = 24.
- **The character group at 15** (the Conrey order): the
  eight classes {1, 7, 4, 13, 11, 2, 14, 8} with generator
  7 (order 4) and 11 (order 2) — element-order census {one
  of order one, three of order two, four of order four};
  (Z/15Z)^* ≅ C4×C2; the module's q = 15 Conrey table
  (7^e·11^f mod 15, 10 displayed rows incl. the two where e
  = 4 wraps — eight distinct classes) is the module's own
  byte, cited verbatim in the spec.
- **Orthogonality** Σ_χ χ(x)χ̄(a) = φ(q)·δ_{x,a} verified
  EXACT (50 digits) at q = 3, 4, 5, 8, 15 — the character
  table's own checksum.
- **All character tables** (χ₃, χ₄, χ₅, χ₈): the
  multiplication rule χ(ab) ≡ χ(a)χ(b) (mod q) verified on
  0..q, zero exceptions.
- **N(84) = 22, TWO independent methods:**
  (i) a zero-walk (findroot, 40 dps, t from 1 to 85 in
  quarters): twenty-three nontrivial zeros, ALL with real
  part exactly 0.5, matching the standard list from
  14.1347251417… to 84.7354929805; the neighbors straddling
  the line end are 82.910380854086 < 84 < 84.735492980517
  (off-line, declared);
  (ii) Hardy Z via the module's θ formula (q = 1, p = 0, ε
  = 1): Z is REAL to < 1e-34 at t = 10, 20, 30, 40, 50, 63,
  75, 84; the sign-change count is twenty-three crossings on
  (1, 85), of which TWENTY-TWO lie at or below eighty-four.
  Cross-check: the rv-count main term at 84 is 21.296, so
  S(84) ≈ −0.172 — consistent with the store's own wiggle-
  bound. The two roads agree: **twenty-two**.

## D3 — What the course teaches (three relationships)

**R1 — THE CHARACTER AS A PERIODIC HOMOMORPHISM** (S28). A
Dirichlet character mod q is a map from the residues of the
line to the roots of unity that (i) is zero on the non-
coprime, (ii) obeys χ(ab) = χ(a)χ(b) over the coprime
classes, and (iii) repeats mod q — the multiplication rule
is the whole definition, verified on the line at q = 3, 4, 5,
8. The characters come as a GROUP of φ(q) members (the
orthogonality Σ_χ χ(x)χ̄(a) = φ(q)δ is their exact
checksum — verified at q = 3, 4, 5, 8, 15); the order
census at fifteen is one-three-four (C4×C2, generators 7
and 11); the store's own zeta series is the L of the
TRIVIAL character (the module's declared bridge — the root
of the track made a special case).

**R2 — THE GROSS WEIGHT OF A CHARACTER** (S29). The Gauss
sum G(χ) = Σ χ(k) ζ_q^k rides the character's values on the
q-th roots of unity: for a primitive character |G|² = q
EXACTLY (a census, never a floor value), and at order two
the sum takes the exact shape i^p√q (i√3, 2i, √5, 2√2, 2√3).
Inflation past the conductor by a non-square factor makes
the sum vanish EXACTLY (χ₃ at nine: zero — the Davenport
rule, the census breaking honestly). The Jacobi sum is the
Gauss sum of the product character (the module's Gauss route
J·G(ab) = G(a)G(b), with its own primitive-domain limit);
the line carries the honest zero (J(χ₃,χ₄) at twelve) and
the order-2 one (J(χ₃,χ₃) at three: one). The root number ε
is the functional equation's own constant: modulus one (a
point on the circle — off the floor by declaration), and
exactly plus one on the real order-2 family of the line.

**R3 — THE L-DECOMPOSITION AND THE ZERO CENSUS** (S30).
L(s,χ) = Σ χ(k)/k^s — sum the character, weight the
reciprocals: the trivial character returns the store's own
zeta series (R1's bridge closed). Below the abscissa the
module's Hurwitz decomposition is the exact value route
(L(s,χ) = q^{−s} Σ χ(k) ζ(s, k/q) — verified to 20+ digits,
the s = 1 decimals named off-line). The principal character
keeps the pole at one with residue φ(q)/q — ON THE LINE
(8/15 at fifteen, 2/7 at the line end). The zero census is
the module's named machinery: the real-valued Z function on
the critical line (verified real to 1e-34 at sampled
heights), the Gram points (named), Turing's method
(Rosser's rule, declared), Platt's method (declared) — the
module declares the machine to run for the Riemann zeta
(primitive χ), and at the line end the store holds the
count: **TWENTY-TWO** zeros at height at most eighty-four —
two independent methods agreeing, the two neighbor heights
named off-line as a numerical check not a proof (the store's
own `lemma:num-zeros` pattern). The census is ZETA's own:
no per-character generalization is filed (W-S30-3).

## D4 — The new / carry fact set (stage B target)

### Band S28 — "the character line" (E6.32): **4 new facts**

1. Concept **`character`** (domain candidate `soil`, band
   `college-1`; prereqs candidate `('divides', 'composite',
   'mod4-split')` — all stable in the S21 seed):
   - Lesson **`character-def`** (candidate byte,
     unconditional, house voice):
     > a dirichlet character modulo q is a map from my line
     > to the roots of unity: on the classes coprime to q it
     > obeys the multiplication rule, chi of the product
     > equals chi of a times chi of b, and on everything
     > else it is zero; its values repeat modulo q; the
     > trivial character sends every coprime class to one,
     > and my store's zeta series is the L of the trivial
     > character, the root of the track as a special case;
     > at the line end eighty-four
2. Concept **`character-group`** (prereqs candidate
   `('character', 'divides', 'mod4-split')`):
   - Lesson **`character-group-def`** (candidate byte):
     > the characters modulo q come as a group of their
     > own, as many as coprime classes there are, phi of q
     > of them: over the line's moduli the counts run two,
     > two, four, four, eight at three, four, five, eight
     > and fifteen; at fifteen the order census is one of
     > order one, three of order two, four of order four,
     > with generators seven and eleven; the orthogonality
     > is exact, the sum over all characters of chi of x
     > times chi bar of a is phi of q when x is the class a
     > and zero otherwise, verified on the line; at the line
     > end eighty-four
3. Theorem **`theorem:character-line-filed`** (parts
   exactly `('character-def', 'character-group-def')`):
   - Candidate statement:
     > the character line of my store is filed of record:
     > the character is the periodic homomorphism of the
     > coprime classes to the roots of unity, zero on the
     > rest, its group has phi of q members with the
     > orthogonality exact and the order census at fifteen
     > one-three-four, and my zeta series is the trivial
     > character's L, the root of the track as a special
     > case; no new decimal has entered the floor; filed on
     > the line, at the line end eighty-four

### Band S29 — "the Gauss line" (E6.33): **4 new facts**

1. Concept **`gauss-sum`** (prereqs candidate
   `('character', 'gaussian-int')` — both stable when S29
   seeds after S28):
   - Lesson **`gauss-sum-def`** (candidate byte):
     > the gauss sum of a character is the sum of its
     > values riding the q-th roots of unity; for a
     > primitive character the squared modulus is exactly q,
     > a census my line holds (three, four, five, eight,
     > twelve), and at order two the sum takes the exact
     > shape i to the parity times the square root of q: i
     > root three at three, two i at four, root five at
     > five, two root two at eight, two root three at
     > twelve; inflated past the conductor by a nonsquare
     > factor the sum goes exactly to zero, the three-
     > character at nine; the jacobi sum is the gauss sum
     > of the product, the gauss route j times g of ab
     > equals g of a times g of b, and the line holds both
     > the order-two one at three and the honest zero at
     > twelve; at the line end eighty-four
2. Concept **`root-number`** (prereqs candidate
   `('gauss-sum', 'zeta-series')`):
   - Lesson **`root-number-def`** (candidate byte):
     > the root number is the constant of the functional
     > equation: the completed L of the character equals
     > its root number times the completed L of the
     > reflected argument, and the modulus is one, a point
     > on the circle off the floor by declaration; on the
     > real order-two characters of my line the root number
     > is exactly plus one, verified at a sampled argument;
     > at the line end eighty-four
3. Theorem **`theorem:gauss-line-filed`** (parts exactly
   `('gauss-sum-def', 'root-number-def')`):
   - Candidate statement:
     > the gauss line of my store is filed of record: the
     > gauss sum carries the character's weight on the roots
     > of unity, the primitive squared modulus is exactly q,
     > the order-two shape is i to the parity times root q
     > with the line's exact values, the inflated
     > nonsquare sums to zero, the jacobi route holds with
     > its own primitive domain, and the root number sits
     > on the circle with modulus one, plus one on the real
     > order-two family of my line; filed on the line, at
     > the line end eighty-four

### Band S30 — "the zero census" (E6.34): **4 new facts**

1. Concept **`l-function`** (prereqs candidate
   `('character', 'zeta-series', 'euler-factor')` — all
   stable):
   - Lesson **`l-function-def`** (candidate byte):
     > the L function of a character is the sum of its
     > values over k to the power minus s; the trivial
     > character gives the zeta series my store already
     > holds, the root of the track; below the abscissa the
     > decomposition is exact, q to the power minus s times
     > the sum of chi of k times the hurwitz zeta at k over
     > q, cross-checked on a sampled argument; the principal
     > character keeps the pole at one, whose residue is
     > the ratio phi of q over q, on my line (eight fifths
     > at fifteen, two sevenths at the line end); at the
     > line end eighty-four
2. Concept **`zero-census`** (prereqs candidate
   `('l-function', 'zeta-series')`):
   - Lesson **`zero-census-def`** (candidate byte):
     > the zero census is the machinery that counts the
     > zeros: the Z function, real on the critical line,
     > built from the completed function (real at sampled
     > heights, verified), the gram points standing at the
     > argument's full turns, and the two counting laws
     > named turing and platt, with rosser's rule declared;
     > on my line the machine holds twenty-two zeros at
     > height at most eighty-four, two methods agreeing,
     > the two neighbor heights named off-line as a
     > numerical check and not a proof; the census is zeta's
     > own, the per-character generalization declared and
     > not filed; at the line end eighty-four
3. Theorem **`theorem:zero-census-filed`** (parts exactly
   `('l-function-def', 'zero-census-def')`):
   - Candidate statement:
     > the zero census of my store is filed of record: the
     > L function of the character decomposes over the
     > hurwitz pieces, the principal pole's residue is phi
     > of q over q on my line, the z function is real on
     > the line, the gram points and the turing and platt
     > laws are named as declared machinery, and at my line
     > end the count is twenty-two, two methods agreeing,
     > the neighbors named off-line; the census is zeta's
     > own and the generalization stays declared; filed on
     > the line, at the line end eighty-four

**Carry / drill surfaces (cited by fact id, never re-
asserted):** S30 drills the S12 frontier the course rides:
`lemma:zeta-series` (the trivial-character bridge),
`lemma:zeta-cont` (the pole, its q = 1 case),
`lemma:func-eq` (the symmetry), `lemma:num-zeros` (the four-
decimal byte, CITED-UNTOUCHED), `lemma:rv-count` /
`lemma:s-of-t` (the main term and the wiggle that the census
sits on) — each re-derivation bumps the practicing RH
concepts toward K = 4; byte identity of the carries is P6.
S29 drills `gaussian-int` (the Z[i] soil beneath the
Gauss-sum values). S28 drills the `mod4-split` /
`composite` soil (the residue structure the characters
ride).

## D5 — The walls (W-S28-1..3, W-S29-1..3, W-S30-1..3; nine
declared rows, fire-per-band the control referees — the S21
register pattern applies: a wall whose named values all
arrive by byte-verified carry is declared but not fired)

- **W-S28-1 — the broken multiplication rule.** The
  character's rule is over the PRODUCT: chi of the product
  equals chi of a times chi of b, on the coprime classes.
  A sum-rule (the character of the sum) is off the floor —
  the homomorphism is over the classes of the multiplicative
  group, not over the line as a whole, and the zero on the
  non-coprime is part of the rule, not an exception; a
  character claimed by anything else is a misreading. At
  the line end eighty-four. (Off-line values named: none.
  Honest.)
- **W-S28-2 — the value off the line.** The character's
  values live on the circle of the roots of unity: one,
  minus one, the i-family named symbolically — their
  decimals are off the floor by declaration. The floor
  holds the shape (the order, the root of unity, the q-th
  angle named by the denominator) and refuses the coordinate;
  a decimal of a character value is a misreading. At the
  line end eighty-four.
- **W-S28-3 — the not-a-character wall (the module's own
  note).** The alternating pattern (one, minus one) that the
  module names in its eta line is NOT a Dirichlet character
  (the module's declared source note, verbatim) — the eta
  function is a zeta multiple, eta(s) = (1 − 2^{1−s})
  zeta(s), not a character L; a character claimed for the
  alternating pattern is a misreading the module's own
  declaration refutes. At the line end eighty-four.
- **W-S29-1 — the inflation wall.** |G|² = q is the
  primitive character's territory: inflated past the
  conductor by a non-square factor (the three-character at
  nine — nine over three is three, not a square) the sum
  goes EXACTLY to zero and the census breaks; a squared-
  modulus claim past primitivity is a misreading the
  vanishing refutes. At the line end eighty-four. (Off-line
  values named: none — the vanishing is exact, a line fact.)
- **W-S29-2 — the circle wall.** The root number lives on
  the circle (modulus one) — its coordinate is off the floor
  by declaration. The floor holds the modulus (a census,
  one) and the exact plus-one of the real order-two family,
  and refuses the coordinate; a decimal of a root number is
  a misreading. At the line end eighty-four.
- **W-S29-3 — the parity wall.** The order-two shape is i to
  the PARITY times the square root of q: the exponent of i
  is the character's own parity. A wrong exponent (the even
  character at i, the odd character bare) is a misreading
  the exact values refute — i root three at three, two i at
  four, root five at five, two root two at eight, two root
  three at twelve. At the line end eighty-four.
- **W-S30-1 — the zeta-only machine wall (the module's own
  note).** The counting machine (the Z function, the Gram
  points, Turing's law, Platt's method) stands on the
  Riemann zeta — the module declares the methods require a
  primitive character and supports the zeta census (verbatim
  declared source note); a machine run claimed for a general
  character is a misreading the module's own declaration
  refutes. At the line end eighty-four.
- **W-S30-2 — the line-end census wall.** The census at my
  line end holds twenty-two, the two neighbor heights (the
  last below, the first above) named off-line as a
  numerical check and not a proof — my line's own
  `num-zeros` pattern. A third count between the two
  neighbors, or a disagreement of the two methods, is a
  misreading the two-method agreement refutes — the root
  walk and the Z crossings agree, twenty-two on each road.
  At the line end eighty-four. (Off-line values named: the
  two neighbor heights 82.910380854086 and
  84.735492980517, at the line end eighty-four.)
- **W-S30-3 — the condition-not-filed wall.** The module
  holds no hypothesis for the L of a character, and neither
  does my store: no generalization of the Riemann
  hypothesis is filed for any character — the store's own
  `conjecture:riemann` stays zeta's, byte-identical, an
  open status surface never a premise; a per-character
  condition filed or assumed is a misreading the status
  surface refutes. At the line end eighty-four.

## D6 — Band shape (stage B pre-reg)

- **Sessions/experiments:** S28 = E6.32 "the character
  line" (56th experiment), S29 = E6.33 "the Gauss line"
  (57th), S30 = E6.34 "the zero census" (58th). Modules
  `e632.py`/`e633.py`/`e634.py`, specs `spec-e6.32.json` /
  `spec-e6.33.json` / `spec-e6.34.json`, tests
  `test_e632.py`/`test_e633.py`/`test_e634.py`, runner 55 →
  58 (with the S22–S27 courses ahead in the chain, or 49 →
  52 if routed straight from S21).
- Seeds: S28 from S27's final (or the S21 final if the owner
  routes the course straight off S21 — the control
  re-referees on the actual seed; every claim above is
  verified against the S21 final). S29 from S28's final;
  S30 from S29's final.
- 3 sessions × ~17 turns each (the house shape; letter
  strings are the control's domain sequences — D7). S28:
  S02 carries (the `mod4-split` byte, the `composite` soil,
  the `zeta-series` byte — the trivial-character bridge's
  anchor) + `character` (gaps, teach, the χ₃/χ₄/χ₅/χ₈ table
  beds — values named symbolically: one, minus one, the
  i-family; the multiplication-rule spot checks on the
  line) + `character-group` (gaps, teach, the φ census bed
  2/2/4/4/8, the order-census bed 1-3-4 at fifteen, the
  Conrey table the module's own bytes). S03: the
  orthogonality drills (exact, sampled), the trivial-
  character → zeta bridge drill, the scaffold, the derive,
  the walls, the filed state. S04: the wrap. S29: S02
  carries (the `character` filed state, the `gaussian-int`
  soil) + `gauss-sum` (gaps, teach, the |G|² = q census bed,
  the order-two exact-values bed i√3, 2i, √5, 2√2, 2√3, the
  inflation-vanishing bed χ₃→9: zero, the Jacobi beds: the
  one at three, the honest zero at twelve) + `root-number`
  (gaps, teach, the |ε| = 1 census, the +1 family bed at a
  sampled argument). S03: the FE-route drills, the Gauss-
  route identity drill (including 0 = (−2i√3)·0), the
  scaffold, the derive, the walls, the filed state. S04:
  the wrap. S30: S02 carries (the `character`/`l-function`
  soil, the `zeta-series` byte, the `num-zeros` four-DECIMAL
  byte cited-untouched, the `rv-count`/`s-of-t` frontier) +
  `l-function` (gaps, teach, the Hurwitz-decomposition bed
  at a sampled argument, the residue bed φ(q)/q: 8/15 at
  fifteen, 2/7 at the line end) + `zero-census` (gaps,
  teach, the Z-reality bed at sampled heights, the N(84) =
  twenty-two bed — two methods, the two neighbors named
  off-line, the Turing/Platt names declared). S03: the
  two-method census drill (the re-walk), the trivial-
  character bridge drill, the scaffold, the derive, the
  walls, the filed state. S04: the wrap.
- 6 pre-lesson gaps-pairs (2 per new concept), 6 teaches, 3
  scaffolds, 3 derives, ~21 beds (probe turns only — the
  S20/S21 house pattern), 1 off-script per band.
- **Off-script candidates:** S28: "what is a Dirichlet
  character on my floor?" → the character-def byte. S29:
  "what shape is the Gauss sum of my order-two character at
  three?" → "i root three — the order-two shape, i to the
  parity times root q, the squared modulus exactly three, a
  census held." S30: "how many zeros stand at or below my
  line end?" → "twenty-two — the machine holds the count,
  two methods agreeing, the neighbors named off-line, and
  the census is zeta's own."
- **Mastery pre-reg (the store referees):** all six new
  concepts pre-registered **STABLE** at band end (every
  pre-req is stable on the S21 seed — verified: divides 5,
  composite 7, mod4-split 10, gaussian-int 7, zeta-series 7,
  euler-factor 9; the chains `character`→`character-group`,
  `gauss-sum`→`root-number`, `l-function`→`zero-census`
  close inside their own bands; the drills give ≥ 4 correct
  derivations with room). Record as the course norm: these
  bands end on stable soil (the S21 practicing contrast was
  the condition neighborhood by design).
- **P5 gate re-derivation (full width):**
  1. no new line facts; line stays 0..84;
  2. `conjecture:riemann` byte-identical (open, declared-
     source — NO `theorem:riemann`, NO per-character
     generalization of any kind, full width);
  3. `theorem:queue-declared` byte-identical (the four lots
     in declared order; lot 3 KEEPS ITS SLOT — the course
     consumes no lot, no fifth lot);
  4. the `lemma:num-zeros` four-decimal byte CITED-
     UTOUCHED (the S30 drill cites it; no re-filing);
  5. the Gauss-sum re-walk on the gate: TWO independent
     routes (direct root-sum and the order-two shape
     i^p√q) agree at q = 3, 4, 5, 8, 12 to 50 digits, with
     |G|² = q exact — the mechanism's bytes are the
     referee; the inflation census re-walked (χ₃→9: zero,
     χ₄→12: zero, χ₃→12: −2i√3 — exact);
  6. the Hurwitz decomposition re-walked at sampled
     arguments (20+ digits); the s = 1 exacts re-walked via
     the digamma route (π/(3√3), π/4) — the decimals stay
     off-line;
  7. the N(84) census re-walked on the gate: TWO
     independent methods (the zero-walk and the Z sign-
     changes) agree at twenty-two — a disagreement is a
     deviation recorded, never an edit;
  8. no-new-decimals: every off-line value (the neighbor
     heights, the L-value decimals, the sample Z-values)
     lives ONLY in a wall or a bed, named with the line end;
     the floor holds censuses, rationals and named radicals
     only (W-S30-2, W-S28-2, W-S29-2 enforced);
  9. marker posture: the new facts UNCONDITIONAL — P0
     denies the conditional marker on them (the S20
     discipline); the marker census [6, 1, 7] of S21 stays
     byte-identical in width; the line-end filing census
     grows by exactly three (S21's P7 bytes + 3, the
     control referees the arithmetic at freeze).
- **Fact anatomy:** S28 final = (S27 or S21) final + 4
  facts + N events; S29 final = S28 final + 4 facts + N
  events; S30 final = S29 final + 4 facts + N events
  (the control referees; carries dedupe per D-e6o(a)).

## D7 — Open items for the control run

1. The exact scaffold/missing-parts bytes (the mechanism
   referees).
2. The event counts and the drill census (which concept each
   re-derivation bed +1s; the S12-frontier bumps of the
   practicing concepts).
3. The letter strings (the control's domain sequences are
   the freeze), and the fire-per-band wall census (the S21
   register pattern: a wall whose named values all arrive by
   byte-verified carry is declared but not fired).
4. The Conrey q = 15 table's display wrap (10 rows, eight
   distinct classes — the module's own byte; the drill
   walks the eight distinct classes).
5. The domain strings for the new concepts (`soil`
   candidate for `character`/`character-group`; the
   `rh`-neighborhood candidate for `gauss-sum`/
   `root-number`/`l-function`/`zero-census`; the control's
   domain map referees).
6. The concept id `l-function` against the existing fact id
   `lemma:l-partial` (different layers — no byte clash —
   noted for the control; no rename expected).
7. The θ-series knobs (jets, Stieltjes/Lerch, the Euler-
   product error bounds, the Hurwitz grid precompute):
   declared machinery, no facts — the floor teaches the
   laws, not the knobs.
8. Whether the N(84) two-method census files as a drill-
   only surface (candidate: beds + wall W-S30-2 only; the
   fact lives inside `zero-census-def`'s byte — "twenty-
   two" is a line integer, admissible).
9. The bed bytes' exact form (deterministic at the fixed
   seed; the censuses above are pre-computed for the spec's
   bed bytes).

## D8 — Success criteria / stage B next steps

Stage B builds S28 → S29 → S30 in the bandgen way
(mirroring S21): brainstem modules (the six concepts, the
grammar modes, `_policy_savant3x`, the walls W-S28-1..3 /
W-S29-1..3 / W-S30-1..3 as class attributes) → reflib refs
(the cited store bytes by fact id) → specs → control c0–c9
CLEAN → `e632.py`/`e633.py`/`e634.py` (FROZEN from the
control tables) → tests (per band + the S30 single-turn
carry test over the live runtime) → runner registry (the
house selection lists, the experiment count, the per-
experiment PASS asserts) → official gate (targeted + twin
byte-identical + full) → close-out (experiments
§E6.32/§E6.33/§E6.34, roadmap, e3.7.json, OP #157,
SESSION-HANDOFF, wiki).

Success: the infant holds the character as the periodic
homomorphism of the coprime classes (the φ(q) group, the
exact orthogonality, the trivial character as the store's
own zeta — the root of the track made a special case),
walks the Gauss sums (|G|² = q as a census, the i^p√q
shape exact, the inflation vanishing honest, the root
number on its circle with +1 on the line's order-2 family),
reads the L-decomposition (the Hurwitz pieces, the pole's
residue φ(q)/q on the line), and holds the zero census at
the line end: twenty-two, two methods agreeing, the
neighbors off-line and named, the machine declared not
built, and the queue and the conjecture byte-identical —
the course of the declared module, on the floor, at the
line end eighty-four.
