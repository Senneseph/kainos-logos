"""E3.2 benchmark correctness (benchmarks/topology/bench.py): the analytic
gradients of BOTH arms must match numeric finite differences — the A/B is only
honest if neither arm's optimizer is secretly broken. Plus the same-budget
structural claim.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "benchmarks"))

from topology.bench import (
    _gen_data,
    fib_batch_grad,
    fib_forward,
    fib_params,
    init_fib,
    init_mlp,
    mlp_batch_grad,
    mlp_forward,
    mlp_params,
)


def _max_rel_grad_error(grad_fn, p, xs, ys, idx, f) -> float:
    h = 1e-6
    gtree = list(grad_fn(xs, ys, idx, p))

    def loss(pp):
        return sum((f(xs[i], pp)[0] - ys[i]) ** 2 for i in idx) / len(idx)

    def flatten(obj, pre=()):
        if isinstance(obj, list):
            for k, v in enumerate(obj):
                yield from flatten(v, pre + (k,))
        else:
            yield pre

    max_err = 0.0
    for path in flatten(p):
        cur = p
        for q in path[:-1]:
            cur = cur[q]
        last = path[-1]
        base = cur[last]
        cur[last] = base + h
        lp = loss(p)
        cur[last] = base - h
        lm = loss(p)
        cur[last] = base
        num = (lp - lm) / (2.0 * h)
        cur2 = gtree
        for q in path[:-1]:
            cur2 = cur2[q]
        max_err = max(max_err, abs(num - cur2[last]) / max(1e-8, abs(num), abs(cur2[last])))
    return max_err


def test_mlp_gradients_match_numeric() -> None:
    xs, ys = _gen_data(7, 40)
    err = _max_rel_grad_error(mlp_batch_grad, init_mlp(11), xs, ys, [0, 1, 2, 3, 4], mlp_forward)
    assert err < 1e-5, err


def test_fibonacci_recurrence_gradients_match_numeric() -> None:
    xs, ys = _gen_data(7, 40)
    err = _max_rel_grad_error(fib_batch_grad, init_fib(11), xs, ys, [0, 1, 2, 3, 4], fib_forward)
    assert err < 1e-5, err


def test_arms_have_identical_parameter_budgets() -> None:
    assert mlp_params() == fib_params() == 115
