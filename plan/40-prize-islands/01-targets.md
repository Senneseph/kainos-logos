# 01 — The prize targets (research survey)

Surveyed 2026-08-24 against: the Clay Mathematics Institute problem
pages, the American Mathematical Society Beal Prize page and the
original 1997 *Notices* announcement (via the Mauldin statement
page), and the **Prize Problem Ledger** (prizeproblems.org —
177 permanently numbered targets, "PPL nnn" citations). Threshold:
**prize ≥ $1,000,000**, problem **outstanding** (no accepted
solution).

## The complete ≥ $1M list (nine entries)

### 1. Riemann hypothesis — Clay Millennium (PPL 056) — $1,000,000

**Statement.** Every nontrivial zero of the Riemann zeta function has
real part exactly 1/2.

**Status.** Open (1859; 167 years). The first 10^13+ zeros verified
numerically on the critical line (trillionth zero, 2000, Gourdon);
no zero off the line in any known computation.

**The frontier our store holds** (S8–S13, built and official): the
zeta family and its three splits (S13), the line partials, the
zero-density territory, the erdos/kest/queue seams, and the store's
own articulated `rh-reach` + named missing ingredient. Island map:
`03-island-riemann.md`.

### 2. Birch–Swinnerton-Dyer — Clay Millennium (PPL 100) — $1,000,000

**Statement (standard form).** For an elliptic curve E over the
rationals, the order of vanishing of its L-function L(E,s) at s = 1
(the **analytic rank**) equals the rank of the group of rational
points E(Q) modulo torsion (the **algebraic rank**).

The prize-grade form is the full BSD conjecture: the rank part plus
the **leading-coefficient formula** (BSD 1.2) expressing L(E,1) (or
its first nonzero derivative) in terms of the Tate–Shafarevich
group order, the Tamagawa numbers, the regulator, the torsion, and
the real period. A solution must establish the formula, not just
the rank equality, for every E/Q.

**Status.** Open (conjecture 1965, Birch's computation-driven
origin; generalized to the L-function form with Swinnerton-Dyer).
Known territory (verified 2026-08-24):

