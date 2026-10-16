# Closure module — abstract spec (outline §8 as a formal composition)

**File:** `rh-missing-tail/formal/RhAttack/Closure.lean`
**Realizes:** outline §8 "The closure" — the conditional contradiction that
turns the P8 floor + §7 detector + §6 bridge into `D ≡ 0`, and (via the
counting lemma, P1) into RH. Nothing here counts zeros inside the proof;
the counting enters only through B0's certified-lemma interface and the
measured/pinned constants at the margin.

## 0. The statement being composed

Assume RH fails. Then (F2 four-tuples + discreteness of zero heights) there
is a **minimal** off-line pair height t₀ at distance δ₀ > 0 from the line,
with D(t₀) > 0. At t₀:

1. **≥ side (zero side).** By the bridge (§6, B3), "definition side −
   zero side" differs from the zero-side kernel change by exactly the
   tail error, bounded by M(G, t₀) (§5, B3Sbar — unconditional, P5).
   The zero-side kernel change of the moved pair at its own height is
   f(δ₀, t₀)·|K(t₀)| with f = |R(½+it₀, δ₀) − 1| (§7, B5 — exact closed
   form, P3-PROVEN).
   Hence |def − zero| ≥ f(δ₀,t₀)·|K(t₀)| − M(G,t₀).

2. **< side (definition side).** By §10 (P8Floor, Route A): the same
   |def − zero| is < f(δ₀,t₀)·|K(t₀)|, without any counting input —
   under the measurement-pinned constants (near floor 0.9975; Xval pin;
   margin ≥ 112× worst-case audit on the straddle windows).

3. **Contradiction.** f·|K| − M ≤ |def − zero| < f·|K| requires M > 0
   absorbed: with the margin hypothesis M(G,t₀) ≤ m·f·|K(t₀)| (m < 1,
   PINNED: m ≤ 1/112.6 on the audited windows) the two sides cannot hold
   simultaneously. Hence D(t₀) = 0; by minimality D ≡ 0; by the counting
   lemma (B0) `RH_of_zeroD`, RH. ∎ (conditional on the pinned margin.)

## 1. Atoms

