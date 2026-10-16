# 10.2 — Semantic IR

The formal intermediate representation every layer speaks (invariant #7). JSON
serializable, versioned (`kainos/ir/1`), validated at every boundary — a malformed IR
must not silently corrupt downstream reasoning.

Normative build: `../../action-steps/03-codex-explain-ir.md`; schema:
`specs/ir.schema.json` (draft 2020-12). If this page and the schema disagree, the
schema wins.

## Core shape (generic IR)

```json
{
  "kind": "state | pattern | query | command",
  "goals":         [ ... ],
  "entities":      [ {"id": "...", "type": "...", "labels": ["..."]} ],
  "relationships": [ {"subject": "...", "relation": "...", "object": "...", "context": {}} ],
  "events":        [ ... ],
  "constraints":   [ {"kind": "...", "value": ...} ],
  "unresolved":    [ {"id": "...", "surface": "...", "candidates": ["..."]} ],
  "hypotheses":    [ ... ],
  "meta":          { }
}
```

Rules:

- `kind` is required; entity ids are required; relationships require
  subject/relation/object (strings).
- `unresolved[]` is how *language* signals "I can't commit to a meaning" — the bridge
  to EXCEPTION territory. Downstream, an unresolved ref must be **resolved or
  escalated**, never guessed (see the pipeline rule in phase-1 spec §4).
- The codec (`kainos.ir.codec`) `validate` raises with a schema path; `load`/`dump`
  round-trip deterministically (golden-tested, byte-stable).

## Dialects

A **dialect** is a domain-specific node vocabulary that maps losslessly onto the
generic IR (`to_generic` / `from_generic`):

| Dialect | Nodes / kinds | Authoritative spec |
|---------|---------------|--------------------|
| Regex | Sequence, Repeat, Class, Literal, Anchor, Alternative, Group, Flag, UnresolvedRef + Quantifier enum | [`../30-phases/phase-1-regex/spec.md`](../30-phases/phase-1-regex/spec.md) §2 |
| 20Q | queries as `constraints` / hypothesis probes over the CODEX concept graph | [`../30-phases/phase-2-20questions/game-spec.md`](../30-phases/phase-2-20questions/game-spec.md) |
| (Phase 3) vision | entities + spatial relationships over synthetic scenes | [`../30-phases/phase-3-generalization/experiments.md`](../30-phases/phase-3-generalization/experiments.md) E3.4 |

Dialect invariants:

1. Generic → dialect round-trip is **lossless** (tested per dialect).
2. A dialect node with no realizable meaning (`UnresolvedRef`) must raise/escalate,
   never emit a guess.
3. Dialects never mutate the generic schema; they consume it.

## Why JSON, not an object graph on the wire (ADR-0003)

Language/modality agnostic, trivially inspectable, diffable for provenance, testable
with golden files. The `Codec` validates at every boundary.
