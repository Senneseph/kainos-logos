# Phase 1 — Actions (concrete, ordered, verifiable)

Action IDs stable (`P1.xx`). Each names files and a verification.

---

## P1.01 — Regex IR dialect models

- `src/kainos/regex/ir.py`: enums + dataclasses for the dialect
  (`Node`, `Sequence`, `Repeat`, `Quantifier`, `Class`, `Literal`, `Anchor`,
  `Alternative`, `Group`, `Flag`, `UnresolvedRef`) with `to_generic()/from_generic()`
  mapping to the Phase 0 generic IR.
- **Verify:** `tests/regex/test_ir.py` — every node round-trips through the generic IR
  and back without loss.

## P1.02 — PCRE emitter

- `src/kainos/regex/emitter.py`: `emit(node) -> str` implementing spec.md §3 exactly.
- Escaping helper for `LITERAL`.
- **Verify:** `tests/regex/test_emitter.py` — table-driven tests for every rule +
  the two canonical examples from spec.md §3 (byte-exact).

## P1.03 — Deterministic language kernel

- `src/kainos/lang/deterministic.py`: `DeterministicKernel` implementing the
  `LanguageKernel` protocol (`parse`, `realize`, `propose`). Uses a small tokenizer +
  recursive-descent parser for spec.md §1. Emits `UNRESOLVED_REF` for vague terms.
- `src/kainos/lang/kernel.py`: the `LanguageKernel` protocol + `Interpretation`.
- **Verify:** `tests/lang/test_deterministic.py` — every clause template + every
  quantifier/class surface maps to the expected AST node.

## P1.04 — Lexicon as CODEX assertions

- Seed the CODEX with spec.md §1.2–§1.3 lexicon as assertions
  (`"hyphen" --realizes_as--> "-"`, `digit --realizes_as--> \d`, etc.), provenance
  `source=seed_corpus, status=established`.
- **Verify:** `tests/regex/test_codex_seed.py` — query each class/literal and assert
  the correct realization is returned; `dump` shows provenance on every assertion.

## P1.05 — Reasoner resolution step

- `src/kainos/regex/resolver.py`: walk the IR; for each node, query CODEX for its
  realization; for `UNRESOLVED_REF`, attempt **rotation** (spec.md §1.5) or mark
  `REQUIRES_CONTEXT` (→ escalation).
- **Verify:** `tests/regex/test_resolver.py` — "hyphen" resolves to `-`;
  "the dash thing" produces candidates and, when ambiguous, an escalation result.

## P1.06 — Test-case generator + judge

- `src/kainos/regex/testgen.py`: seeded positive/negative generator (spec.md §4).
- `src/kainos/regex/judge.py`: `compile` + `fullmatch` verdict with a diff of
  misjudged examples.
- **Verify:** `tests/regex/test_testgen.py` — generator covers every operator;
  judge rejects a deliberately wrong regex with a useful diff.

## P1.07 — End-to-end pipeline

- `src/kainos/regex/pipeline.py`: `describe(text) -> Result` composing
  kernel → IR → resolver → emitter → judge → trace.
- Result includes the **audit trace** (IR, resolved CODEX assertions, emitted PCRE,
  judge verdict) for C4.
- CLI: `kainos regex describe "..."` and `kainos regex explain "..."`.
- **Verify:** `tests/regex/test_pipeline.py` — the canonical example returns a
  passing verdict + trace.

## P1.08 — Seed corpus dataset

- `data/regex/seed_corpus.jsonl` (spec.md §3 canonical + every operator variant).
- A loader `src/kainos/regex/data.py`.
- **Verify:** `tests/regex/test_data.py` — corpus loads, is valid, unique ids, has
  `positive`/`negative` lists.

## P1.09 — E1.1 parity run

- Run pipeline over `seed_corpus`; write `results/phase-1/e1.1.json`.
- **Verify:** accuracy == 1.0; report table in `results.md`.

## P1.10 — Compositional set generator

- `src/kainos/regex/compose.py`: seeded cross-product of operators → novel
  descriptions + expected PCRE + tests (spec.md §4).
- **Verify:** `tests/regex/test_compose.py` — each generated item's expected PCRE
  passes the judge; assert no item duplicates a seed example.

## P1.11 — E1.2 compositionality vs. direct baseline

- Direct baseline = kernel → emitter with **no CODEX/resolver** (meanings hard-coded
  in the kernel), to isolate the CODEX's contribution.
- Run both over `compositional_set`; write `results/phase-1/e1.2.json`.
- **Verify:** threshold met (pipeline ≥ baseline + margin, pipeline ≥ 0.8).

## P1.12 — Persistent-memory teaching + restart (C2)

- Teach `US_PHONE_NUMBER` assertion; `describe("an American phone number")` succeeds.
- Dump CODEX to disk; instantiate a **fresh** pipeline (same kernel code, re-loaded
  CODEX); `describe` again succeeds.
- **Verify:** `tests/regex/test_persistence.py` — before/after both pass; explain
  shows provenance. (This is the document's "shut down / restart" experiment.)

## P1.13 — E1.4 vague-set + escalation (C3)

- `data/regex/vague_set.jsonl`; run pipeline; measure `clarification_rate`,
  `justified_rate`.
- **Verify:** thresholds met; `results/phase-1/e1.4.json`.

## P1.14 — LLM kernel + baseline (for E1.5)

- `src/kainos/lang/llm.py`: `LLMKernel` behind the same interface (local/hosted).
- Model A training script `scripts/train_baseline.py` (tiny seq2seq on seed pairs,
  excluding compositional set) + inference script.
- **Verify:** `tests/lang/test_llm_kernel.py` (mocked backend) proves interface
  compliance; baseline reproduces seed pairs.

## P1.15 — E1.5 A/B run + report

- Run A and B on `compositional_set` + `vague_set`; write `results/phase-1/e1.5.json`
  + `e1.5.md`.
- **Verify:** thresholds met; sign-off in `results.md`.

## P1.16 — Phase 1 results.md + sign-off

- `plan/30-phases/phase-1-regex/results.md`: all E1.1–E1.5 tables, exit criteria
  mapping, reuse stats (P0 artifacts consumed).
- **Verify:** every README exit criterion maps to an artifact path.

---

## Ordering notes

- P1.01–P1.08 are pure build (no experiments yet) but every one is test-gated.
- P1.09 is the first "claim" gate — do not proceed until parity is exact.
- P1.12 (persistent memory) is the emotional center of the whole project; give it
  the cleanest possible demo.
- P1.14–P1.15 (LLM A/B) may be done last and in parallel with Phase 2 planning if a
  model backend is slow to set up; E1.5 must still complete before Phase 1 sign-off.
