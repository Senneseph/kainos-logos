#!/usr/bin/env python3
"""Day-005: S(t) walk 1e6 -> 1e7 at the TWIN-FLOOR budget dt = 5e-4
(projected minimum twin gap at 1e7 ~ 9e-4, from the 0.003 floor at 1e6
scaled by the density trend; dt = 5e-4 is ~2x below it).  Streaming:
per-chunk flip bookkeeping on host, S sampled every 1.0 rad, per-decade
stats inline (no 144 GB Z array).  Validates the GPU port against the
CPU Z_rs at 1e7 scale first (2-term RS engine range check).
~80 min GPU at the measured 3.75 Mpts/s.
Run: ~/venvs/cupy/bin/cupy_py day005_s_walk_1e7.py
"""
import math
import sys
import time

import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False)

T0, T1, DT = 1_000_000.0, 10_000_000.0, 5e-4
N0 = 1_747_142                      # N(1e6), verified day-004 (3 resolutions + 2K)
MAXN = int(math.sqrt(T1 / (2.0 * math.pi))) + 1   # floor(sqrt(t/2pi)) at 1e7 = 1261
LNPI = math.log(math.pi)
LANCZOS = [cp.asarray(a, dtype=cp.float64) for a in zeta_core._LANCZOS]
ntot = int(round((T1 - T0) / DT)) + 1
print("MAXN = %d ; ntot = %d points (projected ~%.0f s at 3.75 Mpts/s)"
      % (MAXN, ntot, (T1 - T0) / DT / 3.75e6))

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

# ---- validation at 1e7 scale (GPU vs CPU Z_rs, 200 scattered points) ----
vt = np.linspace(3.5e6, 9.9e6, 200)
vg = Z_rs_gpu(cp.asarray(vt, dtype=cp.float64)).get()
vc = np.array([zeta_core.Z_rs(float(x)) for x in vt])
err = float(np.abs(vg - vc).max())
print("GPU-vs-CPU Z_rs at 1e7 scale: max |diff| = %.3e over 200 pts" % err)
warn = err > 1e-4
if warn:
    print("WARN: 2-term RS error > 1e-4 at 1e7 -- flip counts near twin dips (~4e-5)")
    print("      are NOT trusted; stats are upper-bound only. Do not quote counts.")

t_start = time.time()
CHUNK = 256_000
SAMPLE = int(round(1.0 / DT))        # S sampled every 1.0 rad
cum_flips = 0
z_prev = None
ND = 9   # [1e6,1e7] in 1e6 bins: [1e6,2e6) ... [9e6,1e7]
dec = [dict(lo=(1 + i) * 1e6, hi=(2 + i) * 1e6 if i < ND - 1 else 1e7,
            mx=0.0, mn=1e30, mxS=-1e30, acc=0.0, cnt=0) for i in range(ND)]
samps = []
t_last = None
for i0 in range(0, ntot, CHUNK):
    i1 = min(i0 + CHUNK, ntot)
    tv = cp.asarray(T0 + DT * np.arange(i0, i1, dtype=np.float64))
    Z = Z_rs_gpu(tv).get()
    varth = vartheta_gpu(tv).get()
    tf = T0 + DT * np.arange(i0, i1)
    sgn = np.sign(Z); sgn[sgn == 0] = 1
    if z_prev is not None:
        seg = np.concatenate(([z_prev], sgn))
        flips = (seg[1:] != seg[:-1]).astype(np.int64)
    else:
        flips = np.zeros(len(sgn), dtype=np.int64)
    pref = np.cumsum(flips)
    cum_before = cum_flips
    N_at = N0 + cum_before + pref
    S_at = N_at - varth / math.pi
    # per-decade stats from the 1.0-rad samples
    idx = range(0, len(sgn), SAMPLE)
    for k in idx:
        t_ = float(tf[k]); S_ = float(S_at[k])
        samps.append((t_, S_))
        d = int((t_ - 1e6) // 1e6)
        if d < 0: d = 0
        if d > ND - 1: d = ND - 1
        dd = dec[d]
        if abs(S_) > dd["mx"]: dd["mx"] = abs(S_)
        if S_ > dd["mxS"]: dd["mxS"] = S_
        if S_ < dd["mn"]: dd["mn"] = S_
        dd["acc"] += abs(S_); dd["cnt"] += 1
        t_last = (t_, S_)
    cum_flips = cum_before + int(pref[-1])
    z_prev = int(sgn[-1])
    done = i1 / ntot
    if (i0 // CHUNK) % 200 == 0:
        print("  ... %.3f (%.0f M pts, %+.0f s)" % (done, i0 / 1e6, time.time() - t_start))

N_end = N0 + cum_flips
print("\nN(1e7) from dt=%.0e walk = %d   (new zeros in (1e6,1e7]: %d)"
      % (DT, N_end, N_end - N0))
if t_last:
    print("S(1e7) @ last 1.0-rad sample t=%.1f = %.4f" % t_last)
S_end = N_end - zeta_core.vartheta(T1) / math.pi
print("S(1e7) (endpoint, exact vartheta) = %.4f" % S_end)
print("\nper-decade max|S| / maxS / minS / mean|S| (1.0-rad samples):")
gm = 0.0
for dd in dec:
    mean = dd["acc"] / dd["cnt"] if dd["cnt"] else 0.0
    gm = max(gm, dd["mx"])
    print("  [%.0e, %.0e):  max|S|=%9.4f  max=%9.4f  min=%9.4f  mean|S|=%.4f"
          % (dd["lo"], dd["hi"], dd["mx"], dd["mxS"], dd["mn"], mean))
print("GUE sqrt(ln ln 1e7) = %.2f" % math.sqrt(math.log(math.log(T1))))

with open("S_t_walk_1e6_1e7_gpu_dt0005.txt", "w") as f:
    for t_, S_ in samps:
        f.write("%.1f\t%.10f\n" % (t_, S_))
print("S samples written: %d rows -> S_t_walk_1e6_1e7_gpu_dt0005.txt" % len(samps))
print("\ntotal %.0f s" % (time.time() - t_start))
