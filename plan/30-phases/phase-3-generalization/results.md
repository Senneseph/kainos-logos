# Phase 3 — Results (final consolidation)

> **Template — filled in by [`action-steps/20-multimodal-final.md`](../../../action-steps/20-multimodal-final.md)**
> after the full project is done. Until then this file is not evidence.

- **Date / commit:** 2026-08-21 / `4105668` (final consolidation, step 20 — project complete)

## Experiment results

| Experiment | Sub-project | Result | Adopt/Reject | Margin/variance |
|------------|-------------|--------|--------------|-----------------|
| E3.1 LLM kernel A/B | LLM kernel | **PASS** (step 17, 2026-08-20: llm 1.0 vs det 0.0 on the 12-item open set) | n/a (feature gate) | 12/12 vs 0/12 judge-verified; byte-exact 11/12; 0 fallback events |
| E3.2 Fibonacci topology | topology | **ADOPT** (step 18, 2026-08-20: recurrence beats the same-budget MLP on all 3 seeds) | adopt | mean relative RMSE improvement +6.87% (per-seed +10.1% / +5.0% / +3.3%) |
| E3.3 distributed reconciliation | exchange | **PASS** (step 19, 2026-08-21: contradiction → new context TERM on both nodes, zero averaged facts) | n/a (feature gate) | 6/6 checks: 1 new TERM `ctx:time:polar_bear` (both nodes), both values established, distinct contexts, disputed 4→0, converged identical knowledge, idempotent re-merge |
| E3.4 multi-modal abstraction (final) | multimodal | **PASS** (step 20, 2026-08-21: text and synthetic vision share one abstract TRANSFER pattern; one entity consolidated from 2 modalities) | n/a (feature gate) | cross-modal pattern match: TRANSFER(object=box) from both "John moved the box" and the box scene (modality-specific parts differ honestly: text knows the actor, vision knows the locations); entity `box` corroborated into the CODEX from text + synthetic_vision (2 modalities, per-modality provenance) |
| E3.5 φ numerics | numerics | **REJECT** (step 18, 2026-08-20: wins precision + histogram, loses the ops axis) | reject | err/op(ingest-incl) 4.50e-6 vs best base 7.60e-6 (−41%); hist L1 0.0 vs 0.070/0.540; ops/result 334.7 vs best base 161.5 (2.07×) |
| E3.6 projection (X1/X2) | projection | **PASS** (step 21, 2026-08-21: validity 1.0 + honest refusal 1.0 + creativity spread + clarification policy) | n/a (feature gate) | validity 1.0 (2/2 achievable); refusal 1.0 (gap `image_capability` named, zero fabricated steps); 4 distinct valid plans at T>0 (floor 2), T=0 deterministic; policy ask (high stakes) / default-recorded (low stakes) |
| E3.7 workspace (X3) | workspace | **PASS** (step 22, 2026-08-21: recursive query at depth 2, fork isolation, candidate-only promotion, anti-corruption negative control) | n/a (feature gate) | query accuracy 1.0 (recursion depth 2); fork isolation true; 1 candidate assertion, source=workspace_PROJECT_GAME_fork; negative control passed (in the result file); 2 append-only analyses, latest v2, hash-change flags stale derivations |

## Step-level progress (partial — final consolidation happens in step 20)

### E3.4 multi-modal + FINAL consolidation (step 20, 2026-08-21)

