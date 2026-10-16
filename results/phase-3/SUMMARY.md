# Experiment results

| name | passed | value | threshold | evidence |
|------|--------|-------|-----------|----------|
| e3.1 | PASS | 1.0 | llm_accuracy >= deterministic_accuracy on open phrasing, downstream identical | `results/phase-3/e3.1.json` |
| e3.2 | PASS | 0.49927791099752583 | residual recurrence beats a same-budget MLP on test RMSE for all 3 seeds at matched depth/params (toy scale, hermetic); adopt or reject with a documented margin (P8) | `results/phase-3/e3.2.json` |
| e3.3 | PASS | 1.0 | >= 1 new context TERM, both conflicting assertions retained as established under distinct contexts, disputed -> 0, nodes converged, zero averaged/blended facts | `results/phase-3/e3.3.json` |
| e3.4 | PASS | 1.0 | one entity consolidated from >=2 modalities; one abstract pattern recognized across modalities | `results/phase-3/e3.4.json` |
| e3.5 | PASS | 4.503901165568838e-06 | strict A/B at 8 bits/value: phi must win err-per-op by >=10% and not lose the histogram or ops axes; adopt or reject with a documented margin (P8) | `results/phase-3/e3.5.json` |
| e3.6 | PASS | 1.0 | validity == 1.0; refusal == 1.0; spread >= 2 distinct valid plans with T=0 deterministic; policy ask (high stakes) / default (low stakes) | `results/phase-3/e3.6.json` |
| e3.7 | PASS | 1.0 | all four checks pass; no un-promoted content visible in the CODEX (the anti-corruption invariant, P12) | `results/phase-3/e3.7.json` |
