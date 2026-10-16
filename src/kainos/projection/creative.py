"""Structured creativity: constrained stochastic traversal of the valid
plan space (X2, ADR-0011, P3.14).

P(next branch) ~ strength x context_fit x novelty x constraint_fit, with a
semantic ``temperature`` controlling exploration — but the HARD constraint
is absolute: **a branch whose effect set contradicts an established
negative fact is pruned before selection.** Temperature varies *which*
valid path is taken, never *whether* an established assertion holds
(P5/P6 remain absolute, novelty X2 never overrides them).

Established-negative facts arrive from the store as property assertions
``<subject> --has_property--> "<fact>=no"`` with status ``established`` —
the same property vocabulary planning reasons over, so the constraint is
data, not code (P11-adjacent: the constraint set is declared in the
CODEX).

Reproducibility: every sampled choice is recorded in the plan's trace as
``(branch, temperature, seed, score_inputs)`` — output variety is
reproducible and auditable (P9).
"""

from __future__ import annotations

import random
from typing import Any

from kainos.codex.models import EpistemicState
from kainos.codex.store import CodexStore
from kainos.projection.capabilities import load_capabilities
from kainos.projection.planner import Plan

__all__ = ["MAX_PLANS", "PRUNE_KIND", "traverse"]

MAX_PLANS = 50
PRUNE_KIND = "pruned_fact_violation"


def _established_negative_facts(codex: CodexStore) -> set[str]:
    """Facts the store marks established-NO (``<fact>=no`` rows that are not
    obsolete) — violating any of them is the pruning condition (X2)."""

    out: set[str] = set()
    for a in codex.query(relation="has_property"):
        if a.status != EpistemicState.established or not isinstance(a.object, str):
            continue
        if a.object.endswith("=no"):
            out.add(a.object.split("=", 1)[0])
    return out


def _enumerate_valid_plans(caps: dict[str, Any], goal: tuple[str, ...], start: frozenset[str], cap: int, max_depth: int, max_cost: float) -> list[list[str]]:
    """ALL distinct valid plans up to ``cap`` (deterministic order)."""

    found: list[list[str]] = []
    by_name = {c.name: c for c in caps.values()}
    order = sorted(by_name)

    def dfs(state: frozenset[str], path: list[str], cost: float) -> None:
        if len(found) >= cap:
            return
        if set(goal) <= set(state):
            found.append(list(path))
            return
        if len(path) >= max_depth or cost >= max_cost:
            return
        for name in order:
            c = by_name[name]
            if name in path or cost + c.cost > max_cost:
                continue
            if not all(p in state for p in c.preconditions):
                continue
            dfs(state | set(c.effect), path + [name], cost + c.cost)

    dfs(start, [], 0.0)
    return found


def _score_branch(path: list[str], caps: dict[str, Any], goal: frozenset[str], history: dict[tuple[str, ...], int]) -> dict[str, float]:
    """Per-branch score inputs (the auditable part of P): strength,
    context fit, novelty, constraint fit (1.0 for every surviving branch —
    pruned ones never reach scoring)."""

    strength = 1.0 / (1.0 + sum(caps[n].cost for n in path))
    progress = sum(1 for n in path if set(caps[n].effect) & set(goal))
    context_fit = progress / len(path) if path else 0.0
    novelty = 1.0 / (1.0 + history.get(tuple(path), 0))
    return {"strength": strength, "context_fit": context_fit, "novelty": novelty, "constraint_fit": 1.0}


def _replay_proof(steps: list[str], caps: dict[str, Any], start: frozenset[str]) -> Plan:
    """Rebuild a Plan with its acceptance chain (proof)."""

    proof: list[dict] = []
    s = start
    for n in steps:
        c = caps[n]
        proof.append(
            {
                "step": n,
                "preconditions_met": sorted(set(c.preconditions) & set(s)),
                "facts_added": sorted(set(c.effect) - set(s)),
                "facts_after": sorted(s | set(c.effect)),
            }
        )
        s = s | set(c.effect)
    return Plan(steps=list(steps), proof=proof, cost=sum(caps[n].cost for n in steps))


