"""`PhiNumerics` — s·φ^n magnitudes (P3.03, ADR-0006, E3.5 candidate).

Every bound asserted here is the one stated in `kainos.numerics.phi`'s module
docstring; the tests pin the documented mathematics, and E3.5 measures the
consequences empirically.
"""

from __future__ import annotations

import math
import random

import pytest

from kainos.numerics.base import Numerics
from kainos.numerics.phi import (
    LOG_PHI,
    PHI,
    PhiNumerics,
    fib_normalize,
    worst_case_relative_error,
)


def test_implements_the_seam_protocol() -> None:
    assert isinstance(PhiNumerics(), Numerics)


def test_bit_budget() -> None:
    pn = PhiNumerics(exp_bits=4, mantissa_bits=3)
    # 1 sign + 4 exponent + 3 mantissa = 8 bits per value
    assert 1 + pn.exp_bits + pn.mantissa_bits == 8
    assert pn.exp_min == -7
    assert pn.exp_max == 7
    assert pn.min_magnitude == PHI ** -7
    assert pn.max_magnitude == PHI ** 8


def test_round_trip_respects_stated_bound() -> None:
    pn = PhiNumerics()
    bound = worst_case_relative_error(pn.mantissa_bits)
    assert bound == (PHI - 1.0) / 16.0
    rng = random.Random(20260820)
    for _ in range(20000):
        n = rng.randint(pn.exp_min, pn.exp_max - 1)
        m = 1.0 + rng.random() * (PHI - 1.0)
        x = m * (PHI ** n) * (1.0 if rng.random() < 0.5 else -1.0)
        rt = pn.decode(pn.encode(x))
        assert abs(rt - x) / abs(x) <= bound


def test_exact_phi_powers_round_trip_within_half_step() -> None:
    pn = PhiNumerics()
    half_step = 0.5 * pn.step
    for n in range(pn.exp_min, pn.exp_max):
        v = PHI ** n
        rt = pn.decode(pn.encode(v))
        assert rt != 0.0
        assert abs(rt - v) / v <= half_step + 1e-15


def test_zero_is_reserved_code() -> None:
    pn = PhiNumerics()
    assert pn.encode(0.0) == 0
    assert pn.decode(0) == 0.0
    # the smallest positive magnitude must NOT collide with the zero code
    c = pn.encode(pn.min_magnitude)
    assert c != 0
    assert pn.decode(pn.multiply(0, c)) == 0.0


def test_negative_zero_is_signed() -> None:
    pn = PhiNumerics()
    c = pn.encode(-phi_magnitude(pn, 2))
    assert c != pn.encode(phi_magnitude(pn, 2))
    assert pn.decode(c) < 0.0


def phi_magnitude(pn: PhiNumerics, n: int) -> float:
    return 1.35 * (PHI ** n)


def test_multiply_is_exponent_add_with_bounded_mantissa_error() -> None:
    pn = PhiNumerics()
    # two input quantizations (each <= half a mantissa step, relative to the
    # factor since mantissas are >= 1) plus one re-quantization of the product
    # mantissa: worst case 1.5 * step, relative to the product.
    bound = 1.5 * pn.step
    rng = random.Random(7)
    for _ in range(20000):
        na, nb = rng.randint(-3, 3), rng.randint(-3, 3)
        a = (1.0 + rng.random() * (PHI - 1.0)) * (PHI ** na)
        b = (1.0 + rng.random() * (PHI - 1.0)) * (PHI ** nb)
        exact = a * b
        got = pn.decode(pn.multiply(pn.encode(a), pn.encode(b)))
        assert abs(got - exact) / abs(exact) <= bound + 1e-14


def test_multiply_of_exact_powers_adds_exponents() -> None:
    pn = PhiNumerics()
    # at the EXACT level (mantissa 1.0 quantizes to the first midpoint,
    # m_q = 1 + step/2), the product must land on the summed exponent, not an
    # off-by-one level: decode / φ^(a+b) must sit in the [1, φ) mantissa band.
    for a, b in ((3, -2), (5, -4), (-6, 6), (1, 1)):
        got = pn.decode(pn.multiply(pn.encode(PHI ** a), pn.encode(PHI ** b)))
        ratio = got / (PHI ** (a + b))
        assert 1.0 - 1e-9 <= ratio < PHI, (a, b, ratio)


def test_fibonacci_identity_unit_form() -> None:
    # 1 unit at level k+2 has the mass of 1 unit at level k+1 plus 1 at level k:
    # φ^(k+2) = φ^(k+1) + φ^k
    a = fib_normalize({2: 1.0})
    b = fib_normalize({1: 1.0, 0: 1.0})
    mass_a = sum(v * (PHI ** k) for k, v in a.items())
    mass_b = sum(v * (PHI ** k) for k, v in b.items())
    assert math.isclose(mass_a, mass_b, rel_tol=1e-12)
    assert math.isclose(mass_a, PHI ** 2, rel_tol= 1e-12)


def test_normalize_preserves_mass_and_bounds_levels() -> None:
    rng = random.Random(11)
    for _ in range(200):
        digits = {k: rng.uniform(-30.0, 30.0) for k in range(-4, 8) if rng.random() < 0.8}
        before = sum(v * (PHI ** k) for k, v in digits.items())
        after = fib_normalize(digits)
        assert all(abs(v) < PHI for v in after.values())
        after_mass = sum(v * (PHI ** k) for k, v in after.items())
        assert math.isclose(before, after_mass, rel_tol=1e-9, abs_tol=1e-12)


def test_normalize_carries_signed_mass_both_directions() -> None:
    pos = fib_normalize({5: 2.5})
    neg = fib_normalize({5: -2.5})
    assert all(abs(v) < PHI for v in pos.values())
    assert all(abs(v) < PHI for v in neg.values())
    assert math.isclose(
        sum(v * (PHI ** k) for k, v in pos.items()), 2.5 * (PHI ** 5), rel_tol=1e-12
    )
    assert math.isclose(
        sum(v * (PHI ** k) for k, v in neg.items()), -2.5 * (PHI ** 5), rel_tol=1e-12
    )


def test_digits_value_fold_matches_float64_sum() -> None:
    pn = PhiNumerics()
    digits = {0: 1.2, 1: -0.4, 3: 2.2}
    normalized = pn.accumulate_digits(digits)
    folded = pn.digits_value(normalized)
    reference = 1.2 * (PHI ** 0) + (-0.4) * (PHI ** 1) + 2.2 * (PHI ** 3)
    assert math.isclose(folded, reference, rel_tol=1e-12)


def test_invalid_widths_rejected() -> None:
    with pytest.raises(ValueError):
        PhiNumerics(exp_bits=0)
    with pytest.raises(ValueError):
        PhiNumerics(mantissa_bits=0)


def test_log_phi_is_consistent() -> None:
    assert math.isclose(LOG_PHI, math.log(PHI), rel_tol=1e-15)
