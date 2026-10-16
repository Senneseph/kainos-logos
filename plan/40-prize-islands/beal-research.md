# Beal island — research record (stage A: the statement, the panel, the census, the ledger)

Island: the Beal conjecture (AMS/Beal Prize, $1,000,000; PPL 126).
Plan: `plan/40-prize-islands/06-island-beal.md`.
Method: every value below is verified by the mechanism's own python
before it is allowed into a band (the store speaks, not the hand).

## D1 — the statement, verbatim, with its record source

**Statement (verbatim, declarative form):**

> "If A^x + B^y = C^z, where A, B, C, x, y, and z are positive
> integers with x, y, z > 2, then A, B, and C have a common prime
> factor."

(Equivalent form, verbatim: "The equation A^x + B^y = C^z has no
solutions in positive integers and pairwise coprime integers A, B,
C if x, y, z > 2.")

Source of record: en.wikipedia.org/wiki/Beal_conjecture (accessed
2026-08-24), consistent with ams.org/math-sciences/beal-conjecture
and the ams.org Beal Prize page. The committed island plan
(`06-island-beal.md`) already carries this statement; this stage
confirms it against the sources (no drift).

**The prize (verbatim, record):** banker Andrew Beal initially
offered a prize of US $5,000 in 1997, raising it to $50,000 over
ten years, and has since raised it to US $1,000,000; the AMS (American
Mathematical Society) holds the $1 million prize in a trust until the
Beal conjecture is solved, supervised by the Beal Prize Committee
(BPC), appointed by the AMS president.

**Structural facts of record (nameable, wall-grade):**

- The equation has infinitely many solutions where the bases share a
  common factor, including the generalizations
  3^(3n) + [2·3^n]^3 = 3^(3n+2) (n ≥ 1);
  [b(a^n−b^n)^k]^n + (a^n−b^n)^(kn+1) = [a(a^n−b^n)^k]^n
  (a > b, b ≥ 1, k ≥ 1, n ≥ 3); and
  [a(a^n+b^n)^k]^n + [b(a^n+b^n)^k]^n = (a^n+b^n)^(kn+1)
  (a, b ≥ 1, k ≥ 1, n ≥ 3); and for each solution there are
  infinitely many with the same exponents and larger non-coprime
  bases (the A_n/B_n/C_n scaling).
- Any counterexample would necessarily involve three terms each of
  which is a 3-powerful number (every prime exponent ≥ 3). The
  smallest two sums of coprime 3-powerful numbers (which are NOT
  Beal solutions — the terms are not single powers):
  271^3 + 2^3·3^5·73^3 = 919^3 = 776,151,559 and
  3^4·29^3·89^3 + 7^3·11^3·167^3 = 2^7·5^4·353^3 = 3,518,958,160,000
  — both far past the line's box (a wall-scale fact, never stored
  as a line value).
- Beal restates Fermat–Catalan: "All Fermat–Catalan conjecture
  solutions will use 2 as an exponent" (FC: finitely many primitive
  solutions with 1/x + 1/y + 1/z < 1; the known primitive solutions
  all carry at least one exponent 2, e.g. 7^3 + 13^2 = 2^9,
  3^5 + 10^2 = 7^3, 2^5 + 7^2 = 3^4, 3^4 + 2^4 = 5^4).
- The closed anchor: the case x = y = z ≥ 3 is Fermat's Last
  Theorem — no solutions (Wiles, 1994; a declared record, not a
  store proof).
- FLT as a special case of Beal: if FLT solutions existed, dividing
  out every common factor would give pairwise-coprime ones.

## D2 — the panel of record (examples the line can hold)

In-box (A, B, C ≤ 84, 3 ≤ x, y, z ≤ 10) — all with their common
factor of record:

| triple (A, B, C, x, y, z) | common prime factor | family |
|---|---|---|
| (7, 7, 14, 3, 4, 3) and (7, 7, 14, 4, 3, 3) | 7 | b(aⁿ−bⁿ)-family, a=2, b=1, n=3 |
| (15, 15, 30, 4, 5, 4) and (15, 15, 30, 5, 4, 4) | 3 (spf of 15) | b(aⁿ−bⁿ)-family, a=2, b=1, n=4 |
| (3, 6, 3, 3, 3, 5) and (6, 3, 3, 3, 3, 5) | 3 | 3^(3n) + (2·3^n)^3 |
| (26, 26, 78, 3, 4, 3) and (26, 26, 78, 4, 3, 3) | 13 | dⁿ + d^(n+1) = (2d)ⁿ, d=26 |
| (28, 84, 28, 3, 3, 4) and (84, 28, 28, 3, 3, 4) | 7 | 28³(1 + 3³) = 28⁴ |
| (17, 34, 17, 4, 4, 5) and (34, 17, 17, 4, 4, 5) | 17 | 17⁴(1 + 4·... ) : 34⁴ + 17⁴ = 17⁵ |
| (31, 31, 62, 5, 6, 5) and (31, 31, 62, 6, 5, 5) | 31 | dⁿ+d^(n+1) = (2d)ⁿ, d=31 |
| (33, 66, 33, 5, 5, 6) and (66, 33, 33, 5, 5, 6) | 3 | 33⁵(1+2⁵) = 33⁵·33 = 33⁶ |
| (19, 38, 57, 4, 3, 3) and (38, 19, 57, 3, 4, 3) | 19 | 19³(19 + 2³) = 19³·27 = 57³ |
| (2, 2, 2, n, n, n+1), n = 3..9 | 2 | the 2^n twin family |

