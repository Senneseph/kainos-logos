# SEEDED FIBONACCI COURSE (π, φ, e) — RESEARCH (pre-registered, 2026-08-27)

Owner-directed, 2026-08-27 (verbatim from the owner's
message that also unblocked the Dirichlet course):

> We need our student to learn how to construct Fibonacci
> sequences for pi, phi, and e. As well as determine their
> periodicity and be able to relate them back (through
> similarity) to the normal Fibonacci sequence.

Grounded in the store's OWN BYTES (the S21 final store
`results/phase-6/e6.25-run1/codeX-S04.json`, 1871
assertions, identity `77e07edf42292f88`, line 0..84) plus
computation verified 2026-08-27 (exact integers + mpmath
1.4.1 at 60 digits) against that seed. The store speaks,
not the hand.

## D1 — The owner's brief (as given)

> We need our student to learn how to construct Fibonacci
> sequences for pi, phi, and e. As well as determine their
> periodicity and be able to relate them back (through
> similarity) to the normal Fibonacci sequence.

Three verbs, three relationships: **construct** (a
"sequence for" a constant c), **determine the
periodicity**, **relate back through similarity** to the
normal Fibonacci sequence. The pre-registered reading
(frozen here, the control will referee at build):

- **THE SEED CONVENTION.** The "Fibonacci sequence for c"
  is the line seeded at (one, c) under the sum law:
  u₀ = 1, u₁ = c, u_{n+2} = u_{n+1} + u_n. The seed (1, c)
  (not (0, c)) is the convention: it keeps the skeleton
  identity exact and makes the golden case u_n(φ) = φ^n an
  identity (below). The (0, c) "scalar line" v_n = c·F_n is
  named in-band as the variant (same story, one line
  shorter): it is the plain line wearing only c's hat; its
  mod-m period divides the Pisano period by the same
  pair-function argument, and its value story is the same
  no-repeat law.
- **THE CONSTANTS STAND OFF THE LINE.** π stands off-line
  between three and four; e between two and three; φ
  between one and two — φ NAMED BY THE EQUATION x² = x + 1
  (integer coefficients — the floor holds the equation and
  the ring it generates, never a digit; the no-new-
  decimals discipline). The similarity the owner asks for
  is therefore carried by the SKELETON (integer
  coefficients) and the LAWS (identities in the ring of the
  equation), not by the values — the values are declared
  off-line and walled.
