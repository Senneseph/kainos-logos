"""E3.2 — Fibonacci recurrence topology vs same-budget MLP (P3.03, ADR-0006
territory: a topology experiment, benchmark-gated, hermetic, pure Python).

Task (documented, pre-registered in the report's `config`):
* n = 10 inputs; target y = w·x + 0.15·Σ_i x_i·x_(i+1 mod 10) — a linear part
  plus adjacent-cyclic pair interactions (smooth, structured, NOT a
  memorizable lookup); x ~ N(0,1)^10; 240 samples (seeded), 180 train /
  60 test.
* Arm A (baseline): MLP 10 -> 6 -> 6 -> 1, tanh, 115 parameters.
* Arm B (Fibonacci residual recurrence): X0 = tanh(W0 x + b0); the SAME map
  f(v) = F v + bf (shared weights — the topological claim) applied with
  Fibonacci residuals X_{k+2} = tanh(f(X_{k+1}) + X_k) for k = 0,1,2;
  y = wr · X3 + br. Parameters: 66 + 42 (shared) + 7 = 115 — EXACTLY the
  MLP budget.
* Training: FULL-BATCH gradient descent on MSE (gradients accumulated over
  all training samples per step, one update), LR = 0.2, 150 steps, the same
  optimizer/schedule/initialization distribution for both arms; 3 seeds
  (7, 8, 9) control data shuffle/split and weight init.
* Metric: test RMSE on the original scale, per seed.
* VERDICT RULE (pre-registered): adopt the recurrence iff it beats the MLP
  on test RMSE for ALL 3 seeds; otherwise reject. The margin is the mean
  relative improvement (negative when the recurrence loses).

Pure Python by design (the package is dependency-minimal); "toy" scale is
the point (P8: the topology claim is architectural, not capacity — the arms
have identical parameter budgets).
"""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path

from kainos.harness.paths import (  # results hygiene
    default_phase_dir,
    default_results_dir,
)

SEEDS = (7, 8, 9)
N_IN = 10
WIDTH = 6  # hidden width (near the Fibonacci schedule 1,1,2,3,5,8)


def _gen_data(seed: int, n: int) -> tuple[list[list[float]], list[float]]:
    """Seeded task data: x ~ N(0,1)^10, y = w·x + 0.15·Σ cyclic pairs."""

    rng = random.Random(10_000 + seed)
    w_task = [rng.gauss(0.0, 0.35) for _ in range(N_IN)]
    xs: list[list[float]] = []
    ys: list[float] = []
    for _ in range(n):
        x = [rng.gauss(0.0, 1.0) for _ in range(N_IN)]
        y = sum(wi * xi for wi, xi in zip(w_task, x))
        for i in range(N_IN):
            y += 0.15 * x[i] * x[(i + 1) % N_IN]
        xs.append(x)
        ys.append(y)
    return xs, ys


# ── MLP (10 -> 6 -> 6 -> 1) ─────────────────────────────────────────────────


def mlp_params() -> int:
    return N_IN * WIDTH + WIDTH + WIDTH * WIDTH + WIDTH + WIDTH + 1


def init_mlp(seed: int):
    rng = random.Random(seed)
    w1 = [[rng.uniform(-0.5, 0.5) for _ in range(N_IN)] for _ in range(WIDTH)]
    b1 = [0.0] * WIDTH
    w2 = [[rng.uniform(-0.5, 0.5) for _ in range(WIDTH)] for _ in range(WIDTH)]
    b2 = [0.0] * WIDTH
    wr = [rng.uniform(-0.5, 0.5) for _ in range(WIDTH)]
    br = 0.0
    return [w1, b1, w2, b2, wr, br]


def mlp_forward(x, p):
    w1, b1, w2, b2, wr, br = p
    h1 = [math.tanh(sum(w1[j][i] * x[i] for i in range(N_IN)) + b1[j]) for j in range(WIDTH)]
    h2 = [math.tanh(sum(w2[j][k] * h1[k] for k in range(WIDTH)) + b2[j]) for j in range(WIDTH)]
    return sum(wr[j] * h2[j] for j in range(WIDTH)) + br, (h1, h2)


