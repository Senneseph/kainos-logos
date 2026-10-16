# Action Step 21 — Projection: capabilities + planner + E3.6 (P3.12–P3.14)

> Self-contained: you need only `00-CONTEXT.md` + this file.

**Runs in Phase 3 — before directive 20 (final consolidation), see the ordering note in
`action-steps/README.md`.**

## Goal

`kainos.projection`: declared capabilities (CODEX terms with preconditions/effects),
a bounded plan search that proves a goal is reachable — or returns a first-class
**NO VALID PLAN** (named gap + nearest viable plan), interaction-type response
contracts, and a structured-creativity traversal. E3.6 runs green.

## Prerequisites

- [ ] Phases 0–2 complete (steps 01–16): `kainos.codex`, `kainos.ir`, `kainos.harness`
  work; the claim registry knows **X1/X2** (`plan/20-roadmap.md`).

## Background

Phases 1–2 contain *mini*-projections (regex pipeline = one-step plan; 20Q = identify
a hidden concept). The general layer that was missing: given a structured goal, find
a sequence of **declared** capabilities whose effects reach a satisfying state —
planning as proof, not guessing. Two invariants govern this step:

1. **P11 — capabilities are declared, not implied.** The planner may only use
   capabilities present as established CODEX assertions. No valid chain ⇒
   `NoValidPlan`, never a fabricated action.
2. **X2 — creativity is constrained.** Traversal may be stochastic (semantic
   temperature) but a branch that would violate an established fact is pruned,
   always. Novelty varies *which valid path*, never *whether a fact holds*.

Authoritative design: `plan/10-architecture/projection.md` (formula, capability
model, clarification policy, response contracts). Experiment spec:
`plan/30-phases/phase-3-generalization/experiments.md` → E3.6, ADR-0011.

**Scope guard:** all capabilities are **simulated** (preconditions/effects only, no
executable side effects). The claim under test is planning faithfulness, not tool
use.

## Steps

### 1. `src/kainos/projection/capabilities.py`

```python
@dataclass(frozen=True)
class Capability:
    name: str
    preconditions: list[str]   # fact names that must hold
    effect: list[str]          # fact names added when applied
    cost: float
    def to_assertion(self) -> "Assertion": ...   # subject=capability term,
    #   relation=has_property(preconditions/effect/cost), status=established,
    #   provenance Source(uri="capability_seed", version="1")

def seed_capabilities(codex, names: list[str]) -> None
def load_capabilities(codex) -> dict[str, Capability]
```

- Seed exactly four simulated capabilities by default:
  `SEARCH_CODEX` (pre: `[]`, effect: `[knowledge_located]`),
  `WRITE_TEXT` (pre: `[knowledge_located]`, effect: `[artifact_available]`),
  `ASK_USER` (pre: `[]`, effect: `[user_clarification]`),
  `READ_SOURCE` (pre: `[source_referenced]`, effect: `[source_content]`).
- There is deliberately **no** `GENERATE_IMAGE` capability in the seed set — the
  unachievable-goal test depends on that absence.
- Adding/removing a capability is a store operation (assertion add / status →
  `obsolete`), never a code change.

### 2. `src/kainos/projection/planner.py`

```python
@dataclass
class Plan:
    steps: list[str]                       # capability names, in order
    proof: list[dict]                      # per step: preconditions_met, facts_after

@dataclass
class NoValidPlan:
    goal: dict
    gap: str                               # unmeetable fact name (missing capability's precondition)
    nearest_prefix: list[str]              # longest valid prefix
    trace: list[dict]

def plan(goal_facts: list[str], codex, budget_depth: int = 6,
         budget_cost: float = 10.0) -> Plan | NoValidPlan
```

- State = set of satisfied fact names (start state from `goal_facts` context; the
  goal is the target set that must become satisfied).
- Bounded search (depth + cumulative cost): apply a capability only if all its
  preconditions are satisfied; add its effects.
- Accept when `goal_facts ⊆ state`. On search exhaustion: `NoValidPlan` with
  `gap` = an unmeetable precondition (one no capability can produce — pick the
  shallowest), `nearest_prefix` = the longest fully-satisfied prefix found,
  `trace` = the search (every branch tried + why rejected).
- **Property to test:** no `Plan.steps` ever names a capability absent from the
  store.

### 3. `src/kainos/projection/contract.py`

