#!/usr/bin/env python3
"""Day-002 close-out: Fibonacci-band vs zero statistics on the measured
census (zeros_T10000.txt, 10,142 zeros, t <= 1e4).

Day-001 S3f falsified the 'unique root prime per band' prediction for
PRIMES. This closes the ZERO side of the thread: are the zeros themselves
Fibonacci-coupled?  Null hypotheses to test at T = 1e4:

  (i)  band counts: zeros in band k (F_k <= t < F_{k+1}) proportional to
       expected count int_{F_k}^{F_{k+1}} (1/2pi) ln(t/2pi) dt      [chi^2]
  (ii) in-band position u = (t - F_k)/(F_{k+1} - F_k) ~
       uniform on (0,1) (no peaking at band edges/centers)          [chi^2]
  (iii) no correlation between in-band position and the (locally scaled)
       spacing to the next zero                                     [Spearman]

METHOD NOTE (self-bug caught on v1 of this script): the LAST band
(6765..10946) is TRUNCATED by the census (t <= 1e4 < 10946).  Treating it
as a full band made all three tests flag "coupling" -- a pure artifact:
expected counts were integrated past the data, u could never exceed
(1e4-6765)/4181 = 0.774 in that band, and the artificial band edge at
10946 inflated distances.  All tests therefore run on COMPLETE bands only
(F_k >= 21 and F_{k+1} <= TMAX); the truncated band is reported verbatim
with its expectation clipped to the data.

Verdict rule: a deviation beyond the stated flag threshold on the
complete-band tests is a COUPLING signal; otherwise the thread is closed
as a measured NULL at T = 1e4.
"""
import math

import numpy as np

ts = np.loadtxt("zeros_T10000.txt", dtype=np.float64)
TMAX = ts.max()
print("zeros loaded: %d   (first: %.6f, last: %.6f)" % (len(ts), ts[0], TMAX))

# Fibonacci bands
F = [1, 1]
while F[-1] < 1.15e4:
    F.append(F[-1] + F[-2])
F = np.array(F, dtype=np.float64)
k_of = np.clip(np.array([int(np.searchsorted(F, t, side="right") - 1) for t in ts], dtype=np.int64),
               1, len(F) - 2)
Fib = F[k_of]
Fib_next = F[k_of + 1]
u = (ts - Fib) / (Fib_next - Fib)

# complete band: fully inside the census, above the first zero
complete = np.array([F[k] >= 21.0 and F[k + 1] <= TMAX for k in range(len(F) - 1)])
band_idx = np.where(complete)[0]
trunc_idx = [k for k in range(len(F) - 1) if F[k] + 1.0 >= TMAX]  # band(s) running past the data


def expected_count(a: float, b: float) -> float:
    f = lambda t: t * (math.log(t / (2 * math.pi)) - 1.0)
    return (f(b) - f(a)) / (2 * math.pi)


print("\n(i)  zeros per Fibonacci band vs expectation:")
print("    [verbatim] truncated/edge bands (NOT part of the chi^2):")
for k in set(trunc_idx) | {k_of[0]}:
    lo, hi = F[k], F[k + 1]
    hi_eff = min(hi, TMAX)
    m = int(np.sum(k_of == k))
    exp = expected_count(lo, hi_eff)
    tag = "TRUNCATED: band runs to %.0f > data %.0f" % (hi, TMAX) if hi > TMAX else "edge band (first zero inside)"
    print("    F_%d = %7.0f .. %7.0f :  %5d zeros   expected %8.1f (clipped)   obs/exp %.3f   %s"
          % (k, lo, hi, m, exp, m / exp, tag))
print("    [test] complete bands F_k >= 21, F_{k+1} <= %.0f:" % TMAX)
chi2 = 0.0
for k in band_idx:
    lo, hi = F[k], F[k + 1]
    m = int(np.sum(k_of == k))
    exp = expected_count(lo, hi)
    chi2 += (m - exp) ** 2 / exp
    print("    F_%d = %7.0f .. %7.0f :  %5d zeros   expected %8.1f   obs/exp %.4f" % (k, lo, hi, m, exp, m / exp))
