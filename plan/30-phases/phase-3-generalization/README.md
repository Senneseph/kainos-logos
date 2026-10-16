# Phase 3 — Generalization (the full-realized architecture)

The final goal: one general architecture that, if it works for any task, will begin
to work and learn.

## Goal

Generalize the proven single-node mechanism (Phases 1–2) into a task-agnostic
cognitive architecture:

- **LLM kernel** replaces (or augments) the deterministic kernel — same interface.
- **Distributed CODEX** — federation, "knowledge Git", cross-node reconciliation.
- **Multi-modal hooks** — image/audio/video/3D perception produce the *same* Semantic
  IR (stubs + one demonstration).
- **φ/Fibonacci numerics** — isolated, benchmark-gated experiments (ADR-0006).
- **Fibonacci topology** — isolated, benchmark-gated (layer widths, residual
  recurrence, golden-angle addressing, sparse attention).
- **Capability projection** (ADR-0011) — declared capabilities, plan search over the
  CODEX, NO VALID PLAN as a first-class result, structured creativity. Claims X1/X2.
- **Recursive workspace memory** (ADR-0012) — WORKSPACE containers with lifetimes,
  explicit promotion, queryable structure. Claim X3.

## The unifying claim (the "one algebra" bet)

> The number system (φ²=φ+1), the topology (Fₙ₊₂=Fₙ₊₁+Fₙ), and the knowledge
> representation (recursive pattern composition) can share **one recurrence**, and
> that sharing yields measurable computational/reasoning gains.

**This is a hypothesis, not an assumption** (P8). Every sub-claim is benchmark-gated
and isolated so a failure in one does not poison the rest.

## What "full-realized" means (acceptance)

A system that:
1. accepts any of ≥2 modalities (text + one synthetic non-text modality) into the
   same CODEX;
2. learns continuously without retraining the neural kernel;
3. expands its own ontology when contradictions reveal missing dimensions;
4. synchronizes knowledge across ≥2 nodes via assertion deltas;
5. abstains/asks at its knowledge boundary;
6. exposes an inspectable trace for every conclusion;
7. plans only over declared capabilities — an unachievable goal yields NO VALID PLAN
   with the named gap + nearest viable plan, never a fabricated action (X1);
8. keeps memory recursively addressable — workspaces nest, "what did we decide?" is
   a graph query, and nothing reaches the CODEX without explicit promotion (X3).

## Sub-projects (each independently gated)

| Sub-project | Claim | Gate |
|-------------|-------|------|
| LLM kernel A/B | Neural parse/realize beats/parities the deterministic kernel on open phrasing, behind the same interface | benchmark |
| Distributed CODEX | 2 nodes reconcile "two truths" into a higher-order representation | benchmark |
| Multi-modal hooks | synthetic vision + text share one abstract CODEX pattern (TRANSFER) | benchmark |
| φ numerics | φ-exponent ops beat FP/INT per bit-op on a MAC/histogram kernel | benchmark (ADR-0006) |
| Fibonacci topology | a Fibonacci recurrence structure improves a measured metric on a toy task | benchmark |
| Projection / planning | plans only over declared capabilities; unachievable goals → NO VALID PLAN + nearest plan; creative traversal stays constraint-valid (X1/X2) | benchmark |
| Recursive workspace | workspaces nest, query, and promote explicitly; CODEX never sees un-promoted content (X3) | benchmark |

## Exit criteria

1. E3.1–E3.7 run green and are reported.
2. The multi-modal demo (E3.4) resolves one abstract pattern across two modalities.
3. The 2-node reconciliation demo (E3.3) produces a higher-order TERM.
4. φ/Fibonacci results are reported as *adopt or reject*, never silently merged.
5. `plan/30-phases/phase-3-generalization/results.md` consolidates all phases and
   states, in one table, whether the unifying claim survived.

## Key documents

- [`experiments.md`](experiments.md) — E3.1–E3.5.
- [`actions.md`](actions.md) — ordered concrete actions.
