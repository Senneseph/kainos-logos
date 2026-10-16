# Phase 2 — Game Spec: 20 Questions

## Game rules (classic, formalized)

- A **hidden concept** `C` is drawn from the corpus (a TERM in the CODEX).
- The **questioner** (the system) asks yes/no questions (or clarifying questions).
- The **oracle** answers `yes` / `no` / `unknown` / `sometimes` (with an optional
  context/condition). A small budget `max_questions = 20` (configurable).
- The game ends when the questioner **guesses** (correctly/incorrectly) or the budget
  is exhausted.

## The oracle (deterministic, seeded)

Each concept has a property table:

```
concept: bicycle
  alive: no
  manufactured: yes
  human_powered: yes
  has_wheels: yes
  wheel_count: 2
  can_carry_person: yes
  has_engine: no
  ...
```

The oracle answers by looking up the property; `unknown` if the property is not
defined for that concept (this is what creates EXCEPTION pressure). `sometimes` is
emitted when the property is conditional (this creates the *missing dimension*
signal for A5).

## Question grammar (reuses Phase 1 kernel)

Questions are constrained to the semantic operators already in the kernel:

```
Is it <property>?            → CONSTRAINT(alive=false / true)
Does it have <property>?     → CONSTRAINT(has_wheels=true)
How many <part>?             → CONSTRAINT(wheel_count=2)  [numeric]
Is it a <category>?          → HYPOTHESIS(is_a=category)
```

The kernel parses the surface question into a Semantic IR `Query`; the reasoner
updates the hypothesis space by applying the constraint against the corpus.

## Hypothesis space & information gain

- `H = {c1..cn}` (concepts still consistent with all constraints so far).
- Question `q` splits `H` into `H_yes`, `H_no`, `H_unknown`, `H_sometimes`.
- Select `q` maximizing expected information gain (entropy reduction):

```
IG(q) = H(H) - Σ_a P(a) · H(H_a)
```

where `P(a) = |H_a| / |H|`. When all questions are binary-ish and `H` is large,
this reduces to near-median splits. Ties broken by (a) larger `|H_unknown|`
reduction (to shrink EXCEPTION) and (b) question cost.

## EXCEPTION handling (the A2/A5 machinery)

- `unknown` answers accumulate; a property undefined for a concept is an `UNSEEN`
  EXCEPTION.
- `sometimes` answers indicate a conditional property → candidate **missing
  dimension** (e.g. `hibernates` is conditional on `species`). The learning loop
  proposes a new context TERM and re-expresses the assertions.
- When a question enters EXCEPTION territory, the reasoner may ask a **clarifying
  question** ("do you mean …?") — the same escalation ladder as Phase 1's C3.

## Learning loop (after each game)

```
observations (answers) → constraints (candidate assertions, status=candidate,
  provenance{source=game_<id>, observer=oracle})
→ verify (consistent with existing?) → consolidate (status=established) 
→ generalize (if a repeated contradiction → new context TERM)
```

No neural weights change. The CODEX is the only thing that grows.

## Metrics

| Metric | Definition |
|--------|------------|
| **Questions-to-solve** | median questions per game (lower is better). |
| **Win rate** | fraction of games guessed correctly within budget. |
| **Info-gain efficiency** | entropy reduction per question. |
| **EXCEPTION coverage** | `Coverage(term, context)` over the corpus, tracked per game. |
| **Ontology size** | #terms, #assertions, #exceptions over time. |
| **Retention** | knowledge present after restart. |
| **Compositional inference** | unseen-concept guess accuracy from property conjunction. |
| **Contradiction→dimension** | # new context TERMs created from `sometimes`/conflicts. |

## Baseline for comparison

- **Random questioner** (uniform choice from valid questions) — lower bound.
- **Greedy but stateless** (no CODEX persistence; recomputes from scratch each game) —
  isolates the value of *persistence*.
