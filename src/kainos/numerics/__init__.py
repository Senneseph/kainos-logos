"""kainos.numerics — the numerics strategy seam (P3.03, ADR-0006).

`FloatNumerics` is the DEFAULT (an exact float64 identity — inert by default);
`PhiNumerics` (s·φ^n magnitudes, exponent-add multiply, Fibonacci-carry
normalization) is the Phase 3 experiment (E3.5). Core code touches only the
`Numerics` protocol; the phi system is never a dependency of the CODEX or the
Phase 0–2 pipeline (benchmark-gated, ADR-0006).
"""

from kainos.numerics.base import FloatNumerics, Numerics, default_numerics
from kainos.numerics.phi import (
    LOG_PHI,
    PHI,
    PhiNumerics,
    fib_normalize,
    worst_case_relative_error,
)

__all__ = [
    "LOG_PHI",
    "PHI",
    "FloatNumerics",
    "Numerics",
    "PhiNumerics",
    "default_numerics",
    "fib_normalize",
    "worst_case_relative_error",
]
