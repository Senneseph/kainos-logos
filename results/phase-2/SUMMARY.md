# Experiment results

| name | passed | value | threshold | evidence |
|------|--------|-------|-----------|----------|
| e2.1 | FAIL | 0.0 | directive: system questions-to-solve median >= 20% lower and win-rate >= baseline | `results/phase-2/e2.1.json` |
| e2.2 | PASS | 0.349 | coverage strictly up and unknown cells strictly down across the run | `results/phase-2/e2.2.json`, `results/phase-2/growth.md` |
| e2.3 | PASS | 0.1463 | with-persistence < without-persistence and learned assertions survive the restart | `results/phase-2/e2.3.json` |
| e2.4 | PASS | 1.0 | accuracy >= 0.7 (baseline with zero labels: 0.0) | `results/phase-2/e2.4.json` |
| e2.5 | PASS | 1 | >= 1 new TERM, both retained, disputed count 0 for the pair after reconciliation | `results/phase-2/e2.5.json` |
