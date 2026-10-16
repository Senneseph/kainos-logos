# 01 — Principles (non-negotiable design invariants)

Every design decision, code review, and phase-exit check is evaluated against these.
If a decision violates one, it is wrong until amended by an ADR in [`03-adr.md`](03-adr.md).

## P1 — Assertions, not facts

The CODEX never stores "the truth". It stores **assertions**: subject + relation +
object **wrapped in** provenance, source, context, validity interval, and epistemic
state. `CAPITAL_OF(France, Paris)` is stored as an assertion with `source`,
`confidence`, `context`, and `status`, never as a bare edge.

## P2 — The neural model is the language organ, not the brain

The neural component (a.k.a. "language kernel") does exactly two things:
`text ↔ Semantic IR` and hypothesis *proposal*. It must not be the store of durable
knowledge. Its weights can be frozen while the system keeps learning.

## P3 — The CODEX is the single source of truth for durable knowledge

Any durable fact lives in the CODEX, nowhere else. Transient context lives in
working memory. If two subsystems disagree about a fact, the CODEX holds the
disagreement (see P6), not a blended weight.

## P4 — Everything is a TERM

Terms are independently addressable semantic nodes, rotatable and searchable
orthogonally through their relationship neighborhoods. `CAPITAL_OF`, `country`,
`city`, `France`, `Paris` are each first-class TERMs; the record is the *pattern of
relationships between them*, not a rigid row.

## P5 — EXCEPTION ≠ impossible

The CODEX has a first-class representation for *unexplored / insufficiently
characterized* valid combinations (EXCEPTION), which is categorically different from
*impossible* (hard constraint violation). `TREE ∈ ANIMAL` is impossible;
`electronic + edible` is an EXCEPTION until characterized. Never conflate them.

## P6 — Contradiction is a signal, not an error

Two disagreeing assertions are *preserved*, not averaged. A recurring contradiction
is evidence of a **missing dimension** and should drive ontology expansion
(higher-order TERM), not probability blending.

## P7 — Semantic IR decouples the pipeline

Perception, reasoning, and realization are separated by a formal Semantic IR so that
any layer can be swapped or scaled independently (and later, modalities can share the
same IR).

## P8 — Measure, don't argue

Every architectural claim becomes a benchmarked experiment with a falsifiable
hypothesis, a metric, and a success threshold *before* it is believed. No unfalsifiable
"Fibonacci = intelligence" claims.

## P9 — Inspectability is a first-class feature

Never hide the CODEX. Every answer exposes its evidence chain and EXCEPTION depth.
This is both a debugging tool and the product's differentiator.

## P10 — Start small, scale later

No premature generalization. Phase 0/1 use the smallest substrate that can falsify
the core claim. Optimize (GPU, distributed, φ-numerics) only after the mechanism is
proven on a tiny domain.

## P11 — Capabilities are declared, not implied

The system may only plan over explicitly declared capabilities (TERMs with
preconditions/effects in the CODEX). A goal with no valid plan is a **first-class
outcome** — named capability gap + nearest viable plan. Never a hallucinated
action (supplemental-ideas integration; ADR-0011).

## P12 — Memory is recursively addressable structure; promotion is explicit

Working memory is not a bigger context window: it is a recursively nestable
WORKSPACE of queryable IRs with lifetimes, and nothing moves from working memory
into the CODEX except a deliberate, provenance-carrying promotion (ADR-0012).
