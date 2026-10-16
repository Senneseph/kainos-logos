"""E3.5 — φ numerics vs FP8 / INT8 at a matched 8-bit budget (P3.03, ADR-0006).

Pre-registered before the official run (recorded verbatim in the report's
`config`):

* All formats use 8 bits per value: φ = 1 sign + 4 exponent + 3 mantissa
  (the library `PhiNumerics` default); FP8 = E4M3 (OCP layout, max 448);
  INT8 = symmetric (-127..127) calibrated to the dataset range.
* Two hermetic, seeded kernel tasks:
  - MAC: 200 dot products of 32 N(0,1) terms (seed 20260820), error vs the
    float64 reference.
  - power-histogram: 4096 log-uniform values in [φ^-6, φ^6] binned by exact
    φ-power bin, L1 count error vs the ground-truth histogram.
* Ops accounting (the "per-op" denominator):
  - ingest quantization: fixed, documented model per value (phi 6, fp8 6,
    int8 3 — the two "scientific" formats pay for a log, int8 only a scale
    multiply); each dataset value is quantized ONCE (cold cache) and the
    total is shared across the task;
  - MAC loop: ops COUNTED LIVE (sign xor = 1, exponent add = 1, mass add = 1
    per pair; a carry = div + mul + sub + add; the final fold = mul + add
    per occupied level); baselines: 1 mul + 1 add per pair + 1 final dequant
    scale;
  - the 8x8 φ product LUT build (64 muls) is a one-time cost reported
    separately, not amortized into per-op; histogram bin lookup tables
    (built once per format) are storage, not ops.
* VERDICT RULE (adopt only if ALL hold; a reject is a valid methodological
  outcome, P8):
  1. MAC: phi.err_per_op (ingest-incl) <= 0.9 * min(fp8, int8).err_per_op
  2. histogram: phi.l1 <= max(fp8, int8).l1 (not worse than the baselines)
  3. phi.ops_per_result (ingest-incl) <= min(fp8, int8).ops_per_result
  Margins are documented as the actual ratios in the report.

The experiment PASSES (harness `Result.passed`) when the A/B produced an
explicit adopt/reject verdict with the documented margin — the gate is the
method, the verdict is the finding.
"""

from __future__ import annotations

import json
import math
import os
import random
from collections.abc import Sequence
from pathlib import Path

from kainos.harness.paths import (  # results hygiene
    default_phase_dir,
    default_results_dir,
)
from kainos.numerics.phi import PHI, PhiNumerics

SEED = 20260820
PHI_EXP_BITS = 4  # 8 bits/value = 1 sign + 4 exponent + 3 mantissa
PHI_MANTISSA_BITS = 3

# fixed ingest-quantization op model (see module docstring)
INGEST_OPS = {"phi": 6, "fp8": 6, "int8": 3}


# ── FP8 E4M3 (OCP: bias 7, no inf/nan, max 448, subnormals to 2^-9) ────────


class Fp8E4M3:
    @staticmethod
    def encode(x: float) -> int:
        if x == 0.0:
            return 0
        sign = 1 if x < 0.0 else 0
        a = abs(x)
        if a >= 448.0:  # overflow -> max normal
            return (sign << 7) | (15 << 3) | 7
        e2 = math.floor(math.log2(a))
        if e2 >= -6:  # normal: (1 + m/8) * 2^(e-7)
            frac = a / (2.0**e2) - 1.0
            q = round(frac * 8.0)
            if q > 7:  # mantissa carry to the next exponent
                q, e2 = 0, e2 + 1
            code_e = e2 + 7
        else:  # subnormal: (m/8) * 2^-6
            q = round(a / (2.0**-9))  # subnormal step is 2^-9
            if q >= 8:  # rounds up to the smallest normal: 2^-6
                return (sign << 7) | (1 << 3)
            code_e = 0
        return (sign << 7) | (code_e << 3) | q

    @staticmethod
    def decode(i: int) -> float:
        sign = -1.0 if i & 0x80 else 1.0
        e = (i >> 3) & 0xF
        m = i & 7
        if e == 0:
            v = (m / 8.0) * 2.0**-6
        elif e == 15 and m == 7:
            v = 448.0
        else:
            v = (1.0 + m / 8.0) * 2.0 ** (e - 7)
        return sign * v


