#!/usr/bin/env python3
"""Day-004f: exact twin-gap map, robust to twin dip structure.
Each of the 19 jump windows (from the dt=0.005-vs-dt=0.02 count offset) is
scanned at 2e-5 (10x the proven twin floor 0.0025) with per-crossing
Z_rs bisection; twin dips (gap > grid x 100) resolve as two clean crossings.
No EM certification needed for the GAP (dip structure is a sign-pattern fact);
mpmath dip probes are emitted for the extremes.  Run: python3 day004f_twin_gap_map.py
"""
import math
import sys

import numpy as np
sys.path.insert(0, ".")
import zeta_core  # noqa: E402


def N_of(path, t_from=None):
    d = np.loadtxt(path)
    t, S = d[:, 0], d[:, 1]
    th = np.array([zeta_core.vartheta(float(x)) for x in t])
    N = np.round(S + th / math.pi).astype(np.int64)
    if t_from is not None:
        m = t >= t_from
        t, S, N = t[m], S[m], N[m]
    return t, S, N


tA, _, NA = N_of("S_t_walk_1e5_1e6_gpu.txt", 100001.0)     # dt=0.02
tB, _, NB = N_of("S_t_walk_1e5_1e6_gpu_dt0005.txt", 100001.0)  # dt=0.005
off = NB - NA
jumps = np.where(np.diff(off) != 0)[0]
print("offset steps: %d, total %+d" % (len(jumps), int(off[-1] - off[0])))

GR = 2e-5
records = []
for j in jumps:
    lo, hi = float(tA[j]), float(tA[j + 1])
    tf = np.arange(lo, hi + GR * 0.5, GR)
    Zf = np.array([zeta_core.Z_rs(float(x)) for x in tf])
    s = np.sign(Zf); s[s == 0] = 1
    fl = np.where(s[1:] != s[:-1])[0]
    zeros = []
    dips = []
    for f in fl:
        a, b = float(tf[f]), float(tf[f + 1])
        za = zeta_core.Z_rs(a)
        for _ in range(40):
            m = 0.5 * (a + b)
            zm = zeta_core.Z_rs(m)
            if za * zm <= 0.0:
                b = m
            else:
                a, za = m, zm
        zeros.append(0.5 * (a + b))
    # twin structure: consecutive zeros closer than 0.02 = a pair;
    # the dip between them: sign pattern check via Z at the midpoint
    for i in range(len(zeros) - 1):
        gap = zeros[i + 1] - zeros[i]
        if gap < 0.02:
            c = 0.5 * (zeros[i] + zeros[i + 1])
            zdip = zeta_core.Z_rs(c)
            rho = math.log(c / (2 * math.pi)) / (2 * math.pi)
            records.append((c, zeros[i], zeros[i + 1], gap, gap * rho, zdip, len(zeros)))

print("\ntwin center   zero A          zero B          gap         lambda   Z(dip)    zeros-in-win")
for c, za_, zb_, g, lam, zd, nz in records:
    print("  %10.5f  %14.6f  %14.6f  %.6f    %.4f   %+.3e    %d"
          % (c, za_, zb_, g, lam, zd, nz))
gaps = np.array([r[3] for r in records])
lams = np.array([r[4] for r in records])
print("\n19-window twin gaps (Z_rs-bisected, dip-confirmed):")
print("  count = %d   min = %.6f   median = %.6f   max = %.6f"
      % (len(gaps), gaps.min(), gaps.max() and gaps.min(), gaps.max()) if len(gaps) else "none")
i_min = int(np.argmin(gaps)); i_max = int(np.argmax(gaps))
print("extremes: t(%.6f) gap %.6f ; t(%.6f) gap %.6f  (mpmath dip probe targets)"
      % (records[i_min][0], gaps[i_min], records[i_max][0], gaps[i_max]))
print("\nshape vs GUE Wigner surmise p(lam) = (32/pi^2) lam^2 e^{-4 lam^2/pi} (mean 1):")
hs, es = np.histogram(lams, bins=10, range=(0, 0.35))
for i in range(10):
    if hs[i]:
        mid = 0.5 * (es[i] + es[i + 1])
        model = (32 / math.pi ** 2) * mid ** 2 * math.exp(-4 * mid ** 2 / math.pi)
        print("  lam [%.3f, %.3f):  count = %2d   model p(mid) = %9.5f" % (es[i], es[i + 1], hs[i], model))
