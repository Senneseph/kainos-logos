# System Overview

## The five layers (canonical)

1. **Language Kernel** — perception: messy text → Semantic IR (and back).
2. **Semantic IR** — the shared, serializable structure.
3. **CODEX** — durable knowledge (assertions + provenance + EXCEPTION).
4. **Reasoner** — search, constrain, verify; produces verified or unresolved state.
5. **Realizer + Execution Fabric** — surface results as text/actions; run the ops.

## Dataflow for a query (happy path)

```
"Match three digits, then a hyphen, then foo or bar, case-insensitive."
  → Kernel: parse → Semantic IR:
      SEQUENCE[
        REPEAT(DIGIT, EXACTLY 3),
        LITERAL("-"),
        ALTERNATIVE(LITERAL("foo"), LITERAL("bar")),
        FLAG(CASE_INSENSITIVE)
      ]
  → Reasoner: resolve each TERM against CODEX (DIGIT→\d, LITERAL→escape, …)
  → Emit PCRE: ^(?:\d{3})-(?:foo|bar)$ (flags: i)
  → Verify: execute against generated positive/negative examples
  → Realizer: return regex + explanation + confidence + trace
```

## Dataflow for an ambiguous/underspecified query

```
"Start with the number thing, three of them, then the dash thing, then more numbers."
  → Kernel: parse → IR with UNRESOLVED references ("number thing", "dash thing")
  → Reasoner: CODEX search → candidates; some collapse, some stay ambiguous
  → EXCEPTION check: cost E = depth × ambiguity × lack_of_evidence
  → if E low: infer best candidate; if E high: ask "did you mean a hyphen?"
  → user clarifies → CODEX records EXCEPTION→VERIFIED (active learning)
```

## The state model (what "state" contains)

```text
STATE {
  entities[], facts[], relationships[], time[],
  goals[], constraints[], uncertainties[], hypotheses[],
  active_processes[], working_memory[]
}
```

Reasoning = a sequence of state transitions; language is emitted only at the edges.

## Lifecycle of a fact (always the same, in every phase)

```
RAW EXPERIENCE → WORKING MEMORY → CANDIDATE KNOWLEDGE → CODEX (long-term)
```

- Training/exposure produces **evidence**, never direct writes to long-term memory.
- Consolidation promotes evidence to assertions only after verification.
- Conflicts are preserved as `disputed`, never silently averaged (P6).

## What this means for the phases

| Phase | Which layers exist | Which claim is tested |
|-------|--------------------|-----------------------|
| 0 | CODEX (min), Semantic IR (min), test harness | "substrate is sound + inspectable" |
| 1 | + Kernel (deterministic), Reasoner (min), Realizer (regex) | "IR + CODEX enable compositional regex generation + persistent memory" |
| 2 | + active-learning loop, EXCEPTION escalation, info-gain | "system actively acquires knowledge + shrinks EXCEPTION" |
| 3 | + LLM kernel, distributed CODEX, φ numerics, multi-modal hooks, **capability projection** (`projection.md`), **recursive workspace memory** (`workspace-memory.md`) | "the same algebra scales beyond one domain" (X1–X3 included) |