# ── INT8, symmetric, range-calibrated ──────────────────────────────────────


class Int8Calibrated:
    def __init__(self, range_max: float) -> None:
        self.range_max = float(range_max)
        self.scale = 127.0 / self.range_max

    def encode(self, x: float) -> int:
        q = round(x * self.scale)
        return min(max(q, -127), 127)

    def decode(self, i: int) -> float:
        return i / self.scale


# ── helpers ─────────────────────────────────────────────────────────────────


def phi_codes(values: Sequence[float], pn: PhiNumerics) -> list[tuple[int, int, int]]:
    """(sign, exponent, q) per value, via the public encode/decode seam."""

    out: list[tuple[int, int, int]] = []
    for v in values:
        c = pn.encode(v)
        s, n, m_q = pn._unpack(c)  # internal read of own packed fields
        q = round((m_q - 1.0) / pn.step - 0.5)
        out.append((s, n, min(max(q, 0), 7)))
    return out


def _phi_table(pn: PhiNumerics) -> tuple[list[float], list[list[tuple[int, float]]]]:
    """Per-quantum mantissa values and the 8x8 product LUT:
    lut[qa][qb] = (carry, m_prod) with m_prod = m_qa · m_qb EXACT (one of
    64 values) and carry = 1 iff m_prod >= φ. Plan-faithful design: the MAC
    mass-adds the exact product of the two quantized mantissas; there is no
    per-product re-quantization. Re-quantization happens only where the plan
    puts it — the Fibonacci-carry division (counted float divide) and the
    final fold."""

    manta = [1.0 + (q + 0.5) * pn.step for q in range(8)]
    lut: list[list[tuple[int, float]]] = []
    for qa in range(8):
        row = []
        for qb in range(8):
            m = manta[qa] * manta[qb]
            if m >= PHI:  # the level shifts up one: the mass is m/phi there
                row.append((1, m / PHI))
            else:
                row.append((0, m))
        lut.append(row)
    return manta, lut


# ── MAC kernels (MAC-loop ops counted live) ─────────────────────────────────


def mac_phi(
    xs: Sequence[tuple[int, int, int]],
    ws: Sequence[tuple[int, int, int]],
    lut: Sequence[Sequence[tuple[int, float]]],
) -> tuple[float, int]:
    """φ MAC (plan-faithful): per pair = sign xor, exponent ADD, mass ADD of
    the EXACT quantized-mantissa product into the digit string; Fibonacci
    carries (φ units of level k -> 1 unit of level k+1, via a counted float
    divide) and the final fold complete it. Returns (value, ops)."""

    ops = 0
    digits: dict[int, float] = {}
    for i, (sx, ex, qx) in enumerate(xs):
        sw, ew, qw = ws[i]
        ops += 1  # sign xor
        s = sx * sw
        carry, m_prod = lut[qx][qw]
        ops += 1  # exponent add (per pair — the advertised replace-the-mul op)
        level = ex + ew + carry
        ops += 1  # mass add into the accumulator digit string
        digits[level] = digits.get(level, 0.0) + s * m_prod
    # Fibonacci-carry normalization (bounded passes; carries move strictly up)
    for _ in range(32):
        moved = False
        for k in sorted(digits):
            d = digits.get(k, 0.0)
            if d != 0.0 and abs(d) >= PHI:
                ops += 4  # div by φ; mul + sub for the remainder; add up a level
                carry_up = d / PHI
                digits[k] = d - carry_up * PHI
                digits[k + 1] = digits.get(k + 1, 0.0) + carry_up
                moved = True
        if not moved:
            break
    total = 0.0
    for k, d in digits.items():
        ops += 2  # mul by φ^k + add
        total += d * (PHI**k)
    return total, ops


