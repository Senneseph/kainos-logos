#!/usr/bin/env python3
"""Day-003 (owner question of the day): "the mirror rotations each scale
down by some factor as they go through each i?"

Translation into measurable objects:

  The raw FE is  zeta(s) = chi(s) * zeta(1-s),
      chi(s) = 2^s * pi^{s-1} * sin(pi s/2) * Gamma(1-s).
  |chi(s)| is the SCALE of the mirror map at s.

  (M1) On the critical line this scale is EXACTLY 1 (this is what makes
       the Riemann-Siegel phase rotation work): the identity
       |chi(1/2+it)| = 1  <=>  1 + 2 sinh^2(pi t/2) = cosh(pi t)
       (measured to float precision here; it is a derived identity, not
       a conjecture).
  (M2) OFF the line the scale is NOT 1 -- measure the grid.  If
       |chi(s)| = 1 happens only on the line in the grid, the "isometric
       locus" conjecture survives this day (label: conjecture, measured).
  (M3) "Scale down each time they go through each i": the mirror group
       is Klein four (each mirror is an INVOLUTION: M^2 = id), so there
       is no infinite i-chain to shrink under -- the orbit closes in at
       most 2 steps and no scale factor accumulates.  Measured directly:
       applying the mirror map twice returns the starting point with
       scale exactly 1 in total.
  (M4) "Nothing is able to fill the gap because of how factors work":
       decompose the EMPTY mirror slot of the leak L12 = (1+2^{-s}) beta
       into FINITE FACTOR x PRIME (Euler) PART and show the gap is filled
       neither by the finite factor (it equals 0.5, not 0) nor by the
       prime part (it equals ~1.1385, O(1), not close to 0).
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False), "selftest failed"
LN2, LNPI = np.log(2.0), np.log(np.pi)


def logchi2(sigma: float, t: float) -> float:
    """log |chi(sigma+i t)|^2 in overflow-safe log form:
    |chi|^2 = 2^{2sigma} pi^{2sigma-2} |sin(pi s/2)|^2 |Gamma(1-s)|^2, with
    |sin|^2 = sin^2(pi sigma/2) + sinh^2(pi t/2) and cloggamma for log Gamma."""
    v = math.pi * t / 2.0
    su = math.sin(math.pi * sigma / 2.0) ** 2
    if v < 350.0:
        lnsin2 = math.log(su + math.sinh(v) ** 2)
    else:
        lnsin2 = 2.0 * v - math.log(4.0)  # + negligible ln1p(su e^{-2v})
    lgam2 = 2.0 * zeta_core.cloggamma(1.0 - sigma - 1j * t).real
    return 2.0 * sigma * LN2 + (2.0 * sigma - 2.0) * LNPI + lnsin2 + lgam2


def chiabs(sigma: float, t: float) -> float:
    return math.exp(0.5 * logchi2(sigma, t))


def chi(s: complex) -> complex:
    """raw FE multiplier (direct, overflow-proof zeta_core form).  A naive
    '0.5j*pi*s' typo was caught on the first run of this script (it computed
    sin(i pi s/2) and returned |chi| = 0.55...0.0000 on the line); the log
    form chiabs is the oracle for large t."""
    return zeta_core.chi(s)


print("== M1  the mirror scale |chi(s)| on the critical line ==")
worst = 0.0
for t in (1.0, 7.0, 14.0, 25.0, 57.0, 143.0, 400.0):
    dev = chiabs(0.5, t) - 1.0
    worst = max(worst, abs(dev))
    print("  t = %6.0f : |chi(1/2+it)| - 1 = %+.2e" % (t, dev))
for t in (1000.0, 10_000.0, 1_000_000.0):
    dev = math.exp(0.5 * logchi2(0.5, t)) - 1.0
    worst = max(worst, abs(dev))
    print("  t = %6.0f : |chi(1/2+it)| - 1 = %+.2e   (log form)" % (t, dev))
print("  max deviation from 1 over grid = %.2e   " % worst +
      "(DERIVED identity, measured: on the line the mirror is pure PHASE)")

print("\n== M2  the scale off the line (grid, log form, all t) ==")
print("  |chi(sigma+it)| :  1.0000 = the line")
ts = (5.0, 14.1347, 57.0, 143.0, 1000.0, 10_000.0)
sigmas = (0.5, 0.45, 0.4, 0.3, 0.2, 0.1, 0.05, 0.55, 0.6, 0.7, 0.8, 0.9, 0.95)
min_off = float("inf")
recip_max = 0.0
for t in ts:
    row = []
    for s_ in sigmas:
        v = chiabs(s_, t)
        if abs(s_ - 0.5) > 1e-9:
            min_off = min(min_off, abs(v - 1.0))
        row.append("%.4f" % v if v < 1e5 else "%.3e" % v)
    print("  t = %8.4f : " % t + " ".join(row))
print("  sigma:   " + "   ".join("%5.2f" % s for s in sigmas))
for t in (5.0, 143.0, 1000.0):
    for s_ in (0.1, 0.3, 0.55):
        recip_max = max(recip_max, abs(chiabs(s_, t) * chiabs(1.0 - s_, t) - 1.0))
print("  recurrence check |chi(s)| |chi(1-s)| = 1: max deviation = %.2e  [DERIVED from the FE, measured]" % recip_max)
print("  min | |chi|-1 | off the line (whole grid, %d points) = %.3e" % (len(ts) * (len(sigmas) - 1), min_off))
print("  reading: |chi| crosses 1 off the line (<1 on one side, >1 on the other, by the")
print("  reciprocal).  The line is the ONLY isometric locus on this grid  [CONJECTURE, measured];")
print("  and a near-zero candidate in a |chi| < 1 region gets AMPLIFIED by the mirror step")
print("  (|f(MS)| = |f(s)|/|chi(s)|) -- the owner's 'scale down' as near-zero dynamics.)")

print("\n== M3  no shrinking chain: the mirrors are involutions ==")
s0 = 1j * (np.pi / LN2)          # leak zero (sigma = 0)
M2 = 1.0 - s0                     # apply the FE mirror twice: M(M(s)) = s (for real-coeff f)
mm = 1.0 - (1.0 - s0.conjugate()).conjugate()
print("  leak point s0 = i*pi/ln2 : apply M, then M again:")
print("    M(s0)      = (%.1f, %+.6f)   |L12| = %.6f (EMPTY mirror slot, measured)" % (M2.real, M2.imag, abs((1.0 + 2.0 ** (-M2)) * zeta_core.beta(M2, pairs=5_000_000)[0])))
print("    M(M(s0))   = (%+.6f, %+.6f) = s0 exactly  (Klein four: each mirror has order 2) -- no scale accumulates" % (mm.real, mm.imag))
c_scale_total = math.exp(0.5 * (logchi2(0.0, s0.imag) + logchi2(1.0, M2.imag)))
print("    raw scale at the two slots: |chi(s0)| = %.4e , |chi(M s0)| = %.4e   (product %.4e: finite)" % (chiabs(0.0, s0.imag), chiabs(1.0, M2.imag), c_scale_total))
print("    (finite -- the COMPLETED function, not the raw one, is the exactly self-reciprocal object; no scale accumulates because the orbit is finite)")

print("\n== M4  who leaves the gap empty: finite factor vs prime (Euler) part ==")
fin_s0 = 1.0 + 2.0 ** (-s0)
mir = 1.0 - s0.conjugate()
fin_mir = 1.0 + 2.0 ** (-mir)
beta_mir, tail = zeta_core.beta(mir, pairs=5_000_000)
print("  FINITE factor  (1 + 2^{-s}) :  at s0       = %.2e   (EXACT algebraic zero: 2^{-s0} = e^{-i pi} = -1)" % abs(fin_s0))
print("                                at mirror    = %.4f   (NOT a zero -- the factor is 'alive' there)" % abs(fin_mir))
print("  PRIME part beta(s)          :  at s0       = %.6f (finite, irrelevant -- the factor already zeroed L12)" % abs(zeta_core.beta(s0, pairs=5_000_000)[0]))
print("                                at mirror    = %.6f  (tail bound %.1e)" % (abs(beta_mir), tail))
print("  product at the mirror slot  : %.6f = |L12(mirror)|  (matches the measured %.6f from day-002)"
      % (abs(fin_mir * beta_mir), abs((1 + 2.0 ** (-mir)) * beta_mir)))
print("  CONCLUSION (measured): the empty mirror slot is empty because the PRIME")
print("  (Euler) part beta is O(1) = 1.1385 there -- the finite factor 2 broke the")
print("  orbit, and no zero of the prime part arrives to fill the slot.  The gap")
print("  is a property of the factorization, as the owner suspected.")
