#!/usr/bin/env python3
"""Day-018 T4 pre-gate (oracle side).

Mechanically checks, in float64, that the 15 MEASURED onset ratios
(out_day004b_onset.txt, day-04b, N x t/N grid) sit inside the explicit
T4 interval [0.5*||s||/n - err, 0.5*||s||/n + err] of the P4 abstract
spec (spec/p4-tail-law-abstract.md, section T4):

    s = 1/2 + i t,  ||s|| = sqrt(t^2 + 1/4)
    center = 0.5 * ||s|| / n
    err(t,n) = (t^2 + 1/4) / (12 n^2) + (sqrt(3)/216) * (t^2 + 1/4) * (||s||+1) / n^3

The interval is the disk the data must sit inside after the second-order
EM form W_n = -1/2 n^{-s} + (s/12) n^{-s-1} + R_{n,1}, |R| bounded by the
OP2 lemma constant — every factor explicit, no fit, no free phase.

Oracle status: closed-form float64 (numpy not required). This is the
independent numeric witness of the P4 line; the Lean P4Float gate is
the theorem-level consumer. Constants computed here, not recalled.

Writes out_day018_t4_pregate.txt.
"""
import math

ONSET = "out_day004b_onset.txt"
OUT = "out_day018_t4_pregate.txt"

N_SET = (1000, 10000, 100000)
FRACTIONS = (0.1, 0.2, 0.5, 1.0, 2.0)


def t4_interval(t, n):
    norm_s = math.sqrt(t * t + 0.25)
    center = 0.5 * norm_s / n
    err = (t * t + 0.25) / (12.0 * n * n) + (
        math.sqrt(3.0) / 216.0
    ) * (t * t + 0.25) * (norm_s + 1.0) / (n * n * n)
    return center - err, center, center + err


def main():
    # parse the measured table (columns: N, t, |I|, C, C/|I|, r)
    measured = {}
    with open(ONSET) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 5 or parts[0] in ("N",):
                continue
            try:
                n = int(float(parts[0]))
                t = float(parts[1])
                ratio = float(parts[4])
            except ValueError:
                continue
            if n not in N_SET:
                continue
            frac = t / n
            for target in FRACTIONS:
                if abs(frac - target) <= 1e-9:
                    measured[(n, frac)] = (t, ratio)
    assert len(measured) == 15, f"expected 15 measured points, got {len(measured)}: {sorted(measured)}"

    lines = []
    lines.append("# Day-018 T4 pre-gate (oracle, float64 closed form)")
    lines.append("# P4 spec T4: measured C/|I| in [0.5||s||/n - err, 0.5||s||/n + err]")
    lines.append("# source data: out_day004b_onset.txt (measured, day-04b, GPU)")
    lines.append(f"{'N':>8} {'frac':>5} {'t':>12} {'meas':>10} {'center':>12} "
                 f"{'err':>12} {'margin%':>9}")
    n_pass = 0
    for n in N_SET:
        for frac in FRACTIONS:
            t, meas = measured[(n, frac)]
            lo, center, hi = t4_interval(t, float(n))
            inside = bool(lo <= meas <= hi)
            margin_pct = ((min(meas - lo, hi - meas) / center) * 100.0) if center > 0 else float("nan")
            n_pass += 1 if inside else 0
            lines.append(
                f"{n:>8d} {frac:>5.1f} {t:>12.1f} {meas!r} {center:.17g} "
                f"{(hi - lo) / 2:.17g} {margin_pct:>8.2f}%{'  PASS' if inside else '  *** FAIL ***'}"
            )
    # the five width-per-ratios rows the spec hand-derived (spec T4; absolute,
    # percentage points of the ratio); N=1000 row for reference
    lines.append("# width per t/N (spec hand-claim: 0.09% / 0.34% / 2.2% / 9.1% / 40% at N-independent scale):")
    for frac in FRACTIONS:
        t = 1000.0 * frac
        n = 1000.0
        lo, center, hi = t4_interval(t, n)
        lines.append(f"  t/N={frac:<4.1f} err(abs)={((hi - lo) / 2):.17g}  err_pct_of_ratio={(hi - lo) / 2:.2%}")
    lines.append(f"PASS {n_pass}/15 containment")
    text = "\n".join(lines) + "\n"
    with open(OUT, "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
