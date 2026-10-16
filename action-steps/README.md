# action-steps/ — Executable task directives

This folder turns the plan in `plan/` into **self-contained, sequential, prompt-like
directives**. Each file is a single unit of work that can be handed to a fresh agent
(or pasted into an AI) and executed to completion.

## The zero-knowledge contract

Each directive is designed so you do **not** need to read `PROJECT_OVERVIEW.md` or the
full plan. You need at most two files:

1. **`00-CONTEXT.md`** — read once. The irreducible background (what we're building,
   the invariants, the repo layout, the conventions). ~1 page.
2. **The current directive** (e.g. `06-regex-ir-emitter.md`) — follow it top to bottom.

Pointers to `plan/…` files inside a directive are *optional* "if stuck" references,
never required reading.

**`LAYOUT.md`** is the optional cross-reference: which directive creates which durable
path, plus the directory conventions and any layout gaps to resolve before executing.

## How to use

- Work through the files **in numeric order**. Each lists its prerequisites.
  **Ordering exception (Phase 3):** `21-projection-planning.md` and
  `22-workspace-memory.md` run **before** `20-multimodal-final.md` — directive 20 is
  the final consolidation and always runs last, despite its number.
- A directive is **done** only when its "Done when" checklist is fully checked and its
  verification command passes.
- After finishing a directive, mark it done in the ledger below (change ⬜ → ✅).

## Ledger

