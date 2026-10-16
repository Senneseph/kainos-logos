# 05 — Island: P versus NP (the difficulty line)

Target: P vs NP (Clay, $1M, PPL 091). Survey: `01-targets.md` §3.

## Objective (what the store can say at island completion)

The store holds the *register* the problem lives in — decision
problems, computability (the halting wall), complexity classes in
their exact finite forms, reductions as a store pattern, and one
genuine in-store difficulty computation (the parity circuit blowup
on the line, an exact exponential census) — and holds the **three
barriers** (relativization, algebrization, natural proofs) as
named declared-theorem walls with their exact statements, plus a
`pnp-reach` fact naming the missing ingredient: *a technique
outside relativization, algebrization, and natural proofs — one
nobody knows the shape of.* **No `theorem:p-vs-np` in the store.**

Why this island is in scope: the goal is "the fundamentals
needed to reason about / answer questions about the problem." The
barriers ARE the current answer to "why can't anyone settle it" —
the exact analog of the RH island's zero-density territory and the
BSD island's Selmer frontier. The store reasons about the
difficulty question; it does not attempt the proof.

## Descent to fundamentals (the chain, ground up)

```
bands 1–3 (exact finite arithmetic)                [built]
  └─ the store as a TAMABLE machine (explicit:
     every query on my line terminates — halting
     is a DESIGN FACT of the line, not a theorem
     about it)                                       [S18]
  └─ decision problems (yes/no questions about
     line objects; the store's own query class)      [S18 lesson]
  └─ computability: the halting problem (DECLARED
     frontier — Turing's non-computable question;
     the store's wall: "there are yes/no questions
     about machines that no machine answers; I am
     one such machine and my line is my safe
     region")                                        [S18 wall]
  └─ reductions (mapping questions so an answer
     to B answers A; the store pattern: my
     pi-count is answered BY my spf census — a
     reduction on my own line)                       [S18 lesson]
  └─ complexity as an exact FINITE notion on the
     line: "cost n = the number of line-steps"
     (the store holds cost as a COUNTER — its
     ledger policy literalizes complexity)          [S18/19]
  ├─ the in-store difficulty census: the smallest
  │  DNF (or CNF) expressing parity on k variables,
  │  k ≤ 84 — the exact exponential blowup counted
  │  on the line (2^{k−1} terms — a BED, S11-style
  │  records)                                        [S19 beds]
  │    └─ the AC⁰ wall (Razborov–Smolensky: parity
  │       needs exponential size in constant-depth
  │       circuits — DECLARED frontier; the on-line
  │       census is its exact small-k shadow)        [S19 wall]
  ├─ P and NP as declared lessons (the definitions
  │  in exact finite form: the polynomial bound,
  │  the certificate; the store's certificate
  │  pattern = its own fact records — a fact is a
  │  certificate verifiable on the line)            [S19 lesson]
  ├─ SAT/completeness (Cook–Levin, 1971: every NP
  │  question reduces to a truth question — the
  │  universal question; DECLARED frontier + the
  │  pigeonhole shadow on the line: the store
  │  counts pigeonhole violations exactly)          [S19 frontier]
  └─ the BARRIERS (the answer to "why no proof"):
       relativization (Baker–Gill–Solovay 1975),
       algebrization (Aaronson–Wigderson 2009 + the
       2026 strengthenings), natural proofs
       (Razborov–Rudich 1997) — three declared
       walls with exact statements; the missing
       ingredient is named in pnp-reach
                                                        [S19 walls]
  └─ pnp-reach (the honest articulation)            [S19]
```