def _score_product(score: dict[str, float]) -> float:
    return score["strength"] * score["context_fit"] * score["novelty"] * score["constraint_fit"]


def traverse(
    goal_facts: list[str],
    codex: CodexStore,
    temperature: float,
    seed: int,
    k: int = 3,
    max_depth: int = 6,
    max_cost: float = 10.0,
) -> list[Plan]:
    """Traverse the valid plan space toward ``goal_facts``.

    - ``temperature == 0``: greedy — the single strongest valid plan
      (deterministic; same seed => same plan, no sampling at all).
    - ``temperature > 0``: sample up to ``k`` DISTINCT valid plans with
      probability ~ score^ (1/T) (higher temperature flattens the
      distribution toward the weak-but-valid); every choice is traced with
      ``(branch, temperature, seed, score_inputs)``.

    Pruning invariant: any partial or full plan whose accumulated effects
    include an established negative fact is removed BEFORE selection —
    recorded in the trace of every returned plan under
    ``pruned_fact_violation`` entries (empty iff nothing had to be pruned).
    """

    if temperature < 0:
        raise ValueError("temperature must be >= 0")
    caps = load_capabilities(codex)
    goal = frozenset(goal_facts)
    start: frozenset[str] = frozenset()
    negative = _established_negative_facts(codex)

    # enumerate the FULL valid space, then prune fact-violating branches
    raw = _enumerate_valid_plans(caps, tuple(sorted(goal_facts)), start, MAX_PLANS, max_depth, max_cost)
    pruned: list[tuple[tuple[str, ...], set[str]]] = []
    valid: list[tuple[str, ...]] = []
    for p in raw:
        effects: set[str] = set()
        violated: set[str] = set()
        for n in p:
            effects |= set(caps[n].effect)
            violated = effects & negative
            if violated:
                break
        if violated:
            pruned.append((tuple(p), violated))
        else:
            valid.append(tuple(p))

    if not valid:
        # No valid plan at all (or every plan violates an established fact):
        # the honest outcome is the empty set — the caller reports NoValidPlan
        # via plan(); nothing fabricated or force-fitted.
        return []

    history: dict[tuple[str, ...], int] = {}
    rng = random.Random(seed)
    chosen: list[tuple[str, ...]] = []
    trace_by_path: dict[tuple[str, ...], list[dict[str, Any]]] = {}

    def trace_for(path: tuple[str, ...]) -> list[dict[str, Any]]:
        return [
            {
                "branch": list(path),
                "temperature": temperature,
                "seed": seed,
                "score_inputs": _score_branch(list(path), caps, goal, history),
            }
        ] + (
            [
                {"kind": PRUNE_KIND, "branch": list(bp), "violated": sorted(v)}
                for bp, v in pruned
            ]
            if pruned
            else []
        )

    if temperature == 0:
        # greedy: single strongest plan — the score product, no sampling
        best: tuple[str, ...] = max(valid, key=lambda pth: _score_product(_score_branch(list(pth), caps, goal, history)))
        chosen = [best]
        for cp in chosen:
            trace_by_path[cp] = trace_for(cp)
    else:
        # sample k distinct valid plans, P ~ score^(1/T) (normalized)
        pool = list(valid)
        while len(chosen) < min(k, len(valid)) and pool:
            weights = []
            for pth in pool:
                sc = _score_branch(list(pth), caps, goal, history)
                weights.append(max(_score_product(sc), 1e-9) ** (1.0 / temperature))
            total = sum(weights)
            pick = rng.random() * total
            acc = 0.0
            idx = len(pool) - 1
            for i, w in enumerate(weights):
                acc += w
                if pick <= acc:
                    idx = i
                    break
            chosen.append(pool.pop(idx))
            history[chosen[-1]] = history.get(chosen[-1], 0) + 1
        for cp in chosen:
            trace_by_path[cp] = trace_for(cp)

    plans: list[Plan] = []
    for cp in chosen:
        plan_obj = _replay_proof(list(cp), caps, start)
        plan_obj.trace = trace_by_path[cp]  # auditable choices + pruned branches
        plans.append(plan_obj)
    return plans
