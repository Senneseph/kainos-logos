"""Interaction-type response contracts as DATA (ADR-0011, P3.14).

Each interaction type has a response contract — the shape of a correct
response — declared as data (required fields + a validator), so the set
grows without new code paths (design doc: "types not listed are simply
unconstrained (no contract check) until added").

The seven kinds and what makes a response valid for them:

- ``request``    — executed plan + result + trace
- ``question``   — answer + evidence + uncertainty state
- ``command``    — action + resulting state
- ``assertion``  — acknowledgement + provenance + epistemic state
- ``correction`` — superseded + replacement, BOTH present
- ``impossible`` — named capability gap + nearest viable plan
- ``ambiguous``  — clarifying question + <= 2 discriminating candidates
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

__all__ = ["CONTRACTS", "Contract", "response_contract", "validate_response"]

Validator = Callable[[dict[str, Any]], list[str]]  # -> list of violation strings


@dataclass(frozen=True)
class Contract:
    required_fields: tuple[str, ...]
    validate: Validator


def _missing(ir: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [f"missing or empty field: {f}" for f in fields if f not in ir or ir[f] in (None, "", [], {})]


def _plain_fields(fields: tuple[str, ...]) -> Validator:
    return lambda ir: _missing(ir, fields)


def _impossible(ir: dict[str, Any]) -> list[str]:
    out = _missing(ir, ("gap", "nearest_plan"))
    if "gap" in ir and ir["gap"] and not isinstance(ir["gap"], str):
        out.append("gap must be a fact/capability name (str)")
    if "nearest_plan" in ir and ir["nearest_plan"] is not None and not isinstance(ir["nearest_plan"], list):
        out.append("nearest_plan must be a list of capability names")
    return out


def _ambiguous(ir: dict[str, Any]) -> list[str]:
    out = _missing(ir, ("clarifying_question", "candidates"))
    cands = ir.get("candidates")
    if isinstance(cands, list) and not (1 <= len(cands) <= 2):
        out.append(f"candidates must hold 1-2 discriminating candidates (got {len(cands)})")
    return out


def _correction(ir: dict[str, Any]) -> list[str]:
    out = _missing(ir, ("superseded", "replacement"))
    if (
        "superseded" in ir
        and "replacement" in ir
        and ir["superseded"]
        and ir["replacement"]
        and ir["superseded"] == ir["replacement"]
    ):
        out.append("superseded and replacement must differ (both must be retained, distinct)")
    return out


CONTRACTS: dict[str, Contract] = {
    "request": Contract(("plan", "result", "trace"), _plain_fields(("plan", "result", "trace"))),
    "question": Contract(("answer", "evidence", "uncertainty_state"), _plain_fields(("answer", "evidence", "uncertainty_state"))),
    "command": Contract(("action", "resulting_state"), _plain_fields(("action", "resulting_state"))),
    "assertion": Contract(("ack", "provenance", "epistemic_state"), _plain_fields(("ack", "provenance", "epistemic_state"))),
    "correction": Contract(("superseded", "replacement"), _correction),
    "impossible": Contract(("gap", "nearest_plan"), _impossible),
    "ambiguous": Contract(("clarifying_question", "candidates"), _ambiguous),
}


def response_contract(kind: str) -> Contract | None:
    """The contract for ``kind`` — or None (pass-through: unconstrained
    until a contract is added, by design)."""

    return CONTRACTS.get(kind)


def validate_response(ir: dict[str, Any], kind: str) -> tuple[bool, list[str]]:
    """Check a response IR against the kind's contract. Unknown kind =>
    (True, []) — no contract, no failure (the pass-through rule)."""

    contract = CONTRACTS.get(kind)
    if contract is None:
        return True, []
    violations = list(contract.validate(ir))
    return (len(violations) == 0), violations
