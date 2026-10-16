#!/usr/bin/env python3
"""Day-004 E1: the missing-term (tail) experiment, batched on GPU (cupy/ROCm).

Owner's question, made measurable: "does the truncated series need the
previous/next terms in relation to the current?"  For the Dirichlet
partial sum P_N(s) = sum_{n<=N} n^{-s} (valid, sigma>1), the MISSING tail
R(s; N) = zeta(s) - P_N(s) is the answer, and it decomposes:

    R(s; N) = [smooth integral continuation: N^{1-s}/(1-s) + 0.5 n^{-s} terms]
             + [the zero-oscillation remainder]

We measure, on a BATCHED (sigma, t) grid (the pattern where cupy wins,
benchmarked 1240x on out_bench_cupy.txt):

  T0 = |zeta(s) - P_N(s)|                       raw tail (what is missing)
  T1 = |R after subtracting N^{1-s}/(1-s) - 0.5*s^{-1} N^{-s}_style 1st order|
       first-order-missing subtracted -> second-order (zero-driven) part

Grid: sigma in [0.3, 1.4] x t = fixed rows {gamma_1, between-gamma, gamma_2,
50, 1000, 50000 (on-line scale), 99999.7 (a 1e5-list zero)}.

Predictions to test (labeled):
  (P1) T0 shrinks as sigma -> 1 for all t (sigma>1 converges): MEASURED.
  (P2) T1 << T0 for large N: the FIRST-ORDER "next term" (the integral)
       captures most of the missing tail: MEASURED (this is the owner's
       'previous/next term' in the series, made real).
  (P3) The residual T1 at sigma < 1 is DOMINATED by the nearest zero: rows
       AT a zero should show a larger / structurally different T1 than rows
       BETWEEN zeros, with the zero's row resonating: MEASURED (the pattern
       of T1(sigma) at t = gamma_k vs t = between).
Run under the cupy venv python (~/venvs/cupy) with LD_LIBRARY_PATH=/opt/rocm/lib.
"""
import math
import os
import sys
import time

import numpy as np
import zeta_core  # CPU engine for the zeta values (verified vs mpmath)

HAVE_CP = False
try:
    os.environ.setdefault("LD_LIBRARY_PATH", "/opt/rocm/lib")
    import cupy as cp
    HAVE_CP = True
except Exception:
    pass
print("gpu:", "cupy", cp.__version__ if HAVE_CP else "UNAVAILABLE (CPU path)")

N = 10_000
nn = np.arange(1, N + 1, dtype=float)
lnN = np.log(nn)

sigmas = np.linspace(0.30, 1.40, 111)          # 201 points per row
rows = {
    "gamma1=14.1347": 14.13472514173469,
    "between12=(22.58)": 22.57838238235312,
    "gamma2=21.0220": 21.02203963877155,
    "t=50": 50.0,
    "t=1000": 1000.0,
    "t=50000": 50_000.0,
    "t=99999.70(1e5 zero)": 99_999.700948,
}

def zeta_cpu(s_arr):  # vectorized EM batch (host, exact to ~1e-11 scale)
    return np.array([zeta_core.zeta(s) for s in s_arr])

def tail_rows(sigma_row, t_row):
    s = sigma_row + 1j * t_row
    # batched P_N(s) on GPU (pattern B from bench_cupy_numpy.py)
    if HAVE_CP:
        s_cp = cp.asarray(sigma_row)
        ln_cp = cp.asarray(lnN)
        E = cp.exp(-s_cp[:, None] * ln_cp[None, :] - 1j * t_row * ln_cp[None, :])
        PN = cp.einsum('ij->i', E).get()
        zc = zeta_cpu(sigma_row + 1j * t_row)
    else:
        E = np.exp(-sigma_row[:, None] * lnN[None, :] - 1j * t_row * lnN[None, :])
        PN = np.einsum('ij->i', E)
        zc = zeta_cpu(sigma_row + 1j * t_row)
    T0 = np.abs(zc - PN)
    # first-order "next-term" (Euler-Maclaurin 1st order): integral from N
    first = N ** (1 - s) / (1 - s)
    T1 = np.abs(zc - PN - first)
    return T0, T1

t_start = time.time()
print("%-22s %8s %8s %10s %10s" % ("row", "sig", "|T0|", "|T1|", "T1/T0"))
for name, tv in rows.items():
    T0, T1 = tail_rows(sigmas, tv)
    for i in (0, 22, 44, 66, 88, 110):
        ratio = T1[i] / T0[i] if T0[i] > 0 else float("nan")
        mark = " <-- Z" if name.startswith(("gamma", "between")) and i in (44, 66) else ""
        print("%-22s %8.3f %10.4e %10.4e %8.3f%s" % (name, sigmas[i], T0[i], T1[i], ratio, mark))
    print()
print("batch time for %d rows x %d sigmas: %.1f s" % (len(rows), len(sigmas), time.time() - t_start))

# key numbers: the ratio T1/T0 per row as a function of sigma
print("P1 check (T0 at t=1000): sigma=0.3: %.3e  sigma=1.0: %.3e  sigma=1.4: %.3e"
      % tuple(tail_rows(sigmas[[0, 89, 110]], 1000.0)[0]))
