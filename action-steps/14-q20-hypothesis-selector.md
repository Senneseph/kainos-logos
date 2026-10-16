# Action Step 14 — Hypothesis space + info-gain selector + game loop (P2.03–P2.06)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

The reasoning core of 20 Questions: a hypothesis space, an information-gain question
selector, and the game loop.

## Prerequisites

- [ ] Step 13 done (corpus + oracle + CODEX seed).

## Background

The learner is rewarded for *eliminating possibilities*, not for generating text. The
selector picks the question that maximizes expected information gain (entropy
reduction), with a tie-break that prefers shrinking EXCEPTION. The question parser
reuses the Phase 1 deterministic kernel's operator vocabulary.

## Steps

### 1. Question parser (reuse kernel)

Extend the deterministic kernel with the 20Q question grammar
(`plan/30-phases/phase-2-20questions/game-spec.md`):

```
"Is it <property>?"            → CONSTRAINT(property = yes/no)
"Does it have <property>?"     → CONSTRAINT(has_<property> = yes/no)
"How many <part>?"             → CONSTRAINT(part = <number>)
"Is it a <category>?"          → HYPOTHESIS(is_a = category)
```

Unknown phrasing → `UnresolvedRef` (so the game can ask a clarifying question).

### 2. `src/kainos/q20/hypothesis.py`

`HypothesisSpace` over concept ids:
- `H` = consistent set; `apply(constraint)` filters it;
- `entropy()` = `log2(|H|)`;
- `split(question)` → sizes of `H_yes, H_no, H_unknown, H_sometimes`.

### 3. `src/kainos/q20/selector.py`

`best_question(H, questions, oracle)` maximizes:

```
IG(q) = H(H) - Σ_a P(a)·H(H_a)     where P(a)=|H_a|/|H|, a ∈ {yes,no,unknown,sometimes}
```

Tie-breaks, in order: (a) larger reduction of `|H_unknown|` (shrink EXCEPTION),
(b) lower question cost. Return `(question, ig)`.

### 4. `src/kainos/q20/game.py`

`Game` state machine: `ask → answer → update → guess/end` with budget
`max_questions=20`. `make_guess(H)`: guess the single remaining concept when `|H|==1`
(or the top concept when `IG < stop_threshold`). Record win/loss + trace.

### 5. Tests

- `tests/q20/test_question_parse.py`: each template → correct CONSTRAINT/HYPOTHESIS;
  unknown phrasing → `UnresolvedRef`.
- `tests/q20/test_hypothesis.py`: `apply(alive=no)` removes alive concepts; entropy 0
  when `|H|==1`; split partitions correctly.
- `tests/q20/test_selector.py`: a near-median-split question is chosen over a lopsided
  one; tie-break order respected.
- `tests/q20/test_game.py`: scripted oracle → correct guess within budget; exhaustion
  → loss; wrong guess recorded.

## Verification

```bash
pytest tests/q20 -q
```

Expect: all green.

## Done when

- [ ] question parser maps templates → Query IR (reusing kernel)
- [ ] hypothesis space + entropy + split correct
- [ ] selector maximizes IG with documented tie-breaks
- [ ] game loop handles win/loss/budget and records a trace

## If stuck

`plan/30-phases/phase-2-20questions/game-spec.md` (info-gain formula + tie-breaks).
