# Phase 3 — Actions (concrete, ordered, verifiable)

Action IDs stable (`P3.xx`). Several are gated on prior-phase completion.

---

## P3.01 — LLM kernel (behind the existing interface)

- `src/kainos/lang/llm.py` (already stubbed in P1.14): productionize `LLMKernel`
  with a configurable backend (local llama.cpp / hosted). Reuse `LanguageKernel`
  protocol exactly.
- **Verify:** `tests/lang/test_llm_kernel.py` — interface compliance + parity on
  Phase 1 seed corpus (LLM kernel ≥ deterministic on open phrasing).

## P3.02 — E3.1 A/B run

- Run LLM vs deterministic kernel on the open-phrasing set; write `results/phase-3/e3.1.json`.
- **Verify:** thresholds met; CODEX/reasoner identical in both arms.

## P3.03 — Numerics strategy seam

- `src/kainos/numerics/` with a `Numerics` protocol (strength/weight encode/decode/
  compare/accumulate). Default `FloatNumerics`. Add `PhiNumerics` as an opt-in.
- **Verify:** `tests/numerics/test_phi.py` — unit-correct φ-exponent encode/decode
  and Fibonacci normalization; core CODEX still passes with `FloatNumerics`
  (no regression).

## P3.04 — E3.5 φ benchmark (gated)

- `benchmarks/phi/` — MAC-like + histogram-of-powers kernels comparing `PhiNumerics`
  vs FP8/INT8 on error-per-op and ops-per-result.
- **Verify:** `results/phase-3/e3.5.json` reports **adopt or reject** with a margin.
  Never merged into core unless adopted.

## P3.05 — Fibonacci topology benchmark (gated)

- `benchmarks/topology/` — toy supervised task; compare `X_{n+2}=f(X_{n+1})+X_n`
  residual recurrence and/or Fibonacci width schedule vs. same-budget MLP (≥3 seeds).
- **Verify:** `results/phase-3/e3.2.json` reports adopt/reject with variance.

## P3.06 — CodexExchange protocol

- `src/kainos/exchange/protocol.py`: assertion-delta message schema; `merge()` that
  preserves conflicts (P6); `reconcile()` that detects contradictions.
- **Verify:** `tests/exchange/test_merge.py` — merge keeps both sides of a conflict;
  provenance preserved; idempotent merge.

## P3.07 — Reconciler (contradiction → missing dimension)

- `src/kainos/exchange/reconciler.py`: on `X` vs `NOT-X`, enumerate candidate
  dimensions (time/location/role/modality/context), propose a new context TERM,
  re-express both assertions.
- **Verify:** `tests/exchange/test_reconciler.py` — the bear/polar-bear example
  produces a new context TERM; both assertions `established`.

## P3.08 — E3.3 two-node demo

- Spin two `CodexStore` instances with different facts; exchange deltas; reconcile;
  write `results/phase-3/e3.3.json`.
- **Verify:** thresholds met.

## P3.09 — Multi-modal hooks

- `src/kainos/multimodal/` — `PerceptionPort` protocol: any modality emits Semantic IR.
  Ship a **synthetic vision** port (grid → features → entities/relations) for the demo.
- **Verify:** `tests/multimodal/test_synthetic_vision.py` — synthetic scene →
  entities + relationships IR; a shared `TRANSFER` pattern is produced from a
  text description *and* the synthetic scene.

## P3.10 — E3.4 multi-modal demo

- Text "John moved the box" + synthetic scene (box position change) → same
  `TRANSFER(object,A,B)` assertion; consolidate entity. Write `results/phase-3/e3.4.json`.
- **Verify:** one entity consolidated from ≥2 modalities.

## P3.11 — Final consolidation + acceptance — **runs last (after 21/22)**

- `plan/30-phases/phase-3-generalization/results.md`: E3.1–E3.7 tables, the
  "unifying claim survived?" table, and the **eight** "full-realized" acceptance
  checks each mapped to evidence.
- Update `plan/20-roadmap.md` status ledger and `plan/03-adr.md` (adopt/reject φ etc.).
- **Verify:** all eight acceptance checks have an artifact path; the north-star
  success criteria (persistent memory, compositionality, honest uncertainty,
  inspectability, compounding) each have end-to-end evidence.

## P3.12 — Capability registry (CODEX terms with preconditions/effects)