dof = len(band_idx) - 1
z = ((chi2 / dof) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * dof))) / math.sqrt(2.0 / (9.0 * dof))
p = 0.5 * math.erfc(z / math.sqrt(2.0))
print("    chi^2 = %.2f on %d dof  ->  p = %.4f   (flag if p < 0.01)" % (chi2, dof, p))

# (ii) in-band position uniformity on complete bands only
uc = u[np.isin(k_of, band_idx)]
U, _ = np.histogram(uc, bins=10, range=(0.0, 1.0))
E = np.full(10, len(uc) / 10.0)
dev = (U - E) / np.sqrt(E)
print("\n(ii) in-band position u (complete bands only, n = %d), 10 bins:" % len(uc))
print("    obs:", U.tolist())
print("    expected (uniform): %.1f each" % E[0])
md = float(np.max(np.abs(dev)))
print("    max |obs-exp|/sqrt(exp) = %.2f   %s" % (md, "uniform (flag at > 3.0)" if md < 3.0 else "*** COUPLING SIGNAL ***"))

# (iii) correlation on complete bands only. PRIMARY scale: local density
# g_i = gap_i * (1/2pi) ln(t_i/2pi) (expectation ~ 1 at each t). The
# global-mean scale flags rho ~ -0.05 (z ~ -4), but the phase-shifted band
# controls (day002_fibonacci_control.py) prove that is a pure smooth-density
# artifact (independent of band phase); local scale: rho ~ 0 for all phases.
mask_c = np.isin(k_of, band_idx)
zi = np.where(mask_c)[0]
gaps_c = ts[zi + 1] - ts[zi]
uc_ = uc
scale = np.minimum(uc_, 1.0 - uc_)
local_c = gaps_c * (np.log(ts[zi] / (2.0 * math.pi)) / (2.0 * math.pi))
gm_c = gaps_c / gaps_c.mean()


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(np.float64)
    ry = np.argsort(np.argsort(y)).astype(np.float64)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    return float(np.sum(rx * ry) / math.sqrt(np.sum(rx * rx) * np.sum(ry * ry)))


rho_edge = spearman(scale, local_c)
rho_pos = spearman(uc_, local_c)
rg_edge = spearman(scale, gm_c)
rg_pos = spearman(uc_, gm_c)
n = len(gaps_c)
print("\n(iii) in-band position vs gap to next zero, complete bands, n = %d:" % n)
print("    PRIMARY scale (local density, g_i * (1/2pi) ln(t_i/2pi)):")
print("    Spearman rho( distance-to-nearer-band-edge , gap ) = %+.4f   (z = %+.2f)" % (rho_edge, rho_edge * math.sqrt(n - 1)))
print("    Spearman rho( in-band position u           , gap ) = %+.4f   (z = %+.2f)" % (rho_pos, rho_pos * math.sqrt(n - 1)))
print("    [artifact demo] global-mean scale: rho edge %+.4f (z %+.2f), rho pos %+.4f (z %+.2f)" % (rg_edge, rg_edge * math.sqrt(n - 1), rg_pos, rg_pos * math.sqrt(n - 1)))
print("    [phase controls show the artifact is band-phase independent: out_day002_fibonacci_control.txt]")
print("    (flag at |z| > 2.58)")

flag = (p < 0.01) or (md >= 3.0) or (abs(rho_edge) * math.sqrt(n - 1) > 2.58) or (abs(rho_pos) * math.sqrt(n - 1) > 2.58)
print("\nVERDICT: %s" % ("COUPLING SIGNAL DETECTED -- investigate." if flag
                        else "no Fibonacci coupling observed at T = 1e4 (complete-band counts, in-band position, and gap structure all within tolerance). Thread closed as a measured NULL; re-open only if a future census shows a complete-band signal."))
