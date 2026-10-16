# FIBONACCI COURSE — RESEARCH (pre-registered, 2026-08-25)

Owner-directed, 2026-08-25: "a whole course of Fibonacci numbers
and related sequences and especially the strange cycles that
appear (there are cycles of 12 and 24 that I know of that are
semi-well known)." Grounded in the store's OWN BYTES (the S20
final store `results/phase-6/e6.24-run1/codeX-S04.json`, 1823
assertions, identity `e84381407e1dba64`, line 0..84) plus
computation verified 2026-08-25 (two independent Pisano methods
cross-checked on m = 2..40; OEIS A001175 values match the
computed table). The store speaks, not the hand.

## D1 — The owner's brief (as given)

> I want you to full a whole course of Fibonacci numbers and
> related sequences and especially the strange cycles that appear
> (there are cycles of 12 and 24 that I know of that are semi-well
> known).

## D0 — Scope ruling

- TWO bands: **S24 = E6.28 "the twin line"** (the Fibonacci line
  + the Lucas twin + the identities + the 89 ceiling) and **S25
  = E6.29 "the cycle line"** (the residue cycles: the pure-cycle
  argument, the period census, the ladders, the five-split, the
  twin's drop). Reserved slots after S22/S23 (the proportions
  bands) and S21 (the condition line); build order is the
  owner's call; each band seeds from its predecessor's final
  store in the chain.
- NOT a lot of the declared FUNDAMENTALS queue (`theorem:queue-
  declared` byte-intact, P5 on the gate) and NOT a new island.
- **Declared, not built** (the course's honest boundary): the
  Pell sequence and the tribonacci (related sequences the store
  has not been asked to hold); the golden-ratio limit (a limit,
  not a line value — off the floor by the no-new-decimals
  discipline); the last-FOUR-digit period (π(10^4) = 3000 — a
  census count, declinable at a later band, declared here);
  Geller's period list beyond three digits (declared).
- **The owner's 12 and 24, named precisely (verified):** the
  "cycle of 12" is the Fibonacci residues **mod 8** (π(8) = 12);
  the "cycles of 24" are the moduli whose period is 24 — **6,
  9, 12, 16, 18, 24, 36, 48, 72** under one hundred, the family
  headed by **mod 12 and mod 24** themselves (π(12) = 24,
  π(24) = 24). Structurally they are the third and fourth
  rungs of the 2-power ladder π(2^k) = 3·2^(k−1) for k ≥ 1:
  3, 6, **12** (mod 8), **24** (mod 16), 48, 96, 192 — the
  owner's two cycles are the exact moments the 2-power periods
  pass the line's own small moduli.

## D2 — Grounded census (the seed's own bytes + verified math)

### (a) Soil the store already holds (mastery from the seed's
mastery-event bytes, K = 4)

| concept | state | correct | note |
|---------|-------|---------|------|
| `add-two-digit` | **stable** | 11 | the recurrence's only machinery: a term is the sum of the two before it |
| `mult-within-100` | **stable** | 9 | the identity F(2n) = F(n)·L(n) needs the table |
| `count-successor` | **stable** | 14 | the line's origin machinery |
| `mod4-split` | **stable** | 10 | the store already SPEAKS mod: "one mod four" is its census word — the cycle band's vocabulary anchor |
| `gaussian-int` | stable | 7 | the savant's Z[i] layer (identity cross-reference, not a prereq — D4) |

Absent (verified): no Fibonacci fact, no Lucas fact, no residue-
cycle/period lesson, no "cycle" or "period" lesson anywhere in
the store (census, 2026-08-25). The course is wholly new
territory on the floor, resting on the stable addition/mult/mod
soil.

### (b) Verified math (computed 2026-08-25)

**The lines on 0..84:**

