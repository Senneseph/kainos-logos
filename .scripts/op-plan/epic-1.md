**Source:** `plan/30-phases/phase-1-regex/README.md` + `plan/20-roadmap.md`

## Goal

Natural-language regex descriptions → Semantic IR (regex dialect) → PCRE →
executable verdicts, with three claims demonstrated on the smallest domain that has
a *formal* judge:

- **C1** — compositional generalization
- **C2** — persistent learning without retraining
- **C3** — honest uncertainty

(Claim registry: `plan/20-roadmap.md`.)

## Why regex first

The computer itself is the judge — correctness means the emitted pattern passes
full-match tests against generated positive/negative examples, not "looks
plausible". That gives a strong, objective training signal and a clean A/B
baseline. Pipeline is Python-in-Docker (ADR-0010); the judge is Perl (ADR-0009).

## Scope

Action steps **06–12** (`P1.01`–`P1.16`). Experiments E1.1–E1.5
(`plan/30-phases/phase-1-regex/experiments.md`). Normative grammar/emitter specs:
`plan/30-phases/phase-1-regex/spec.md`.

## Claim tested (compounding contract)

> IR + CODEX yield *compositional* regex generation + *persistent* memory + *honest*
> uncertainty.

**Artifact left behind:** `kainos.lang` (deterministic kernel), `kainos.regex`
(dialect + emitter + testgen), benchmark suite.
**Consumed from prior phases:** CODEX, IR, harness.

## Ordering notes (from `actions.md`)

- P1.01–P1.08 are pure build (no experiments yet) but every one is test-gated.
- P1.09 is the first "claim" gate — do not proceed until parity is exact.
- P1.12 (persistent memory) is the **emotional center** of the whole project.
- P1.14–P1.15 (LLM A/B) may run in parallel with Phase 2 planning if a model
  backend is slow, but E1.5 must complete before Phase 1 sign-off.

## Exit criteria

Five exit criteria (E1.1 parity, E1.2 vs. baseline, E1.3/E1.4, E1.5 A/B, signed
`results.md`) are tracked in the **"Phase 1 sign-off"** Milestone, together with
kill criteria **K1/K2** from `plan/04-reality-check.md` §4.