def mac_plain(xs_q: Sequence[float], ws_q: Sequence[float], out_scale: float) -> tuple[float, int]:
    """Baseline MAC: 1 mul + 1 add per pair on the quantized values, one
    final dequant scale (1 mul). Returns (value, ops)."""

    ops = 0
    acc = 0.0
    for xq, wq in zip(xs_q, ws_q):
        ops += 1  # mul
        acc += xq * wq
        ops += 1  # add
    ops += 1  # final dequant scale
    return acc * out_scale, ops


# ── the A/B ─────────────────────────────────────────────────────────────────


def run_e3_5(
    out_dir: str | Path | None = None,
    n_dots: int | None = None,
    n_terms: int | None = None,
    n_hist: int | None = None,
) -> dict:
    """The pre-registered A/B (module docstring). Writes `e3.5.json` (+ flat
    `results/e3.5.{json,md}`). Returns the report with `verdict` + `passed`."""

    n_dots = n_dots if n_dots is not None else int(os.environ.get("KAINOS_E35_DOTS", "200"))
    n_terms = n_terms if n_terms is not None else int(os.environ.get("KAINOS_E35_TERMS", "32"))
    n_hist = n_hist if n_hist is not None else int(os.environ.get("KAINOS_E35_HIST", "4096"))

    rng = random.Random(SEED)
    pn = PhiNumerics(exp_bits=PHI_EXP_BITS, mantissa_bits=PHI_MANTISSA_BITS)
    _, lut = _phi_table(pn)
    lut_build_ops = 64  # 8x8 product table: one multiply per entry (one-time)

    # ── MAC data (quantized ONCE per value — cold cache) ───────────────────
    ws = [rng.gauss(0.0, 1.0) for _ in range(n_terms)]
    dots: list[list[float]] = [[rng.gauss(0.0, 1.0) for _ in range(n_terms)] for _ in range(n_dots)]
    all_vals = ws + [x for row in dots for x in row]
    range_max = max(abs(v) for v in all_vals)
    int8 = Int8Calibrated(range_max)

    ws_phi = phi_codes(ws, pn)
    xs_phi_all = [phi_codes(row, pn) for row in dots]
    ws_fp8 = [Fp8E4M3.decode(Fp8E4M3.encode(w)) for w in ws]
    ws_int8 = [int8.decode(int8.encode(w)) for w in ws]
    xs_fp8_all = [[Fp8E4M3.decode(Fp8E4M3.encode(x)) for x in row] for row in dots]
    xs_int8_all = [[int8.decode(int8.encode(x)) for x in row] for row in dots]

    # Error metric (documented refinement of the plan's "error-per-op"): per-dot
    # error is normalized by the REFERENCE signal scale ||y||_2 over all dots
    # (fixed, never near zero — a per-dot |y| denominator is unstable because
    # 32-term N(0,1) dot products land arbitrarily close to 0). All formats
    # share the same denominator.
    y_exact = [math.fsum(x * w for x, w in zip(row, ws)) for row in dots]
    ref_scale = math.sqrt(sum(y * y for y in y_exact))

    mac_ops = {"phi": 0, "fp8": 0, "int8": 0}
    mac_rel: dict[str, list[float]] = {"phi": [], "fp8": [], "int8": []}
    for i, row in enumerate(dots):
        y, ops = mac_phi(xs_phi_all[i], ws_phi, lut)
        mac_rel["phi"].append(abs(y - y_exact[i]) / ref_scale)
        mac_ops["phi"] += ops

        y, ops = mac_plain(xs_fp8_all[i], ws_fp8, 1.0)
        mac_rel["fp8"].append(abs(y - y_exact[i]) / ref_scale)
        mac_ops["fp8"] += ops

        y, ops = mac_plain(xs_int8_all[i], ws_int8, (range_max / 127.0) ** 2)
        mac_rel["int8"].append(abs(y - y_exact[i]) / ref_scale)
        mac_ops["int8"] += ops

    n_ingest_values = n_terms + n_dots * n_terms
    ingest_ops = {fmt: INGEST_OPS[fmt] * n_ingest_values for fmt in ("phi", "fp8", "int8")}

    # ── power histogram (single pass) ───────────────────────────────────────
    # ground truth + per-format bins. Bins are exact φ-exponent bins over
    # [-6, 6]; each format bins its QUANTIZED value. φ reads the exponent
    # straight from its code (0 ops); fp8/int8 use a precomputed code->bin
    # lookup table (built once — storage, not ops).
    truth: dict[int, int] = {}
    bins: dict[str, dict[int, int]] = {"phi": {}, "fp8": {}, "int8": {}}
    rng_h = random.Random(SEED + 1)

    fp8_bin_lut = {
        c: _phi_bin_of(Fp8E4M3.decode(c)) for c in range(256) if c != 0
    }
    int8_bin_lut = {c: _phi_bin_of(int8.decode(c)) for c in range(-127, 128) if c != 0}

    for _ in range(n_hist):
        a = PHI ** rng_h.uniform(-6.0, 6.0)
        truth[_phi_bin_of(a)] = truth.get(_phi_bin_of(a), 0) + 1

        c_p = pn.encode(a)
        _, n_p, _ = pn._unpack(c_p)  # the exponent is the code's own field
        bins["phi"][n_p] = bins["phi"].get(n_p, 0) + 1

        code = Fp8E4M3.encode(a)
        n_b = fp8_bin_lut[code] if code != 0 else -6
        bins["fp8"][n_b] = bins["fp8"].get(n_b, 0) + 1

        q_i = int8.encode(a)
        n_i = int8_bin_lut[q_i] if q_i != 0 else -6
        bins["int8"][n_i] = bins["int8"].get(n_i, 0) + 1

    def l1(b: dict[int, int]) -> float:
        keys = set(truth) | set(b)
        return sum(abs(b.get(k, 0) - truth.get(k, 0)) for k in keys) / n_hist

    # ── assemble ────────────────────────────────────────────────────────────
    per_format = {}
    for fmt in ("phi", "fp8", "int8"):
        total_rel = sum(mac_rel[fmt])
        total_ops_mac = mac_ops[fmt]
        total_ops_incl = mac_ops[fmt] + ingest_ops[fmt]
        per_format[fmt] = {
            "mac_rms_rel_err_refnorm": math.sqrt(sum(r * r for r in mac_rel[fmt]) / n_dots),
            "mac_total_rel_err_refnorm": total_rel,
            "mac_ops_per_result_mac_only": total_ops_mac / n_dots,
            "mac_ops_per_result_ingest_incl": total_ops_incl / n_dots,
            "mac_err_per_op_mac_only": total_rel / total_ops_mac,
            "mac_err_per_op_ingest_incl": total_rel / total_ops_incl,
            "hist_l1_err": l1(bins[fmt]),
        }
    per_format["phi"]["lut_build_ops_one_time"] = lut_build_ops

    phi_mac = per_format["phi"]["mac_err_per_op_ingest_incl"]
    base_mac = min(per_format["fp8"]["mac_err_per_op_ingest_incl"], per_format["int8"]["mac_err_per_op_ingest_incl"])
    phi_l1 = per_format["phi"]["hist_l1_err"]
    base_l1_max = max(per_format["fp8"]["hist_l1_err"], per_format["int8"]["hist_l1_err"])
    phi_ops = per_format["phi"]["mac_ops_per_result_ingest_incl"]
    base_ops = min(
        per_format["fp8"]["mac_ops_per_result_ingest_incl"],
        per_format["int8"]["mac_ops_per_result_ingest_incl"],
    )
    c1 = phi_mac <= 0.9 * base_mac
    c2 = phi_l1 <= base_l1_max
    c3 = phi_ops <= base_ops
    adopt = c1 and c2 and c3
    verdict = "adopt" if adopt else "reject"
    failed = [
        *([f"mac err/op {phi_mac:.4g} vs allowed 0.9*min(base) {0.9 * base_mac:.4g}"] if not c1 else []),
        *([f"hist L1 {phi_l1:.4g} > max(base) L1 {base_l1_max:.4g}"] if not c2 else []),
        *([f"ops/result {phi_ops:.4g} > min(base) {base_ops:.4g}"] if not c3 else []),
    ]
    note = "phi wins all three axes (err-per-op by >=10%, hist not worse, ops not worse)" if adopt else "rejects; " + "; ".join(failed)

    report = {
        "config": {
            "seed": SEED,
            "n_dots": n_dots,
            "n_terms": n_terms,
            "n_hist": n_hist,
            "bits_per_value": 8,
            "formats": {
                "phi": "1 sign + 4 exponent (bias 7) + 3 mantissa; midpoint quanta over [1, phi)",
                "fp8": "E4M3 (bias 7, max 448, subnormals to 2^-9)",
                "int8": f"symmetric -127..127 calibrated to dataset range R={range_max:.6g}",
            },
            "ingest_ops_model": INGEST_OPS,
            "ingest_policy": "each dataset value quantized once (cold cache); total shared across the task",
            "error_metric": (
                "per-dot |y_hat - y| / ||y_ref||_2 (shared reference scale over all dots — "
                "robust vs a per-dot denominator, which is unstable for near-zero 32-term "
                "dot products); err_per_op = total rel err / total ops"
            ),
            "mac_ops_counted": (
                "live per format: phi = sign xor + exponent add + mass add per pair, carries "
                "(div+mul+sub+add), fold (mul+add per level); fp8/int8 = mul+add per pair + 1 dequant scale"
            ),
            "hist_bin_policy": "phi bins from its own code field (0 ops); fp8/int8 via precomputed code->bin LUT (storage, not ops)",
            "lut_build_ops_one_time": lut_build_ops,
            "mass_product_policy": (
                "plan-faithful: the exact product of the two quantized mantissas is the "
                "added mass (64-valued one-time table); no per-product re-quantization; "
                "re-quantization only via Fibonacci-carry division and the final fold"
            ),
            "verdict_rule": (
                "adopt iff (1) phi MAC err_per_op(ingest-incl) <= 0.9 * min(fp8,int8) AND "
                "(2) phi hist L1 <= max(fp8,int8) L1 AND (3) phi ops_per_result(ingest-incl) <= "
                "min(fp8,int8); else reject. Experiment passes on producing an explicit verdict "
                "with documented margin (P8: reject is a valid outcome)."
            ),
        },
        "per_format": per_format,
        "margins": {
            "phi_mac_err_per_op_ingest_incl": phi_mac,
            "min_base_mac_err_per_op_ingest_incl": base_mac,
            "phi_hist_l1": phi_l1,
            "max_base_hist_l1": base_l1_max,
            "phi_ops_per_result_ingest_incl": phi_ops,
            "min_base_ops_per_result_ingest_incl": base_ops,
            "checks": {"c1_err_per_op_10pct": bool(c1), "c2_hist_not_worse": bool(c2), "c3_ops_not_worse": bool(c3)},
        },
        "verdict": verdict,
        "verdict_note": note,
        "passed": True,  # an explicit verdict with a documented margin was produced
    }

    out = Path(out_dir) if out_dir is not None else default_phase_dir(3)  # results hygiene
    out.mkdir(parents=True, exist_ok=True)
    (out / "e3.5.json").write_text(json.dumps(report, indent=2))
    flat = default_results_dir()  # follows KAINOS_RESULTS_DIR (tests: session tmpdir)
    flat.mkdir(parents=True, exist_ok=True)
    (flat / "e3.5.json").write_text(json.dumps(report, indent=2))
    lines = [
        "# E3.5 — φ numerics vs FP8 / INT8 at 8 bits/value",
        "",
        f"**Verdict: {verdict.upper()}** — {note}",
        "",
    ]
    for fmt, p in per_format.items():
        lines.append(
            f"- **{fmt}**: MAC rms rel err (ref-norm) {p['mac_rms_rel_err_refnorm']:.4g} | "
            f"err/op (ingest-incl) {p['mac_err_per_op_ingest_incl']:.4g} | "
            f"err/op (MAC-only) {p['mac_err_per_op_mac_only']:.4g} | "
            f"ops/result (ingest-incl) {p['mac_ops_per_result_ingest_incl']:.1f} | "
            f"hist L1 {p['hist_l1_err']:.4g}"
        )
    lines += [
        "",
        (
            f"A/B: {n_dots} dot products x {n_terms} N(0,1) terms (seed {SEED}); "
            f"histogram of {n_hist} values log-uniform in [φ⁻⁶, φ⁶]. 8 bits/value in all formats."
        ),
        "",
        f"Int8 calibration range: {range_max:.4g}. φ product LUT build: {lut_build_ops} one-time muls.",
    ]
    (flat / "e3.5.md").write_text("\n".join(lines) + "\n")
    return report


