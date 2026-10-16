# Phase 1 — Regex (first proof of concept)

**Goal:** natural-language regex descriptions → Semantic IR (regex dialect) → PCRE →
executable verdicts, with three claims demonstrated on the smallest domain that has a
*formal* judge: **C1** compositional generalization, **C2** persistent learning
without retraining, **C3** honest uncertainty (claim IDs: `../20-roadmap.md`).

**Why regex first:** the computer itself is the judge — correctness means the emitted
pattern passes full-match tests against generated positive/negative examples, not
"looks plausible". That gives an objective training signal and a clean A/B baseline.

**Scope:** action-steps 06–12 (`P1.01`–`P1.16`). Experiments E1.1–E1.5
(`experiments.md`). The pipeline is Python-in-Docker; the judge is Perl
(ADR-0009).

## Exit criteria

1. E1.1 parity == 1.0 on the seed corpus (every operator). *(09)*
2. E1.2: pipeline beats the no-CODEX baseline on novel combinations by ≥0.1
   absolute, pipeline ≥ 0.8. *(10)*
3. E1.3: teach → restart → reuse with frozen kernel (C2) + E1.4 vague set never
   emits an unjustified regex (C3). *(11)*
4. E1.5: Model B > Model A on held-out combinations; B abstains correctly on the
   vague set where A cannot. *(12)*
5. `results.md` signed off with reuse stats (compounding contract). *(12)*

## Documents

- [`spec.md`](spec.md) — grammar, dialect, emitter table, resolver, judge (normative).
- [`experiments.md`](experiments.md) — E1.1–E1.5 definitions.
- [`benchmarks.md`](benchmarks.md) — A/B protocol.
- [`actions.md`](actions.md) — P1.01–P1.16 → directives.
- [`results.md`](results.md) — sign-off (filled by step 12).
