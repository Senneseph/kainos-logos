#!/usr/bin/env python3
"""Day-004 continuation (GPU): S(t) over (1e5, 1e6] - the growth envelope
one decade further.  Same all-GPU method as day004_s_walk_gpu.py (batched
Z_rs + vectorized vartheta, sign bookkeeping on host).  There is NO zero
LIST to cross-check against past 1e5, so the endpoint N(1e6) is verified by
the independent dps-40 mpmath 2K identity (separate container run, see
day004b_n1e6_mpmath.py).  Writes S_t_walk_1e5_1e6_gpu.txt.
Run: ~/venvs/cupy/bin/cupy_py day004b_s_walk_1e6.py
"""
import math
import sys
import time

import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False)
zeros = np.loadtxt("zeros_T100000.txt")

T0, T1, DT = 100_000.0, 1_000_000.0, 0.02
MAXN = int(math.sqrt(T1 / (2.0 * math.pi))) + 1  # 399
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

# validate the port on this machine again (cheap, honest)
tval = np.linspace(T0 + 1.0, T1 - 1.0, 200)
zcpu = np.array([zeta_core.Z_rs(float(t)) for t in tval])
zgpu = Z_rs_gpu(cp.asarray(tval)).get()
dv = float(np.max(np.abs(zcpu - zgpu)))
print("GPU port validation: %d points, max |Z_gpu - Z_cpu| = %.3e" % (len(tval), dv))
assert dv < 1e-5

ntot = int(round((T1 - T0) / DT)) + 1  # 45,000,000
CHUNK = 256_000
t_start = time.time()
Z_all, var_all = [], []
for i0 in range(0, ntot, CHUNK):
    tv = cp.asarray(T0 + DT * np.arange(i0, min(i0 + CHUNK, ntot), dtype=np.float64))
    Z_all.append(Z_rs_gpu(tv).get())
    var_all.append(vartheta_gpu(tv).get())
    if (i0 // CHUNK) % 10 == 0:
        print("  ... %.0f M of %d pts (%.0f s)" % (i0 / 1e6, ntot, time.time() - t_start))
Z = np.concatenate(Z_all)
varth = np.concatenate(var_all)
print("batched Z + vartheta for %.1f M points: %.0f s" % (ntot / 1e6, time.time() - t_start))

sgn = np.sign(Z)
sgn[sgn == 0] = 1
flip = (sgn[1:] != sgn[:-1]).astype(np.int32)
cum = np.cumsum(flip, dtype=np.int64)
nzero_at = np.empty(ntot, dtype=np.int64)
nzero_at[0] = int((zeros <= T0).sum())  # 138065
nzero_at[1:] = nzero_at[0] + cum
N_end = int(nzero_at[-1])
print("N(1e5) = %d (from list) -> N(1e6) from walk = %d (new zeros %d)" % (int(nzero_at[0]), N_end, int(flip.sum())))

idx = np.arange(50, ntot, 50)  # every 1.0 in t
t_rec = T0 + DT * idx
S_rec = nzero_at[idx] - varth[idx] / math.pi
np.savetxt("S_t_walk_1e5_1e6_gpu.txt", np.column_stack([t_rec, S_rec]))

S1e6 = N_end - zeta_core.vartheta(T1) / math.pi
print("S(1e6) from walk-count = %+.4f   (pending mpmath 2K verification)" % S1e6)

amp = np.abs(S_rec)
print("\nS(t) stats (t in [%.0f, %.0f]):" % (t_rec.min(), t_rec.max()))
print("  max |S| = %.4f at t = %.2f" % (amp.max(), t_rec[np.argmax(amp)]))
print("  min  S  = %.4f at t = %.2f" % (S_rec.min(), t_rec[np.argmin(S_rec)]))
print("  max  S  = %.4f at t = %.2f" % (S_rec.max(), t_rec[np.argmax(S_rec)]))
print("  mean |S| = %.4f" % amp.mean())
print("  GUE scale sqrt(ln ln 1e6) = %.2f ;  ln(T)/2pi = %.2f"
      % (math.sqrt(math.log(math.log(T1))), math.log(T1) / (2.0 * math.pi)))

print("\nper-decade max|S| (growth envelope):")
for k in range(int(T0 // 100_000), int(T1 // 100_000) + 1):
    m = (t_rec >= k * 100_000) & (t_rec < (k + 1) * 100_000)
    if m.any():
        print("  [%6.0f, %6.0f):  max|S| = %8.4f   mean|S| = %.4f"
              % (k * 100_000, (k + 1) * 100_000, np.abs(S_rec[m]).max(), np.abs(S_rec[m]).mean()))
print("\ntotal %.0f s" % (time.time() - t_start))
