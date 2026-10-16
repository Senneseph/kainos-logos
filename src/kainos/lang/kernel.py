"""The LanguageKernel contract (invariant #2: text <-> IR only).

A kernel never answers in prose — it returns structured interpretations. Phase 1
implements `parse` deterministically; `propose` is empty until the step-08 reasoner
plugs in. Later kernels (neural, step 17) implement the same protocol.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

__all__ = ["Interpretation", "LanguageKernel"]


@dataclass
class Interpretation:
    """One structured reading of an input text.

    `ir` is a regex dialect Node in Phase 1 (later: a generic SemanticIR);
    `score` is 1.0 for the deterministic kernel (one reading, full score) and
    becomes a probability once a neural kernel lands; `unresolved` lists the
    surfaces the parser could not pin to a realization (for the reasoner/human).
    """

    ir: object
    score: float
    unresolved: list[str] = field(default_factory=list)


@runtime_checkable
class LanguageKernel(Protocol):
    def parse(self, text: str, context: dict | None = None) -> list[Interpretation]: ...

    def realize(self, ir: object, style: str | None = None) -> str: ...

    def propose(self, ir: object) -> list[dict]: ...
