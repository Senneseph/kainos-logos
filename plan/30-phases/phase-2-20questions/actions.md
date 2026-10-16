# Phase 2 — Actions (concrete, ordered, verifiable)

Action IDs stable (`P2.xx`).

---

## P2.01 — Concept corpus + property oracle

- `data/q20/concepts.json`: 100–300 concepts (animals, objects, foods, vehicles,
  places, people) each with a property table (spec above).
- `src/kainos/q20/oracle.py`: seeded, deterministic `answer(concept, question) ->
  yes/no/unknown/sometimes`.
- `data/q20/questions.json`: the valid question set (property probes + category
  probes).
- **Verify:** `tests/q20/test_oracle.py` — deterministic; `unknown` for undefined
  property; `sometimes` for a marked conditional property.

## P2.02 — Corpus → CODEX seed

- Load `concepts.json` as assertions (`bicycle --has_property--> manufactured=true`,
  `bicycle --is_a--> vehicle`, …) with `source=corpus, status=established`.
- **Verify:** `tests/q20/test_seed.py` — every concept/property present; `dump`
  shows provenance; no bare edges (ADR-0008).

## P2.03 — Question parser (reuse Phase 1 kernel)

- Extend the deterministic kernel with the 20Q question grammar (spec §Question
  grammar). Produce `Query` IR (`CONSTRAINT`, `HYPOTHESIS`).
- **Verify:** `tests/q20/test_question_parse.py` — each template maps to the right
  `Query`; unknown phrasing → `UNRESOLVED_REF`.

## P2.04 — Hypothesis-space engine

- `src/kainos/q20/hypothesis.py`: `HypothesisSpace` (consistent set H), `apply(constraint)`,
  `entropy()`, `split(question)`.
- **Verify:** `tests/q20/test_hypothesis.py` — applying `alive=no` removes all alive
  concepts; entropy is 0 when |H|=1; split partitions correctly.

## P2.05 — Information-gain selector

- `src/kainos/q20/selector.py`: `best_question(H, questions)` maximizing IG with the
  tie-breaks from spec (shrink EXCEPTION, then cost).
- **Verify:** `tests/q20/test_selector.py` — a near-median-split question is chosen
  over a lopsided one; tie-break order respected.

## P2.06 — Game loop + win detection

- `src/kainos/q20/game.py`: `Game` state machine (ask → answer → update → guess/end),
  budget enforcement, `make_guess(H)` (when |H| small or IG < stop threshold).
- **Verify:** `tests/q20/test_game.py` — a scripted oracle yields a correct guess
  within budget; budget exhaustion → loss; wrong guess recorded.

## P2.07 — Learning loop (post-game consolidation)

- `src/kainos/q20/learn.py`: turn answers into candidate assertions → verify against
  existing → consolidate (`established`) → detect `sometimes`/conflicts → propose new
  context TERM (A5).
- **Verify:** `tests/q20/test_learn.py` — a `sometimes` answer creates a candidate
  context TERM; a repeated conflict re-expresses both assertions without averaging.

## P2.08 — Baselines

- `src/kainos/q20/baselines.py`: `RandomQuestioner`, `StatelessGreedy` (no
  persistence).
- **Verify:** `tests/q20/test_baselines.py` — random is valid and non-deterministic
  (seeded reproducible); stateless ignores CODEX history.

## P2.09 — Growth dashboard

- `src/kainos/q20/dashboard.py`: sample `Coverage(T,C)` + exception count per K games;
  render `results/phase-2/growth.md`.
- **Verify:** `tests/q20/test_dashboard.py` — coverage computed correctly on a tiny
  fixture; output file renders.

## P2.10 — E2.1 active-acquisition run

- Run ≥500 games (system vs random) over the corpus; write `results/phase-2/e2.1.json`.
- **Verify:** thresholds met.

## P2.11 — E2.2 exception-shrinkage run

- Run a long sequence of games; write coverage/exception trend to `growth.md` +
  `e2.2.json`.
- **Verify:** thresholds met.

## P2.12 — E2.3 persistence + restart

- Split corpus: train on set 1, dump CODEX, restart (fresh pipeline, reload CODEX),
  play set 2. Ablation: no-CODEX control. Write `e2.3.json`.
- **Verify:** with-persistence beats without-persistence.

## P2.13 — E2.4 compositional inference

- Hold out labels for a concept subset (properties still learned); measure inference.
  Write `e2.4.json`.
- **Verify:** accuracy ≥ 0.7.

## P2.14 — E2.5 contradiction → dimension

- Inject the `bear`/`polar bear` hibernation conflict; run the learning loop; assert
  a new context TERM. Write `e2.5.json`.
- **Verify:** ≥1 new context TERM; both assertions retained as `established`.

## P2.15 — Phase 2 results.md + sign-off

- `plan/30-phases/phase-2-20questions/results.md`: E2.1–E2.5 tables, growth curve,
  exit-criteria mapping, reuse stats (P0+P1 artifacts consumed).
- **Verify:** every README exit criterion maps to an artifact path.

---

## Ordering notes

- P2.01–P2.09 build the game; P2.10 begins the experiments. Do not skip the
  baselines (P2.08) — they are what make A1/A3 claims *falsifiable* rather than
  "it works, trust me".
- E2.3 (persistence) and E2.5 (contradiction) are the two most important results for
  the project's thesis; invest most debugging effort there.
