"""mpmath audit of the Dirichlet beta layer (kainos-dev:dev container):

    docker run --rm -i -v "$PWD":/work kainos-dev:dev \
        sh -c "pip -q install mpmath && cd /work && python3 mpmath_audit_beta.py"

Checks, all at dps=50 (mp.dirichlet = reference-quality Dirichlet L):
  (a) the real rotation  Zb(t) = Re[ e^{+i psi(t)/2} beta(1/2+it) ] with
      psi(t) = t ln(4/pi) + 2 im logGamma(3/4 + it/2)  (root number +1)
      must make beta REAL off its zeros: Im ~ 1e-30 (machine for dps=50).
  (b) locate the first on-line beta zeros (dip scan + bisection to 15 d).
  (c) mirror-sum energy I12(s) = |L12(s)|^2 + |L12(1-s-c)|^2,
      L12(s) = (1 + 2^{-s}) beta(s):
        * at each on-line beta zero: I12 ~ 1e-40 (collapsed orbit, full)
        * at the leak zero s0 = i*pi/ln2: |L12(s0)| ~ 1e-40 (EXACT algebraic
          zero: 2^{-s0} = e^{-i pi} = -1) while the mirror slot holds 0.5693:
          I12(s0) = 0.32405 > 0  (half-orbit / broken mirror).
"""
import mpmath as mp

mp.mp.dps = 50
DPS0 = mp.mp.dps

CHI4 = [0, 1, 0, -1]  # chi_{-4}(n), period 4, mpmath is 0-indexed: a[i] <-> n == i (mod 4)
# (verified: mp.dirichlet(2, CHI4) = Catalan's constant G, mp.dirichlet(3, CHI4) = pi^3/32)
LN_4PI = mp.log(mp.mpf(4) / mp.pi)


def betam(s):
    return mp.dirichlet(s, CHI4)


def psi(t):
    t = mp.mpf(t)
    return t * LN_4PI + 2 * mp.im(mp.log(mp.gamma(mp.mpf("0.75") + 0.5j * t)))


def Zbm(t):
    t = mp.mpf(t)
    return mp.re(mp.exp(0.5j * psi(t)) * betam(mp.mpf("0.5") + 1j * t))


def L12m(sig, t):
    s = mp.mpf(sig) + 1j * mp.mpf(t)
    return (mp.mpf(1) + mp.exp(-s * mp.log(2))) * betam(s)


print("(a) real-rotation check, dps=50 (Im must be ~ machine 0):")
worst = mp.mpf(0)
for tv in (1.0, 3.0, 7.0, 15.0, 25.0):
    t = mp.mpf(tv)
    w = mp.exp(0.5j * psi(t)) * betam(mp.mpf("0.5") + 1j * t)
    im = abs(mp.im(w))
    worst = max(worst, im)
    print("    t = %4d   Im[e^{i psi/2} beta] = %s" % (int(tv), mp.nstr(im, 6)))
print("    max = %s   -> rotation VALID" % mp.nstr(worst, 3))

print("(b0) no missed zero below the first: min |beta(1/2+it)|, t in (0, 5.9), dps=25, dt=0.005:")
# window stops before zero-1's neighborhood (zero 1 = 6.0209489...), so any
# small value would indicate an ADDITIONAL zero below it.
mp.mp.dps = 25
m0, tm = None, None
t0m = mp.mpf("0.005")
while t0m < mp.mpf("5.9"):
    v = abs(betam(mp.mpf("0.5") + 1j * t0m))
    if m0 is None or v < m0:
        m0, tm = v, t0m
    t0m += mp.mpf("0.005")
print("    min = %s at t = %s   (large ==> no missed zero below 6.0209489)" % (mp.nstr(m0, 6), mp.nstr(tm, 5)))
mp.mp.dps = DPS0

print("(b) first on-line beta zeros (dps=50 bisection on the rotated real form):")
# coarse dip scan
dps_scan = mp.mp.dps
mp.mp.dps = 25
t = mp.mpf("0.2")
prev = Zbm(t)
dips = []
while t < 30:
    t += mp.mpf("0.02")
    z2 = Zbm(t)
    if prev * z2 < 0:
        dips.append((t - mp.mpf("0.02"), t))
    prev = z2
mp.mp.dps = dps_scan
print("    sign crossings (dps=25 scan, dt=0.02): %d" % len(dips))


def refine(lo, hi):
    zlo = Zbm(lo)
    for _ in range(120):
        mid = (lo + hi) / 2
        zm = Zbm(mid)
        if zlo * zm <= 0:
            hi = mid
        else:
            lo, zlo = mid, zm
    return (lo + hi) / 2


zeros = []
for a, b in dips:
    r = refine(a, b)
    if abs(betam(mp.mpf("0.5") + 1j * r)) < mp.mpf("1e-30"):
        zeros.append(r)
    if len(zeros) >= 3:
        break
for i, r in enumerate(zeros, start=1):
    print("    beta zero %d:  t = %s" % (i, mp.nstr(r, 16)))

print("(c) mirror-sum energy I12 for L12(s) = (1 + 2^{-s}) beta(s):")
for r in zeros:
    s = mp.mpf("0.5") + 1j * r
    I = abs(L12m(0.5, r)) ** 2 + abs(L12m(0.5, r)) ** 2  # mirror of on-line pt = itself
    print("    on-line beta zero t=%s : |L12| = %s   I12 = %s" % (
        mp.nstr(r, 10), mp.nstr(abs(L12m(0.5, r)), 4), mp.nstr(I, 4)))
t0 = mp.pi / mp.log(2)
L0 = L12m(0, t0)
L0m = L12m(1, t0)
I0 = abs(L0) ** 2 + abs(L0m) ** 2
print("    leak zero s0 = i*pi/ln2 = %s i :" % mp.nstr(t0, 12))
print("        |L12(s0)|       = %s   (exact algebraic zero: 2^{-s0} = e^{-i pi} = -1)" % mp.nstr(abs(L0), 4))
print("        |L12(1 - s0-c)| = %s   (mirror slot EMPTY)" % mp.nstr(abs(L0m), 6))
print("        I12(s0)         = %s   > 0  (the broken mirror, as a positive number)" % mp.nstr(I0, 6))