Out of the band's condition (an exponent 2 — the Fermat–Catalan
primitive territory; named on the wall, NOT stored as band content):
7^3 + 13^2 = 2^9, 3^5 + 10^2 = 7^3, 2^5 + 7^2 = 3^4, and the trivial
1^m + 2^3 = 3^2 family (the Fermat–Catalan known-solutions list all
carry at least one exponent 2).

## D3 — the Beal verification census (verified, the island's
signature bed)

**The box:** A, B, C ≤ 84 (the line end), 3 ≤ x, y, z ≤ 10 (the
exponent depth). **Verified by strict enumeration (0 invalid
entries):** exactly **83 solutions** in the box, and **every one of
the 83 carries a common prime factor** (gcd(A,B,C) ≥ 2; the factor is
2, 3, 7, or 13/17/19/31 — the spf of the gcd). **Zero primitive
triples on the line.**

The 83, verbatim (the ledger the store will hold — recorded
occurrence, never optimized):

```
2^3+2^3=2^4   2^4+2^4=2^5   2^5+2^5=2^6   2^6+2^6=2^7
2^7+2^7=2^8   2^8+2^8=2^9   2^9+2^9=2^10
2^5+2^5=4^3   2^7+2^7=4^4   2^9+2^9=4^5
2^8+2^8=8^3   2^6+4^3=2^7   2^8+4^4=2^9   2^8+4^4=8^3
2^9+8^3=2^10  2^9+8^3=4^5
3^3+6^3=3^5   3^6+18^3=3^8  3^6+18^3=9^4
4^3+2^6=2^7   4^4+2^8=2^9   4^4+2^8=8^3
4^3+4^3=2^7   4^4+4^4=2^9   4^4+4^4=8^3
4^7+4^7=8^5   4^10+4^10=8^7 4^7+4^7=32^3
4^10+16^5=8^7 4^10+32^4=8^7
6^3+3^3=3^5   7^3+7^4=14^3  7^4+7^3=14^3
8^3+2^9=2^10  8^3+2^9=4^5   8^3+8^3=2^10
8^3+8^3=4^5   8^5+8^5=4^8   8^5+8^5=16^4
8^9+8^9=16^7  8^8+8^8=32^5  8^8+16^6=32^5
8^5+32^3=4^8  8^5+32^3=16^4 8^8+64^4=32^5
9^3+18^3=3^8  9^3+18^3=9^4
15^4+15^5=30^4 15^5+15^4=30^4
16^5+4^10=8^7 16^6+8^8=32^5 16^5+16^5=8^7
16^6+16^6=32^5 16^5+32^4=8^7 16^6+64^4=32^5
17^4+34^4=17^5 18^3+3^6=3^8 18^3+3^6=9^4
18^3+9^3=3^8  18^3+9^3=9^4
19^4+38^3=57^3 26^3+26^4=78^3 26^4+26^3=78^3
28^3+84^3=28^4 31^5+31^6=62^5 31^6+31^5=62^5
32^4+4^10=8^7 32^3+8^5=4^8 32^3+8^5=16^4
32^4+16^5=8^7 32^3+32^3=4^8 32^4+32^4=8^7
32^3+32^3=16^4 32^7+32^7=16^9 32^7+32^7=64^6
33^5+66^5=33^6 34^4+17^4=17^5 38^3+19^4=57^3
64^4+8^8=32^5 64^4+16^6=32^5 64^4+64^4=32^5
66^5+33^5=33^6 84^3+28^3=28^4
```

(the full 83-row list is the mechanism output of 2026-08-24; the
store holds the census as declared facts, the per-triple common
factor named, at the line end 84; the census re-derivation takes
< 1 s on the reference, gate-safe.)

