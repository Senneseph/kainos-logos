#!/usr/bin/env python3
"""Day-004e: exact localization of the 19 twin pairs missed by the dt=0.02
S(1e6) walk.  The +2 steps of the (dt=0.005 count) - (dt=0.02 count) offset
mark the twin windows (1.0-rad resolution); each window is re-walked at
dt=0.0001 with the VERIFIED Day-003 census refine pattern: 16 RS bisections
+ EM gate + 26 EM bisections, certified |zeta| < 1e-7.  Outputs the exact
twin gaps and the GOE Wigner-surmise (p ~ lambda^2) shape comparison.
Run: python3 day004e_twin_localize.py
"""
import math
import sys
import time

import numpy as np
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

# FIX: EM term cap (80k, day-003 sized) truncates too early at t > ~1.03e5;
# raise it for [1e5, 1e6] certification (M(1e6) = 0.78t+30 = 780,060).
zeta_core._NMAX = 1_200_000
assert zeta_core.selftest(verbose=False)
t_start = time.time()


def refine(lo_i, hi_i, zp_i):
    """Day-003 census refine (verified): RS bisection + EM gate + EM bisection."""
    lo, hi, zp = lo_i, hi_i, zp_i
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        zm = zeta_core.Z_rs(mid)
        if zp * zm <= 0.0:
            hi = mid
        else:
            lo, zp = mid, zm
    tc = 0.5 * (lo + hi)
    if abs(zeta_core.Z(tc)) < 1e-4:
        a, b = tc - 1e-4, tc + 1e-4
    else:
        a, b = lo_i, hi_i
    za, zb = zeta_core.Z(a), zeta_core.Z(b)
    if za * zb > 0.0:
        return None
    for _ in range(26):
        mid = 0.5 * (a + b)
        zm = zeta_core.Z(mid)
        if za * zm <= 0.0:
            b = mid
        else:
            a, za = mid, zm
    t0 = 0.5 * (a + b)
    zv = abs(zeta_core.zeta(0.5 + 1j * t0))
    if zv >= 1e-7:
        print("  WARN |zeta| = %.2e at t = %.6f (EM cap?) - skipped" % (zv, t0))
        return None
    return t0


def N_of(path):
    d = np.loadtxt(path)
    t, S = d[:, 0], d[:, 1]
    th = np.array([zeta_core.vartheta(float(x)) for x in t])
    return t, np.round(S + th / math.pi).astype(np.int64)


tA, NA = N_of("S_t_walk_1e5_1e6_gpu.txt")        # dt=0.02 counts (t from 100001)
tB, NB = N_of("S_t_walk_1e5_1e6_gpu_dt0005.txt")  # dt=0.005 counts (t from 100000)
m = tB >= tA[0]
tB, NB = tB[m], NB[m]
off = NB - NA
doff = np.diff(off)
jumps = np.where(doff != 0)[0]
print("offset steps: %d, total %+d" % (len(jumps), int(off[-1] - off[0])))

twins = []
for j in jumps:
    lo, hi = float(tA[j]), float(tA[j + 1])
    tf = np.arange(lo, hi + 1e-9, 0.0001)
    Zf = np.array([zeta_core.Z_rs(float(x)) for x in tf])
    s = np.sign(Zf); s[s == 0] = 1
    fl = np.where(s[1:] != s[:-1])[0]
    zeros = []
    for f in fl:
        z = refine(float(tf[f]), float(tf[f + 1]), float(Zf[f]))
        if z is not None:
            zeros.append(z)
    if len(zeros) >= 2:
        for i in range(len(zeros) - 1):
            gap = zeros[i + 1] - zeros[i]
            if gap < 0.02:
                rho = math.log(0.5 * (lo + hi) / (2 * math.pi)) / (2 * math.pi)
                twins.append((0.5 * (lo + hi), gap, gap * rho, len(zeros)))

print("\ntwin center    gap         scaled (GOE units)   zeros-in-window")
for c, g, lam, nz in twins:
    print("  %11.3f   %.6f     %.5f                     %d" % (c, g, lam, nz))
gaps = np.array([x[1] for x in twins])
lams = np.array([x[2] for x in twins])
print("\nmeasured twin gaps (EM-certified |zeta|<1e-7):")
print("  count = %d   min = %.6f   median = %.6f   max = %.6f"
      % (len(gaps), gaps.min(), np.median(gaps), gaps.max()))

print("\nshape vs GUE Wigner surmise p(lam) = (32/pi^2) lam^2 e^{-4 lam^2/pi} (mean 1):")
hs, es = np.histogram(lams, bins=10, range=(0, 0.3))
for i in range(10):
    mid = 0.5 * (es[i] + es[i + 1])
    model = (32 / math.pi ** 2) * mid ** 2 * math.exp(-4 * mid ** 2 / math.pi)
    print("  lam [%.3f, %.3f):  count = %2d   model p = %9.5f" % (es[i], es[i + 1], hs[i], model))
print("\ntotal %.0f s" % (time.time() - t_start))
