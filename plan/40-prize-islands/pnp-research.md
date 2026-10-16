# P vs NP island — research record (stage A: the statement, the
# panel of record, the line's censuses, the walls, the two band shapes)

Target: P vs NP — the Clay Millennium problem (the CMI holds the
$1,000,000 prize; the island plan is `05-island-p-np.md`).

Method: every value below is verified by the mechanism's own python
(the record-don't-optimize policy — recorded occurrences, never
optimized), and the canonical statements are captured VERBATIM from
the record sources (the CMI problem document of Stephen Cook,
`pvsnp.pdf` on claymath.org, retrieved 2026-08-25; the ITCS 2026
algebrization paper, LIPIcs 362:37, retrieved 2026-08-25).

---

## D0 — the schema register check (recorded 2026-08-25)

The island plan's register-novelty flag: *if the machine/complexity
register is short of the band-spec schema, extend the schema FIRST
and record it.* Checked against `specs/band_spec.schema.json` and the
brainstem `Concept` shape:

- the spec's concept item carries only `id` / `name` / `prereqs` /
  `lesson` (slug + statement) — there is NO register or domain enum
  at concept level;
- the band-level `domain` is a free-form string (the band's own
  name);
- the brainstem `Concept(id, description, college, domain, prereqs)`
  takes `domain` as a free-form string (S11 `soil`, S14–S16 `bsd`,
  S17 `beal`).

**Conclusion: no schema extension is required.** The
machine/complexity register is carried where the island plan
predicted — in the CONCEPTS and LESSONS (the human-written part);
the compiler's checks (letters, mastery, walls, carries, discipline)
already cover it. This section IS the recorded first-check the
island plan required ("verify that claim at the first spec stage").

---

## D1 — the statement, verbatim, with its record source

**Source of record:** the Clay Mathematics Institute's problem
document for the Millennium problem — Stephen Cook, "THE P VERSUS
NP PROBLEM" (claymath.org, the `pvsnp.pdf` problem statement, the
CMI's own page for the problem). The CMI website's short form:
*"If it is easy to check that a solution to a problem is correct, is
it also easy to solve the problem? This is the essence of the P vs
NP question."*

The document's opening, verbatim:

> "The P versus NP problem is to determine whether every language
> accepted by some nondeterministic algorithm in polynomial time is
> also accepted by some (deterministic) algorithm in polynomial
> time."

and the problem statement line, verbatim:

> "Problem Statement. Does P = NP ?"

The formal definitions, verbatim from the same document:

**The model.** "The standard computer model in computability theory
is the Turing machine, introduced by Alan Turing in 1936." The
appendix's machine clause, verbatim: "A Turing machine M consists of
a finite state control (i.e., a finite program) attached to a
read/write head moving on an infinite tape."

**Class P.** "M runs in polynomial time if there exists k such that
for all n, T_M(n) ≤ n^k + k." and "P = { L | L = L(M) for some
Turing machine M that runs in polynomial time }." The document's
robustness clause, verbatim: "Thus P is a robust class and has
equivalent definitions over a large class of computer models." Its
informal line, verbatim: "Informally the class P is the class of
decision problems solvable by some algorithm within a number of
steps bounded by some fixed polynomial in the length of the input."

**Class NP (the certificate form).** "NP stands for 'nondeterministic
polynomial time'." The modern defining clause, verbatim: "a language
L over Σ is in NP iff there is k ∈ N and a polynomial-time checking
relation R such that for all w ∈ Σ*, w ∈ L ⇔ ∃y (|y| ≤ |w|^k and
R(w, y))." The document calls such a y *a certificate for x* ("In
the case of an NP-complete problem it is easy to see that the search
problem can be efficiently reduced to the corresponding decision
problem").

**The prize.** The CMI's $1,000,000 Millennium Prize (the problem is
one of the seven; unsolved as of record).

---

## D2 — the panel of record (the structural facts, each verbatim
from the record sources)