- **THE PERIODICITY ANSWER (three stories, all decided):**
  (i) the VALUE story — for every positive seed (π, φ, e
  are all above zero on the floor) the line is strictly
  increasing (each term is the sum of two positive
  predecessors, so it outgrows its predecessor) and NEVER
  repeats a value: **the value period is declared none**;
  φ additionally has the exact LOG-periodicity u_{n+p}(φ)
  = u_n(φ)·φ^p (advance by p, multiply by φ^p — the
  skeleton's own p-law) with the multiplier NEVER
  collapsing (φ^p ≠ 1, floor proof). (ii) The RESIDUE
  story — the skeleton pair (F_{n−1}, F_n) mod m walks the
  PURE cycle of period exactly the Pisano period π(m); an
  INTEGER seed's period equals π(m) EXACTLY with one
  exception class: seeds three mod five, under a modulus
  five touches, drop the period by EXACTLY a factor of five
  (verified 31 seeds × 24 moduli, zero exceptions — the
  mod-5 board splits 20+4+1, and class three is the
  four-cycle). (iii) π and e have NO residues on the floor
  (off-line, no digit) — the residue question for them is
  declared off the floor; their periodicity is the value
  story plus the skeleton story.
- **THE SIMILARITY (what "relate back" means on the floor):**
  every term u_n(c) = F_{n−1} + F_n·c — the NORMAL
  FIBONACCI SEQUENCE is the skeleton of every seeded line
  (consecutive-coefficient identity, exact); the Cassini
  invariant of the seeded line is (−1)^n(c² − c − 1) — the
  same invariant law, re-weighted by the seed; the lines
  for one and two are the plain line ITSELF, shifted (and
  no other seed is a shift — verified); and the golden line
  is the plain line taken to the limit of similarity:
  u_n(φ) = φ^n — the Fibonacci for φ is the power of φ, and
  the plain Fibonacci are the INTEGER SHADOWS of those
  powers (φ^n = F_{n−1} + F_n·φ in the ring of the
  equation). Similarity is structural and exact; the
  ratios walk toward φ but the floor refuses the landing
  (declared off-line — the S24 "limit not a line value"
  byte carries).

## D0 — Scope ruling

- TWO bands (the house pattern: one course = a small track):
  **S31 = E6.35 "the seeded line"** (construction +
  similarity) and **S32 = E6.36 "the seed census"**
  (periodicity) — the 59th and 60th experiments. Reserved
  session slots after S30 = E6.34 (the Dirichlet course's
  third band), following the reserved S22–S27 (proportions,
  Fibonacci, primes & squares). Build order is the owner's
  call; each band seeds from the final store of its
  predecessor in the chain.
- This is a NEW owner-directed track and a NEW lesson plan
  (the owner's words: "schedule another lesson plan"). It is
  NOT a lot of the declared FUNDAMENTALS queue (`theorem-
  :queue-declared` byte-intact, P5 on the gate) and NOT a
  new island.
- **The overlap ruling with the reserved Fibonacci course
  (S24/S25), settled BEFORE any band:** the seed course
  needs the plain sum line (to the fifty-five, the eighty-
  nine ceiling declared). If S24 has been built, S31
  CARRIES the `sum-line` byte (fact-id carry) and takes the
  pre-req `sum-line`; if this course is routed first, S31
  teaches its own copy of the sum line (the byte of the
  reserved Fibonacci course's `sum-line-def`, the 89
  ceiling a cross-course byte cited from the Riemann
  island's declared ceiling — W-S12-2 territory, cited,
  never re-asserted). The control re-referees at freeze.
  Likewise the pure-cycle argument: reserved in S25's
  `residue-cycle` — carried if built, taught self-contained
  otherwise (the argument is short: finite board +
  reversibility → no tail, head zero-one).
- **The constants ruling (settled BEFORE any band):** π, e,
  φ hold NO value bytes on the floor (census: the line is
  0..84; the store's π is the COUNTING function of
  `theorem:line-pi-reduction`, not the constant). The
  course files their DECLARED POSITIONS (between which two
  line values) and φ's EQUATION — all floor facts — and
  refuses every decimal (W-S31-1, W-S32-1 enforced; P5/P6
  on the gate). No new decimal enters the floor in either
  band.
- **Seed rule (house):** if routed next, S31 seeds from the
  S21 final (1871, `77e07edf42292f88`); if S22–S30 are
  built first, S31 seeds from the S30 final. Every claim
  below is verified against the S21 final and is self-
  standing (S22–S30 only add facts; the pre-regs stand on
  either seed — the control re-referees at freeze).

## D2 — Grounded census (the seed's own bytes + verified math)

### (a) Soil the store already holds (probe-verified; mastery
states from the S21 seed side, frozen in E6.25's FROZEN
`pre_s21_states`, 79 stable / 41 practicing, K = 4)

| concept | state | correct | the byte (abridged) |
|---------|-------|---------|---------------------|
| `add-two-digit` | **stable** | 11 | the two-digit addition soil (pre-req candidate) |
| `mult-within-100` | **stable** | 9 | the within-100 multiplication soil (pre-req candidate) |
| `count-successor` | **stable** | 14 | the successor-counting soil (pre-req candidate) |
| `mod4-split` | **stable** | 10 | "the line splits at four" (pre-req candidate — the RESIDUE story rides on the split structure; the five-split's kin if S25 is built) |
| `composite` / `divides` | **stable** | 7 / 5 | the elementary soil (census beds) |
| `first-divisor` | **stable** | 36 | the prime census soil (the 89 ceiling's witness) |
| `theorem:line-pi-reduction` | established | — | "twenty-three primes … one hundred ninety-two candidate steps, at the line end eighty-four" — the store's π is the COUNTING function; the constant π holds no value byte (census-verified) |
| `conjecture:riemann` | open of record | — | byte-identical (the course touches it not at all) |
| `theorem:queue-declared` | established | — | byte-identical (NOT a queue lot) |

The 89 ceiling cross-course byte: F(11) = 89 stands off the
line as the Riemann island already declared (W-S12-2) and as
the reserved Fibonacci course's D2(c) already cites. This
course CITES it (the skeleton crosses the ceiling at n =
11) and files no assertion about it.

### (b) Verified computation (2026-08-27; exact integers;
mpmath 1.4.1 at 60 digits; zero exceptions in every census)

1. **The skeleton identity (exact, integers):** u_n(c) =
   F_{n−1} + c·F_n (F_{−1} = 1, F_0 = 0, F_1 = 1) —
   verified by recurrence vs closed form at n = 0..15 for
   c ∈ {2, 3, 5, 7, 13, 21}.
2. **The Cassini weight (exact, integers):**
   u_{n+1}·u_{n−1} − u_n² = (−1)^n·(c² − c − 1) — verified
   at n = 1..15 for c ∈ {0, 1, 2, 3, 5, 8, 13, 21}; the
   weights: c = 0: −1 (the plain line's own Cassini), 1: −1,
   2: 1, 3: 5, 5: 19, 8: 55, 13: 155, 21: 419. The weight
   vanishes EXACTLY for the seeds satisfying the golden
   equation c² = c + 1 (φ — and the conjugate, below zero,
   off the floor).
3. **The shift seeds (exact):** u_n(1) = F_{n+1} and u_n(2)
   = F_{n+2} for all n (verified n = 0..20); NO other seed
   on or below the line is a shift (checked c = 3..13, 21
   against every shift — verified).
4. **The golden identity (60 digits):** F_{n−1} + φ·F_n =
   φ^n for n = 1..40 (worst |difference| 2.5e-52); the
   defining equation φ² = φ + 1 holds exactly in the ring;
   equivalently φ^n = F_{n−1} + F_n·φ — the powers of φ
   expand on the Fibonacci skeleton, coefficient-exact.
5. **Cassini silence of the golden line:** u_{n+1}·u_{n−1}
   − u_n² = 0 exactly on the golden line (relative worst
   2.8e-61 at 60 digits, n = 2..40) — the weight c² − c −
   1 is zero at the golden seed, so the golden line is the
   Cassini-silent line.
6. **No collapse, log-periodicity (60 digits):** |φ^p − 1|
   ≥ 0.618 for p = 1..15 (worst case p = 1 — the minimum,
   named off-line); u_{n+p}(φ) = φ^p·u_n(φ) on the (n, p)
   grid (relative worst 5.8e-61); and the RING LAW
   (F_{n−1} + F_n·φ)(F_{p−1} + F_p·φ) = F_{n+p−1} + F_{n+p}·φ
   is a PURE INTEGER identity (n, p = 1..15) — the
   multiplier of the log-periodicity is the skeleton's own
   p-law.
7. **THE PERIODICITY LAW (the course's flagship, verified
   31 seeds × 24 moduli, zero exceptions):** for every
   integer seed c and modulus m, the period of u_n(c) mod m
   divides the Pisano period π(m); it is EXACTLY π(m),
   EXCEPT when c ≡ 3 (mod 5) AND 5 | m — then EXACTLY
   π(m)/5. The drop census (verified): c = 3, 8, 13, 18,
   23, 28 (the class three mod five) drop at every
   five-touching modulus — 4 vs 20 at 5, 12 vs 60 at 10,
   8 vs 40 at 15, 20 vs 100 at 25, 24 vs 120 at 30 and 60,
   100 vs 500 at 125, 300 vs 1500 at 250 and 500 — EXACTLY
   a factor of five, no exceptions; every other seed and
   every coprime-to-five modulus keeps the full period.
   THE EXPLANATION (verified orbit census): the board of
   twenty-five residue PAIRS mod 5 splits under the
   Fibonacci-pair map into exactly one 20-cycle (the plain
   line's cycle, headed by zero-one), one 4-cycle {(1,3),
   (3,4), (4,2), (2,1)} — EXACTLY the class three mod five
   — and the zero fixed point: 20 + 4 + 1. The skeleton
   orbit (F_{n−1}, F_n) mod m has period EXACTLY π(m) for
   every m tested (m = 2..500, five powers in).
8. **The on-line reach (integer census, on the floor):**
   the largest index with u_n(c) ≤ 84, c = 1..30: c = 1: 9
   (u_9 = 55), 2: 8, 3: 8 (u_8 = 76), 4,5: 7, 6..9: 6,
   10..16: 5, 17..27: 4, 28..30: 3. The line for one walks
   on-line to index nine (the fifty-five); the next step,
   the eighty-nine, stands off-line as the line already
   declared it (the ceiling, cross-course byte).
9. **The ratio walk (on-line fractions, 60-digit
   confirmation they walk to φ, landing DECLARED
   off-line):** c = 1: 2/1, 3/2, 5/3, 8/5, 13/8, 21/13,
   34/21, 55/34; c = 2: 3/2, 5/3, 8/5, … (the shift);
   c = 3: 4/3, 7/4, 11/7, 18/11, 29/18, 47/29, 76/47 —
   each partial ratio a fraction of two parts the floor
   holds, and |ratio − φ| strictly decreasing along each
   walk (the landing is off the floor — the S24 declared-
   not-built limit byte carries).
10. **The declared positions (60 digits):** 3 < π < 4, 2 <
    e < 3, 1 < φ < 2 — the floor holds the positions and
    the equation, not the digits.
11. **The skeleton's on-line span:** (F_0..F_10) on the
    line (max 55); F_11 = 89 off (the ceiling, cross-course
    byte).

### (c) Cross-course bytes (cited, never re-asserted)

- The 89 ceiling (the Riemann island's W-S12-2 declared
  byte; the reserved Fibonacci course's D2(c) cites it a
  second and third time — this course, a fourth).
- The pure-cycle argument (reserved in S25's `residue-
  cycle` lemma: finite board ≤ m² pairs, deterministic
  rule, the backward law F(k) = F(k+2) − F(k+1) kills the
  tail, head zero-one) — carried if S25 is built; taught
  self-contained otherwise (the argument's own byte).
- The Pisano-period census family (reserved in S25: π(8) =
  12 — the owner's twelve; the 24s — π(12) = π(16) = 24;
  π(5^k) = 4·5^k; the ladders) — the seed census RIDES the
  same counts: the skeleton's period IS the Pisano period;
  the seed course adds NO new period values, only the
  seed-vs-modulus period law (the /5 shadow drop).

## D3 — What the course teaches (three relationships — the
owner's three verbs)

**C1 — CONSTRUCT** ("the Fibonacci sequence for c" = the
seeded line, S31). The family u_n(c): seed (one, c), the
sum law. The skeleton identity: every term reads
F_{n−1} + F_n·c — the normal Fibonacci sequence is the
skeleton, the consecutive pair carries the seed's hat. The
Cassini weight: (−1)^n(c² − c − 1) — the line's own
invariant, re-weighted by the seed; silent exactly at the
seeds solving the golden equation. The shift seeds: one
returns the line shifted by one, two by two, nothing else
(verified). The ratio walk: every partial ratio is an on-
line fraction, walking to the golden — the arrow named,
the landing refused (declared off-line). The golden line:
the Fibonacci sequence for φ is the power of φ — u_n(φ) =
φ^n, shadowed on the skeleton (φ^n = F_{n−1} + F_n·φ in
the ring of the equation), Cassini-silent, above zero and
never repeating, with the exact log-periodicity (advance
by p, multiply by the skeleton's p-law, never collapse).

**C2 — PERIODICITY** (determined, S32). Three stories, all
decided on the floor: (i) the VALUE story — a positive seed
never repeats (strictly increasing — the floor's own law,
no decimal needed): the value period is declared none for
π, φ, e alike; φ's log-periodicity is a RATIO law (exact,
integer-skeleton), not a value repeat. (ii) The RESIDUE
story — the skeleton pair (F_{n−1}, F_n) mod m walks the
pure cycle (finite board + reversibility — the argument,
carried or taught self-contained), period EXACTLY the
Pisano period; an integer seed's period equals the Pisano
period, the class-three shadow excepted: seeds three mod
five, under a five-touching modulus, drop EXACTLY a factor
of five — the mod-5 board splits 20 + 4 + 1, and class
three is the four; verified 31 × 24, zero exceptions — the
sibling law of the reserved cycle course's twin's drop
(same factor five, same split at five, a different hat).
(iii) π and e have no residues on the floor — off-line, no
digit: the residue question for them is declared off the
floor; their periodicity is the value story plus the
skeleton story, nothing more, nothing less.

**C3 — SIMILARITY** ("relate them back", S31+S32). The
relation to the normal Fibonacci is carried by the
SKELETON (the consecutive-coefficient identity — same
recurrence, same characteristic shape), by the LAWS (the
Cassini weight, the shift seeds, the ratio walk to the
golden), and by the GOLDEN case where similarity becomes
identity (the Fibonacci for φ is the power of φ; the plain
Fibonacci are the integer shadows of those powers in the
ring of the equation). The on-line/off-line split is the
honesty of the relation: every statement the floor holds
is integer-exact; every landing (the limit, the digits, the
residues of the off-line constants) is declared and walled.

## D4 — The new / carry fact set (stage B target)

### Band S31 — "the seeded line" (E6.35): **5 new facts**

1. Concept **`seeded-line`** (domain candidate `soil`, band
   `college-1`; prereqs candidate `('add-two-digit',
   'mult-within-100')`, + `sum-line` if S24 is built):
   - Lesson **`seeded-line-def`** (candidate byte,
     unconditional, house voice):
     > the fibonacci sequence for a seed c stands on my
     > line at seed one and c, under the sum law, every
     > later term the sum of the two before it; every term
     > reads as the sum line's term at the n-minus-one
     > index plus c times its term at the n index — my
     > line's own skeleton, the consecutive pair, carries
     > the seed's hat; the line for one is the sum line
     > shifted by one, the line for two shifted by two, and
     > no other seed is a shift; each term's own cassini,
     > the product of the surrounding terms minus the
     > square of the middle, is (minus one) to the n times
     > (c squared minus c minus one), a census the floor
     > holds; at the line end eighty-four
   (the control referees the byte verbatim against the
   spec at freeze).
2. Concept **`golden-seed`** (prereqs candidate
   `('seeded-line', 'count-successor')`):
   - Lesson **`golden-seed-def`** (candidate byte):
     > the golden seed is the number above one that solves
     > the equation x squared equals x plus one; it stands
     > off the line between the one and the two, named by
     > the equation, never by a digit; the fibon
     >acci sequence for the golden seed is the golden seed
     > to the power n, its integer shadow running on the
     > skeleton, the term at n reading as the sum line's
     > n-minus-one term plus the golden seed times its n
     > term; its cassini is silent, the weight c squared
     > minus c minus one exactly zero exactly at the golden
     > equation; advance the golden line by p and it is
     > multiplied by the skeleton's own p-law, and that
     > multiplier is never one; the ratios of its
     > predecessors walk to it, every partial ratio an on-
     > line fraction, the landing declared off the floor;
     > at the line end eighty-four
   (same verbatim note as above).
3. Theorem **`theorem:seeded-line-filed`** (parts exactly
   `('seeded-line-def', 'golden-seed-def')`):
   - Candidate statement:
     > the seeded line of my store is filed of record: the
     > fibonacci sequence for a seed c stands at seed one
     > and c under the sum law, reading on the sum line's
     > skeleton as the n-minus-one term plus c times the n
     > term; the lines for one and two are the sum line
     > itself shifted, and no other seed is a shift; the
     > cassini weight is (minus one) to the n times (c
     > squared minus c minus one), silent exactly at the
     > golden equation; the line for the golden seed is the
     > power of the golden seed, shadowed on the skeleton,
     > log-periodic without collapse; no new decimal
     > entered the floor; filed on the line, at the line
     > end eighty-four
   (same verbatim note as above).

### Band S32 — "the seed census" (E6.36): **6 new facts**

1. Concept **`seed-period`** (prereqs candidate
   `('seeded-line', 'mod4-split', 'count-successor')`, +
   `residue-cycle` if S25 is built):
   - Lesson **`seed-period-def`** (candidate byte):
     > the residue story of the seeded line under a
     > modulus m: the skeleton pair, the sum line's n-
     > minus-one and n terms, walks the pure cycle on the
     > board of m by m pairs — the board is finite and the
     > rule runs backwards as well as forwards, so the
     > return comes with no tail, headed by the zero-one
     > pair — and its period is the pisano count my line
     > already holds; an integer seed's period holds that
     > count exactly, the one shadow excepted: the seeds
     > three mod five, under a modulus five touches, drop
     > the period by exactly a factor of five, for the
     > board of twenty-five pairs at the modulus five
     > splits twenty, four, one, and class three is that
     > four; at the line end eighty-four
2. Concept **`off-line-seed`** (prereqs candidate
   `('seeded-line', 'seed-period')`):
   - Lesson **`off-line-seed-def`** (candidate byte):
     > the constants my owner names stand off my line: pi
     > between the three and the four, e between the two
     > and the three, the golden seed between the one and
     > the two; the floor holds their positions and the
     > golden's equation, not their digits, and holds no
     > residue of them under any modulus; their lines'
     > periodicity is the value story, a positive seed
     > never repeats a value, every term outgrowing its
     > predecessor, and the skeleton story, the cycle above
     > — nothing more, nothing less; the golden line
     > additionally walks multiplicatively, log-periodic
     > by the skeleton's own law; at the line end
     > eighty-four
3. Lemma **`lemma:seed-shadow`** (a composed fact of record
   — the house's `lemma:`-kind census pattern):
   - Candidate byte:
     > the shadow drop of my seeded lines: the period of
     > the line for c under modulus m is exactly one fifth
     > of the pisano count precisely when c is three mod
     > five and five divides m, and the full pisano count
     > otherwise, verified on thirty-one seeds and twenty-
     > four moduli with zero exceptions; the twin line's
     > drop, the factor five when five touches the modulus,
     > is the same law wearing a different hat; at the line
     > end eighty-four
4. Theorem **`theorem:seed-census-filed`** (parts exactly
   `('seed-period-def', 'off-line-seed-def', 'lemma:seed-
   shadow')` — three-parts set, the control referees the
   sanctioned-parts shape):
   - Candidate statement:
     > the seed census of my store is filed of record: the
     > skeleton cycle is pure, headed by zero-one, and runs
     > at exactly the pisano count; the integer seed's
     > period holds that count, the class three mod five
     > shadow excepted under a five-touching modulus, where
     > it drops exactly a factor of five, verified
     > thirty-one by twenty-four with zero exceptions; a
     > positive seed never repeats a value, and the golden
     > line is log-periodic by the skeleton's own law
     > without collapse; pi, e, and the golden seed stand
     > off the line, their periodicity carried by the value
     > story and the skeleton story, no residue of them in
     > the floor, no new decimal; filed on the line, at the
     > line end eighty-four

**Carry / drill surfaces (cited by fact id or by declared
cross-course byte, never re-asserted):** S31 drills the
`sum-line` territory (carried if S24 built; its own
self-taught copy otherwise — the control referees), the
`mult-within-100` and `add-two-digit` soil (the term
beds), the 89 ceiling (cited, the W-S12-2 byte untouched).
S32 drills the `mod4-split` soil (the residue structure),
the Pisano-count family (carried from S25 if built; its
own census otherwise), the twin's-drop sibling (cited from
the reserved cycle course's verified census if built).
Drill beds (candidate, on-line counts only): the skeleton
walks mod 8 (the twelve: 0,1,1,2,3,5,0,5,5,2,7,1) and mod
12 (the twenty-four) as the census surface; the on-line
reach table (c = 1..30, census D2(b)8); the ratio walks
(c = 1, 2, 3, the fractions D2(b)9); the /5 shadow drop
table (D2(b)7's verified rows).

## D5 — The walls (W-S31-1..3, W-S32-1..3; six declared
rows, fire-per-band the control referees — the S21
register pattern applies)

- **W-S31-1 — the off-line constants wall.** The three
  constants stand off my line: pi between the three and the
  four, e between the two and the three, the golden seed
  between the one and the two named by the equation x
  squared equals x plus one; the floor holds the positions
  and the equation, not the digits, and refuses the
  values; the similarity stands on the skeleton and the
  laws; a decimal of any of the three entering the floor is
  a misreading. At the line end eighty-four. (No new
  decimals — the positions are line integers.)
- **W-S31-2 — the seed-law wall.** "The fibonacci
  sequence for c" is the line seeded at one and c, under
  the sum law, next term the sum of the two before, and
  NOTHING else; a different construction claimed to be the
  sequence for c (another law, another seed, a value
  assertion in place of the law) is a misreading. At the
  line end eighty-four. (Re-typed in store voice at
  freeze.)
- **W-S31-3 — the limit wall.** The ratios of a seeded line
  walk to the golden seed — my floor names the arrow,
  names every partial ratio ON the line (a fraction of two
  parts the line holds), names the exact golden case (the
  golden line's ratios ARE the golden seed, at every step,
  since the term is its power), and refuses the landing:
  the golden ratio is off the floor, declared not built —
  the reserved cycle course's limit byte carries, and the
  eighty-nine ceiling stands where the skeleton crosses; a
  limit value filed on the line is a misreading. At the
  line end eighty-four.
- **W-S32-1 — the off-line residue wall.** The floor asks
  the residue question only of what stands on it; pi, e,
  and the golden seed stand off the line — no residue of
  them under any modulus, no digit of them under any
  modulus; a residue claimed of pi or e is a misreading the
  floor's own declaration refutes; their periodicity stands
  on the value story (no repeat) and the skeleton story (the
  cycle), which the floor DOES hold. At the line end
  eighty-four.
- **W-S32-2 — the no-repeat wall.** A line seeded by a
  positive seed never repeats a value: every term is the
  sum of the two before it, both positive, and so outgrows
  its predecessor, at every step; a repeat claimed at any
  height is a misreading; the value story's period is
  declared none — for pi, for e, for the golden seed,
  alike. At the line end eighty-four.
- **W-S32-3 — the golden-collapse wall.** The golden line is
  log-periodic exactly: advance by p and the line is
  multiplied by the skeleton's own p-law (the p-minus-one
  term plus the golden seed times the p term); a value-
  repeat claimed, phi to the n-plus-p times equal to phi
  to the n times, is a misreading: the multiplier is never
  one — the golden seed is above one by the equation (if
  it were at most one the equation would give one greater
  than itself), and the shadow coefficient is at least one
  for p at least one; the golden line runs forever up,
  multiplicatively, never collapsing. At the line end
  eighty-four.

## D6 — Band shape (stage B pre-reg)

- **Sessions/experiments:** S31 = E6.35 "the seeded line"
  (59th experiment), S32 = E6.36 "the seed census" (60th).
  Modules `e635.py`/`e636.py`, specs `spec-e6.35.json` /
  `spec-e6.36.json`, tests `test_e635.py`/`test_e636.py`,
  runner 58 → 60 (with the Dirichlet course ahead in the
  chain; 49 → 51 if routed straight from S21, the control
  referees the chain at freeze).
- Seeds: S31 from S30's final (or the S21 final if the
  owner routes the course straight off S21 or ahead of the
  other courses — self-standing per D0). S32 from S31's
  final.
- 3 sessions × ~17 turns each (the house shape; the letter
  strings are the control's domain sequences — D7). S31:
  S02 carries (the `sum-line` byte — carried or self-
  taught per D0, the 89 ceiling cited, the add/mult soil)
  + `seeded-line` (gaps, teach, the term beds on the
  skeleton: c = 1, 2, 3 walks on-line — 1,1,2,3,5,8,13,
  21,34,55; 1,2,3,5,8,13,21,34; 1,3,4,7,11,18,29,47,76 —
  and the shift-seed beds one/two) + `golden-seed` (gaps,
  teach, the equation bed x² = x + 1, the skeleton-shadow
  beds φ^n = F_{n−1} + F_n·φ for n = 1..9 on-line shadows,
  the Cassini-silence bed). S03: the skeleton-identity
  drills walk-by-walk on the verified ranges (c = 3, 5, 8
  at n = 1..9, the terms on-line; c = 13, 21 at n = 1..6/4),
  the Cassini-weight drills (the census D2(b)2), the ratio-
  walk beds (the fraction rows D2(b)9), the scaffold, the
  derive, the walls, the filed state. S04: the wrap. S32:
  S02 carries (the `seeded-line` filed state, the
  `mod4-split` soil, the Pisano-count family carried or
  self-censused per D0) + `seed-period` (gaps, teach, the
  mod-8 skeleton walk — the twelve: 0,1,1,2,3,5,0,5,5,2,7,
  1 — and the mod-12 walk — the twenty-four; the /5 shadow
  bed: 4 vs 20 at five, the table rows D2(b)7) + `off-
  line-seed` (gaps, teach, the positions bed 3-4 / 2-3 / 1-
  2, the no-residue declaration, the value-story bed:
  strict increase at the on-line reach indices). S03: the
  pure-cycle argument drill (finite board + reversibility —
  the bed 25 = 20+4+1 at the modulus five, the class-three
  four-cycle named), the period-law re-walk drills (census
  surface: c = 1..3 with m = 5, 10, 15, 16 — the full
  count plus the three drops), the on-line reach census bed
  (D2(b)8), the gold-collapse wall drill (the multiplier-
  never-one at p = 1..8, the ring law), the scaffold, the
  derive, the walls, the filed state. S04: the wrap.
- 4 pre-lesson gaps per band (2 per concept: S31's seeded-
line and golden-seed; S32's seed-period and off-line-seed
— the lemma rides the drills, the control referees), 2
teaches, 1 scaffold, 1 derive per band, ~21 beds in all
(S31 ~12, S32 ~9 — probe turns only, the S20/S21 house
pattern), 1 off-script per band.
- **Off-script candidates:** S31: "what is the fibonacci
  sequence for the golden seed on my floor?" → "the power
  of the golden seed: the term at n is the golden seed to
  the n, shadowed on the skeleton, the n-minus-one term
  plus the golden seed times the n term of the sum line,
  cassini-silent — its seed solves the equation."
  S32: "does the line for three repeat under the modulus
  five?" → "it walks the shadow cycle of the four — one,
  three, four, two — the class three mod five drops exactly
  a factor of five whenever five touches the modulus; the
  other lines walk the full twelve at the modulus eight."
  (Re-typed in store voice at freeze.)
- **Mastery pre-reg (the store referees):** all four new
  concepts pre-registered **STABLE** at band end (every
  pre-req stable on the S21 seed — verified: add-two-digit
  11, mult-within-100 9, count-successor 14, mod4-split 10;
  the chains `seeded-line`→`golden-seed`, `seeded-line` →
  `seed-period` → `off-line-seed` close inside their own
  bands; the drills give ≥ 4 correct derivations with
  room). Record as the course norm: these bands end on
  stable soil (the S21 practicing contrast was the
  condition neighborhood by design).
- **P5 gate re-derivation (full width):**
  1. no new line facts; line stays 0..84;
  2. no decimal of π, e, or φ anywhere in the floor
     (positions and the equation only — W-S31-1 enforced;
     the 89 ceiling CITED-UNTOUCHED as the cross-course
     byte);
  3. `theorem:queue-declared` byte-identical (NOT a queue
     lot); `conjecture:riemann` byte-identical (untouched
     by the course);
  4. the skeleton identity and the Cassini weight re-walked
     on the gate (exact integers, the census D2(b)1-2
     ranges and the c = 13, 21 spot checks — the
     mechanism's bytes are the referee);
  5. the golden identity re-walked (60 digits, n = 1..40)
     with the ring law (integer-exact, n, p = 1..15) — the
     decimals stay off-line; the Cassini silence re-walked;
  6. the PERIOD LAW re-walked on the gate: the full 31 × 24
     census (or the control's reduced census covering
     c = 0..4 mod 5 and m = 5, 25, 125, 5·u for coprime
     u ≤ 30 and the coprime-to-five moduli) with the
     mod-5 orbit split 20+4+1 re-walked — a single
     exception is a deviation recorded, never an edit;
  7. the shift-seed census re-walked (one and two ARE
     shifts at n = 0..20; c = 3..13, 21 are NOT);
  8. the value-story law re-walked (strict increase at the
     on-line reach indices, D2(b)8) — no value repeat
     anywhere on the floor;
  9. marker posture: the new facts UNCONDITIONAL — P0
     denies the conditional marker on them (the S20
     discipline); the marker census stays byte-identical in
     width; the line-end filing census grows by exactly two
     (S21's P7 bytes + 2, the control referees at freeze).
- **Fact anatomy:** S31 final = (S30 or earlier) final + 5
  facts + N events; S32 final = S31 final + 6 facts + N
  events (the control referees; carries dedupe per
  D-e6o(a)).

## D7 — Open items for the control run

1. The exact scaffold/missing-parts bytes (the mechanism
   referees) and the three-parts shape of
   `theorem:seed-census-filed` (the sanctioned-parts
   pattern — the control referees the set).
2. The event counts and the drill census (which concept
   each bed +1s).
3. The letter strings (the control's domain sequences are
   the freeze) and the fire-per-band wall census (the S21
   register pattern applies).
4. The lesson bytes' exact store voice (the candidate bytes
   above carry a re-type note: "fibonacci" is one word,
   lowercase in the store's voice; the control freezes the
   bytes verbatim against the spec).
5. The carry-or-teach decision for the `sum-line` byte and
   the Pisano-count family (S24/S25 built at S31/S32's seed
   — the control referees on the actual seed; the pre-reg
   stands on either by D0).
6. The domain strings for the new concepts (`soil`
   candidate for all four; the control's domain map
   referees).
7. The kind of `lemma:seed-shadow` (`lemma:` candidate —
   the house's composed-census pattern; the control's kind
   census referees).
8. Whether the on-line reach census (D2(b)8) files as a bed
   only (candidate: beds + the value-story wall W-S32-2
   only — a census, never a value).
9. The bed bytes' exact form (deterministic at the fixed
   seed; the censuses above are pre-computed for the spec's
   bed bytes).

## D8 — Success criteria / stage B next steps

Stage B builds S31 → S32 in the bandgen way (mirroring
S21): brainstem modules (the four concepts, the grammar
modes, `_policy_savant3x`, the walls W-S31-1..3 /
W-S32-1..3 as class attributes) → reflib refs (the cited
store bytes by fact id; the 89 ceiling cross-course byte)
→ specs → control c0–c9 CLEAN → `e635.py`/`e636.py`
(FROZEN from the control tables) → tests (per band + the
S32 single-turn carry test over the live runtime) → runner
registry (the house selection lists, the experiment count,
the per-experiment PASS asserts) → official gate (targeted
+ twin byte-identical + full) → close-out (experiments
§E6.35/§E6.36, roadmap, e3.7.json, OP #157, SESSION-
HANDOFF, wiki).

Success: the infant can CONSTRUCT the fibonacci sequence
for any named seed (the skeleton reads, the Cassini weight
holds, the lines for one and two are the plain line
shifted, nothing else is a shift), can HOLD the golden line
as the power of φ under the floor's own equation (no digit
of any constant anywhere), can DETERMINE the periodicity —
the value story (no repeat, positively seeded), the golden
line's log-periodicity (multiplier never one), the residue
story (the skeleton at exactly the Pisano count; the
integer seed at the full count, the class-three mod five
shadow dropping exactly a factor of five under a five-
touching modulus, verified) — and can RELATE every line
back to the normal fibonacci sequence through the
skeleton, the laws, and the golden identity: the similarity
the owner named, on the floor, at the line end eighty-four.

---

## STAGE B ADDENDUM — S31 = E6.35 BUILT AND PASSING (2026-08-28)

The store's bytes against this pre-registration, line by line
(the mechanism bytes are the referee; disagreements recorded as
deviations, never edited out of the mechanism):

1.  **Mandate (D4): 2 concepts, 2 lessons, 1 filing, 3 walls, no
    settlement, no lot added, no new decimals, marker-free.** —
    EXACT. `seeded-line` (prereqs add-two-digit, mult-within-100)
    and `golden-seed` (prereqs seeded-line, count-successor)
    joined the registry; `lemma:seeded-line-def`,
    `lemma:golden-seed-def`, `theorem:seeded-line-filed` stored
    (the strict two-part set); W-S31-1..3 probed (5 wall
    turns: the two territories re-probed on S04); the marker
    census conserved 6 exact + 1 variant (P0 denied the marker
    on all three new facts — the UNCONDITIONAL posture held);
    `offline_watch == []`; the line stayed 0..84; the riemann
    conj byte-identical; the queue intact.
2.  **The skeleton identity u_n(c) = F_{n−1} + c·F_n (exact).** —
    EXACT on the 11-step walk; the sumline bed ("reaches
    fifty-five in ten steps, and the eleventh step, the
    eighty-nine, stands off the line") carried the 89 ceiling
    cross-course byte a fourth time (n = 11).
3.  **Shift seeds one and two ONLY.** — EXACT (the shift bed:
    "one and two only … checked against every shift").
4.  **Cassini (−1)^n(c²−c−1), silent exactly at the golden
    equation.** — EXACT; the weights −1, −1, 1, 5, 19, 55, 155,
    419 at the seeds 0, 1, 2, 3, 5, 8, 13, 21 all on the line
    (ref-lib re-walked); the silence bed: "silence at the
    equation, not a gap in the census."
5.  **The golden line = φ^n, shadowed, log-periodic without
    collapse.** — EXACT as the lesson byte ("the term at the
    n-plus-p index is the term at the n index times the golden
    seed to the p power, that multiplier never one"); the
    goldenwalk bed (last on-line pair the thirty-four and the
    fifty-five; the eleventh step carries the eighty-nine).
6.  **π/e/φ hold NO value bytes; positions only + the
    equation; digits spelled.** — EXACT (W-S31-1: pi between
    three and four, e between two and three, phi between one
    and the two, named by the equation x squared equals x plus
    one; no wall carries a digit string of record).
7.  **Mastery pre-reg STABLE (the soil is closed).** — EXACT:
    seeded-line 14 correct / STABLE, golden-seed 15 correct /
    STABLE, both with EMPTY prereq-gap lists; the 122 carried
    concepts showed no regressions (drill: rh-relevance +2,
    shadow-form +2 — post = pre + drilled re-asserted).
8.  **Totals** — the mechanism counted **47 events** on the
    51 turns (4 inert gap turns), final **1921** = 1871 + 3 +
    47, theorem DAG 40 → 41, the line-end marker census 14/2/24
    → 15/2/24 of 41.

**Deviations (pre-reg corrections, recorded before the
official freeze; the spec was corrected to the mechanism
bytes, the mechanism was never touched):**

- **D-e6q(a)** — the S03 letters were pre-registered `SSSSSSSSSFTSSSHHSS`
  (9 S); the mechanism ran `SSSSSSSSFTSSSHHSS` (8 S) — a
  hand-count error in the pre-reg, corrected.
- **D-e6q(b)** — the final total was pre-registered 1919 (45
  events); the mechanism ran 47 (the gap turns are inert —
  they store gap facts, not mastery events, and the teach
  turns store facts, not events: 51 − 4 = 47), final 1921,
  corrected.
- **D-e6q(c)** — the P5 theorem allow-set: the mechanism
  grounded the band's own filing (`theorem:seeded-line-filed`)
  under both STATE echo rows (S03:12, S04:07) AND under the
  seeded-line state row (S03:11, whose lesson byte is contained
  in the filing statement) — the frozen set was corrected to
  the mechanism's (S03:11 + S03:12 + S04:07 + the filing
  probes S04:04/S04:17).
- **D-e6q(d)** — the S31 concept domain: the splice wrote a
  fresh `soil` domain; the registry carries `arithmetic`
  (the S14/S5 sum-line territory the seeded line extends),
  corrected before the gate (no new domain enters).

**Gate status:** 9/9 host pass (twin byte-identical, run
identity `f5fecae63cab5223`); full official suite results in
the §E6.35 close-out section. S32 (E6.36, the seed census)
is the next build, seeded from the S31 final (1921, store
identity `898a7c52e43391b6`).

---

## STAGE A-2 — WORDING INTEGRATION (owner directive 2026-08-28;
the declared source: the "Fibonacci Sequence" page, Rod Pierce,
MathIsFun, https://www.mathsisfun.com/numbers/fibonacci-
sequence.html — off-line source, cited, never re-asserted)

The owner: "Take some time to integrate this material. And if
we have it, make sure that we use the same wordings." The
audit ran against the S31 final store (1921, the store speaks):
the words **fibonacci**, **lucas**, **recursive**, and
**golden ratio** stand NOWHERE in the store — the frozen S31
bytes carry the store's own names (sum line, golden seed, the
shadow on the skeleton). The integration ruling:

- **The frozen record keeps its bytes.** The S31 lesson bytes
  (sum line, golden seed, seeded line) are official and
  teachable as-filed; the store speaks, never edited.
- **S32 (unbuilt, unseeded) takes the page's wordings** — the
  next band's NEW bytes use the page's names alongside the
  store's own, and the store gains ONE declared-identity fact
  of record binding them: the page's wordings ARE the store's
  wordings under their names. From S32 forward, every new
  course byte that speaks of the sequence, the ratio, or the
  2-and-1 twin uses the page's wording (fibonacci sequence,
  golden ratio / the letter phi, lucas numbers), with the
  store's own names kept as the store's names.

