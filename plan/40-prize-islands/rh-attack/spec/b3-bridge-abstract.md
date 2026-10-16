# B-3 — ABSTRACT SPECIFICATION (what it is supposed to do, from docs/RH-PROOF-OUTLINE.md)

*Not a status report. Not an error map. The target state, written as a
mathematical specification with a Lean 4.33.1 type-compatibility ledger.
Source: outline §6 + §9 rows P6/P7, cross-checked against §3, §5, §7, §8,
§10. Lean facts pinned against the official 4.33.1 docs
(`kainos-logos/references/official-lean4-docs/`, `LEAN4-4331-QUICKREF.md`)
and the pinned mathlib source (`.lake/packages/mathlib`).*

---

## 0. What B-3 is FOR in the argument (outline §3, §6, §8)

The closure of §8 needs two inequalities about **one and the same
quantity**: the gap, at height t, between the definition side and the
zero side.

- §7 (detector, P3, proven in `B5.lean`) gives the **≥ side**: an off-line
  pair forces a change of at least f(δ, t₀)·|K|, f = |R − 1|, bounded
  below independently of δ.
- §10 (floor, P8, open) gives the **< side**: the same quantity is
  smaller than f(δ_min, t)·|K|, from the definition side alone.

**B-3 is the bridge: the statement that the two sides are NOT two
objects being compared, but one object written two ways.** Its only
disagreement term is the rigorously bounded tail of §5. Without B-3 the
≤ and ≥ sides never touch and the contradiction of §8 does not exist.

B-3 is the **ζ-free finite core** of the bridge identity (P6/P7): the
statement is about a finite height list L, a counting step, a smooth
Riemann–von Mangoldt (RVM) comparator, and the on-line pair kernel fT.
The one step that invokes ζ (ζ = K in the product sense, DLMF 25.2.12)
is the classical citation the outline assigns to B-3's classical part —
**there is no ζ in the Lean file, by design** (25.2.12 is not in Mathlib;
same no-ζ convention as B-0).

## 1. The mathematical content, theorem by theorem

Regime throughout: e ≤ G < B, 0 < t < G, x ≥ G.

### T1 — the residual split (P6 core)

For a finite height list L, a tail list T with positive "kernel values"
F, a tail model Tt, define the **bridge map** Ψ_L = exp(Tt) · ∏_{g∈L} F(g)
and the **truncated kernel** K_{L∪T} = ∏_{g∈L∪T} F(g). Then

    exp(Tt) · ∏_L F  =  ∏_{L∪T} F · exp(Tt − Σ_{g∈T} ln F(g)).

The residual of the bridge **is exactly** exp(Tt − Σ_T ln F) — the single
number measuring how well the tail model Tt approximates the logarithm of
the true tail product. No other remainder exists, term by term. This is
the abstract form of "ζ = kernel; the only disagreement is the tail
model's own error," and it is what P8 will consume: once Tt is the
§4/§5 tail model, |bridge error| is measured by |Tt − Σ_T ln F| against
the §5.2 bound — the floor must beat that, and the detector must not.

### T2 — the exact finite Abel decomposition (P7 core)

For the counting step N_L(x) = #{g ∈ L : g ≤ x} (a right-continuous
step function taking values in ℝ) and a once-differentiable f with
continuous f' on [a, b], a < b:

    ∫_a^b N_L(x) f'(x) dx  =  f(b)·N_L(b) − f(a)·N_L(a) − Σ_{g∈L, a<g≤b} f(g).

The jump at a jump point g contributes exactly f(g); the integral of the
flat pieces is the FTC (f(b)−f(c) between successive jumps). This turns
the **discrete** zero set (a finite list of heights) into an **exact
continuous** statement — the outline's "Σ-vs-∫ with the counting step"
— so that a kernel sum Σ_{g} f(γ) over the list and an integral over
heights are *provably the same object*, not approximations.

### T3 — the smooth comparator (P7)

RVM main term and its density, on (0, ∞):

    n̂(x)  = ln(x/(2π)) / (2π),
    N̂(x)  = (x/(2π)) · (ln(x/(2π)) − 1) + 7/8,   N̂' = n̂.

