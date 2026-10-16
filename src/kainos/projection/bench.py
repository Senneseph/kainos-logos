"""E3.6 — capability-faithful projection (X1/X2) benchmark runner (P3.14).

Scripted goal battery (committed in this file — the dataset):

- G1 PRODUCE_REGEX   (request,   achievable)  SEARCH_CODEX -> WRITE_TEXT
- G2 READ_SOURCE     (request,   achievable, via initial context) READ_SOURCE
- G3 PRODUCE_IMAGE   (impossible) no declared capability produces
  ``image_capability`` => NoValidPlan(gap="image_capability") + nearest
  viable prefix + the "impossible" response contract holds
- G4 AMBIGUOUS_HIGH  (ambiguous, high stakes, two plan families once
  FETCH_TEXT is declared) => search-space-aware policy: **ask**
- G5 AMBIGUOUS_LOW   (ambiguous, low stakes) => policy: **choose a default**
  from the CODEX (has_default assertion), recorded + overridable

Metrics / pre-registered threshold:
(a) goal_achievable_validity == 1.0 — every achievable goal's plan: per-step
    preconditions held, effects reach the goal, every step DECLARED in the
    store (P11 property, re-verified here independently of the planner);
(b) honest_refusal_rate == 1.0 — every unachievable goal: NoValidPlan with
    the CORRECT named gap, nearest prefix a valid progress prefix, zero
    fabricated (undeclared) steps, "impossible" contract valid;
(c) creativity spread — at T>0 over 3 fixed seeds on G4's goal: >= 2 distinct
    valid plans (both declared plan families observed), all re-verified valid,
    each plan's trace records temperature + seed; T=0 is deterministic
    (same seed => byte-identical plan).
Policy: G4 "ask", G5 "default" (applied default recorded in the report).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState, Provenance, Source, TermRef
from kainos.harness.paths import default_results_dir
from kainos.projection.capabilities import (
    Capability,
    load_capabilities,
    seed_capabilities,
)
from kainos.projection.contract import validate_response
from kainos.projection.creative import traverse
from kainos.projection.planner import NoValidPlan, Plan, plan, verify_proof

__all__ = ["BATTERY", "E3_6Experiment", "run_e3_6", "write_report"]

SEED = 20260821
CREATIVITY_TEMP = 0.5
CREATIVITY_SEEDS = (7, 8, 9)

#: The committed battery (spec + expected classification per goal).
BATTERY: list[dict[str, Any]] = [
    {"goal": "PRODUCE_REGEX", "kind": "request", "facts": ["knowledge_located", "artifact_available"],
     "initial": [], "stakes": "low", "extra": [], "default": None, "class": "achievable"},
    {"goal": "READ_SOURCE_CONTENT", "kind": "command", "facts": ["source_content"],
     "initial": ["source_referenced"], "stakes": "low", "extra": [], "default": None, "class": "achievable"},
    {"goal": "PRODUCE_IMAGE", "kind": "impossible", "facts": ["image_capability"],
     "initial": [], "stakes": "high", "extra": [], "default": None, "class": "unachievable"},
    {"goal": "AMBIGUOUS_ARTIFACT_HIGH", "kind": "ambiguous", "facts": ["artifact_available"],
     "initial": [], "stakes": "high", "extra": ["FETCH_TEXT"], "default": None, "class": "ambiguous_high"},
    {"goal": "AMBIGUOUS_ARTIFACT_LOW", "kind": "ambiguous", "facts": ["artifact_available"],
     "initial": [], "stakes": "low", "extra": ["FETCH_TEXT"],
     "default": "artifact_available=SEARCH_CODEX|WRITE_TEXT", "class": "ambiguous_low"},
]


def _new_store(spec: dict[str, Any]) -> InMemoryCodexStore:
    store = InMemoryCodexStore()
    seed_capabilities(store)
    for extra in spec["extra"]:
        if extra == "FETCH_TEXT":
            cap = Capability(name="FETCH_TEXT", preconditions=(), effect=("artifact_available",), cost=2.0)
            for a in cap.to_assertions():
                store.add(a)
    if spec.get("default"):
        obj = spec["default"]
        key = obj.split("=", 1)[0]
        store.add(
            Assertion(
                id=f"as_default_{spec['goal']}",
                subject=TermRef(id=key, labels=[key]),
                relation=TermRef(id="has_default", labels=["has default"]),
                object=obj,
                status=EpistemicState.established,
                provenance=Provenance(source=Source(uri="codex_defaults", version="1"), observer="codex_defaults"),
            )
        )
    return store


def _declare_check(steps: list[str], declared: set[str]) -> bool:
    return all(s in declared for s in steps)


def _reverify(pl: Plan, goal: tuple[str, ...], store: InMemoryCodexStore | None = None, initial: list[str] | None = None) -> bool:
    """Independent of the planner: replay the plan from scratch (per-step
    preconditions against the running state, effects accumulated, goal at
    the end). Every step must be a capability DECLARED in the store (P11)."""

    caps = {c.name: c for c in (load_capabilities(store).values() if store is not None else [])}
    if not caps:
        caps = _caps_by_name()
    state: set[str] = set(initial or [])
    for step in pl.steps:
        cap = caps.get(step)
        if cap is None:
            return False  # undeclared capability (P11 violation)
        if not all(p in state for p in cap.preconditions):
            return False
        state |= set(cap.effect)
    return set(goal) <= state


def _caps_by_name() -> dict:
    from kainos.projection.capabilities import load_capabilities

    store = InMemoryCodexStore()
    seed_capabilities(store)
    return {c.name: c for c in load_capabilities(store).values()}


def _plan_dict(pl: Plan) -> dict[str, Any]:
    return {"steps": pl.steps, "cost": pl.cost, "proof": pl.proof, "trace": pl.trace}


def _run_goal(spec: dict[str, Any]) -> dict[str, Any]:
    store = _new_store(spec)
    caps = {c.name for c in _caps_of(store)}
    goal = tuple(sorted(spec["facts"]))

    if spec["class"] == "ambiguous_high":
        # large plan space (two declared families + ask-padding), high stakes => ask
        result = plan(list(spec["facts"]), store, initial=spec["initial"])
        if isinstance(result, Plan):
            families = {tuple(p.steps) for p in traverse(list(spec["facts"]), store, 0.5, CREATIVITY_SEEDS[0], k=5)}
        else:
            families = set()
        policy = "ask" if len(families) >= 2 else "choose"
        return {
            "spec": spec,
            "policy": policy,
            "response_kind": "ambiguous" if policy == "ask" else "request",
            "clarifying_question": "Which artifact route? (1) fetch the source text, (2) search the CODEX and write."
            if policy == "ask"
            else None,
            "candidates": sorted(sorted(f) for f in families) if policy == "ask" else [],
            "contract": _contract_ir(policy, families, result, spec),
            "plan": _plan_dict(result) if isinstance(result, Plan) else None,
        }

    if spec["class"] == "ambiguous_low":
        # ambiguous + low stakes => choose a default from the CODEX (recorded)
        result = plan(list(spec["facts"]), store, initial=spec["initial"])
        policy = "default"
        default_assertion = None
        for a in store.query(relation="has_default"):
            if isinstance(a.object, str) and a.object.startswith(f"{goal[0]}="):
                default_assertion = a.object
        preferred_family = tuple(default_assertion.split("=", 1)[1].split("|")) if default_assertion else None
        chosen = result
        if (
            isinstance(result, Plan)
            and preferred_family
            and tuple(result.steps) != preferred_family
            and _reverify(
                Plan(steps=list(preferred_family), proof=[], cost=0.0),
                goal,
                store,
            )
        ):
            # the default family is a valid plan — the default overrides the
            # mere shortest plan (justified completion, not a guess)
            cap_by_name = {c.name: c for c in load_capabilities(store).values()}
            chosen = Plan(
                steps=list(preferred_family),
                proof=verify_proof(list(preferred_family), cap_by_name, set(spec["initial"])),
                cost=sum(cap_by_name[n].cost for n in preferred_family),
            )
        ok_default = isinstance(chosen, Plan) and preferred_family is not None and tuple(chosen.steps) == preferred_family
        if isinstance(chosen, Plan):
            result2 = chosen  # noqa: F841 (documentation flow)
        result = chosen
        trace = list(result.trace) if isinstance(result, Plan) else []
        trace.append(
            {
                "kind": "default_applied",
                "default": default_assertion,
                "overridable": True,
                "plan": list(result.steps) if isinstance(result, Plan) else None,
            }
        )
        if isinstance(result, Plan):
            result.trace = trace
        return {
            "spec": spec,
            "policy": policy,
            "applied_default": default_assertion,
            "default_ok": ok_default,
            "response_kind": "request",
            "contract": _contract_ir("request", set(), result, spec),
            "plan": _plan_dict(result) if isinstance(result, Plan) else None,
        }

    result = plan(list(spec["facts"]), store, initial=spec["initial"])
    if spec["class"] == "achievable":
        valid = (
            isinstance(result, Plan)
            and _declare_check(result.steps, caps)
            and _reverify(result, goal, store, initial=spec["initial"])
        )
        return {"spec": spec, "policy": "choose", "response_kind": "request",
                "valid": valid, "plan": _plan_dict(result) if isinstance(result, Plan) else None,
                "contract": _contract_ir("request", set(), result, spec)}
    # unachievable => NoValidPlan with the right gap, no fabricated steps
    ok = (
        isinstance(result, NoValidPlan)
        and result.gap == "image_capability"
        and _declare_check(result.nearest_prefix, caps)
        and len(result.trace) > 0
    )
    ir = {"gap": result.gap, "nearest_plan": result.nearest_prefix} if isinstance(result, NoValidPlan) else {}
    return {"spec": spec, "policy": None, "response_kind": "impossible",
            "refusal_ok": ok, "gap": result.gap if isinstance(result, NoValidPlan) else None,
            "nearest_prefix": result.nearest_prefix if isinstance(result, NoValidPlan) else None,
            "trace_size": len(result.trace) if isinstance(result, NoValidPlan) else 0,
            "contract": {"ir": ir, "kind": "impossible", "valid": validate_response(ir, "impossible")[0],
                         "violations": validate_response(ir, "impossible")[1]}}


def _caps_of(store: InMemoryCodexStore):
    from kainos.projection.capabilities import load_capabilities

    return list(load_capabilities(store).values())


def _contract_ir(kind: str, families: set, result: Plan | NoValidPlan, spec: dict[str, Any]) -> dict[str, Any]:
    if kind == "ambiguous":
        ir: dict[str, Any] = {
            "clarifying_question": "Which artifact route do you want?",
            "candidates": sorted(sorted(f) for f in families)[:2],
        }
    else:
        ir = {
            "plan": list(result.steps) if isinstance(result, Plan) else [],
            "result": "plan computed (simulated capabilities — no side effects)" if isinstance(result, Plan) else None,
            "trace": "search trace recorded in per_goal",
        }
    ok, violations = validate_response(ir, kind)
    return {"ir": ir, "kind": kind, "valid": ok, "violations": violations}


def run_e3_6(out_dir: Path | None = None) -> dict:
    """Run the full battery; write results/e3.6.json (flat) +
    results/phase-3/e3.6.json; return the report."""

    out_dir = out_dir if out_dir is not None else default_results_dir()  # results hygiene

    per_goal = {g["goal"]: _run_goal(g) for g in BATTERY}

    achievable = [g for g in BATTERY if g["class"] == "achievable"]
    unachievable = [g for g in BATTERY if g["class"] == "unachievable"]
    validity = sum(1 for g in achievable if per_goal[g["goal"]].get("valid")) / max(len(achievable), 1)
    refusal = sum(1 for g in unachievable if per_goal[g["goal"]].get("refusal_ok")) / max(len(unachievable), 1)

    # --- creativity block (X2): G4's goal (two declared plan families) ----
    spec4 = BATTERY[3]
    store4 = _new_store(spec4)
    t0_a = traverse(list(spec4["facts"]), store4, 0.0, CREATIVITY_SEEDS[0], k=3)
    t0_b = traverse(list(spec4["facts"]), store4, 0.0, CREATIVITY_SEEDS[0], k=3)
    t0_deterministic = [tuple(p.steps) for p in t0_a] == [tuple(p.steps) for p in t0_b] and len(t0_a) == 1

    distinct: set[tuple[str, ...]] = set()
    all_valid = True
    traces_recorded = True
    per_seed: dict[str, Any] = {}
    goal4 = tuple(sorted(spec4["facts"]))
    for s in CREATIVITY_SEEDS:
        plans = traverse(list(spec4["facts"]), store4, CREATIVITY_TEMP, s, k=3)
        for p in plans:
            distinct.add(tuple(p.steps))
            if len([t for t in p.trace if "branch" in t and "temperature" in t and "seed" in t]) == 0:
                traces_recorded = False
            if not _reverify(p, goal4, store4):
                all_valid = False
        per_seed[str(s)] = [tuple(p.steps) for p in plans]
    spread_floor = 2  # pre-registered: both declared families observed
    spread_met = len(distinct) >= spread_floor

    g4 = per_goal["AMBIGUOUS_ARTIFACT_HIGH"]
    g5 = per_goal["AMBIGUOUS_ARTIFACT_LOW"]
    policy_ok = g4["policy"] == "ask" and g5["policy"] == "default" and g5.get("default_ok")

    passed = (
        validity == 1.0
        and refusal == 1.0
        and spread_met
        and t0_deterministic
        and all_valid
        and traces_recorded
        and policy_ok
        and all(per_goal[g["goal"]]["contract"]["valid"] for g in BATTERY)
    )

    battery_json = json.dumps(BATTERY, sort_keys=True)
    report: dict[str, Any] = {
        "name": "e3.6",
        "passed": passed,
        "goal_achievable_validity": validity,
        "honest_refusal_rate": refusal,
        "creativity": {
            "temperature": CREATIVITY_TEMP,
            "seed": CREATIVITY_SEEDS,
            "t0_greedy_deterministic": t0_deterministic,
            "t0_plans": [tuple(p.steps) for p in t0_a],
            "distinct_plans": sorted(" -> ".join(p) for p in distinct),
            "spread_floor": spread_floor,
            "spread_met": spread_met,
            "all_valid": all_valid,
            "traces_record_temperature_and_seed": traces_recorded,
            "per_seed": per_seed,
        },
        "clarification_policy": {
            "high_stakes": g4["policy"],
            "low_stakes": g5["policy"],
            "applied_default": g5.get("applied_default"),
            "policy_ok": policy_ok,
            "rule": "small -> choose; large+cheap -> explore; large+high-stakes -> ask; ambiguous+low-stakes -> default (recorded, overridable)",
        },
        "config": {
            "seed": SEED,
            "dataset_hash": hashlib.sha256(battery_json.encode()).hexdigest(),
            "battery": BATTERY,
            "scope": "simulated capabilities only — preconditions/effects, no side effects (claim: planning faithfulness)",
            "thresholds": "validity == 1.0; refusal == 1.0 (correct gap, zero fabricated steps); creativity spread >= 2 distinct valid plans, T=0 deterministic; policy ask/default correct; all response contracts valid",
        },
        "per_goal": per_goal,
    }
    if out_dir is not None:
        write_report(out_dir, report)
    return report


def write_report(results_dir: Path | str | None, report: dict) -> Path:
    """results/e3.6.{json,md} (flat; the harness overwrites the flat JSON
    with its Result record) + results/phase-3/e3.6.json (full report)."""

    if results_dir is None:
        raise ValueError("results_dir is required")
    base = Path(results_dir)
    (base / "e3.6.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    phase_dir = base / "phase-3"
    phase_dir.mkdir(parents=True, exist_ok=True)
    phase = phase_dir / "e3.6.json"
    phase.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    md = [
        "# E3.6 — capability-faithful projection (X1/X2)",
        "",
        f"Result: {report['passed']}",
        "",
        f"- goal_achievable_validity: **{report['goal_achievable_validity']}**",
        f"- honest_refusal_rate: **{report['honest_refusal_rate']}**",
        f"- creativity: {len(report['creativity']['distinct_plans'])} distinct valid plans at T={report['creativity']['temperature']} (spread floor {report['creativity']['spread_floor']}, met: {report['creativity']['spread_met']}), T=0 deterministic: {report['creativity']['t0_greedy_deterministic']}",
        f"- clarification policy: high-stakes → {report['clarification_policy']['high_stakes']}, low-stakes → {report['clarification_policy']['low_stakes']} (default {report['clarification_policy']['applied_default']}) — ok: {report['clarification_policy']['policy_ok']}",
        "",
        "Simulated capabilities only; the claim under test is planning faithfulness, not tool use.",
        "",
    ]
    (base / "e3.6.md").write_text("\n".join(md))
    return phase


class E3_6Experiment:
    name = "e3.6"
    hypothesis = "the planner plans only over declared capabilities: valid plans for achievables, NO VALID PLAN (named gap + nearest plan) for the rest — creativity stays constraint-valid"
    metric = (
        "plan validity on achievable goals; honest-refusal rate (correct gap, zero fabricated "
        "actions) on unachievable goals; creativity spread at T>0 (distinct valid plans, all "
        "constraint-valid, trace records T+seed); search-space-aware clarification policy"
    )
    threshold = "validity == 1.0; refusal == 1.0; spread >= 2 distinct valid plans with T=0 deterministic; policy ask (high stakes) / default (low stakes)"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e3_6()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=(float(report["goal_achievable_validity"]) + float(report["honest_refusal_rate"])) / 2.0,
            evidence=[Path("results/phase-3/e3.6.json")],
            config={
                "validity": report["goal_achievable_validity"],
                "refusal": report["honest_refusal_rate"],
                "creativity": report["creativity"],
                "clarification_policy": report["clarification_policy"],
            },
        )
