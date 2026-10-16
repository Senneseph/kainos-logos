# SPEC — zero-walks-and-certificates (counting machinery)

PURPOSE. Count zeros below T and certify counts (twin-floor + dt/2
stability + 2K parity + dps spots). All published counts are
resolution-limited measurements (P-0.2).

RULES (P-0).
1. dt < twin-floor(t); smallest measured gap on (1e5,1e6] = 0.002954.
2. Every walk ships a dt/2 stability re-walk; equal flip counts.
3. 2K(T) = (N − main + 1) − argζ/π (dps) is a per-height PARITY
   reading (even = consistent), not a count verifier.
4. dps spot certifications (N, S, 2K at the height) are the
   certificates of record: S(1e5) = −2.558419306, S(1e6) =
   −2.508632116, 2K = −2 at 5e5 & 1e6 (dps-40).
5. Float64 2-term engine validity map: twin-safe t ≥ 1e5 only
   (zero-core spec).
6. Defective files are RENAMED .DEFECTIVE with a NOTICE (P-0.9) —
   current: the two dt=0.1 files on [1e4,1e5] (invalid below ~2e4)
   and the GPU re-walk file on [1e4,1.9e4] (engine twin-unsafe there).

JOBS (2026-09-09 evening / 2026-09-10 ~00:40).
- DONE (CPU): day005g dt025 window [9.9e6, 1e7]: coarse 227,197 =
  fine 227,197 flips, EXACT agreement (out_day005g_dt025.txt);
  θ/π@9.9e6 = 20908927.312166, @1e7 = 21136124.205718.
  ⇒ corrected N(1e7) = 20,908,926 + 227,197 = **21,136,123**
  (S_file = −1.2057182 to 7 digits by the θ convention) — the
  pre-registered +246 candidate CONFIRMED by an independent
  exact-agreement re-walk. Pending: day006 early re-walk (region
  (1e6, 3.026e6]) + day005h dps verifier (2K parity, dps S) → THEN
  the repo number moves (claim policy).
- RUNNING (CPU): day006 early re-walk (1e6 → 3.026e6) — 683 CPU-min
  at 00:40 (single-threaded; output buffers to end-of-run).
- DONE (GPU): day009b seg00 (1e5→3e5) CERTIFIED re-walk (466,655,
  both passes); [3e5, 6e6] deferred (owner: test later).

INVENTORY (certified, locked).
- N(1e5)=138,065 (certified; zeros_T100000.txt, 138,065 lines).
- N(1e6)=1,747,142 (dps-40 + twin-corrected walk).
- N(1.9e4)=21,211 (certified zero list — the reference that exposed
  the float64 low-t defect).
- N(1e7) DEFECTIVE 21,135,877 / candidate 21,136,123 (pending re-walks).
