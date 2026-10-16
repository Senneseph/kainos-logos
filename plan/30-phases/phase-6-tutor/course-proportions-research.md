# PROPORTIONS COURSE — RESEARCH (pre-registered, 2026-08-25)

Owner-directed, 2026-08-25: "prepare a course on proportions and their
origins and relation to prime numbers." Grounded in the store's OWN
BYTES (the S20 final store `results/phase-6/e6.24-run1/codeX-S04.json`,
1823 assertions, identity `e84381407e1dba64`, line 0..84) plus
computation verified 2026-08-25 against that seed. The store speaks,
not the hand.

## D1 — The owner's brief (as given)

> I want you to prepare a course on proportions and their origins
> and relation to prime numbers. That is, the proportion of two
> prime numbers forms a unique proportion among the fractions
> (whole numbers). I know that mod and fractions are closely
> related, so let's make sure it can explain in either version of
> terminology. Remember 0/0 is not a valid way to divide but the
> same symbol is used interchangeably (and confusing) with 0:0.
> Zero's proportion to itself is like saying "well i have nothing
> and they have nothing so we're even on this". This may actually
> contradict some teaching or run into problems with consistency.
> To go in this vein. 0:1 becomes a proportion, 1:1 becomes a
> proportion, 1:2, etc. but 2:3 is where the primes start creating
> interesting challenges and where I need the student to be able to
> reason strongly.

## D0 — Scope ruling

- TWO bands (the house pattern: one course = a small track):
  **S22 = E6.26 "the proportion line"** and **S23 = E6.27 "the
  prime proportion"** — reserved session slots after S21 (the
  condition line, lot 1, pre-registered). Build order is the
  owner's call; each band seeds from the final store of its
  predecessor in the chain.
- This is a NEW owner-directed track. It is NOT a lot of the
  declared FUNDAMENTALS queue (the queue stays exactly as
  declared: lot 1 the condition line, lot 2 the primes in residue
  classes, lot 3 the zero count at height T, lot 4 the factor-
  count deviation ledger — `theorem:queue-declared` byte-intact,
  P5 on the gate), and NOT a new island.