1. **The halting problem** (Turing 1936; from the CMI document,
   verbatim): "We define the Halting Problem HP as follows: HP =
   {⟨M⟩ | M is a Turing machine that halts on input ⟨M⟩}. Turing
   used a simple diagonal argument to show that HP is not
   decidable." — the DECLARED FRONTIER for S18.

2. **Reductions** (from the CMI document, verbatim): "L1 ≤m L2 iff
   there is a (total) computable function f : Σ*1 → Σ*2 such that
   x ∈ L1 ⇔ f(x) ∈ L2, for all x." and the key fact: "It is easy
   to see that if L1 ≤m L2 and L2 is decidable, then L1 is
   decidable." — the store's own shadow: the prime-count question
   answered BY the first-divisor census (D3).

3. **NP-completeness and Cook–Levin** (from the CMI document,
   verbatim): "A language L is NP-complete iff L is in NP, and L'
   ≤p L for every language L' in NP." and Proposition 1(c): "If L
   is NP-complete and L ∈ P, then P = NP." The document's history
   line, verbatim: "In 1971 the present author [Cook] introduced a
   notion of NP-completeness ... The main results in [9] are that
   several natural problems, including Satisfiability and 3-SAT ...
   and subgraph isomorphism are NP-complete." (Cook 1971: "The
   complexity of theorem-proving procedures", STOC 1971 — the
   Cook–Levin theorem; Levin's independent "universal search
   problem" of 1973.) — DECLARED for S19 (the universal question).

4. **The relativization barrier** (Baker–Gill–Solovay 1975:
   "Relativizations of the P = ? NP question", SIAM J. Comput.
   4(4):431–442). From the CMI document, verbatim: "However, in [3]
   it was shown that there is an oracle set A relative to which P =
   NP, suggesting that diagonalization with reduction cannot be
   used to separate these two classes." — DECLARED FRONTIER for
   S19 (W-S19-1).

5. **The circuit path for a P ≠ NP proof** (from the CMI document,
   verbatim): "Thus to prove P ≠ NP it suffices to prove a
   super-polynomial lower bound on the size of any family of
   Boolean circuits solving some specific NP-complete problem, such
   as 3-SAT." The context of record, verbatim: "In 1949 Shannon
   proved that for almost all Boolean functions f : {0,1}^n →
   {0,1}, any Boolean circuit computing f requires at least 2^n/n
   gates." and "all attempts to find even super-linear lower bounds
   for unrestricted Boolean circuits for 'explicitly given' Boolean
   functions have met with total failure; the best such lower bound
   proved so far is about 4n."

6. **The AC⁰ frontier** (from the CMI document, verbatim):
   "Exponential lower bounds for NP problems have been proved for
   restricted circuit models, including monotone circuits [Razborov
   1985; Alon–Boppana 1987] and bounded depth circuits with
   unbounded fan-in gates [Hästad 1989; Smolensky 1987]."
   (Smolensky, "Algebraic methods in the theory of lower bounds for
   boolean circuit complexity", STOC 1987: parity needs exponential
   size in constant-depth circuits — the result D4's census shadows
   at exact small k.) — DECLARED FRONTIER for S19 (W-S19-4).

