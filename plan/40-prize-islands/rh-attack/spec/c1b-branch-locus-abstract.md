# C1b — the branch-locus detector floor (own-regime promotion)

Status: DRAFT SPEC (2026-09-16, goal turn). The open analysis atom of the
outline: promote the PINNED near-regime detector floor
(`p9_f_pin = 0.9975`, Closure P9; day-010 d4d3 audit) to a LEAN theorem.
Parent spec: `closure-module-abstract.md` §1. Route-A's price per
outline §10.

## 1. The object

The deviation ratio (B5, Lean-proven `b5Ratio`/`b5Abs`, T ≠ γ branch):

    R(γ, δ, t) = pref(γ,δ,t) · exp((½ + it)·ω_δ)

with the EXACT rational forms (Lean: `B5.pref`, `B5.omegaD`):

    pref(γ,δ,t) = (¼+γ²)·((γ−t)²+δ²)·((γ+t)²+δ²)
                  / ((γ²−t²)·(¼+γ²+δ+δ²)·(¼+γ²−δ+δ²))

    ω_δ = (1+2δ)/(¼+γ²+δ+δ²) + (1−2δ)/(¼+γ²−δ+δ²) − 1/(¼+γ²)  ∈ ℝ

The detector (P8/P9): ‖R(γ,δ,t) − 1‖, at the candidate off-line pair
(γ, d₀), evaluated at the point t.

## 2. Branch-locus structure (the part the δ = 0 Lean facts do not see)

- pref has denominator factor (γ² − t²): pole at t = γ for every δ > 0.
  The B5 Lean theorems (b5Ratio, b5Abs, p8_pref_omega_zero) all carry
  the hypothesis t ≠ γ — the t = γ column is OUT of the Lean core.
- At t = γ, δ > 0: the RATIO poff/pairProd has pairProd = 0 (the on-line
  factor at its own height: (1 − s/ρ)|_{s=ρ} = 0) — a GENUINE pole —
  ‖R − 1‖ = ∞ there. The pole column is therefore DETECTOR-TRIVIAL
  (the ≥ side is infinite); no floor is needed at t = γ itself.
- Along δ = 0 (removable): pref(γ,0,t) = (γ²−t²)/(¼+γ²) — R(γ,0,γ) = 0,
  ‖R−1‖ = 1 exactly (LEAN-PROVEN by A3.2b.1 at δ = 0 for t ≠ γ, and by
  continuation at t = γ if desired).
- The near-window floor must cover t ≠ γ, |t − γ| ≤ W, δ ∈ (0, δ_max]:
  there |R| = |pref|·e^{ω_δ/2} is SMALL (pref ~ (t−γ)/(γ+t) → 0 at the
  column), and the reverse-triangle fact (P8 A3.2a,
  `p8_detector_abs_lower`) gives

      ‖R − 1‖ ≥ ||R| − 1| = 1 − |R|        (when |R| ≤ 1)

  So a LOWER bound on the detector is a UPPER bound on |R|:

      THE C1b STATEMENT (working form):
        ∀ γ, t, δ in the window (γ ≥ γ₀, 0 < |t − γ| ≤ W,
        0 < δ ≤ δ_max),
            |pref(γ,δ,t)| · exp(ω_δ/2) ≤ 1 − f   (f = 0.9975 pinned,
            or a sharper f proven from the analysis),
        hence ‖R(γ,δ,t) − 1‖ ≥ f.

## 3. The window (must match the audited regime)

From the day-020 worstcase audit (`scripts/rh/out_day020_worstcase.txt`)
and the day-010 d4d3 record:
- γ in the audited range of candidate pair heights
  (γ₀ ≈ 14.13 the smallest certified zero height is the natural lower
  edge — the floor must hold at LEAST from there up; the audit verified
  γ ~ 10³; the γ-dependence of pref is monotone in (γ+t) — check the
  direction numerically first),
- W = 10 (the d4 audit window; the worstcase audit used 12 — re-pin),
- δ ∈ [0.005, 0.5] (the measured d-grid edge = `p9_d_min` to
  δ_max = 0.5),
- t ≠ γ (the pole column is detector-trivial, documented separately).

## 4. Analysis plan (one category at a time)

Step 0 (measurement, pin never recall): a numerical probe on the exact
rational pref finds (i) the WORST POINT (γ*, t*, δ*) of
|R| = |pref|·e^{ω/2} on the window and the value 1 − f_proven, (ii) the
γ-direction (does |R| grow or shrink with γ?), (iii) the δ-direction.
Script: `scripts/rh/day021_c1b_worstpoint.py` (mirror `B5.pref`/
`B5.omegaD` line-for-line, dps verification of the worst point).

Step 1 (Lean atom C1b.1): the γ-monotonicity of |pref(γ,δ,t)|·e^{ω/2}
on the window — if monotone decreasing in γ (γ growing shrinks pref like
1/(γ+t)·γ²/γ⁴ ~ 1/γ²), it suffices at γ₀; the exponential factor
e^{ω/2} with ω_δ ≤ 2/(¼+γ₀²) (tiny) is bounded by e^{2/(¼+γ₀²)} — a
named constant.

