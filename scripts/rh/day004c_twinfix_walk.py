#!/usr/bin/env python3
"""Day-004c (GPU): twin-defect re-walk.  The 07:34 audit found the day-004b
S(1e6) walk (dt=0.02, NO midpoint dip check) reproduced the Day-003 hidden-twin
defect: twin pairs with gap < dt are invisible to the sign walk.  GOE-scaled
empirical projection (from the verified <=1e5 list: 32 pairs <0.05, zero <0.02):
~11-20 missed twin PAIRS in [1e5, 1e6] on a dt=0.02 grid = 22-40 missed zeros,
matching the observed S(1e6) = -40.5 vs the flat 1e5 envelope (offset ~38-42,
even, consistent with the 2K parity-only check at 6.5e-9).

This run re-walks [1e5, 1e6] at dt=0.005 (expected residual twin pairs < 0.5,
measured projection) and tracks the cumulative OFFSET versus the dt=0.02 walk
to watch the missed twins come back (staircase of +2 per recovered pair).
Run: ~/venvs/cupy/bin/cupy_py day004c_twinfix_walk.py
"""
import math
import sys
import time

import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False)
T0, T1, DT = 100_000.0, 1_000_000.0, 0.005
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

t_start = time.time()
ntot = int(round((T1 - T0) / DT)) + 1  # 180,001
print("dt=0.005 walk: %d points" % ntot)
CHUNK = 256_000
Z_all, var_all = [], []
for i0 in range(0, ntot, CHUNK):
    tv = cp.asarray(T0 + DT * np.arange(i0, min(i0 + CHUNK, ntot), dtype=np.float64))
    Z_all.append(Z_rs_gpu(tv).get())
    var_all.append(vartheta_gpu(tv).get())
    if (i0 // CHUNK) % 100 == 0:
        print("  ... %.0f M pts (%.0f s)" % (i0 / 1e6, time.time() - t_start))
Z = np.concatenate(Z_all)
varth = np.concatenate(var_all)
print("batched eval: %.0f s" % (time.time() - t_start))

sgn = np.sign(Z)
sgn[sgn == 0] = 1
flip = (sgn[1:] != sgn[:-1]).astype(np.int32)
cum = np.cumsum(flip, dtype=np.int64)
N_end = int((np.loadtxt("zeros_T100000.txt") <= T0).sum()) + int(flip.sum())
print("N(1e6) @ dt=0.005 = %d   (dt=0.02 walk gave 1,747,104 ;  new flips %d)"
      % (N_end, int(flip.sum())))

# ---- offset curve vs the dt=0.02 walk (its zero count rebuilt from S file) ----
old = np.loadtxt("S_t_walk_1e5_1e6_gpu.txt")
t_old, S_old = old[:, 0], old[:, 1]
th_old = np.array([zeta_core.vartheta(float(t)) for t in t_old])
N_old = S_old + th_old / math.pi          # integer-valued counts

print("\nt            N@dt=0.005   N@dt=0.02   offset(recovered twins)")
STEP = 200                                # 1.0 in t
for k in range(0, ntot, 100000):
    t_k = T0 + DT * k
    nnew = int(N_old[0]) + int(cum[k - 1]) if k > 0 else int(N_old[0])
    i_old = int(round(t_k - t_old[0]))
    i_old = min(max(i_old, 0), len(N_old) - 1)
    noff = float(np.round(N_old[i_old]))
    if t_k >= 1.0 * T0:
        print("  %10.0f   %12d   %12.0f   %+11.0f" % (t_k, nnew, noff, nnew - noff))

# final
i_old = len(N_old) - 1
print("  %10.0f   %12d   %12.0f   %+11.0f   <-- FINAL OFFSET (missed twins at dt=0.02)"
      % (T1, N_end, float(np.round(N_old[i_old])), N_end - float(np.round(N_old[i_old]))))

# ---- S statistics on the corrected walk ----
idx = np.arange(0, ntot, 200)               # every 1.0 in t
t_rec = T0 + DT * idx
S_rec = (int(N_old[0]) + cum[idx - 1]) - varth[idx] / math.pi
S_rec[0] = int(N_old[0]) - varth[0] / math.pi
np.savetxt("S_t_walk_1e5_1e6_gpu_dt0005.txt", np.column_stack([t_rec, S_rec]))
amp = np.abs(S_rec)
print("\nS(t) @ dt=0.005 corrected, t in [1e5, 1e6]:")
print("  S(1e5)  = %+.4f" % S_rec[0])
S1e6 = N_end - zeta_core.vartheta(T1) / math.pi
print("  S(1e6)  = %+.4f" % S1e6)
print("  max |S| = %.4f at t = %.2f" % (amp.max(), t_rec[np.argmax(amp)]))
print("  min  S  = %.4f at t = %.2f" % (S_rec.min(), t_rec[np.argmin(S_rec)]))
print("  mean|S| = %.4f" % amp.mean())
print("per-decade max|S|:")
for k in range(1, 11):
    m = (t_rec >= k * 100_000) & (t_rec < (k + 1) * 100_000)
    if m.any():
        print("  [%6.0f, %6.0f):  max|S| = %8.4f   mean|S| = %.4f"
              % (k * 100_000, (k + 1) * 100_000, np.abs(S_rec[m]).max(), np.abs(S_rec[m]).mean()))
print("\ntotal %.0f s" % (time.time() - t_start))
