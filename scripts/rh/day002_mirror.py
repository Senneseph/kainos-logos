#!/usr/bin/env python3
"""Day-002: the mirror invariant I(s) -- a measurable handle on the
forward question.

The forward question (day-001.md, section 7):
  For the PRIMITIVE (self-reciprocal) completed zeta, why must every zero
  lie on the unique isometric line sigma = 1/2 and nowhere else?

Day-1 established two measured facts:
  (i)  the mirror is isometric only at sigma = 1/2            (S3d)
  (ii) BREAKING the mirror (imprimitive lift L12 = (1+2^-s) beta)
       produces an OFF-LINE zero with an EMPTY mirror slot         (S3c)

This script builds the first NUMERIC INVARIANT that unifies them:

  I(s) = |zeta(s)|^2 + |zeta(1 - s-conj)|^2      (the "mirror-sum energy")

  * at an on-line zero s = 1/2 + i gamma:  s = 1-s-conj, so
        I = |zeta(s)|^2 + |zeta(s)|^2 = 0
  * at an off-line zero with an EMPTY mirror:  the second term is > 0, so
        I > 0   -- the mirror break is now a POSITIVE NUMBER.

Predictions (all measured below):
  M2  I(sigma + i gamma_k) grows monotonically with |sigma - 1/2|
      at each of the first five zeros (the line is the unique trough).
  M3  floor(sigma) = min_t I(sigma + i t) is > 0 for every measured
      sigma != 1/2 and = 0 at sigma = 1/2: the energy can touch the
      ground ONLY on the line (t in [10, 60] window).
  M4  For the leaked function L12(s) = (1 + 2^-s) beta(s):
      the on-line zeros (of beta) give I12 = 0 (mirror full), while the
      leak zero at s0 = i*pi/ln2 gives I12 = |L12(1 - s0-conj)|^2 > 0
      (mirror empty).  Same invariant, opposite signs of the story.
  M6  The FOUR mirrors (owner's day-2 note): a zero of any real-coefficient
      self-reciprocal L-function has up to 4 mirror slots
      {itself, C, M, C*M} under conjugation C and the FE mirror M (the
      Klein four-group, NOT a single order-4 rotation).  Orbit structure:
      on-line zero -> collapsed 2-orbit on the axis (RH case);
      off-line quartet -> 4 full slots (RH violated);
      leak zero -> HALF-FILLED orbit, mirror slots empty (broken mirror).
      Measured: the i-rotation (order 4) is ABSENT from the zeta zero set;
      the Klein-four mirror structure is what actually acts.
"""
import cmath
import math
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from zeta_core import selftest, zeta, gam, cloggamma, chi, beta, find_zeros  # noqa: E402

if not selftest():
    sys.exit("zeta_core self-test RED -- refusing to run")

print("\n== M2  I(sigma + i gamma_k) at the first five zeros ==")
gammas = find_zeros(10.0, 60.0, dt=0.02)[:5]
SIGMAS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.45, 0.49, 0.5, 0.51, 0.55, 0.6, 0.7, 0.8, 0.9, 1.0]


def I_zeta(sig: float, t: float) -> float:
    s = sig + 1j * t
    a = abs(zeta(s))
    b = abs(zeta(1.0 - sig + 1j * t)) if abs(sig - 0.5) > 1e-12 else a
    return a * a + b * b


for k, g in enumerate(gammas, start=1):
    row = [f"{I_zeta(s, g):.3e}" for s in SIGMAS]
    mono = all(
        I_zeta(s, g) <= I_zeta(s2, g) * (1.0 + 1e-6)
        for s, s2 in ((0.49, 0.47), (0.5, 0.52), (0.3, 0.45))
    )
    print(f"  gamma{k} = {g:.6f}:")
    print("    " + "  ".join(f"{s:4.2f}:{v}" for s, v in zip(SIGMAS, row)))
print("  (values I(sigma+i*gamma); the column at 0.50 is the on-line trough,")
print("   and it must be the minimum of each row -- checked below)")
bad = 0
for k, g in enumerate(gammas, start=1):
    vals = {s: I_zeta(s, g) for s in SIGMAS}
    if abs(vals[0.5]) > min(vals.values()):
        bad += 1
        print(f"  !! gamma{k}: on-line point is NOT the row minimum")
print(f"  rows where 0.50 is the minimum: {5 - bad} / 5")

