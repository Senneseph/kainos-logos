# PRIZE PLAN (day-021) — from conditional closure to prize-grade, or an honest route-death verdict

Objective: take the staged program (machine-proven core complete: P1–P9,
the §8 closure as one statement, `p9_closure_at_audit_point`) to a
prize-grade RH proof — or produce the pre-registered honest verdict
that Route A verifies up to a computable ceiling.

Assets that de-risk this (verified on disk, 2026-09-13):
- zero list to T = 6×10⁶: `zeros_T6000000_ext_full.txt`
  (12,193,869 zeros) — the trend experiment is data-feasible NOW.
- per-audit-point cost ~0.1–0.5 s (kernel + ζ) — hours, not months,
  per band.

## PHASE 0 — harden what exists (engineering; no research risk)

- **P0.1 Certification (required before ANY prize submission).**
  Interval-arithmetic re-run (dps-30, tracked error budgets) of the
  weak-spot window (g ≈ 50000.4) and every closing point of the band
  → certified "margin > 1 by explicit ε" at each scanned point.
  Kills the "dps-15 digits, trusted" hole. Feasibility: the 5% margin
  at the weak spot dwarfs any 1e-12 error budget.
- **P0.2 Fill the g-gaps.** Candidate pair every ~100 zero heights
  across [10³, 10⁵] + the unscanned low band [14.13, 10³]
  (the zero list covers both; the day-010 d4 was the only low-band
  record). Result: continuous candidate coverage of [14.13, 10⁵].
- **P0.3 (optional, off critical path):** C1b — promote the t ≠ g
  window floor to a Lean theorem.

## PHASE 1 — the universality question (research; tripwire pre-registered)

This is the only phase with genuine research risk. It is where the
prize is won or honestly declared out of reach.

- **P1.1 The trend scan (decisive experiment, start here).**
  Extend the cross-band margin scan (same window W=12, DT=0.5,
  7-delta grid; G_MAX → 6×10⁶, the T6e6 list) to candidate pairs at
  1×10⁶, 2×10⁶, 4×10⁶, 6×10⁶.
  PRE-REGISTERED DECISION RULE:
  - margin crosses below 1 in any scanned window → Route A's
    pointwise decision fails at T\*; the argument is a verification
    with a computable ceiling T\*; report the ceiling; the prize
    route via this argument is CLOSED; pivot decision (honestly
    logged, as the 246 incident was).
  - margin stays > 1 with a bounded/slow-decaying envelope through
    6×10⁶ → proceed to P1.2.
- **P1.2 The uniform theorem (THE prize mathematics).**
  Prove analytically, for ALL t (and all δ): the squeeze gap holds —
  the uniform package:
    (i)  upper: LHS = |ζ − K_on| ≤ (P4 floor + P5 tail) — mostly
         already theorem-strength (P8Floor A2/A4.3, B3 Sbar);
    (ii) lower: the detector (dev, exact own-height mass by C1a,
         window by C1b) DOMINATES the LHS uniformly in t
         (dev − Mf > Bf + Mr for all t) — the new inequality.
  This is a new uniform inequality for ζ. If proven, compose it into
  Lean (P2.1) and the argument is unconditional.
  OUTCOMES: (a) proven → Phase 2; (b) disproven (the crossing P1.1
  was trending toward) → Phase-1a ceiling report; (c) open after
  serious honest attack → the program stands as the strongest
  verification to date + a falsification program, and the repo says
  exactly that. No outcome is a loss; (b)/(c) are not a proof.

## PHASE 2 — uncondition + publish (only if P1.2(a))

- P2.1 Lean: the uniform package as theorems; C5b closes without the
  hmargin hypothesis; wire B0's axioms to the ACTUAL ζ zero set
  (HNR/HCJ/HFIN from classical theorems — a formalization task).
- P2.2 Paper: the named argument (P1–P9) + the machine-checked core +
  the P0.1 certification record. The certification layer IS the
  community-trust layer; do not write before the math lands.

## STICKY POINTS (ranked)

1. **P1.2 is open mathematics — no guarantee, possibly months.**
   "A uniform inequality for ζ, for all t" is a research theorem,
   and the eroding envelope (112.6 → 1.053 → recovery 2.269) means
   the truth of (ii) is genuinely unknown. The P1.1 scan is a
   tripwire, not a proof. Accept the pre-registered ceiling outcome
   as a legitimate finish — an honest wall is the store's discipline.
2. **The 5% weak-spot margin.** No prize submission can rest on
   dps-15 digits there. P0.1 is mandatory; it is cheap by the
   project's standards.
3. **High-t numerics.** Float64 product over 12M zeros is adequate
   for TREND (at low-margin points resid ~ O(|K|), not tiny), but
   any NEW closing point at high t must be re-certified at high
   precision before it becomes a pin. Budget this; don't let it
   silently become a precision hole like the one C7 caught.
4. **The low band [14.13, 10³].** Never audited as a package; a
   counter-pair's height is a priori anywhere, so the first zeros
   are part of "every height." Cheap to fill (P0.2).
5. **Social layer.** Prize = publication + community validation.
   Sequenced behind the math (P2.2), not before.

## First move (starts immediately)

P1.1 tripwire scan: pairs at 10⁶, 2×10⁶, 4×10⁶, 6×10⁶ (T6e6 list,
G_MAX = 6e6), verbatim day020 functions, records + committed script.
The trend verdict (hold vs cross) is the single most valuable
artifact of the next few hours.
