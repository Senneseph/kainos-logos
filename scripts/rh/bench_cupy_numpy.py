#!/usr/bin/env python3
"""CuPy (ROCm gfx1151) vs numpy benchmark on the RH workloads.

A: single-t RS main sum (N = 400 and 40000 terms): sequential-walk pattern.
B: batched grid: 2000 points x 20000 terms power-sum matrix (E1 pattern).
Everything TIMED on this machine (no assumed speedups).
"""
import math
import time

import numpy as np

try:
    import cupy as cp
    HAVE_CP = True
except ImportError:
    HAVE_CP = False

def t_mean(fn, n=50):
    fn()
    a = time.time()
    for _ in range(n):
        fn()
    return (time.time() - a) / n

if HAVE_CP:
    print("cupy device:", cp.cuda.runtime.getDeviceProperties(0)['name'])

# ---------- A: single-t main sum ----------
for N in (400, 40000):
    n_np = np.arange(1, N + 1, dtype=float)
    ln_np = np.log(n_np)
    t_rs = 12345.678

    def np_one():
        return np.cos(t_rs - ln_np).dot(n_np ** -0.5)
    t_np = t_mean(np_one, 200)

    if HAVE_CP:
        n_cp = cp.arange(1, N + 1, dtype=cp.float64)
        ln_cp = cp.log(n_cp)
        s_cp = cp.sqrt(n_cp)

        def cp_one():
            return float((cp.cos(t_rs - ln_cp) / s_cp).sum())
        t_cp = t_mean(cp_one, 200)
    print("A: single sum N=%6d :  numpy %8.1f us   cupy %8.1f us   (%.2fx %s)"
          % (N, t_np * 1e6, t_cp * 1e6 if HAVE_CP else float('nan'),
             t_cp / t_np if HAVE_CP else float('nan'), "cupy faster" if HAVE_CP and t_cp < t_np else "numpy faster"))

# ---------- B: batched grid ----------
NP, NT = 2000, 20000
sigma = np.linspace(0.3, 1.2, NP)
tt = np.linspace(1000, 2000, NP)
lnN = np.log(np.arange(1, NT + 1, dtype=float))

def np_batch():
    E = np.exp(-sigma[:, None] * lnN[None, :] - 1j * tt[:, None] * lnN[None, :])
    return np.einsum('ij->i', E)
E_np = None
t_npB = t_mean(np_batch, 5)

if HAVE_CP:
    s_cp = cp.asarray(sigma)
    t_cp_ = cp.asarray(tt)
    lnN_cp = cp.asarray(lnN)

    def cp_batch():
        E = cp.exp(-s_cp[:, None] * lnN_cp[None, :] - 1j * t_cp_[:, None] * lnN_cp[None, :])
        return cp.einsum('ij->i', E)
    v_np = np_batch()
    v_cp = cp_batch().get()
    diff = float(np.max(np.abs(v_np - v_cp)))
    t_cpB = t_mean(cp_batch, 10)
    print("B: batch %4dx%5d :  numpy %8.0f ms   cupy %8.0f ms   (%.1fx %s)   max|diff| = %.2e"
          % (NP, NT, t_npB * 1e3, t_cpB * 1e3, t_npB / t_cpB,
             "cupy faster" if t_cpB < t_npB else "numpy faster", diff))

print("\nVERDICT: use cupy for B (batched independent points) if >3x; A stays numpy if transfer-bound.")