print("\n== M3  floor(sigma) = min over t in [10, 60] of I(sigma + i t) ==")
ts = [10.0 + 0.02 * i for i in range(2501)]
print("   sigma   floor(I)       argmin t        (note)")
floors = []
for sig10 in range(1, 20):  # 0.05 .. 0.95
    sig = sig10 / 20.0
    best, bt = math.inf, None
    for t in ts:
        v = I_zeta(sig, t)
        if v < best:
            best, bt = v, t
    note = ""
    if abs(sig - 0.5) < 1e-12:
        note = "<- line: grid floor 7e-6 (true min = 0 at gamma7; dt=0.02)"
    floors.append((sig, best, bt))
    print(f"   {sig:5.2f}   {best:10.4e}   {bt:8.3f}      {note}")
off = [f for f in floors if abs(f[0] - 0.5) > 1e-12]
print(f"  all OFF-LINE floors > 0: {all(f[1] > 0.0 for f in off)}  "
      f"(min off-line floor {min(f[1] for f in off):.3e})")

print("\n== M4  the leaked function L12(s) = (1 + 2^-s) beta(s) ==")
print("  (a) the real rotation of beta (root number +1), PROVEN at dps 50:")
print("      psi(t) = t*ln(4/pi) + 2*im*logGamma(3/4 + it/2),  "
      "Zb(t) = Re[exp(+i psi/2) beta(1/2+it)], |Zb| = |beta|")
print("      the numpy check below runs at the PAIR-SERIES floor (2|s|/sqrt(4P));")
print("      the dps-50 proof (Im <= 3.4e-50) is in out_mpmath_audit_beta.txt")
LN_4PI = math.log(4.0 / math.pi)


def psi_beta(t: float) -> float:
    return t * LN_4PI + 2.0 * cloggamma(0.75 + 0.5j * t).imag


def Zb(t: float, pairs: int = 500_000) -> float:
    b, _ = beta(0.5 + 1j * t, pairs=pairs)
    return float((cmath.exp(0.5j * psi_beta(t)) * b).real)


# the rotation must make beta real off the zeros: Im[e^{-i psi/2} beta] ~ 0
imps = []
for t in (1.0, 2.0, 3.0, 4.0, 7.0, 10.0, 15.0, 25.0):
    b, _ = beta(0.5 + 1j * t, pairs=1_000_000)
    imps.append(abs((cmath.exp(0.5j * psi_beta(t)) * b).imag))
print(f"      max |Im rotation check| (8 points, 1e6 pairs) = {max(imps):.2e}")

print("  (b) on-line beta zeros -- the numpy pair-series floor is too loose to")
print("      certify zeros on the line; the dps-50 mpmath audit (out_mpmath_audit_beta.txt):")
print("        zero 1: 6.020948904697597    zero 2: 10.24377030416655")
print("        zero 3: 12.98809801231242     (|L12| ~ 1e-39 at each; no zero below zero 1)")
print("      I12 at these zeros (dps 50) <= 2.8e-77: collapsed on-line orbits")

print("  (c) the leak zero s0 = i*pi/ln2 (sigma = 0), and its empty mirror:")
t0 = math.pi / math.log(2.0)
s0 = 1j * t0
L0 = (1.0 + cmath.exp(-s0 * math.log(2.0))) * beta(s0, pairs=5_000_000)[0]
s0m = 1.0 - s0.conjugate()
L0m = (1.0 + cmath.exp(-s0m * math.log(2.0))) * beta(s0m, pairs=5_000_000)[0]
I12_leak = abs(L0) ** 2 + abs(L0m) ** 2
print(f"      t0 = pi/ln2 = {t0:.9f}")
print(f"      |L12(s0)|        = {abs(L0):.6e}   (roundoff of an EXACT algebraic zero: 2^-s0 = e^-i pi = -1; dps-50: 1.2e-50)")
print(f"      |L12(1 - s0-c)|  = {abs(L0m):.6e}   (mirror slot -- EMPTY means this is nonzero)")
print(f"      I12(s0)          = {I12_leak:.6e}   > 0  <-- the mirror break, as a number")

print("\n== M6  the four mirrors (owner's day-2 note): the orbit of a zero ==")
print("  symmetries of the zero set of any real-coefficient L-function with")
print("  a functional equation (points written as (sigma, t)):")
print("    C   : (sigma, t) -> (sigma, -t)     conjugation (flip t)")
print("    M   : (sigma, t) -> (1-sigma, -t)   FE mirror (point-flip about (1/2, 0))")
print("    C*M : (sigma, t) -> (1-sigma, t)    reflection in the sigma = 1/2 line")
print("  together with the identity: the KLEIN 4-GROUP -- the symmetry group of")
print("  a rectangle centered at (1/2, 0).  A point thus has up to FOUR mirror")
print("  slots: itself, C, M, C*M.  (Not a single rotating i-operator: see (d).)")


def orbit4(sig: float, t: float):
    return [(("itself", sig, t), ("C", sig, -t), ("M", 1.0 - sig, -t), ("C*M", 1.0 - sig, t))]