def _phi_bin_of(v: float) -> int:
    """The exact φ-power bin of a positive v: the canonical exponent whose
    mantissa lies in [1, φ), with the same tolerant top-boundary snap the
    library's normalize uses (1e-9)."""

    if v <= 0.0:
        return -6
    n = math.floor(math.log(v) / math.log(PHI))
    if v / (PHI**n) >= PHI * (1.0 - 1e-9):
        n += 1
    return n


class E3_5Experiment:
    """Registered as `e3.5` in the harness registry (P3.03, ADR-0006)."""

    name = "e3.5"
    hypothesis = (
        "phi positional s*phi^n arithmetic (exponent-add multiply, sign xor, "
        "per-power mass add, Fibonacci-carry normalization) is more "
        "computationally efficient than FP8/INT8 quantized arithmetic at a "
        "matched 8-bit budget, with an error-per-op advantage"
    )
    metric = "err-per-op (total MAC rel error / total ops, ingest-incl) + hist L1 + ops/result, 8-bit A/B vs FP8 and INT8"
    threshold = (
        "strict A/B at 8 bits/value: phi must win err-per-op by >=10% and not lose the "
        "histogram or ops axes; adopt or reject with a documented margin (P8)"
    )

    def run(self):
        from kainos.harness.runner import Result

        report = run_e3_5()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=report["per_format"]["phi"]["mac_err_per_op_ingest_incl"],
            threshold=self.threshold,
            evidence=[Path("results/phase-3/e3.5.json")],
            config={
                "verdict": report["verdict"],
                "verdict_note": report["verdict_note"],
                "phi_mac_err_per_op_ingest_incl": report["margins"]["phi_mac_err_per_op_ingest_incl"],
                "min_base_mac_err_per_op_ingest_incl": report["margins"]["min_base_mac_err_per_op_ingest_incl"],
                "phi_hist_l1": report["margins"]["phi_hist_l1"],
                "max_base_hist_l1": report["margins"]["max_base_hist_l1"],
                "phi_ops_per_result_ingest_incl": report["margins"]["phi_ops_per_result_ingest_incl"],
                "min_base_ops_per_result_ingest_incl": report["margins"]["min_base_ops_per_result_ingest_incl"],
                "bits_per_value": report["config"]["bits_per_value"],
                "seed": report["config"]["seed"],
            },
        )