**P3.09 (perception ports):** `src/kainos/multimodal/port.py` +
`synthetic_vision.py` — a `PerceptionPort` is anything that turns a RAW
modality input into a Semantic IR dict (`kainos/ir/1`, validated at the
boundary): `TextPort` (declared grammar: "<actor> moved [the|a] <object>" —
it names what it can see) and `SyntheticVisionPort` (a scene = objects ×
timestamps → one `located_at` relationship per (object, timestamp), the
spec's own `box --located_at--> (x,y,z)` notation). Input outside a port's
declared grammar is rejected outright — ports do not pretend.

**The modality-blind reduction:** `abstract_pattern(ir)` runs the SAME step
on every port's IR, two declared routes into one abstract `TRANSFER`
pattern — an explicit move event (`actor --moved--> object`) or observed
motion (the same object located at A then B ≠ A). No transfer in the IR →
`None` (the honest negative, mirroring the planner's NoValidPlan).

**E3.4 official run** (`PASS e3.4: 1.0`; report `results/phase-3/e3.4.json`):
text "John moved the box" → `TRANSFER(object=box, actor=john, from=None,
to=None)`; the synthetic scene → `TRANSFER(object=box, actor=None,
from=(0.0,0.0,0.0), to=(4.0,4.0,4.0))`. **One abstract pattern recognized
across modalities** (text-compatible-with-vision = same pattern type +
object), and each modality keeps the knowledge only it has — the algebra
unifies what is shared and preserves what is specific. The shared entity
`box` is corroborated into a real CODEX store from BOTH modalities: one
candidate assertion per modality, `provenance.source` naming the modality —
**one entity consolidated from ≥2 modalities**. Threshold met.

**Results hygiene — the recurring "vanished reports" defect, root-caused
and fixed this step (owner-reported).** The reports were never deleted;
they were **overwritten in place by the test suite**: every `run_e3_x`
defaulted its output root to the CWD-relative `results/`, and experiment
classes call the bench WITHOUT the harness out_dir — so each pytest gate
re-wrote the committed official artifacts with test-time data
(`commit: unknown`, fast-sample env), and `experiment report` itself used
to crash on the phase-3 directory (its result-record heuristic also
matched full reports) leaving `SUMMARY.md` stale. Fix (all shipped in this
commit):
- `src/kainos/harness/paths.py` — `default_results_dir()` /
  `default_phase_dir(phase)` read **KAINOS_RESULTS_DIR** (unset → `results`;
  official runs byte-identical to before). Every bench + the dummy now
  resolves its default output root through this at call time — no new bench
  may use a literal `Path("results")`.
- `tests/conftest.py` — sets `KAINOS_RESULTS_DIR` to a session tmpdir, so
  **test runs can no longer touch the repo's `results/` at all**.
  Verified: the full gate (589/2) leaves `git status results/` exactly as
  pre-gate.
- `load_results` now REQUIRES `value` in a persisted result record (the
  contract always has it) — full reports can no longer be mistaken for
  result records, so `kainos experiment report` renders cleanly.
- **Standing procedure (handoff + wiki):** gate → official run (with
  KAINOS_GIT_COMMIT) → `kainos experiment report --results-dir results
  --phase N --out results/phase-N/SUMMARY.md` → commit results + SUMMARY in
  the same commit.

**Final consolidation:** `results/phase-3/SUMMARY.md` re-rendered by the
harness (7 experiments: e3.1–e3.7). All eight "full-realized" acceptance
checks and the five north-star criteria are mapped to their end-to-end
evidence below; the unifying-claim table is final.

Recorded as **ADR-0019** (cross-modal corroboration semantics: ports →
validated IRs → one modality-blind abstraction; consolidation = per-modality
provenance corroboration in the CODEX, candidates only).


### E3.7 — recursive workspace memory (step 22, 2026-08-21)

**P3.15 (containers):** `src/kainos/workspace/workspace.py` —
`WorkSpace` (id, label, `lifetime` ∈ {EPHEMERAL, SESSION, PROJECT, LONG_TERM},
parent pointer, `irs: role → Semantic-IR dict`, children). `query` is a BFS
over **every** contained IR at **every** depth — a decision stored in a
grandchild is found from the project root (string predicate = case-sensitive
substring over subject/relation/object, or a callable; rows sorted by
workspace/role/index for determinism — this is the whole point: query,
don't reprocess). `fork(new_id)` = deep copy rooted at a new id, no parent —
mutations are isolated both directions (tested). `dump`/`load` is a
byte-deterministic round-trip (how a session restarts; P12: workspaces are
JSON, they ride the existing codec).

**P3.16 (sources vs analyses):** `workspace/source.py` — `SourceRef(uri,
hash, version)` + `SourceRegistry`: analyses are **immutable + append-only**
(vN+1, never overwritten); `latest_analysis` answers "what did we conclude
last time?"; `stale_derivations(source, new_hash)` flags every analysis that
declared `derived_from <source>` when — and only when — the hash
changes. Scope guard honored: local file sources only (`hash_file` = SHA-256).

**P3.17 (promotion):** `workspace/promote.py` — `promote(root_ws, ir_role,
codex, observer)` resolves the role recursively over the tree (unique-or-
error; deviation D10) and writes the IR's relationships as **candidate**
assertions: `provenance.source = workspace_<root_id>`, `derived=True`,
deterministic id `as_promoted_ws_<root>_<role>_r<i>` → re-promotion is an
idempotent no-op (the step-19 delta-merge discipline). `lapse(ws, sink)` dumps
an expired workspace to results-class storage and never touches the CODEX.

**E3.7 script** — `PROJECT_GAME` (PROJECT) → children `WORLD` →
grandchild `TRANSPORT` (transport-decision IR) and sibling `COMBAT`
(combat-decision IR); fork/revise cycle (in the fork only: `convoy_route_a`
→ `convoy_route_b`); `promote(fork, "transport_decision", codex)`; a local
file source with two versioned analyses:

| check | outcome (official)
|---|---
| query accuracy | **1.0** — from the project root the grandchild's decision is returned (recursion depth **2**, no root-level echo); the post-revision latest decision is read from the fork's state
| fork isolation | **true** — root still returns `convoy_route_a`; the fork returns `convoy_route_b`; edits on either side never leak
| promotion | **1 assertion**, status `candidate` (not established — the phase-2 path is skipped by nothing), `source=workspace_PROJECT_GAME_fork`, `derived=True`; the original un-revised decision never reaches the CODEX
| negative control | **passed** — *in the result file*: the never-promoted combat IR yields **zero** CODEX assertions (the anti-corruption invariant, P12)
| source versioning | 2 analyses, latest **v2**, v1 immutable after v2; hash change flags both `derived_from` markers stale, same hash flags none

**Evidence:** `results/phase-3/e3.7.json` (full report — config, query
accuracy, recursion depth, fork isolation, promotion block, negative-control
flag, source versioning; flat harness record `results/e3.7.json`, value 1.0,
commit 8fb8682).

**Deviations from the directive wording (none loosens a threshold):**

- **D10 — promotion resolves roles recursively and credits the root.** The
  script promotes a role held by a GRANDCHILD through the forked root
  (`promote(fork, "transport_decision", ...)`). The role is resolved by
  deterministic BFS over the subtree (must be unique — ambiguity is a
  ValueError, never a silent merge); provenance `workspace_<id>` and assertion
  ids credit the ROOT the promotion was invoked on. "Promoted out of project
  GAME-fork" is the correct epistemic statement, not "promoted out of node
  TRANSPORT".
- **D-m7 — demo analysis timestamps pinned** (`created_at` constants), the
  D-m5 discipline: the transport would wall-clock, the demo must be
  byte-reproducible.

Recorded as **ADR-0018** (workspace promotion + query operational semantics).

### E3.6 — capability-faithful projection (step 21, 2026-08-21)

**P3.12 (capabilities):** `src/kainos/projection/capabilities.py` —
capabilities are **first-class CODEX terms** (P11): the four simulated seeds
(`SEARCH_CODEX`, `WRITE_TEXT`, `ASK_USER`, `READ_SOURCE`) are stored as
term + `preconditions`/`effect`/`cost` property assertions (established,
`capability_seed` provenance). Adding a capability = assertion add;
removing = status → `obsolete` — both exercised in tests, both change
planning outcomes without a code change. The seed set **deliberately has no
image capability** — E3.6's honest-refusal test depends on that absence.

**P3.13 (planner):** `projection/planner.py` — bounded DFS (depth + cost
bound, sorted capability order — deterministic) over the declared set. A
`Plan` carries its **acceptance chain** (per step: preconditions held at
that step + state after) — the proof IS the evidence (P9). On exhaustion:
first-class `NoValidPlan` with (1) `gap` = an unmeetable fact (one no
declared capability can produce — the shallowest), (2) `nearest_prefix` =
the longest no-repetition progress prefix found (every step
preconditions-satisfied + at least one new fact — deviation D8 bounds
"longest"; without it a no-precondition capability like `ASK_USER` makes
the prefix unbounded), (3) full `trace` of every tried step and why it
stopped. The plan-level property — **no step ever names an undeclared
capability** — is tested hypothesis-driven (120 random goal/initial pairs).

**P3.14 (contracts + creativity):** `projection/contract.py` — the seven
interaction types as DATA (`request, question, command, assertion,
correction, impossible, ambiguous`; unknown kinds pass through
unconstrained, by design). `projection/creative.py` — constrained stochastic
traversal (X2): score = strength × context_fit × novelty × constraint_fit
(cheaper stronger, goal-progress fits, novelty decays with same-seed
repeats); T=0 → single strongest plan (deterministic); T>0 → sample k
distinct valid plans with P ~ score^(1/T). **Pruning invariant:** any branch
whose accumulated effects touch an **established negative fact** (a
`<fact>=no` established assertion — the constraint set is store data, not
code) is removed before selection and recorded in every returned plan's
audit trace (`branch, temperature, seed, score_inputs` + pruned branches).

**E3.6 battery** (5 scripted goals, committed in the runner): two achievable
(regex via SEARCH_CODEX→WRITE_TEXT; source-content via READ_SOURCE from an
initial context), one unachievable (image ⇒ `NoValidPlan(gap=
"image_capability")` + nearest prefix `[ASK_USER, SEARCH_CODEX, WRITE_TEXT]`
+ valid "impossible" contract), and the two ambiguous goals (two plan
families once `FETCH_TEXT` is declared as a store operation):

| check | outcome (official)
|---|---
| goal_achievable_validity | **1.0** (both plans re-verified independently of the planner, P11-declared)
| honest_refusal_rate | **1.0** (gap correct, nearest prefix valid-progress, zero fabricated steps, impossible contract holds)
| creativity spread | **4 distinct valid plans** at T=0.5 over seeds 7/8/9 (floor 2 — both families observed), all re-verified valid, traces record T+seed; T=0 deterministic single plan (`FETCH_TEXT`)
| clarification policy | high stakes → **ask** (clarifying question + ≤2 candidates, contract holds); low stakes → **default** applied from the CODEX `has_default` assertion (`artifact_available=SEARCH_CODEX|WRITE_TEXT`), recorded in the plan trace, overridable

**Evidence:** `results/phase-3/e3.6.json` (full report; flat harness record
`results/e3.6.json`, commit be439a3).

**Deviations from the directive wording (none loosens a threshold):**

- **D8 — no capability repetition within a plan** (bounds the search; makes
  "longest valid prefix" well-defined). Recorded per skipped step in the
  trace (`repeated_capability`).
- **D9 — the clarification policy is operationalized on plan-family counts +
  a stakes flag:** "large" = ≥ 2 distinct valid plans for the goal; "high
  stakes" = the goal's declared stakes (the battery's constructed cases). The
  design doc's information-gain question selection over plan branches is
  out of scope for the simulated battery (no hidden user model to reduce);
  the selected question is the family discriminator.
- **D-m6 — low-stakes default SEMANTICS:** the default family is the
  CHOSEN plan (justified completion per the design doc: "defaults are
  applied as `X = DEFAULT(term)` values"), validated as a legal plan
  before application — not merely reported alongside the shortest plan.

Recorded as **ADR-0017** (operationalization of the clarification policy +
capability-gap semantics).

### E3.3 — distributed CODEX: exchange + reconciliation (step 19, 2026-08-21)

**P3.06 (protocol):** `src/kainos/exchange/protocol.py` +
`specs/assertion_delta.schema.json`. The exchange unit is a **semantic
transaction** — an Assertion (contract `kainos/codex/1` v1) + sender
`node_id` + ISO-8601 `timestamp` — validated at every boundary against the
JSON contract (the IR-codec boundary-check pattern; the contract is
self-contained, internal `$refs` only, house style). `merge(target, deltas)`:
- **idempotent** — a delta whose id the target already holds is a no-op
  (counted `duplicate`);
- **conflict-preserving** — same subject + relation + aspect with a
different value ⇒ the incoming assertion is stored `disputed` AND every
clashing sibling is set `disputed` with **cross-linked evidence in both
directions**; the sender's status never overrides the receiver's store
(each node derives its epistemic state from identical evidence — Principle
4); only `status`/`evidence`/`exception` are ever touched — objects and
polarities are byte-preserved (no averaging, invariant #6).

**P3.07 (reconciler):** `src/kainos/exchange/reconciler.py` — the
distributed form of the single-node E2.5 `detect_dimension`. Given a
conflicting group (same aspect, ≥2 distinct values, all live
epistemic states), it runs the plan's fixed candidate list in order
(`time, location, role, modality, context`) under an operational test:
- a **specific** dimension D *explains* the group iff **every pair of sides
  with different values carries different D values** in their context data
  (an absent key does not distinguish);
- the catch-all `context` explains iff the sides' context data differ in at
  least one key (some contextual fact separates them, un-named).

Explained ⇒ a NEW context TERM `ctx:<D>:<subject>` is created (term kind
`context`) and **declared as knowledge**
(`<subject> --declares_context--> ctx:D:subject`, established, derived,
reconciler-observed — a first-class assertion, visible to the reasoner,
the E2.5 `declares_dimension` pattern generalized), every side is
re-expressed under its own context (gains `context_term` + `dimension`) with
`exception=requires_context`, and disputed sides are **re-established** —
the contradiction is explained, not hidden. Unexplained ⇒ the group is left
`disputed` and nothing is invented (honest negative, tested).

**P3.08 (E3.3 demo):** the Phase 2 bear story, distributed. Node A (winter
arctic) consolidates two games into established `polar_bear
--has_property--> hibernates=yes` and stamps its observation context
`{time: winter}`; node B (summer) consolidates the same probe as
`hibernates=no` under `{time: summer}`. Each node exports its deltas; merge
runs in **both directions**; each node reconciles **independently**.

Threshold (pre-registered) — **all six met on both nodes**:

| check | outcome |
|-------|---------|
| ≥1 new context TERM | `ctx:time:polar_bear` on both nodes (1 distinct id) |
| both values retained `established` | `hibernates=yes` and `hibernates=no`, both established ×2 each side |
| distinct contexts | winter-side and summer-side contexts differ (time + term) |
| disputed count → 0 for the pair | 4 disputed after merge → 0 after reconcile, both nodes |
| zero averaged/blended facts | exactly the two original values exist — no third |
| **converged identical knowledge** (Principle 4, stricter than the threshold) | the two nodes' assertion sets (id, value, polarity, status, context) are byte-identical after exchange+reconcile |

Re-merging the same deltas is a no-op everywhere (idempotency verified in
the report, not assumed). Two findings from the official report:
- **Cycle-robustness is exercised, not just unit-tested:** in the
two-direction exchange each node re-receives its OWN facts via the other
node; both merge reports list those round-trip ids under `duplicates` — the
idempotent no-op fires on real traffic.
- **Convergence, not consensus:** neither node's side ever disappears or
changes value; the nodes end up with the SAME knowledge because they derive
it from the SAME evidence independently.

**Evidence:** `results/phase-3/e3.3.json` (this commit; flat mirror
`results/e3.3.json`, `results/e3.3.md`). **Verdict: PASS (feature gate)** —
the exchange + reconciliation mechanism works as designed; no adopt/reject
axis (there is no competing approach A/B'd).

**Deviations from the directive wording (none loosens a threshold):**

- **D7 — the delta contract is a self-contained MIRROR of `kainos/codex/1`,
  not a `$ref` to it.** House style is self-contained specs (internal `$refs`
  only — `codex.schema.json`, `ir.schema.json`), and RFC 3986 relative-URI
  resolution makes a naive `$ref: "kainos/codex/1"` unresolvable from the
  delta's own `$id` base. So `assertion_delta.schema.json` inlines the v1
  assertion shape verbatim with a keep-in-sync note; a codex v2 bump must
  bring `kainos/exchange/assertion-delta/2` with it (recorded in ADR-0016).
- **D-m5 — fixed exchange timestamps for reproducibility.** A transport
  would stamp wall-clock time; the demo pins two fixed ISO timestamps
  (documented constants in `run_e3_3`) so the report is byte-reproducible.
  Timestamps are opaque to merge/reconcile — a real transport changes
  nothing.
- **The operational test for "D explains both sides" is this step's
  refinement of the plan's prose** ("discovering a missing dimension"); the
  candidate list is the plan's, verbatim and in order. The test + its honest
  negative (unexplainable ⇒ stays disputed, nothing invented) are pinned in
  `tests/exchange/test_reconciler.py`.

Recorded as **ADR-0016** (merge semantics + contract coupling).

### E3.2 + E3.5 — numerics seam, topology A/B, φ A/B (step 18, 2026-08-20)

**P3.03 (seam):** `src/kainos/numerics/` — the `Numerics` protocol (encode /
decode/compare/accumulate), `FloatNumerics` as the inert default (exact float64
bit-pattern identity), `PhiNumerics` as the experimental implementation (s·φ^n,
midpoint mantissa quanta over [1,φ), exponent-add `multiply`, sign-aware
`fib_normalize` carries). Core code touches only the protocol; the
seam-neutrality regression proves E1.1 passes unchanged under the default
(`tests/numerics/test_seam_neutral.py`). Library invariants (round-trip bound
(φ−1)/2^(m+1), the Fibonacci identity φ^(k+2) = φ^(k+1) + φ^k in unit form,
mass preservation, the reserved zero code) are pinned numerically in
`tests/numerics/`.

**E3.2 — Fibonacci residual recurrence vs same-budget MLP — ADOPT.** 115 params
each (structurally asserted), 10→6→6→1 tanh MLP vs recurrence
X0 = tanh(W0 x + b0) with the SHARED map f(v) = F v + bf applied three times
under Fibonacci residuals X_{k+2} = tanh(f(X_{k+1}) + X_k), readout at X3;
y = w·x + 0.15·Σ cyclic pair interactions, 180 train / 60 test, true full-batch
GD, LR 0.2, 150 steps, seeds 7/8/9. Gradients of both arms are verified against
finite differences in the suite (max rel err < 1e-6). The pre-registered rule
(adopt iff recurrence wins all 3 seeds) is met:

| seed | MLP test RMSE | recurrence test RMSE | relative improvement |
|------|---------------|----------------------|----------------------|
| 7 | 0.7115 | 0.6396 | +10.1% |
| 8 | 0.5343 | 0.5075 | +5.0% |
| 9 | 0.3625 | 0.3507 | +3.3% |

Mean +6.87%; both arms far beat the no-learning baseline (1.99/0.96/0.91), so
the delta is a real capacity-at-equal-budget effect, not a training accident.
This CONTRADICTS the plan's honest expectation ("null or negative"); the finding
is that the shared-map recurrence's residual (linear-shortcut) topology — not
its parameter count — buys the optimization/generalization edge at equal budget.
Recorded as ADR-0015; the topology enters the architecture as an option for the
reasoner's numeric core, still behind the benchmark record.

**E3.5 — φ numerics vs FP8/INT8 at 8 bits/value — REJECT (on the ops axis).**
The plan-faithful φ MAC (exponent-add per pair, sign xor, mass-add of the exact
quantized-mantissa product from a one-time 8×8 table, Fibonacci-carry
normalization, final fold) vs E4M3-FP8 and range-calibrated INT8; 200 dot
products × 32 N(0,1) terms + a 4096-value power histogram over [φ⁻⁶, φ⁶];
MAC-loop ops counted live, ingest costs a documented fixed model (φ 6, fp8 6,
int8 3 ops/value, cold cache). Error metric: per-dot |Δy| normalized by the
shared reference scale ‖y‖₂ (documented refinement — a per-dot denominator is
unstable for near-zero 32-term dot products).

| format (8-bit) | MAC rms rel err (ref-norm) | err/op (ingest-incl) | ops/result (ingest-incl) | hist L1 |
|----------------|----------------------------|----------------------|--------------------------|---------|
| φ | **0.00186** (best) | **4.50e-6** (best) | 334.7 (worst) | **0.0** |
| FP8 E4M3 | 0.00247 | 7.60e-6 | 258.0 | 0.0698 |
| INT8 (calibrated) | 0.0707 | 3.49e-4 | **161.5** (best) | 0.5396 |

Pre-registered verdict rule (all three must hold to adopt): c1 err/op ≤ 0.9×
best base — **met** (4.50e-6 vs 7.60e-6, −41%); c2 hist L1 ≤ max base —
**met** (0.0); c3 ops/result ≤ best base — **FAILED** (334.7 vs 161.5, 2.07×).
So φ is the most PRECISE per op and the only format whose dynamic range natively
covers the power bins, but its MAC pays 3 ops per pair (sign xor + exponent add
+ mass add) plus carries and a spread digit-string fold that baselines read out
in one dequant scale. At 8 bits the local-rewrite overhead swamps the precision
edge: **reject** — the φ system stays an isolated experiment behind the numerics
seam (exactly ADR-0006's rule), recorded as ADR-0014. No threshold was moved;
the verdict is the pre-registered rule applied to measured numbers.

**Deviations from the directive wording (none loosens a threshold):**

- **D4 — error-per-op needs an error definition; the plan names the axis, the
  benchmark defines the metric.** Per-dot error is normalized by the shared
  reference-signal scale ‖y_ref‖₂ (not the per-dot |y|, which is unstable near
  zero). Pre-registered in the report `config` before the official run.
- **D5 — "same op budget" is implemented as an honest per-format ops MODEL**
  (MAC-loop ops counted live in each kernel; ingest quantization at a fixed,
  documented per-format cost; one-time LUT builds reported separately).
  Hardware op models vary; the model is stated in the report so any reviewer can
  re-derive or swap it.
- **D6 — e3.2's topology arm is the residual recurrence (the plan's "and/or"):**
  the width-schedule variant (1,1,2,3,5,8) was not run as a separate arm to keep
  the A/B tight; the recurrence arm is the stronger claim (shared map +
  Fibonacci residual), and the schedule is the natural extension recorded in the
  ADR.
- **D-m2 (step 18) — zero-code collision in the φ representation:** code 0 as
  packed (+, n = exp_min, q = 0) collided with the zero value; fixed by
  reserving code 0 and shifting the stored exponent, which costs one exponent
  level at the top (usable range [φ⁻⁷, φ⁸) instead of [φ⁻⁷, φ⁹); documented in
  `kainos.numerics.phi`. Caught by the round-trip sweep, not by the A/B.
- **D-m3 (step 18) — FP8 subnormal encode step:** the first draft divided by
  2⁻⁶×8 (=2⁻³) instead of 2⁻⁹, silently zeroing values down to ~0.0125;
  caught by the format round-trip test, fixed before the official run.

### E3.1 — LLM kernel A/B (step 17, 2026-08-20)

- **Verdict: PASS** — threshold met (`llm_accuracy >= deterministic_accuracy` on open
  phrasing): **1.0 vs 0.0**, with the CODEX/reasoner/emitter/judge identical in both
  arms (one shared `default_codex()` instance; per-item CODEX generation delta = 0).
- **Evidence:** `results/phase-3/e3.1.json` (this commit; flat mirror `results/e3.1.json`).
- **Model snapshot (pinned in the run config):** `pi-qwen-fast:latest` —
  `qwen35moe` MoE 35.5B, owner's LAN Ollama `http://192.168.1.65:11434`, native
  `/api/chat` with `think: false`, `format: "json"`, temperature 0;
  `modified_at 2026-08-20T00:57:55-04:00`.
- **Set:** `data/regex/open_phrasing.jsonl` — 12 hand-labeled idioms/synonyms OUTSIDE
  the deterministic grammar (verified: the deterministic arm fails all 12 — 10 parse
  errors, 2 escalations). Each record: `description`, hand-labeled `expected_ir` (the
  generic-IR AST), emitter-derived `expected_pcre`, hand-picked `positive`/`negative`
  judge examples. `load_open_phrasing()` self-checks every label (IR -> emit ->
  judge) at load time.
- **The kernel is the only thing that differs:** the step-17 seam —
  `describe(text, codex=<store>, kernel=<kernel>)` with a `LanguageKernel`; the
  resolver/emitter/judge path is kernel-independent (exactly invariant #2 at the
  language organ).

| Arm | Accuracy (judge-verified) | Byte-exact vs hand label |
|-----|---------------------------|--------------------------|
| LLM (`LLMKernel`, Ollama) | **1.0** — 12/12 | 0.917 — 11/12 (op_03 emitted `^[A-Za-z]{1}`, spelling-equivalent to the labeled `^[A-Za-z]`; judge PASS) |
| Deterministic (`DeterministicKernel`) | **0.0** — 0/12 (10 parse errors, 2 escalations) | 0.0 |

- Fallback events: 0 (the backend never failed in the run); the fallback path itself
  is unit-tested (`tests/lang/test_llm_kernel.py`: used/failed/absent, score marking).
- The A/B isolates the step-17 claim cleanly: the deterministic kernel — a hand-written
  grammar — cannot parse any idiom it wasn't written with; the LLM kernel, with the SAME
  dialect contract in its prompt, maps all 12 onto valid dialect ASTs that the unchanged
  CODEX pipeline then resolves/justifies exactly as before.

**Deviations from the directive wording (none loosens a threshold):**

- **D1 — pass yardstick is judge-verified PCRE correctness**, byte-equality with the
  hand label is a *secondary statistic*. Rationale: structurally equivalent ASTs can
  emit spelling-equivalent patterns (the op_03 case); the step's own E1.1 precedent is
  PCRE-level parity against an authored expectation, and both arms are held to the same
  hand-picked examples.
- **D2 — the AST prompt moved v1 (step 12) -> v2.** v1 encoded the deterministic
  grammar's vocabulary verbatim — right for the in-grammar seed corpus, wrong for this
  step's goal ("handles open phrasing the deterministic kernel cannot"). v2 keeps the
  dialect contract (types, relationships, vocabulary classes) and adds an explicit
  idiom-mapping instruction. Documented in `src/kainos/lang/llm.py` (module docstring).
- **D3 — the harness gained `Result.skipped`.** `e3.1` needs the LAN Ollama server;
  when it is unreachable the experiment reports SKIP (no pass, no false fail, exit code
  unaffected). `make bench` (which passes no OLLAMA env) therefore skips e3.1; official
  runs pass the endpoint. The skip semantics are unit-tested
  (`tests/harness/test_runner.py::test_module_main_name_and_all`).
- **D-m1 — bug fix surfaced by the new tests:** `OllamaBackend`'s native-API base
  derivation was wrong for endpoints with a trailing slash (`.../v1/` kept the `/v1`).
  Fixed (strip-trailing-slash ordering) + test
  (`test_ollama_base_derives_native_api_from_v1_url`).

## Did the unifying claim survive?

> One recurrence across numbers, topology, and knowledge representation — a
> hypothesis, not an assumption (P8). **Final** verdicts (project complete, step 20), one row per sub-project, adopt/reject + margin.

| Sub-project | Verdict (final) |
|-------------|------------------|
| topology (E3.2) | **ADOPTED** — shared-map Fibonacci residual recurrence beats the same-budget MLP on all 3 seeds (+6.87% mean test RMSE). The recurrence *hypothesis survives* at toy scale: the edge is the residual/shared-map topology at equal parameters, which is precisely the "recurrence across topology" claim. Caveat: toy task + pure-Python GD; the margin is real but small (3–10%). |
| numerics (E3.5) | **REJECTED** — φ numerics win precision-per-op (−41% vs best baseline at 8 bits) but lose the ops axis (2.07× the best baseline). The recurrence *does not transfer to numbers* at this bit budget; the φ system stays isolated behind the seam (ADR-0006/0014). The honest negative is the result. |
| LLM kernel (E3.1) | feature gate PASS (capability added; not part of the recurrence claim) |
| exchange (E3.3) | **PASS (feature gate)** — the SINGLE-NODE recurrence (contradiction → missing dimension → new TERM, E2.5) generalizes to a distributed exchange: merge preserves both sides, reconcile finds the same TERM independently on both nodes, and the nodes converge on identical knowledge with zero averaging. The recurrence *across knowledge representation* survives in its distributed form. |
| projection (E3.6) | **PASS (feature gate)** — the plan layer (X1/X2) behaves exactly as the design requires: plans are computed as PROOF over declared capabilities only (validity 1.0), unachievable goals are a first-class, inspectable NO VALID PLAN with the correct named gap (refusal 1.0), and temperature genuinely varies WHICH valid path is taken without ever violating an established fact (pruning invariant tested). No contradiction to record: the claim holds at its stated scale. |
| workspace (E3.7) | **PASS (feature gate)** — memory as recursively addressable structure (P12) holds at the scripted scale: decision found by graph query at depth 2 (no reprocessing), fork isolation exact, and the anti-corruption rule is enforced by construction AND evidence — the CODEX gains only a candidate assertion with `source=workspace_<id>`, and the never-promoted IR is provably invisible (negative control in the result file). Working memory did not become truth.
| multimodal (E3.4) | **PASS (feature gate)** — the one-algebra claim at the modality level holds at its stated (synthetic) scale: text and a scene — two different PerceptionPorts — emit validated IRs that the SAME modality-blind step reduces to the same abstract TRANSFER pattern (object=box), and the shared entity consolidates into the CODEX with per-modality provenance. Honest scope: one synthetic port, one declared grammar each — the claim is about the algebra under the ports, not about pixels. |
| **unifying claim — FINAL** | The recurrence survives where the algebra was designed for it and is honestly REJECTED where it was not (numerics): **ADOPTED** for topology (E3.2, +6.87% at equal parameters), **gates PASS** for the knowledge-representation generalizations (E2.5→E3.3, E3.6, E3.7, E3.4), **REJECTED** for φ numerics (E3.5, ops axis) — every verdict with its margin, none forced. |

## Eight acceptance checks (phase README "full-realized") — FINAL mapping

| # | Acceptance check | Evidence artifact | Status (final) |
|---|------------------|-------------------|--------|
| 1 | ≥2 modalities into the same CODEX | E3.4 + `results/phase-3/e3.4.json`: `box` consolidated from text + synthetic_vision, per-modality provenance, one abstract pattern shared | ✅ |
| 2 | Continuous learning without kernel retraining | E1.3 (teach → restart → identical behavior, frozen kernel, provenance `user_instruction/1`, `results/phase-1/e1.3.json`) + E2.3 (growth persists across restart, `results/phase-2/e2.3.json`) — both ✅ in their phases | ✅ |
| 3 | Ontology self-expansion on contradiction | E2.5 (the bear story: contradiction → missing dimension → new TERM `ctx:time:*`, never an averaged probability) reproduced DISTRIBUTED in E3.3 (both nodes invent the same TERM independently; `results/phase-3/e3.3.json`) | ✅ |
| 4 | ≥2-node sync via assertion deltas | E3.3: two-direction delta exchange over the JSON contract, idempotent merge, byte-identical converged knowledge (Principle 4), 23 tests in `tests/exchange/` | ✅ |
| 5 | Abstain/ask at the knowledge boundary | E1.4 (clarification_rate 0.7, justified_rate 1.0 on the vague set — `results/phase-1/e1.4.json`) + the Phase-2 q20 unknown-concept path (abstain-or-ask per the game loop) + E3.6's clarification policy (ask on high-stakes ambiguity, contract-validated) | ✅ |
| 6 | Inspectable trace for every conclusion | the CODEX `explain` golden tests (provenance on every assertion, A8) + every Phase-3 experiment file IS an evidence chain: E3.6 plan acceptance chains + T/seed/score traces, E3.3 per-merge reports + reconciliation, E3.7 check-by-check report incl. the negative control, E3.4 per-modality provenance | ✅ |
| 7 | Plans only over declared capabilities; unachievable → NO VALID PLAN + nearest plan (X1) | E3.6: validity 1.0 (hypothesis property over 120 random pairs pins it), honest refusal 1.0 (correct named gap, zero fabricated steps), nearest valid prefix — `results/phase-3/e3.6.json` | ✅ |
| 8 | Recursive, queryable, explicitly-promoting workspace memory (X3) | E3.7: query at depth 2, fork isolation, candidate-only promotion `source=workspace_<id>`, NEGATIVE CONTROL IN THE RESULT FILE (un-promoted → zero CODEX assertions) — `results/phase-3/e3.7.json` | ✅ |

## North-star criteria (all phases, end-to-end)

| Criterion | End-to-end evidence |
|-----------|---------------------|
| **Persistent memory** | E1.3 (teach → restart → identical, frozen kernel) → E2.3/E2.4 (concept growth survives restart; persistent across sessions) → E3.7 (workspace dump/load round-trip = a session restarting as a JSON object) + E3.3 (converged knowledge persists on both nodes) |
| **Compositionality** | Phase 1 (NL → IR → regex out of parts, E1.1–E1.3; emitter composes over learned terms) → E3.4 (different modalities compose onto one abstract pattern + one entity) → E3.6 (plans compose from declared preconditions/effects) → E3.7 (workspaces compose: parents only carry what survives abstraction) |
| **Honest uncertainty** | E1.4 (abstain 0.7 / justified 1.0) → q20 unknown-concept abstain/ask → E2.1 reported as a genuine FAIL (deviation D1, owner ruling) → E3.5 REJECTED on the ops axis (P8: a reject is a valid result) → E3.6 `NoValidPlan` with the correct named gap, zero fabricated steps → E3.7's honest negative: un-promoted content provably absent |
| **Inspectability** | A8 (provenance on every assertion) + the CODEX `explain` golden tests → every experiment JSON is an evidence chain (acceptance chains, merge/reconciliation reports, T/seed/score traces, the E3.7 negative-control flag) → the ADR ledger records every adoption/rejection with its margin |
| **Compounding (reuse stats)** | the roadmap's compounding contract, exercised: E3.1 swapped ONE kernel into the Phase-1 pipeline (resolver/emitter/judge unchanged — invariant #2); E3.3 reused Phase-2 `consolidate` as the nodes' learning; E3.6 made CODEX terms into capabilities (assertion add/remove = planning change, no code); E3.4 reused the `kainos/ir/1` codec as the modality contract; the harness registry grew 4 → 18 experiments on the SAME contract |

## The one test

**Did the system ever discover an abstraction its designer did not explicitly put in
the ontology?**

**Verdict (final): YES — at the term/dimension level, inside the designed
procedure; the honest scope statement is part of the answer.**

* The seed ontology never contained a `time`-dimension TERM for locations:
  the contradiction "polar bear hibernates / does not hibernate" forced the
  consolidation loop (E2.5, A5) to find the missing dimension `time` and
  coin the new TERM `ctx:time:*` — the bear story's values then coexist as
  established facts under distinct contexts, **never averaged**. No human
  labeled, prompted, or enumerated that term.
* E3.3 is the replication that makes it a discovery rather than a lucky
  run: two nodes with **separate, never-merged ontologies** each ran the
  same loop independently, and each invented the SAME new TERM
  (`ctx:time:polar_bear`); the exchange then converged them to byte-identical
  knowledge (Principle 4) with zero averaging (`results/phase-3/e3.3.json`).
* Scope honesty (P8): what the designers DID put in was the *procedure* —
  the candidate-dimension list and the TERM-coining rule (a designed
  search space). What the system discovered — **which** dimension resolves
  the contradiction and the concrete term naming it — lies inside that space
  but was not specified by any design artifact, prompt, or label. Invention
  of structurally new RELATION TYPES remained outside everything observed:
  the system discovered values/contexts, not new algebra.

This is the final verdict of the project (mirrored in
`../../90-appendices/research-questions.md`, Q13).

## Ledger upkeep

- [ ] `plan/20-roadmap.md` status updated
- [x] `plan/03-adr.md` updated (φ/topology adopt/reject ADRs) — ADR-0014 (φ numerics: rejected at 8 bits) + ADR-0015 (Fibonacci residual recurrence: adopted as option) added step 18
