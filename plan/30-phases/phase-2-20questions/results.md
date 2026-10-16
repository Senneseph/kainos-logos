# Phase 2 — Results (sign-off)

> Filled in by step 16 (`action-steps/16-q20-e2-runs.md`).

- **Date / commit:** 2026-08-20 — sign-off commit closing step 16 (E2.1–E2.5 + this
  file). Step commits: 13 = `f33609f`, 14 = `3a0bfa6`, 15 = `ccb1f4a`, 16 = this
  commit.
- **Claims demonstrated:** A1 (info-gain selection — measured by *convergence*; see
  deviation D1), A2 (EXCEPTION shrinkage), A3 (persistent growth across restart),
  A4 (compositional recognition), A5 (contradiction → dimension) — claim IDs per
  `../../20-roadmap.md`.

## Experiment results

| Experiment | Metric(s) | Threshold | Value | Pass |
|------------|-----------|-----------|-------|------|
| E2.1 active acquisition (A1) | questions-to-solve median + win-rate, 500 seeded games each | system ≥20% fewer; win-rate ≥ baseline | solved-games median **17 vs 17** (0% fewer); win-rate **0.262 vs 0.326** — both at the corpus's 0.3087 ceiling; **convergence: median 4.0 vs 11.0 questions (−63.6%)** | ❌ (D1) |
| E2.2 EXCEPTION shrinkage (A2) | coverage ↑ + unknown remainder ↓, 200 games from an EMPTY CODEX, sampled every 25 | monotone, strict end-to-end delta | coverage **0.0 → 0.349** (monotone), unknown cells **1490 → 1150** (−340), dimensions **0 → 6**, sometimes **0 → 43** | ✅ |
| E2.3 persistent growth (A3) | median oracle (world) queries per held-out set-2 game, with vs without the persisted CODEX after a true restart | with < without; learned assertions survive | **4166 vs 4880 (−14.6%)**; 369 learned assertions; `learned_present_after_restart = true` (dump → `Assertion.from_dict` round-trip, same seam as E1.3) | ✅ |
| E2.4 compositional recognition (A4) | accuracy on 12 label-held-out concepts (the vector-identifiable region, D3); labels given: 0 | ≥ 0.7 (zero-label baseline) | **1.0 (12/12)** vs baseline 0.0 | ✅ |
| E2.5 contradiction→dimension (A5) | new context TERM; both sides retained, not averaged; disputed → 0 | ≥1 new TERM; distinct contexts; dispute reconciled | new `dim:hibernates`; both `hibernates=no` / `hibernates=yes` retained under **2 distinct contexts**; disputed **2 → 0**, both re-`established` | ✅ |

All five persist as `results/phase-2/e2.{1..5}.json` (+ `SUMMARY.md` rendered by
`kainos experiment report --phase 2`) and are re-producible via
`kainos experiment run --phase 2`.

## What E2.1 actually showed (deviation D1 in detail, `results/phase-2/e2.1.json`)

The directive threshold (questions-to-solve median ≥20% lower **and** win-rate ≥
baseline) is **structurally unreachable on the published corpus**:

- The 149 concepts form **46 equivalence classes** under the 17 questions
  (size distribution: 1×20, 2×10, 3×4, 4×3, 5×3, 6×2, 7×1, 13×1, 14×1, 24×1 —
  incl. a 24-way `objects` class: table, chair, door, window, phone, computer,
  …). Class members share answers to *every* question, so **no question policy**
  can distinguish them.
