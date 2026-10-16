# 00 — CONTEXT (read once)

This is the irreducible background for every directive in this folder. Read it once,
then follow any `NN-*.md` directive self-contained.

## What we're building

**Kainos-Logos** (καινός = new · λόγος = reason/order): a cognitive architecture where
a neural "language kernel" maps natural language ↔ a formal **Semantic IR**, and all
durable knowledge lives in a **CODEX** — an explicit, inspectable graph of TERMs +
typed relationships + provenance + context + time + epistemic state + an **EXCEPTION**
boundary. The neural model learns *how to operate on knowledge*; the CODEX
*accumulates the knowledge* — so the system keeps learning **without retraining**.

```text
text → LANGUAGE KERNEL → SEMANTIC IR → CODEX ⇄ REASONER → verified IR → REALIZER → text

Phase 3 adds two structures around this line (ADR-0011/0012):
  • WORKSPACE — recursive, lifetime-scoped containers of IRs (memory as queryable
    structure; explicit promotion into the CODEX — `plan/10-architecture/workspace-memory.md`)
  • PROJECTION — goal-directed planning over declared CAPABILITIES
    (Response = Realize(Project(Parse(Input), …)); NO VALID PLAN is a first-class
    result — `plan/10-architecture/projection.md`)
```

## The invariants (non-negotiable; code must respect these)

1. **Assertions, not facts** — the CODEX stores `subject--relation-->object` *wrapped
   in* source/provenance/context/validity/status. Never a bare edge.
2. **Neural model = language organ, not brain** — it does `text ↔ IR` and proposes
   hypotheses. It never stores durable knowledge.
3. **CODEX = single source of truth** for durable knowledge.
4. **Everything is a TERM** (independently addressable semantic node).
5. **EXCEPTION ≠ impossible** — unexplored valid combos vs. hard-constraint violations
   are categorically different.
6. **Contradiction is a signal** — preserve conflicts; drive ontology expansion, never
   average probabilities.
7. **Semantic IR decouples** the pipeline (any layer swappable).
8. **Measure, don't argue** — every claim is a benchmarked experiment.
9. **Inspectability is first-class** — every answer exposes its trace.
10. **Start small, scale later** — no premature generalization.
11. **Capabilities are declared, not implied** — the planner only uses declared
    capabilities; an unachievable goal returns NO VALID PLAN (gap + nearest viable
    plan), never a hallucinated action.
12. **Memory is recursively addressable structure; promotion is explicit** — working
    memory is nestable WORKSPACE containers of queryable IRs; nothing reaches the
    CODEX without a deliberate, provenance-carrying promotion.

## Critical vocabulary

- **TERM** — semantic node (concept/relation/operator/constraint/source/entity).
- **ASSERTION** — a relationship + mandatory metadata (source, context, validity
  interval, confidence, `status`, provenance). The atomic CODEX unit.
- **CODEX** — the persistent semantic store (SQLite-backed behind an interface).
- **Semantic IR** — JSON-serializable, versioned intermediate representation.
- **EXCEPTION** — a representable-but-unverified valid combination; states:
  `UNSEEN, UNRESOLVED, AMBIGUOUS, CONFLICTING, UNVERIFIED, REQUIRES_CONTEXT, IMPOSSIBLE`.
- **Epistemic states** (an assertion's `status`): `candidate, established, disputed,
  obsolete, hypothesis, ambiguous, contradicted, inapplicable`.

## Repo layout (key paths)

```
src/kainos/           # the package (codex/, ir/, lang/, reasoner/, regex/, q20/, ...)
tests/                # mirrors src/ one-to-one + golden/ dirs
specs/                # ir.schema.json, codex.schema.json
data/                 # regex/ and q20/ corpora (committed, small;
                      # data/codex.sqlite is the CLI's runtime DB — gitignored, not corpus)
results/              # experiment outputs (gitignored)
plan/                 # the descriptive plan (why) — optional reading
                      # (claim registry: plan/20-roadmap.md)
action-steps/         # this folder (how) — the executable runbook
```

Full layout: `plan/90-appendices/repo-layout.md` (optional).

## Conventions

- **Package:** single package `kainos`; phases add submodules, never sibling packages.
- **Toolchain:** run everything inside the pinned Docker image (ADR-0010); don't
  pollute the host. Python ≥3.11 with type hints; dev deps (`pytest`, `hypothesis`,
  `mypy`, `ruff`) live in the image.
- **Regex judge** runs under **Perl** (ADR-0009), not Python `re`.
- **Long-term language:** Rust (ADR-0001) — port the proven core behind the same
  interfaces; no premature port.
- **Action IDs** (`P0.01`…`P3.17`) are stable and referenced by directives. Never
  renumber. (Directives 21/22 were appended by the supplemental-ideas integration;
  they run before the final consolidation, step 20.)
- **Claim IDs** (`C1–C3`, `A1–A5`, `X1–X3`) are defined in `plan/20-roadmap.md` and
  stable. Never renumber. Results cite claims by ID.
- **DoD (definition of done)** for any directive = its "Done when" checklist complete
  **and** its verification command passing.
- **Run tests:** `pytest` (unit+integration+golden), `make typecheck`, `make lint`,
  `make bench` (experiments). CI must stay green.

## Phase sequence

| Phase | What | First directive |
|-------|------|-----------------|
| 0 Foundation | substrate (CODEX + IR + harness), no intelligence | `01` |
| 1 Regex | NL → IR → PCRE; compositionality + persistence + uncertainty | `06` |
| 2 20 Questions | active learning, information gain, EXCEPTION shrinkage | `13` |
| 3 Generalization | LLM kernel, distributed CODEX, multi-modal, gated φ/Fibonacci, projection, recursive workspace | `17` (final consolidation: `20`, runs after `21`–`22`) |

## The one test that matters most

**Can the system discover an abstraction its designer didn't explicitly put in the
ontology?** (Phase 2 E2.5, Phase 3 E3.3.) If yes, we crossed the boundary from
"fills slots in a fixed framework" to "expands the space in which it reasons."
