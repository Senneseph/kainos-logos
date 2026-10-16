# PRIMES-AND-SQUARES COURSE — RESEARCH (pre-registered, 2026-08-25)

Owner-directed, 2026-08-25: "another one about for rules about
primes and squares — everything in this category. There is some
especially rich material that give us constraints on things and
even an open conjecture that says 'yeah, there might be primes
between every consecutive perfect square'." Grounded in the
store's OWN BYTES (the S20 final store
`results/phase-6/e6.24-run1/codeX-S04.json`, 1823 assertions,
identity `e84381407e1dba64`, line 0..84) plus computation
verified 2026-08-25, plus the external sources cited per
claim (the conjectures' statements and status). The store
speaks, not the hand.

## D1 — The owner's brief (as given)

> Another one about for rules about primes and squares —
> everything in this category. There is some especially rich
> material that give us constraints on things and even an open
> conjecture that says "yeah, there might be primes between
> every consecutive perfect square".

## D0 — Scope ruling

- TWO bands: **S26 = E6.30 "the square rules"** (the square
  arithmetic of primes on the line: the residual rules, the
  two-square fact, the depth rule) and **S27 = E6.31 "the
  square-gap conjecture"** (the gap census, the two open
  conjectures filed as records, the root-scale non-closure
  wall). Reserved slots; build order is the owner's call; each
  band seeds from its predecessor's final store in the chain.
- NOT a lot of the declared FUNDAMENTALS queue (the queue
  stands exactly as declared — `theorem:queue-declared`
  byte-intact, P5 on the gate) and NOT a new island. It is,
  however, the course with the DEEPEST connection to the
  closed Riemann island: the square gap at height n² is two
  roots wide, and the condition the island holds open gives
  errors of the root-LOG scale — the course's signature wall
  (W-S27-1) says the condition does NOT close the square-gap
  question, deepening W-S12-4 ("the condition does not close
  the condition") into this category.
- **The two open conjectures, stated exactly (sources:
  Wikipedia/MathWorld/OEIS, checked 2026-08-25):**
  1. **Legendre's conjecture** (Legendre, 1798; one of
     Landau's problems, 1912; OPEN): for every positive
     integer n, a prime p with n² < p < (n+1)². Verified
     computationally up to 7·10^13 (a 2024 computation — off
     the line, declared, not built). This is the owner's
     "there might be primes between every consecutive perfect
     square."
  2. **Brocard's conjecture** (Brocard, 1904; OPEN as of
     2025): for every n ≥ 2 with p_n ≥ 3, at least four
     primes strictly between (p_n)² and (p_{n+1})² — BETWEEN
     CONSECUTIVE PRIME SQUARES (not all integer squares — the
     statement's exact form, checked: the n = 1 row, between
     4 and 9, holds only 5, 7 — the declared exception).
  - **The RH implication, checked and REFUSED:** the Riemann
    condition implies prime gaps of order √p·log p — a WIDER
    bound than the square-gap width 2√p for large p. At
    height x = n² the conditional error is √x·log x =
    2n·log n while the gap is only 2n + 1 wide: the error
    swallows the gap. **Legendre remains open EVEN UNDER the
    condition** — the course teaches this as the flagship
    wall's content, verified by the algebra above.
- **Declared, not built** (the category's honest boundary):
  Oppermann's and Andrica's conjectures (the neighboring gap
  statements — one ledger line each, declared); Brocard's
  n!+1 = m² problem (off the line: the factorials outrun 84 at
  n = 5 — 121); Dirichlet's progression theorem (the
  store's `chebotarev`/`tower-*` soil already declares the
  splitting machinery — the infinitude lives past the line,
  cross-referenced, not re-built); the square-root scale's
  unconditional refinements (PNT-in-short-intervals
  territory — past the line).

## D2 — Grounded census (the seed's own bytes + verified math)

### (a) Soil the store already holds (mastery from the seed's
mastery-event bytes, K = 4)

