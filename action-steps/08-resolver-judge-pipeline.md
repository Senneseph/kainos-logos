# Action Step 08 — Resolver + testgen/judge + pipeline (P1.05–P1.07)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

The end-to-end pipeline: resolve the AST against the CODEX, emit PCRE, generate test
cases, execute, and return a verdict **with an audit trace**.

## Prerequisites

- [ ] Steps 06–07 done (emitter + kernel + lexicon).

## Background

The resolver is where the architecture earns its keep: an `UnresolvedRef` ("the dash
thing") is resolved by **rotation** through the CODEX or escalated. The judge is the
objective arbiter — it *executes* the regex against generated examples, so "correct"
means "matches the intended language", not "looks plausible".

## Steps

### 1. `src/kainos/regex/resolver.py`

`resolve(node: Node, codex) -> Resolved` where `Resolved = (node, trace: list[dict])`.

- Walk the AST. For each `Class`, look up its `realizes_as` in the CODEX (lexicon from
  step 07) and record a trace entry `{term, realized_as, assertion_id}`.
- For `UnresolvedRef`, attempt **rotation**: query CODEX neighbors of each candidate;
  if exactly one candidate's realization is reachable → resolve to it; if several →
  keep as unresolved and record `status=REQUIRES_CONTEXT` with candidates; if none →
  `UNSEEN`.
- Any remaining unresolved at the end → return an **escalation result** (see pipeline).

### 2. `src/kainos/regex/testgen.py` (seeded, deterministic)

`generate(node, seed=0) -> (positive: list[str], negative: list[str])`

- Positive: instantiate each node with concrete strings (digit→`0`, letter→`a`,
  literal→itself); expand quantifiers to a few lengths within bounds.
- Negative: mutate exactly one element (wrong class, out-of-range count, wrong
  literal, missing anchor, extra suffix) to violate one constraint.
- Deterministic under a fixed `seed`.

### 3. `src/kainos/regex/judge.py` + Perl judge (ADR-0009)

- `judge(pcre: str, positive, negative) -> Verdict` **invokes a Perl script**
  (`scripts/judge.pl`) that compiles the pattern and full-matches each example,
  returning JSON. The Perl engine is canonical (ADR-0009); Python `re` is not used.
- `Verdict(ok, mismatches=[...])` with a human-readable diff of any misjudged example.

### 4. `src/kainos/regex/pipeline.py`

`describe(text: str) -> Result` composing: `parse → resolve → emit → generate → judge`.
`Result` = `{ir, resolved_trace, pcre, verdict, escalation, confidence}`.

- If `resolve` found unresolved refs → set `escalation = {"status": "requires_context",
  "candidates": [...], "recommended_action": "ask_human"}` and do **not** emit a
  regex (invariant: never emit what you can't justify).
- Otherwise emit + judge, with `confidence` from the trace.

### 5. CLI

`kainos regex describe "..."` and `kainos regex explain "..."` (explain prints the full
IR + trace + PCRE + verdict).

### 6. Tests

- `tests/regex/test_resolver.py`: "hyphen" resolves to `-` via CODEX; "the dash thing"
  yields candidates and (when ambiguous) an escalation result.
- `tests/regex/test_testgen.py`: generator covers every operator; judge rejects a
  deliberately wrong regex with a useful diff.
- `tests/regex/test_pipeline.py`: canonical example returns `ok` + a non-empty trace;
  a vague description returns escalation (not a guessed regex).

## Verification

```bash
pytest tests/regex -q && kainos regex describe "three digits, then a hyphen, then two letters"
```

Expect: all green; the CLI prints a passing verdict + trace.

## Done when

- [ ] resolver resolves via CODEX and escalates when ambiguous
- [ ] testgen + judge deterministic and useful
- [ ] pipeline returns verdict + full audit trace; escalates instead of guessing
- [ ] `kainos regex describe` / `explain` work
- [ ] `pytest tests/regex -q` green

## If stuck

`plan/30-phases/phase-1-regex/spec.md` §4–§5, `plan/30-phases/phase-1-regex/actions.md` → P1.05–P1.07.
