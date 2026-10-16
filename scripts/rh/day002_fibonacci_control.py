#!/usr/bin/env python3
"""Control for day002_fibonacci_closeout.py test (iii).

Hypothesis: the rho(u, gap) = -0.049 flag was an ARTIFACT of scaling gaps
by the GLOBAL mean, while the smooth ln-density makes gaps shrink ~5-16%
from the bottom to the top of every band (any band ratio, not Fibonacci-
specific). Controls:
  (A) local-density scaling:  g_i = gap_i * (1/2pi) ln(t_i/2pi)  ~ 1 in
      expectation; the smooth trend is removed.
  (B) phase-shifted partition: bands a*F_k .. a*F_{k+1}, same ratio
      1.618, phase a = 1.3 -- if the (iii) signal is density-driven it
      persists; if it were Fibonacci-phase-specific it would vanish.
"""
import math
import numpy as np

ts = np.loadtxt("zeros_T10000.txt", dtype=np.float64)
TMAX = ts.max()
F = [1, 1]
while F[-1] < 1.15e4:
    F.append(F[-1] + F[-2])
F = np.array(F, dtype=np.float64)

def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(np.float64)
    ry = np.argsort(np.argsort(y)).astype(np.float64)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    return float(np.sum(rx * ry) / math.sqrt(np.sum(rx * rx) * np.sum(ry * ry)))

def bands_for(a):
    lo = a * F[:-1]; hi = a * F[1:]
    idx = np.clip(np.searchsorted(lo, ts, side="right") - 1, 0, len(lo) - 1)
    m = (ts >= lo[idx]) & (ts < hi[idx])
    valid = np.array([lo[j] >= 21.0 and hi[j] <= TMAX for j in range(len(lo))])
    m &= valid[idx]
    return lo, hi, idx[m], m

def report(lo, hi, idx, m):
    zi = np.where(m)[0]           # zeros in complete bands (last census zero is in the truncated band)
    u = (ts[zi] - lo[idx]) / (hi[idx] - lo[idx])
    g = ts[zi + 1] - ts[zi]
    local = g * (np.log(ts[m] / (2 * math.pi)) / (2 * math.pi))
    gm = g / g.mean()
    n = len(g)
    r1 = spearman(u, gm)
    r2 = spearman(u, local)
    print("  n = %d :  rho(u, GLOBAL-scaled gap) = %+.4f (z = %+.2f)   |   rho(u, LOCAL-density-scaled gap) = %+.4f (z = %+.2f)"
          % (n, r1, r1 * math.sqrt(n - 1), r2, r2 * math.sqrt(n - 1)))

print("(A) Fibonacci partition (a=1.0), two scalings:")
lo, hi, idx, m = bands_for(1.0)
report(lo, hi, idx, m)
print("(B) phase-shifted partition (a = 1.3, same ratio 1.618):")
lo, hi, idx, m = bands_for(1.3)
report(lo, hi, idx, m)
print("(C) phase-shifted partition (a = 0.99, near-identity phase):")
lo, hi, idx, m = bands_for(0.99)
report(lo, hi, idx, m)
print("""
Interpretation:
  * (A) LOCAL row should be ~ 0 if the (iii) flag was the smooth-density artifact.
  * (B)/(C) GLOBAL rows should stay around -0.04..-0.05 if density-driven
    (phase-insensitive); a Fibonacci-SPECIFIC effect would vanish at the
    shifted phases.
""")
