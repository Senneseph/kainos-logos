# Language Kernel

The "language organ". Its **only** jobs:

1. `parse(text, context) → Semantic IR` (+ candidate interpretations with scores)
2. `realize(ir) → text`
3. `propose(observation) → hypotheses[]` (candidate meanings for the reasoner to test)

It **must not** store durable knowledge (P2) and **must not** decide truth (that's
the reasoner's job).

## The interface (contract)

```python
class LanguageKernel(Protocol):
    def parse(self, text: str, context: WorkingMemory) -> list[Interpretation]:
        """Return 1..n candidate Semantic IRs, each with a confidence score."""
    def realize(self, ir: SemanticIR, style: str | None = None) -> str:
        """Surface a verified IR as natural language."""
    def propose(self, ir: SemanticIR) -> list[Hypothesis]:
        """Propose candidate relationships for the reasoner to verify."""
```

`Interpretation = (ir: SemanticIR, score: float, unresolved: list[TermRef])`.

## Two implementations (ADR-0004)

| Impl | When | Notes |
|------|------|-------|
| `DeterministicKernel` | Phase 1 default | Hand-written parser over the restricted regex-description grammar (`phase-1-regex/spec.md`). No ML. |
| `LLMKernel` | Phase 1 A/B, Phase 3 | Any local/hosted model behind the same interface. Used for the "conventional vs. CODEX" comparison. |

Keeping both behind one interface is what makes the A/B experiment clean: the only
thing that changes is *where* interpretation happens, not the downstream CODEX path.

## The bootstrap vocabulary (Phase 1 minimal set)

The kernel only needs to recognize a small, explicit vocabulary of **semantic
operators** — not full English:

- **Quantifiers:** `one or more` (+), `zero or more` (*), `optional` (?),
  `exactly N`, `at least N`, `at most N`, `between N and M`.
- **Classes:** `digit`, `letter`, `word`, `whitespace`, `any`, `number` (disambiguate
  digit vs. numeric literal), `character`.
- **Anchors:** `beginning/start of string`, `end of string`.
- **Structure:** `followed by`, `then`, `and`, `or`/`either...or`, `group`,
  `ignore case`, `literal`.
- **Reference:** `thing`, `the ... thing`, `it` (coreference to a prior term).

The grammar in `phase-1-regex/spec.md` formalizes exactly this subset.

## Why a deterministic parser first (the confound argument)

The core claim is about **knowledge separation**, not parsing. If we hand-wave
parsing with an LLM, we cannot tell whether success came from the CODEX or from the
LLM's latent regex knowledge. A deterministic parser:
- is free and deterministic (CI-safe, golden-file testable),
- has zero latent "regex memory" to leak into the experiment,
- makes the LLM a *second* implementation so the A/B is apples-to-apples.

## Pragmatics (later, Phase 3)

The kernel must eventually distinguish `Can you pass the salt?` (REQUEST) from a
literal yes/no QUESTION, and `It's cold in here` (REQUEST/COMPLAINT) from an
OBSERVATION. This is the "language bootstrap" the document calls out as the missing
layer. Phase 1 deliberately defers it — the regex grammar is directive enough that
pragmatic ambiguity is minimal, and we want to test the substrate, not pragmatics.