Step 2 (Lean atom C1b.2): the (t, δ) two-variable maximum of
|pref| on {0 < |t−γ| ≤ W, 0 < δ ≤ δ_max} — at γ = γ₀ — via the
polynomial form: |pref|·(den) = num is a polynomial in
u = t−γ, v = t+γ, w = δ (all-positive-coefficient analysis per B5
`b5NoffIsPolynomial` style); candidate critical points: boundary
corners (|u| = W, δ = δ_max or δ → 0+) and any interior stationary
point — the δ → 0+ edge: pref(γ,0,t) = (γ²−t²)/(¼+γ²) — |γ²−t²| ≤
W(2γ+W): bounded by W(2γ₀+W)/(¼+γ₀²) — a clean linear bound in W.

Step 3 (Lean atom C1b.3): composition
  ‖R − 1‖ ≥ 1 − |pref|·e^{ω/2} ≥ f  (f pinned from Step 0)
  as `p9_c1b_near_floor : ... ≤ |pref|·exp(ω/2) → ...` → the
  `p9_f_pin` promotion: replace the PINNED constant in C1-own with the
  theorem (the window becomes a hypothesis of the theorem).

Step 4 (Composition root): the own-regime half of C1 becomes
LEAN-PROVEN on the window; the C5b margin hypothesis's `flo` witness
becomes the theorem (far: A4.1; near: C1b) instead of the pinned
constant — the §8 closure's last measurement input retires to a day-log
constant (W, γ₀, δ_max — the window parameters, still pinned; the
detector SCALE becomes proven).

## 5. Honest split (target)