def mlp_batch_grad(xs, ys, idx, p):
    """Accumulate (e² loss) gradients over the training set. Full batch."""

    _w1, _b1, w2, _b2, wr, _br = p
    g1 = [[0.0] * N_IN for _ in range(WIDTH)]
    gb1 = [0.0] * WIDTH
    g2 = [[0.0] * WIDTH for _ in range(WIDTH)]
    gb2 = [0.0] * WIDTH
    gwr = [0.0] * WIDTH
    gbr = 0.0
    for i in idx:
        x, y = xs[i], ys[i]
        yhat, (h1, h2) = mlp_forward(x, p)
        e = 2.0 * (yhat - y)  # d(yhat-y)^2/dyhat, mean over the batch applied in the step
        gbr += e
        dh2 = [e * wr[j] * (1.0 - h2[j] * h2[j]) for j in range(WIDTH)]
        for j in range(WIDTH):
            gwr[j] += e * h2[j]
            gb2[j] += dh2[j]
            for k in range(WIDTH):
                g2[j][k] += dh2[j] * h1[k]
        for k in range(WIDTH):
            acc = 0.0
            for j in range(WIDTH):
                acc += dh2[j] * w2[j][k]
            gb1[k] += acc * (1.0 - h1[k] * h1[k])
            for i2 in range(N_IN):
                g1[k][i2] += acc * (1.0 - h1[k] * h1[k]) * x[i2]
    n = float(len(idx))  # gradients of the MEAN loss
    for j in range(WIDTH):
        for i in range(N_IN):
            g1[j][i] /= n
        gb1[j] /= n
        for k in range(WIDTH):
            g2[j][k] /= n
        gb2[j] /= n
        gwr[j] /= n
    gbr /= n
    return g1, gb1, g2, gb2, gwr, gbr


def mlp_step(xs, ys, idx, p, lr) -> None:
    w1, b1, w2, b2, wr, br = p
    g1, gb1, g2, gb2, gwr, gbr = mlp_batch_grad(xs, ys, idx, p)  # mean-loss gradients
    for j in range(WIDTH):
        for i in range(N_IN):
            w1[j][i] -= lr * g1[j][i]
        b1[j] -= lr * gb1[j]
        for k in range(WIDTH):
            w2[j][k] -= lr * g2[j][k]
        b2[j] -= lr * gb2[j]
        wr[j] -= lr * gwr[j]
    br -= lr * gbr


# ── Fibonacci residual recurrence ──────────────────────────────────────────


def fib_params() -> int:
    return N_IN * WIDTH + WIDTH + WIDTH * WIDTH + WIDTH + WIDTH + 1


def init_fib(seed: int):
    rng = random.Random(seed)
    w0 = [[rng.uniform(-0.5, 0.5) for _ in range(N_IN)] for _ in range(WIDTH)]
    b0 = [0.0] * WIDTH
    F = [[rng.uniform(-0.2, 0.2) for _ in range(WIDTH)] for _ in range(WIDTH)]  # shared map
    bf = [0.0] * WIDTH
    wr = [rng.uniform(-0.5, 0.5) for _ in range(WIDTH)]
    br = 0.0
    return [w0, b0, F, bf, wr, br]


def fib_forward(x, p):
    w0, b0, F, bf, wr, br = p
    X0 = [math.tanh(sum(w0[j][i] * x[i] for i in range(N_IN)) + b0[j]) for j in range(WIDTH)]
    X1 = [math.tanh(sum(F[j][k] * X0[k] for k in range(WIDTH)) + bf[j]) for j in range(WIDTH)]
    z2 = [sum(F[j][k] * X1[k] for k in range(WIDTH)) + bf[j] + X0[j] for j in range(WIDTH)]
    X2 = [math.tanh(z) for z in z2]
    z3 = [sum(F[j][k] * X2[k] for k in range(WIDTH)) + bf[j] + X1[j] for j in range(WIDTH)]
    X3 = [math.tanh(z) for z in z3]
    return sum(wr[j] * X3[j] for j in range(WIDTH)) + br, (X0, X1, X2, X3)


