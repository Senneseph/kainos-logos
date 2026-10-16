# Execution Fabric

The heterogeneous runtime that executes compiled Semantic IR operations.

## Principle: don't GPU-accelerate the graph DB

Graph traversal is pointer-chasing + branching (GPUs hate it). Matrix math is SIMD
(GPUs love it). So split:

```
PERSISTENT CODEX (graph DB: irregular traversal, indexing, persistence)
        │
   query planner
        │
        ▼
GPU CODEX CACHE (compiled, packed, massively parallel semantic ops)
        │
        ▼
CPU SOLVER (complex branching reasoning, final verification)
```

The graph DB is the **authoritative store**; the GPU gets a *compiled* slice of the
parts needed for the current workload.

## Compiled representation (packed integer IDs)

Relationships become arrays of packed ints — the GPU doesn't care that `[1842, 17,
8291, 4, 2, 731]` means `CAPITAL_OF`; it just processes IDs:

```
TERM_ID, RELATION_ID, TARGET_ID, CONTEXT_ID, STATE_ID, SOURCE_ID
```

Human-readable semantics stay in the DB layer.

## Bitsets & masks

Represent a term's related set as a bitset; `∩`/`∪`/`\` become bitwise
AND/OR/ANDNOT. "Semantic rotation" becomes a giant parallel
`candidate ∩ context ∩ relation ∩ constraint` mask op. GPUs are excellent at this.

## Sparse tensors (CSR/COO)

For M terms × N relations, use CSR/COO adjacency:

```
TERM_OFFSETS[], RELATION[], TARGET[], CONTEXT[], WEIGHT[], STATE[]
```

A query `(term, relation)` is a range lookup; the GPU then evaluates millions of
candidate relationships simultaneously.

## JIT-compiled hot paths

Common traversals (`PERSON→OWNS→OBJECT`, `EVENT→CAUSED_BY→AGENT`) get compiled into
specialized kernels/cached structures — the CODEX **learns which reasoning ops
deserve acceleration**. (Phase 3.)

## Semantic IR as the universal operation format

```
Semantic IR → { CPU | GPU | DB | NEURAL | TOOL }
```

The kernel/reasoner emit operations as IR; the fabric decides *where* to run them.
The neural model becomes just another execution engine among several.

## Zipf-aware representation & caching (from the document)

Language is heavy-tailed: a tiny number of terms occur constantly, an enormous
number occur rarely. Exploit this where the document suggests:

- **Semantic CPU cache** — hot TERMs/relationships get cheap compiled
  representations (L0/L1); rare ones take the deep, expensive path (L2+).
- **Zipfian conditional computation** — `Compute(x) ∝ f(x)^α`; common semantic
  structures get specialized fast paths, rare ones invoke progressively more
  expensive machinery. (Phase 3; not a Phase 0–2 dependency.)
- **Cache-placement key** — not frequency alone ("thing" is frequent but useless), but
  `frequency × structural_usefulness × disambiguation_power`. This is what decides
  which concepts deserve optimized representation.

These are heuristics to benchmark in Phase 3, never correctness dependencies.

## Phase mapping (and a hard scope guard)

| Phase | Fabric |
|-------|--------|
| 0 | In-process Python (SQLite + dicts). No GPU. |
| 1 | Same, + the regex executor as the "TOOL" engine. |
| 2 | Same, + an oracle/verifier engine. |
| 3 | Optional GPU slice (bitset/mask ops), remote-RPC work packages. |

**Scope guard:** Phases 0–2 never touch a GPU. The φ numerics (next file) are a
Phase-3, benchmark-gated experiment. The fabric abstraction must *exist* from
Phase 0 (so engines are pluggable) but its GPU backends are strictly deferred.
