"""The `Numerics` seam and its default, `FloatNumerics` (P3.03, ADR-0006).

The default must be INERT: encode/decode are exact float64 bit-pattern
round trips, so any pipeline running under `FloatNumerics` is behaviorally
identical to the pre-seam pipeline (the E1.1 regression in
`test_seam_neutral.py` is the executable proof).
"""

from __future__ import annotations

import math

from kainos.numerics import FloatNumerics, Numerics, default_numerics


def test_protocol_is_runtime_checkable() -> None:
    assert isinstance(FloatNumerics(), Numerics)
    assert isinstance(default_numerics(), Numerics)


def test_default_numerics_is_float_identity() -> None:
    n = FloatNumerics()
    # encode/decode are EXACT: float64 bit patterns round trip with no
    # tolerance whatsoever (that is what makes the seam inert by default).
    for x in (0.0, -0.0, 1.0, -1.0, math.pi, 1e-300, 1e300, 0.1, -7.25):
        assert n.decode(n.encode(x)) == x
    # the extreme bit patterns too
    for x in (float.fromhex("0x1.fffffffffffffp-1023"), float.fromhex("0x1.fffffffffffffp+1023")):
        assert n.decode(n.encode(x)) == x


def test_zero_is_its_own_exact_round_trip() -> None:
    n = FloatNumerics()
    # -0.0 must survive as -0.0 (bit pattern), not collapse to +0.0
    assert math.copysign(1.0, n.decode(n.encode(-0.0))) < 0.0
    assert n.decode(n.encode(0.0)) == 0.0


def test_compare_ordering() -> None:
    n = FloatNumerics()
    assert n.compare(1.0, 2.0) == -1
    assert n.compare(2.0, 1.0) == 1
    assert n.compare(1.5, 1.5) == 0
    assert n.compare(-1.0, -2.0) == 1


def test_accumulate_is_faithful_sum() -> None:
    n = FloatNumerics()
    vals = [0.1] * 10 + [-0.1] * 10
    assert n.accumulate(vals) == 0.0  # fsum where naive sum drifts
    assert n.accumulate([]) == 0.0


def test_encode_bit_pattern_is_little_endian_int() -> None:
    n = FloatNumerics()
    one = n.encode(1.0)
    # float64 1.0 = 0x3FF0000000000000
    assert one == 0x3FF0000000000000


def test_protocol_rejects_non_conforming_objects() -> None:
    class NotNumerics:
        def encode(self, x: float) -> int:  # missing the rest of the protocol
            return 0

    # runtime_checkable protocols check method presence: a partial class is
    # simply NOT an instance (no error, honest False)
    assert not isinstance(NotNumerics(), Numerics)