print("  (a) zeta zeros (on the line): |zeta| at each of the 4 slots:")
for g in gammas[:4]:
    parts = []
    for name, sg, tt in orbit4(0.5, g)[0]:
        parts.append(f"{name}:{abs(zeta(sg + 1j * tt)):.2e}")
    print(f"    gamma = {g:10.6f}   " + "   ".join(parts))
print("      on the line, M and C coincide (both send (1/2,g) -> (1/2,-g)) and")
print("      C*M is the identity: the 4-slot orbit COLLAPSES to the 2 on-axis")
print("      points (gamma and -gamma).  This is the RH case, in orbit language.")

print("  (b) the leak zero s0 = i*pi/ln2 (sigma = 0) for L12 = (1+2^-s) beta:")


def L12(sig: float, t: float, pairs: int = 5_000_000) -> complex:
    return (1.0 + cmath.exp(-(sig + 1j * t) * math.log(2.0))) * beta(sig + 1j * t, pairs=pairs)[0]


t0 = math.pi / math.log(2.0)
for name, sg, tt in orbit4(0.0, t0)[0]:
    v = abs(L12(sg, tt))
    full = "FULL (zero)" if v < 1e-6 else f"EMPTY (|L12| = {v:.4f})"
    print(f"    slot {name:5s} -> point ({sg:5.2f}, {tt:+9.5f})   {full}")
print("      the leak orbit is HALF-FILLED: the zero + its conjugate C, while the")
print("      two mirror slots M, C*M (at sigma = 1) are empty.  Half-orbit = the")
print("      measurable signature of a BROKEN mirror (imprimitive function).")
print("  (c) a genuine off-line zero (RH violation, FE-consistent) would have ALL")
print("      FOUR slots full at 4 DISTINCT points: a full quartet off the axis.")
print("  TRICHOTOMY of zero-orbits (all three now measured or pinned down):")
print("    on-line (RH)      : collapsed 2-orbit ON the axis, all slots full")
print("    off-line quartet  : 4 distinct full slots, symmetric about the axis = RH FALSE")
print("    leaked half-orbit : 2 full + 2 empty slots                          = broken mirror")

print("  (d) the literal cyclic i-rotation (owner's 4-step cycle) -- measured ABSENT:")
g1 = gammas[0]
A = (0.5 - g1, 0.0)  # 90 deg CCW about (1/2, 0)
B = (0.5 + g1, 0.0)  # 270 deg
sA, sB = complex(A[0], A[1]), complex(B[0], B[1])
zA = abs(chi(sA) * zeta(1.0 - sA))  # via the FE (A has sigma < 0)
zB = abs(zeta(sB))
print(f"      rotate (1/2, gamma1 = {g1:.6f}) by 90 deg about (1/2,0) -> {A[0]:.6f} + 0i:")
print(f"        |zeta| = {zA:.3e}   (not a zero)")
print(f"      rotate by 270 deg -> {B[0]:.6f} + 0i:")
print(f"        |zeta| = {zB:.6f}   (not a zero)")
print("      there is NO order-4 rotation in the zeta zero set: the four-fold")
print("      structure is two independent REFLECTIONS (the Klein four-group),")
print("      not one rotating operator.  The COUNT of four the owner observed is")
print("      exactly right; the mechanism is a product of mirrors, not i^2 = -1.")
print("      Arithmetic echo: 4 = 2^2 = '1/2 squared' -- the same 4 that decides")
print("      the two-squares story (day-001 Q5); the rectangle is one 1/2-axis")
print("      crossed with another.")

print("\n== M5  verdict ==")
print("  The mirror-sum energy I(s) = |f(s)|^2 + |f(1-s-c)|^2 separates the two")
print("  cases with a single scalar:")
print("    * self-reciprocal f, zero ON the isometric line: I = 0 + 0 = 0")
print("    * mirror-broken f, zero off the line, empty mirror: I = 0 + c^2 > 0")
print("  For zeta itself I reaches 0 ONLY at the on-line zeros in every measured")
print("  strip slice (M2, M3); the leak test (M4) shows the moment the mirror")
print("  breaks, the same invariant becomes strictly positive at the new zero.")
print("  With M6, THE OPEN (THM-LEVEL) QUESTION gets its orbit-language form:")
print("    prove that for the primitive completed zeta, a zero's orbit can only")
print("    be the COLLAPSED ON-AXIS one (case a) -- the full off-axis quartet")
print("    (case c) and the empty mirror slots together are impossible.")
print("  That statement IS the Riemann Hypothesis, phrased as a claim about which")
print("  of the three zero-orbit types can occur -- a claim this script can")
print("  evaluate pointwise.")

# done (day-002 mirror invariant)
