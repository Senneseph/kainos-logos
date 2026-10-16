# Action Step 20 — Multi-modal demo + final consolidation (P3.09–P3.11)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

Prove the "one algebra" claim at the modality level (a synthetic vision port and text
share one abstract CODEX pattern), then write the final consolidated acceptance report.

## Prerequisites

- [ ] Steps 17–19 **and 21–22** done (LLM kernel, numerics/topology verdicts,
  distributed reconciliation, projection, workspace). Note: 21 and 22 run *before*
  this final consolidation despite their numbers — see the ordering note in
  `action-steps/README.md`.

## Background

The unifying claim: the same abstract Codex represents patterns across modalities.
This step demonstrates it with the cheapest honest modality — a synthetic "vision"
port — and then signs off the whole project against the **eight** "full-realized"
checks (six original + X1 projection + X3 workspace).

## Steps

### 1. `src/kainos/multimodal/port.py` + `synthetic_vision.py`

- `PerceptionPort` protocol: `perceive(raw) -> SemanticIR`.
- `SyntheticVisionPort`: input = a grid/scene description (list of objects with
  positions at two timestamps) → emit IR `entities` + `relationships` (e.g.
  `box --located_at--> (x1,y1,z1)` then `(x2,y2,z2)`).

### 2. E3.4 demo

`run_e3_4()`: text `"John moved the box"` **and** the synthetic scene both reduce to
`TRANSFER(object=box, A, B)`; consolidate the shared entity. → `results/phase-3/e3.4.json`.
Threshold: one entity consolidated from ≥2 modalities; one abstract pattern recognized
across modalities.

### 3. Tests

`tests/multimodal/test_synthetic_vision.py`: synthetic scene → IR with entities +
relationships; the shared `TRANSFER` pattern is produced from both text and scene.

### 4. Final consolidation

`plan/30-phases/phase-3-generalization/results.md`:
- E3.1–E3.5 tables;
- a "did the unifying claim survive?" table (per sub-project: adopt/reject + margin);
- map each of the **eight** "full-realized" acceptance checks (from
  `phase-3-generalization/README.md` — six original + X1 projection + X3 workspace)
  to an evidence artifact;
- map each north-star success criterion (persistent memory, compositionality, honest
  uncertainty, inspectability, compounding) to its end-to-end evidence across phases.
- render `results/phase-3/SUMMARY.md` via the harness `report` command (matching
  phases 1–2).
- Update `plan/20-roadmap.md` status ledger and `plan/03-adr.md` (φ/topology adopt/reject).

## Verification

```bash
pytest tests/multimodal -q && kainos experiment run --name e3.4
```

Expect: multimodal test green; E3.4 thresholds met; final results.md complete.

## Done when

- [ ] synthetic vision port emits the same abstract `TRANSFER` pattern as text
- [ ] E3.4 threshold met (≥2 modalities consolidate one entity)
- [ ] final `results.md` maps all **eight** acceptance checks + all five north-star criteria to evidence
- [ ] `results/phase-3/SUMMARY.md` rendered by the harness
- [ ] ADRs + roadmap ledger updated

## Full project DONE after this step.

Update `action-steps/README.md` (all steps ✅) and consider `plan/90-appendices/research-questions.md` — did the system ever discover an abstraction its designer didn't put in the ontology? That's the final verdict.

## If stuck

`plan/30-phases/phase-3-generalization/experiments.md` → E3.4, `plan/30-phases/phase-3-generalization/README.md` (acceptance checks).
