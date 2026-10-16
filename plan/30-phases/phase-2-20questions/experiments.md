# Phase 2 — Experiments (E2.1–E2.5)

---

## E2.1 — Active knowledge acquisition (A1)

- **Hypothesis:** Information-gain question selection converges in fewer questions
  than a random baseline.
- **Metric:** median `questions-to-solve` and `win-rate` vs. random baseline, over
  ≥500 seeded games on the corpus.
- **Threshold:** system median < baseline median (≥20% fewer) and win-rate ≥ baseline.

## E2.2 — EXCEPTION shrinkage (A2)

- **Hypothesis:** As games accumulate, `Coverage(T,C)` rises and the count of
  `UNSEEN`/`UNRESOLVED` exceptions falls — the ontology becomes more expressive.
- **Metric:** coverage + exception count sampled every K games; report the trend
  (monotone improvement or a plateau with explanation).
- **Threshold:** coverage increases and exception count decreases across the run
  (statistically, not by eyeball).

## E2.3 — Persistent growth across restart (A3)

- **Hypothesis:** Knowledge learned in game set 1 improves game set 2 after a full
  restart, with frozen neural weights.
- **Metric:** questions-to-solve on a *held-out* concept set in game set 2, with vs.
  without the CODEX from game set 1 (ablation).
- **Threshold:** with-persistence < without-persistence (fewer questions), and the
  learned assertions are present post-restart.

## E2.4 — Compositional concept recognition (A4)

- **Hypothesis:** The system guesses a concept it has *no label for* by conjoining
  learned properties (`manufactured + vehicle + two wheels + human powered → bicycle`).
- **Metric:** accuracy on a set of concepts whose labels were held out but whose
  properties were learned.
- **Threshold:** accuracy ≥ 0.7 (vs. a "can only guess labeled concepts" baseline
  at ~0).

## E2.5 — Ontology expansion via contradiction (A5)

- **Hypothesis:** A repeated `sometimes`/conflict (`bear hibernates` vs `polar bear
  doesn't`) yields a new context TERM (e.g. `species`) rather than a blended weight.
- **Metric:** # new context TERMs created, and the re-expressed assertions are both
  retained as `established` under distinct contexts (P6).
- **Threshold:** ≥1 new context TERM; both original assertions retained (not
  averaged); `disputed` count == 0 for that pair after reconciliation.

## Reporting

All results → `results/phase-2/*.json` + the growth dashboard
(`results/phase-2/growth.md`) + `plan/30-phases/phase-2-20questions/results.md`.
