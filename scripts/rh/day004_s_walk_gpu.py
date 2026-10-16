#!/usr/bin/env python3
"""Day-004 E2 (GPU): the S(t) fluctuation walk over (1e4, 1e5] on cuPy/ROCm.

    S(t) = nzero(t) - vartheta(t)/pi      (t not a zero; exact)
with vartheta = DLMF 25.10.2 and nzero(t) = zeros in (0, t], obtained by
counting sign flips of the real Z(t) on a DT = 0.02 grid (the census list
zeros_T100000.txt is the reference for cross-checking).

WHY GPU (measured, out_bench_cupy.txt): the 4.5M point evaluations are
independent (batch pattern B: 1241x faster on the 8060S than numpy CPU);
the CPU sign-walk took 306 s, this batched version runs in seconds.

Engine: faithful vector port of zeta_core.Z_rs (2-term RS remainder) +
zeta_core.vartheta (Lanczos log-gamma), cross-checked pointwise against the
CPU engines before use.  Zero-count cross-checked against the census list
window by window.  Writes S_t_walk_1e4_1e5_gpu.txt.

Run:  ~/venvs/cupy/bin/cupy_py day004_s_walk_gpu.py
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

T0, T1, DT = 10_000.0, 100_000.0, 0.02
MAXN = int(math.sqrt(T1 / (2.0 * math.pi))) + 1  # 127
LNPI = math.log(math.pi)

LANCZOS = [cp.asarray(a, dtype=cp.float64) for a in zeta_core._LANCZOS]

def vartheta_gpu(tv):
    """Vector port of zeta_core.vartheta (base formula, ns = 0 for Re z > 0)."""
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
    wgt = (1.0 / cp.sqrt(nvec))
    mask = (nvec[None, :] <= N[:, None]).astype(cp.float64)
    S1 = (cp.cos(th[:, None] - tv[:, None] * lnn[None, :]) * (mask * wgt)).sum(axis=1)

    def psi(q):
        return cp.cos(2.0 * math.pi * (q * q - q - 0.0625)) / cp.cos(2.0 * math.pi * q)

    h = 1e-3
    d3 = (psi(p + 3j * h) - 3 * psi(p + 2j * h) + 3 * psi(p + 1j * h) - psi(p)).real / h ** 3
    sign = cp.where(((N - 1) % 2) == 0, 1.0, -1.0)
    R = sign * (psi(p).real / u - d3 / (96.0 * math.pi ** 2 * u ** 3))
    return 2.0 * S1 + R

# ---- validate the GPU port against the CPU engines before trusting it ----
tval = np.unique(np.concatenate([
    np.linspace(T0 + 1.0, T1 - 1.0, 300),
    zeros[(zeros > T0) & (zeros < T1)][::5000] + 0.37,
]))
zcpu = np.array([zeta_core.Z_rs(float(t)) for t in tval])
zgpu = Z_rs_gpu(cp.asarray(tval)).get()
dv = float(np.max(np.abs(zcpu - zgpu)))
print("GPU port validation: %d points, max |Z_rs_gpu - Z_rs_cpu| = %.3e" % (len(tval), dv))
assert dv < 1e-5, "GPU port diverges from the validated CPU engine"

# ---- the walk (batched) ----
ntot = int(round((T1 - T0) / DT)) + 1
CHUNK = 512_000
t_start = time.time()
Z_all = []
var_all = []
for i0 in range(0, ntot, CHUNK):
    tv = cp.asarray(T0 + DT * np.arange(i0, min(i0 + CHUNK, ntot), dtype=np.float64))
    Z_all.append(Z_rs_gpu(tv).get())
    var_all.append(vartheta_gpu(tv).get())
Z = np.concatenate(Z_all)
varth = np.concatenate(var_all)
print("Z values + vartheta for %d grid points: %.1f s" % (ntot, time.time() - t_start))

sgn = np.sign(Z)
sgn[sgn == 0] = 1
flip = (sgn[1:] != sgn[:-1]).astype(int)
cum = np.cumsum(flip)  # cum[j] = flips in grid intervals [0..j]
nzero_at = np.empty(ntot, dtype=int)   # nzero_at[j] = zeros in (0, T0 + DT*j]
nzero_at[0] = 10142
nzero_at[1:] = 10142 + cum
n_total = int(nzero_at[-1])
print(" flips detected: %d   (census list in (1e4, 1e5]: %d)" % (int(flip.sum()), int(((zeros > T0) & (zeros <= T1)).sum())))

# window-by-window cross-check against the census list (1000-step windows)
bad = 0
worst = (0, 0)
for k in range((ntot - 1) // 1000):
    j0 = k * 1000
    j1 = min(j0 + 1000, ntot - 1)
    nlist = int(np.searchsorted(zeros, T0 + DT * j1, side='left')) - int(np.searchsorted(zeros, T0 + DT * j0, side='left'))
    nwalk = int(nzero_at[j1] - nzero_at[j0])
    if abs(nlist - nwalk) > worst[1]:
        worst = (k, abs(nlist - nwalk))
    bad += 0 if nlist == nwalk else 1
print("window cross-check: %d/10000 windows mismatch the census list; worst: window %d off by %d" % (bad, worst[0], worst[1]))

# ---- record S(t) every 1.0 in t ----
idx = np.arange(50, ntot, 50)
t_rec = T0 + DT * idx
S_rec = nzero_at[idx] - varth[idx] / math.pi
np.savetxt("S_t_walk_1e4_1e5_gpu.txt", np.column_stack([t_rec, S_rec]))

for Tend, Sne in ((10_000.0, 0.0347), (100_000.0, -2.5584)):
    Nep = int((zeros <= Tend).sum())
    Sev = Nep - zeta_core.vartheta(Tend) / math.pi
    print("S(%.0e): from list = %+.4f   expected %+.4f  %s"
          % (Tend, Sev, Sne, "CONSISTENT" if abs(Sev - Sne) < 5e-3 else "CHECK"))

amp = np.abs(S_rec)
print("\nS(t) stats (t in [%.0f, %.0f]):" % (t_rec.min(), t_rec.max()))
print("  max |S| = %.4f at t = %.2f" % (amp.max(), t_rec[np.argmax(amp)]))
print("  min  S  = %.4f at t = %.2f" % (S_rec.min(), t_rec[np.argmin(S_rec)]))
print("  max  S  = %.4f at t = %.2f" % (S_rec.max(), t_rec[np.argmax(S_rec)]))
print("  mean |S| = %.4f" % amp.mean())
print("\n  GUE scale sqrt(ln ln 1e5) = %.2f ;  ln(T)/2pi = %.2f"
      % (math.sqrt(math.log(math.log(T1))), math.log(T1) / (2.0 * math.pi)))

print("\nper-10k max|S| (growth envelope):")
for k in range(int(T0 // 10_000), int(T1 // 10_000) + 1):
    m = (t_rec >= k * 10_000) & (t_rec < (k + 1) * 10_000)
    if m.any():
        print("  [%6.0f, %6.0f):  max|S| = %8.4f   mean|S| = %.4f"
              % (k * 10_000, (k + 1) * 10_000, np.abs(S_rec[m]).max(), np.abs(S_rec[m]).mean()))
print("\ntotal: %.1f s" % (time.time() - t_start))
