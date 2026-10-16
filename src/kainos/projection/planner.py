"""Bounded plan search over declared capabilities — planning as proof
(ADR-0011, P3.13).

A plan is a sequence ``c_1 ... c_n`` such that, starting from the initial
world state and applying each capability's effects, every ``c_i``'s
preconditions hold at its step and the terminal state satisfies the goal
(``goal_facts`` ⊆ state). The acceptance chain (per-step precondition check +
effect application) **is** the evidence artifact — it is recorded as the
plan's ``proof`` (inspectability, P9).

Invariants:

- **P11 — declared, not implied:** a step may only name a capability present
  in the store (established). If no chain reaches the goal, the result is a
  first-class :class:`NoValidPlan` — named gap + nearest viable plan + the
  full search trace — never a fabricated action.
- The search is bounded (depth + cumulative cost), tries capabilities in
  sorted name order (deterministic), and **no capability is repeated within
  a plan** (a repeating no-precondition capability would otherwise make
  "longest valid prefix" unbounded — deviation D8, results.md).

Nearest viable plan (``NoValidPlan.nearest_prefix``): the longest
no-repetition capability sequence found in the search in which every step
(1) satisfies its preconditions and (2) adds at least one new fact — the
furthest point at which the system can still do provable work toward the
goal. The "impossible" response contract reports it as-is; the refusal is
inspectable (trace), not a wall of text.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from kainos.codex.store import CodexStore
from kainos.projection.capabilities import load_capabilities

__all__ = ["NoValidPlan", "Plan", "plan", "verify_proof"]


@dataclass
class Plan:
    """A valid plan: the capability sequence + the acceptance chain that
    proves it (per step: preconditions held at that step + state after)."""

    steps: list[str] = field(default_factory=list)
    proof: list[dict] = field(default_factory=list)
    cost: float = 0.0
    #: optional audit trail (creative.py: per-choice branch/temperature/seed
    #: + score inputs + pruned fact-violating branches) — P9 inspectability
    trace: list[dict] = field(default_factory=list)

    def terminal_state(self) -> set[str]:
        return set(self.proof[-1]["facts_after"]) if self.proof else set()


@dataclass
class NoValidPlan:
    """First-class outcome: the goal is unreachable over the declared
    capability set. ``gap`` names an unmeetable fact (one no declared
    capability can produce — the shallowest, i.e. first in sorted goal
    order); ``nearest_prefix`` is the longest valid progress prefix;
    ``trace`` records every tried step and why it stopped — the refusal is
    inspectable, not a wall of text."""

    goal: dict
    gap: str
    nearest_prefix: list[str] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)
    cost: float = 0.0


def verify_proof(steps: list[str], caps: dict, start: frozenset[str] | set[str] = frozenset()) -> list[dict]:
    """Replay a capability sequence and record the acceptance chain
    (public: E3.6's independent re-verification uses this, not the planner)."""

    proof: list[dict] = []
    state: set[str] = set(start)
    for step in steps:
        cap = caps[step]
        proof.append(
            {
                "step": step,
                "preconditions_met": sorted(set(cap.preconditions) & set(state)),
                "facts_added": sorted(set(cap.effect) - set(state)),
                "facts_after": sorted(state | set(cap.effect)),
            }
        )
        state = state | set(cap.effect)
    return proof


def plan(
    goal_facts: list[str],
    codex: CodexStore,
    initial: list[str] | None = None,
    budget_depth: int = 6,
    budget_cost: float = 10.0,
) -> Plan | NoValidPlan:
    """Search for a plan from the ``initial`` world facts to a state
    satisfying ``goal_facts``. Deterministic for a given store.

    ``initial`` models the goal's context: facts already true when the plan
    starts (the directive's "start state from the goal_facts context").
    """

    caps = load_capabilities(codex)
    goal = tuple(sorted(goal_facts))
    start: frozenset[str] = frozenset(initial or ())
    by_name = {c.name: c for c in caps.values()}
    order = sorted(by_name)

    trace: list[dict] = []
    best: Plan | None = None
    best_prefix: list[str] = []

    def dfs(state: frozenset[str], path: list[str], cost: float) -> None:
        nonlocal best, best_prefix
        # every node visited by dfs is a valid progress prefix (preconditions
        # held, new fact added, no repetition — enforced below), so the
        # longest one found is the nearest viable plan on exhaustion
        if len(path) > len(best_prefix):
            best_prefix = list(path)
        if set(goal) <= set(state):
            if best is None or len(path) < len(best.steps) or (len(path) == len(best.steps) and cost < best.cost):
                best = Plan(steps=list(path), proof=verify_proof(path, by_name, start), cost=cost)
            return
        if len(path) >= budget_depth or cost >= budget_cost:
            trace.append(
                {
                    "path": list(path),
                    "state": sorted(state),
                    "outcome": "budget",
                    "reason": "depth or cumulative-cost bound",
                }
            )
            return
        for name in order:
            cap = by_name[name]
            if name in path:
                trace.append(
                    {"path": list(path), "step": name, "outcome": "repeated_capability", "reason": "no repetition (D8)"}
                )
                continue
            missing = [p for p in cap.preconditions if p not in state]
            if missing:
                trace.append({"path": list(path), "step": name, "outcome": "precondition_failed", "missing": missing})
                continue
            if cost + cap.cost > budget_cost:
                trace.append({"path": list(path), "step": name, "outcome": "budget", "reason": "cost bound"})
                continue
            added = set(cap.effect) - set(state)
            if not added:
                trace.append({"path": list(path), "step": name, "outcome": "no_new_fact", "reason": "no progress"})
                continue
            dfs(state | added, path + [name], cost + cap.cost)

    dfs(start, [], 0.0)

    if best is not None:
        return best
    unmeetable = [f for f in goal if not any(f in by_name[n].effect for n in order)]
    gap = unmeetable[0] if unmeetable else (goal[0] if goal else "unknown")
    return NoValidPlan(
        goal={"facts": sorted(goal_facts), "initial": sorted(start)},
        gap=gap,
        nearest_prefix=best_prefix,
        trace=trace,
    )
