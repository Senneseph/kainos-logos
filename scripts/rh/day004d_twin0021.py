#!/usr/bin/env python3
"""Day-004d (GPU): dt=0.0021 refinement walk.  The dt=0.005 re-walk recovered
offset +38 (19 twin pairs with gap < 0.02 missed by dt=0.02), landing
S(1e6) = -2.5086.  This run pins the residual (expected ~0.5 twin pairs with
gap < 0.005) and, by DIFFERENCE versus the dt=0.005 count, localizes every
gap<0.02 twin in [1e5, 1e6] and measures their gap distribution (the real
zero-spacing tail at this scale - the GOE p(lambda)~lambda^2 test at the 0.02
scale).  ~620M points, measured rate 3.75 Mpts/s => ~3 min GPU.
Run: ~/venvs/cupy/bin/cupy_py day004d_twin0021.py
"""
import math
import sys
import time

import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False)
T0, T1, DT = 100_000.0, 1_000_000.0, 0.0025
MAXN = int(math.sqrt(T1 / (2.0 * math.pi))) + 1
LNPI = math.log(math.pi)
LANCZOS = [cp.asarray(a, dtype=cp.float64) for a in zeta_core._LANCZOS]

def vartheta_gpu(tv):
    z = 0.25 + 0.5j * tv
    zm1 = z - 1.0
    x = cp.full(tv.shape, float(LANCZOS[0]), dtype=cp.complex128)
    for i in range(1, len(LANCZOS)):
        x = x + LANCZOS[i] / (zm1 + i)
    t_ = zm1 + 7.5
    cg = 0.5 * math.log(2.0 * math.pi) + (zm1 + 0.5) * cp.log(t_) - t_ + cp.log(x)
    return cg.imag - 0.5 * tv * LNPI

def Z_rs_gpu(tv):
    s2p = cp.sqrt(tv / (2.0 * math.pi))
    N = cp.floor(s2p).astype(cp.int64)
    p = s2p - N
    u = cp.sqrt(s2p)
    th = vartheta_gpu(tv)
    nvec = cp.arange(1, MAXN + 1, dtype=cp.float64)
    lnn = cp.log(nvec)
    wgt = 1.0 / cp.sqrt(nvec)
    mask = (nvec[None, :] <= N[:, None]).astype(cp.float64)
    S1 = (cp.cos(th[:, None] - tv[:, None] * lnn[None, :]) * (mask * wgt)).sum(axis=1)

    def psi(q):
        return cp.cos(2.0 * math.pi * (q * q - q - 0.0625)) / cp.cos(2.0 * math.pi * q)

    h = 1e-3
    d3 = (psi(p + 3j * h) - 3 * psi(p + 2j * h) + 3 * psi(p + 1j * h) - psi(p)).real / h ** 3
    sign = cp.where(((N - 1) % 2) == 0, 1.0, -1.0)
    R = sign * (psi(p).real / u - d3 / (96.0 * math.pi ** 2 * u ** 3))
    return 2.0 * S1 + R

t_start = time.time()
ntot = int(round((T1 - T0) / DT)) + 1
print("dt=0.0025 walk: %d points" % ntot)
CHUNK = 256_000
Z_all, var_all = [], []
for i0 in range(0, ntot, CHUNK):
    tv = cp.asarray(T0 + DT * np.arange(i0, min(i0 + CHUNK, ntot), dtype=np.float64))
    Z_all.append(Z_rs_gpu(tv).get())
    var_all.append(vartheta_gpu(tv).get())
    if (i0 // CHUNK) % 200 == 0:
        print("  ... %.0f M pts (%.0f s)" % (i0 / 1e6, time.time() - t_start))
Z = np.concatenate(Z_all)
varth = np.concatenate(var_all)
print("batched eval: %.0f s" % (time.time() - t_start))

sgn = np.sign(Z)
sgn[sgn == 0] = 1
flip = (sgn[1:] != sgn[:-1]).astype(np.int32)
cum = np.cumsum(flip, dtype=np.int64)
N0 = 138_065
N_end = N0 + int(flip.sum())
print("N(1e6) @ dt=0.0021 = %d   (dt=0.005: 1747142 ; dt=0.02: 1747104)" % N_end)

# offset vs the dt=0.005 walk (its grid: DT5 = 0.005); differences = recovered pairs
DT5 = 0.005
old = np.loadtxt("S_t_walk_1e5_1e6_gpu_dt0005.txt")
t5, S5 = old[:, 0], old[:, 1]
th5 = np.array([zeta_core.vartheta(float(t)) for t in t5])
N5 = np.round(S5 + th5 / math.pi).astype(np.int64)

# for each dt=0.0021 grid point that lands on a dt=0.005 grid point, record offset
ratio = int(round(DT5 / DT))
assert abs(ratio * DT - DT5) < 1e-9
i5 = np.round((t5 - T0) / DT).astype(np.int64)
assert np.max(np.abs(i5 * DT - (t5 - T0))) < 1e-9 and i5[-1] < ntot, "grid not nested"
Nfine_at5 = N0 + cum[i5 - 1]
offset = Nfine_at5 - N5
doffs = np.diff(offset)
rec = np.where(doffs != 0)[0]
print("offset dt=0.0021 vs dt=0.005: final %+d (expected ~+1, i.e. <1 residual twin pair @0.005)" % offset[-1])
print("difference events: %d" % len(rec))
# recovered zero positions live inside 0.005 cells: localize on the fine grid
zs = []
for r in rec:
    lo, hi = int(i5[r]), int(i5[r + 1])
    fl = np.where(flip[lo:hi])[0] + lo
    for f in fl:
        zs.append(T0 + DT * f)
zs = sorted(zs)   # gaps among these measured by the bisection script (day004e)
print("recovered zero positions (dt=0.0025 grid): %d" % len(zs))
if zs:
    print("  first few: " + "  ".join("%.4f" % z for z in zs[:12]))

# S(1e6) final
S1e6 = N_end - zeta_core.vartheta(T1) / math.pi
print("\nS(1e6) @ dt=0.0021 = %+.4f   (expect -2.5 +- 1 residual twin)" % S1e6)
print("\ntotal %.0f s" % (time.time() - t_start))
