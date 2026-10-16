"""Perception ports and the cross-modal abstraction (E3.4, P3.09).

The unifying claim at the modality level: the same abstract CODEX
represents patterns across modalities. The cheapest HONEST demonstration is
a synthetic "vision" port: a text port and a scene port — two different
`PerceptionPort`s — both emit Semantic IRs (``kainos/ir/1``) that reduce
through the SAME abstraction step to the same abstract pattern
(``TRANSFER(object, …)``) and corroborate the same entity.

Nothing here is a neural network or a real camera; the point is the
algebra, not the pixels (the spec's own framing: "the cheapest honest
modality").
"""

from kainos.multimodal.port import (
    AbstractPattern,
    PerceptionPort,
    TextPort,
    abstract_pattern,
)
from kainos.multimodal.synthetic_vision import SyntheticVisionPort

__all__ = [
    "AbstractPattern",
    "PerceptionPort",
    "SyntheticVisionPort",
    "TextPort",
    "abstract_pattern",
]
