"""bandgen acceptance (S13 reference case).

The compiler's contract is proven on the one band that already
exists: ``bands/spec-e6.17.json`` (backfilled from the official S13
artifacts) must, when driven through the full control, reproduce
``e617.FROZEN`` EXACTLY, key by key, and its computed beds must
equal the brainstem's S13_BEDS table. If the compiler's table
drifts from the frozen experiment, the compiler is lying — and the
freeze discipline of every future band inherits that lie.

The dry-run drives the real mechanism (85 labeled turns, x2 for the
determinism twin, plus the seed-only carry run); expect ~1 minute.
"""

from __future__ import annotations

import json

import pytest

from tools.bandgen.control import run_control
from tools.bandgen.spec import load_spec, structural_checks

SPEC = "bands/spec-e6.17.json"


def _norm(x):
    """Json-normalize both sides so tuples/ints/keys compare as the
    frozen tables do when serialized (the house store-identity
    convention, not a new one)."""
    return json.loads(json.dumps(x, sort_keys=True, default=str))


@pytest.fixture(scope="module")
def spec() -> dict:
    return load_spec(SPEC)


@pytest.fixture(scope="module")
def frozen() -> dict:
    from kainos.tutor import e617

    return e617.FROZEN


@pytest.fixture(scope="module")
def report() -> dict:
    return run_control(load_spec(SPEC))


def test_spec_validates_and_structural_clean(spec: dict) -> None:
    assert structural_checks(spec) == []


def test_table_reproduces_frozen(report: dict, frozen: dict) -> None:
    table = _norm(report["table"])
    want = _norm(frozen)
    diffs = []
    for key in sorted(set(want) | set(table)):
        if key not in table:
            diffs.append(f"missing key: {key}")
        elif key not in want:
            diffs.append(f"unexpected key: {key}")
        elif table[key] != want[key]:
            tv, wv = table[key], want[key]
            if isinstance(tv, dict) and isinstance(wv, dict):
                for k2 in sorted(set(tv) | set(wv)):
                    if tv.get(k2) != wv.get(k2):
                        diffs.append(f"{key}[{k2}]: table {str(tv.get(k2))[:70]!r} != frozen {str(wv.get(k2))[:70]!r}")
            else:
                diffs.append(f"{key}: table {str(tv)[:100]!r} != frozen {str(wv)[:100]!r}")
    assert not diffs, "the compiler's table drifts from e617.FROZEN:\n" + "\n".join(diffs[:40])


def test_computed_beds_match_brainstem_report(report: dict) -> None:
    from kainos.tutor.brainstem import S13_BEDS

    table = _norm(report["computed_beds"])
    want = _norm(S13_BEDS)
    for key, want_v in want.items():
        assert key in table, f"computed beds missing {key}"
        assert table[key] == want_v, (
            f"computed bed {key}: {table[key]!r} != brainstem {want_v!r} "
            "(a bed that is computed, not written, must agree with the referee's table)"
        )
    assert set(table) == set(want), f"bed key set drift: {sorted(set(table) ^ set(want))}"


def test_control_is_clean(report: dict) -> None:
    assert report["ok"], "the S13 control must be CLEAN (all checks pass)"
    for name, c in report["checks"].items():
        assert c["pass"], f"{name}: {c.get('bad', [])[:4]}"


def test_determinism_twin_held(report: dict) -> None:
    assert report["checks"]["c8_totals"]["twin"] is True


def test_offline_hygiene_watchlist(report: dict, spec: dict) -> None:
    # The declared off-line witnesses must be the wall values (the
    # D-e6z hygiene): present in the spec, absent from the on-line
    # answers in the captured table.
    watch = spec["expect"]["offline_watch"]
    assert len(watch) >= 6, "the hygiene watchlist must carry the wall witness values"
    derived = report["table"]["derived_table"]
    for lit in watch:
        for ref, ans in derived.items():
            assert lit not in ans, f"off-line literal {lit} present in on-line answer at {ref}"
