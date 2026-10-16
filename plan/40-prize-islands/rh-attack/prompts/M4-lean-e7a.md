# PROMPT M4 — Lean E7a (formalization, the easy win)

CONTEXT.
- THE-EULER-ACTION.md §1 (E7a statement: the Euler action identity)
- scripts/rh/day006_e7a_action_identity.py + out
  (EXACT, dps-50, 5/5 PASS — the executable oracle)
- spec/formula-ledger-and-discipline.md (provenance rules).

WHY FIRST. E7a is the project's exact finite-sum identity (telescoping
action = edge action; 5 test cases dps-50 exact). It is the shortest
path to a machine-checked artifact (the owner: "a Lean proof is good,
too") and it needs no zero-side numerics.

TASK.
1. Lean toolchain (lake init in scripts/rh-lean/); port the finite
   sequences as fin n → ℚ (or ℝ): the identity statement with the
   exact same 5 (a(n), N) instances.
2. Prove the general identity (telescoping; expected to be a few
   lines over `ring`/`sums` lemmas).
3. Run the 5 instances as `#eval`-checked examples matching the
   Python oracle's outputs (recorded in a comment with the file
   path).

DONE WHEN. lake build green; 5/5 instances check out against the
recorded Python values; the statement in the .lean file quotes
FORMULAS.md §2.1 (provenance).
CONSTRAINTS. No new numbers (Lean proves the identity; the values come
from the existing certified outputs). Keep the .lean self-contained
(no network deps beyond the standard library if possible).
OUT OF SCOPE. Anything zero-side (that's the E7b line, not E7a).

---
STATUS (2026-09-10, day-011): **PHASE 1 DONE.**
- `lake build` green (Lean 4.34.0-rc2 + Mathlib via community prebuilt cache).
- `eulerAction` proven over any commutative ring (RhAttack/EulerAction.lean).
- 5/5 oracle instances cross-checked: exact-ℤ #eval layer (10/10 A-values)
  + lean float64 LHS pipeline vs dps-20 oracle, worst |diff| = 2×10⁻¹⁴
  (out_rhattack_day011.txt). Statement + provenance headers quote
  FORMULAS.md §2.1 and the oracle file, per this prompt's DONE WHEN.
- Commit: db2cae3 (+ lake-manifest.json amend). See day-011.md §1-§2
  (ground rules learned: elan-from-GitHub, Mathlib cache, non-#eval-able
  Complex, no ring axioms over Float, 4.34 class shapes, s! formats).
- **PHASE 2 DONE (2026-09-10, same day, after the repo-side deliverables).**
  B-4 on-line pair identity in Lean (RhAttack/B4.lean), Mathlib analysis:
  T1 `pairClosedForm` (exact, no exclusion, the two-zero factor collapses
  to (real signed prefactor) × (one exponential)); T2 `pairLogAbs`
  (la_pair verbatim); T3a `pairArgAngle` (ar_pair mod 2π, exact, in the
  circle type Real.Angle); T3b `pairArLedger` (ℝ form with explicit
  2πℤ multiple). `lake build` green. PART 4 float64 cross-check: 16/16
  recorded points, worst dLa = 8.5e-14, dAr = 4.4e-16 (PASS), recorded
  in out_rhattack_day011.txt. Ground rules added (day-011 §3): Coe-real
  projection mechanics (ofReal_re/im as explicit rewrites; squares over ℂ
  need pow_two before the re-projection; ascription of a sum elaborates as
  a sum of Coes), Real.Angle as the branch-cut-free carrier
  (arg_mul_coe_angle, arg_cos_add_sin_mul_I_coe_angle — unconditional
  mod 2π, Iff.mp/mpr directions, angle_eq_iff_two_pi_dvd_sub),
  exp_add_mul_I carries ℂ-typed args.
- Phase 3 (B-0 counting equivalence) — **CLOSED 2026-09-10**,
  machine-checked in `RhAttack/B0.lean`: `eqNtotMinusNon`, `nondec`,
  `offSliceEven` (off-line slice = 2-cycles under the fixed-point-free
  involution `ι(ρ)=1−ρ̄` ⇒ even), `zeroD_of_RH`/`RH_of_zeroD`, and
  `RH_iff_Dzero`. Exact computable cross-check via the `B0Model`
  namespace (`(ℚ×ℚ)` zero lists, five `#eval!`: D steps 0→2→4, all
  slices even, `D=Ntot−Non` at every height). Also this phase carries
  the READ-THE-DOCS correction of the "disabled synthesis" misreading
  (day-011 §4d).
- **day-012 (independent re-verification):** fresh `lake build` green
  (17,520 jobs, post-9620ff4 tree) + `lake exe rhattack` reproduced
  the record byte-identically — E7a 5/5 (worst 0.019664×10⁻¹²) and
  B-4 16/16 (worst dLa·1e15 = 85.265128, dAr·1e15 = 0.444089).
  Record: `scripts/rh-lean/out_rhattack_day012.txt`. Phase 2 stands
  closed and reproducible. (B-0: closed same day in the owner session —
  `RhAttack/B0.lean` committed; see §4d of day-011 and the Phase 3 note
  above.) Daily runs may build the full package.