7. **The natural proofs barrier** (Razborov–Rudich, "Natural
   proofs", J. Comput. Syst. Sci. 55(1):24–35, 1997). From the CMI
   document, verbatim: "Razborov and Rudich explain this failure by
   pointing out that all methods used so far can be classified as
   'natural proofs', and natural proofs for general circuit lower
   bounds are doomed to failure, assuming a certain
   complexity-theoretic conjecture asserting that strong
   pseudo-random number generators exist. Since such generators have
   been constructed assuming the hardness of integer factorization,
   we can infer the surprising result that a natural proof for a
   general circuit lower bound would give rise to a more efficient
   factoring algorithm than is currently known." — DECLARED
   FRONTIER for S19 (W-S19-3).

8. **The algebrization barrier** (Aaronson–Wigderson, "Algebrization:
   A new barrier in complexity theory", STOC 2008 / ACM Trans.
   Comput. Theory 1(1):2, 2009) — and the 2026 strengthening of
   record (Chen–Hu–Ren, "New Algebrization Barriers to Circuit
   Lower Bounds via Communication Complexity of Missing-String",
   ITCS 2026, LIPIcs 362:37:1–37:20; arXiv:2511.14038). The ITCS
   2026 abstract's three results, verbatim: "(1) We construct an
   oracle A₁ and its multilinear extension such that PostBPE has
   linear-size A₁-oracle circuits on infinitely many input lengths.
   That is, proving PostBPE ⊄ i.o.-SIZE[O(n)] requires non-
   algebrizing techniques. (2) We construct an oracle A₂ ... such
   that BPE has linear-size A₂-oracle circuits on all input
   lengths. (3) ... For every super-half-exponential function
   h(n), we construct an oracle A₃ ... such that this natural
   subclass of MA_E has h(n)-size A₃-oracle circuits on all input
   lengths. This suggests that half-exponential might be the
   correct barrier for MA_E circuit lower bounds w.r.t.
   algebrizing techniques." — DECLARED FRONTIER for S19 (W-S19-2),
   with the 2026 line as the barrier's own still-extending record.

9. **The class inclusions of record** (from the CMI document,
   verbatim): "LOGSPACE ⊆ P ⊆ NP ⊆ PSPACE. A simple diagonal
   argument shows that the first is a proper subset of the last,
   but we cannot prove any particular adjacent inclusion is
   proper." and Proposition 3: "If A then BPP = P. If not-A then
   P ≠ NP." (A = the assertion that some exponential-time language
   requires exponential circuit complexity; the first implication
   is the Impagliazzo–Wigderson theorem, the second the Kabanets
   observation.)

10. **The crypto joint** (from the CMI document, verbatim — the
    R4 joint the island plan names): "An efficient factoring
    algorithm would break the RSA public key encryption scheme" and
    the record's own reduction example, verbatim: "Given an integer
    b > 1, the smallest prime divisor of b can be found with about
    log₂ b queries to L_fact, using binary search." (L_fact =
    {⟨a, b⟩ | ∃d (1 < d < a and d | b)}.) — the spf-by-binary-
    search reduction, of record: the same shape as the store's own
    first-divisor census reduction (D3).

11. **The belief of record** (from the CMI document, verbatim):
    "Most complexity theorists believe that P ≠ NP." — the island's
    question stays OPEN in the store: declared, not settled.

