"""Numerics strategy seam (P3.03, ADR-0006) — isolated, benchmark-gated.

Core code touches only the `Numerics` protocol. `FloatNumerics` is the DEFAULT:
an identity pass-through whose encode/decode are exact (float64 bit patterns),
under which the core must behave identically — proven by the seam-neutrality
regression test (`tests/numerics/test_seam_neutral.py`: E1.1 passes unchanged).

The non-default `PhiNumerics` (s·φ^n, exponent-add multiply, Fibonacci carry
normalization) is a Phase 3 experiment (E3.5). It is **never** a dependency of
the CODEX schema or the Phase 0–2 pipeline (ADR-0006): the seam exists so the
experiment can be taken in or out without touching core behavior.
"""

from __future__ import annotations

import math
import struct
from collections.abc import Sequence
from typing import Protocol, runtime_checkable

__all__ = ["FloatNumerics", "Numerics", "default_numerics"]


@runtime_checkable
class Numerics(Protocol):
    """A number system for bounded scalars, behind one seam.

    - `encode(x)`: quantize a float into this system's integer code.
    - `decode(i)`: the float represented by a code.
    - `compare(a, b)`: -1 / 0 / +1.
    - `accumulate(values)`: the protocol's reduction (a faithful sum of the
      values); kernel-specific accumulation strategies (e.g. the Fibonacci-carry
      MAC accumulator) live on concrete classes or in the benchmarks, because
      they are strategies, not part of the seam.
    """

    def encode(self, x: float) -> int: ...

    def decode(self, i: int) -> float: ...

    def compare(self, a: float, b: float) -> int: ...

    def accumulate(self, values: Sequence[float]) -> float: ...


class FloatNumerics:
    """The DEFAULT numerics: float64 identity.

    `encode` freezes the exact float64 bit pattern into an int (little-endian,
    signed) and `decode` reverses it — so `decode(encode(x)) == x` EXACTLY for
    every finite float, and a pipeline running under this class is bit-for-bit
    the pipeline it was before the seam existed.
    """

    def encode(self, x: float) -> int:
        return int.from_bytes(struct.pack("<d", float(x)), "little", signed=True)

    def decode(self, i: int) -> float:
        return struct.unpack("<d", i.to_bytes(8, "little", signed=True))[0]

    def compare(self, a: float, b: float) -> int:
        return (a > b) - (a < b)

    def accumulate(self, values: Sequence[float]) -> float:
        return math.fsum(values)


def default_numerics() -> FloatNumerics:
    """The seam's default: identity float numerics (the inert-by-default rule,
    ADR-0006). Consumers that want phi must ask for `PhiNumerics` explicitly."""

    return FloatNumerics()
