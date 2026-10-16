# 10.4 — Distributed CODEX (exchange + reconciliation)

Design summary for Phase 3 (action-step 19, experiment E3.3). The single-node
mechanisms it generalizes: EXCEPTION states and contradiction→dimension (invariant #6,
see `codex.md` + phase-2 game-spec).

## Principles

1. **The exchange unit is a semantic transaction, never a raw mutation.**
   Deltas carry `Assertion` + provenance + node identity + timestamp:

   ```json
   {"assertion": {...}, "node_id": "...", "timestamp": "..."}
   ```

2. **Merge preserves conflict.** If node A asserts `X` and node B asserts `¬X`, both
   remain, flagged `disputed` with linked evidence. Merging is **idempotent**
   (re-merging the same delta is a no-op).
3. **Contradiction → missing dimension, not averaging.** The reconciler enumerates
   candidate dimensions — `time, location, role, modality, context` — and asks: under
   which added dimension can both assertions be true? If one explains both, create a
   **new context TERM** and re-express both assertions under distinct contexts.
   Otherwise they stay `disputed`.
4. **Evidence-consistent consistency model.** Nodes exchange evidence (assertion +
   provenance + confidence + context + time) and derive local state independently;
   states may differ temporarily while the evidence is identical. Strong consistency
   is reserved for system configuration, not knowledge.

## Why this is interesting

A conventional distributed system blends knowledge into weights (or votes one side
dead). This design makes *disagreement itself* data: two "different truths" can force
the **ontology** to grow a concept neither node had ("Neither of us is wrong — we lack
the term to describe the difference."). That is the distributed form of the project's
core learning test: does the system expand the space in which it reasons?

## Scope guard

No clustering, no replication protocol, no network transport in Phase 3 — two local
nodes in one process exchange deltas through the protocol module. The protocol is the
deliverable; the transport is not.
