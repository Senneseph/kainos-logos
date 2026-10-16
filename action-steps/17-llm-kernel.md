# Action Step 17 — Production LLM kernel + E3.1 A/B (P3.01–P3.02)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

Productionize the LLM kernel (same interface as the deterministic kernel) and prove it
handles open phrasing the deterministic kernel cannot, with the CODEX/reasoner unchanged.

## Prerequisites

- [ ] Phase 1 complete (step 12 built the `LLMKernel` stub). Phase 2 optional for this step.

## Background

The kernel is just the language organ (invariant #2). Swapping a deterministic parser
for an LLM must not change anything downstream — that's what makes the comparison
clean. This step finishes the adapter started in step 12.

## Steps

### 1. `src/kainos/lang/llm.py`

- Configurable backend (local llama.cpp or hosted); `parse(text)` prompts the model
  to emit the dialect AST as JSON → validate against `specs/ir.schema.json` → build
  the dialect node. Retry once on validation failure (self-correction prompt).
- `realize(ir)` = emit (same as deterministic). `propose(ir)` = `[]` (reasoner still
  proposes in the full architecture).
- Deterministic fallback: if the LLM times out/errors, fall back to
  `DeterministicKernel` and mark the interpretation `score` lower.

### 2. Open-phrasing set

`data/regex/open_phrasing.jsonl`: descriptions using synonyms/idioms the deterministic
grammar doesn't cover ("match stuff that's just numbers and letters mixed", etc.).
Hand-label expected AST/PCRE.

### 3. E3.1 runner

`run_e3_1()`: LLM vs deterministic kernel on the open-phrasing set, **identical**
CODEX/reasoner in both arms. → `results/phase-3/e3.1.json`. Threshold: LLM ≥
deterministic on open phrasing.

## Verification

```bash
kainos experiment run --name e3.1
```

Expect: `llm_accuracy >= deterministic_accuracy` on the open set, with CODEX/reasoner
identical in both arms (assert same codex object reused).

## Done when

- [ ] `LLMKernel` validates its JSON output against the IR schema, retries once, falls back
- [ ] open-phrasing set exists
- [ ] E3.1 threshold met (LLM ≥ deterministic), downstream identical

## If stuck

`plan/30-phases/phase-3-generalization/experiments.md` → E3.1.
