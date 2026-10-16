# 00 — North Star

## The vision (one paragraph)

Build **Kainos-Logos**: a machine where a *neural language kernel* translates messy
human input into a formal **Semantic IR**, all durable knowledge is stored in an
explicit, inspectable **CODEX** (a graph of TERMS, typed RELATIONSHIPS, CONTEXT,
SOURCE, provenance, time, and epistemic state with an **EXCEPTION** boundary), and a
**Reasoner** searches, constrains, and verifies before a *realizer* turns the result
back into language. The neural component learns **how to operate on knowledge**; the
CODEX **accumulates the knowledge itself** — so the system keeps learning without
retraining its neural parameters.

## The core claim to prove (falsifiable)

> A small neural language interface coupled to a persistent, explicitly structured
> semantic memory can achieve competitive reasoning while learning new knowledge
> **without modifying its neural parameters**.

## Success criteria (measurable, in priority order)

1. **Persistent memory** — the system learns a term/fact in one session, is
   restarted (neural weights unchanged), and still uses that knowledge correctly.
2. **Compositional generalization** — it solves combinations of abstractions that
   never co-occurred in training (train on "three digits" + "optional" separately,
   test "three digits, optionally followed by a hyphen and two letters").
3. **Honest uncertainty** — it distinguishes *inferable* from *searchable* from
   *must-ask-the-human*, and abstains or clarifies instead of hallucinating.
4. **Inspectable reasoning** — every conclusion exposes the TERMS, constraints,
   traversals, and EXCEPTION depth that produced it. No opaque "probably".
5. **Compounding artifacts** — every phase leaves behind reusable substrate the next
   phase actually uses (measured by "lines reused vs. rewritten").

## What we are NOT trying to prove (scope guards)

- Not "replace transformers everywhere."
- Not "φ is magically optimal" — the φ/Fibonacci numerics are an isolated,
  *optional*, benchmarked experiment (Phase 3), never a dependency of Phases 0–2.
- Not "build AGI." The first claim is narrow: *can we separate learning from
  remembering, pattern recognition from reasoning, and knowledge from language?*

## The one-line test of everything

> **Can the system discover an abstraction that its designer did not explicitly
> put into the ontology?**
>
> If yes, we crossed the boundary from "fills slots in a predefined framework" to
> "expands the space in which it reasons." That is the whole point.
