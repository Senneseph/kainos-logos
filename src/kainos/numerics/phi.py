"""PhiNumerics (P3.03, ADR-0006) — magnitudes as s·φ^n: exponent-add
multiplication and Fibonacci-carry accumulation. EXPERIMENTAL and
benchmark-gated (E3.5); never a dependency of the CODEX or the Phase 0–2
pipeline.

Representation (`exp_bits` biased exponent + `mantissa_bits` mantissa, 1 sign
bit — the total bit budget is 1 + exp_bits + mantissa_bits):

  normalize:  x = s · m · φ^n  with m ∈ [1, φ)
              (n = floor(log_φ|x|), carrying n up one while m reaches φ)
  encode:     pack (sign, n + bias, q) where q quantizes m uniformly across
              (φ − 1) steps of width Δ = (φ − 1) / 2**mantissa_bits
  decode:     (−1)^sign · (1 + q·Δ) · φ^n
  multiply:   (s_a·φ^na·ma)(s_b·φ^nb·mb) = s_a·s_b · (ma·mb) · φ^(na+nb)
              — exponent ADDITION, then one local re-normalization of the
              mantissa product (divide by φ when it reaches φ: φ^(n+1) = φ^n·φ)
  fib_normalize: the accumulation rewrite on a digit string (dict: exponent
              level -> mass) using the Fibonacci identity
              φ^(k+2) = φ^(k+1) + φ^k, i.e. carrying φ units of level k up
              into 1 unit of level k+1 until every level holds less than φ
              mass. This is the local-rewrite step of the E3.5 MAC kernel.

Round-trip tolerance (stated, tested in tests/numerics/test_phi.py):
    |decode(encode(x)) − x| / |x|  ≤  (φ − 1) / 2**(mantissa_bits + 1)
(the worst case is m = 1 with a half-step mantissa miss; the exponent is
exact, only the mantissa is quantized).
"""

from __future__ import annotations

import math
from collections.abc import Sequence

__all__ = ["LOG_PHI", "PHI", "PhiNumerics", "fib_normalize", "worst_case_relative_error"]

PHI: float = (1.0 + 5.0 ** 0.5) / 2.0
LOG_PHI: float = math.log(PHI)


def worst_case_relative_error(mantissa_bits: int) -> float:
    """The stated round-trip bound for a given mantissa width (see module
    docstring)."""

    return (PHI - 1.0) / 2.0 ** (mantissa_bits + 1)


def fib_normalize(digits: dict[int, float], max_passes: int = 512) -> dict[int, float]:
    """Fibonacci-carry normalization of a digit string (level -> mass).

    Rewrite used (the Fibonacci identity in unit form, from
    φ^(k+2) = φ^(k+1) + φ^k): φ units of level k become 1 unit of level k+1 —
    sign-aware, so signed MAC accumulators normalize in either direction.

    Each outer pass carries strictly upward; a carry landing on a level that
    was not in this pass's snapshot is picked up by the next pass, so the
    function returns when a full pass moves nothing (total mass is finite,
    mass only moves up, hence termination).
    """

    d = {k: float(v) for k, v in digits.items() if v}
    for _ in range(max_passes):
        moved = False
        for k in sorted(d):
            while d.get(k, 0.0) != 0.0 and abs(d[k]) >= PHI:
                carry = d[k] / PHI
                d[k] -= carry * PHI  # remainder stays at level k
                d[k + 1] = d.get(k + 1, 0.0) + carry
                moved = True
            if d[k] == 0.0:
                del d[k]
        if not moved:
            break
    return {k: v for k, v in d.items() if v != 0.0}