- `src/kainos/projection/capabilities.py`: `Capability` dataclass
  (`name, preconditions, input_spec, effect, cost`) + `seed_capabilities(codex)`
  that registers a small simulated set (e.g. `WRITE_TEXT`, `ASK_USER`, `SEARCH_CODEX`,
  `READ_SOURCE`) as established CODEX assertions (so capability = knowledge, P11).
- **Verify:** `tests/projection/test_capabilities.py` — registry reflects CODEX
  state; adding/removing a capability is a store operation, not a code change.

## P3.13 — Planner (bounded precondition/effect search) + NO VALID PLAN

- `src/kainos/projection/planner.py`: `plan(goal_state, capabilities, budget)` →
  `Plan(steps, proof)` or `NoValidPlan(gap, nearest_prefix, trace)`. Bounded search
  (depth + cost), every step precondition-checked against the running state.
- `src/kainos/projection/contract.py`: interaction-type **response contracts**
  (REQUEST/QUESTION/COMMAND/ASSERTION/CORRECTION + impossible + ambiguous)
  implemented as data; `validate_response(ir, contract)`.
- **Verify:** `tests/projection/test_planner.py` — achievable goal yields a plan
  whose effect chain satisfies the goal; unachievable goal yields
  `NoValidPlan` with the correct missing capability + a valid nearest prefix;
  no plan ever uses an undeclared capability (property test).

## P3.14 — E3.6 run + structured-creativity traversal (X1/X2)

- `src/kainos/projection/creative.py`: `traverse(goal, temperature, seed)` —
  P(branch) = f(strength, context fit, novelty, constraint fit, history); hard
  guard: a branch that would violate an established fact is pruned, always.
- `run_e3_6()`: goal battery (achievable / unachievable / underspecified high-stakes
  / low-stakes); metrics per E3.6 (validity, honest-refusal, spread, clarification
  policy); → `results/phase-3/e3.6.json`.
- **Verify:** E3.6 thresholds all met; trace includes temperature + seed for every
  creative choice.

## P3.15 — WORKSPACE container (recursive, lifetime-scoped, queryable)

- `src/kainos/workspace/workspace.py`: `WorkSpace(id, parent=None, lifetime, label)`
  with `add_ir`, `query(predicate)` (graph query over contained IRs), `fork()`,
  `add_child()`, `dump()/load()` (JSON — rides the IR codec). Lifetimes:
  `EPHEMERAL|SESSION|PROJECT|LONG_TERM`.
- **Verify:** `tests/workspace/test_workspace.py` — recursion ≥2 levels; a decision
  stored in a grandchild is found by a query from the project root.

## P3.16 — Promotion + source/analysis versioning (P12 discipline)

- `WorkSpace.promote(ir)` → writes the IR's relationships as **candidate**
  assertions with `provenance.source = workspace_<id>` (ordinary consolidation path
  applies afterwards); `WorkSpace.demote_lapsed()` for expired lifetimes (dump to
  results-class storage or discard — never to CODEX).
- `source.py`: source object + `ANALYSIS_vN` versioned IRs; re-analysis = new
  workspace op, never an overwrite; hash change flags `DERIVED_FROM` knowledge stale.
- **Verify:** `tests/workspace/test_promotion.py` — promoted IR appears as candidate
  with correct provenance; **un-promoted content is invisible to CODEX queries**
  (the anti-corruption negative control).

## P3.17 — E3.7 run (X3)

- `run_e3_7()`: scripted project (PROJECT_GAME → WORLD → TRANSPORT fork/revise +
  promote + two source analyses) per E3.7; → `results/phase-3/e3.7.json`.
- **Verify:** all E3.7 checks pass; the negative control is part of the result
  file, not an optional test.

---

## Ordering notes

- P3.01–P3.02 (LLM kernel) can start as soon as Phase 1 E1.5 backend is available.
- P3.03–P3.05 (φ/topology) are **isolated** and may run in parallel with anything;
  they never block the core (ADR-0006).
- P3.06–P3.08 (distributed) require the Phase 2 learning loop's reconciliation
  primitives — reuse, don't reimplement.
- P3.09–P3.10 (multi-modal) require only the generic IR + CODEX; a synthetic vision
  port keeps it cheap and testable.
- **P3.11 (final consolidation) runs last — after P3.12–P3.17.** Directives 21 and
  22 therefore execute before directive 20 despite the numbering; the runbook
  README states this exception explicitly. P3.12–P3.14 (projection) and
  P3.15–P3.17 (workspace) are independent of each other and of P3.01–P3.10;
  both require only Phase 0–2 substrate.
