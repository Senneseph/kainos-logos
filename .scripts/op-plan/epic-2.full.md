**Source:** `plan/30-phases/phase-2-20questions/README.md` + `plan/20-roadmap.md`

## Goal

Build a 20 Questions game where the Kainos-Logos system:

1. maintains a **hypothesis space** over a concept corpus,
2. selects **maximally informative questions** (expected information gain),
3. records every answer as a **CODEX constraint** with provenance,
4. recognizes and escalates **EXCEPTION** territory (asks a clarifying question),
5. **persists** everything it learns, growing the CODEX across games and restarts.

## Scope

Action steps **13–16** (`P2.01`–`P2.15`). Experiments E2.1–E2.5
(`plan/30-phases/phase-2-20questions/experiments.md`). Game rules/grammar/info-gain
formula: `plan/30-phases/phase-2-20questions/game-spec.md`.

## Architectural claims tested

1. **A1 — Active knowledge acquisition:** converges on the hidden concept in fewer
   questions than a random/no-info baseline.
2. **A2 — EXCEPTION shrinkage:** over many games the EXCEPTION space shrinks while
   the ontology grows (`Coverage(T,C)` ↑, exception count ↓).
3. **A3 — Persistent growth:** knowledge from game N is retained (restart) and
   improves game N+1, with frozen neural weights.
4. **A4 — Compositional concept recognition:** infers an unseen concept from a
   conjunction of learned properties (not a memorized label).
5. **A5 — Ontology expansion via contradiction:** a repeated contradiction yields a
   new context TERM rather than a blended weight.

## Compounding contract

**Artifact left behind:** `kainos.q20` (game loop, oracle, info-gain, learning
loop), concept corpus, growth dashboard.
**Consumed from prior phases:** CODEX, IR, reasoner (domain packages), harness,
`kainos.lang` (deterministic kernel, reused for question/answer parsing).

## Why 20Q second

It needs the persistent CODEX + reasoner from Phase 1, and it adds the *active*
dimension (what to ask next) that regex doesn't exercise.

## Ordering notes (from `actions.md`)

- P2.01–P2.09 build the game; P2.10 begins the experiments. Do not skip the
  baselines (P2.08) — they make A1/A3 *falsifiable*.
- **E2.3 (persistence) and E2.5 (contradiction) are the two most important results
  for the project's thesis.**
- The "bear hibernates" vs "polar bear doesn't" conflict is the canonical test
  case for A5.

## Exit criteria

Four exit criteria (E2.1–E2.5 green, growing dashboard, restart demo, signed
`results.md`) are tracked in the **"Phase 2 sign-off"** Milestone, together with
kill criterion **K3** from `plan/04-reality-check.md` §4.

## Work packages (this epic)

| Ticket | Directive | Plan actions | Priority |
|---|---|---|---|
| #122 | [13] 20Q corpus + property oracle + CODEX seed (P2.01–P2.02) | P2.01–P2.02 | Normal |
| #123 | [14] Hypothesis space + info-gain selector + game loop (P2.03–P2.06) | P2.03–P2.06 | Normal |
| #124 | [15] Learning loop + baselines + growth dashboard (P2.07–P2.09) | P2.07–P2.09 | Normal |
| #125 | [16] E2.1–E2.5 runs + Phase 2 sign-off (P2.10–P2.15) | P2.10–P2.15 | High |