Response contracts as **data** (extendable without new code paths):

```python
CONTRACTS: dict[str, Contract]   # Contract = (required_ir_fields, validator_fn)
def response_contract(kind: str) -> Contract
def validate_response(ir: dict, kind: str) -> tuple[bool, list[str]]
```

Kinds: `request` (executed plan + result + trace), `question` (answer + evidence +
uncertainty state), `command` (action + resulting state), `assertion` (ack +
provenance + epistemic state), `correction` (superseded + replacement both
present), `impossible` (named capability gap + nearest viable plan), `ambiguous`
(clarifying question present, ≤ 2 discriminating candidates). Unknown kind → no
contract (pass-through).

### 4. `src/kainos/projection/creative.py`

```python
def traverse(goal_facts: list[str], codex, temperature: float,
             seed: int) -> list[Plan]
```

- Enumerate distinct valid plans up to a cap (e.g. 50); score each branch by
  `P ∝ strength × context_fit × novelty × constraint_fit` where `novelty` decays
  with history (same-seed repeat is less likely); `temperature = 0` ⇒ greedy
  (single strongest plan); `temperature > 0` ⇒ sample K distinct valid plans.
- **Pruning invariant:** a branch whose effect set contradicts any `established`
  polarity assertion is removed *before* selection — test this explicitly.
- Record per choice: `(branch, temperature, seed, score_inputs)` in the plan trace
  (reproducible + auditable).

### 5. E3.6 runner

`run_e3_6()` in this step (register as `e3.6` in `kainos.harness.runner.REGISTRY`),
scripted goal battery (committed in the runner, ~6–8 goals):

- achievable: `PRODUCE_REGEX` → `[knowledge_located, artifact_available]` via
  `SEARCH_CODEX → WRITE_TEXT`;
- unachievable: `PRODUCE_IMAGE` (requires fact `image_capability` — no capability
  produces it) ⇒ `NoValidPlan(gap="image_capability")` + nearest prefix + the
  "impossible" response contract holds (names the gap, offers the text-description
  nearest plan);
- ambiguous, high stakes (two plan families, high cost) ⇒ the
  search-space-aware policy picks **ask** (`ASK_USER` branch in the response);
- ambiguous, low stakes ⇒ picks **default**: a `DEFAULT(<term>)` value is applied
  and *recorded* in the trace (overridable, visible).

Write `results/phase-3/e3.6.json`: `{config, goal_achievable_validity,
honest_refusal_rate, creativity: {temperature, seed, distinct_plans},
clarification_policy: {high_stakes: "ask", low_stakes: "default"}}`.

### 6. Tests

- `tests/projection/test_capabilities.py`: seed → load round-trip; removing a
  capability (status → obsolete) changes `plan()` outcomes; provenance visible.
- `tests/projection/test_planner.py`: achievable goal → plan whose per-step preconds
  hold and effects reach the goal; unachievable → `NoValidPlan` with correct gap +
  valid prefix; property test — plans never use undeclared capabilities.
- `tests/projection/test_contracts.py`: each contract kind passes its exemplar IR
  and fails a missing-field variant.
- `tests/projection/test_creative.py`: T=0 deterministic (same seed ⇒ same plans,
  single strongest); T>0 with 3 seeds ⇒ ≥3 distinct valid plans; the pruning
  invariant (no fact-violating branch ever selected).

## Verification

```bash
pytest tests/projection -q && kainos experiment run --name e3.6 \
  && python -c "import json;d=json.load(open('results/phase-3/e3.6.json'));print(d['goal_achievable_validity'], d['honest_refusal_rate'])"
```

Expect: suite green; both rates == 1.0; creativity block shows temperature + seed.

## Done when

- [ ] capabilities are CODEX assertions (P11); no side effects anywhere
- [ ] planner returns proof or `NoValidPlan` (gap + nearest prefix + trace)
- [ ] response contracts exist for all seven kinds, validated
- [ ] creative traversal: T=0 deterministic, T>0 varied, pruning invariant holds
- [ ] E3.6: validity == 1.0, honest-refusal == 1.0, clarification policy correct
- [ ] `results/phase-3/e3.6.json` written with config (seed/commit/dataset_hash)

## If stuck

`plan/10-architecture/projection.md` (the whole design), `plan/30-phases/phase-3-generalization/experiments.md` → E3.6, `plan/03-adr.md` → ADR-0011.
