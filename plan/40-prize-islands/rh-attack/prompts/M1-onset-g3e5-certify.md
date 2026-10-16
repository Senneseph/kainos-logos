# PROMPT M1 — publish onset-bridge Stage-1 (CERTIFIED, done 20:35)

CONTEXT (open, don't assume).
- spec/onset-bridge-e7b1.md — the whole piece: measurement, prediction,
  corrected error budget, per-point table, incident log (a)–(f).
- day-009.md §8 (the short version) + out_day009c_onset_pred_certified.
  txt (the canonical output; docker mpmath 1.3.0, certified list).
- out_day009c_onset_pred_ext.txt = INVALIDATED (buggy list) — do NOT
  cite; kept as detection-path record only.

WHAT IS DONE (do not redo).
- G=3e5 zero list CERTIFIED: N(3e5) = 466,655 (dt/dt2 agree, gate
  6.5e-10, min gap 0.005750, anchor 138,065). File:
  scripts/rh/zeros_T300000_ext_full.txt (466,655 +γ, strict monotone).
- Onset Stage-1 run in docker 1.3.0: clean PASS (1e3,1.0) +0.29%,
  (1e4,0.1) −1.2%; borderline (1e3,2.0) +5.8%, (1e4,0.2) +4.2%; rest
  in-budget (C below the zero-side error floor).

TASK (repo update only — no new runs).
1. rh-missing-tail: Stage-2 table + results/certified-zero-survey.md:
   add N(3e5) = 466,655 (certified 2026-09-09, walk dt/dt2 agree +
   engine gate + dps anchor chain). Add a Stage-4 (E7b-1) status
   paragraph: Stage-1 result with the per-point table and the honest
   ceilings (density tail saturates; N=1e5 row needs G ≳ 5–6e6 = the
   M5 decision matrix). Label: MODEL output (prediction vs measured),
   per claim policy; no RH claims.
2. Commit kainos-logos rh-attack paths (day-009 §8, spec, FORMULAS,
   the day009b/c scripts + certified outputs + flips + the 3e5 list);
   exclude: the 1.2GB defective S-walk (already VCS-excluded), the
   .PARTIAL-only-upto-300000 zero files (incomplete by name).
3. Push rh-missing-tail (status + certified N(3e5)).

DONE WHEN. The repo reflects: certified N(3e5); Stage-1 onset table
with error floors; both incident findings the reader needs (mpmath
1.4.1 quad defect → "docker 1.3.0 verified environment"; sort -g).
CONSTRAINTS. P-0.9 provenance on every number; certified numbers only
(claim policy); no e6.28 paths in any git command.
OUT OF SCOPE. Running the G=5e6+ walk (M5, on the owner's
"test extensively later" decision).