The **connect joints** (the owner's requirement):
- **P/NP ↔ CRYPTO (R4):** R4's RSA attempt is a difficulty
  instance *inside* this register; the barriers explain why R4's
  wall (the door holds) is the expected behavior, not an
  accident. The declared "first difficulty-class conjecture"
  (RSA-breaking = factoring, open) lives on this island's soil.
- **P/NP ↔ Beal (S17):** the computability register (decision
  problems, tamability) is the same register Beal's primitive-
  triple question lives in ("does a primitive triple exist?" is a
  decision question whose answer the store's line does not reach)
  — the Beal band's census pattern is the P/NP island's census
  pattern.
- **P/NP ↔ RH/ BSD:** the zero-density and Selmer frontiers are
  the *analytic* cousins of the barrier walls — every island ends
  at a named frontier of known technique; this island holds the
  frontier of the *proof* techniques themselves.

## Research plan (verify BEFORE the first spec freezes)

1. **The canonical statements (verbatim sources of record):**
   the Clay P vs NP problem page (the proof requirements,
   including the explicit non-uniform lower-bound requirement for
   a "P ≠ NP" resolution); the Cook–Levin theorem statement
   (1971/1979 forms); Baker–Gill–Solovay (1975);
   Razborov–Rudich (1997, the natural-proofs assumptions);
   Aaronson–Wigderson (2009, the algebrization definition); the
   ITCS-2026 algebrization line (the 2026 strengthenings —
   citation of record); the Razborov–Smolensky AC⁰ parity result.
2. **The parity census (computed, cross-checked):** the exact
   DNF/CNF term counts for parity on k variables for k = 1..16
   (the exponential 2^{k−1}; the scratch-computation rule:
   bounded + independently cross-checked — the DNF minimality
   for small k via exhaustive truth-table enumeration, an exact
   finite computation); verify against the classical literature
   value.
3. **The store-as-machine framing (design review):** the exact
   wording of "the store terminates on my line" (the design fact,
   not a stored theorem — the wall must name it as a design
   property to avoid the over-claim class): the store's
   mechanism is a finite-state line walk by construction; the
   halting problem is about the UNIVERSE of machines, of which
   the store is one bounded inhabitant.
4. **The certificate pattern (design review):** the store's fact
   records as certificates (a stored fact = a certificate of its
   own derivation path) — the NP-verification pattern in the
   store's own terms; the exact phrasing for the lesson.

## Band plan (built the bandgen way)

Two bands (the register is conceptually heavier than BSD's but
arithmetically lighter — no new L-family, no descent; the cost is
concept precision, not computation):

### S18 — "the decidable line" (e6.21), seed = (BSD island end;
if the islands interleave, the FUNDAMENTALS queue end — the spec
research stage fixes the actual seed store)

- **Concepts (4):** `decision-question` (yes/no on line objects),
  `tamable-machine` (the store's halting design fact),
  `reduction` (question-to-question mapping, cost preserved up
  to polynomial), `cost-counter` (line-steps as the cost
  measure — the ledger policy made explicit).
- **Lessons (4):** the decision question, tamability, reduction
  (the store's own pi-count-byspf-census reduction as the
  example), cost.
- **Theorems/walls:** the halting problem (DECLARED frontier wall
  — Turing's non-computable question, verbatim statement; the
  store's safe region named); the pigeonhole principle (an
  on-line verifiable combinatorial truth — the store counts
  pigeonhole violations exactly on the line; the lesson's
  evidence bed).
- **Carries:** the S11 spf/ledger (the cost counter's soil) +
  the store's own fact-records (the certificate pattern).

### S19 — "the difficulty line" (e6.22), seed = S18 store

- **Concepts (4):** `class-p`, `class-np` (the exact finite
  definitions), `circuit-size` (the DNF/CNF blowup as a
  computable census), `barrier` (the meta-theorem class: a
  theorem about WHICH techniques cannot work).
- **Lessons (4):** P, NP, the size census, the barriers
  (each a lesson + a declared wall with its exact statement).
- **Beds (computed):** the parity DNF/CNF term-count table
  (k = 1..16, the 2^{k−1} exact records — the in-store
  difficulty census, S11 ledger policy), the pigeonhole
  violation counts, the "cost of the store's own queries"
  table (a self-cost census: how many line-steps the store's
  standard queries take — the store measuring its own
  polynomials).
- **Frontier/walls:** Cook–Levin (declared), AC⁰-parity
  (declared + the on-line census as its small-k shadow), the
  three barriers (declared walls, exact statements),
  **pnp-reach** (the missing ingredient named: outside all
  three barriers; the shape unknown).
- **P-checks:** no `theorem:p-vs-np` (the candidate invariant);
  the unconditional/conditional marker discipline (the barriers
  are statements about proof technique — unmarked or
  appropriately marked, decided at the spec stage by the
  mechanism's convention).

## Execution notes

Same bandgen discipline as the BSD island; the reference
functions for this island are the truth-table/DNF/CNF/pigeonhole
computations (the shared `_pnp_py_*` refstyle) — all exact
finite, all S11-ledger-shaped. The register novelty (machines,
complexity) is carried in the CONCEPTS and LESSONS (the
human-written part); the compiler's checks (letters, mastery,
walls, carries, discipline) already cover it — no compiler
change is needed to build this island (verify that claim at the
first `make band-validate`; if the schema is short of the new
register, extend the schema FIRST, record it, then build).