- C1b.1–C1b.3: LEAN-PROVEN (window parameters pinned).
- The window itself (W = 10, γ₀ = 14.13..., δ_max = 0.5): PINNED
  (measurement + certification data; the window is the instrument's
  honest range of validity, per the outline's route decision).
- If Step 0 shows the worst point is OUTSIDE (W, δ_max) or the bound
  needs W < 10: re-pin the window (the audit margin 112.6× has room:
  the decision survives any floor ≥ resid/dev ≥ 1/112.6 ≈ 0.0089 —
  i.e., the floor only needs to beat ~1%, not 99.75% — the near-floor
  is conservative by design).

## 6. Method pins (from the P9/C0 session, 4.33.1)

- `set ... with` for unopacity equations (lets are opaque).
- `Finite.mem_toFinset` needs `open Set`.
- `noncomputable def` for any ℝ-division constant.
- reverse triangle: `p8_detector_abs_lower` (A3.2a) — no re-proof.
- the δ = 0 closed form: `p8_pref_omega_zero` /
  `p8_detector_norm_at_zero` (A3.2b.1) — the removable branch is
  already Lean-proven for t ≠ γ.
- no MVT style: prefer polynomial/monotonicity/ring arguments (the
  B5/P8 house style).

## RESOLVED (day-021) — the critical path was the pole, not the window

The audit (`rh-missing-tail/scripts/rh/day021_c1b_worstpoint.py`)
found the branch locus is the **pole at t = g**: the on-line pair's
25.2.12 factor vanishes at its own point (pairProd(g, g) = 0) while
the four off-line factors are nonzero for 0 < d < 1/2. The §8 closure
(C5b) evaluates the detector at the MINIMAL off-line pair height
t0 = g — **at the pole** — so its ≥ side is the EXACT finite kernel
change poff(g, d, g), a strictly positive constant (Lean: C1a, 7
atoms in `RhAttack/Closure.lean`, commit `6d7f369`):
`p9_fac_self_zero`, `p9_pairProd_at_own_height`, `p9_fac_ne_zero_of_ne`,
`p9_poff_own_height_nz_full`, `p9_kernel_change_at_own_height`,
`p9_detector_at_own_height`, `p9_poff_own_height_pos`.

Consequences:
  1. The "f ≥ 0.998 at own height" line of the outline is replaced by
     an exact statement (the ratio has a pole at own height; the
     kernel-change mass is positive).
  2. The 0.9975 pin degrades from *critical path* to *recorded window
     audit*: it bounds |R − 1| on the t ≠ g straddle window, which the
     closure does not evaluate. Its C1b promotion (the two-variable
     minimum of |R − 1| on the window) is now OPTIONAL.
  3. The window structure is still characterized for the record:
     |R| crosses 1 with a phase jump of π (unit-circle crossing =
     sign flip of Re(R − 1)), |R − 1| dips of ~0.06–0.11·(1/γ) at
     γ ≈ 1000 for δ in [0.005, 0.05]; far tails saturate at 1.

Toolchain pin recorded in DISCOVERY_LOG 15: a nondeterministic
linarith "synthetic hole" failure on equality goals with strict
hypotheses in Lean 4.33.1 — C1a uses deterministic tactics only.

## RESOLVED-2 (day-023 25i) — the pole-RIDGE; the statement re-shaped

Step 0 (`rh-missing-tail/scripts/rh/day023_c1b_globalmin.py`,
DISCOVERY_LOG 25i) located the worst structure of ‖R − 1‖ on the
CONTINUOUS window: a RIDGE approaching the pole column from u → 0⁻ at
d → 0.5⁻ (u = t − γ):

    R → e^{i·θ(γ)} · 1,   θ(γ) ≈ 1/γ   (|R| → 1 through the 1/u pref
    pole at u* ≈ 0.5/γ).

  dps-30 global min ‖R − 1‖ = 0.0201349167917 at γ = 49.66730, u =
  −0.01, d = 0.498 (|R| = 0.9988886, arg(R) = 0.02011574 ≈ 1/γ);
  ridge value → 1/γ → 0 as γ → ∞.

Consequences (the spec's working-form statement is re-shaped):
  1. §2's "THE C1b STATEMENT (working form)" — the |R| ≤ 1 − f
     UPPER-bound route — is REFUTED as a continuous-window theorem:
     |R| is unbounded near the pole column and tends to 1 along the
     ridge; there is NO positive uniform floor on the continuous
     window.  (Day-021 V6's "min → 0.9995 as g → 1e5" was a grid
     artifact that missed the ridge below du = 0.01.)
  2. The 0.9975 pin is a DISCRETE-STRADDLE pin: the closure evaluates
     the detector at the MEASURED straddle heights u ∈ 0.5·ℤ \ {0}
     (+ the pole column = the C1a regime).  The ridge point
     u* ≈ 0.5/γ falls BETWEEN grid points, so the DISCRETE floor is a
     separate, much larger object:
         floor_disc(γ) = min over u = 0.5k (0 < |u| ≤ W), 0 < d ≤ ½
                    of ‖R(γ, d, γ+u) − 1‖
         ~ min( corner(γ), 1 − c/γ ),
     the |u| = W corner carrying |R| ≈ 2(u²+¼)/(γ|u|) (≈ 2(W/|u|)·
     2·(W²+¼)/W/γ = O(W/γ)), and a small-γ corner minimum
     (measured 0.02384820641 at γ₀ = 14.1347, u = −W, d = ½, coarse).
     Pin consistency: 1 − 24/1000 = 0.9976 ≈ 0.9975 (the pin's own
     audit height ~ 10³).
  3. If the promotion is pursued (still OPTIONAL for the closure — the
     measured dev at each witness exceeds the pin it replaces; the
     ridge shows WHY the closure can stay on measured-dev language),
     the theorem to prove is the DISCRETE floor bound
        ‖R(γ, d, γ + 0.5k) − 1‖ ≥ min(m_corner, 1 − c/γ)
     for the grid k = ±1..±⌊2W⌋, 0 < d ≤ ½, γ ≥ γ₀ — an elementary
     rational-function bound (|pref| upper bound from the all-positive
     polynomial form + the arg(pref) = 0 / t·ω_δ phase structure on
     the grid, the ridge excluded by DISCRETENESS, not by an estimate).
     Constants (m_corner, c): Step 0b (`day023_c1b_discrete.py`, dense
     dps-30 map, in flight).  Then Step 1 (the bounds), Step 2 (Lean).

## RESOLVED-3 (day-023 25k) — constants fixed; promotion OPTIONAL

Step 0b (`day023_c1b_discrete.py`, out_day023_c1b_discrete.txt) on the
corrected window grid (0.005 ≤ δ ≤ ½, u = 0.5k, |k| ≤ 24, 38 log γ
points, dps-30):

  - floor_disc(γ) MONOTONE INCREASING: 0.02384820641 (γ₀, u = −12,
    δ = ½) → 1 − 24.0458/γ·(1 + o(1)) (corner asymptote 2(u²+δ²)/
    (γ|u|) = 24.04/γ at |u| = 12).
  - Candidate theorem `p9_c1b_disc_floor` (ZERO violations on the
    grid):  ‖R(γ, δ, γ + 0.5k) − 1‖ ≥ min(0.023, 1 − 25/γ)
    (γ ≥ γ₀, k = ±1..±24, 0 < δ ≤ ½).
  - Pin consistency CLOSED: 1 − 24.04/1000 = 0.997596 ≈ 0.9975 at
    the pin's own audit height (γ ~ 10³).

SCOPE DECISION (in force): the promotion is OPTIONAL for the closure.
The closure evaluates the detector at its MEASURED witness points
(per-point recorded dev, exceeding the pin); it can never touch the
pole-ridge (u* ≈ 0.5/γ is off the 0.5·ℤ straddle grid).  Replacing
the working pin with the coarser proven bound is bookkeeping value
only.  The map is the deliverable: S4's blind spot is precisely
scoped (window fully characterized; S4 = the squeeze theorem on the
g-gaps between measured zeros + heights > 3.15e7 pending data +
γ < γ₀).  Constants recorded for a future `p9_c1b_disc_floor`.
