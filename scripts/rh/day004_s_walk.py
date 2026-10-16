#!/usr/bin/env python3
"""Day-004 E2: the S(t) fluctuation walk over (1e4, 1e5].

S(T) = arg_cont(zeta(1/2+iT))/pi - 1.  With the real Z(t) = e^{i vartheta(t)}
zeta(1/2+it) and the continuously tracked argument of Z: arg(Z) starts at pi
(Z(0) = zeta(1/2) < 0) and increases by +pi at EVERY zero crossing
(upward: (2k+1)pi -> (2k+2)pi; downward: (2k)pi -> (2k+1)pi), so
    argZ_cont(t) = pi * (1 + nzero(t))     (nzero = zeros in (0, t])
and between zeros:
    S(t) = nzero(t) - vartheta(t)/pi       (exact)

nzero is initialized to N(T0) = count of zeros_T100000.txt below 1e4
(v1 bug: it started at 0, so every recorded S was off by -10142).
Flip counts are EM-gated (16 RS bisections + one |Z| < 1e-4 confirm):
v1 counted 127925 flips vs the true 127923 (2 RS-noise flips, visible as a
+2 step in the recorded S near t ~ 7e4).

Walk: Z_rs (~65 us/eval).  One recorded point per 1.0 in t.
Run: ~8-10 min CPU.  Writes S_t_walk_1e4_1e5.txt.
"""
import math
import sys
import time

import numpy as np

sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False)

T0, T1 = 10_000.0, 100_000.0
DT = 0.02
zeros = np.loadtxt("zeros_T100000.txt")

t = T0
zprev = zeta_core.Z_rs(t)
nzero = int((zeros <= T0).sum())  # zeros in (0, t]

ts, ss = [], []
t_start = time.time()
n = 0
spur = 0
while t <= T1:
    n += 1
    if n % 200_000 == 0:
        print("  ... t = %.0f (%.0f s, %d gated flips)" % (t, time.time() - t_start, spur))
    z = zeta_core.Z_rs(t)
    if zprev * z < 0.0:
        lo, hi, zp = t - DT, t, zprev
        for _ in range(16):
            mid = 0.5 * (lo + hi)
            zm = zeta_core.Z_rs(mid)
            if zp * zm <= 0.0:
                hi = mid
            else:
                lo, zp = mid, zm
        if abs(zeta_core.Z(0.5 * (lo + hi))) < 1e-4:
            nzero += 1
        else:
            spur += 1
    if n % 50 == 0:
        ts.append(t)
        ss.append(nzero - zeta_core.vartheta(t) / math.pi)
    zprev = z
    t += DT

ts = np.array(ts)
ss = np.array(ss)
print("walk done in %.0f s: %d points, nzero(T1) = %d (expect %d), %d spurious flips gated"
      % (time.time() - t_start, len(ss), nzero, int((zeros <= T1).sum()), spur))

for Tend, Sne in ((10_000.0, 0.0347), (100_000.0, -2.5584)):
    Nep = int((zeros <= Tend).sum())
    Sev = Nep - zeta_core.vartheta(Tend) / math.pi
    print("S(%.0e): N = %d  from list = %+.4f   expected %+.4f  (diff %+.4f)  %s"
          % (Tend, Nep, Sev, Sne, Sev - Sne, "CONSISTENT" if abs(Sev - Sne) < 5e-3 else "CHECK"))

amp = np.abs(ss)
print("\nS(t) stats on the walk (t in [%.0f, %.0f]):" % (ts.min(), ts.max()))
print("  max |S| = %.4f at t = %.2f" % (amp.max(), ts[np.argmax(amp)]))
print("  min  S  = %.4f at t = %.2f" % (ss.min(), ts[np.argmin(ss)]))
print("  max  S  = %.4f at t = %.2f" % (ss.max(), ts[np.argmax(ss)]))
print("  mean |S| = %.4f" % amp.mean())
print("\n  GUE scale sqrt(ln ln 1e5) = %.2f ;  ln(T)/2pi = %.2f"
      % (math.sqrt(math.log(math.log(T1))), math.log(T1) / (2 * math.pi)))

print("\nper-10k max|S| (growth envelope):")
for k in range(int(T0 // 10_000), int(T1 // 10_000) + 1):
    m = (ts >= k * 10_000) & (ts < (k + 1) * 10_000)
    if m.any():
        print("  [%6.0f, %6.0f):  max|S| = %8.4f   mean|S| = %.4f"
              % (k * 10_000, (k + 1) * 10_000, np.abs(ss[m]).max(), np.abs(ss[m]).mean()))

np.savetxt("S_t_walk_1e4_1e5.txt", np.column_stack([ts, ss]))
print("\nwrote S_t_walk_1e4_1e5.txt  (%d points)" % len(ts))