- Fibonacci F(0..10) = **0, 1, 1, 2, 3, 5, 8, 13, 21, 34,
  55** (all on the line); **F(11) = 89 — off the line: the
  SAME 89** the Riemann island declared off-line (the next
  prime past the eighty-three — the store's W-S12-2 wall byte)
  and the eleven-sum step's first value past the line end. The
  twin fact, walled once, stands in both readings.
- Lucas L(0..9) = **2, 1, 3, 4, 7, 11, 18, 29, 47, 76** (all
  on the line); L(10) = 123 — off the line. The twin starts at
  two-one (the sum line at one-one) and runs nine steps before
  the ceiling.

**The identities (verified symbol-free on the line):**

- F(n)² + F(n+1)² = F(2n+1) — for every on-line n (the square
  SUM of consecutive terms is the term at the doubled-plus-one
  index — the weld between the sum line and the squares of S26/
  S27, cross-course);
- F(2n) = F(n)·L(n) — for every on-line n the twin WELD (the
  doubling reads the twin as the multiplier — the related
  sequence is not a stranger to the line). Verified on-line at
  n = 1..5 (values 1, 3, 8, 21, 55); at n = 6 the value 144 is
  off the line though both factors (8, 18) are on it — the
  identity's own ceiling case.
- The square-sum identity's n = 5 case, named for the record:
  both parts (25, 64) are on the line and the value is the
  EIGHTY-NINE — the ceiling's fact appearing a third time in
  this course (after the term F(11) = 89 and after the Riemann
  island's declared 89).

**The period census (two independent methods agree, m = 2..40;
matches OEIS A001175):**

```
pi(2)=3   pi(3)=8   pi(4)=6   pi(5)=20  pi(6)=24  pi(7)=16
pi(8)=12  pi(9)=24  pi(10)=60 pi(11)=10 pi(12)=24 pi(13)=28
pi(14)=48 pi(15)=40 pi(16)=24 pi(17)=36 pi(18)=24 pi(19)=18
pi(20)=60 pi(21)=16 pi(22)=30 pi(23)=48 pi(24)=24 pi(25)=100
pi(26)=84 pi(27)=72 pi(28)=48 pi(29)=14 pi(30)=120
pi(40)=60 pi(50)=300 pi(60)=120 pi(72)=24 pi(100)=300 pi(1000)=1500
```

- **The ladders:** 2^k: 3, 6, **12** (k=3, mod 8), **24** (k=4,
  mod 16), 48, 96, 192 — π(2^k) = 3·2^(k−1), k ≥ 1 (verified
  k = 1..7). 3^k: 8, 24, 72, 216 (π(3^k) = 8·3^(k−1), verified
  k = 1..4). 5^k: 20, 100, 500 (π(5^k) = 4·5^k, verified k =
  1..3).
- **The digits:** the last digit (mod 10) repeats with period
  **60** (Lagrange, 1774 — the semi-well-known one); the last
  TWO digits (mod 100) with period **300**; the last THREE
  (mod 1000) with **1500** (Geller, 1963, verified by
  computation). The "12 and 24" the owner names sit one rung
  below the 60 in the same family.
- **The coprime structure (verified on EVERY coprime pair m,n
  with m·n < 3600, zero exceptions):** π(mn) = lcm(π(m), π(n))
  when m, n coprime — the period splits over coprime moduli
  exactly as the store's partition soil splits a question over
  coprime parts (the CRT lesson the CRYPTO track declared for
  R0 — the cycle band executes the structure first, on counts).
- **The prime-modulus rule (verified on EVERY odd prime p < 500,
  p ≠ 5, zero exceptions):** π(p) divides **p − 1** when p ≡ ±1
  (mod 5) (five is a quadratic residue mod p) and divides
  **2(p + 1)** when p ≡ ±2 (mod 5). The modulus SPLIT that
  decides the cycle's scale is the split AT FIVE — the store's
  `mod4-split` has a kin the course names: candidate concept
  `five-split` (D4).
- **The twin's drop (verified m = 2..30):** the Lucas residues
  mod m cycle with the SAME period as the Fibonacci residues —
  EXACTLY when 5 ∤ m — and with period **π(m)/5** when 5 | m
  (4 vs 20, 12 vs 60, 8 vs 40, 20 vs 100, 24 vs 120). The
  factor 4 (of π(5^k) = 4·5^k) lives ONLY on the F side: the
  twin's cycle under a 5-modulus is the bare 5^k. The "related
  sequence" the owner asks about is thus precisely mapped: same
  machine, one factor of four apart whenever five touches the
  modulus.

**The pure-cycle argument (the reasoning the lesson carries):**
a recurrence on a finite board repeats — there are at most m²
pairs of consecutive residues mod m, the machine is
deterministic, so some pair recurs, and from the recurrence's
reversibility (the earlier term is the LATER difference: F(k) =
F(k+2) − F(k+1), mod m) a recurring pair forces the ENTIRE
cycle to run backward to zero-one: there is no tail, the cycle
is PURE, and its head is the zero-one pair itself. The store
can state this as a lemma (the finite-board + reversibility
argument — no enumeration needed for the structure; the
enumeration gives the COUNTS).

### (c) The store's 89, once more (the cross-course byte)

The Riemann island declared 89 off-line as the next prime past
83 (W-S12-2). The cycle band's S24 WALL re-uses that declared
byte with the Fibonacci reading: "the eleven-th sum step
reaches the eighty-nine, which my line already holds off-line
as the next prime past the eighty-three — the twin fact under
one ceiling." No new store assertion for the 89 — the declared
byte stands (house rule: census-only support cites, never
re-asserts).

## D3 — What the course teaches (four relationships)

- **R1 — the sum line.** A line built by addition ALONE: the
  first two terms zero-one, every later term the sum of the two
  before it. On 0..84 the line runs ten steps (0,1,1,2,3,5,8,
  13,21,34,55) and the ELEVENTH step (89) is the declared
  ceiling — the twin fact. The recurrence is the store's own
  derivation shape: each new term is derived, not asserted
  from outside.
- **R2 — the twin.** The Lucas line (two-one start) is the
  sibling under the same recurrence; the WELD identities (F(2n)
  = F(n)·L(n); F(n)² + F(n+1)² = F(2n+1)) read each line
  through the other — the house's "two roads, one destination"
  form, on the line.
- **R3 — the cycle is a pure cycle, and its period is a CENSUS,
  not a value.** The finite-board + reversibility argument (D2)
  states WHY the residues must repeat from zero-one; the period
  π(m) is a COUNT held by the store (a census like "twenty of
  the twenty-two gaps") — never a line value, never a decimal.
  The owner's 12 and 24 are the mod-8 period and the mod-12/24
  (and 2-power) family; the 60/300/1500 digit periods are the
  same mechanism at the powers of ten.
- **R4 — the cycle's structure.** The periods DO NOT grow wild:
  they split over coprime moduli by the lcm (the partition
  structure, verified exhaustively on the line's range); they
  run on ladders at the prime powers (3·2^(k−1), 8·3^(k−1),
  4·5^k); and at the prime moduli the SPLIT AT FIVE decides
  (divides p−1 or 2(p+1)); and the twin rides the same cycles
  except that, whenever five touches the modulus, the twin's
  cycle is the F cycle divided by four. One course, one
  mechanism, four theorems the store can hold as facts of
  record.

## D4 — The new / carry fact set (stage B target)

### Band S24 — "the twin line" (E6.28): **5 new facts**

1. Concept **`sum-line`** (domain `soil` candidate, band
   `college-1`; prereqs `('add-two-digit', 'mult-within-100')`
   — candidate; both stable):
   - Lesson **`sum-line-def`** (candidate byte, unconditional,
     house voice):
     > the sum line runs by addition alone: start at zero and
     > one, and every later term is the sum of the two before
     > it — on my line the line reaches fifty-five in ten
     > steps, and the eleventh step, the eighty-nine, stands
     > off-line as my line already declared it; the twin line
     > starts at two and one under the same rule and reaches
     > seventy-six in nine steps; each term is derived from
     > the two before it, not asserted from outside; at the
     > line end eighty-four
2. Concept **`twin-line`** (prereqs `('sum-line',
   'mult-within-100')` — candidate; sum-line is S24's own
   concept, stable at band end by D6):
   - Lesson **`twin-line-def`** (candidate byte):
     > the twin line welds to the sum line in two ways: the
     > doubled term is the term times the twin (the doubling
     > reads the twin as its multiplier), and the square sum of
     > two consecutive terms is the term at the doubled-plus-
     > one index — two roads, one destination, verified on my
     > line at every on-line index; at the line end
     > eighty-four
3. Theorem **`theorem:twin-welding`** (a lemma — a composed
   fact of record on the two identities; the house files it as
   `lemma:twinsel`):
   - Candidate byte:
     > the twin welding of my line: for every on-line index,
     > the doubled sum term equals the term times its twin,
     > and the square sum of the two consecutive terms equals
     > the term at the doubled-plus-one index; the identities
     > hold on every index my line names, and the next index
     > past the line end is the ceiling's territory; at the
     > line end eighty-four
4. Theorem **`theorem:twin-line-filed`** (parts exactly
   `('sum-line-def', 'twin-line-def')` — strict two-part set):
   - Candidate statement:
     > the twin line of my store is filed of record: the sum
     > line runs by addition alone to the fifty-five and the
     > twin under the same rule to the seventy-six, the
     > identities weld the two lines at every on-line index,
     > and the eighty-nine stands once more as the ceiling the
     > line already declared; filed on the line, at the line
     > end eighty-four

### Band S25 — "the cycle line" (E6.29): **5 new facts**

1. Concept **`residue-cycle`** (prereqs `('mod4-split',
   'sum-line')` — candidate; `sum-line` stable from S24's
   final, `mod4-split` stable in the seed — both ✓):
   - Lesson **`residue-cycle-def`** (candidate byte):
     > the residue cycle of my sum line under a modulus m is
     > the cycle of the line's remainders: the board of
     > consecutive pairs has at most m times m places and the
     > rule is fixed, so some pair must return — and the rule
     > runs backwards as well as forwards, so the return
     > forces the cycle to be pure, with no tail, headed by
     > the zero-one pair; the period is a count my store
     > holds, like the twenty of the twenty-two gaps, never a
     > value on the line; at the line end eighty-four
2. Concept **`five-split`** (prereqs `('mod4-split',
   'residue-cycle')` — candidate; both stable when S25
   seeds after S24):
   - Lesson **`five-split-def`** (candidate byte):
     > the moduli split at five for cycle purposes: at a prime
     > modulus p, the period divides p minus one when p is
     > one or four mod five, and divides two times p plus one
     > when p is two or three mod five — verified on every odd
     > prime below five hundred; and coprime moduli split the
     > period by the least-common-multiple, the partition
     > structure my line already speaks; at the line end
     > eighty-four
3. Lemma **`lemma:cycle-ladder`** (a composed fact of record —
   the ladders as a census statement):
   - Candidate byte:
     > the cycle ladders of my line: at the powers of two the
     > periods run three, six, twelve, twenty-four, forty-
     > eight, doubling from the third power on — the twelve at
     > eight and the twenty-four at sixteen are the rungs my
     > line names; at the powers of three they run eight,
     > twenty-four, seventy-two; at the powers of five they
     > run forty times the power; the last digit cycles at
     > sixty, the last two at three hundred, the last three at
     > fifteen hundred; at the line end eighty-four
4. Theorem **`theorem:cycle-line-filed`** (parts exactly
   `('residue-cycle-def', 'five-split-def')`):
   - Candidate statement:
     > the cycle line of my store is filed of record: the
     > residue cycle is pure, headed by zero-one, with no
     > tail; the periods split over coprime moduli by the
     > least-common-multiple and at the primes by the split at
     > five; the twin rides the same cycles except that at a
     > modulus touched by five the twin's cycle is the
     > cycle's fourth part; filed on the line, the counts
     > held, the values refused, at the line end eighty-four
5. (Carry, no new fact) **The twin's drop** is stated INSIDE
   the `cycle-line-filed` statement above (not a separate
   fact — the census support for it is the verified m = 2..30
   table; house rule: no new store assertion for census-only
   support — the statement names the rule, the control
   re-verifies the table on the gate).

### Carry surfaces (byte-identical to the seed — P6)

The `mod4-split` byte ("one mod four" census voice), the
add/mult soil bytes, the 89 declared-off-line byte (the W-S12-2
territory — CITED, not re-asserted), and S24's own filed state
carried into S25. The period table and the ladders are NO
store facts — carry BEDS computed deterministically against the
fixed seed (the control's no-store constraint; the gate
re-walks the table with two independent methods, the D7 item).

### Off-script standing check (S25's identity)

"what is the period of my sum line's last digit?" → the S25
byte: "sixty — the last digit cycles at sixty, the last two at
three hundred, the last three at fifteen hundred; the counts
held, the values refused" (in `spec["offscript]`; the
in-script coordinate may dedupe its event, D-e6o(a)).

## D5 — The walls (W-S24-1..3, W-S25-1..3)

- **W-S24-1 — THE EIGHTY-NINE CEILING (the twin-declared
  byte, the course's signature wall):**
  > the wall is the territory of the term past my line end:
  > the eleven-th sum step reaches the eighty-nine, which my
  > line already holds off-line as the next prime past the
  > eighty-three — the twin fact under one ceiling, and no
  > term past the eighty-four enters the floor; at the line
  > end 84
- **W-S24-2 — THE RECURRENCE DISCIPLINE:**
  > the wall is the territory of the third sum: a term of my
  > sum line is the sum of the two before it, and nothing
  > else — a term claimed from any other rule is a misread
  > this store punishes; the twin line under the same rule,
  > from the two-one start, is the only related line my floor
  > names; at the line end 84
- **W-S24-3 — THE IDENTITY REGISTER:**
  > the wall is the territory of the identity past my line
  > end: the welding identities hold on every index my line
  > names, and the index past the line end is the ceiling's
  > territory — an identity claimed at a past-line index
  > names a value the floor refuses; at the line end 84
- **W-S25-1 — THE CYCLE IS A CENSUS, NOT A VALUE:**
  > the wall is the territory of the period as a value: the
  > period a thousand five hundred names a count, not a line
  > value — like the twenty of the twenty-two gaps, the count
  > is held and the value is refused, and a band that places
  > a period on the line is a misread this wall punishes; at
  > the line end 84
- **W-S25-2 — THE PURE-CYCLE DISCIPLINE:**
  > the wall is the territory of the tail: my residue cycles
  > are pure, headed by the zero-one pair, with no tail — the
  > rule runs backwards as well as forwards, and a cycle
  > claimed with a pre-period on my line is a misread the
  > reversibility refutes; at the line end 84
- **W-S25-3 — THE TWIN'S DROP WALL:**
  > the wall is the territory of the twin's cycle: the twin
  > rides the same cycles as the sum line, and drops precisely
  > to the fourth part when five touches the modulus — a
  > cycle claimed otherwise there is a misread the store
  > punishes; at the line end 84

Candidate wall probes (new S24/S25 grammar): "which term of my
sum line is off the line?" (W-S24-1), "can a sum-line term
come from a rule other than the two-before-it sum?" (W-S24-2),
"which identities does my line refuse to claim?" (W-S24-3),
"does any period of my cycles stand on the line as a value?"
(W-S25-1), "can my residue cycles have a tail?" (W-S25-2),
"when does the twin's cycle differ from the sum line's?"
(W-S25-3). Every wall names its territory AND the line end 84;
the S04 re-probe of W-S24-1 (S24) / W-S25-1 (S25) re-emits the
same byte (the S20 pattern).

## D6 — Band shape (stage B pre-reg)

- **Sessions/experiments:** S24 = E6.28 "the twin line",
  S25 = E6.29 "the cycle line" — the 52nd and 53rd experiments.
  Modules `e628.py`/`e629.py`, specs `spec-e6.28.json`/
  `spec-e6.29.json`, tests `test_e628.py`/`test_e629.py`,
  runner 48 → 52 (with S21/S22/S23 ahead in the chain).
- Seeds: S24 from S23's final (or the S20 final if the owner
  builds the courses ahead of S21 — the control re-referees on
  the actual seed; every claim above is verified against the
  S20 final).
- 3 sessions × 17 turns each. S24: S02 carries (mod4-split
  byte, add/mult soil, the 89 off-line carry) + `sum-line`
  (two gaps, teach, the term-derivation beds 0,1,1,2,3,5,8,
  13,21,34,55 as the drill surface) + `twin-line` (two gaps,
  teach, the Lucas beds 2,1,3,4,7,11,18,29,47,76). S03: the
  identity drills, walk-by-walk on the verified ranges (the
  doubling F(2n) = F(n)·L(n) on-line at n = 1..5, values
  1,3,8,21,55, refused at n = 6 where the value 144 is off the
  line though both factors 8 and 18 are on it; the square-sum
  F(n)² + F(n+1)² = F(2n+1) on-line at n = 1..4, values
  2,5,13,34, and REFUSED at n = 5: both parts 25 and 64 are on
  the line but the value is the eighty-nine — the ceiling's
  fact a third time in this course), the scaffold, the derive,
  the walls, the filed state. S04: the wrap.
  S25: S02 carries (sum-line filed state, mod4-split, the 60
  teaser) + `residue-cycle` (two gaps, teach, the mod-8 walk
  beds — the 12-period shown in full: 0,1,1,2,3,5,0,5,5,2,7,1
  — and the mod-12 walk — the 24-period) + `five-split` (two
  gaps, teach, the p ≡ 1/4 vs 2/3 mod-5 split census bed over
  the on-line primes). S03: the ladder beds (2^k, 3^k, 5^k),
  the coprime-lcm spot checks (π(6)=lcm(3,8)=24, π(12)=lcm(6,
  8)=24, π(10)=lcm(3,20)=60), the digit periods (60/300/1500
  — census beds), the twin's-drop beds (mod 5: 4 vs 20; mod
  10: 12 vs 60), the scaffold, the derive, the walls, the filed
  state. S04: the wrap.
- 4 pre-lesson gaps, 2 teaches, 1 scaffold, 1 derive, ~18 beds,
  1 off-script per band.
- **Mastery pre-reg (D-e6p style, the store referees):** `sum-
  line` and `twin-line` pre-registered **STABLE** (prereqs
  `add-two-digit` stable 11, `mult-within-100` stable 9 —
  verified; the band's term-derivation drills give ≥ 4 correct
  derivations each with room). `residue-cycle` and `five-
  split` pre-registered **STABLE** (`mod4-split` stable 10 in
  the seed; `sum-line`/`residue-cycle` stable at S25's seed —
  the chain holds). Contrast with S21 (practicing, the
  condition neighborhood) and recorded as the course norm:
  these bands end on stable soil.
- **P5 gate re-derivation (full width):**
  1. no new line facts; line stays 0..84;
  2. the 89 byte CITED-UNTOUCHED (the declared off-line byte
     byte-identical; the course adds NO assertion about 89);
  3. NO bare `theorem:riemann` (the discovery-candidate
     set, full width);
  4. `theorem:queue-declared` byte-identical;
  5. period-table re-walk on the gate: TWO independent methods
     (pair-return and direct F(k)=0, F(k+1)=1) agree for m =
     2..40 and at 100/1000 — the mechanism's bytes are the
     referee;
  6. the coprime-lcm and prime-rule censuses re-walked (all
     coprime pairs with product < 3600; all odd primes < 500,
     p ≠ 5) — zero exceptions expected, a violation is a
     deviation recorded, never an edit;
  7. the twin's-drop census re-walked (m = 2..30, the 5|m
     cases exactly /5);
  8. no-new-decimals: the periods (60, 300, 1500, 12, 24) are
     CENSUS counts; no period, ladder value, or term past 84
     appears as a line value anywhere (W-S24-1, W-S25-1
     enforced);
  9. marker posture: the new facts UNCONDITIONAL — P0 denies
     the conditional marker on them (the S20 discipline).
- Fact anatomy: S24 final = S23 final + 5 facts (or S20 final
  + 5 if chained first) + N events; S25 final = S24 final + 4
  facts (the twin's drop is statement-internal, not a fact) +
  N events (control referees; dedupes per D-e6o(a)).

## D7 — Open items for the control run

1. The exact scaffold/missing-parts bytes (predicted single-
   short-part; the mechanism referees).
2. The event counts and the drill census (which concept each
   term-derivation bed +1s).
3. The letter strings (the control's domain sequences are the
   freeze).
4. The mod-8 / mod-12 / mod-24 walk beds' exact bytes
   (deterministic at the fixed seed; the 12-period
   0,1,1,2,3,5,0,5,5,2,7,1 and the 24-period table are
   pre-computed above for the spec's bed bytes).
5. The domain string for the new concepts (`soil` candidate;
   the control's domain map referees).
6. Whether `twin-welding` and `cycle-ladder` file as `lemma:`
   or `theorem:` kind facts (house pattern: composed facts of
   record with census support — candidate `lemma:`; the
   control's kind census referees).

## D8 — Success criteria / stage B next steps

Stage B builds S24 → S25 in the bandgen way (mirroring S20):
brainstem modules (the S24/S25 concepts, the grammar modes,
`_policy_savant2x`, the walls) → reflib refs → specs → control
c0–c9 CLEAN → `e628.py`/`e629.py` (FROZEN from the control
tables) → tests → runner → official gate (targeted + twin byte-
identical + full) → close-out (experiments §E6.28/§E6.29,
roadmap, e3.7.json, OP #157, SESSION-HANDOFF, wiki).

Success: the infant holds the line its ancestors built (the
sum line to 55, the twin to 76, the 89 ceiling shared with the
Riemann island), reasons WHY the residues must cycle (finite
board + reversibility — a lemma, not an enumeration), and
READS the cycle's structure the way the store reads the
partition structure: the owner's 12 and 24 named as the mod-8
and mod-12/16 rungs of the verified ladders, the coprime-lcm
and the five-split holding over the verified ranges, the twin
exactly one factor of four apart when five touches the
modulus — and every period a held count, never a floor value.