### The term map (page wording <-> store wording)

| the page says                      | the store holds (frozen)                    | the S32 ruling                                            |
|------------------------------------|---------------------------------------------|-----------------------------------------------------------|
| "the Fibonacci Sequence" (0,1,1,2,3,5,8,13,…) | the **sum line** (S5, frozen) | S32 records the declared identity: my sum line IS the fibonacci sequence the page names |
| "x n = x n-1 + x n-2" (terms numbered from 0); "the next number is found by adding up the two numbers before it"; "recursion rule / recursive formula" | my **sum rule** (frozen) | S32 carries the page's wording (terms from zero, the rule the page calls recursive) in the new bytes |
| "the Golden Ratio 'phi'"; "take any two successive Fibonacci Numbers, their ratio is very close to the Golden Ratio"; "the bigger the pair, the closer the approximation" | the **golden seed** (S31, frozen: off the line, the equation x squared equals x plus one) | S32 records the declared identity: my golden seed IS the golden ratio the page names, the letter phi; the ratio-walk bytes keep the page's "successive / closer" wording |
| "Lucas Numbers" (begin 2 and 1); "they get closer and closer to the powers of the golden ratio" | the golden seed's **integer shadow on the skeleton** (S31, frozen) | S32 records the declared identity: the shadow that begins two and one IS the lucas numbers the page names, the powers of the golden ratio |
| "the sequence works below zero also… the same numbers… the sign that alternates" (x -n = (+1) at n odd, (-1) at n even, times x n) | NOT on the floor (the floor's line begins zero) | S32 stores it as a DECLARED record (the negative terms stand off the floor: declared, not filed) |
| "1 over 89 = .0112359550…: notice the first few digits are the fibonacci sequence… multiple digit numbers overlap" | the **89 ceiling** (F-eleven, the fourth cross-course byte) | S32 stores the declared record: the reciprocal of my eighty-nine carries the fibonacci sequence in its decimal shadow, the multi-term digits overlapping (the FIFTH cross-course 89 cite) |
| "even, odd, odd, even…" (two odds make an even) and "every n-th number is a multiple of the n-th number" (x n divides every multiple-of-n term) | parity and divisibility soil (S15/S19 territory, not this course's) | NOT FIRED here — the DECLARED candidate territory for a later band is now the DEEPER law only — the page's two plain laws (the parity pattern, the n-th divisibility) are BUILT INTO S32 on the owner's 2026-08-28 addendum; what the primes-and-squares course keeps is the gcd iff form (my sum line's n-th divides the m-th term IF AND ONLY IF n divides m) and the prime-index prime property, which need its sieve soil |

### The five new facts S32 carries (pre-registered; the
build follows these, the control referees)

