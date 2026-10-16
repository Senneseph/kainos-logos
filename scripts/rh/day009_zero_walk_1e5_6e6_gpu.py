#!/usr/bin/env python3
"""Day-009: GPU flip walk 1e5 -> 6e6 (dt = 2.5e-4, twin-safe) to extend
the certified zero list (float64 flip positions, ~1e-4 in gamma —
sufficient for the 25.2.12 product at t <= 2e5: phase error
~ t*dgamma/gamma^2 ~ 5e-10 rad).

Twin-floor note: floor ~ 0.003 on [1e5, 1e6], projected ~9e-4 by 1e7 —
dt = 2.5e-4 is 3-9% of the floor across the whole window; the dt/2
stability re-walk is the certificate (P-0 twin-floor rule).

Engine: post-d3-fix 2-term RS (twin-safe for t >= 1e5 per day-009 §5:
error O(u^-5) ~ 1e-8 there). Outputs: flip positions (zero list
extension), N(6e6), min gap, dt vs dt/2 agreement.

Run: ~/venvs/cupy/bin/cupy_py day009_zero_walk_1e5_6e6_gpu.py
"""
import math
import sys
import time

import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False), "zeta_core selftest failed"

T0, T1, DT = 100_000.0, 6_000_000.0, 2.5e-4
MAXN = int(math.sqrt(T1 / (2.0 * math.pi))) + 1
LNPI = math.log(math.pi)
LANCZOS = [cp.asarray(a, dtype=cp.float64) for a in zeta_core._LANCZOS]

gam0 = np.loadtxt("zeros_T100000.txt")
N0 = int(np.searchsorted(gam0, T0))
print("N(1e5) anchor =", N0, "(expect 138065)")
assert N0 == 138065

vt = np.linspace(T0 + 11.3, T1 - 11.3, 12)
vg = cp.asarray(vt, dtype=cp.float64)

def vartheta_gpu(tv):
    z = 0.25 + 0.5j * tv
    zm1 = z - 1.0
    x = cp.full(tv.shape, float(LANCZOS[0]), dtype=cp.complex128)
    for i in range(1, len(LANCZOS)):
        x = x + LANCZOS[i] / (zm1 + i)
    t_ = zm1 + 7.5
    cg = 0.5 * math.log(2 * math.pi) + (zm1 + 0.5) * cp.log(t_) - t_ + cp.log(x)
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
    S1 = (cp.cos(th[:, None] - tv[:, None] * lnn[None, :])
          * (mask * wgt)).sum(axis=1)

    def psi(q):
        return cp.cos(2.0 * math.pi * (q * q - q - 0.0625)) \
            / cp.cos(2.0 * math.pi * q)

    h = 1e-3
    S3 = (psi(p + 3j * h) - 3 * psi(p + 2j * h)
          + 3 * psi(p + 1j * h) - psi(p))
    d3 = -S3.imag / h ** 3          # DAY-007 FIX
    sign = cp.where(((N - 1) % 2) == 0, 1.0, -1.0)
    R = sign * (psi(p).real / u - d3 / (96.0 * math.pi ** 2 * u ** 3))
    return 2.0 * S1 + R

vgZ = Z_rs_gpu(vg).get()
vc = np.array([zeta_core.Z_rs(float(x)) for x in vt])
err = float(np.abs(vgZ - vc).max())
print("GPU-vs-host (post-fix): max |diff| = %.3e" % err)
assert err < 1e-6

def walk2(dt, tag):
    t_start = time.time()
    steps = int(round((T1 - T0) / dt)) + 1
    CHUNK = 32768
    cum = 0
    z_prev = None
    flips_t = []
    s_rows = []
    for i0 in range(0, steps, CHUNK):
        i1 = min(i0 + CHUNK, steps)
        tv = cp.asarray(T0 + dt * np.arange(i0, i1, dtype=np.float64))
        Z = Z_rs_gpu(tv).get()
        varth = vartheta_gpu(tv).get()
        sgn = np.sign(Z); sgn[sgn == 0] = 1.0
        if z_prev is not None:
            seg = np.concatenate(([z_prev], sgn))
            fl = (seg[1:] != seg[:-1]).astype(np.int64)
        else:
            fl = np.zeros(len(sgn), dtype=np.int64)
        pref = np.cumsum(fl)
        N_at = N0 + cum + pref
        S_at = N_at - varth / math.pi
        tf = T0 + dt * np.arange(i0, i1)
        flt = tf[fl == 1]
        flips_t.append(flt)
        if (i1 % (CHUNK * 4)) == 0:
            print("   ... %d / %d  (N now %d)  %.0f s"
                  % (i1, steps, N_at[-1], time.time() - t_start))
        cum += int(pref[-1])
        z_prev = int(sgn[-1])
    fl_all = np.concatenate(flips_t)
    N_end = N0 + cum
    el = time.time() - t_start
    print("[%s] dt=%.1e: N(6e6) = %d  flips = %d  elapsed %.1f s"
          % (tag, dt, N_end, len(fl_all), el))
    return fl_all, N_end

fl_dt, N_dt = walk2(DT, "dt")
gaps = np.diff(fl_dt)
gmin = float(gaps.min()) if len(gaps) else float("nan")
print("min gap on [1e5, 6e6]: %.6f" % gmin)

fl_dh, N_dh = walk2(DT / 2, "dt/2")
agree = (N_dt == N_dh)
print("[stability] N(dt)=%d  N(dt/2)=%d  agree=%s" % (N_dt, N_dh, agree))

# merge with the 1e5 list and save the extension (and full list)
new_list = np.concatenate((gam0, fl_dt))
np.savetxt("zeros_T6000000_ext.txt", new_list, fmt="%.10e")
np.savetxt("zeros_T6000000_ext_GT100000.txt", fl_dt, fmt="%.10e")
S_first_t = T0 + DT
print("extension written: zeros_T6000000_ext.txt (%d zeros, up to 6e6)"
      % len(new_list))
print("dt/2 agreement =", agree, " (P-0 twin certificate; if False the")
print("1e7/1e5 walk findings apply — inspect before use)")
