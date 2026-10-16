# Phase 2 — 20 Questions (active-learning environment)

The second phase, per the project brief: the training game that exercises
EXCEPTION, information gain, and persistent memory — and produces the cleanest
possible demonstration that the system *learns* without retraining.

## Goal

Build a 20 Questions game where the Kainos-Logos system:

1. maintains a **hypothesis space** over a concept corpus,
2. selects **maximally informative questions** (expected information gain),
3. records every answer as a **CODEX constraint** with provenance,
4. recognizes and escalates **EXCEPTION** territory (asks a clarifying question),
5. **persists** everything it learns, growing the CODEX across games and restarts.

## Architectural claims tested

1. **Active knowledge acquisition (A1)** — the system converges on the hidden
   concept in fewer questions than a random/no-info baseline.
2. **EXCEPTION shrinkage (A2)** — over many games the EXCEPTION space shrinks while
   the ontology grows (`Coverage(T,C)` ↑, exception count ↓).
3. **Persistent growth (A3)** — knowledge from game N is retained (restart) and
   improves game N+1, with **frozen neural weights**.
4. **Compositional concept recognition (A4)** — it infers an unseen concept from a
   conjunction of learned properties (not from a memorized label).
5. **Ontology expansion via contradiction (A5)** — a repeated contradiction
   (`bear hibernates` vs `polar bear doesn't`) yields a new context TERM rather than
   a blended weight.

## Inputs (from Phases 0–1)

`kainos.codex`, `kainos.ir` (generic core), `kainos.reasoner`, `kainos.lang`
(deterministic kernel — reused for question/answer parsing), `kainos.harness`.

## Outputs (left behind for Phase 3)

- `kainos.q20` (game loop, oracle, info-gain selector, learning loop).
- Concept corpus + property oracle (the seed ontology).
- The "growth dashboard" (exception coverage over time).

## Exit criteria

1. E2.1–E2.5 run green and are reported.
2. The growth dashboard shows exception space shrinking across ≥N games.
3. A restart demo: train on game set 1 → restart → play game set 2, showing
   retention + improvement with frozen kernel.
4. `plan/30-phases/phase-2-20questions/results.md` has metric tables + the growth curve.

## Key documents

- [`game-spec.md`](game-spec.md) — game rules, question grammar, oracle, info-gain formula.
- [`experiments.md`](experiments.md) — E2.1–E2.5.
- [`actions.md`](actions.md) — ordered concrete actions.