- **Order 0:** unconditional (post-modularity: Gross–Zagier formula
  + Kolyvagin's Euler systems, 1990).
- **Order 1:** for modular E/Q (Kolyvagin 1990; modularity of all
  elliptic curves over Q: Wiles 1995, completed by Taylor–Wiles,
  Ribet, Breuil–Conrad–Diamond–Taylor 2001).
- **Order 2:** the "1 and 2" direction of the Breuil–Conrad–Diamond–
  Taylor 2001 work (under its stated hypotheses, e.g. ordinary
  reduction at the auxiliary prime).
- **Parity:** the parity conjecture (algebraic rank ≡ analytic rank
  mod 2) is a theorem for E/Q (Kolyvagin 2004, Logachev 2004, via
  modularity of the adjoint representation + the Kolyvagin
  system); the generalization to abelian varieties over number
  fields remains open.
- **Verification:** BSD (rank part) verified for the large database
  of low-conductor curves (LMFDB; the classical computations down
  to 1965); recent (2026) Burungale–Skinner–Tian–Wan work proves
  strong BSD for infinite families of quadratic twists of
  suitable curves; the rank ≤ 1, conductor-bounded verifications are
  the standing computational baseline.
- **Missing ingredient (as the store would name it):** the
  non-archimedean control — the order of the Tate–Shafarevich
  group and the Selmer-group machinery beyond the known orders.

Full plan: `04-island-bsd.md`.

### 3. P versus NP — Clay Millennium (PPL 091) — $1,000,000

**Statement (per the Clay problem page, canonical form).** P is the
class of decision problems solvable by a deterministic Turing
machine in polynomial time; NP is the class whose "yes" instances
have polynomial-size certificates verifiable in polynomial time.
Prove or disprove **P = NP** (and, for the disproof case: show a
problem in NP that requires more than polynomial time in the
appropriate non-uniform sense, with the explicit requirements of
the CMI page — the proof must establish a superpolynomial lower
bound for a specific NP problem).

**Status.** Open (1971; 55 years).

**The frontier (the barriers as our store would hold them):**

- **Relativization barrier** (Baker–Gill–Solovay 1975): oracle
  relativizations cannot settle P vs NP (there are oracles relative
  to which P = NP and oracles relative to which P ≠ NP).
- **Natural proofs barrier** (Razborov–Rudich 1997): under a
  standard pseudorandomness assumption, no "natural" proof can give
  the circuit lower bounds separating P from NP.
- **Algebrization barrier** (Aaronson–Wigderson 2009): the
  algebrization technique in relativization cannot either; new
  ITCS-2026 algebrization results (ECCC TR25-184 line) keep
  strengthening the boundary.
- **Existing lower bounds:** parity requires exponential size in
  constant-depth (AC⁰) circuits (Razborov–Smolensky); the
  "magnification" program links slightly-superlinear formula lower
  bounds to superpolynomial formula lower bounds for NP — real
  progress, short of the prize.
- **Missing ingredient:** a technique outside relativization,
  algebrization, and natural proofs — nobody knows what shape that
  would take.

Full plan: `05-island-p-np.md`.

### 4. Beal conjecture — AMS/Beal Prize (PPL 126) — $1,000,000

**Statement (verbatim, original 1997 *Notices* announcement via the
AMS/Mauldin statement page).**

> If A^x + B^y = C^z, where A, B, C, x, y and z are positive
> integers and x, y and z are all greater than 2, then A, B and C
> must have a common prime factor.

**Status.** Open (conjecture 1992; prize raised to $1M in 2013,
held by the AMS under a 2013 MOU). Prize for a proof **or a
counterexample**, published in a refereed respected journal.

**The frontier:**

- **Fermat (Wiles–Taylor, 1995):** the equal-exponent case is
  closed — for x = y = z there are no solutions at all with A, B, C
  pairwise coprime (every solution has a common factor). The
  (3,3,3) triple is the Euclidean boundary case (1/3+1/3+1/3 = 1).
- **Darmon–Granville (1994):** A^x + B^y = C^z with x, y, z ≥ 3 and
  1/x + 1/y + 1/z < 1 has only **finitely many** primitive (pairwise
  coprime A,B,C) solutions — via Faltings, so *ineffective*
  (finiteness without an algorithm to list them). This is exactly
  the territory of the Beal conjecture, which asserts the list is
  empty.
- **Darmon–Merel (1997):** the unexponented-C case
  (A^x + B^y = C) has only trivial solutions.
- **Distinct-exponent partials:** various (x,y,z)-triple cases via
  the modular method (Ribet-type, Darmon–Lafont–Merel–Murty and
  successors); the hyperbolic triples with small exponents are
  largely covered.
- **The standing examples** (why the hypotheses are exactly as
  stated): 3² + 6² = 3³ (a common factor 3 — no contradiction);
  7³ + 13² = 2⁹ (no common factor — but the exponent 2 is not
  > 2, so the conjecture does not claim).
- **Missing ingredient:** a uniform control of the primitive
  solutions for arbitrary triples of distinct exponents ≥ 3 — the
  modularity machinery reaches the equal and two-exponent-equal
  cases, not the fully-distinct hyperbolic case.

Full plan: `06-island-beal.md`.

### 5. Navier–Stokes existence and smoothness — Clay (PPL 011) — $1,000,000

**Statement (canonical form).** For the incompressible three-
dimensional Navier–Stokes equations on ℝ³ × [0,∞) and on the three-
torus, given smooth initial data, prove that smooth (infinite-
differentiability) global solutions exist and remain smooth for all
time — or exhibit a finite-time breakdown (a singularity forming).

**Status/frontier.** Leray weak existence (1934); partial regularity
(Caffarelli–Kohn–Nirenberg 1982: the singular set has Hausdorff
dimension ≤ 1 in the parabolic measure); the 1- and 2-dimensional
worlds are fully solved. **OUT OF SCOPE** (see `02-scope.md`): the
store's analysis is exact-finite; the NS problem is continuous
functional analysis (limits of solution families), a register the
store does not hold.

### 6. Yang–Mills existence and mass gap — Clay (PPL 069) — $1,000,000

**Statement (canonical form).** For every compact simple gauge
group, construct a nontrivial quantum Yang–Mills theory on
(continuum) four-dimensional space satisfying the Wightman axioms
after Wick rotation, and show that the theory has a positive mass
gap Δ > 0 (the lightest particle's mass is bounded below by Δ, and
Δ is positive).

**Status/frontier.** Classical gauge theory is deep (Donaldson);
constructive QFT exists for 2D (and some 3D) models; the 4D
non-abelian case is beyond existing axiomatic control. **OUT OF
SCOPE:** constructive quantum field theory is a continuous
analysis register the store does not hold.

### 7. Hodge conjecture — Clay (PPL 110) — $1,000,000

**Statement (canonical form).** On a smooth projective complex
algebraic variety, every rational Hodge class is a rational linear
combination of classes of algebraic cycles (with the precise
cohomological grading by (p,q)-types from the statement page).

**Status/frontier.** Known for (1,1) (Lefschetz), for curves, for
complex tori in the classical degrees; open already for abelian
varieties in higher degree. **OUT OF SCOPE:** sheaf cohomology /
algebraic-cycle machinery — the store holds no cohomology register.

### 8. IUT Challenger Prize (PPL 102) — $1,000,000 — open since 2023

**Terms (ledger citation).** Publish the first qualifying paper
that demonstrates an essential and inherent flaw in Shinichi
Mochizuki's inter-universal Teichmüller theory (the context:
resolving the peer-review standoff over the claimed abc proof;
earlier related $1M offer: the Kawakami/Dwango IUT prize).

