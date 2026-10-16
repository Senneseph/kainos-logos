"""Seam neutrality (P3.03, ADR-0006): with the DEFAULT numerics in play, the
Phase 1 pipeline must pass E1.1 UNCHANGED.

The `Numerics` seam is inert-by-default: `default_numerics()` is
`FloatNumerics`, an exact float64 identity, so importing the seam and running
the core under it must not perturb any Phase 1 behavior. E1.1 — byte-exact
PCRE plus a passing judge verdict on every authored-corpus record — is the
regression that proves it.
"""

from __future__ import annotations

from pathlib import Path

from kainos.numerics import FloatNumerics, default_numerics
from kainos.regex.bench import run_e1_1


def test_default_numerics_is_the_float_identity() -> None:
    n = default_numerics()
    assert isinstance(n, FloatNumerics)
    # identity, no tolerance: the exact bit pattern round-trips
    assert n.decode(n.encode(0.1)) == 0.1


def test_e1_1_passes_unchanged_under_default_numerics(tmp_path: Path) -> None:
    # The seam is imported and instantiated first: the core runs in the same
    # process, with the default numerics resolvable, and must come out exactly
    # as it did before the seam existed.
    from kainos.numerics import Numerics

    assert isinstance(default_numerics(), Numerics)

    report = run_e1_1(out_dir=tmp_path)
    assert report["accuracy"] == 1.0
    assert all(item.get("ok") for item in report["per_item"])
    assert len(report["per_item"]) > 0
