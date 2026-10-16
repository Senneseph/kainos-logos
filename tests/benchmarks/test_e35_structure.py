"""E3.5 benchmark structure (benchmarks/phi/bench.py): format semantics
(round-trips, ranges), the verdict machinery, and fast-size hermetic runs."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "benchmarks"))

from phi.bench import Fp8E4M3, Int8Calibrated, run_e3_5

from kainos.numerics.phi import PHI, PhiNumerics


def test_fp8_e4m3_round_trips_and_bounded_range() -> None:
    # normals: relative quantization error <= half a mantissa step (2^-4)
    for x in (1.0, -1.0, 0.5, 448.0, -448.0, 2.0**-6, 100.0, -0.01, 7.25, 2.0**8):
        rt = Fp8E4M3.decode(Fp8E4M3.encode(x))
        assert abs(rt - x) / abs(x) <= 0.125 + 1e-9, (x, rt)
    # subnormals: absolute error <= one subnormal step (2^-9), possibly to zero
    for x in (1e-3, -1e-3, 2.0**-9, 3.0 * 2.0**-9):
        rt = Fp8E4M3.decode(Fp8E4M3.encode(x))
        assert abs(rt - x) <= 2.0**-9 + 1e-12, (x, rt)
    # overflow clamps, never raises
    assert Fp8E4M3.decode(Fp8E4M3.encode(1e6)) == 448.0
    assert Fp8E4M3.decode(Fp8E4M3.encode(-1e6)) == -448.0
    assert Fp8E4M3.encode(0.0) == 0


def test_int8_calibration_round_trips() -> None:
    q = Int8Calibrated(range_max=4.0)
    for x in (0.0, 1.0, -1.0, 4.0, -4.0, 0.123):
        rt = q.decode(q.encode(x))
        assert abs(rt - x) <= 4.0 / 127.0 + 1e-12, (x, rt)


def test_run_e35_fast_produces_a_verdict_with_margins(tmp_path: Path) -> None:
    report = run_e3_5(out_dir=tmp_path, n_dots=24, n_terms=16, n_hist=256)
    for fmt in ("phi", "fp8", "int8"):
        p = report["per_format"][fmt]
        assert p["mac_err_per_op_ingest_incl"] > 0
        assert p["hist_l1_err"] >= 0.0
        assert p["mac_ops_per_result_ingest_incl"] > p["mac_ops_per_result_mac_only"]
    assert report["verdict"] in ("adopt", "reject")
    assert report["verdict_note"]
    assert report["passed"] is True
    assert (tmp_path / "e3.5.json").exists()
    assert set(report["margins"]["checks"]) == {
        "c1_err_per_op_10pct",
        "c2_hist_not_worse",
        "c3_ops_not_worse",
    }


def test_bit_budgets_are_equal() -> None:
    pn = PhiNumerics(exp_bits=4, mantissa_bits=3)
    assert pn.exp_bits + pn.mantissa_bits + 1 == 8  # sign + exp + mantissa
    assert 7 + 1 == 8  # fp8 E4M3
    # int8: 8 bits (symmetric)


def test_format_boundaries_are_as_documented() -> None:
    """The 8-bit formats have different dynamic ranges (measured, asserted):
    phi (4-bit exponent) spans [phi^-7, phi^8) ~= 2.5 decades; fp8 E4M3 spans
    ~[2^-9, 448] ~= 5.5 decades. The benchmark's power-histogram kernel over
    [phi^-6, phi^6] is inside both formats' ranges, so the histogram axis
    measures RESOLUTION alignment to power bins, not out-of-range crush
    (which int8, calibrated to the dataset range, does exhibit)."""

    pn = PhiNumerics(exp_bits=4, mantissa_bits=3)
    assert abs(pn.min_magnitude - PHI**-7) < 1e-12
    assert abs(pn.max_magnitude - PHI**8) < 1e-9
    assert 0.01 < pn.min_magnitude < 0.1  # phi spans ~2.5 decades at 4 exp bits
    # smallest positive phi magnitude round-trips (nonzero code, right bin)
    c = pn.encode(pn.min_magnitude)
    assert c != 0
    rt = pn.decode(c)
    assert abs(rt / pn.min_magnitude - 1.0) < 0.08
    # fp8 E4M3 boundaries
    assert Fp8E4M3.decode(0x7F) == 448.0
    assert abs(Fp8E4M3.decode(0x01) - 2.0**-9) < 1e-12  # smallest subnormal