**Status/frontier.** IUT remains disputed (some working mathematicians
accept aspects; the 2020–2023 community reports split). **OUT OF
SCOPE** (see `02-scope.md`): this is an adversarial *refutation*
meta-problem about a specific 500-page theory, not a constructive
target the store can descend to. The **ABC soil** it shares (via
the Diophantine equations) is already in the Beal and BSD islands.

### Notable below-threshold / non-qualifying entries (recorded for completeness)

- **Certicom ECC challenge (PPL 012):** 163-bit binary-field ECDLP
  — a computational challenge, not open mathematics (and: it is a
  *live target for the CRYPTO-TRACK's R4 band* — the store's small-
  RSA attempt is its analog for the elliptic side).
- **Ethereum Proximity Prize pool shares:** shares of a $1M pool,
  coding challenges — not open math proofs.
- **1-billion-digit prime (PPL 104): $250,000** — below threshold
  (and: a ledger-census shape the S11 machinery could one day
  service).
- **Erdős problem prizes:** largest in the catalog are $1,500–$5,000
  class — below threshold (the store already carries the Erdős
  seam facts from the S11/S12 queues).

## Sources of record

- Clay Millennium problem statements: claymath.org/millennium-problems/
  (per-problem pages; cited in the island plans).
- Beal: AMS Beal Prize rules (ams.org, 2013 MOU) + original statement
  (Mauldin page, mirroring the Dec-1997 *Notices* announcement
  by B. Beal).
- Prize Problem Ledger: prizeproblems.org (PPL 011/056/069/091/100/
  102/110/126 citations).
- Frontiers: Wiles (1995), Gross–Zagier (1986), Kolyvagin (1990),
  Breuil–Conrad–Diamond–Taylor (2001), Kolyvagin (2004) /
  Logachev (2004), Darmon–Granville (1994), Darmon–Merel (1997),
  Baker–Gill–Solovay (1975), Razborov–Rudich (1997),
  Aaronson–Wigderson (2009), ITCS-2026 algebrization line,
  Burungale–Skinner–Tian–Wan (2026 twist families), Leray (1934),
  Caffarelli–Kohn–Nirenberg (1982).
