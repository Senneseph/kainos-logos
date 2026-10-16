# 40 — Benchmark registry

Stable experiment IDs. Each entry: phase, claim, metric, threshold, status.

| ID | Phase | Claim | Metric | Threshold | Status |
|----|-------|-------|--------|-----------|--------|
| E0.1 | 0 | substrate soundness | round-trip fidelity | == 1.0 | 🟡 planned |
| E0.2 | 0 | harness self-test | dummy passed | True | 🟡 planned |
| E1.1 | 1 | parity | accuracy | == 1.0 | ⚪ planned |
| E1.2 | 1 | compositionality (C1) | accuracy vs baseline | ≥ baseline + margin, ≥ 0.8 | ⚪ planned |
| E1.3 | 1 | persistent memory (C2) | retention before/after restart | == 1 both | ⚪ planned |
| E1.4 | 1 | honest uncertainty (C3) | clarification/justified rate | ≥ 0.5 / == 1.0 | ⚪ planned |
| E1.5 | 1 | A/B vs conventional (C1) | compositional accuracy | B > A (significant) | ⚪ planned |
| E2.1 | 2 | active acquisition (A1) | questions-to-solve vs random | ≥ 20% fewer, win-rate ≥ | ⚪ planned |
| E2.2 | 2 | EXCEPTION shrinkage (A2) | coverage ↑, exceptions ↓ | trend, statistically | ⚪ planned |
| E2.3 | 2 | persistent growth (A3) | with vs without CODEX | with < without | ⚪ planned |
| E2.4 | 2 | compositional recognition (A4) | inference accuracy | ≥ 0.7 | ⚪ planned |
| E2.5 | 2 | contradiction → dimension (A5) | new context TERMs | ≥ 1, no averaging | ⚪ planned |
| E3.1 | 3 | LLM kernel A/B | open-phrasing accuracy | LLM ≥ deterministic | ⚪ planned |
| E3.2 | 3 | Fibonacci topology (gated) | accuracy @ matched budget | strictly better or reject | ⚪ planned |
| E3.3 | 3 | distributed reconciliation | new context TERM | ≥ 1, no blending | ⚪ planned |
| E3.4 | 3 | multi-modal abstraction | cross-modal consolidation | ≥ 2 modalities | ⚪ planned |
| E3.5 | 3 | φ numerics (gated) | computation per bit-op | strictly better or reject | ⚪ planned |

Status legend: 🟡 in progress · ⚪ planned · 🟢 passed · 🔴 rejected (gated) · ⛔ failed.
