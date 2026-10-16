**Source:** `plan/30-phases/phase-3-generalization/README.md` + `plan/20-roadmap.md`

## Goal

Generalize the proven single-node mechanism (Phases 1–2) into a task-agnostic
cognitive architecture:

- **LLM kernel** replaces (or augments) the deterministic kernel — same interface.
- **Distributed CODEX** — federation, "knowledge Git", cross-node reconciliation.
- **Multi-modal hooks** — non-text perception produces the *same* Semantic IR
  (stubs + one demonstration).
- **φ/Fibonacci numerics** — isolated, benchmark-gated experiments (ADR-0006).
- **Fibonacci topology** — isolated, benchmark-gated.
- **Capability projection** (ADR-0011, claims X1/X2) — declared capabilities, plan
  search over the CODEX, NO VALID PLAN as a first-class result, structured
  creativity.
- **Recursive workspace memory** (ADR-0012, claim X3) — WORKSPACE containers with
  lifetimes, explicit promotion, queryable structure.

## The unifying claim (the "one algebra" bet)

> The number system (φ²=φ+1), the topology (Fₙ₊₂=Fₙ₊₁+Fₙ), and the knowledge
> representation (recursive pattern composition) can share **one recurrence**, and
> that sharing yields measurable computational/reasoning gains.

**This is a hypothesis, not an assumption (P8).** Every sub-claim is benchmark-gated
and isolated so a failure in one does not poison the rest.

## Scope

Action steps **17–22** (`P3.01`–`P3.17`). Experiments E3.1–E3.7
(`plan/30-phases/phase-3-generalization/experiments.md`).

**Ordering exception:** directives **21 and 22 run BEFORE directive 20** (final
consolidation always runs last, despite its number). The predecessor links on the
tickets encode this; `action-steps/README.md` states it explicitly.

## Compounding contract

**Artifact left behind:** `kainos.exchange`, `kainos.numerics`, `kainos.multimodal`
(stubs), `kainos.projection`, `kainos.workspace`.
**Consumed from prior phases:** everything.

## Sub-projects (each independently gated)

| Sub-project | Claim | Gate |
|---|---|---|
| LLM kernel A/B (E3.1) | neural parse/realize beats/parities the deterministic kernel on open phrasing, behind the same interface | benchmark |
| Distributed CODEX (E3.3) | 2 nodes reconcile "two truths" into a higher-order representation | benchmark |
| Multi-modal hooks (E3.4) | synthetic vision + text share one abstract CODEX pattern (TRANSFER) | benchmark |
| φ numerics (E3.5) | φ-exponent ops beat FP/INT per bit-op on a MAC/histogram kernel | benchmark (ADR-0006) |
| Fibonacci topology (E3.2) | a Fibonacci recurrence structure improves a measured metric on a toy task | benchmark |
| Projection / planning (E3.6, X1/X2) | plans only over declared capabilities; unachievable goals → NO VALID PLAN + nearest plan; creative traversal stays constraint-valid | benchmark |
| Recursive workspace (E3.7, X3) | workspaces nest, query, and promote explicitly; CODEX never sees un-promoted content | benchmark |

## Exit criteria

Five exit criteria plus the **eight** "full-realized" acceptance checks are tracked
in the **"Phase 3 sign-off (project acceptance)"** Milestone.
