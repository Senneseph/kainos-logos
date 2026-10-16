#!/usr/bin/env python3
"""Day-004 continuation (GPU): the second-order ZERO-ONSET crossover.

From the day-004 missing-term law: tail = -I(s) + (second order), with
I(s) = N^{1-s}/(1-s) the first-order "next term".  The zeros live in the
second order; the day-004 grid measured the ONSET between t = 1e3 and
5e4 at N = 1e4 (T1/T0: 2.000 -> 0.821).  This run pins the crossover on
the scale t/N:

    for N in {1e3, 1e4, 1e5}  and  t = N * {0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50}:
      A = |I|                                  first-order size
      C = |tail + I|                           second-order size (after removal)
      r = |tail - I| / |tail|                  (2.000 = first-order exact, -> 1.0 = first-order dead)
    onset := t/N where C becomes comparable to A.
Run: ~/venvs/cupy/bin/cupy_py day004b_onset.py
"""
import math
import sys
import time

import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False)
t_start = time.time()

Ns = (10 ** 3, 10 ** 4, 10 ** 5)
tfracs = (0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0)

print("%-8s %-12s %10s %10s %10s %10s" % ("N", "t (N*frac)", "|I|", "C(2nd ord)", "C/|I|", "r=T1/T0"))
onsets = []
for Nn in Ns:
    nn = cp.arange(1, Nn + 1, dtype=cp.float64)
    lnn = cp.log(nn)
    maxt = Nn * tfracs[-1]
    MAXN0 = int(math.sqrt(maxt / (2.0 * math.pi))) + 1  # not needed here (P_N is N terms, fixed)
    for f in tfracs:
        tv = Nn * f
        s = 0.5 + 1j * tv
        I = Nn ** (1 - s) / (1 - s)                       # first order
        zt = zeta_core.zeta(s)
        Pn = (cp.exp(-0.5 * lnn) * cp.exp(-1j * tv * lnn)).sum()
        tail = zt - Pn
        A = abs(I)
        C = abs(tail + I)                                  # second order (after removing -I)
        R0 = abs(tail)
        r = abs(tail - I) / R0
        mark = ""
        if A > 0 and 0.4 < C / A < 2.5:
            mark = "   <-- onset band"
        print("%-8d %-12.5g %10.4e %10.4e %10.4f %10.4f%s" % (Nn, tv, A, C, C / A if A else 0.0, r, mark))
        if C > A * 0.4 and not onsets:
            pass
print("\n(reading: r = 2.000 means tail = -I exactly (first order owns the tail);\n"
      " C/|I| ~ 1 means the second-order zero-oscillation is comparable to the first order;\n"
      " r -> 1.0 means the first order is dead.)")
print("\ntotal %.1f s" % (time.time() - t_start))