**The line's statement (the in-store Beal, at the line end):** on my
line, every recorded triple (83 of 83) carries its common prime
factor; no primitive triple lives on my line; the line ends where
the primitive triples would live (the box is 84 × depth 10), and the
primitive territory is a wall.

## D4 — the LTE ledger (verified, the prescribed theorem)

**The identity (classical odd-p form):** for an odd prime p with
p | (x − y) and p ∤ x·y: v_p(x^n − y^n) = v_p(x − y) + v_p(n).

**The ledger box (on the line):** odd primes p ≤ 84 (the line's
primes); 1 ≤ y ≤ 84 with p ∤ y; x = y + m·p ≤ 84 (m ≥ 1) with p ∤ x;
3 ≤ n ≤ 84. **Instance count: 249,280.** **Verified: the identity
holds in every one of the 249,280 instances (0 deviations);**
the largest difference factored is 162 digits; the full ledger
re-derivation runs in **0.2 s** (gate-safe as a P-check
re-derivation). v_p is read off the spf chain's p-rung (the S11
machinery, promoted to a lesson).

## D5 — the walls (declared off-line territory)

- **W-Beal-1 (the primitive territory):** no pairwise-coprime
  solution with x, y, z > 2 exists — that is exactly what the
  conjecture asserts; the line's box (84 × 10) holds 83 triples,
  none primitive; a counterexample would need three 3-powerful
  terms (the smallest known coprime 3-powerful sums,
  271^3 + 2^3·3^5·73^3 = 919^3 = 776,151,559, are far past the
  line), at the line end 84. Named, never stored as a value.
- **W-Beal-2 (the Fermat–Catalan boundary):** the primitive
  solutions with 1/x + 1/y + 1/z < 1 are finite (Darmon–
  Granville, ineffective) and — Beal's restatement — every known
  one uses 2 as an exponent (7^3 + 13^2 = 2^9, 3^5 + 10^2 = 7^3,
  2^5 + 7^2 = 3^4 — the
  exponent-2 solutions sit outside this band's condition x, y, z
  > 2), at the line end 84.
- **W-Beal-3 (the closed anchor):** the equal-exponent case
  x = y = z ≥ 3 is Fermat's Last Theorem — no positive-integer
  solutions (Wiles, 1994; a declared record of record, the store
  does not hold the proof), at the line end 84.

## D6 — band shape (pre-reg, for S17 = E6.21 "the valuation line")

- **Seed:** the official S16 store (1581, identity
  `e21eaaf32b475930`, line 0..84, seam 122).
- **New concepts (prereqs point DOWN to the spf/valuation soil of
  S11 and the arithmetic of band-2):** `valuation` (v_p = the
  p-rung of my spf chain; prereq: the S11 spf/prime soil),
  `lte-form` (the LTE identity's odd-p form; prereq: valuation),
  `beal-summit` (the statement itself, a declared record fact;
  prereqs: valuation + the S11 divisibility soil), `beal-census`
  (the verification census: the box, the 83 triples, the common
  factor invariant, the primitive-emptiness on the line; prereqs:
  beal-summit + the S11 census pattern).
- **Lessons:** `valuation-def` (v_p read off the spf chain),
  `lte-def` (the odd-p LTE identity, the classical form),
  `beal-def` (the statement verbatim, house-voiced — the AMS
  record), `census-def` (the verification census on the line:
  the box 84 × 10, 83 triples, every one carrying its common
  factor, none primitive).
- **Theorems (prescribed, strict parts):** the LTE ledger
  composition (lte-form: lte-def + valuation-def — verified on the
  line by the 249,280-instance ledger, 0 deviations) and the
  census-satisfaction composition (beal-summit: beal-def +
  census-def — the line's 83 triples satisfy the statement; the
  primitive territory is declared, not reached).
- **Walls:** the three W-Beal walls (D5). **Candidate invariant:**
  NO `theorem:beal` (the statement stands as the declared record
  fact `lemma:beal-def` + the census-satisfaction composition; the
  bare conj id is the island's wall, not its store fact).
- **The beal-reach:** the missing ingredient, named — uniform
  control of the primitive solutions for fully-distinct hyperbolic
  triples (the gap between the finiteness wall and the emptiness
  claim, exactly the BSD *-reach* pattern in the valuation soil).
- **offline_watch:** the 3-powerful counterexample scale
  (776,151,559-class values) and the FLT/DG territory — named on
  the walls, never as line decimals.

Execution: the bandgen way — spec (spec-e6.21.json) → validate →
dryrun (control #1) → freeze → e621.py (P0–P8) → official gate →
close-out. Deviation family for this band: **D-e6l** (pre-reg
corrections, recorded at closeout).
