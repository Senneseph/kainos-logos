"""Semantic IR (P0.05) — the JSON-serializable, versioned structure every layer speaks (invariant #7).

Contract: ``specs/ir.schema.json`` (``kainos/ir/1``). The codec validates at
every boundary; the models are thin convenience constructs over the dict.
"""

from kainos.ir.codec import dump, load, validate
from kainos.ir.models import (
    Constraint,
    Entity,
    Goal,
    Hypothesis,
    Relationship,
    SemanticIR,
    UnresolvedRef,
)

__all__ = [
    "Constraint",
    "Entity",
    "Goal",
    "Hypothesis",
    "Relationship",
    "SemanticIR",
    "UnresolvedRef",
    "dump",
    "load",
    "validate",
]
