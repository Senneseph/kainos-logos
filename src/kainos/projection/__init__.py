"""Capability-faithful projection (Phase 3, ADR-0011; claims X1/X2).

Response = Realize( Project( Parse(Input), Context, Knowledge,
Capabilities, Goal ) ) — this package is the Project step over a CODEX:
declared capabilities (P11: the planner may only use what the store says
exists), bounded plan search as proof, first-class NO VALID PLAN (named
gap + nearest viable plan + trace), response contracts as data, and
constrained stochastic creativity (novelty never violates established
facts). Scope guard: simulated capabilities only — no side effects.
"""

from kainos.projection.capabilities import (
    CAPABILITY_KIND,
    DEFAULT_CAPABILITIES,
    Capability,
    load_capabilities,
    obsoletize_capability,
    seed_capabilities,
)
from kainos.projection.contract import (
    CONTRACTS,
    Contract,
    response_contract,
    validate_response,
)
from kainos.projection.creative import traverse
from kainos.projection.planner import NoValidPlan, Plan, plan

__all__ = [
    "CAPABILITY_KIND",
    "CONTRACTS",
    "DEFAULT_CAPABILITIES",
    "Capability",
    "Contract",
    "NoValidPlan",
    "Plan",
    "load_capabilities",
    "obsoletize_capability",
    "plan",
    "response_contract",
    "seed_capabilities",
    "traverse",
    "validate_response",
]
