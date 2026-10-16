# PROMPT M3 — 1e7 certification closeout (the two CPU re-walks land)

CONTEXT.
- spec/zero-walks-and-certificates.md (rules + job list)
- scripts/rh/out_day005g_dt025.txt + out_day006_early_rewalk.txt
  (buffer to end-of-run; PIDs 1142168 / 1142170, launched ~13:17)
- scripts/rh/day005h_verify_1e7.py (pre-staged dps-45 verifier)
- LOCKED: N(1e7) defective 21,135,877 (246 missed flips, one dead 256k
  GPU chunk near 1.06e6); candidate 21,136,123.

STATUS (2026-09-10 00:40).
- dt025 window [9.9e6, 1e7]: DONE — 227,197 = 227,197 EXACT
  (out_day005g_dt025.txt); θ/π @1e7 = 21136124.205718.
  Corrected N(1e7) = 20,908,926 + 227,197 = 21,136,123, S_file =
  −1.2057182 (θ convention) — the +246 candidate CONFIRMED pending
  the two remaining M3 gates below.
- day006 early re-walk (1e6 → 3.026e6): RUNNING (683 CPU-min).
- day005h dps verifier: PENDING (runs after the re-walk).
STATUS (2026-09-10, day-012). UNCHANGED, still blocked.
- day006 early re-walk: PID 1142170, ~22 CPU-h, single-thread ~99 %,
  output 0 bytes (buffered). Do-not-kill (owner rule).
- day005h dps verifier: still PENDING behind it.
- Side data landed for the closeout context: 6e6 list completed +
  float re-certified (day-011 §4c incident; chain-verify PASS on the
  corrected 12,193,869-zero list; S(6e6) = −2.9349) + G=6e6 onset
  rows (out_day010_onset_G6e6.txt) + independent S-profile witness
  (scripts/rh/out_day012_s6e6_profile.txt; N(3e5)/N(1e6) anchors
  exact). None of this substitutes the re-walk gate.

STATUS (2026-09-11, day-014). **DONE — with the LOCKED +246 revised to +244.**
- The do-not-kill re-walk (PID 1142170) completed its window and exited
  (file written 2026-09-10 20:22 local): [1e6, 1.4e6], CPU engine,
  dt = 5e-4 AND dt/2 = 2.5e-4, 773829 = 773829 EXACT (STABLE), min gap
  0.0065 (≫ 2·dt). Cumulative diff vs the reconstructed N_orig plateaus
  at **+244 by t = 1,000,128 and is flat to 1.4e6** — the dead chunk is
  (1.0×10⁶, 1.000128×10⁶], 128 rad, NOT near 1.06×10⁶ as the early
  S-plateau estimate said. Cross-instrument: the day-009 6e6 zero list
  contains EXACTLY 773829 zeros in (1e6, 1.4e6] — two independent
  engines agree on every zero of the window. N(1.4e6) = 1,747,142 +
  773,829 = 2,520,971 by exact arithmetic on certified inputs.
- The pre-registered "LOCKED +246 / candidate 21,136,123 / S = −1.2057"
  is **FALSIFIED WITH COMPUTATION**: +246 was the coarse |ΔS|-estimate
  ("S drops from −2.5 to −~248.75"), never a direct count. Corrected:
  **N(10⁷) = 21,136,121, S(10⁷) = −3.205718 (dps-45), 2K(10⁷) = −2**
  (dist-to-even 2.25×10⁻⁹); parities at 1.4e6/5e6/9.9e6 all EVEN
  (dist ≤ 1.8×10⁻⁹). Record: out_day014_dps45_arg1e7.txt.
- HONEST WALL (new, recorded): 244 vs 246 differ by exactly 2 → the
  2K/even-identity (at ANY precision, float or dps-45) can NEVER
  arbitrate them — the principal arg of ζ(1/2+it) is known mod 2πK and
  N enters the identity mod 2 only. The arbiter is the DIRECT dt/dt2
  stable count (773829), doubly confirmed by the 6e6 list. A parity
  certificate is a parity certificate; it is not a count certificate.
- BUG FOUND IN THE PRE-STAGED VERIFIER (day005h_verify_1e7.py): (1) the
  mp payload was concatenated into the program source instead of being
  piped as stdin data (SyntaxError); (2) its formula
  g = arg(Γ(1/4+it/2)) − (t/2)lnπ via mpmath gives the PRINCIPAL arg
  (∈(−π,π]) — the DLMF 25.10.2 θ needs the continuously-continued arg,
  so its "dps-45 S" line is unusable at ANY t (first exposed today at
  t = 1.4e6: it printed "S = 255063.93"). Fixed: (1) script-file +
  stdin payload, (2) replaced by the day003-sanctioned principal-arg
  test (day014_dps45_arg1e7.py), which is exactly the strength the
  identity has (mod-2 parity + O(1) S), and no more.
- Middle window (1.4e6, 9.9e6) of the defective file: single-blackout
  model (pre-registered) — S_file flat at −247.0…−247.3 with no jump >
  0.27 across it; residual risk of 1–2 flips below 1-rad sampling in
  the flat region: UNMAPPED, not certified by re-walk (≈ days of CPU
  work). Tail (9.9e6, 1e7]: CPU dt/dt2 exact (227197 = 227197).

TASK (remaining).
1. When both output files are non-empty: read them. Check dt vs dt/2
   flip agreement (P-0.2), min gaps, blackout localization in the
   [9.9e6, 1e7] window.
2. Run day005h_verify_1e7.py (docker mpmath, dps-45): 2K at 1e7 and
   5e6, S(1e7) exact.
3. Record: corrected N(1e7), S(1e7), dead-chunk delta; P-0.9
   provenance lines (script revisions, dt, floor, dt/2 result).
4. Update: day-005.md (the 1e7 entry — replace the DEFECTIVE block
   with the certified one, keep the defect story as history),
   POSTULATES P-Z row, repo Stage 2 + results/certified-zero-survey.md,
   then push (this IS a certification: claim policy satisfied).

DONE WHEN. N(1e7) and S(1e7) are on record as dps-certified with the
re-walk certificates (dt/dt2 agree, floor, 2K parity) — and the
DEFECTIVE label is gone from the repo.
CONSTRAINTS. Do not touch the re-walks while running (owner rule).
If dt/dt2 DISAGREE: stop, write the disagreement down, do NOT publish
numbers from that window (that's a wall, log it as a wall).
OUT OF SCOPE. Any walk below 1e5 (engine map says unreliable; dps
spots own that range).
