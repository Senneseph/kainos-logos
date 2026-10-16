# Reasoner / Solver

Searches the CODEX, applies constraints, checks consistency, and either produces a
**verified state** or an **unresolved state**. It does not generate language and it
does not store knowledge.

## Core operations

```
resolve(term, context)      → pinned TermRef | Unresolved
infer(relation, a, b)       → verified | contradicted | unknown
verify(assertion)           → pass | fail | needs_evidence
expand(term, depth)         → broader semantic neighborhood
find_exception(pattern)     → is this in EXCEPTION territory?
retrieve(source)            → pull evidence from a SOURCE
```

## Search depth & abstraction levels

Escalation ladder, cheapest first:

```
EXACT → synonym → related concept → structural relationship → abstract pattern
```

with an explicit depth budget. Depth is a *parameter* the caller sets; it is how
"creativity" (proposal space) is separated from "logic" (verification space).

## Consistency checking

The reasoner knows hard constraints vs. soft ones (P5):

- **Hard:** `person cannot be in two places at once`, `TREE ∈ ANIMAL is impossible`.
  Violation → `IMPOSSIBLE` / contradiction, never a soft "unlikely".
- **Soft:** confidence-weighted; violation → `disputed`/`ambiguous`.

`CAUSES(A,B)` implies `t_A < t_B`; if the CODEX has `B before A`, that's a
contradiction the reasoner reports, not a paragraph it papers over.

## Output contract

A reasoner result is **always** one of:

```text
VERIFIED     { ir, evidence_chain, exception_depth, confidence }
UNRESOLVED   { status, known[], unknown[], attempted[], best_candidates[], recommended_action }
```

`recommended_action ∈ { infer, search_deeper, retrieve_evidence, ask_human }` is
chosen by the EXCEPTION cost `E` (see exception-system.md). This is the formal
"when should the AI stop pretending it knows?" answer.

## Where it gets its constraints

Constraints come from two places: (1) the CODEX (assertions of kind `constraint`),
and (2) the task dialect (e.g. regex validity rules: a quantifier needs a target,
alternatives need ≥2 branches). The reasoner is dialect-agnostic; dialect-specific
rules are data, loaded like any other assertions.

## Phase mapping

| Phase | Reasoner capability |
|-------|---------------------|
| 0 | `verify`, `resolve` (trivial), `dump` |
| 1 | + `infer` (regex term → PCRE), `expand` (rotation for "thing") |
| 2 | + `find_exception`, depth budget, `recommended_action` (info-gain question selection) |
| 3 | + contradiction→missing-dimension detection, distributed reconcile |