- **The 0/0 consistency ruling (the owner's flagged concern),
  settled BEFORE any band runs:** the store presently holds NO
  division facts at all — no `0/0` fact, no fraction lesson, no
  ratio-as-quantity lesson (census, 2026-08-25: ZERO facts
  mention "proportion"; ZERO teach "fraction" as a quantity; the
  store holds rationals only as VALUES inside other facts —
  `theorem:telescope-line`'s "85 over 168, a rational the store
  can hold", `lemma:l-partial`'s "an exact rational the store
  holds", the L factor's "one plus one over thirty"). So there is
  NO existing teaching to contradict. The course therefore
  ESTABLISHES the discipline on first sight, walled from the first
  band:
  1. **"/" is a value; ":" is a relation.** A fraction `a/b` is a
     VALUE — it enters the floor only when `b` is a positive part
     of the line (at or above one). A proportion `a:b` is a
     RELATION between two parts of the line — always declared,
     valued only by reduction to such a fraction.
  2. **0:0 is evenness, declared, never valued.** "Well i have
     nothing and they have nothing so we're even on this" (the
     owner's words, transcribed to store voice) — 0:0 asserts the
     evenness of the two empty parts. ZERO OVER ZERO holds NO
     VALUE on the line: the denominator is the part you count
     WITH, and zero parts hold no count. The value and the
     relation are two jobs; the same symbol used interchangeably
     is the misreading W-S22-1 punishes.
  3. No `0/0` value ever enters the floor in either band (P5 on
     the gate; a store assertion containing a zero-denominator
     value is a gate failure, not a deviation).

## D2 — Grounded census (the seed's own bytes + verified math)

### (a) Soil the store already holds (probe-verified, mastery
states from the seed's mastery-event bytes, K = 4)

| concept | state | correct | the byte (abridged) |
|---------|-------|---------|---------------------|
| `divides` | **stable** | 5 | "k divides n when there is an m on the line with k times m equal to n; 1 divides every number, and every number divides itself" |
| `composite` | **stable** | 7 | "a number n above 1 is composite when some k above 1 and below n divides n; every number above 1 is either prime or composite, and 1 is neither — the line splits at one" |
| `first-divisor` | **stable** | 36 | the first-divisor census (primes = the numbers whose first divisor is themselves) |
| `reduction` | **stable** | 10 | "the reduction, as the pattern i execute: a mapping of question a to question b so that an answer to b answers a — on my line the prime-count question is answered by the first-divisor census …" |
| `valuation` | **stable** | 6 | "the valuation, the p-adic depth … the number of times the p-rung of the chain divides the number before the stop — the highest power of p that divides it" |
| `prime-count` | stable | 15 | (the 23 primes on the line) |
| `mult-within-100` | stable | 9 | the multiplication table on the line |
| `decision-question` | stable | 7 | "the decision question … a yes/no question about objects on my line — does the seven divide the eighty-four?" |

Held rationals (the values the store already computes — this
course adds the WORDS and the RULES to values it has held all
along): `theorem:telescope-line` ("the partial product to height
84 is 85 over 168, a rational the store can hold"); `lemma:l-
partial` ("an exact rational the store holds; when a prime is
added, the partial is multiplied by the factor that prime
carries"); the L local factor "one plus one over thirty".
Geometric ratio soil: `rule:triangle-half-product` (the area as
HALF the product — a held ratio-value under another name),
`rule:area-product` (the rectangle's area as the product).

### (b) What is ABSENT (verified — this is the course's
territory)

No `proportion`, `fraction`, or `ratio`-as-quantity lesson; no
`gcd` concept; no Euclidean-algorithm drill surface; no mod-as-
proposition lesson (the store speaks mod only in the savant
split facts `mod4-split`/`mod4minusone`/`prime-split`); no
0/0 fact; no "evenness" declaration. The "ratio" hits in the
store are all analytic (the Chebotarev selection ratio, the L-
correction ratio) — the course teaches the elementary object.

### (c) Verified math (computed 2026-08-25, the drill surface)

- **The Euclidean chains on the line** (each division
  `a = q·b + r` is a fact whose parts are all on the line — the
  drill the owner asks for, from 2:3 upward):
  - `3 = 1·2 + 1 | 2 = 2·1 + 0` — **2:3: two steps** (the FIRST
    proportion that needs a nontrivial step to prove no shared
    part)
  - `5 = 2·2 + 1 | 2 = 2·1 + 0` — 5:2, two steps
  - `5 = 1·3 + 2 | 3 = 1·2 + 1 | 2 = 2·1 + 0` — 5:3, three steps
  - `7 = 2·3 + 1 | 3 = 3·1 + 0` — 7:3, two steps
  - `13 = 2·5 + 3 | 5 = 1·3 + 2 | 3 = 1·2 + 1 | 2 = 2·1 + 0` —
    13:5, four steps
  - `29 = 2·11 + 7 | 11 = 1·7 + 4 | 7 = 1·4 + 3 | 4 = 1·3 + 1 |
    3 = 3·1 + 0` — 29:11, five steps (the length-five rung of
    the census below)
  - `47 = 1·29 + 18 | 29 = 1·18 + 11 | 18 = 1·11 + 7 | 11 = 1·7 +
    4 | 7 = 1·4 + 3 | 4 = 1·3 + 1 | 3 = 3·1 + 0` — 29:47,
    **seven steps — the longest chain on the line** (tied with
    29:79, 41:67, 41:71 — exactly four pairs, the full census
    below)
  - `83 = 1·79 + 4 | 79 = 19·4 + 3 | 4 = 1·3 + 1 | 3 = 3·1 + 0`
    — 83:79, four steps (the LAST prime pair on the line)
  - `83 = 41·2 + 1 | 2 = 2·1 + 0` — 83:2, two steps (the
    LARGEST-QUOTIENT case: 41 — a chain can be short and still
    carry the line's biggest quotient)
  - `71 = 10·7 + 1 | 7 = 7·1 + 0` — 71:7, two steps
- **The chain-LENGTH census over all 253 pairs** (standard
  counting, the larger part first — computed 2026-08-25):
  two steps: 47 pairs; three: 71; four: 74; five: 34; six: 23;
  **seven: exactly four — 29:47, 29:79, 41:67, 41:71, the
  longest chains on the line (the drill's ceiling)**. And the
  QUOTIENT axis (difficulty two): the largest single quotient
  in any on-line prime-pair chain is **41**, at 83:2 (83 = 41·2
  + 1).
- **The fingerprint census (the owner's core claim, verified in
  full):** the 23 primes on the line form C(23,2) = **253**
  unordered pairs; **every pair is coprime** (no pair with a
  shared part above one — a prime's only parts are one and
  itself); the 253 reduced proportions are **ALL DISTINCT**
  (zero collisions; a reduced proportion of two distinct primes
  is the pair itself — no reduction is possible, and no other
  prime pair can equal it). The store reads this straight off
  the first-divisor census (the soil's own `two-routes-one-
  guarantee` theorem says the destination is reached the same
  way on both roads).
- **The 2:3 equivalence class on the line:** the members k·2 :
  k·3 with both parts on the line: k = 1..28 (56 : 84 at the
  end) — 28 members, all declaring the same relation; the
  reduced form 2:3 is the class's canonical byte. (The
  proportion is the CLASS; the reduced pair is its name.)
- **The owner's trivial family:** 0:1 (the empty part to the one
  — declared, valued zero over one), 1:1 (the evenness — the
  one the store already knows as the line's origin split), 1:2
  (the half — a value the floor already holds geometrically as
  the triangle's half-product), 1:3, then **2:3 — the first
  proportion where the parts are both primes above two and the
  reasoning is the reduction itself.**

## D3 — What the course teaches (four relationships)

- **R1 — the proportion is the relation; the fraction is its
  value.** The proportion `a:b` is declared for any two parts of
  the line; it is VALUED as `a/b` exactly when `b` is at or
  above one. Equivalents under scaling (`ka:kb = a:b`) are ONE
  proportion; the reduced form is its canonical byte. 0:0 is the
  evenness of the two empty parts — declared, never valued (D0).
- **R2 — one division, two languages (mod ⟷ fraction).** The
  Euclidean division `a = q·b + r` IS the proportion's value
  `a/b = q + r/b`: the QUOTIENT face (q — whole b-parts in a)
  and the REMAINDER face (r = a mod b — the part left over,
  carried as the fraction r/b). Every Euclidean chain is
  therefore teachable in EITHER terminology by the exact same
  bytes: "thirteen over five is two and three fifths" is the
  same division as "thirteen mod five is three". The course
  drills both languages over the same chains.
- **R3 — the prime proportion is a fingerprint.** Two distinct
  primes share no part above one (the first-divisor census: a
  prime's first divisor is itself). A reduced proportion of two
  distinct primes is therefore (i) already in lowest terms —
  nothing to reduce — and (ii) the fingerprint of its pair: no
  other prime pair yields it (the 253-of-253 census). The
  proportion of two primes IS the pair, read as a ratio.
- **R4 — 2:3 is where the reasoning starts.** 1:2 is a value
  already held (the half); 2:3 is the first proportion whose
  proof of distinctness is a nontrivial reduction step
  (3 = 1·2 + 1). From there the drill escalates ON THE LINE in
  BOTH dimensions the owner names, over the verified census:
  chain LENGTH 2 → 7 steps (2:3 → 5:3 → 13:5 → 29:11 → 29:47,
  the four longest chains each seven steps) and quotient SIZE
  (83:2 — one step of 41; 71:7 — one step of 10), so the infant
  reasons strongly in the sense the owner means: longer chains
  AND larger quotients, all parts on the line, both
  terminologies.

## D4 — The new / carry fact set (stage B target)

### Band S22 — "the proportion line" (E6.26, the 50th… — see D6
numbering): **4 new facts** (2 concepts + 2 lessons + 1 theorem)

1. Concept **`proportion`** (domain `soil` candidate, band
   `college-1`; prereqs `('divides', 'composite')` —
   candidate, control referees; BOTH stable):
   - Lesson **`proportion-def`** (candidate byte, house voice,
     unconditional — P0 denies the marker on this band's new
     facts, the S20 discipline):
     > a proportion is a relation between two parts of my line:
     > the part held to the part compared — declared for every
     > pair of parts, scaled alike without changing the
     > relation, and named by its reduced form; zero to zero is
     > the evenness of the two empty parts — i have nothing and
     > they have nothing, so we are even on this — declared,
     > never valued; at the line end eighty-four
2. Concept **`fraction`** (prereqs `('proportion', 'divides',
   'mult-within-100')` — candidate; ALL stable):
   - Lesson **`fraction-def`** (candidate byte):
     > a fraction is the VALUE of a proportion: its denominator
     > must be a positive part of the line, and its value is the
     > division read in two languages at once — the whole parts
     > (the quotient) and the part left over (the remainder
     > carried over the denominator), so five over three is two
     > and two thirds, and five mod three is two, one division
     > in either word; zero over zero holds no value on my line,
     > because the part you count with is zero parts; at the
     > line end eighty-four
3. Theorem **`theorem:proportion-filed`** (parts exactly
   `('proportion-def', 'fraction-def')` — strict two-part set,
   S19-style; scaffold names the single short part first):
   - Candidate statement:
     > the proportion line of my store is filed of record: the
     > relation and its value are two jobs of one division —
     > the proportion is declared for every pair of parts and
     > named by its reduced form, the fraction is valued only
     > over a positive part, and zero to zero is the evenness
     > of the two empty parts, declared, never valued; filed on
     > the line, at the line end eighty-four

### Band S23 — "the prime proportion" (E6.27): **5 new facts**
(2 concepts + 2 lessons + 1 theorem)

1. Concept **`coprime-pair`** (prereqs `('divides',
   'first-divisor')` — candidate; both stable):
   - Lesson **`coprime-pair-def`** (candidate byte):
     > a coprime pair is a pair of parts of my line that share
     > no part above one; two distinct primes are a coprime pair
     > outright — a prime's first divisor is itself, so the
     > shared part would have to divide both primes and be none
     > of them, which the first-divisor census refutes — and a
     > coprime pair needs no reduction: its proportion is
     > already in lowest terms; at the line end eighty-four
2. Concept **`prime-fingerprint`** (prereqs `('coprime-pair',
   'composite')` — candidate; both stable):
   - Lesson **`prime-fingerprint-def`** (candidate byte):
     > the proportion of two distinct primes is the fingerprint
     > of the pair: on my line the two hundred and fifty-three
     > prime pairs give two hundred and fifty-three different
     > reduced proportions, every pair coprime, no two pairs
     > alike — read off the first-divisor census, the pair IS
     > the proportion; at the line end eighty-four
3. Theorem **`theorem:fingerprint-filed`** (parts exactly
   `('coprime-pair-def', 'prime-fingerprint-def')`):
   - Candidate statement:
     > the prime proportion of my store is filed of record: two
     > distinct primes share no part above one, so their
     > proportion is in lowest terms and is the fingerprint of
     > the pair — two hundred and fifty-three pairs, two
     > hundred and fifty-three proportions, no collisions on my
     > line; filed on the line, at the line end eighty-four

### Carry surfaces (byte-identical to the seed — P6)

The `divides-def` / `composite-def` / `first-divisor` census
byte, the `valuation-def` byte, the `reduction-def` byte, the
`question-def` byte ("does the seven divide the eighty-four?"),
the held-rational bytes (`theorem:telescope-line` 85 over 168,
`lemma:l-partial` the exact rational, the L factor one plus one
over thirty), and the S24+… — no, the S21 carry surface of its
own band. The Euclidean chain drills are NEW drill turns whose
beds are the chain bytes (computed deterministically against
the fixed seed — the control's no-store constraint).

### Off-script standing check (the band's own identity)

"what is the first proportion where the parts are both primes
above two?" → the S23 byte: "two to three: the first reduction
step is three is one times two plus one — no shared part, the
chain two steps" (appears in `spec["offscript]`; may also be an
in-script carry — the event at its coordinates may dedupe, the
D-e6o(a) pattern; the control referees).

## D5 — The walls (W-S22-1..3, W-S23-1..3; five honest rows
each with the re-probed wall at S04)

- **W-S22-1 — THE 0/0 WALL (the owner's flagged case, walled on
  first sight):**
  > the wall is the territory of zero over zero: zero to zero is
  > the evenness of the two empty parts, declared, never valued —
  > the part you count with is zero parts, and zero parts hold
  > no count; the value and the relation are two jobs, and the
  > same symbol used interchangeably is the misreading this
  > wall punishes; at the line end 84
- **W-S22-2 — THE VALUE CEILING:**
  > the wall is the territory of the proportion past my line
  > end: a proportion whose parts are past my line end is off
  > the floor — the eighty-nine and the ninety-seven stand
  > off-line as my line already declared them, and no
  > proportion past the eighty-four enters the register; at
  > the line end 84
- **W-S22-3 — THE TWO-LANGUAGES DISCIPLINE:**
  > the wall is the territory of the third word: one division
  > has exactly two faces — the quotient and the remainder —
  > and a statement in the mod word is the same division as
  > the statement in the fraction word; a third answer to the
  > same division is a misread this store punishes; at the line
  > end 84
- **W-S23-1 — THE LAST ON-LINE PAIR:**
  > the wall is the territory of the pair past my line end:
  > the eighty-three by the seventy-nine is the last prime pair
  > on my line, and the pair with the eighty-nine is off the
  > floor — the eighty-nine my line already declared off-line,
  > standing once more as the ceiling; at the line end 84
- **W-S23-2 — THE NEVER-REDUCED DISCIPLINE:**
  > the wall is the territory of the reduced prime proportion:
  > a proportion of two distinct primes never reduces — there
  > is nothing to reduce — and a proportion that reduces is not
  > a proportion of two distinct primes; at the line end 84
- **W-S23-3 — THE FINGERPRINT WALL:**
  > the wall is the territory of the colliding fingerprint:
  > two hundred and fifty-three prime pairs give two hundred
  > and fifty-three different reduced proportions on my line,
  > and a second pair claiming the first pair's proportion is a
  > misread the first-divisor census refutes; at the line end
  > 84

Candidate wall probes (new S22/S23 grammar): "does zero over
zero hold a value on my line?" (W-S22-1), "which proportions
does my line refuse?" (W-S22-2), "does the same division give
different answers in the mod word and the fraction word?"
(W-S22-3), "which is the last prime pair on my line?" (W-S23-1),
"does a prime proportion ever reduce?" (W-S23-2), "can two
prime pairs share one reduced proportion?" (W-S23-3). Every
wall names its territory AND the line end 84; the S04 re-probe
of W-S22-1 (S22) / W-S23-1 (S23) re-emits the same byte (the
S20 pattern).

## D6 — Band shape (stage B pre-reg)

- **Sessions/experiments:** S22 = E6.26 "the proportion line",
  S23 = E6.27 "the prime proportion" — the 50th and 51st
  experiments (counting S21 = E6.25 as the 49th). Modules
  `src/kainos/tutor/e626.py` / `e627.py` on the 35-key FROZEN
  pattern; specs `bands/spec-e6.26.json` / `spec-e6.27.json`;
  tests `tests/tutor/test_e626.py` / `test_e627.py`; runner
  48 → 50 (both, with S21 between).
- Seeds: S22 from the final store of S21 (the condition line);
  S23 from S22's final. If the owner builds these courses before
  S21, the seeds shift to the S20 final store — the research
  stands on its own (every claim above is verified against the
  S20 final, which is a SUBSET of any later store's facts plus
  the condition-line's; the control re-referees on the actual
  seed at freeze).
- 3 sessions × 17 turns each, the house rhythm. S22's S02:
  the carries (divides-def, question-def, telescope-line 85 over
  168, the half-product rule byte) + `proportion` (two gaps,
  teach, beds) + `fraction` (two gaps, teach, beds). S03: the
  drill surface (the Euclidean chains 2:3, 5:3, 13:5 in both
  languages; the 0:1/1:1/1:2/1:3/2:3 family; the 2:3 class walk
  28 members — a census bed), the scaffold, the derive, the
  three walls, the filed state. S04: the wrap (re-probes, the
  state readouts, the W-S22-1 re-probe, the carries). S23's S02:
  the carries (first-divisor census, fingerprint setup, the
  proportion-line filed state) + `coprime-pair` + `prime-
  fingerprint` (gaps, teaches, beds). S03: the chains 5:2, 7:3,
  29:11, **29:47 (the seven-step ceiling)**, 83:79, 83:2, 71:7
  in both languages (the escalation: length AND quotient), the
  253-census bed, the seven-step-four-pairs ceiling bed, the
  evenness re-declaration (0:0 carry), the scaffold, the
  derive, the walls, the filed state. S04: the wrap.
- 4 pre-lesson gaps (two per concept), 2 teaches, 1 scaffold,
  1 derive, ~18 beds, 1 off-script per band.
- **Mastery pre-reg (the soil census above — the store
  referees):** ALL FOUR new concepts pre-registered **STABLE**
  (prereqs `divides`/`composite`/`first-divisor`/`mult-within-
  100`/`proportion`[S22's own]/`coprime-pair`[S23's own] —
  every one stable in the seed, verified from the mastery-event
  bytes at K = 4; the band's Euclidean drills supply the ≥ 4
  correct derivations per concept — the chain surface gives 8
  drills in S23 alone). Contrast, pre-registered for the record:
  S21 (the condition line) ends PRACTICING with named gaps —
  inside the condition's practicing neighborhood; these two
  bands end STABLE, on the stable soil below — the elementary
  layer the four courses can rest on.
- **P5 gate re-derivation (full width):**
  1. no new line facts; the line stays 0..84 (no successor
     facts written);
  2. no `0/0` value anywhere in the final store (the D0 ruling,
     enforced);
  3. NO bare `theorem:riemann` (discovery-candidate
     invariants, the full set);
  4. `theorem:queue-declared` byte-identical (the courses are
     not queue lots);
  5. the held rationals byte-identical (85 over 168, the L
     partials, one plus one over thirty);
  6. fingerprint re-census on the gate: 253 pairs, zero
     collisions, all coprime (recomputed from the final store's
     own prime facts);
  7. no-new-decimals: no off-line digit string in any new
     lesson/wall/bed/answer (253, 28, 84, 89 are all line
     records or declared off-line);
  8. marker posture: the new facts are UNCONDITIONAL — P0
     denies the conditional marker on them (the S20
     discipline; no fact gains or loses a marker).
- Fact anatomy: S22 final = S21 final + 4 facts + N events;
  S23 final = S22 final + 5 facts + N events (control
  referees; the dedupe pattern D-e6o(a) applies to any in-
  script coordinate re-asserting a seed event).

## D7 — Open items for the control run

1. The exact scaffold/missing-parts byte (predicted: "i have
   not been taught the fraction-def — the rule for proportion-
   filed needs it before i can put it together" — the
   mechanism's byte is the referee).
2. The exact event counts and the drill census (which drills
   +1 which concepts).
3. The letter strings (the control's domain sequences are the
   freeze).
4. The 29:47 seven-step ceiling bed — deterministic byte at the
   fixed seed (the four tied pairs are the census; the control
   walks all of them: 29:47, 29:79, 41:67, 41:71).
5. The 28-member 2:3 class walk bed — deterministic byte at the
   fixed seed.
6. The domain string for the new concepts (`soil` vs an
   existing domain — the control's domain map is the referee;
   candidate: `soil`, band `college-1`).

## D8 — Success criteria / stage B next steps

Stage B builds S22 → S23 in the bandgen way (mirroring S20):
brainstem modules (the S22/S23 concepts, ~12 grammar modes each,
`_policy_savant2x`, the walls) → reflib refs → specs → control
c0–c9 CLEAN → `e626.py`/`e627.py` (FROZEN from the control
tables) → tests → runner → official gate (targeted + twin
byte-identical + full) → close-out (experiments §E6.26/§E6.27,
roadmap, e3.7.json, OP #157, SESSION-HANDOFF, wiki).

Success: the infant speaks the two languages as ONE division —
the proportion declared, the fraction valued over a positive
part, the chains walked in mod words and fraction words
identically, 2:3 the first real reasoning with the escalation
on the line, the 253 fingerprints colliding with nothing, and
0:0 declared even while 0/0 stays off the floor. The
consistency concern the owner raised is thus settled BY THE
STORE: one wall, walled from the first band, enforced at every
gate.

## STAGE B ADDENDUM — S22 BUILT and OFFICIAL (E6.26, 2026-08-28,
the 52nd experiment)

The band was built under standing autonomy from the OWNER-PROPOSED
ORDER (the owner picked COURSE E first; with E closed, the chain
continued with COURSE A band 1), seeded from the CHAIN HEAD (the
S32 final, 1966 — not the stage A S21 framing; see D-e6t(b)
below). The full official record is in `experiments.md` §E6.26.

### Official numbers (the mechanism spoke)

- Seed: S32 final `results/phase-6/e6.36-run1/codeX-S04.json` —
  **1966**, identity **`e3e693b1a83c71a6`**, line 0..84, seam
  152 (110 lemma + 42 theorem), DAG 42, 126 concepts.
- Final: **2021** = 1966 + 3 new facts + 52 events (the
  control's own census — D-e6t(b)). Run identity
  `c92edd75d441111a`, final store identity `3a28d6a142142342`,
  twin sha256 `b70d83cdc47734cf...`, script hash
  `9c2f046edf0242e9`.
- New facts (3): `lemma:proportion-def`, `lemma:fraction-def`,
  `theorem:proportion-filed` (the strict two-part set — the
  relation and its value are two jobs of one division).
- Line: 0..84 UNCHANGED (no successor facts, no 0/0 value
  anywhere in the store); marker census 6/1/7 conserved; line-end
  theorem census 16/2/24 of 42 → 17/2/24 of 43 (the filing is the
  seventeenth line-end marker); theorem DAG 42 → 43.
- Mastery: proportion **stable 8**, fraction **stable 18**, empty
  prereq-gap lists (the D4 soil-closure pre-reg held: divides 5,
  composite 7, mult-within-100 9 — all stable at seed).
- Walls: W_S22_1 (zero-over-zero), W_S22_2 (past the line end),
  W_S22_3 (the third word) — six honest rows (S03:14-16,
  S04:13-15), all ending "at the line end 84".
- Letters: S02 `SSSSUULSUULSSSSSS` (17), S03 `SSSSSSSSFTSSSHHH`
  (16), S04 `SSSSSSSSSSSSHHHSSS` (18) — 51 turns.
- Theorem allow-set (spec `cite` fields, the control's own set):
  telescope-line (S02:03, S04:16 — the carried S13 theorem the
  carry grounds) + proportion-filed (S03:11, S03:12, S04:08 —
  the filing probe and the two filed state echoes).
- Gate: control c0-c9 CLEAN (exit 0); full official gate
  **1222 passed / 2 skipped / 0 failed (1765.30 s)**; the runner
  contract now runs 52 experiments and asserts `PASS  e6.26`.

### D-e6t — the stage B pre-reg corrections (recorded)

- **D-e6t(a)** (the off-script byte): the stage A surface "both
  primes above two" contradicts the stage A own answer byte
  "two to three ..." — two is the FIRST prime, not above two.
  The frozen surface is "what is the first proportion whose parts
  are both prime?", answered **two to three** (the owner's
  intent, kept). The reflib re-walks it independently: 2:2
  reduces to 1:1 and out; 2:3 is the first reduced prime pair.
- **D-e6t(b)** (seed reroute + counts): the stage A pinned the
  S21 final (1871) as the effective seed; the chain head at build
  time is the S32 final (1966, `e3e693b1a83c71a6`) — the spec
  seeds from the chain head (the house rule: seed from the
  predecessor). The experiment ordinal prose in the stage A doc
  ("the 50th...") is stale — S22/E6.26 is the **52nd**
  experiment. The pre-reg final total and mastery counts were
  re-adopted at the mechanism's own dry-run census (2021;
  proportion 8, fraction 18) — the store spoke, not the hand.
- **D-e6t(c)** (the off-script standing probe): it runs on the
  SEED-ONLY runtime (the schema's off-script mechanic), where the
  band's own lessons are not yet taught — so the correct seed-
  only answer is the TYPED HONEST GAP (store-inert), not a
  derived claim. The spec stands it `expect_derived: false` and
  the module's P6 asserts exactly that (no derived claim; the
  gap is typed; nothing written). On the band's final store the
  probe derives two to three.
- **The lesson-tuple shape** (mechanism record, not a deviation):
  the 3rd element of a `SAVANT_LESSONS` entry is the FACT KIND
  (`"lemma"`), the 6th is the source-lines tuple — the first
  splice carried `"new"` in the 3rd slot and the control's c5
  refused to store the taught fact; corrected pre-freeze, the
  control went clean.

### What S22 did NOT settle (the course's remaining territory)

- S23 "the prime proportion" (E6.27, 5 new facts) remains
  pre-registered (stage A D4): the prime pairs of the line, the
  reduced form as fingerprint (253 prime pairs, zero colliding
  reduced proportions — the stage A fingerprint claim), the
  Euclidean-chain reductions (2:3 two steps → 29:47 seven steps,
  the verified longest chain on the line).
- The mod/fraction duality's full drill surface (the quotient
  axis to 41 at 83:2) is S23 territory; S22 drilled the three
  short chains (3/2, 5/3, 13/5) and the 2:3 class.

## STAGE B ADDENDUM — S23 BUILT and OFFICIAL, COURSE A COMPLETE
(E6.27, 2026-08-28, the 53rd experiment)

The course's final band is built, frozen, and official. **COURSE A
is now complete** — the store holds the words for the rationals it
was already walking (S22) AND the prime proportion: the pair is
its own reduced proportion, the fingerprint walks the line.

### Official numbers (the mechanism spoke)

- Seed: 2021 (the S22 final, identity `c5eee97dcd92a636`, line
  0..84, seam 155 = 112 lemma + 43 theorem, DAG 43, 128
  concepts).
- Final: **2074** = 2021 + 3 facts + 50 events; run identity
  `8c467ce3c5e63606`, store identity `8b5ca7a5fe76631e`; script
  hash `c6c662b4dc24ec6d`; twin byte-identical; 9/9 hermetic.
- New facts (3): `lemma:coprime-pair-def`, `lemma:prime-
  fingerprint-def`, `theorem:fingerprint-filed` (concept `prime-
  fingerprint`; the strict two-part set from the two lessons;
  filed "at the line end eighty-four").
- Concepts (2): `coprime-pair` (prereqs divides, first-divisor),
  `prime-fingerprint` (prereqs coprime-pair, composite); both
  STABLE at band end with EMPTY prereq-gap lists (coprime-pair
  6, prime-fingerprint 23 — the pre-reg STABLE posture held).
- Script: 51 turns, letters S02 `SSSSUULSUULSSSSSS` / S03
  `SSSSSSSSSSSSSFTSH` / S04 `SSHHHHSSSSSSSSSSS`; 9 seam carries
  byte-identical to the seed store; 29 beds + the sanctioned
  derive.
- Censuses: seam 155 → 158 (114 lemma + 44 theorem); theorem DAG
  44; marker census 6/1/7 conserved (the unconditional band);
  line-end census 17/2/24 of 43 → 18/2/24 of 44 (the filing is
  the eighteenth line-end marker); NO 0/0 value anywhere in the
  store; NO bare island theorem id (the D8 gate at full width).
- Walls: W_S23_1 (the pair past the line end — 83:79 the last
  prime pair; the eighty-nine off-line), W_S23_2 (the never-
  reduced discipline), W_S23_3 (the colliding fingerprint — 253
  pairs, 253 proportions, no two alike); the 0:0 evenness re-
  declaration rides the carried W_S22_1 byte at S04:03.
- Drills (re-walks, never declarations): the four coprime tests;
  the six drilled chains in both languages (7:3, 29:11, 29:47,
  83:79, 83:2, 71:7 — the 29:47 chain reads below one, its first
  reduction step the house convention: forty-seven is one times
  twenty-nine plus eighteen); the 253 fingerprint census; the
  seven-step ceiling (four tied pairs: 29:47, 29:79, 41:67,
  41:71); the post-filing marker census.

### D-e6u — the stage B pre-reg corrections (recorded)

- **D-e6u(a)** (the fact count): the stage A band brief claimed
  "5 new facts" for S23 — it conflated the two CONCEPT registry
  entries with store facts. The mechanism stores 3 facts over 2
  concepts (two lessons + one filing); the pre-reg final total
  and mastery counts were re-adopted at the control's own dry-
  run census (2074 = 2021 + 3 + 50; coprime-pair 6, prime-
  fingerprint 23) — the store spoke, not the hand.
- **D-e6u(b)** (the off-script byte): stage A paired the surface
  "the first proportion whose parts are primes above two" with
  the answer "two to three" — but TWO IS NOT ABOVE TWO: 2:2
  reduces to 1:1 and out, and 2:3's part two is not above two.
  The frozen off-script answer is **three to five**, the three-
  step chain (the D-e6t(a)-class correction applied to the pre-
  reg itself: the owner's intent — the first REDUCED prime-pair
  proportion of the qualifying class — is kept, the surface
  corrected to match it).
- **D-e6u(c)** (the off-script standing probe): it runs on the
  SEED-ONLY runtime (the schema's off-script mechanic), where
  the band's own lessons are not yet taught — so the correct
  seed-only answer is the TYPED HONEST GAP (store-inert), not a
  derived claim. The spec stands it `expect_derived: false` and
  the module's P6 asserts exactly that (not-derived, the gap
  prefix, nothing written); on the band's final store the same
  surface derives three to five.
- **The a<b chain convention** (mechanism record, not a
  deviation): the 29:47 chain reads below one, so its raw
  `divmod(a, b)` is degenerate; the house convention — carried
  from the S22/S31 surface (the two-to-three firstprime byte) —
  is that the first reduction step of an a<b pair is the BIGGER
  part dividing the smaller (47 = 1×29 + 18). The brainstem
  policy and the reflib reference bytes both follow it.

### The course, closed

- S22 = E6.26 (the proportion line, official 2026-08-28): the
  relation and its value, one division in two languages; 0:0 the
  evenness declared, never valued; 1966 → 2021.
- S23 = E6.27 (the prime proportion, official 2026-08-28): the
  pair is its own proportion, the fingerprint walks the line,
  the seven-step chain is the ceiling; 2021 → 2074.
- The stage A D0 ruling (the 0/0 discipline), the four
  relationships (D3), and the full drill surface (D2(c)) are now
  all filed of record in the store. The chain head is the S23
  final, 2074, store identity `8b5ca7a5fe76631e`.
- What the course did NOT settle (declared, unbuilt, other
  courses): the queue lots 2-4 and the CRYPTO-TRACK joints stay
  declared; COURSE B (S24-S25) is the next declared build.