class PhiNumerics:
    """s·φ^n numerics: exponent-add multiply, Fibonacci-carry accumulation.

    The `Numerics` seam protocol (encode/decode/compare/accumulate) plus the
    two strategy extensions the E3.5 kernels use: `multiply` (exponent-add)
    and `accumulate_digits` (Fibonacci-carry accumulator over a digit string).
    """

    def __init__(self, exp_bits: int = 4, mantissa_bits: int = 3) -> None:
        if exp_bits < 1 or mantissa_bits < 1:
            raise ValueError("exp_bits and mantissa_bits must be >= 1")
        self.exp_bits = exp_bits
        self.mantissa_bits = mantissa_bits
        self.bias = (1 << (exp_bits - 1)) - 1
        # CODE 0 IS RESERVED FOR ZERO, so the stored exponent field uses
        # stored = n + bias + 1 ∈ [1, 2^exp_bits - 1] (otherwise the smallest
        # positive magnitude, (n == exp_min, q == 0, +), packs to 0 and
        # collides with the zero code).
        self.exp_min = -self.bias
        self.exp_max = (1 << exp_bits) - 2 - self.bias
        self.step = (PHI - 1.0) / 2.0 ** mantissa_bits  # Δ
        self.n_mantissa = 2.0 ** mantissa_bits
        self.max_magnitude = PHI ** (self.exp_max + 1)  # m < φ, so top level + 1
        self.min_magnitude = PHI ** self.exp_min

    # ── normalize / pack / unpack ──────────────────────────────────────────

    def _normalize(self, x: float) -> tuple[int, int, float]:
        """x -> (sign, n, m) with m ∈ [1, φ). Zero -> (0, exp_min, 0.0)."""

        if x == 0.0:
            return 0, self.exp_min, 0.0
        s = -1 if x < 0 else 1
        a = abs(x)
        n = math.floor(math.log(a) / LOG_PHI)
        m = a / (PHI ** n)
        # Tolerant bucket boundaries: exact (or float-rounding-adjacent) powers
        # of phi must snap to the canonical bucket m == 1 at level n, not sit
        # at m ~= phi one level down. The tolerance (1e-9) is many orders
        # above float ulp and far below the quantization step.
        up = PHI * (1.0 - 1e-9)
        while m >= up:  # carry up one level (φ^n·φ = φ^(n+1))
            m /= PHI
            n += 1
        # A mantissa landing a hair BELOW 1.0 (quotient rounded over the floor)
        # is left in place: it quantizes to the m == 1 quantum with ulp-level
        # error, which is exactly the canonical bucket for φ-powers.
        return s, n, m

    def _quantize_mantissa(self, m: float) -> float:
        """Quantize m ∈ [1, φ) onto MIDPOINT quanta m_q = 1 + (q + 1/2)·Δ,
        q = 0..2^mantissa_bits−1 — symmetric half-step error everywhere,
        including the top of the range (the last quantum represents the
        interval up to φ). Returns the quantum value."""

        if m <= 1.0:
            return 1.0 + 0.5 * self.step
        t = (m - 1.0) / self.step - 0.5
        q = min(max(math.floor(t + 0.5), 0), int(self.n_mantissa - 1))
        return 1.0 + (q + 0.5) * self.step

    def _pack(self, sign: int, n: int, qm: float) -> int:
        """(sign, exponent, quantized mantissa) -> packed int. Out-of-range
        exponents clamp to the range ends (the format's overflow/underflow
        behavior, counted as clamps by the benchmarks)."""

        n = min(max(n, self.exp_min), self.exp_max)
        q = 0
        if qm is not None and qm > 0:
            t = (qm - 1.0) / self.step - 0.5
            q = min(max(math.floor(t + 0.5), 0), int(self.n_mantissa - 1))
        sbit = 1 if sign < 0 else 0
        stored = n + self.bias + 1  # in [1, 2^exp_bits - 1]
        return (sbit << (self.exp_bits + self.mantissa_bits)) | (stored << self.mantissa_bits) | q

    def _unpack(self, i: int) -> tuple[int, int, float]:
        """packed int -> (sign, n, quantized mantissa value m_q)."""

        q = i & (int(self.n_mantissa) - 1)
        stored = (i >> self.mantissa_bits) & ((1 << self.exp_bits) - 1)
        sbit = i >> (self.exp_bits + self.mantissa_bits)
        return (-1 if sbit else 1), stored - self.bias - 1, 1.0 + (q + 0.5) * self.step

    # ── the Numerics seam protocol ─────────────────────────────────────────

    def encode(self, x: float) -> int:
        if x == 0.0:
            return 0  # reserved code
        s, n, m = self._normalize(x)
        return self._pack(s, n, m)

    def decode(self, i: int) -> float:
        s, n, m = self._unpack(i)
        if i == 0:
            return 0.0
        return s * m * (PHI ** n)

    def compare(self, a: float, b: float) -> int:
        return (a > b) - (a < b)

    def accumulate(self, values: Sequence[float]) -> float:
        """The protocol's faithful reduction: decode-quantized exact sum.

        (The Fibonacci-carry *strategy* is `accumulate_digits`, used by the
        kernels that have an accumulator to normalize.)"""

        return math.fsum(values)

    # ── strategy extensions (E3.5 kernels) ─────────────────────────────────

    def multiply(self, a: int, b: int) -> int:
        """(s_a·m_a·φ^na)·(s_b·m_b·φ^nb) via EXONENT ADDITION: the product's
        level is na+nb (one add), the mantissas multiply, and one local
        re-normalization (divide by φ) brings m_a·m_b ∈ [1, φ²) back into
        [1, φ). Zero codes multiply to the zero code."""

        if a == 0 or b == 0:
            return 0
        sa, na, ma = self._unpack(a)
        sb, nb, mb = self._unpack(b)
        m = ma * mb
        n = na + nb
        if m >= PHI:  # one local rewrite: φ^n·φ = φ^(n+1)
            m /= PHI
            n += 1
        return self._pack(sa * sb, n, m)

    def accumulate_digits(self, digits: dict[int, float]) -> dict[int, float]:
        """Fibonacci-carry normalization of a MAC accumulator digit string
        (level -> mass). See module docstring: the rewrite is
        φ units of level k -> 1 unit of level k+1."""

        return fib_normalize(digits)

    def digits_value(self, digits: dict[int, float]) -> float:
        """Fold a (normalized) digit string to a float: Σ_k d_k·φ^k."""

        return math.fsum(d * (PHI ** k) for k, d in digits.items())
