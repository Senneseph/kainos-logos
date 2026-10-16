# RH proof scaffold — discharge report (kainos training run)
**date** 2026-09-10   **identity** `7ce80adc320c`   **store generation** 87

## facts (from canonical outputs — the store speaks)

- **m-onset-4d**: measured 4-digit law (rows=15 certified, clean=2)
- **m-stage1**: Stage-1 clean rows: (1000,1.0):+0.29%; (10000,0.1):-1.17%
- **f-list-3e5**: N(3e5)=466655 (dt=dt2, gate 6.5e-10, min gap 0.00575)
- **f-window-1e7**: 227197 flips STABLE
- **f-cert-1e5**: 2K=-2@6.6e-08 S=-2.5584
- **f-cert-1e6**: 2K=-2@6.6e-09 S=-2.5086
- **f-cert-1e7c**: 2K=0@2.2e-09 S=-1.2057
- **f-pair-id**: B-4 unit PASS (dLa 3e-14, dAr 3e-16)
- **d4-dev**: D4/D3 complete (gstar=999.791572)
- **b5-core**: core theorem VERIFIED (fs-vs-meas 0.0005, vs-direct 6e-26)
- **d4-far**: far-scale LANDED (|R-1| = c^2 6-digit, max 10000)
- **d3floor**: fine floor LANDED (median 2.9e-03, p90 1.9e-02, max 3.9e-02)
- **d1-6e6**: PENDING (6e6 walk in flight)
- **d5-1e7-red**: PENDING (in flight)
- **d2-fits**: PENDING (queued, small)

## line end (record complete up to)

- **certified-fac-cert-1e5**: N=138065 S=-2.5584 2K=-2
- **certified-fac-cert-1e6**: N=1747142 S=-2.5086 2K=-2
- **certified-fac-cert-1e7c**: N=21136123 S=-1.2057 2K=0
- **certified-list-3e5**: N(3e5)=466655 gate=6.541e-10
- **stable-window-1e7**: {'flips_9p9e6_1e7': 227197, 'window': '[9.9e6, 1e7]', 'dt2_matches_dt': True}

## discharge: plan-A (route A, definition-side)

- closure: 18 nodes
- FULFILLED (10): b5-core, b5-detector, c-25212, c-fe, c-rvm, d-pair-unit, d4-dev, fa-pair-id, m-onset-4d, m-stage1
- PENDING-DATA (2): d1-6e6, d2-fits
- TO-BUILD (6): b0-counting-equiv, b1-onset-thm, b2-rigorous-tail, b3-bridge-id, b6a-route-a, c-zeta-pos
- **runnable frontier (prereqs all fulfilled)**: d1-6e6, d2-fits, c-zeta-pos

## discharge: plan-B (route B, uniform dynamics)

- closure: 9 nodes
- FULFILLED (5): c-fe, c-rvm, fac-cert-1e5, fac-cert-1e6, fac-cert-1e7c
- PENDING-DATA (0): —
- TO-BUILD (4): b0-counting-equiv, b6b-route-b, c-zeta-pos, x-s-theory
- **runnable frontier (prereqs all fulfilled)**: c-zeta-pos, x-s-theory

## discharge: plan-C (hybrid interim: RH to T)

- closure: 3 nodes
- FULFILLED (3): fac-cert-1e6, fac-cert-1e7c, fac-window-1e7
- PENDING-DATA (0): —
- TO-BUILD (0): —
- **runnable frontier (prereqs all fulfilled)**: — (blocked upstream)

## circularity + invariants

- cycles: **0** (CLEAN)
- P5 violations: **0** (none — rh stays hypothesis)