# P8Floor (Route A) — abstract spec

*The residual floor module: the < side of the §8 contradiction. Follows the
P4Limit pattern: formal spec → online research → modular Lean draft →
documentation → one green commit per atom. Lean 4.33.1 + mathlib (f001ca3a4
pin). Honest walls: what is machine-proven vs what is cited vs what is
measurement-pinned, stated per atom.*

## 0. The required theorem (outline §10, restated for Lean)

For all t > 0 (s = ½ + it), with W_n(s) := ζ(s) − P_n(s) + I(n,s),
I(n,s) := n^{1−s}/(1−s), K_on(t) the on-line kernel value at t:

    | W_n(t) − [K_on(t) − (P_n(s) − I(n,s))] | < min_δ f(δ, t),

proved **from the definition side alone** — no zero-count at any height
enters the proof; the height bound T never appears. The RHS is the detector
scale of §7 (near the pair: ≥ 0.998·|K|; far: (t/γ)²·|K|; δ-structure from
P3/B5).

## 1. Algebraic reduction (the shape the floor must bound)

W_n − [K_on − (P_n − I)] = (ζ − P_n + I) − K_on + P_n − I = **ζ(s) − K_on(t)**.

So the LHS is exactly the P6 bridge residual |ζ − K_on| — "definition side"
and "zero side" are the same object (bridge §6), and the floor bounds that
one number.

**Honest split.** The exact equality ζ = K (infinite product sense, DLMF
25.2.12) is CLASSICAL and CITED; the finite-G residual identity
(`b3ResidualDecomp`, `RhAttack.B3`) is LEAN-PROVEN for the finite
constructions. The floor theorem below works with the finite
constructions only — no infinite product is evaluated.

## 2. Atom plan

| Atom | Content | Status source |
|------|---------|---------------|
| A0 | Finite-floor definitions: `p8_Wn (s n) := riemannZeta s - p4_P_n s + p4_I s n` (reuse P4Limit defs), `p8_Kfin (L t)` the truncated finite kernel (reuse B3 kernel primitives), and the same-object lemma `p8_same_object : p8_Wn s n - (p8_Kfin L t - (p4_P_n s - p4_I s n)) = riemannZeta s - p8_Kfin L t` (ring). | Lean (definitional + ring) |
| A1 | Triangle: `‖ζ(s) − K_L‖ ≤ ‖W_n(s)‖ + ‖K_L − (P_n − I)‖` (norm_add_le on the A0 rearrangement). | Lean |
| A2 (definition side, core) | Floor bound: `‖W_n(½+it)‖ ≤ B_n(t)` via `p4_T4_bound` + the cited W_n-equality at Re s = ½ (P4Limit L5, honest split documented), and `‖K_L − (P_n − I)‖ ≤ M(G, t)` via the P5/P6 assets (`B3Sbar`/`B3`: `b3BoundExplicit`, the K̄(G) machinery). | Lean (B-term LEAN-PROVEN via P4Limit; the Re-½ equality CITED per DLMF 25.2.8; M-term LEAN-PROVEN finite core, see B3 header) |
| A3 | δ-minimization: `min_δ f(δ, t) = f(0, t)·|K|` — the numerator of `‖R(s,δ) − 1‖` is a δ-polynomial with all positive coefficients (B5 `b5NoffIsPolynomial` LEAN-PROVEN) ⇒ the minimum over δ ≥ 0 is at δ = 0. | Lean (build on B5 assets; the polynomial-positivity argument is the new work) |
| A4 | Comparison (the floor < the detector): `B_n(t) + M(G, t) < f(0, t)·|K(t)|` **under the measurement-pinned threshold** |δ| ≥ δ_min(t) and the floor-sensitivity constants. | LEAN: the symbolic inequality under the pinned constants as hypotheses; MEASUREMENT: the constants are pinned by the day-017/019 audit (margin ≥ 14× at the pair's own height vs the local audit floor; ceiling t ≈ 10⁴–2×10⁴). |

**Honesty rule per atom** — every atom's docstring carries one of:
LEAN-PROVEN / CITED (source) / PINNED (measurement, script + day-ref).

## 3. The δ_min pin (Route A's price, stated up front)

Route A works for |δ| ≥ δ_min(t) — the floor's sensitivity threshold
(§10). δ_min is pinned by measurement (the P4Float gate), not invented:
δ_min(t) := sup of the floor's sensitivity constants from A4. The Route-B
fallback (§10) is the δ-robust escape if the pin collapses below the
measured margins.

## 4. Module shape

`formal/RhAttack/P8Floor.lean` — imports P4Limit (B_n, W_n defs,
p4_T4_bound), B3/B3Sbar (M(G,t) assets), B5 (detector R, b5Abs,
b5NoffIsPolynomial). Atoms A0→A4, one green commit each. Module header:
same-document template as P4Limit (STATUS / ROLE / THEOREMS /
CITATIONS / NUMERICS-COMPARED-NOT-PROVED / DISCIPLINE).

## 5. What this module does NOT do

- It does not prove ζ = K as an infinite product (cited, DLMF 25.2.12).
- It does not evaluate the tail product over the zero set (the M(G,t)
  bound is unconditional by construction — Platt–Trudgian S̄, P5).
- It does not decide Route A vs B: it delivers Route A with the
  measurement-pinned constants as explicit hypotheses; the day-logs carry
  the pin values.
- It does not touch the counting data (§2) — the floor is counting-free by
  construction (that is the point of §10's "definition side alone").
