#!/usr/bin/env python3
"""Day-009: twin-safe corrective GPU re-walk of [1e4, 1.9e4].

WHY: the original day-003/004 CPU walk (S_t_walk_1e4_1e5.txt, dt = 0.1)
is defective — sampled above the twin floor, it misses flip pairs; its
S_file collapses to ~-45 on [1.02e4, 1.85e4] (~22 missed twin events,
22*2 = 44 count deficit). This re-walk at dt = 2.5e-4 (200x below the
smallest measured gap in the window, computed from the certified zero
list) is the twin-safe S_file for the E7b-1 bridge test.

Also carries the DAY-007 d3 fix: psi'''(p) = -Im[S3]/h^3 (complex step,
the legacy Re[S3]/h^3 was an O(h*psi'''') residual). The 1e6->1e7 GPU
walk ran pre-fix; this one runs post-fix (host zeta_core selftest +
goldens gate first).

Run: ~/venvs/cupy/bin/cupy_py day009_s_walk_1e4_1p9e4_gpu.py
"""
import math
import sys
import time

import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False), "zeta_core selftest failed"

T0, T1, DT = 10_000.0, 19_000.0, 2.5e-4
MAXN = int(math.sqrt(T1 / (2.0 * math.pi))) + 1
LNPI = math.log(math.pi)
LANCZOS = [cp.asarray(a, dtype=cp.float64) for a in zeta_core._LANCZOS]
ntot = int(round((T1 - T0) / DT)) + 1

# N0 from the certified zero list (exact integer)
gammas = np.loadtxt("zeros_T100000.txt")
N0 = int(np.searchsorted(gammas, T0))
print("N(1e4) from zero list =", N0)

# twin floor in the window (from the same zero list)
inside = gammas[(gammas > T0) & (gammas < T1)]
gaps = np.diff(inside)
gmin = float(gaps.min())
print("zeros in window:", len(inside), " min gap:", gmin,
      " dt/gmin =", DT / gmin)
assert DT < gmin / 10.0, "dt not safely below the twin floor"

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
    S3 = (psi(p + 3j * h) - 3 * psi(p + 2j * h) + 3 * psi(p + 1j * h) - psi(p))
    d3 = -S3.imag / h ** 3          # DAY-007 FIX (-Im[S]/h^3, not Re)
    sign = cp.where(((N - 1) % 2) == 0, 1.0, -1.0)
    R = sign * (psi(p).real / u - d3 / (96.0 * math.pi ** 2 * u ** 3))
    return 2.0 * S1 + R

# sanity: engine vs host at a few scattered points (post-fix both sides)
vt = np.linspace(T0 + 3.7, T1 - 3.7, 12)
vg = Z_rs_gpu(cp.asarray(vt, dtype=cp.float64)).get()
vc = np.array([zeta_core.Z_rs(float(x)) for x in vt])
err = float(np.abs(vg - vc).max())
print("GPU-vs-host Z_rs (post-fix d3): max |diff| = %.3e" % err)
assert err < 1e-6, "Z_rs mismatch — abort"

def walk(dt, tag):
    t_start = time.time()
    steps = int(round((T1 - T0) / dt)) + 1
    CHUNK = 128_000
    cum = 0
    z_prev = None
    rows = []
    for i0 in range(0, steps, CHUNK):
        i1 = min(i0 + CHUNK, steps)
        tv = cp.asarray(T0 + dt * np.arange(i0, i1, dtype=np.float64))
        Z = Z_rs_gpu(tv).get()
        varth = vartheta_gpu(tv).get()
        sgn = np.sign(Z); sgn[sgn == 0] = 1
        if z_prev is not None:
            seg = np.concatenate(([z_prev], sgn))
            flips = (seg[1:] != seg[:-1]).astype(np.int64)
        else:
            flips = np.zeros(len(sgn), dtype=np.int64)
        pref = np.cumsum(flips)
        cum_before = cum
        N_at = N0 + cum_before + pref
        S_at = N_at - varth / math.pi
        tf = T0 + dt * np.arange(i0, i1)
        rows.append(np.stack([tf, S_at], axis=1))
        cum = cum_before + int(pref[-1])
        z_prev = int(sgn[-1])
    arr = np.vstack(rows)
    N_end = N0 + cum
    el = time.time() - t_start
    print("[%s] dt=%.1e: N(1.9e4) = %d  (new zeros: %d)  elapsed %.1f s"
          % (tag, dt, N_end, N_end - N0, el))
    return arr, N_end

arr_dt, N_dt = walk(DT, "dt")
arr_dh, N_dh = walk(DT / 2, "dt/2")
ag = N_dt == N_dh
print("[stability] dt vs dt/2 flip counts agree: %s  (N: %d vs %d)"
      % (ag, N_dt, N_dh))
np.savetxt("S_t_walk_1e4_1p9e4_gpu_dt00025.txt", arr_dt,
           fmt="%.12e %+.9f")
S_first = float(arr_dt[0, 1]); S_last = float(arr_dt[-1, 1])
Smin = float(arr_dt[:, 1].min()); Smax = float(arr_dt[:, 1].max())
amax = float(np.abs(arr_dt[:, 1]).max())
print("S_file(1e4)=%.4f  S_file(1.9e4)=%.4f" % (S_first, S_last))
print("max|S| on window = %.4f   (min %+.4f / max %+.4f)"
      % (amax, Smin, Smax))
print("written S_t_walk_1e4_1p9e4_gpu_dt00025.txt (%d rows)" % len(arr_dt))
