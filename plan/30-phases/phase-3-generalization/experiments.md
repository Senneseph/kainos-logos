# Phase 3 — Experiments (E3.1–E3.7)

---

## E3.1 — LLM kernel A/B (open phrasing)

- **Hypothesis:** An `LLMKernel` behind the same `LanguageKernel` interface handles
  open/vague phrasing the deterministic kernel cannot, while the CODEX path is
  unchanged.
- **Metric:** parse→IR fidelity on an open-phrasing regex/20Q set; downstream task
  accuracy with LLM vs deterministic kernel.
- **Threshold:** LLM kernel ≥ deterministic kernel on open phrasing, with **identical**
  CODEX/reasoner (isolates the kernel contribution).

## E3.2 — Fibonacci topology (gated)

- **Hypothesis:** A Fibonacci-structured residual recurrence
  `X_{n+2} = f(X_{n+1}) + X_n` (or Fibonacci info-capacity constraint) improves a
  measured metric on a toy supervised task vs. a same-budget MLP.
- **Metric:** accuracy / loss at matched parameter budget.
- **Threshold:** strictly better, with ≥3 seeds and a reported variance. If not,
  record **reject** and move on (P8).

## E3.3 — Distributed reconciliation

- **Hypothesis:** Two nodes trained on different facts reconcile a contradiction
  ("X" vs "NOT-X") by discovering a missing dimension (context/time/role), producing
  a higher-order TERM.
- **Metric:** both original assertions retained as `established` under distinct
  contexts; a new context TERM exists; `disputed` count → 0.
- **Threshold:** ≥1 new context TERM; zero averaged/blended facts.

## E3.4 — Multi-modal abstraction (synthetic)

- **Hypothesis:** A synthetic "vision" modality and text produce the *same* abstract
  CODEX pattern (e.g. `TRANSFER(object,A,B)`) and corroborate a shared entity.
- **Metric:** cross-modal corroboration (vision `canine 0.96` + text `"dog" 0.99`
  consolidate to one entity); pattern-match success.
- **Threshold:** one entity consolidated from ≥2 modalities; one abstract pattern
  recognized across modalities.

## E3.5 — φ numerics (gated)

- **Hypothesis:** A φ-exponent number format/bitwise kernel achieves better
  "useful computation per bit-op" than FP8/INT8 on a MAC-like or histogram-of-powers
  kernel.
- **Metric:** error-per-op at matched bit budget; ops per result.
- **Threshold:** strictly better with a written margin, else **reject**.

## E3.6 — Capability-faithful projection (X1/X2)

- **Hypothesis:** A planner restricted to *declared* capabilities (CODEX terms with
  preconditions/effects) finds valid plans for achievable goals and — critically —
  returns a **NO VALID PLAN** contract (named capability gap + nearest viable plan)
  for unachievable ones, never a hallucinated capability. Creative traversal
  (temperature > 0) produces varied outputs, all of which stay constraint-valid.
- **Setup:** a small simulated capability registry (e.g. `WRITE_TEXT`, `ASK_USER`,
  `SEARCH_CODEX`, `READ_SOURCE`) — **no image generator, no real side effects**;
  a goal set mixing achievable goals (e.g. produce a regex → `WRITE_TEXT` chain) and
  unachievable ones ("picture of a dragon"), plus one underspecified goal with a
  large plan space.
- **Metric:** (a) plan validity rate on achievable goals (every plan's effect chain
  actually reaches the goal, every precondition holds); (b) honest-refusal rate on
  unachievable goals (NO VALID PLAN with correct gap named, 0 fabricated actions);
  (c) creativity spread at T>0 (≥K distinct valid plans over a fixed goal, all
  constraint-satisfying, trace records T + seed).
- **Threshold:** (a) == 1.0; (b) == 1.0; (c) met with the spread floor. The
  search-space-aware clarification policy (choose/explore/ask/default) must pick
  "ask" on the constructed high-stakes ambiguous goal and "default" (recorded)
  on the low-stakes one.

## E3.7 — Recursive workspace memory (X3)

- **Hypothesis:** A WORKSPACE container can hold, nest, fork, revise, and *query*
  IRs; "what did we decide about X?" is answered by graph query without
  reprocessing the conversation; and promotion discipline holds — the CODEX gains
  only explicit, provenance-carrying candidates.
- **Setup:** a scripted project: workspace `PROJECT_GAME` with children
  `WORLD` → `TRANSPORT` and `COMBAT`; decisions recorded as IRs; one fork/revise
  cycle (transport decision changes); one `promote()` of a single IR; a SOURCE with
  two versioned analyses.
- **Metric:** query accuracy on "what did we decide about transportation?" (latest
  IR, post-revision); recursion depth ≥2 exercised; `promote()` output =
  candidate assertions with `source=workspace_<id>` (verified against the store);
  negative control: queries for un-promoted workspace content return **no** CODEX
  assertions.
- **Threshold:** all four checks pass; no un-promoted content visible in the CODEX
  (this is the anti-corruption invariant, P12).

## Reporting

All results → `results/phase-3/*.json` + `plan/30-phases/phase-3-generalization/results.md`
with a consolidated "did the unifying claim survive?" table.