| concept | state | correct | the byte (abridged) |
|---------|-------|---------|---------------------|
| `mod4-split` | **stable** | 10 | the primes split mod 4 — the store's census word for the two-square territory |
| `mod4minusone` | (lemma, stable territory) | — | **"x squared plus one equals zero modulo an odd prime q has a solution exactly when q is one modulo four, and it feeds the tower …"** — the two-square GATE fact is ALREADY on the line (probe-verbatim) |
| `gaussian-int` | **stable** | 7 | the savant's Z[i] layer — the norm a² + b² is exactly the two-square register |
| `adjoin-i` | practicing | 1 | (gap `[disc-rd]` — the savant chain; **deliberately NOT a prereq of these bands**: the course files the elementary facts on the stable soil and cross-references the savant layer) |
| `prime-count` | stable | 15 | the 23 primes on the line |
| `first-divisor` | stable | 36 | the factor chains of the line |
| `valuation` | stable | 6 | **"the valuation, the p-adic depth … the highest power of p that divides it"** — the store already holds the DEPTH word the depth rule speaks in |
| `decision-question` | stable | 7 | the yes/no discipline the open-declared concept builds on |
| `shape-square` | stable | 5 | the geometric square (the category's own shape, already a concept) |
| `grid-lattice` | stable | 10 | the lattice soil the two-square fact draws on |

Also in the seed, carried byte-identical (P6): the
`criterion-gap` theorem byte ("the best error term in my
store, of order x times e to the minus c times the square root
of log x, does not meet the scale the equivalence demands, x
to the one-half plus epsilon … the square-root improvement is
the missing ingredient") and the `rh-bound-scale` conditioned
byte (the root-SCALE of the conditioned gap) — the two
scale-facts W-S27-1 references (cited, not asserted).

### (b) Verified math (computed 2026-08-25)

**The squares and the gap ladder on the line:** squares on
0..84: 0, 1, 4, 9, 16, 25, 36, 49, 64, 81. The gap
(k+1)² − k² = 2k + 1 — the ODD ladder: 1, 3, 5, 7, 9, 11,
13, 15, 17 (k = 0..8). The square gap at height n² is two
roots wide (2n + 1) — the category's own scale.

**The Legendre census on the line (EVERY on-line gap holds a
prime — verified; the partial last gap at the ceiling):**

| gap (n², (n+1)²) | primes within | count |
|------------------|---------------|-------|
| 1–4 | 2, 3 | 2 |
| 4–9 | 5, 7 | 2 |
| 9–16 | 11, 13 | 2 |
| 16–25 | 17, 19, 23 | 3 |
| 25–36 | 29, 31 | 2 |
| 36–49 | 37, 41, 43, 47 | 4 |
| 49–64 | 53, 59, 61 | 3 |
| 64–81 | 67, 71, 73, 79 | 4 |
| 81–100 (partial) | **83 on the line; 89, 97 off the line** | 3 (1 on-line) |

Counts [2,2,2,3,2,4,3,4,3]; **minimum 2**, at the gaps 1–4,
4–9, 9–16, 25–36. The 81–100 gap is the boundary: 83 stands
on the line, 89 and 97 off it — the 89 a third time the
declared ceiling byte (after the Riemann island's
declaration and the Fibonacci course's F(11)).

**The Brocard census (prime-SQUARE gaps, the exact statement's
terms):**

| gap ((p_n)², (p_{n+1})²) | primes | count |
|--------------------------|--------|-------|
| 4–9 (n = 1, p = 2 — the declared exception) | 5, 7 | 2 |
| 9–25 (n = 2, p = 3) | 11, 13, 17, 19, 23 | 5 |
| 25–49 (n = 3, p = 5) | 29, 31, 37, 41, 43, 47 | 6 |
| 49–121 (n = 4, p = 7) | 8 on the line (53..83) + 7 off (89, 97, 101, 103, 107, 109, 113) | 15 |

The four-prime claim holds on the line at every n ≥ 2 on-line
row (5, 6, 15 — all ≥ 4); the row at n = 5 (121–169) starts
off the line entirely (127 first) — declared territory.

**The residual rules (verified, zero exceptions on the line):**

- The square of every odd prime on the line (22 primes) is
  **1 mod 8** — and 1 mod 4. No other residue occurs.
  (Constraint: an odd square that is not 1 mod 8 is not an
  odd prime's square on the line.)
- **The two-square census** (Fermat's theorem's on-line
  instances, all verified): ten primes are sums of two
  squares — 2 = 1²+1², 5 = 1²+2², 13 = 2²+3², 17 = 1²+4²,
  29 = 2²+5², 37 = 1²+6², 41 = 4²+5², 53 = 2²+7², 61 =
  5²+6², 73 = 3²+8² — each with EXACTLY ONE representation
  up to order (uniqueness verified on the line; the theorem
  names it up to order and sign, 1640 Fermat, Euler's proof —
  a settled classical fact, filed as a fact of record with the
  on-line census as the verifying evidence, the store's
  epistemic register); and the THIRTEEN primes three mod four
  (3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83) are NONE
  of them a sum of two squares (verified).
- **The depth rule** (the category's richest constraint, in
  the store's own `valuation` word): a number that carries a
  prime three mod four at ODD depth (odd p-adic depth) is NOT
  a sum of two squares — ZERO violations on the line (verified
  over all n ≤ 84); conversely the 36 numbers on the line that
  ARE sums of two squares (2, 4, 5, 8, 9, 10, 13, 16, 17, 18,
  20, 25, 26, 29, 32, 34, 36, 37, 40, 41, 45, 49, 50, 52, 53,
  58, 61, 64, 65, 68, 72, 73, 74, 80, 81, 82) are exactly the
  ones whose three-mod-four depths are all even (verified).
  (The general theorem — a settled classical fact, filed as a
  fact of record with the on-line census as evidence.)
- **The 25-square cross-course weld (verified):** F(n)² +
  F(n+1)² = F(2n+1) (the Fibonacci course's square-sum
  identity) is the same register: the squares of consecutive
  SUM terms land on the sum line. Cross-course citation only
  (the Fibonacci course files it; this course's square
  register receives it as a declared kin).

### (c) The status-surface pattern (how the store holds an open
conjecture — the pattern the two new conjecture facts follow;
the seed's own two precedent facts, probe-verbatim)

`conjecture:riemann`'s context: `conjecture_status: open`,
`source_role: declared-source`, `essence: "the target itself —
believed, not known; a status surface, never a premise"`,
`source_lines: "the conjecture (1859) — the target of the
RH-TRACK"`. `conjecture:erdosguess`'s context:
`conjecture_status: falsified` (the fifth summit-shape
instance — the store already holds a conjecture that turned
out FALSE, filed as a record), `source_role: declared-source`.
The pattern: an open conjecture is a FACT of kind
`conjecture` with its status declared — the store holds the
statement and its status, never the proof; a band may CITE a
conjecture of record (as the condition is cited) but never
REASON UNDER it (the status-surface discipline, W-S27-2).

## D3 — What the course teaches (four relationships)

- **R1 — the gap ladder.** Consecutive squares are two roots
  apart (2n + 1 at n²): the odd ladder 3, 5, 7, …, 17 on the
  line. Every gap on the line holds a prime (the verified
  census; minimum two), and the last gap is the boundary
  (83 on, 89/97 off). The Legendre question is thus verified
  ON THE LINE and OPEN PAST IT — filed as a conjecture of
  record, believed, not known, one of Landau's problems.
- **R2 — the residual rules (the constraints).** Odd prime
  squares are one mod eight (all 22, zero exceptions — the
  store's mod-4 census word at the doubled modulus); the gate
  fact the store already holds (`mod4minusone`: x² + 1 = 0
  mod q solvable exactly when q is one mod four) is drilled as
  the two-square territory's threshold; and the TWO-SQUARE
  FACT (Fermat, 1640 — settled, filed as a fact of record
  with the on-line census as evidence): exactly the primes
  one mod four (and two) are sums of two squares, unique up
  to order; the DEPTH RULE in the store's own valuation word:
  a three-mod-four prime at odd depth kills the
  representation (the richest constraint in the category — it
  classifies the 36 representable numbers on the line
  exactly).
- **R3 — the two open conjectures, filed.** Legendre
  (1798: a prime between every pair of consecutive squares —
  every on-line instance verified, the question open past the
  line; computationally verified to 7·10^13 — off the line,
  declared) and Brocard (1904: at least four primes between
  consecutive PRIME squares for n ≥ 2 — the on-line rows 5, 6,
  15 verify the four-prime claim, the n = 1 row the declared
  exception). Both filed as `conjecture` facts of record
  (the store's own status-surface pattern — the riemann and
  erdosguess precedents), the course's teaching of how the
  store holds an open question: the statement and its status,
  never the proof; cited, never reasoned under.
- **R4 — the condition does not close the category (the
  flagship wall).** The store's conditioned error scale (the
  root-LOG scale, `rh-bound-scale`/`criterion-gap` bytes) is
  WIDER than the square-gap width (two roots): at height n²
  the conditional error 2n·log n swallows the gap 2n + 1.
  Legendre is open EVEN UNDER the condition — deepening
  W-S12-4 into the square category. The course's deepest
  lesson for the infant: a strong condition can still be too
  wide for the question; the store names the scale it holds
  (root log), the scale the gap has (root), and the gap
  between them, as the reason the question stays open under
  the condition it names.

## D4 — The new / carry fact set (stage B target)

### Band S26 — "the square rules" (E6.30): **6 new facts**
(2 concepts + 2 lessons + 1 lemma + 1 theorem)

1. Concept **`odd-square-rule`** (domain `soil` candidate, band
   `college-1`; prereqs `('mod4-split', 'composite')` —
   candidate; both stable):
   - Lesson **`odd-square-rule-def`** (candidate byte,
     unconditional, house voice):
     > the odd square rule of my line: square an odd prime and
     > its residue is one, mod eight — all twenty-two odd
     > primes on my line give one, and zero give anything
     > else; the same rule at the halved modulus gives one
     > mod four; a square that is not one mod eight is not an
     > odd prime's square on my line; at the line end
     > eighty-four
2. Concept **`two-square`** (prereqs `('mod4-split',
   'gaussian-int')` — candidate; both stable, verified):
   - Lesson **`two-square-def`** (candidate byte):
     > the two-square fact of my line: a prime is a sum of
     > two squares exactly when it is two or one mod four —
     > on my line the ten such primes each write one way up
     > to order, from five is one squared plus two squared to
     > seventy-three is three squared plus eight squared, and
     > the thirteen primes three mod four write none; and the
     > depth rule in my line's own valuation word: a prime
     > three mod four at odd depth kills the representation,
     > and the thirty-six representable numbers on my line
     > are exactly the ones whose three-mod-four depths are
     > all even; at the line end eighty-four
3. Lemma **`lemma:odd-depth-rule`** (a composed fact of
   record — the depth rule as its own census statement):
   - Candidate byte:
     > the odd depth rule of my line: no number on my line
     > that carries a prime three mod four at odd depth is a
     > sum of two squares — verified over all of my line,
     > zero violations; and the representable numbers are
     > exactly the ones whose three-mod-four depths are all
     > even, thirty-six in number; at the line end
     > eighty-four
4. Theorem **`theorem:two-square-filed`** (parts exactly
   `('odd-square-rule-def', 'two-square-def')` — strict
   two-part set):
   - Candidate statement:
     > the two-square fact of my store is filed of record:
     > the odd prime's square is one mod eight, all of them
     > on my line; the primes one mod four and two are
     > exactly the sums of two squares, unique up to order,
     > and the depth rule holds at every number my line
     > names — a settled fact of record, its proof declared
     > and not executed on the line, its census verified
     > every instance on my line; at the line end
     > eighty-four

### Band S27 — "the square-gap conjecture" (E6.31): **7 new
facts** (2 concepts + 2 lessons + 2 conjecture facts + 1
theorem — the largest band of the three courses, justified by
the two open conjectures it files)

1. Concept **`square-gap`** (prereqs `('prime-count',
   'first-divisor')` — candidate; both stable, verified):
   - Lesson **`square-gap-def`** (candidate byte):
     > the square gap of my line: consecutive squares are two
     > roots apart, the gap between the square of n and the
     > next is two n plus one, the odd ladder three five
     > seven to seventeen on my line; every gap my line gives
     > holds a prime — the smallest holds two, and the last
     > gap, eighty-one to one hundred, holds the eighty-three
     > on the line with the eighty-nine and the ninety-seven
     > off it; the question of a prime in every square gap is
     > verified on my line and open past it; at the line end
     > eighty-four
2. Concept **`open-declared`** (prereqs `('decision-
   question', 'prime-count')` — candidate; both stable,
   verified): the register by which the store holds an open
   conjecture (generalizing the seed's two precedent
   facts):
   - Lesson **`open-declared-def`** (candidate byte):
     > an open conjecture of record in my store is a status
     > surface, never a premise: the statement is held with
     > its status declared, believed and not known, and the
     > source declared; my census verifies every instance
     > my line names, and the verification rests at my line
     > end; a band that reasons under an open conjecture as
     > if it were fact is a misread this store punishes —
     > cited, never assumed, at the line end eighty-four
3. Conjecture fact **`conjecture:legendre`** (following the
   seed's precedent context exactly):
   - Context candidate: `kind: conjecture`, concept
     `square-gap`, `conjecture_status: open`, `source_role:
     declared-source`, `depends: []`, `source_lines: "the
     conjecture (1798) — one of Landau's problems (1912)"`,
     `essence: "the square gap of record — believed, not
     known; a status surface, never a premise; verified on
     my line, open past it"`.
   - Object candidate (the statement, store voice):
     > a prime stands between every pair of consecutive
     > squares: between the square of n and the square of
     > n plus one there is a prime, for every n above zero —
     > every such gap my line names verified, the question
     > open past my line end, at the line end eighty-four
4. Conjecture fact **`conjecture:brocard`**:
   - Context candidate: `kind: conjecture`, concept
     `square-gap`, `conjecture_status: open`, `source_role:
     declared-source`, `depends: []`, `source_lines: "the
     conjecture (1904) — between the squares of consecutive
     primes"`, `essence: "the four-prime square gap of
     record — believed, not known; a status surface, never a
     premise; the on-line rows five, six and fifteen
     verify it, the exception row two, known"`.
   - Object candidate (the statement, store voice):
     > at least four primes stand between the square of a
     > prime and the square of the next prime, for every
     > prime above two — the on-line rows five, six and
     > fifteen verify the four, the row at four to nine
     > holds the two as the declared exception, and the row
     > past my line end is open, at the line end
     > eighty-four
5. Theorem **`theorem:square-gap-open-filed`** (parts
   exactly `('square-gap-def', 'open-declared-def')` —
   strict two-part set):
   - Candidate statement:
     > the square-gap line of my store is filed of record as
     > open: the gaps my line names all hold a prime, the
     > smallest two, and the question of every gap is
     > verified on my line and filed open — one of the
     > Landau problems, believed and not known; and the
     > condition my store holds open does not close it: at
     > the height of the square the conditional error is the
     > root-log scale, wider than the gap's two roots, so
     > the error swallows the gap, and the one-prime
     > question stands open under the condition — filed
     > open, at the line end eighty-four

### Carry surfaces (byte-identical to the seed — P6)

The `mod4minusone` gate byte (the S26 signature carry), the
`mod4-split` byte, the `valuation-def` byte, the `shape-
square` / `grid-lattice` soil, the `criterion-gap` theorem
byte and the `rh-bound-scale` conditioned byte (the two
scale-facts W-S27-1 and the filed theorem cite), the
`conjecture:riemann` byte (carried through S27 as the
pattern's first instance), the 89/97 declared-off-line
territory (cited, not re-asserted).

### Off-script standing check (S27's identity)

"between the eighty-one and the one hundred, which primes
does my line name?" → the S27 byte: "the eighty-three — the
eighty-nine and the ninety-seven stand off-line as my line
already declared them; the gap's census rests where my line
ends" (in `spec["offscript]`; the in-script coordinate may
dedupe its event, D-e6o(a)).

## D5 — The walls (W-S26-1..3, W-S27-1..3)

- **W-S26-1 — THE ONE-MOD-EIGHT CENSUS:**
  > the wall is the territory of the odd square's residue:
  > every odd prime's square on my line is one mod eight —
  > all twenty-two, zero exceptions — and a square claimed
  > at any other odd residue is a misread the census
  > refutes; at the line end 84
- **W-S26-2 — THE UNIQUENESS DISCIPLINE:**
  > the wall is the territory of the second representation:
  > a prime one mod four on my line writes its two squares
  > one way, up to order — a second representation on my
  > line is a misread the census refutes, and the unique up
  > to order wording is the word the fact holds; at the
  > line end 84
- **W-S26-3 — THE DEPTH REGISTER:**
  > the wall is the territory of the depth word: the depth
  > rule speaks my line's own valuation word — a prime three
  > mod four at odd depth, a representation that is not —
  > and a representability claimed past the depth rule is a
  > misread the zero-violation census refutes; at the line
  > end 84
- **W-S27-1 — THE NON-CLOSURE (the course's flagship wall,
  deepening W-S12-4):**
  > the wall is the territory of the condition over the
  > square gap: my condition does not close the square gap —
  > at the height of the square the conditional error is the
  > root-log scale, and the gap between consecutive squares
  > is only two roots wide; the error swallows the gap, and
  > the one-prime question stands open even under the
  > condition, at the line end 84
- **W-S27-2 — THE STATUS-SURFACE WALL:**
  > the wall is the territory of the conjecture as premise:
  > a conjecture of record is a status surface, never a
  > premise — the legendre and the brocard are believed,
  > not known, and a band that reasons under them as if
  > they were fact is a misread the store punishes; at the
  > line end 84
- **W-S27-3 — THE PARTIAL-GAP WALL:**
  > the wall is the territory of the witness past my line
  > end: the last gap my line names, eighty-one to one
  > hundred, holds the eighty-three on the line, and the
  > eighty-nine and the ninety-seven stand off it as my line
  > already declared them — the verification rests at my
  > line end, and no witness past it enters the floor; at
  > the line end 84

Candidate wall probes (new S26/S27 grammar): "which odd
squares does my line claim at a residue other than one mod
eight?" (W-S26-1), "can a one-mod-four prime on my line
write two different two-square sums?" (W-S26-2), "can a
number at odd three-mod-four depth be a sum of two squares?"
(W-S26-3), "does my condition give a prime in every square
gap?" (W-S27-1), "may a band of my store reason under the
legendre as if it were fact?" (W-S27-2), "which witnesses
does my line hold in the last square gap?" (W-S27-3). Every
wall names its territory AND the line end 84; the S04
re-probe of W-S26-1 (S26) / W-S27-1 (S27) re-emits the same
byte (the S20 pattern).

## D6 — Band shape (stage B pre-reg)

- **Sessions/experiments:** S26 = E6.30 "the square rules",
  S27 = E6.31 "the square-gap conjecture" — the 54th and
  55th experiments. Modules `e630.py`/`e631.py`, specs
  `spec-e6.30.json`/`spec-e6.31.json`, tests
  `test_e630.py`/`test_e631.py`, runner 48 → 54.
- Seeds: S26 from S25's final (or the S20 final if the owner
  builds these ahead in the chain — every claim above is
  verified against the S20 final, the control re-referees on
  the actual seed at freeze).
- 3 sessions × 17 turns each. S26: S02 carries (mod4-split,
  mod4minusone, valuation-def, shape-square) + `odd-square-
  rule` (two gaps, teach, the mod-8 census bed over the 22
  odd primes + the "not one mod eight" refusal) + `two-
  square` (two gaps, teach, the ten-representation bed, the
  thirteen-none bed). S03: the depth-rule drill as PAIRED beds on the
  verified lists (refusers at odd three-mod-four depth:
  3, 6, 12, 15 — all v3 = 1, none a sum of two squares;
  57 = 3·19 and 69 = 3·23 — the other three-mod-four
  primes at odd depth; representables that carry a 3-PART
  AT EVEN depth against them: 18 = 3² + 3² and 45 = 6² +
  3², both v3 = 2) — the walk byte-by-byte over the 36
  representables and the refusers, the control re-referees
  — then the odd-depth-rule lemma, the scaffold, the
  derive, the walls, the filed state. S04: the wrap. S27: S02 carries
  (conjecture:riemann as the register's first instance, the
  criterion-gap + rh-bound-scale scale bytes, the 89/97
  off-line territory) + `square-gap` (two gaps, teach, the
  gap-ladder bed 3,5,7..17, the census bed [2,2,2,3,2,4,3,4],
  the 83/89/97 partial-gap bed) + `open-declared` (two gaps,
  teach, the status-surface byte over the riemann precedent +
  the erdosguess falsified instance). S03: the Legendre
  filing (the conjecture fact + its statement byte + the
  verified-on-line census bed), the Brocard filing (the
  conjecture fact + the rows 5/6/15 + the exception row 2),
  the non-closure drill (the 2n·log n vs 2n+1 scale byte —
  the W-S27-1 territory walked as a drill before its wall),
  the scaffold, the derive, the walls, the filed state.
  S04: the wrap.
- 4 pre-lesson gaps (two per concept), 2 teaches, 2
  conjecture filings, 1 scaffold, 1 derive, ~18 beds, 1
  off-script per band.
- **Mastery pre-reg (the soil census, D-e6p style, the
  store referees):** all SIX new concepts pre-registered
  **STABLE** — `odd-square-rule` ← `mod4-split` (stable 10)
  + `composite` (stable 7); `two-square` ← `mod4-split`
  (stable 10) + `gaussian-int` (stable 7); `square-gap` ←
  `prime-count` (stable 15) + `first-divisor` (stable 36);
  `open-declared` ← `decision-question` (stable 7) +
  `prime-count` (stable 15) — every prereq verified stable
  from the seed's mastery-event bytes; the band drills
  supply the ≥ 4 correct derivations. **Deliberate design
  decision (recorded):** `adjoin-i` (practicing, gap
  `[disc-rd]` — the savant chain) is NOT a prereq of any of
  the six bands' concepts: the two-square fact files on the
  STABLE elementary soil (`mod4-split` + `gaussian-int`), and
  the savant layer (adjoin-i, the norm facts) is a cross-
  reference in the statement's context, not a mastery edge —
  the band ends stable where it ends on stable soil.
- **P5 gate re-derivation (full width):**
  1. no new line facts; line stays 0..84;
  2. the 89/97 declared-off-line bytes byte-identical
     (cited, never re-asserted — no new store assertion about
     89 or 97);
  3. `conjecture:riemann` byte-identical + `open` +
     `declared-source` (the pattern's first instance
     untouched); NO bare `theorem:riemann` (the discovery-
     candidate set, full width);
  4. `theorem:queue-declared` byte-identical;
  5. the two new conjecture facts on the gate: `kind:
     conjecture`, `conjecture_status: open`, `source_role:
     declared-source`, both CITED-ONLY (no mastery chain
     reasons under them — W-S27-2 enforced);
  6. the gap census re-walked on the gate: [2,2,2,3,2,4,3,4]
     + the 83/89/97 partial row; the Brocard rows (2 excepted,
     5, 6, 15); the mod-8 census (22 primes, all one); the
     two-square census (10/10 representable, unique up to
     order; 13/13 non-representable); the depth rule (zero
     violations; the 36 representables exactly the even-depth
     set) — the mechanism's bytes are the referee, a
     violation is a recorded deviation, never an edit;
  7. no-new-decimals: no off-line digit string in any new
     lesson/wall/bed/answer (89, 97, 101..113 named only as
     declared off-line; 7·10^13 appears ONLY in the
     legendre context as a declared external verification —
     the control's offline-watch checks it stays in the
     context, never in a lesson/wall byte);
  8. marker posture: the new facts are UNCONDITIONAL — P0
     denies the conditional marker on them (the S20
     discipline; the non-closure statement talks ABOUT the
     condition the way `s12-selved` does in the seed —
     conditioned bytes stay conditioned, and none of the new
     ones is one).
- Fact anatomy: S26 final = S25 final (or S20 final) + 6
  facts + N events; S27 final = S26 final + 7 facts + N
  events (control referees; dedupes per D-e6o(a)).

## D7 — Open items for the control run

1. The scaffold/missing-parts bytes (S26: predicted "i have
   not been taught the two-square-def — the rule for two-
   square-filed needs it before i can put it together"; S27:
   the open-declared-def part; the mechanism referees).
2. The exact event counts and the drill census (which concept
   each census bed +1s; the two conjecture filings' event
   coordinates).
3. The letter strings (the control's domain sequences are
   the freeze).
4. The S26 depth-rule paired beds (representable-refuser
   walk — the control walks the verified 36 + refuser lists
   at the fixed seed).
5. Whether `conjecture:` kind facts accept the `concept:`
   context key pointing at a NEW concept (`square-gap`) —
   the seed precedent (riemann → concept `riemann`) says
   yes; the control's census shape-checks it.
6. The 7·10^13 external-verification string: its exact
   placement (context `source_lines`? `essence`?) —
   candidate: `source_lines: "the conjecture (1798) — one of
   Landau's problems (1912); verified by computation to 7·
   10^13, off the line, declared"`. The control places it
   where offline-watch keeps it out of the floor's values.
7. The domain string for the new concepts (`soil`
   candidate; the control's domain map referees).

## D8 — Success criteria / stage B next steps

Stage B builds S26 → S27 in the bandgen way (mirroring S20):
brainstem modules (the S26/S27 concepts, the grammar modes
including the two conjecture-filing turns, `_policy_
savant2x`, the walls) → reflib refs → specs → control c0–c9
CLEAN → `e630.py`/`e631.py` (FROZEN from the control
tables) → tests → runner → official gate (targeted + twin
byte-identical + full) → close-out (experiments §E6.30/
§E6.31, roadmap, the islands README's Riemann-status-line
annotation if the owner wants the cross-reference,
e3.7.json, OP #157, SESSION-HANDOFF, wiki).

Success: the infant holds every constraint in the category —
the odd squares one mod eight, the two-square fact with its
on-line census and its depth rule in the store's own
valuation word — and holds the two open conjectures the way
the store holds openness: Legendre and Brocard filed as
status surfaces (believed, not known; every on-line
instance verified; the verification rests at the line end),
cited, never reasoned under — while the flagship wall says
the course's deepest word: the condition does not close the
square gap, because at the height of the square the
condition's error is wider than the gap it is meant to
fill.