def fib_batch_grad(xs, ys, idx, p):
    """Full-batch gradients for the recurrence.

    Graph (per sample):
      z3 = F X2 + bf + X1 ; X3 = tanh(z3)         (readout on X3)
      z2 = F X1 + bf + X0 ; X2 = tanh(z2)
      z1 = F X0 + bf      ; X1 = tanh(z1)
      z0 = W0 x + b0      ; X0 = tanh(z0)
    The shared map F accumulates gradients from ALL THREE applications;
    everything is accumulated over the whole training set before returning.
    """

    _w0, _b0, F, _bf, wr, _br = p
    g0m = [[0.0] * N_IN for _ in range(WIDTH)]
    gb0 = [0.0] * WIDTH
    gF = [[0.0] * WIDTH for _ in range(WIDTH)]
    gbf = [0.0] * WIDTH
    gwr = [0.0] * WIDTH
    gbr = 0.0
    for i in idx:
        x, y = xs[i], ys[i]
        yhat, (X0, X1, X2, X3) = fib_forward(x, p)
        e = 2.0 * (yhat - y)  # d(yhat-y)^2/dyhat, mean over the batch applied in the step
        gbr += e
        g3 = [e * wr[j] * (1.0 - X3[j] * X3[j]) for j in range(WIDTH)]  # dL/dz3

        # readout
        for j in range(WIDTH):
            gwr[j] += e * X3[j]

        # application 3 (z3 = F X2 + bf + X1)
        dX1 = list(g3)  # the linear +X1 leg
        for j in range(WIDTH):
            gF_row = gF[j]
            gbf[j] += g3[j]
            X2r = X2
            for k in range(WIDTH):
                gF_row[k] += g3[j] * X2r[k]
        dX2 = [0.0] * WIDTH
        for j in range(WIDTH):
            Fj = F[j]
            for k in range(WIDTH):
                dX2[k] += Fj[k] * g3[j]
        g2 = [dX2[j] * (1.0 - X2[j] * X2[j]) for j in range(WIDTH)]  # dL/dz2

        # application 2 (z2 = F X1 + bf + X0)
        dX0 = list(g2)  # the linear +X0 leg
        for j in range(WIDTH):
            gF_row = gF[j]
            gbf[j] += g2[j]
            for k in range(WIDTH):
                gF_row[k] += g2[j] * X1[k]
        for j in range(WIDTH):
            Fj = F[j]
            for k in range(WIDTH):
                dX1[k] += Fj[k] * g2[j]
        g1 = [dX1[j] * (1.0 - X1[j] * X1[j]) for j in range(WIDTH)]  # dL/dz1

        # application 1 (z1 = F X0 + bf)
        for j in range(WIDTH):
            gF_row = gF[j]
            gbf[j] += g1[j]
            for k in range(WIDTH):
                gF_row[k] += g1[j] * X0[k]
        for j in range(WIDTH):
            Fj = F[j]
            for k in range(WIDTH):
                dX0[k] += Fj[k] * g1[j]
        g0 = [dX0[j] * (1.0 - X0[j] * X0[j]) for j in range(WIDTH)]  # dL/dz0

        # input layer
        for j in range(WIDTH):
            gb0[j] += g0[j]
            row = g0m[j]
            g0j = g0[j]
            for i2 in range(N_IN):
                row[i2] += g0j * x[i2]
    n = float(len(idx))  # gradients of the MEAN loss
    for j in range(WIDTH):
        for i in range(N_IN):
            g0m[j][i] /= n
        gb0[j] /= n
        for k in range(WIDTH):
            gF[j][k] /= n
        gbf[j] /= n
        gwr[j] /= n
    gbr /= n
    return g0m, gb0, gF, gbf, gwr, gbr


