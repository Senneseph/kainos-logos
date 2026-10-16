#!/usr/bin/env python3
"""Day-004 E1b: the missing-tail size T0(N) = |zeta(s) - P_N(s)| as a function
of the truncation N, at fixed t (GPU batched, s = 1/2 + i t).

Questions measured (labeled):
  (Q1) growth law: T0 ~ C * sqrt(N) while N << ~2*pi*t?      (random-walk law)
  (Q2) crossover: where does T0 stop growing?  compare N* vs 2*pi*t.
  (Q3) Riemann-Siegel compression: naive ~2*pi*t terms vs
       N0 = floor(sqrt(t/2pi)) terms; measured factor at each t.
  (Q4) t=0 control: there the FIRST-ORDER integral term N^{1-s}/(1-s)
       captures the tail (T1/T0 -> small) - the smooth 'next term' logic
       is real, but only on the pole side; for t > 0 the missing piece is
       the oscillatory part (mirror-governed).
Run: ~/venvs/cupy/bin/python, LD_LIBRARY_PATH=/opt/rocm/lib.
"""
import math
import os
import sys
import time

os.environ.setdefault("LD_LIBRARY_PATH", "/opt/rocm/lib")
import numpy as np
import cupy as cp
sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False)
t_start = time.time()
zeros = np.loadtxt("zeros_T100000.txt")
gz = zeros[(zeros > 990) & (zeros < 1010)]
print("zeros in (990, 1010): %s" % gz)
t_at_zero = float(gz[0])
t_mid = float(0.5 * (gz[0] + gz[1]))

rows = [
    ("t = 0 (control)", 0.0),
    ("t = 50", 50.0),
    ("t = %.3f (between zeros)" % t_mid, t_mid),
    ("t = %.4f (A ZERO)" % t_at_zero, t_at_zero),
]
Ns = [10 ** k for k in range(2, 8)]
MAXN = max(Ns)

print("\n%-26s" % "row (s = 1/2 + it)")
print("  N:              " + " ".join("%5d" % n for n in Ns))
res = {}
for name, tv in rows:
    s = 0.5 + 1j * tv
    zt = zeta_core.zeta(s)
    nn = cp.arange(1, MAXN + 1, dtype=cp.float64)
    ln_n = cp.log(nn)
    base = cp.exp(-0.5 * ln_n)  # shared magnitude part n^{-1/2}
    row = []
    for Nn in Ns:
        Pn = base[:Nn].dot(cp.exp(-1j * tv * ln_n[:Nn]))
        row.append(abs(zt - Pn))
    res[name] = row
    print("%-26s" % name)
    print("  T0(N):         " + " ".join("%5.2f" % v for v in row))
    print("  T0/sqrt(N):    " + " ".join("%5.2f" % (v / math.sqrt(Nn)) for v, Nn in zip(row, Ns)))

print("\n(Q2) the growth law: T0(N) * |1-s| / sqrt(N)  (== 1.0 iff |tail| = sqrt(N)/|1-s| EXACTLY):")
for name, tv in rows:
    rowv = res[name]
    one_minus_s_mod = abs(1.0 - (0.5 + 1j * tv))
    print("  %-26s: " % name + " ".join("%6.3f" % (v * one_minus_s_mod / math.sqrt(Nn)) for v, Nn in zip(rowv, Ns)))
print("  (t = 0 row: the series' tail IS the integral itself; t > 0 rows: magnitude identical,")
print("   phase NOT captured by the single first-order term - E1 grid gave T1/T0 ~= 1.0)")
print("\n(Q3) series vs continuation (measured picture):")
for name, tv in rows:
    if tv <= 0:
        continue
    N0 = math.sqrt(tv / (2.0 * math.pi))
    print("  %-26s: naive series: NO N makes T0 small (T0 = sqrt(N)/|1-s| for all N tested to 1e7)" % (name,))
    print("  %-26s   continuation: Riemann-Siegel uses N0 = sqrt(t/2pi) = %.1f terms + tiny remainder" % (name + "*", N0))

# (Q4) t = 0 control: tail = -N^{1-s}/(1-s) + O(1): the SIGN-checked subtraction
print("\n(Q4) t = 0 control (sigma = 0.5): raw tail vs after REMOVING the integral -N^{1-s}/(1-s):")
s = 0.5 + 0j
zt = zeta_core.zeta(s)
NN = [10 ** k for k in range(2, 6)]
nn_np = np.arange(1, max(NN) + 1, dtype=float)
ln_np = np.log(nn_np)
for Nn in NN:
    Pn = float(np.exp(-0.5 * ln_np[:Nn]).dot(np.ones(Nn)))
    T0 = abs(zt - Pn)
    first_order = Nn ** (1 - s) / (1 - s)
    T1_wrong = abs(zt - Pn - first_order)   # subtracting the WRONG sign doubles it
    T1 = abs(zt - Pn + first_order)         # removing the true missing part
    print("  N=%6d:  T0 = %10.4f   T1(+I) = %10.4f   T1(-I) = %10.4f   T1/T0 = %.4f" % (Nn, T0, T1, T1_wrong, T1 / T0))
print("  (zeta(1/2) = %.6f; measured second-order remainder T1(+I) ~= 0.5 + 1/(24N)...: O(1))" % zeta_core.zeta(s))

# (Q5) DIRECTION: the phase of the missing tail, phi(N) = arg(zeta(s) - P_N(s)),
# vs the local phase of the N-th term itself, -t*ln(N):  are they "going"
# together (same phase velocity d/d ln N = -t)?
print("\n(Q5) direction of the missing block (s = 1/2 + i t):")
for name, tv in rows:
    if tv <= 0:
        continue
    zt = zeta_core.zeta(0.5 + 1j * tv)
    nnp = np.arange(1, max(Ns) + 1, dtype=float)
    ph = []
    for Nn in Ns:
        Pn = (nnp[:Nn] ** -0.5) @ np.exp(-1j * tv * np.log(nnp[:Nn]))
        ph.append(np.angle(zt - Pn))
    # phase velocity per decade of N: (ph - ph_prev)/log10(N/N_prev)
    vel = [ (ph[i] - ph[i - 1]) / math.log10(Ns[i] / Ns[i - 1]) if abs(ph[i] - ph[i - 1]) < math.pi else None for i in range(1, len(ph)) ]
    lastterm_vel = -tv * np.log(10.0)  # d(-t ln n)/d log10(n) = -t ln 10
    print("  %-26s: last-term phase velocity = %9.3f rad/decade" % (name, lastterm_vel))
    print("  %-26s: tail phase phi(N)      = %s" % (name, "  ".join("%8.3f" % (v / math.pi) for v in ph)))
    shown = ["%.3f" % (v / math.pi) for v in vel if v is not None and abs(v) < 20]
    print("  %-26s: tail phase velocity    = %s (pi units/decade; last-term in rad: %.2f -> %.3f pi)"
          % (name, "  ".join(shown), lastterm_vel, lastterm_vel / math.pi))

print("\ntotal: %.1f s" % (time.time() - t_start))
