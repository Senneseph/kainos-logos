# 40 — Metrics (defined once, reused everywhere)

## Correctness (regex)

| Metric | Definition |
|--------|------------|
| syntax | output compiles |
| semantic_correctness | judge verdict (matches intended language) |
| overmatching | # invalid generated strings accepted |
| undermatching | # valid generated strings rejected |
| accuracy | correct / total |

## Generalization

| Metric | Definition |
|--------|------------|
| generalization | accuracy on novel descriptions |
| compositionality | accuracy on unseen operator combinations |

## Memory & learning

| Metric | Definition |
|--------|------------|
| memory_retention | knowledge retained after restart (binary + assert count) |
| updating | term meaning changed without retraining (binary) |
| contradiction_handling | conflicting definitions preserved, not averaged (binary) |
| coverage(T,C) | verified / encountered combinations for term T in context C |
| ontology_size | #terms / #assertions / #exceptions over time |
| compositional_inference | unseen-concept guess accuracy from property conjunction |

## Uncertainty

| Metric | Definition |
|--------|------------|
| abstention | correct "I don't know / clarify" rate on vague input |
| clarification_rate | fraction escalated to a clarifying question |
| justified_rate | fraction of emitted answers with a complete audit trace |
| exception_depth | EXCEPTION cost E at decision time |

## 20 Questions

| Metric | Definition |
|--------|------------|
| questions_to_solve | median questions per game |
| win_rate | games solved within budget |
| info_gain_efficiency | entropy reduction per question |

## Efficiency (Phase 3)

| Metric | Definition |
|--------|------------|
| useful_computation_per_bit_op | the φ-numerics headline metric |
| error_per_op | numeric error at matched bit budget |
| ops_per_result | operations to produce a result |
| data_movement_delta | bytes moved for an incremental knowledge update (vs checkpoint) |

## Meta

| Metric | Definition |
|--------|------------|
| lines_reused | prior-phase LOC reused vs. new LOC (compounding) |