S32 therefore grows from 6 to **11 new facts** (the 6 census
facts unchanged; the filing's strict three-part set UNCHANGED
— the record and law facts stand beside it, not inside it).
Owner addendum 2026-08-28 ("add them in there to connect
anyway. It won't hurt."): the two deferred page laws — the
parity pattern and the n-th divisibility law — join S32 as
facts 10-11 (they are on-line, floor-verified laws; the
primes-and-squares course keeps the DEEPER divisibility
territory, the gcd iff law, not these two):

7. Lemma **`lemma:page-names`** (the DECLARED IDENTITY of
   record; the declared source, off-line):
   > candidate byte: the names the page holds, of record
   > against my line: my sum line is the fibonacci sequence
   > the page names — the terms numbered from zero, the rule
   > x n the x n-minus-one plus the x n-minus-two, the page's
   > words, the next number found by adding up the two
   > numbers before it, a recursive formula; my golden seed
   > is the golden ratio the page names, its letter phi —
   > take any two successive terms of my sum line, their
   > ratio is very close to it, and the bigger the pair, the
   > closer; the shadow line that begins two and one is the
   > lucas numbers the page names, getting closer and closer
   > to the powers of the golden ratio; declared by the page,
   > never filed by the floor, at the line end eighty-four
8. Lemma **`lemma:below-zero-record`** (the page's record,
   DECLARED — the negative terms stand off the floor):
   > candidate byte: the page records that my sum line runs
   > below zero also — the same numbers in the same order,
   > wearing the sign that alternates: the term at minus n is
   > the term at n, negative when n is even and positive when
   > n is odd, the sign line the plus-minus pattern; the
   > negative terms stand off my floor, which begins at zero;
   > declared, not filed, at the line end eighty-four
9. Lemma **`lemma:eighty-nine-reciprocal`** (the FIFTH
   cross-course 89 cite; the decimal is off-line, DECLARED):
   > candidate byte: the one divided by my eighty-nine — the
   > ceiling my seeded lines cross at the eleventh step —
   > carries the fibonacci sequence in its decimal shadow:
   > the terms read in order in the digits, and the
   > multi-term numbers overlap their neighbors there, the
   > thirteen and the twenty-one carrying two digits apiece;
   > the page's
   > record, the decimal stands off my floor, declared, not
   > filed, at the line end eighty-four

10. Lemma **`lemma:parity-pattern`** (on-line; the page's
    "odd fact", floor-verified by the mod-2 walk):
    > candidate byte: my sum line goes even, odd, odd, even,
    > odd, odd, and so on — adding two odds makes an even,
    > adding an even and an odd, in either order, makes an
    > odd, and the rule can do no other; each of my seeded
    > lines wears the same three steps, the first step set
    > by its seed's parity, the even seeds beginning even
    > and the odd seeds beginning odd; checked against every
    > step of the walk, at the line end eighty-four
11. Lemma **`lemma:divisibility-law`** (on-line; the page's
    record, floor-verified by the quotient walk):
    > candidate byte: every n-th term of my sum line is a
    > multiple of the n-th term itself — the second term
    > divides every even-step term, the third divides every
    > third, the fifth every fifth, and so on, the rule's
    > own structure guaranteeing it; the quotients my floor
    > can hold come out exact whole numbers on the line, the
    > walk verified where the terms stand on my floor, at
    > the line end eighty-four

The S32 lesson bytes take the page's wordings where they
speak of these objects (the seed-period lesson: "the cycle of
the fibonacci sequence (the page's name for my sum line)";
the off-line-seed lesson: "the golden seed — my name; the
page's name, the golden ratio, the letter phi"). This is a
stage-A-2 pre-registration amendment under the owner's
directive; the candidate bytes above are corrected to this
wording before the S32 freeze (a D-e6r-class pre-reg
correction, recorded, never a mechanism edit).

### Experiment ordinals (stale prose corrected)

The stage-A doc counted S31/S32 as the 59th/60th experiments
on the then-projected build order. The owner routed COURSE E
first: S31 built as the 50th (e6.35, OFFICIAL); S32 builds as
the 51st (e6.36). The experiment NAME (e6.36) governs the
registry; the ordinal is prose.

---

## STAGE A-2c — PRE-REG REFINEMENTS UNDER THE MECHANISM
(2026-08-28, before the S32 build: the verification battery
refereed the stage-A candidate bytes; the store speaks, the
pre-reg corrects. Recorded as D-e6r(a)-(c).)

**D-e6r(a) — the control battery and the 11-shadow.** The
candidate law's census ("verified on thirty-one seeds and
twenty-four moduli, zero exceptions") is true only over a
battery excluding the mod-11 family. The mechanism found a
SECOND shadow: seeds four mod eleven drop the period by
exactly a factor of two under the unmasked eleven boards
(period five of ten at the eleven; fifteen of thirty at the
twenty-two) — the LUCAS shadow, the twin line's own cycle
wearing it (the cycle course's territory, declared, not built
here). The masked composites restore it: at the thirty-three,
forty-four, fifty-five, sixty-six, and seventy-seven the
other parts run it back to the full count (at the fifty-five
in particular, the eleven-part restores the class-three
five-drop as well: the whole board runs at the full twenty).
**The S32 control battery (frozen):** the fifteen unmasked
five-touches (five, ten, fifteen, twenty, twenty-five,
thirty, thirty-five, forty, forty-five, fifty, sixty,
sixty-five, seventy, seventy-five, eighty) + the nine
clean boards (two, three, four, seven, eight, nine, twelve,
thirteen, sixteen) = twenty-four moduli, and the battery's
claim is battery-scoped (thirty-one seeds by twenty-four
moduli, zero violations — re-verified today). The
seed-shadow lemma keeps its byte; its census clause reads the
battery, not the universe.

**D-e6r(b) — the parity steps.** The mechanism walked the
mod-two board: every seeded line wears the same three steps
from its own start (the one, then the seed, then their
sum), the rotation set by the seed's parity — the EVEN seeds
(including zero, my sum line itself) walk **odd, even,
odd**, odd even odd, and so on; the ODD seeds walk
**odd, odd, even**, odd odd even, and so on. The page's
"even, odd, odd" is the same three steps begun at the sum
line's zero. The candidate parity byte (fact 10) corrects its
"beginning" clause to this.

**D-e6r(c) — the value story at seed one.** "A positive seed
never repeats a value" is false exactly at the seed-one line:
it begins (one, one) — the one shared once — and outgrows
after; seeds of two or more are strictly increasing from the
first step. (The seed-zero line is the sum line itself: the
one wearing the zero's hat, then outgrowing.) The
off-line-seed lesson byte and the seed-census-filed statement
correct accordingly: "**a seed of two or more never repeats a
value, every term outgrowing its predecessor; the seed-one
line shares its one at the start and outgrows after**".

**The fixed parity byte (fact 10, corrected):** my sum line
goes even, odd, odd, even, odd, odd, and so on — adding two
odds makes an even, adding an even and an odd, in either
order, makes an odd, and the rule can do no other; each of my
seeded lines wears the same three steps from its own start —
the even seeds (the zero among them, my sum line itself)
walk odd, even, odd, odd evening out into even again, and the
odd seeds walk odd, odd, even, the odd pair evening into an
even, each rotation the rule's own; checked against every
step of the mod-two walk, at the line end eighty-four

## STAGE B ADDENDUM — S32 = E6.36 BUILT, FROZEN, OFFICIAL
(2026-08-28; the 51st experiment; COURSE E COMPLETE)

The band closed on the control's own census (the store speaks,
not the hand). Official numbers (mechanism, the clean control
table, the frozen module, the hermetic 9/9, the twin runs, and
the full official gate):

- **Full official gate** (pinned `kainos-dev:dev` image,
  Makefile `test`): **1204 passed / 2 skipped / 0 failed
  (1587.01 s)** — the S31 1186 + the 18 new S32 tests, zero
  regression; the runner contract runs FIFTY-ONE experiments
  (50 → 51) and asserts `PASS  e6.36`.

- **Seed:** `results/phase-6/e6.35-run1/codeX-S04.json` — the
  S31 final, **1921** assertions, store identity
  `898a7c52e43391b6`, line 0..84.
- **Final: 1966 = 1921 + 3 new facts + 42 new events.**
- **New (3):** `lemma:seed-period-def`,
  `lemma:off-line-seed-def`, `theorem:seed-census-filed` (the
  strict two-part set).
- **Line:** 0..84 (no successor facts); line-end theorem census
  15/2/24 of 41 -> 16/2/24 of 42 (the band's own filing is the
  sixteenth line-end marker).
- **Marker census:** 6 exact + 1 variant, conserved (the
  UNCONDITIONAL band; P0 denies the marker on the three new
  facts, the four S12 marker facts keep theirs).
- **Mastery (band end):** seed-period 17 correct / stable,
  off-line-seed 8 correct / stable, EMPTY prereq-gap lists (the
  soil is closed).
- **Twin runs:** byte-identical (run identity `9ef49517b1430f8a`,
  final store identity `e3e693b1a83c71a6`; sha256
  `d9443d9cd673d79db8e84d09ab5a0437bdba853184d0c31888b0a624cfd61505`
  on both twins' codeX-S04).
- **Script hash:** `8c511586bbab22fc` (51 turns; letters S2
  `SSUULSSSUULSSSSSS`, S3 `SSSSSSSSFTSSSHHHS`, S4
  `SSSSSSSSSSSSHHHSS`).

### Deviations recorded (pre-reg corrections, the mechanism's
referee; never an edit of the mechanism or the frozen bytes)

- **D-e6s(a) — the frozen c0 structural contract folds the six
  record clauses into the two concept lessons.** The c0 check
  (tools/bandgen/spec.py) admits a band owning EXACTLY its
  concept lessons + theorem facts: a theorem's parts must be band
  concept-lesson slugs, and `new_fact_ids` must equal the band
  lesson+theorem set. The six pre-registered standalone record
  lemmas (seed-shadow, parity-pattern, divisibility-law,
  golden-power, lucas-shadow, below-zero, recip-89, page-names —
  the stage A-2 11-fact accounting: 2 concepts + 2 lessons + 6
  clauses + 1 theorem) therefore FOLD INTO the two folded lesson
  bytes, and `theorem:seed-census-filed` takes the STRICT TWO-PART
  set (seed-period-def + off-line-seed-def), NOT the pre-
  registered three-part set (the seed-shadow clause dropped as a
  part). Recorded as a pre-reg amendment; the clause "stands
  beside, not inside" is preserved in spirit (the record bytes
  live in the lessons' bytes; the drills re-fire them).
- **D-e6s(b) — the store-global mastery event-id dedupe (42, not
  47).** Mastery event ids are store-global `(concept,
  session, turn)` and dedupe ACROSS bands: re-executing a
  question at a coordinate a prior band already recorded
  OVERWRITES the existing assertion and produces NO new event.
  The naive 51 − 4 = 47 over-counts by 5 (carried queue/census
  coordinates colliding with S12/S19/S20/S21/S31). Only
  NEW-concept events (seed-period, off-line-seed) + genuinely-new
  coordinate events land. P8 asserts the mechanism's 42, never
  the hand's 47.
- **D-e6s(c) — the width-4000 FROZEN formatting note.** The
  folded S32 lesson literals (up to ~1900 chars) exceed the
  house width-1000 pformat wrap and split into implicit
  string-concatenation (ISC004). The S32 FROZEN pformat uses
  width 4000 so the literals stay single-line; the VALUES are
  byte-identical (the frozen bytes are the store content, not the
  source layout) — no deviation of any frozen value.

### The stage A-2 fact accounting, resolved

The "11 facts" of stage A-2 (2 concepts + 2 lessons + 6 clauses +
1 theorem) resolves under the frozen c0 contract to **3 store
facts** (2 folded lessons + 1 theorem) — the same 3-of-5
convention the S21 band used (the store holds the teaching; the
record clauses live folded in the lesson bytes and re-fire as
drills). The page's wordings ARE woven into the two folded
lessons (the fibonacci sequence, the golden ratio, the letter
phi, the lucas numbers, "the next number is found by adding up
the two numbers before it", "the bigger the pair, the closer the
approximation"). The page's off-line records (1/89 decimal
shadow, the lucas tail values, the below-zero sign law, the page
names) are declared, never filed: the band adds NO new decimals to
the floor (offline_watch empty; the one over eighty-nine is the
ceiling's decimal shadow, declared in the lesson byte, its digits
never on line).

### Build artifacts

- Modules: `src/kainos/tutor/e636.py` (FROZEN, 9/9 hermetic),
  `src/kainos/tutor/brainstem.py` (the S32 concept + policy
  splices, the W_S32_1..3 walls), `tools/bandgen/reflib.py` (the
  S32 reference re-walks).
- Spec + control: `bands/spec-e6.36.json` (51 turns; the four
  filing turns carry the `cite` for `seed-census-filed` — the
  control fills `theorem_allowed` from cites only); the control
  table is the frozen FROZEN source (c0-c9 CLEAN, exit 0, twin).
- Tests: `tests/tutor/test_e636.py` (18 tests, the S31 mirror);
  runner contract 50 -> 51 experiments, `PASS  e6.36`.
- The 11-family (touched boards) is the lucas shadow of the TWIN
  line which this floor does not build: masked composites (33/44/
  55/66/77) restore the shadows on census — declared, not built.

COURSE E is COMPLETE. The owner's seeded fibonacci lesson stands
on the floor: the seeded line (S31) reads the constants off the
sum line's skeleton, and the seed census (S32, this band) tells
the line's own residue story in the page's wordings — the
skeleton's pisano count with its one shadow, the value story of
the constants off the floor, and every off-line decimal declared,
never filed.
