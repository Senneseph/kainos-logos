# Phase 1 — Results (sign-off)

- **Date / commit:** 2026-08-20 — sign-off commit closing step 12 (E1.5);
  per-experiment commits: E1.1 `a05bab0`, E1.2 `44bc63a`, E1.3/E1.4 `4079aa8`,
  E1.5 this commit.
- **Claims demonstrated:** C1 (compositional generalization), C2 (persistent
  memory), C3 (honest uncertainty) — claim IDs per `../../20-roadmap.md`.
- **Runtime note (owner decision 2026-08-20):** the E1.5 LLM runtime is the
  owner's local Ollama server (LAN, offline) with the model from `OLLAMA_MODEL`
  (snapshot recorded in experiment configs); it replaces the llama-server/GGUF
  pin in `plan/04-reality-check.md` §5. Model A (the trained baseline) needs no
  LLM at all. `torch==2.13.0+cpu` was added to the pinned lockfile
  (owner-approved: "as long as dependencies are pinned, we're good").

## Experiment results

| Experiment | Metric(s) | Threshold | Value | Pass |
|------------|-----------|-----------|-------|------|
| E1.1 seed parity | accuracy on 55-record seed corpus (every operator) | == 1.0 | **1.0** (55/55 byte-exact, all judge-verified) | ✅ |
| E1.2 compositionality | pipeline vs DirectBaseline on 40 novel combinations | ≥ 0.8; ≥ baseline + 0.1 | **1.0 vs 0.35** (margin 0.65) | ✅ |
| E1.3 persistence (C2) | teach → success → RESTART → success, frozen kernel, provenance shown | all 6 conditions | **passed** — before: escalation; after: `\d{3}-\d{3}-\d{4}`; restart: identical; judgment: real regex (matches 555-123-4567); provenance `user_instruction/1` | ✅ |
| E1.4 uncertainty (C3) | clarification_rate / justified_rate on 10-record vague set | ≥ 0.5; justified == 1.0 | **0.7 / 1.0** (7 escalate, 3 resolve via rotation, 0 unjustified) | ✅ |
| E1.5 A/B (C1) | B vs A on 20-record holdout + vague-set abstention | B > A; exact McNemar p ≤ 0.20; B abstains where A cannot | **1.0 vs 0.0, p = 2e-06**; vague: B abstains 7/10 + justified emits, A always emits (no abstention path) | ✅ |

All five persist as `results/phase-1/e1.{1..5}.json` (+ `.md` reports) and are
re-producible via `kainos experiment run --name <e1.x>` / `make bench`.

## What E1.5 actually showed (per-item, `results/phase-1/e1.5.json`)

Model A (char-level transformer seq2seq, dim 96, 2+2 layers, ~0.5M params,
trained 200 epochs / seed 42 on the **55 seed pairs only**):

- memorizes the training set (final loss 4.3e-06) and **mode-collapses on
  novel combinations**: 0/20 byte-exact holdout; outputs are degenerate runs
  (`....`, `----zz-`, `}}}}...`). Epoch sensitivity: 40/80/120-epoch variants
  also score 0/20 with the same collapse — the gap is architectural, not a
  recipe artifact.
- has **no abstention mechanism**: on the vague set it always emits (10/10).

Model B (the CODEX pipeline): 20/20 holdout byte-exact + judge-verified; on the
vague set it escalates 7/10 (`ask_human`) and resolves 3/10 purely via CODEX
neighborhood rotation — every emit carries a complete justification trace.

Exact McNemar on the 20 matched pairs: a_only = 0, b_only = 20, p = 2×2⁻¹⁹ ≈
2e-06. Threshold (`B > A`, p ≤ 0.20) met by six orders of magnitude.

## Exit-criteria mapping

