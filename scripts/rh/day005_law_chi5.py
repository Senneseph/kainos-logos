#!/usr/bin/env python3
"""Day-005 (FUSION experiment): the missing-term law for L(s, chi_5).
The zeta law (day-004, measured): tail_zeta = zeta - P_N = -I + second order,
|I| = sqrt(N)/|1-s| (GROWING on the line - the series is on the divergent
side of sigma=1).  The chi_5 series converges on the line: the predicted
dual: tail_chi = sum_{n>N} chi(n) n^{-s} ~ -A(N) N^{-s} (FIRST order, where
A(N) = sum_{n<=N} chi(n) is the bounded periodic partial-sum residue,
values in {0, +/-1, +/-2, ...} stepping with N mod 5; size O(N^{-1/2}),
DECAYING), with a second order O(N^{-1/2 - 1}) analog.
Measures: T0 = |L - P_N| (should decay ~ N^{-1/2}),
          T1 = |L - P_N + A(N) N^{-s}| (should decay faster),
          T1/T0 (chi-version of the day-004 T1/T0 = 2.000 identity).
If the half-power + first-order-removal structure survives with the
character-modulated boundary term, the law is structural to Euler
continuations beyond zeta.  Run: python3 day005_law_chi5.py
"""
import math
import sys
import time

import numpy as np
sys.path.insert(0, "/home/jsmille/Projects/kainos-logos/scripts/rh")
t_start = time.time()

CHI5 = np.array([0, 1, -1, -1, 1], dtype=np.float64)  # chi_5(n) = (5/n), n=0..4 pattern


def chi5_vec(N):
    j = np.arange(N)                       # 0-based index j represents n = j+1
    return CHI5[(j + 1) % 5].astype(np.float64)   # chi_5(n) = CHI5[n mod 5]


def L5_block(t, M):
    """L(s, chi_5) via 5-period blocks: sum_m [ (5m+1)^-s + (5m+4)^-s
    - (5m+2)^-s - (5m+3)^-s ], m = 0..M-1 (covers n = 1..5M)."""
    s = complex(0.5, t)
    m = np.arange(M, dtype=np.float64)
    vals = []
    for r, cc in ((1, 1.0), (2, -1.0), (3, -1.0), (4, 1.0)):
        x = 5.0 * m + r
        vals.append(cc * np.exp(-s * np.log(x)))
    return complex(np.sum(np.array(vals)))


def power_fit(Ns, Ts):
    b, a = np.polyfit(np.log(Ns), np.log(np.maximum(Ts, 1e-300)), 1)
    return a, b   # T ~ a * N^b


NMAX = 100_000
c = chi5_vec(NMAX)
logs = np.log(np.arange(1, NMAX + 1, dtype=np.float64))
Ngrid = np.unique((10 ** np.linspace(2.0, 5.0, 51)).astype(int))

for t in (1.0, 10.0, 100.0, 1000.0, 1e4):
    s = complex(0.5, t)
    base = c * np.exp(-s * logs)
    cum = np.concatenate(([0.0], np.cumsum(base)))
    Mref = 5_000_000                     # n = 1..2.5e7
    L1 = L5_block(t, 2_000_000)          # n = 1..1e7
    L2 = L5_block(t, 4_000_000)          # n = 1..2e7
    L4 = L5_block(t, 5_000_000)          # n = 1..2.5e7
    conv = abs(L4 - L2), abs(L2 - L1)    # empirical convergence scale
    Lref = L4
    T0 = np.array([abs(Lref - cum[int(n)]) for n in Ngrid])
    def _A(N):
        # A(N) = sum_{n<=N} chi(n): full periods sum to 0, so A(N) = sum of the
        # first rem residues of the period (periodic residue function)
        rem = int(N) % 5
        return float(CHI5[1:rem + 1].sum())   # sum of residues 1..rem
    A_N = np.array([_A(int(n)) for n in Ngrid])
    T1 = np.array([abs(Lref - cum[int(Ngrid[i])] + A_N[i] * (Ngrid[i] ** -s)) for i in range(len(Ngrid))])
    a0, b0 = power_fit(Ngrid, T0)
    m1 = T0 > 0
    a1, b1 = power_fit(Ngrid[m1], T1[m1])
    ratio = np.where(T0 > 0, T1 / np.maximum(T0, 1e-300), np.nan)
    print("t = %8.0f  (ref convergence: |L(2.5e7)-L(2e7)| = %.2e, |L(2e7)-L(1e7)| = %.2e)"
          % (t, conv[0], conv[1]))
    print("  T0 = |L - P_N| ~ %.2e * N^(%.3f)    [zeta law face: would be N^{+0.5}/|1-s|]"
          % (a0, b0))
    print("  T1 = T0 + A(N)N^{-s} ~ %.2e * N^(%.3f)    [first-order removal]" % (a1, b1))
    print("  T1/T0 at N = 1e2/1e3/1e4/1e5: %.3f %.3f %.3f %.3f"
          % (ratio[0], ratio[len(Ngrid) // 4], ratio[3 * len(Ngrid) // 4], ratio[-1]))
    print("  A(N) sequence over N mod 5: %s" % ["%.0f" % _A(k) for k in (1, 2, 3, 4, 5)])
print("\ntotal %.0f s" % (time.time() - t_start))