- **Win-rate is capped at 46/149 = 0.3087 for ANY policy**: both policies end in
  the same terminal state (the target's equivalence class) and share the same
  `min(H)` fallback guess. The deterministic 500-game seed lands at 0.262 vs
  0.326 — a coin toss around the shared ceiling, not a policy difference. No
  re-seeding was attempted; the numbers are what the published seed gives.
- **Questions-to-solve is dominated by class-min wins**, which are decidable only
  after *all* 17 questions for either policy → both medians pin at 17 (0% fewer).

The A1 hypothesis itself — "information-gain question selection **converges** in
fewer questions than a random baseline" — is **strongly supported** when measured
against the corpus's identifiability floor: the system reaches the minimal H it
can reach in a **median of 4.0 questions** (mean 4.21) vs **11.0** (mean 10.66)
for random → **−63.6% median convergence**. Worked example: `mushroom` is
identified in 2 questions (`made=unknown` → H 149→15; `green=no` → 15→1).

**Owner decision required at sign-off** (milestone #134):
(i) accept the recorded E2.1 verdict as a deviation, with A1 supported on the
convergence metric; (ii) redirect E2.1 (e.g. threshold on questions-to-identify,
or a fully-identifiable corpus); (iii) otherwise. No threshold was loosened and
no seed was re-rolled.

## Growth curve (E2.2 — empty CODEX start → 200 games; full narrative in
`results/phase-2/growth.md`)

| game | coverage_mean | unknown_cells | sometimes | dimensions | assertions |
|-----:|--------------:|--------------:|----------:|-----------:|-----------:|
| 0 | 0.0000 | 1490 | 0 | 0 | 0 |
| 25 | 0.0134 | 1422 | 5 | 2 | 236 |
| 50 | 0.0470 | 1359 | 8 | 4 | 472 |
| 75 | 0.0872 | 1304 | 15 | 5 | 696 |
| 100 | 0.1678 | 1270 | 20 | 6 | 944 |
| 125 | 0.2215 | 1245 | 25 | 6 | 1171 |
| 150 | 0.2550 | 1203 | 35 | 6 | 1392 |
| 175 | 0.3087 | 1172 | 40 | 6 | 1621 |
| 200 | 0.3490 | 1150 | 43 | 6 | 1857 |

Coverage is `verified_combinations / encountered_combinations` per
`plan/02-glossary.md` (mean over all 149 concepts). The mechanism: a first
visit to a concept leaves *unverified candidates* (coverage 0 for those
cells); a second visit is an independent corroboration → both sides
`established` with `provenance.verified=True` (D-m2) → coverage rises per
repeat. Unknown cells only ever fall (absence is never written). Six dimension
TERMs (`dim:can_carry_person`, `dim:has_engine`, `dim:has_wheels`,
`dim:is_green`, `dim:lives_in_water`, `dim:manufactured`) emerged from
`sometimes` cells in the same curve — A2 and A5 compounding in one run.

## Exit-criteria mapping

| Criterion (phase README) | Evidence | Status |
|--------------------------|----------|--------|
| 1. E2.1–E2.5 run green and are reported | `results/phase-2/e2.{1..5}.json` + `SUMMARY.md`: all five ran and are reported; E2.2–E2.5 green; **E2.1's directive threshold unmet (D1)** | ⚠️ pending owner ruling on D1 |
| 2. Growth dashboard shows exception space shrinking across ≥N games | `growth.md` + `e2.2.json`: 200 games; unknown 1490 → 1150, coverage monotone 0.0 → 0.349, 6 dimensions | ✅ |
| 3. Restart demo: train set 1 → restart → set 2, retention + improvement, frozen kernel | `e2.3.json`: `store.dump()` → `Assertion.from_dict` round-trip (same seam as E1.3); 369 assertions retained; world queries −14.6% | ✅ |
| 4. `results.md` with metric tables + growth curve | this file | ✅ |
| 5. Self-abstraction signal (designer-unknown TERM?) | E2.5's `dim:hibernates` is a system-generated context TERM for the canonical conflict — **kill criterion K3 (reality-check §4) not triggered**: the term is clean, human-sign-off-able, registered as knowledge (`declares_dimension`), and closes the dispute by *explaining* it. The six runtime dimensions in E2.2 are generated at run time from the corpus's seeded `sometimes` cells, not enumerated in any data file. Fully open surface (new property words from the LLM parser) is step-17 territory | ✅ |

## Reuse stats (compounding contract)

Phase 0–1 artifacts **consumed, not rewritten**:

| Artifact | LOC | P2 treatment |
|----------|----:|--------------|
| `src/kainos/codex/` (models, store, memory, sqlite, explain) | 875 | consumed as-is — assertions, provenance, coverage, dump are the *entire* learning substrate |
| `src/kainos/ir/` (schema, codec) | 228 | untouched (the 20Q question grammar carries its own `Query` IR; the Phase-1 kernel *pattern* — template match → typed node, unknown → `UnresolvedRef` — is reused, not the package) |
| `src/kainos/harness/` (runner, report) | 391 | consumed as-is; registry extended 6 → 11 experiments; one bug fix (phase filter in `load_results` + regression test, D-m3) |
| `src/kainos/cli.py` (`experiment run/report` domain) | 389 | consumed as-is for the official runs + SUMMARY rendering |
| `src/kainos/regex/` (Phase-1 surface) | 2850 | **not consumed by 20Q** (different task surface); kept green untouched |
| `src/kainos/lang/` + `src/kainos/llm/` | 769 + 360 | untouched; the `LLMKernel`/`OllamaBackend` seam is what step 17 builds on |

New Phase-2 surface: `src/kainos/q20/` — **1822 LOC across 11 modules**
(oracle 114, seed 81, question_parse 139, hypothesis 70, selector 73, game 139,
baselines 98, learn 257, dashboard 90, bench 736, `__init__` 25). `src/` is now
7685 LOC / 45 files; Phase 2 is 24% of the tree, built **on** the P0/P1 code,
never around it. Test surface: 4530 LOC / 43 files (tests/q20: 887 LOC).

**CODEX continuity:** same assertion schema, same store protocol, same
provenance rules as P0/P1. The 20Q world is *seeded into the CODEX* (641
assertions, `q20_corpus/1`), and E2.2/E2.3 show the CODEX — not the weights —
is the only thing that grows across games and across a process restart.

Gate: **445 passed / 2 skipped** (live-Ollama smoke + `KAINOS_SLOW` retrain),
ruff clean, mypy clean (45 files).

## Deviations recorded (for the next reviewer)

1. **D1 — E2.1 verdict** (owner decision required). The directive threshold is
   structurally unreachable on the published corpus (identifiability ceiling
   46/149; shared terminal state + shared `min(H)` guess; class-min wins pin
   both questions-to-solve medians). `e2.1.passed = false` is recorded with the
   full evidence incl. the ceiling computation; A1 is supported on the
   convergence metric (−63.6% median). No re-seeding, no threshold change.
2. **D2 — E2.3 metric** = median oracle (world) *queries* per set-2 game with
   the persisted CODEX vs empty (codex answers are free; the world is queried
   less). Question *counts* are identical by construction (the CODEX answers
   with the same values the world would), so queries — not counts — are the
   pass metric; selector partition probes count as world queries. Stated in
   the JSON `config.codex_answer_policy`.
3. **D3 — E2.4 holdout** = the vector-identifiable region (12 of the 20
   concepts with unique 17-answer vectors): twins (pig=sheep, the 24-way
   objects class, …) are unrecognizable by *any* property conjunction, so the
   designed A4 testable region is, like a holdout, the identifiable one.
4. **D4 — E2.5 world injected** (bear/polar_bear + `q_hibernates`): the
   canonical conflict is not in the seeded corpus (the corpus has no
   hibernation property); it enters as established assertions with provenance
   `e2.5_injection/1` and the probe passes through
   `consolidate(..., extra_questions=...)`.
5. **D-m1 — `GreedyIGPolicy` asks each question at most once** (the 20Q rule,
   matching the deck semantics `RandomQuestioner` documents). Previously it
   re-asked the same question endlessly once IG plateaued (H had reached the
   target's equivalence class), burning the budget — visible as wasted
   questions in every E2.1 twin-class game.
6. **D-m2 — `_verify` corroboration bootstrap**: two independent same-value
   observations now both become `established` with `provenance.verified=True`
   (the game-spec learning loop: "verify (consistent with existing?) →
   consolidate (status=established)"). Previously promotion required an
   *already-established* sibling, so from an empty CODEX nothing could ever be
   established (bootstrap problem) and E2.2's coverage was stuck at 0.0.
7. **D-m3 — harness `load_results` phase-filter bug** (looked up key `e2.` in
   a map keyed by `e2`) — phase reports could never render ("no persisted
   results"); fixed with a regression test in `tests/harness/test_runner.py`.
8. **D-m4 — q20 data paths** get a package-anchored repo-root fallback (the
   Phase-1 regex-bench convention) so harness runs from a tmp CWD can find
   `data/q20/`.

**Phase 2 is DONE** — code, results, gate, and the sign-off document are
complete; the milestone awaits the owner's ruling on **D1** (#134).
Steps 13–16 ✅. Next: `action-steps/17-llm-kernel.md` (production LLM kernel —
where the owner's Ollama model comes in).
