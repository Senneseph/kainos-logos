# 90 — Prior Art (do not reinvent; borrow deliberately)

The document's own survey, condensed into a reference list with "what we take vs.
what we change".

| System / field | What it is | What we take | What we change |
|----------------|------------|--------------|----------------|
| **Cyc** | Symbolic common-sense KB + rules | explicit, inspectable knowledge | we extract it *from experience* instead of hand-authoring |
| **WordNet / ConceptNet / Wikidata / RDF-OWL** | knowledge graphs / ontologies | typed relationships, provenance | add EXCEPTION, temporal epistemic states, "assertions not facts" |
| **Neuro-symbolic AI** | neural perception → symbolic reasoning → neural generation | the pipeline shape | explicit persistent, mutable, expanding ontology; learning = ontology growth not weight updates |
| **RAG / vector DB / external memory** | retrieve-then-generate | external store | the store is *part of reasoning*, not a lookup appendix |
| **20Q (Robin Burgener)** | the game + ML; the user's historical reference | the game as training env; info-gain | inspectable CODEX + provenance + EXCEPTION + persistent learning |
| **Active learning / Bayesian experimental design** | optimal question selection | IG formula | integrate with the CODEX/EXCEPTION architecture |
| **LNS (logarithmic number systems)** | multiply = add exponents | the φ-variant idea | Fibonacci normalization as a *structured* addition fix (gated) |
| **Knowledge-graph provenance / named graphs / temporal DBs** | fact + source + time | SOURCE/provenance/validity | epistemic-state taxonomy + EXCEPTION boundary |
| **Mixture-of-experts / conditional computation** | sparse routing | "compute ∝ usefulness" (Zipf) idea | tie to semantic TERM frequency, not just routing |
| **MorphoHDL (Mordvintsev, Apache-2.0)** | minimal circuit-growing language: tiny rewrite kernel + fallback + interleaved pruning | seven mechanism patterns (M1–M7): materialization cache, prune-while-growing, fanout-bounded materialization, fallback → NO VALID PLAN, space–time duality, largest-first ordering, flat binding-point genome | the substrate (bit buses / LUT circuits) is left behind — patterns re-implemented in assertion-graph semantics, each benchmark-gated, no dependency, no foreign code (ADR-0013; transfer record: `SCAVENGE_MORPHO.md`) |

## The honest summary (from the document)

> Pieces of this have absolutely been done. The **particular combination** —
> persistent neuro-symbolic learning through an explicit, expanding, provenance-aware
> semantic Codex, with an EXCEPTION boundary and active clarification — is not an
> established solved architecture.

## Why prior attempts stalled (the five reasons, kept as warnings)

1. Symbolic AI's **knowledge-acquisition problem** (hand-authoring doesn't scale).
2. **LLMs made brute force irresistible** (big matrix beat hand-built systems).
3. **Symbolic reasoning doesn't parallelize** like matrix multiply (GPUs).
4. **Symbolic systems are brittle** ("no rule" vs "plausible answer").
5. The hard part is **automatic abstraction discovery**, not the database.

Each warning maps to a design decision in this plan:
1 → learn from experience (P2/P6), 2 → the A/B experiment E1.5, 3 → the execution
fabric (compile to bitsets/tensors), 4 → EXCEPTION + abstention (C3/A2), 5 → the
contradiction→dimension mechanism (A5/E3.3).
