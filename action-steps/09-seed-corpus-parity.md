# Action Step 09 — Seed corpus + E1.1 parity (P1.08–P1.09)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

A hand-authored seed corpus covering every operator, and proof (E1.1) that the pipeline
achieves 100% parity on it.

## Prerequisites

- [ ] Steps 06–08 done (full pipeline works).

## Background

The seed corpus is the *explicit form* of the grammar — the only thing the
deterministic kernel is "trained" on. E1.1 is the first claim gate: the pipeline must
translate every seed description exactly. Do not proceed to compositionality until
parity is exact.

## Steps

### 1. `src/kainos/regex/data.py`

`load_corpus(path) -> list[dict]` — each record
`{id, description, expected_pcre, positive: [str], negative: [str]}`.

### 2. `data/regex/seed_corpus.jsonl`

Author ~40–80 records, one per operator + representative combinations. Must cover:
every quantifier (one_or_more, zero_or_more, optional, exactly N, at_least N, at_most N,
between N M), every class, both anchors, `Literal` (incl. a metachar like `.` to test
escaping), `Alternative`, `Group`, `Flag(case_insensitive)`. Include the two canonical
examples from step 06. Each record needs non-empty `positive` and `negative` lists.

### 3. E1.1 runner

`src/kainos/regex/bench.py` — `run_e1_1()`: for each corpus record, `describe` it,
compare `pcre` to `expected_pcre` **and** judge against `positive`/`negative`.
Write `results/phase-1/e1.1.json` with `{config, accuracy, per_item:[{id, ok, pcre, expected}]}`.

Register E1.1 in the harness registry (`kainos.harness.runner.REGISTRY`) with
`name="e1.1"`, `metric="accuracy"`, `threshold="== 1.0"`.

## Verification

```bash
kainos experiment run --name e1.1 && python -c "import json;d=json.load(open('results/phase-1/e1.1.json'));print(d['accuracy'])"
```

Expect: `accuracy == 1.0`.

## Done when

- [ ] seed corpus covers every operator (assert in a test: all operators present)
- [ ] E1.1 accuracy == 1.0
- [ ] `results/phase-1/e1.1.json` written with config + per-item details
- [ ] harness registry includes `e1.1`

## If stuck

`plan/30-phases/phase-1-regex/benchmarks.md`, `plan/30-phases/phase-1-regex/experiments.md` → E1.1.