def fib_step(xs, ys, idx, p, lr) -> None:
    w0, b0, F, bf, wr, br = p
    g0m, gb0, gF, gbf, gwr, gbr = fib_batch_grad(xs, ys, idx, p)  # mean-loss gradients
    for j in range(WIDTH):
        for i in range(N_IN):
            w0[j][i] -= lr * g0m[j][i]
        b0[j] -= lr * gb0[j]
        for k in range(WIDTH):
            F[j][k] -= lr * gF[j][k]
        bf[j] -= lr * gbf[j]
        wr[j] -= lr * gwr[j]
    br -= lr * gbr


# ── the experiment ─────────────────────────────────────────────────────────


def run_e3_2(
    out_dir: str | Path | None = None,
    n_total: int | None = None,
    n_steps: int | None = None,
    lr: float = 0.2,
) -> dict:
    """The pre-registered A/B (module docstring). Writes `e3.2.json` (+ flat
    `results/e3.2.{json,md}`). Returns the report with `verdict` + `passed`."""

    n_total = n_total if n_total is not None else int(os.environ.get("KAINOS_E32_SAMPLES", "240"))
    n_steps = n_steps if n_steps is not None else int(os.environ.get("KAINOS_E32_STEPS", "150"))
    n_test = max(8, n_total // 4)
    n_train = n_total - n_test

    per_seed = []
    for seed in SEEDS:
        xs, ys = _gen_data(seed, n_total)
        order = list(range(n_total))
        random.Random(seed + 1_000_000).shuffle(order)
        tr = [order[i] for i in range(n_train)]
        te = [order[i] for i in range(n_train, n_total)]

        mlp_p = init_mlp(seed)
        for _ in range(n_steps):
            mlp_step(xs, ys, tr, mlp_p, lr)
        mlp_rmse = _rmse(xs, ys, te, mlp_p, mlp_forward)

        fib_p = init_fib(seed)
        for _ in range(n_steps):
            fib_step(xs, ys, tr, fib_p, lr)
        fib_rmse = _rmse(xs, ys, te, fib_p, fib_forward)

        base_rmse = _baseline_rmse(xs, ys, te)
        per_seed.append(
            {
                "seed": seed,
                "mlp_rmse": mlp_rmse,
                "fib_rmse": fib_rmse,
                "baseline_rmse_no_learning": base_rmse,
                "fib_won": fib_rmse < mlp_rmse,
            }
        )

    mlp_mean = sum(s["mlp_rmse"] for s in per_seed) / len(per_seed)
    fib_mean = sum(s["fib_rmse"] for s in per_seed) / len(per_seed)
    mean_rel = (mlp_mean - fib_mean) / mlp_mean  # positive = recurrence better
    wins = [s["seed"] for s in per_seed if s["fib_won"]]
    adopt = len(wins) == len(SEEDS)
    verdict = "adopt" if adopt else "reject"
    note = (
        f"recurrence beats MLP on all {len(SEEDS)} seeds (mean relative improvement {mean_rel:+.2%})"
        if adopt
        else f"recurrence wins on {len(wins)}/{len(SEEDS)} seeds, mean relative "
        f"improvement {mean_rel:+.2%} (rule: must win ALL seeds)"
    )

    report = {
        "config": {
            "seeds": list(SEEDS),
            "n_total": n_total,
            "n_train": n_train,
            "n_test": n_test,
            "n_steps": n_steps,
            "lr": lr,
            "task": "y = w·x + 0.15·Σ x_i·x_(i+1 mod 10), x ~ N(0,1)^10 (linear + cyclic pair interactions)",
            "arms": {
                "mlp": f"10 -> 6 -> 6 -> 1 tanh, {mlp_params()} params",
                "fibonacci_recurrence": (
                    f"X0 = tanh(W0 x + b0); shared f(v) = F v + bf; X_{{k+2}} = tanh(f(X_{{k+1}}) + X_k), "
                    f"k = 0..2; y = wr·X3 + br; {fib_params()} params (shared F applied 3x)"
                ),
            },
            "param_budget": {"mlp": mlp_params(), "fibonacci_recurrence": fib_params(), "equal": mlp_params() == fib_params()},
            "training": "true full-batch GD (gradient accumulated over all training samples per step, single update), MSE, identical schedule and init distributions for both arms",
            "verdict_rule": (
                "adopt iff the recurrence beats the MLP on test RMSE for ALL 3 seeds; "
                "otherwise reject. Passed = an explicit verdict with documented margin (P8)."
            ),
        },
        "per_seed": per_seed,
        "summary": {
            "mlp_mean_test_rmse": mlp_mean,
            "fib_mean_test_rmse": fib_mean,
            "fib_wins": wins,
            "mean_relative_improvement": mean_rel,
        },
        "verdict": verdict,
        "verdict_note": note,
        "passed": True,  # an explicit verdict with a documented margin was produced
    }

    out = Path(out_dir) if out_dir is not None else default_phase_dir(3)  # results hygiene
    out.mkdir(parents=True, exist_ok=True)
    (out / "e3.2.json").write_text(json.dumps(report, indent=2))
    flat = default_results_dir()  # follows KAINOS_RESULTS_DIR (tests: session tmpdir)
    flat.mkdir(parents=True, exist_ok=True)
    (flat / "e3.2.json").write_text(json.dumps(report, indent=2))
    lines = [
        "# E3.2 — Fibonacci residual recurrence vs same-budget MLP",
        "",
        f"**Verdict: {verdict.upper()}** — {note}",
        "",
        "| seed | MLP test RMSE | recurrence test RMSE | recurrence wins |",
        "|---|---|---|---|",
    ]
    for sline in per_seed:
        lines.append(
            f"| {sline['seed']} | {sline['mlp_rmse']:.4f} | {sline['fib_rmse']:.4f} | "
            f"{'yes' if sline['fib_won'] else 'no'} |"
        )
    lines += [
        "",
        (
            f"Mean test RMSE: MLP {mlp_mean:.4f} vs recurrence {fib_mean:.4f} "
            f"(relative improvement {mean_rel:+.2%})."
        ),
        "",
        (
            f"{mlp_params()} params each (identical budget); {n_train} train / {n_test} test; "
            f"{n_steps} steps; full-batch GD lr={lr}."
        ),
        "",
    ]
    (flat / "e3.2.md").write_text("\n".join(lines) + "\n")
    return report


def _rmse(xs, ys, te, p, forward) -> float:
    sse = 0.0
    for i in te:
        yhat = forward(xs[i], p)[0]
        sse += (yhat - ys[i]) ** 2
    return math.sqrt(sse / len(te))


def _baseline_rmse(xs, ys, te) -> float:
    mean = sum(ys[i] for i in te) / len(te)
    sse = sum((ys[i] - mean) ** 2 for i in te)
    return math.sqrt(sse / len(te))


class E3_2Experiment:
    """Registered as `e3.2` in the harness registry (P3.03, ADR-0006 territory)."""

    name = "e3.2"
    hypothesis = (
        "Fibonacci recurrence topology (X_{n+2} = f(X_{n+1}) + X_n with a shared "
        "f, and Fibonacci width schedules 1,1,2,3,5,8) extracts more structure "
        "per parameter than a same-budget MLP"
    )
    metric = "test RMSE on a linear + cyclic-pair-interaction task, same parameter budget, 3 seeds"
    threshold = (
        "residual recurrence beats a same-budget MLP on test RMSE for all 3 seeds at matched "
        "depth/params (toy scale, hermetic); adopt or reject with a documented margin (P8)"
    )

    def run(self):
        from kainos.harness.runner import Result

        report = run_e3_2()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=report["summary"]["fib_mean_test_rmse"],
            threshold=self.threshold,
            evidence=[Path("results/phase-3/e3.2.json")],
            config={
                "verdict": report["verdict"],
                "verdict_note": report["verdict_note"],
                "mlp_mean_test_rmse": report["summary"]["mlp_mean_test_rmse"],
                "fib_wins": report["summary"]["fib_wins"],
                "mean_relative_improvement": report["summary"]["mean_relative_improvement"],
                "seeds": report["config"]["seeds"],
                "param_budget": report["config"]["param_budget"],
            },
        )