| atom | content | status |
|---|---|---|
| C0 | Counting interface: B0 `zeroD_of_RH` / `RH_of_zeroD` / `RH_iff_Dzero`; the minimal off-line pair height exists when RH fails (discreteness: zero heights have no accumulation, classical — the smallest non-trivial zero ≈ 14.13, certified). | LEAN-PROVEN (import B0) + the discreteness fact CITED (classical, RVM) |
| C1 | Detector at the pair's OWN height: for δ₀ ≥ δ_min = 0.005, f(δ₀, t₀) = |R(½+it₀, δ₀; γ = t₀) − 1| ≥ f_pin := 0.9975 on the audited own-height window. Far-regime half (t ≥ 2γ) is LEAN-PROVEN (P8Floor A4.1: ≥ 1, hence > f_pin). The own-height (branch-locus) half: the two-variable δ → 0, t → γ limit of B5's closed form — MEASURED 0.9975–1.0201 (d4d3 audit; closed form vs direct 4-zero to 1e-16 cross-checked in the day-020 worstcase run) — PINNED; the C1b promotion is CLOSED day-023 (see the C1b row). | far: LEAN (import) · own: PINNED · C1b: closed (25i refutes the continuous reading; 25s/25t prove the discrete-grid floor; the pin stays the witness constant, 25k[4]) |
| C1b (closed day-023) | Lean proof of the own-height regime: |R(½+it, δ; γ = t) − 1| ≥ 0.9975 for 0.005 ≤ δ ≤ 0.5 and |t − γ| ≤ 10 — i.e. the δ,t two-variable minimum of |R−1| on the window, from the closed form (P3). The branch point (t = γ, δ = 0) is a removable singularity of R; the window minimum is a compactness + closed-form analysis. This is the remaining LEAN work that would remove C1's pin. | CLOSED — split record (DISCOVERY_LOG 25i/25k-25t): the CONTINUOUS 0.9975 window floor is REFUTED as stated (25i: pole-ridge — ‖R−1‖ reaches 1/γ scale off the 0.5·ℤ straddle grid; no uniform 0.9975 window floor exists). The DISCRETE straddle-grid successor (u = 0.5k, k = ±1..±24, 0 < δ ≤ 1/2, γ ≥ 707/50) is LEAN-PROVEN: `formal/RhAttack/C1b.lean` `c1b_disc_floor` / `p9_c1b_disc_floor` — ‖R(½+it,δ;γ)−1‖ ≥ min(23/1000, 1−25/γ) at t = γ+u, 17-theorem module, 0 sorry, Lean 4.33.1. The pin 0.9975 is the u = −12 corner of the same curve at its audit height (1 − 24.0458/10³, 25k[3]) and stays the witness-scale constant (25k[4] scope); the open remainder is the S4 blind-spot mathematics, not this floor. |
| C2 | ≥ side: |def − zero| ≥ f·|K| − M — composition: A0 (LHS = ζ − K), A1 (triangle: ‖W_n‖ + ‖residual‖), A2b.1 (residual factored), A4.3 (|x| ≤ Xval wire), with M = the b3BoundExplicit output. All atoms LEAN-PROVEN in P8Floor/B3 — C2 is the recorded composition (one lemma restating the chain with the M(G,t) term explicit). | LEAN-PROVEN (composition over imports) |
| C3 | < side: |def − zero| < f·|K| under the pinned constants — P8Floor A4.2 `p8_zero_decision_far` (far) / the pinned near floor 0.9975 (near, the audited window). | LEAN (far, import) · PINNED (near window) |
| C4 | Margin: M(G, t₀) ≤ m·f(δ₀,t₀)·|K(t₀)| with m := 1/112.6 — the worst-case audit constant (day-020 worstcase run, 4 candidate pairs × straddle ±12, min margin 112.6×; the M(G,t) side itself is the unconditional P5 bound). | PINNED (measurement) — the explicit margin hypothesis of the closure |
| C5 | The composition: (C0 + C1 + C4) with C2/C3 as the two sides ⇒ D(t₀) = 0 (contradiction at the minimal pair height) ⇒ D ≡ 0 (minimality) ⇒ RH (`RH_of_zeroD`). ONE theorem in the module: the contradiction step, stated with C1's f_pin and C4's m as EXPLICIT hypotheses (the pinned constants live in the day logs + P8Floor pins, not re-asserted here). | LEAN-PROVEN (arithmetic composition under explicit hypotheses — the atom of this module) |

**Honesty rule:** every docstring carries LEAN-PROVEN / CITED / PINNED.
The module's theorem is a CONDITIONAL composition (its hypotheses are the
pinned margin + the own-height detector floor); the outline §8 "∎
(conditional on §10)" is preserved verbatim in that conditionality. No
prize claim, no `theorem: riemann` naming (B0's `RH_of_zeroD` is the
counting lemma, P1 — the closed, machine-proven piece).

## 2. Module shape

- Imports: Mathlib, RhAttack.B0, RhAttack.P8Floor (which imports
  P4Limit/B3/B5), RhAttack.B3Sbar (M(G,t) names).
- Order: header (same template as P8Floor: SPEC / OUTLINE / ROLE /
  STATUS / HONEST SPLIT / CITATIONS / DISCIPLINE / COMPOSITION ROOT)
  → C0/C1 imports + pin defs (f_pin, δ_min, m_pin as defs with
  day-log attribution comments) → C1 far-regime corollary (import of
  P8Floor A4.1, restated at f_pin) → C2 (restated ≥ side chain) →
  C3 (restated < side) → C5 (the composition theorem) → C1b sketch
  (the open analysis atom, documented, not a sorry — a commented goal
  statement per the no-sorry discipline).
- One green commit per atom; C5's commit is the module's green commit.

## 3. What this module does NOT do

- It does not prove C1b (the own-height δ,t minimum of |R−1| in Lean) —
  that is the open analysis atom, kept separate and explicitly OPEN.
- It does not promote C4's margin to a universal ∀t statement — the
  margin is the audited-window pin; the Route-A ceiling (t ≈ 10⁴–2×10⁴)
  is the data-driven boundary of the instrument (outline §10 route
  decision).
- It does not evaluate ζ or the zero set anywhere in Lean — all ζ
  content enters through the CITED bridge (ζ is its own kernel, DLMF
  25.2.12) and the measured records.
- It does not decide Route A vs B — it delivers §8's closure with Route
  A's constants as explicit hypotheses.