| # | File | Maps to | Status |
|---|------|---------|--------|
| 01 | `01-scaffold.md` | P0.01 | ✅ |
| 02 | `02-codex-model-store.md` | P0.02–P0.03 | ✅ |
| 03 | `03-codex-explain-ir.md` | P0.04–P0.05 | ✅ |
| 04 | `04-golden-cli.md` | P0.06–P0.07 | ✅ |
| 05 | `05-harness-ci.md` | P0.08–P0.10 | ✅ |
| 06 | `06-regex-ir-emitter.md` | P1.01–P1.02 | ✅ `32079f6` |
| 07 | `07-kernel-lexicon.md` | P1.03–P1.04 | ✅ `49f1d98` |
| 08 | `08-resolver-judge-pipeline.md` | P1.05–P1.07 | ✅ `a92cbac` |
| 09 | `09-seed-corpus-parity.md` | P1.08–P1.09 | ✅ (E1.1 = 1.0; this commit) |
| 10 | `10-compositionality.md` | P1.10–P1.11 | ✅ (E1.2: pipeline 1.0 vs baseline 0.35; this commit) |
| 11 | `11-persistence-uncertainty.md` | P1.12–P1.13 | ✅ (E1.3 all 6 conditions; E1.4 clar 0.7 / justified 1.0; this commit) |
| 12 | `12-llm-ab-baseline.md` | P1.14–P1.16 | ✅ (E1.5: B 1.0 vs A 0.0, p=2e-6; Phase 1 signed off — this commit) |
| 13 | `13-q20-corpus-oracle.md` | P2.01–P2.02 | ✅ `f33609f` |
| 14 | `14-q20-hypothesis-selector.md` | P2.03–P2.06 | ✅ `3a0bfa6` |
| 15 | `15-q20-learning-dashboard.md` | P2.07–P2.09 | ✅ `ccb1f4a` |
| 16 | `16-q20-e2-runs.md` | P2.10–P2.15 | ✅ (E2.2–E2.5 green: coverage 0.0→0.349, queries −14.6%, accuracy 1.0, dim:hibernates; E2.1 recorded FAIL on the directive threshold — deviation D1, owner ruling at sign-off; this commit) |
| 17 | `17-llm-kernel.md` | P3.01–P3.02 | ✅ (E3.1 pass: LLM 1.0 vs deterministic 0.0 on the 12-item open set, byte-exact 11/12, 0 fallbacks, shared CODEX across arms; P3.01: schema-validated + retry + fallback (score-marked) LLMKernel, pipeline kernel seam, harness SKIP semantics; D1–D3 + D-m1 documented; this commit) |
| 18 | `18-numerics-topology.md` | P3.03–P3.05 | ✅ (Numerics seam + inert FloatNumerics default (E1.1 unchanged, 23 tests) + PhiNumerics (s·φ^n, exponent-add multiply, Fibonacci-carry normalize); E3.5 φ vs FP8/INT8 @8-bit: REJECT — err/op winner (−41%), hist L1 0.0, but 2.07× the best ops/result; E3.2 vs same-budget MLP @115 params: ADOPT — recurrence wins all 3 seeds, +6.87% mean test RMSE (contradicts the plan's null expectation — recorded as-is); ADR-0014/0015; D4–D6 + D-m2/D-m3 documented; this commit) |
| 19 | `19-distributed-codex.md` | P3.06–P3.08 | ✅ (AssertionDelta semantic-transaction contract (specs/assertion_delta.schema.json, mirrors kainos/codex/1) + idempotent conflict-preserving merge (both sides disputed, cross-linked evidence both directions, no averaging) + reconciler: contradiction → candidate-dimension search (time/location/role/modality/context, plan's list verbatim) → new context TERM ctx:D:subject declared as knowledge; unexplainable stays disputed (honest negative); E3.3 two-node bear story: winter yes vs summer no → all 6 checks met on both nodes (TERM on both, disputed 4→0, converged identical knowledge, idempotent re-merge incl. round-trip dups); ADR-0016; D7 + D-m5 documented; this commit) |
| 20 | `20-multimodal-final.md` | P3.09–P3.11 | ✅ (multimodal layer: PerceptionPort (declared grammars, reject-outside-grammar) + SyntheticVisionPort (scene → located_at IR, ir/1-validated); one modality-blind abstract_pattern step; E3.4: text "John moved the box" + box scene BOTH reduce to TRANSFER(object=box) (modality-specific parts preserved), entity `box` consolidated from 2 modalities with per-modality CODEX provenance; FINAL consolidation: all 8 acceptance checks ✅ with evidence, 5 north-star criteria mapped, unifying-claim FINAL (ADOPT topology / REJECT numerics / PASS gates), one-test verdict recorded (ctx:time discovery + replication), SUMMARY.md rendered (7 experiments); results-hygiene root-cause fix (KAINOS_RESULTS_DIR + tests/conftest.py + load_results value-required) — test runs no longer touch repo results/; ADR-0019; **ALL STEPS COMPLETE — PROJECT DONE** this commit) |
| 21 | `21-projection-planning.md` | P3.12–P3.14 | ✅ (projection layer: capabilities as CODEX terms (P11, add/remove = store ops, no image capability by design); bounded no-repetition plan search w/ acceptance-chain proof; NoValidPlan = named unmeetable gap + longest valid-progress prefix + full trace; 7 response contracts as data; constrained T-traversal (pruning invariant: established negative facts never violated); E3.6: validity 1.0, refusal 1.0 (gap image_capability, zero fabricated steps), 4 distinct valid plans at T>0 (floor 2), T=0 deterministic, policy ask/default (default applied from has_default, recorded); 43 tests incl. hypothesis P11 property; ADR-0017; D8/D9/D-m6 documented; this commit) |
| 22 | `22-workspace-memory.md` | P3.15–P3.17 | ✅ (workspace layer: containers — recursive/lifetime-scoped/queryable/forkable/JSON-round-trippable (query = BFS over all IRs at all depths, sorted rows); sources ≠ analyses — immutable append-only versioning + latest_analysis + hash-change stale-flagging via derived_from; promotion — explicit, idempotent, candidate-only, source=workspace_<root_id> (role resolved recursively, unique-or-error); lapse → results storage, never the CODEX; E3.7: query accuracy 1.0 at recursion depth 2, fork isolation true, 1 candidate assertion with correct provenance, NEGATIVE CONTROL PASSED IN THE RESULT FILE (un-promoted IR → zero CODEX assertions), 2 append-only analyses latest v2 with stale-flagging; 19 tests; ADR-0018; D10/D-m7 documented; this commit) |

## Directive template (keep new directives consistent)

```markdown
# Action Step NN — <Title>
> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal (one sentence: what exists when done)
## Prerequisites (checked box = prior directive done)
## Background (30 seconds)
## Steps (numbered, exact paths/commands/signatures)
## Verification (exact command + expected output)
## Done when (checklist)
## If stuck (optional pointer into plan/)
```
