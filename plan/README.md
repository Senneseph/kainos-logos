# Kainos-Logos — Project Plan

> *καινός* (kainos) = new · *λόγος* (logos) = word / reason / ordering principle
>
> **The New Logos**: a cognitive architecture where a neural "language organ" maps
> natural language ↔ a formal Semantic IR, and all durable knowledge lives in a
> mutable, inspectable **CODEX** — an explicit semantic graph with provenance,
> context, time, epistemic state, and an **EXCEPTION** boundary.

## What this folder is

A hierarchical, executable plan. It starts at the level of vision and principles
and drills down — architecture → phases → actions → individual tasks — until the
leaves are concrete, ordered, verifiable steps.

## How to navigate

| Path | What it is |
|------|------------|
| [`00-north-star.md`](00-north-star.md) | The vision in one page + measurable success criteria. Start here. |
| [`01-principles.md`](01-principles.md) | Non-negotiable design invariants. Every decision must not violate these. |
| [`02-glossary.md`](02-glossary.md) | The controlled vocabulary (TERM, CODEX, EXCEPTION, …). |
| [`03-adr.md`](03-adr.md) | Architecture Decision Records. Living log of choices + rationale. |
| [`10-architecture/`](10-architecture/README.md) | The full system design, layer by layer. |
| [`20-roadmap.md`](20-roadmap.md) | Phase sequence, dependency graph, and the *compounding* contract. |
| [`30-phases/`](30-phases/README.md) | Phase-by-phase plans, each drilling to concrete actions. |
| [`40-testing/`](40-testing/README.md) | Test strategy, metrics, benchmarks, harness design. |
| [`90-appendices/`](90-appendices/prior-art.md) | Prior art, risks, open research questions, proposed repo layout. |

## The executable runbook

[`../action-steps/`](../action-steps/README.md) is the **operational** sibling of this
folder: 20 self-contained, sequential, prompt-like directives (plus a one-page
`00-CONTEXT.md` bootstrap). Each directive maps to the `P*.xx` actions below and can
be executed by a fresh agent without re-reading this plan. Read the plan for *why*;
follow `action-steps/` for *what to type*.

## The four phases (in order)

1. **Phase 0 — Foundation** (`30-phases/phase-0-foundation/`): scaffolding, CODEX
   data model, Semantic IR, test harness. No intelligence yet — just the substrate.
2. **Phase 1 — Regex** (`30-phases/phase-1-regex/`): the first proof of concept.
   Natural-language regex descriptions → Semantic IR → PCRE → executable tests.
3. **Phase 2 — 20 Questions** (`30-phases/phase-2-20questions/`): the active-learning
   training environment that exercises EXCEPTION, information gain, and persistent
   memory.
4. **Phase 3 — Generalization** (`30-phases/phase-3-generalization/`): the
   full-realized, task-agnostic architecture (multi-modal hooks, distributed
   CODEX, φ/Fibonacci numerics).

> The document's requested order is regex-first, then 20 Questions, then the
> full architecture. This plan preserves that ordering while inserting a
> Phase 0 because *both* later phases need the same substrate, and building it
> once is exactly the "compounding effect" the project depends on.

## The compounding contract

Every phase must **leave behind reusable artifacts** for the next phase and must
**test a specific architectural claim**, not just "build a thing". See
[`20-roadmap.md`](20-roadmap.md) for the explicit claim → artifact → test mapping.