Both are C¹ there (n̂: C¹, N̂: C¹, N̂' = n̂ exactly). N̂ is the *smooth*
version of the integer counting function N(t): where N_L is a step
function whose jumps are the zero heights, N̂ is the deterministic
RVM-flow line whose jumps are *modelled* by the continuous density n̂.
The fluctuation of a true counting function about N̂ is exactly the
S-type quantity, bounded by the Platt–Trudgian S̄ (P5).

### T4 — the IBP bridge (P7)

For a ∈ (0, ∞):

    ∫_a^b n̂(x) f(x) dx  =  N̂(b) f(b) − N̂(a) f(a) − ∫_a^b N̂(x) f'(x) dx.

Integration by exact parts: it moves the derivative **off the
comparator** (where it is the bounded, explicit, continuous object n̂)
**onto the arbitrary f** (where only differentiability + continuity of
f' is needed). This is the calculus that lets T2 (steps, needs f') and
T3 (smooth, needs f) sit in the same identity.

### T5 — the pair-kernel machinery (P7 support, P5 engine)

The on-line pair kernel (real part of the §5.1 pair factor; the exact
closed form is P2's, proven in B4), for evaluation height t and zero
height x > t:

    fT(t, x) = ½/u(x) + ln(1 − w(t)/u(x)),   u = x²+¼, w = t²+¼.

with closed-form derivative fTp (explicit, from B4 algebra), and the
scalar bounds for x ≥ G > t:

    |fT(t,x)|  ≤ Bf(t,G)          (explicit Bf, spec §2 Lemma 1),
    |fTp(t,x)| ≤ Cf(t,G) / x³     (explicit Cf).

plus the elementary inequality −ln(1−y) ≤ y/(1−y) for 0<y<1 (itself
proven by the FTC on 1/z, where z ∈ [1−y, 1]).

### T6 — the S̄-primitives and the explicit K̄ (P5 engine, B-2's M at finite B)

The Platt–Trudgian unconditional bound (J. Number Theory **147** (2015)
842–851, Cor. 1; model copy, read from the original PDF):

    S̄(x) = 0.110·ln x + 0.290·ln ln x + 2.290,   x ≥ e.

Its three pieces have explicit antiderivatives on [e, ∞):

    P011′ = 0.110·ln x·x⁻³,   Q029′ = 0.290·ln ln x·x⁻³ − 0.290/(2 x³ ln x),
    R229′ = 2.290·x⁻³.

Hence, for e ≤ G < B,

    ∫_G^B S̄(x)·x⁻³ dx  ≤  K̄(G),

where K̄(G) is explicit in G (a combination of the three primitive values
at G; the B-side primitive values are ≤ 0 and drop out, and the last
remainder ∫ 0.290/(2x³ ln x) is capped by ∫ 0.290/(2x³) using 1/ln x ≤ 1
for x ≥ e). This is the **finite-B form** of B-2's tail integral: spec
§5 has K as ∫_G^∞; B-3 proves it at working finite B, and B → ∞ is a
documented limit step (B-6A consumes the finite form).

### T7 — the master bound (P7 crown: the finite M(G,t))

For a finite list L, 0 < t < G, e ≤ G < B, and a fluctuation hypothesis

    (H)  ∀ x ∈ [G, B],  |N_L(x) − N̂(x)| ≤ S̄(x),

(the model assumption that the counting step tracks the RVM line within
the Platt–Trudgian envelope — this IS what a true S-type fluctuation is,
and it is the one hypothesis P8's floor must eventually *lift* to the
definition side):

    | Σ_{g∈L, G<g≤B} fT(t,g)  −  ∫_G^B n̂(x) fT(t,x) dx |
        ≤  Bf(t,G)·(S̄(B) + S̄(G))  +  Cf(t,G)·K̄(G).

**This is M(G,t) of the outline at finite B.** The proof is pure
composition of T2 + T4 + T5 + T6: Abel turns Σ into ∫ of the step; IBP
turns ∫ of n̂·fT into endpoint terms + ∫ of N̂·fT′; the difference of the
two ∫'s is exactly ∫ of (N_L − N̂)·fT′ — the fluctuation against the
kernel derivative — and (H) + |fTp| ≤ Cf/x³ + T6 cap it by S̄-weighted
K̄. **Every constant in the bound is explicit.** This is the "bounded
error" of §6 for which "there is no hidden remainder."

### T8 — the A/B float layer (the cross-check gate, not part of the claim)

A pure-Float64 mirror of T1–T7's *formulas* (no ℝ, no conversion):
8-node Gauss–Legendre (composite over 8 segments, moment self-check
< 1e-12; roots/weights COMPUTED at 50 dps, never recalled), segment
splits at the toy zero heights L = [7.3, 12.1, 19.4, 27.8, 33.0],
t = 2.5, G = 6, B = 40: (1) the EXACT Abel identity T2, quadrature
error < 1e-9; (2) the T7 bound, margin > 0. Gate: both PASS, printed by
`lake exe rhattack` after E7a/B-4/B-0/B-5. P-0.9: a PASS with a flagged
anomaly is not a PASS.

## 2. The type system of B-3, and why each type is 4.33.1-compatible

*(The owner's requirement, checked against the official docs, not
assumed. "Lives" = where the API actually exists in the pinned toolchain.)*

| Choice | Where it lives (pinned) | Compatibility verdict |
|---|---|---|
| **ℝ** for all heights/values | core `Real`; mathlib analysis | ✓ The whole analysis stack in mathlib 4.33.1 is ℝ-first: `deriv`, `HasDerivAt`, `ContinuousOn`, `intervalIntegrable`, the FTC, `log`, `exp` — all state ℝ → ℝ forms with `volume` and `NullSingletonClass ℝ`. B-3 stays 1-D: height is a line; the argument's ζ-free core has no complex input (B-4/B-5 already proved the pair algebra in ℝ as la_pair/ar_pair closed forms). No `ℂ`, no `ℂ`-valued integrals — mathlib has them but they would import a second API surface for zero argument-value. |
| **List ℝ** (finite height lists) — not `Set`, not `Finset`, not `ℕ`-indexed | core `List` (tag v4.33.1, `Init/Data/List/`): `map`, `sum`, `prod`, `cons` lemmas, `mem_append*` | ✓ List has **no typeclass burden** — `List.sum`/`prod` exist for *any* `AddMonoidWithTop`/`CommMonoid`, so `(L.map (fun g => if g ≤ x then (1:ℝ) else 0)).sum` is a core-level fact needing only `AddMonoid ℝ`. `Finset ℝ` / `Set ℝ` would force `DecidableEq ℝ` (classical, available but an instance dependency) and `Set` forces choice for enumeration; the walk that produces the list is ordered, so List is the faithful image. Duplicate heights are harmless (N_L is a multiset count; the Abel sum counts multiplicities, exactly as the zero walk does). |
| **Counting values in ℝ**, not `ℕ` | ℝ-carrying `ite`: `if g ≤ x then (1:ℝ) else 0` | ✓ The Abel identity adds N_L *inside* a real integral — a `ℕ`-valued count would need a `ℕ → ℝ` coercion (exists: `Nat.cast`) at every step and would fight simp/ring in the calc chains. Writing the count directly in ℝ (documented in the def) is the zero-coercion choice; the *mathematical* fact that N_L(x) ∈ ℕ is a separate (unneeded) observation. The `if` decidable: ℝ ≤ is decidable in the file's `noncomputable section` (`Classical.propDecidable`) — standard, the same convention the file's header pins. |
| **Pointwise functions `ℝ → ℝ`** — no Pi-spaces, no normed spaces | `Pi` function type (core); mathlib calculus | ✓ All of mathlib's ℝ-calculus is stated on `ℝ → ℝ` pointwise. Vector-valued variants exist but are a different API (`HasFDerivAt`, `Continuous` on normed spaces) with no benefit here: every quantity in the bridge is scalar-in-height. |
| **HasDerivAt (pointwise) + ContinuousOn (deriv f)** as the differentiability hypothesis — *not* `ContDiffOn n` | mathlib `Analysis/Calculus/Deriv/` + FTC `MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean:1149` (`integral_eq_sub_of_hasDerivAt`) | ✓ **This is the ONLY shape that works in 4.33.1**: `HasDerivAt.contDiffOn` does not exist in the pinned version (checked in source), so the theorem statements take `(hfderiv : ∀ x ∈ Icc a b, HasDerivAt f (deriv f x) x)` + `(hf'cont : ContinuousOn (deriv f) (Icc a b))`. That pair is precisely the pointwise→ae idiom Mathlib's own FTC examples use (ContDiff.lean:34-46). No `C¹` wrapper is hidden; the two hypotheses ARE the C¹ condition, unrolled. |
| **The interval integral `∫ x in a..b, e` with implicit `∂volume`** | mathlib `MeasureTheory/Integral/IntervalIntegral/` | ✓ `NullSingletonClass ℝ` is a global instance, so `∂volume` is omitted everywhere; `integral_congr_uIoo` gives value-congruence on the open interval for free; `intervalIntegrable_of_Icc` converts ContinuousOn-on-closed to integrability. **Notation is greedy** (owner PEMDAS pin, doc-verified grammar): the body extends right across newlines — every additive-context integral is parenthesized in the Lean image, and this spec's identities T2/T4/T7 are written with that convention in mind. |
| **ite-based ray integrand** `(c ≤ x) ⟼ deriv f x` | core `ite`; `Set.EqOn.aeEq_restrict` for the a.e. bridge | ✓ The three-case ray argument is `by_cases` on `c ≤ a` / `c < b` (classical, available); the measure bridge uses exactly the mathlib idiom: pointwise equality on `Ioo` → `EqOn.aeEq_restrict` → `restrict_Ioo_eq_restrict_Ioc` → `uIoc_of_le` → `IntervalIntegrable.congr_ae` / `IntervalIntegrable.congr_uIoo`. |
| **`lift` (function transport over pointwise equality)** | built from `Eq.mp` + `congrArg` (core) | ✓ 4.33.1 has no `HasDerivAt.congr_f`; the congrArg-bridge `lift {S C} (hfe : S = C) (h : HasDerivAt S D x) : HasDerivAt C D x` is the doc-transport for the surface-shape constructors (hasDerivAt_id', HasDerivAt.comp, .mul, .add, .sub, .const_mul) whose *surface* functions (`fun z => (fun y => y) z * c`, `(h₂ ∘ h)`, …) must be bridged to the flat forms the rest of the file uses. Flat-def discipline (B-5 lesson) means every def feeding ring/nlinarith/HasDerivAt is a flat monomial, so `ext z; ring`/`field_simp` closes every bridge. |
| **Float (pure) for the A/B layer — no ℝ** | core `Float` (tag v4.33.1, `Init/Data/Float/`): opaque `@[extern]` ops incl. `Float.log`, `Float.sqrt` | ✓ Core 4.33.1 has **no** `Float ↔ ℝ` coercion (checked — this is why the A/B design is *mirror formulas*, not `↑`-lifting: any `Real.toFloat`-style bridge would be an unproven axiom and would break the gate's meaning). Float literals for the constants (π = 3.141592653589793; GL nodes/weights from the 50-dps computed table) with the documented `glMomErr` moment self-check in-file. |
| **`noncomputable section`** | core | ✓ Required for `ite g ≤ x` on ℝ (classical decidability of ℝ ≤); no `decide`/`native_decide` anywhere — nothing here is a decidable computation, everything is a theorem. |

**Consequence of the ledger:** every type in T1–T8 is a core-ℝ or
mathlib-ℝ type with the mathlib API *documented at file:line*; the only
two custom constructors are `lift` (3 lines, core `Eq.mp` + `congrArg`)
and Float mirroring (forced by the absence of a coercion). Nothing in
B-3 relies on: ℂ, Finset/Set, Nat-cast, normed spaces, ContDiffOn,
`continuity`-tactic luck, or any instance beyond `NullSingletonClass ℝ`
and `Classical.propDecidable` — all global in the pinned toolchain.

## 3. What counts as B-3 COMPLETE

1. T1–T7 stated and proven in `RhAttack/B3.lean`, in the file's header
   mapping (P6/P7 rows), with the §-numbering of §4/§5/§6 of the file
   aligning to the pieces above (T2 = b3Abel, T4 = nHatIBP, T7 =
   b3BoundExplicit, T1 = b3ResidualDecomp, T3 = NHat_deriv/continuous
   lemmas, T5–T6 = deriv + bound lemmas + Kbar_le).
2. The statements match this spec **exactly** — if a statement in the
   file has drifted from T1–T7 (extra/missing hypothesis, wrong
   endpoint convention a<g≤b, wrong regime e ≤ G), the file is wrong,
   not the spec: the owner-approved refactor license covers restoring
   spec-faithfulness.
3. `RhAttack.B3` imported by `RhAttack.lean` (the one line its header
   names); `lake build` fully green; `lake exe rhattack` gate: E7a 5/5,
   B-4 16/16, B-0, B-5 12/12, and B-3 CROSS-CHECK PASS (T8), margin > 0.
4. Outline §9 rows P6/P7 move from "in progress in Lean — no claim" to
   "Proven in Lean (`RhAttack/B3.lean`)"; the mirror is re-synced
   byte-identical.
5. P8 (the residual floor, §10) becomes the unambiguous next target:
   its input is exactly T7's RHS written at the true counting function —
   the fluctuation hypothesis (H) is the contract between B-3 and P8,
   and Route A's floor must produce a bound *below* f(δ_min, t)·|K|
   using only the definition side.

*No claim on RH is made or implied by B-3 being complete: it is the
calculus and the explicit bound, ζ-free, exactly as §6/§9 say it is.*