| Criterion (phase README) | Evidence | Status |
|--------------------------|----------|--------|
| 1. E1.1 parity == 1.0 | `results/phase-1/e1.1.json` (55/55) | ✅ |
| 2. E1.2 pipeline ≥ 0.8 and ≥ baseline + 0.1 | `results/phase-1/e1.2.json` (1.0 vs 0.35) | ✅ |

**Borrowed mechanism (M-ID, ADR-0013):** **M1 — specialization / materialization
cache ADOPTED** in `regex/resolver.py` (`SpecializationCache`, key =
(abstraction, context-signature), seam-neutral: OFF ⇒ byte-identical). Final
verdict on the E1.2 compositional set (scavenge sweep 2026-08-22): cached vs
uncached resolution **byte-identical at a 1.60x wall-time margin** (916µs →
574µs, 51 hits / 5 misses, 40 records) — `results/scavenge/m1.json` (interim
seed-corpus run preserved as `m1-seed-corpus.json`). Verdict line: ADR-0013 §4.
| 3. C2 + C3 (E1.3/E1.4) | `results/phase-1/e1.3.json`, `e1.4.json`, `tests/regex/test_persistence.py` (6 tests) | ✅ |
| 4. E1.5 B > A, B abstains | `results/phase-1/e1.5.json` + `e1.5.md` (p = 2e-06) | ✅ |
| 5. Reuse stats + sign-off | below | ✅ |

## Reuse stats (compounding contract)

Phase 0 artifacts **consumed, not rewritten**:

| P0 artifact | P0 LOC | P1 treatment |
|-------------|-------:|--------------|
| `src/kainos/codex/` (models, store, memory, sqlite, explain) | 875 | consumed as-is; **one** additive protocol member (`generation`, +~30 LOC) for the M1 cache |
| `src/kainos/ir/` (schema, codec) | 228 | consumed as-is; regex dialect maps losslessly onto `kainos/ir/1` |
| `src/kainos/harness/` (runner, report) | 382 | consumed as-is; registry extended 1 → 3 → 6 experiments |
| `src/kainos/cli.py` | 367 | two additive domains (`regex`, `modela`) |
| P0 golden files / CI / pinned image | — | golden IR + CI gates kept green throughout |

New P1 surface: `src/kainos/lang/` (769 LOC: deterministic kernel, LLMKernel),
`src/kainos/regex/` (2850 LOC: dialect, emitter, resolver, testgen, judge
client, pipeline, compose, bench), `src/kainos/llm/` (360 LOC: Model A +
training). P1 is 68% of the current `src/` LOC — and the P0 33% is what makes
the compounding contract visible: the regex pipeline was built **on** the
CODEX/IR/harness, never around them. Test surface: 3609 LOC / 382 tests, all
green; `make lint` + `make typecheck` clean (34 source files).

## Deviations recorded (for the next reviewer)

1. **E1.5 runtime** — owner's Ollama (LAN) instead of llama-server + pinned
   GGUF (reality-check §5 updated; owner direction, 2026-08-20). E1.5 itself
   does not call any LLM: Model A is the in-repo torch baseline, Model B is the
   deterministic pipeline. The Ollama server serves the `LLMKernel` seam
   (step-17 territory) and is smoke-tested when reachable.
2. **`scripts/` paths in directives 08/12** (`judge.pl`,
   `train_baseline.py`, `predict.py`) live in-package
   (`src/kainos/regex/judge.pl`, `kainos.llm.train`) because the user-managed
   root `.gitignore` excludes `scripts/` — that file is never modified.
3. **`Literal.raw`** (additive; `kainos:raw` marker label) — CODEX-taught
   values are regex fragments, never escaped literal text (E1.3's taught
   phone pattern is judge-verified as a real regex).
4. **`torch==2.13.0+cpu`** appended to the pinned lockfile (CPU index, hashes;
   owner-approved, 2026-08-20).

**Phase 1 is DONE.** Steps 06–12 ✅. Next: `action-steps/13-q20-corpus-oracle.md`
(plus the open Scavenge steps C–I on the board).
