**Source:** `plan/30-phases/phase-0-foundation/README.md` + `plan/20-roadmap.md`

## Goal

The substrate — CODEX model + store, versioned Semantic IR, golden serialization,
CLI, experiment harness, CI. **No intelligence yet** — nothing in this phase
"thinks". Everything later phases touch must be stable, inspectable, and versioned.

## Scope

Action steps **01–05** (`P0.01`–`P0.10`).
**Out of scope:** any domain logic (regex, 20Q), any model training, anything GPU
(ADR-0010: CPU-only in-container).

## Claim tested (compounding contract)

> The substrate is sound, versioned, inspectable.

**Artifact left behind:** `kainos.codex`, `kainos.ir`, `kainos.harness`, schema
validation, golden tests. **Consumed from prior phases:** — (first phase).
Claim/artifact registry: `plan/20-roadmap.md` ("The compounding contract").

## Position in the sequence

```
Phase 0 FOUNDATION → Phase 1 REGEX → Phase 2 20 QUESTIONS → Phase 3 GENERALIZATION
```

This epic is first: every later directive assumes its artifacts exist. Per the
ordering rationale, both Phase 1 and 2 need this same substrate, and building it
once is the "compounding effect" the project depends on.

## Exit criteria

The six exit criteria (package, assertions-only, store parity, IR discipline,
harness, CI + sign-off) are tracked in the **"Phase 0 sign-off"** Milestone; step 05
maps each to evidence and fills `plan/30-phases/phase-0-foundation/results.md`.

## Risks / notes

- The schemas (`codex.schema.json`, `ir.schema.json`) are the contract. Any field
  change is a *breaking* change needing a schema version bump + ADR, because Phase
  1–2 data will be stored against them.
- `data/codex.sqlite` is the CLI's runtime DB — gitignored; not part of the
  committed substrate.

## Work packages (this epic)

| Ticket | Directive | Plan actions | Priority |
|---|---|---|---|
| #110 | [01] Repo scaffolding (P0.01) | P0.01 | Normal |
| #111 | [02] CODEX data model + store (P0.02–P0.03) | P0.02–P0.03 | Normal |
| #112 | [03] CODEX explain + Semantic IR codec (P0.04–P0.05) | P0.04–P0.05 | Normal |
| #113 | [04] Golden files + CLI (P0.06–P0.07) | P0.06–P0.07 | Normal |
| #114 | [05] Harness + CI + Phase 0 sign-off (P0.08–P0.10) | P0.08–P0.10 | Normal |
