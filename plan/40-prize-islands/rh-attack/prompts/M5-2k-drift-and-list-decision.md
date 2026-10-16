# PROMPT M5 — 2K drift formal write-up (+ extended zero list, on demand)

CONTEXT.
- FORMULAS.md §2.3 (2K identity + drift reading; Day-007 correction:
  per-height, not conserved)
- day-007.md (drift exponent, the −3 at γ*±0.25 reading)
- spec/zero-walks-and-certificates.md (the jobs/defects map)

TASK (write-up, no new long runs).
1. A tight section in THE-EULER-ACTION.md: what 2K(T) is (identity),
   what it drifts (derivation of the ~−3/rad rate from ṁain + Ṡ),
   why per-height evenness is the valid certificate, what an ODD 2K
   at a certified height WOULD mean (off-line zero candidate → the
   protocol), and why the −3 readings at γ*±0.25 are expected
   (they're on the drift ramp, at half-integer height offsets from a
   certified zero).
2. The extended-list decision matrix: from the onset error budget
   (spec onset-bridge, LIMITATIONS), the exact (T_max of interest) →
   G needed pairs; the day009b script (P-0.8 compliant) is the
   executor — launch it at the chosen G when a milestone needs it
   (M1's G=3e5 is the current ceiling; 6e6 = the full N=1e5 row).

DONE WHEN. The 2K section is committed (claim: inference, labeled;
the drift rate is DERIVED with the derivation shown; the evenness
certificate is MEASURED at 1e5/5e5/1e6).
OUT OF SCOPE. Running the 6e6 walk now (owner: build the model first,
test extensively later).

STATUS (2026-09-10, day-012): data COMPLETE for the write-up.
- The 6e6 walk was later owner-ordered and LANDED (day-011 §4c
  truncation incident + fix; `75d2ba5`): N(6e6) = 12,193,869, float
  re-certified, S(6e6) = −2.9349 (O(1)), G=6e6 onset rows landed
  (out_day010_onset_G6e6.txt; method ceiling t ~ 10⁴–2×10⁴; Stage-1
  five-row pattern within ≤6 %).
- Onset budget now has two operating points: G = 3×10⁵ and
  G = 6×10⁶ — the (T_max)→G decision matrix is buildable today.
- S/2K heights ready: 1e5 (cert), 1e6 (cert), 6e6 (float),
  1e7 (cert, corrected) — see out_day010_dps1e7.txt + day-012 §4
  (the 6e6 point is float-only; dps cert = the named missing
  ingredient for a MEASURED label at every height).
- The "2k ledger" item (M4-Ph3 queue) has no written spec in the
  store — owner to define; the write-up does not depend on it.