The feasibility thesis, verbatim (for the lessons' grounding): "A
natural problem has a feasible algorithm iff it has a polynomial-
time algorithm."

---

## D3 — the S18 censuses (computed and cross-checked, 2026-08-25)

The S18 band ("the decidable line") holds on the line:

**The decision table** (the store's own yes/no query class — every
probe terminates with a yes or a no; cross-checked against the S11
divides reference):

| p | n | divides? |
|---|---|----------|
| 7 | 84 | yes |
| 13 | 84 | no |
| 2 | 84 | yes |
| 3 | 84 | yes |
| 17 | 84 | no |

**The prime-count reduction** (the store's own reduction, D2.2):
the question "how many primes lie at or below the line end 84?" is
answered BY the first-divisor census — the scan is the S11 spf walk
(`d = 2; while d*d <= n: if n % d == 0: return d; d += 1; return
n`), and a number is prime exactly when its walk ends at itself:

- **π(84) = 23** (the chain census: 23 of the numbers 2..84 have
  first-divisor themselves; cross-checked by an independent
  brute-force primality scan — 23 = 23 ✓; the primes of the line:
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
  61, 67, 71, 73, 79, 83 — the same 23-prime set the S14 panel
  censuses ran over).

**The self-cost census** (cost is a COUNTER — the ledger policy
literalized; the cost function is the spf walk's candidate count,
instrumented and cross-checked against its closed form for every n
in 2..84 — instrumented == closed form, all 83 rows ✓):

- total candidate steps of the scan over the whole line (2..84):
  **192**;
- the heaviest single query on the line: n = 83 (a prime),
  **8** candidate steps (the walk tries 2..⌊√83⌋ = 2..9);
- spot rows: spf-cost(64) = 1 (divided by 2 on the first try),
  spf-cost(49) = 6 (7², the walk tries 2,3,4,5,6,7), spf-cost(84)
  = 1, spf-cost(12) = 1, spf-cost(2) = 0 (the loop never runs);
- the S11 kill-trials pattern (the ledger cost the store already
  holds — the composite-only walk) re-agrees: 95 candidate steps
  over all composites with ALL candidates, 87 with prime candidates
  only.

**The pigeonhole table** (the line's combinatorial truth — the
store counts violations exactly; n+1 objects into n boxes, "a
violation" = an injective map, which the principle says cannot
exist; cross-checked by BRUTE-FORCE enumeration for n ≤ 6 — zero
violations on every one):

| n (boxes) | total maps (n+1)^n | violations (injective) |
|---|---|---|
| 1 | 2 | 0 |
| 2 | 9 | 0 |
| 3 | 64 | 0 |
| 4 | 625 | 0 |
| 5 | 7 776 | 0 |
| 6 | 117 649 | 0 |
| 7 | 2 097 152 | 0 |
| 8 | 43 046 721 | 0 |
| 9 | 1 000 000 000 | 0 |
| 10 | 25 937 424 601 | 0 |

(the minimum shared occupancy is 2 on every row: ceiling((n+1)/n)).

---

## D4 — the parity census (computed and cross-checked, 2026-08-25)

The S19 band's one genuine in-store difficulty computation (the
island plan's prescribed census): the exact DNF (and CNF) term
count of the PARITY question (even count of ones) on k variables,
k = 1..16.

**The result (verbatim ledger):** the smallest DNF and the smallest
CNF of parity_k each need exactly **2^(k−1)** terms/clauses:

| k | terms (dnf = cnf) |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 4 |
| 4 | 8 |
| 5 | 16 |
| 6 | 32 |
| 7 | 64 |
| 8 | 128 |
| 9 | 256 |
| 10 | 512 |
| 11 | 1 024 |
| 12 | 2 048 |
| 13 | 4 096 |
| 14 | 8 192 |
| 15 | 16 384 |
| 16 | 32 768 |

**Cross-checks (the scratch-computation rule: bounded +
independent):**

1. *The structural claim*, verified by exhaustive check for EVERY
   k in 1..16 (2^16 × 16 = 1,048,576 flip checks, seconds of
   python): every 1-row of parity has, on every single-bit flip, a
   0-row — so the 1-set of parity carries NO 1-cube with more than
   a single vertex; every DNF term is a cube of 1s, so every term
   is a single minterm; the 1-set has exactly 2^(k−1) rows; hence
   any DNF needs all 2^(k−1) of them — and the symmetric argument
   (every 0-row's flip is a 1-row) gives the CNF clause count.
2. *The minterm DNF evaluates parity exactly* on the FULL truth
   table — exhaustive for k = 12 (4 096 rows, every row checked
   against the minterm-DNF evaluation) ✓.
3. *The minterm count itself* (the 1-set size 2^(k−1)) re-agrees
   for all k by direct truth-table census ✓.

Against the record (D2.5/6): Shannon's 2^n/n counting bound at n =
16 is 4 096 — below the census's 32 768 (the census is the EXACT
value; the record bound is an almost-all-functions statement). This
is the exact small-k SHADOW of the AC⁰ exponentials (W-S19-4): the
blowup the record proves at scale, counted to the term on the line.

---

## D5 — the walls (declared off-line territory)

Each wall names its record place AND the line end 84; off-line
values appear ONLY in wall/lesson declaration bytes, never as store
assertions; the no-new-decimals rule holds (record numbers named at
their scale, never stored as values).

**S18 (the decidable line):**

- **W-S18-1 — the halting wall (the declared frontier):** the
  halting problem, of record (the turing record of 1936): there is
  no machine that decides, for every machine and every input,
  whether the machine halts — turing's diagonal argument, of
  record; yes/no questions about MACHINES in general are, in
  general, unanswered questions; MY line is finite by CONSTRUCTION
  — a DESIGN FACT of the line, not a theorem about machines — every
  question about my line's objects ends on the line, and the
  non-terminating territory lies past my line, at the line end 84.
- **W-S18-2 — the machine-universe wall:** the record's machines
  carry an INFINITE TAPE (the cmi document's own machine clause);
  i am one bounded inhabitant of the machine universe — my ledger
  holds what my walk computes, and a machine's questions about its
  OWN halting are declared territory, not my answers, at the line
  end 84. (The design-fact discipline the island plan requires: the
  tamability is named AS a design property of the finite line —
  never a universal claim.)

**S19 (the difficulty line):**

- **W-S19-1 — the relativization barrier (the baker-gill-solovay
  record of 1975):** there is an oracle world where p = np and an
  oracle world where p≠ np (of record) — a technique that
  relativizes (that keeps working with an oracle attached) answers
  both worlds and so answers neither question; declared frontier,
  at the line end 84.
- **W-S19-2 — the algebrization barrier (the aaronson-wigderson
  record of 2009, the chen-hu-ren 2026 line):** the barrier that
  arithmetization (multilinear extensions) still does not escape —
  of record, extended in 2026: new oracle worlds with LINEAR-SIZE
  circuits for subclasses of postbpe (on infinitely many lengths)
  and bpe (on all lengths), and h(n)-size circuits for a natural
  subclass of ma_e against EVERY super-half-exponential h(n) —
  'half-exponential might be the correct barrier', of record, 2026;
  declared frontier, at the line end 84.
- **W-S19-3 — the natural proofs barrier (the razborov-rudich
  record of 1997):** assuming strong pseudo-random generators exist
  (of record, constructed assuming the hardness of factoring),
  'natural' proof techniques for general circuit lower bounds are
  doomed — a natural proof would give a faster factoring algorithm
  than the record holds; declared frontier, at the line end 84.
- **W-S19-4 — the ac0 wall (the razborov-smolensky / hastsad
  record):** parity needs EXPONENTIAL size in constant-depth
  circuits, of record (smolensky stoc 1987; hastsad stoc 1989) —
  the declared frontier whose EXACT SMALL-K SHADOW is my census
  (2 to the k-minus-1 terms, k up to sixteen — D4), at the line end
  84.

**The honest articulation (stored in S19 as the band's reaching
lesson, `shadow-def`, concept `size-shadow`):** the line's side
holds — the parity census ends exactly at small k, and the line's
own walk settles the parity question in BOUNDED cost; the question
of the island itself is OPEN of record (the cmi); most complexity
theorists believe p≠ np, of record, but no proof settles it — and
the missing ingredient is named: a technique that works OUTSIDE
relativization, algebrization, AND natural proofs — one nobody
knows the shape of.

---

## D6 — band shapes (pre-reg)

**S18 = E6.22 — "the decidable line"** (seed: the S17 close-out
store, `results/phase-6/e6.21-run1/codeX-S04.json` — 1641
assertions, identity `e092ef1261ef7210`, twin-verified, line
0..84, seam 128, theorem DAG 36; the S11 soil stable: first-divisor
36 correct, divides 5, scan-ledger 12; S17 all stable: valuation 6,
lte-form 7, beal-summit 4, beal-census 10; rh-relevance still
practicing 17).

- **Domain:** `pnp` (the new band-domain; the D0 check says the
  schema holds it as-is).
- **Concepts (4, college-1, prereqs point DOWN — S18-internal or
  seed):**
  1. `decision-question` (prereq: `divides` — the yes/no query
     class the S11 divides lesson already holds);
  2. `tamable-machine` (prereq: `decision-question`);
  3. `reduction` (prereqs: `decision-question`, `scan-ledger` —
     the reduction example IS the S11 census);
  4. `cost-counter` (prereqs: `reduction`, `scan-ledger` — cost is
     the ledger's own pattern).
- **Lessons (4, verbatim lines = the stored bytes):**
  1. `question-def` — the decision question: yes/no about line
     objects; every such question the line runs ends with a yes or
     a no (the line's own pattern, named at the line end);
  2. `tamable-def` — tamability AS DESIGN FACT (finite walks on a
     finite line; 'not a theorem about machines in general' — the
     over-claim class the island plan names, walled off inside the
     lesson);
  3. `reduction-def` — reduction: answer-to-B answers-A; the store's
     OWN instance: the prime-count question answered by the
     first-divisor census (D3);
  4. `cost-def` — cost is a counter (candidate-steps of the walk;
     the line's scan takes one hundred ninety-two; the heaviest
     single query takes eight, at 83).
- **Theorem (1, scaffolded, strict part set):**
  `line-pi-reduction` (concept `reduction`; parts
  (`question-def`, `reduction-def`)): the count question ends on
  the line — twenty-three primes at or below the line end, each a
  number whose first divisor is itself; the census that answers it
  is a walk that ends (one hundred ninety-two candidate steps).
- **Walls (2):** W-S18-1 (the halting wall, D5), W-S18-2 (the
  machine-universe wall, D5).
- **Beds (on-line, exact against the mechanism's python — D3):**
  the decision table (5 rows); the π-reduction (23 + the prime
  list-of-23 as the census row); the cost census (total 192, max 8
  at 83, spot rows 64:1 / 49:6 / 84:1 / 12:1 / 2:0; kill-trials
  95 / 87); the pigeonhole table (n = 1..10 rows, violations all 0).
- **Seam (6 carries + 1 off-script, pre-reg — the actual bytes
  fixed at the spec stage):** the beal-def statement carry; the
  census-def (beal census) carry; the S17 primitive-territory WALL
  carry (H); the S15 ramification-correction carry; the queue
  carry; the S11 first-divisor carry (the decision question's
  soil). Off-script: "state the beal-line-satisfaction rule" (the
  just-closed island's summit).
- **Letter contract (expected, pre-reg — the mechanism's census
  governs):** pattern U/L per lesson, F on the missing-parts and
  scaffold-failure probes, T on the sanctioned derive, H on the two
  walls (+ the S17-wall H carry at S4), S elsewhere; 51 turns
  (17+17+17); ~54 events (the S15–S17 drift pattern is expected and
  REPORTED, not asserted).
- **P0/P5 invariants (PRE-REG):** NO bare candidate fact of any
  p-vs-np conclusion — the denylist extends: no fact id containing
  `pvsnp` / `p-vs-np` / `pnp` as a `theorem:` (the question itself
  lives as DECLARED LANGUAGE in the S19 summit lesson, never as a
  settled theorem); the six carries + off-script byte-identical;
  the line 0..84 unchanged (no new successor facts); the riemann
  conj byte-identical.

**S19 = E6.23 — "the difficulty line"** (seed: the S18 close-out
store — 1641 + 6 facts + ~54 events ≈ 1701, identity TBD by the
S18 gate).

- **Concepts (4, domain `pnp`):**
  1. `class-p` (prereq: `cost-counter` — the polynomial bound as
     the line's own counter discipline);
  2. `class-np` (prereqs: `class-p`, `cost-counter` — the
     certificate checked in polynomial cost; the store's own
     pattern: a fact record IS a certificate of its own derivation
     path);
  3. `pnp-summit` (prereq: `class-np` — the question itself, a
     DECLARED RECORD FACT: 'does p = np' — the cmi record, open);
  4. `size-shadow` (prereqs: `pnp-summit`, `class-np` — the
     line's side: the parity census as the exact small-k shadow of
     the record's exponentials + the named missing ingredient).
- **Lessons (4):** `p-class-def` (P in exact finite form, the line
  voiced); `np-class-def` (NP as the certificate-checked question;
  a stored fact = a certificate the line can check — the store's
  own NP pattern); `pnp-def` (the question of the island,
  verbatim of record — "Does P = NP?" house-voiced — declared,
  open, with the record's belief 'most complexity theorists
  believe p≠ np' and the proof requirement — a P≠NP proof must
  show a specific NP question requires super-polynomial cost, by a
  technique outside the three barriers); `shadow-def` (the census:
  1, 2, 4, ... 32 768 terms at sixteen variables — the exponential
  recorded as a counter; the line's walk settles the question in
  bounded cost; the missing ingredient OUTSIDE relativization,
  algebrization, AND natural proofs — nobody knows the shape).
- **Theorem (1, scaffolded):** `parity-blowup-filed` (concept
  `size-shadow`; parts (`shadow-def`, `np-class-def`)): the
  difficulty filed on the line — parity is a certificate-checked
  question whose smallest expression (dnf AND cnf) grows to
  thirty-two thousand seven hundred sixty-eight terms by sixteen
  variables while the line's own walk settles it in bounded
  cost — the exponential is a record on the line, at the line end
  84.
- **Walls (4):** W-S19-1 relativization, W-S19-2 algebrization
  (with the 2026 chen-hu-ren line), W-S19-3 natural proofs,
  W-S19-4 ac0 (D5).
- **Beds (on-line, exact — D4):** the parity table (k = 1..16,
  2^(k−1) rows — the in-store difficulty census, S11-ledger-
  shaped); the Shannon context named at its scale (2^16/16 = 4096
  — named, never stored).
- **Seam (6 carries + 1 off-script, pre-reg):** the
  line-pi-reduction (S18 theorem) carry; the S18 halting WALL
  carry (H); the beal-def (S17) carry; the bsd-statement (S16)
  carry; the S17 primitive WALL carry (H); the queue carry.
  Off-script: "state the parity-blowup-filed rule" (the band's own
  — the S2→S4 self-carry pattern is NOT used; the off-script is an
  EARLIER island's theorem: "state the line-pi-reduction rule" —
  the S18 summit). [Final off-script choice fixed at the spec
  stage: the pattern is an earlier island's filed theorem — the
  S18 line-pi-reduction.]
- **P0/P5 invariants:** the denylist (no theorem of any
  p-vs-np conclusion — the island CLOSES on the store's terms: the
  question held verbatim, the line's side exact, the barriers as
  walls; `theorem:p-vs-np` never appears, as `theorem:beal` never
  appeared); the line 0..84 unchanged; the riemann conj
  byte-identical; the three-barrier walls cross-checked byte-
  identical to the Brainstem attributes.

**The deviation family D-e6m** (declared, pre-reg — recorded at
closeout, the mechanism's own bytes govern): (a) expected
gap/teach/state byte drift on the new register's concepts; (b)
expected mastery-census drift (the S4 re-probes drill the band's
own concepts — the S15–S17 pattern); (c) expected event-count drift
(~54 events for 51 turns, reported not asserted); (d) the
missing-parts/scaffold bytes on the two theorem part-sets (the
S16/S17 both-parts pattern governs if both parts are untaught at
the probe); (e) articulation-fragment fixes (house hyphenation of
compounds — 'p vs np' / 'ac0' / 'chen-hu-ren' — the wall's own
byte wins before freeze, the store speaks not the hand).

**Build order:** S18 first (it seeds S19), each through the full
bandgen pipeline (spec → control #1 c0–c9 CLEAN → freeze →
official gate (twin runs byte-identical + full suite) → close-out),
one commit for the pipeline, the D-e6m corrections recorded as
they surface, the owner gets the island-close headline when S19
lands (the P vs NP island — the last in-scope island — closes the
12-band track).
