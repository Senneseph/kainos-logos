# 02 — Glossary (controlled vocabulary)

These terms are used with fixed meanings throughout the plan and (later) the code.
Do not invent synonyms; extend here instead.

## Core entities

| Term | Definition |
|------|------------|
| **TERM** | An independently addressable semantic node (concept, entity, relation, operator, constraint, source…). Has an ID, one or more labels, and a semantic neighborhood. Everything is a TERM. |
| **RELATIONSHIP** | A typed, directed edge between TERMs: `SUBJECT --RELATION--> OBJECT`. Types include `is_a`, `part_of`, `causes`, `enables`, `requires`, `prevents`, `implies`, `correlates_with`, `precedes`, `followed_by`, `located_at`, `has_property`, etc. |
| **ASSERTION** | A relationship **wrapped in metadata**: provenance, source, context, validity interval, epistemic state, confidence. The atomic unit of CODEX storage. |
| **CONTEXT** | The conditions under which a relationship holds (domain, time, perspective, role, modality…). Relationships are indexed *by context*, not globally. |
| **SOURCE** | First-class TERM describing where an assertion came from: URI, media type, version, hash, retrieved-at, authority, accessibility. |

## The substrate

| Term | Definition |
|------|------------|
| **CODEX** | The persistent semantic substrate: a graph store of TERMs + typed RELATIONSHIPs + CONTEXT + SOURCE + provenance + EXCEPTION. The single source of truth for durable knowledge. |
| **Working Memory** | Transient, per-session state (active entities, hypotheses, goals, recent referents). Not durable. |
| **Semantic IR** | The formal intermediate representation that all layers speak. A serializable, language-independent structure (entities, relations, events, constraints, quantifiers, modality, time). |

## The pipeline

| Term | Definition |
|------|------------|
| **Language Kernel** | The neural (or initially rule-based) component mapping `text ↔ Semantic IR` and proposing candidate interpretations. The "language organ". |
| **Reasoner / Solver** | Searches the CODEX, applies constraints, checks consistency, expands/contracts search depth. Produces a *verified* state or an *unresolved* state. |
| **Realizer** | Maps a verified Semantic IR back to natural language (surface realization). |
| **Execution Fabric** | The heterogeneous runtime (CPU graph traversal, GPU bitwise/parallel ops, DB persistence) that executes compiled Semantic IR operations. |

## Assertion `status` (lifecycle states)

An assertion's `status` field — how established a particular assertion is:

`candidate` · `established` · `disputed` · `obsolete` · `hypothesis` ·
`ambiguous` · `contradicted` · `inapplicable`

These are **not** the same list as the uncertainty states below; do not mix them.

## Uncertainty states (query/solver output)

When the solver answers a query it reports *which situation* the uncertainty is in
— a probability alone cannot distinguish these:

| State | Meaning | Typical cause |
|-------|---------|---------------|
| **KNOWN** | Verified/established under stated context. | — |
| **UNKNOWN** | No assertion on record. | never encountered |
| **AMBIGUOUS** | Multiple interpretations remain viable. | underspecified input |
| **HYPOTHETICAL** | Proposed but unverified. | inference, not observation |
| **CONTRADICTED** | Evidence supports incompatible interpretations. | conflicting sources |
| **INAPPLICABLE** | The relationship doesn't apply in this context. | wrong context selected |
| **IMPOSSIBLE** | Hard constraint violation (not merely unknown). | ontology constraint broken |

(`IMPOSSIBLE` overlaps the exception taxonomy below because a violated hard
constraint is also an EXCEPTION state — P5 keeps the categories distinct from
merely-*unknown*.)

## The knowledge boundary

| Term | Definition |
|------|------------|
| **EXCEPTION** | A *representable but insufficiently characterized* valid combination of TERMs/relationships. Its states: `UNSEEN`, `UNRESOLVED`, `AMBIGUOUS`, `CONFLICTING`, `UNVERIFIED`, `REQUIRES_CONTEXT`, `IMPOSSIBLE`. |
| **EXCEPTION depth / cost (E)** | `depth × ambiguity × lack_of_evidence`. Determines the runtime escalation: infer → search deeper → retrieve evidence → ask the human. |
| **Coverage(T, C)** | `verified_combinations / encountered_combinations` for a TERM `T` in context `C`. Measures "how well does the system understand this term?". |

## Memory tiers

`ephemeral` (next utterance) · `session` (this conversation) · `episodic` (event
memory) · `semantic` (generalized knowledge) · `procedural` (reusable how-to) ·
`hypothesis` (unverified candidate) — separated explicitly, never mashed into one
parameter space. The *containers* for the transient tiers are **WORKSPACE** objects
(see "The substrate" below and `10-architecture/workspace-memory.md`); the
`project` lifetime sits between `session` and `long_term`.

## The projection layer (Phase 3, ADR-0011)

| Term | Definition |
|------|------------|
| **WORKSPACE** | A bounded, named, lifetime-scoped, recursively nestable container of IRs, hypotheses, constraints, plans, exceptions, and references. Memory as queryable structure, not a bigger context window (P12). |
| **Lifetime** | A workspace's scope: `EPHEMERAL \| SESSION \| PROJECT \| LONG_TERM`. Content migrates only by explicit promotion. |
| **Promotion** | The deliberate operation that writes a workspace IR's relationships into the CODEX as *candidate* assertions with provenance (`source=workspace_<id>`). Never implicit. |
| **CAPABILITY** | A first-class TERM declaring an operation the system may invoke, with `PRECONDITION`, `INPUT`, `EFFECT`, `COST`. The planner may use only declared capabilities (P11). |
| **PLAN** | A sequence of declared capabilities whose effect application takes a start state to a terminal state satisfying the goal — a proof, not a guess. |
| **NO VALID PLAN** | The first-class result for an unachievable goal: names the missing capability and gives the nearest viable plan. Never a hallucinated action. |
| **PROJECTION** | The step `Response = Realize(Project(Parse(Input), Context, Knowledge, Capabilities, Goal))` — goal-directed semantic transformation. |
| **RESPONSE CONTRACT** | The per-interaction-type shape of a correct response (REQUEST/QUESTION/COMMAND/ASSERTION/CORRECTION/impossible/ambiguous), checked at realization. |
| **Semantic temperature** | The creativity parameter over *constrained* graph traversal: varies which valid path is taken, never whether an established fact holds (novelty must not violate P5/P6). |

## Learning loop

`observe → interpret → hypothesize → verify → consolidate → generalize` — the
learning objective replaces "predict next token" with "shrink the EXCEPTION space
and expand the ontology".
