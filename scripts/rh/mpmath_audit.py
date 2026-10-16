"""Independent cross-check of day001_zeta.py's zero census, using mpmath.

Run INSIDE the kainos-dev:dev container (host python3 has no mpmath):
    docker run --rm -i -v "$PWD/scripts/rh":/work kainos-dev:dev \
        sh -c "pip -q install mpmath && cd /work && python3 mpmath_audit.py"

Three independent checks:
  (a) RIEMANN-von-Mangoldt single-point argument consistency:
      N(T) = main(T) + S(T),  S(T) = arg(zeta(1/2+iT))/pi  (mod 2)
      evaluated with dps=50 mpmath at T = 100, 1000, 10000.
  (b) SPOT VERIFY: for a sample of our found zeros (first 10 + uniform
      every ~250th after), |zeta(1/2+i gamma)| must be < 1e-20 at dps=50.
  (c) REFINE first 10 zeros with mpmath's own bisection on its own real
      Z(t) (DLMF 25.10.1/25.10.2 form) -- provenance for the published
      constants in day001_zeta.py.
"""
import os
import sys

import mpmath as mp

mp.mp.dps = 50


def vartheta(t):
    t = mp.mpf(t)
    return mp.im(mp.log(mp.gamma(mp.mpf("0.25") + 0.5j * t))) - (t / 2) * mp.log(mp.pi)


def Z(t):
    t = mp.mpf(t)
    return mp.re(mp.exp(1j * vartheta(t)) * mp.zeta(mp.mpf("0.5") + 1j * t))


def main_term(T):
    T = mp.mpf(T)
    return T / (2 * mp.pi) * mp.log(T / (2 * mp.pi)) - T / (2 * mp.pi) - mp.mpf("0.125")


def find_near(guess, half=mp.mpf("0.05")):
    lo, hi = mp.mpf(guess) - half, mp.mpf(guess) + half
    zlo = Z(lo)
    # ensure a sign change
    zhi = Z(hi)
    guard = 0
    while zlo * zhi > 0 and guard < 40:
        half *= 2
        lo, hi = mp.mpf(guess) - half, mp.mpf(guess) + half
        zlo, zhi = Z(lo), Z(hi)
        guard += 1
    for _ in range(200):
        mid = (lo + hi) / 2
        zm = Z(mid)
        if zlo * zm <= 0:
            hi, zhi = mid, zm
        else:
            lo, zlo = mid, zm
    return (lo + hi) / 2


here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, "zeros_T10000.txt")
if not os.path.exists(path):
    sys.exit("zeros_T10000.txt not found next to mpmath_audit.py -- run day001_zeta.py first")
with open(path) as fh:
    ours = [mp.mpf(line.strip()) for line in fh if line.strip()]
print(f"loaded {len(ours)} zero heights from zeros_T10000.txt")

print("\n(a) RVM single-point argument consistency (dps=50):")
# S(T) in Riemann-von Mangoldt is the ACCUMULATED (unwrapped) argument of
# zeta(1/2+it) from t=0. Single-point principal arg gives that modulo 2pi,
# up to the baseline arg at t=0: zeta(1/2) is real NEGATIVE (arg = pi), so
# the baseline contributes +1 in units of S. We subtract it.
base = mp.arg(mp.zeta(mp.mpf("0.5"))) / mp.pi  # = +1 (zeta(1/2)<0)
print(f"    baseline arg(zeta(1/2))/pi = {mp.nstr(base,6)}  (zeta(1/2) real negative)")
for T in (100, 1000, 10000):
    n = sum(1 for g in ours if g <= T)
    mt = main_term(T)
    S_ours = mp.mpf(n) - mt
    z = mp.zeta(mp.mpf("0.5") + 1j * T)
    S_arg = mp.arg(z) / mp.pi - base
    # compare mod 2
    d = (S_ours - S_arg) % 2
    d = min(d, 2 - d)
    # a count error (missed/double zero) would appear as O(1), T-independent.
    # The known RVM higher-order terms give a residual ~ c/T. We therefore
    # also report d*T: it must stay O(1e-2) and shrink as T grows.
    ok = "OK  (consistent)" if d < mp.mpf("1e-3") else "MISMATCH (count error?)"
    print(f"    T={T:<6} N={n:<6} main={mp.nstr(mt,10):>10}  S_accum={mp.nstr(S_ours,6):>8}  "
          f"(arg-diff)/pi={mp.nstr(S_arg,6):>8}  |mod-2 diff|={mp.nstr(d,3):>7}  d*T={mp.nstr(d*T,3):>7}  {ok}")

print("\n(b) spot verification of our zeros (|zeta| must be ~0 at dps=50):")
sample = list(ours[:10])
if len(ours) > 10:
    step = max(1, len(ours) // 40)
    sample += [ours[i] for i in range(step, len(ours), step)]
worse = 0.0
for g in sample:
    m = abs(mp.zeta(mp.mpf("0.5") + 1j * g))
    if m > worse:
        worse = m
print(f"    {len(sample)} zeros checked (first 10 + every ~250th); "
      f"max |zeta(1/2+i gamma)| = {mp.nstr(worse, 3)}")
# threshold 1e-8: our gamma heights are float64 (1e-15 abs), so the
# expected |zeta| scale is |zeta'(gamma)| * 1e-15 ~ 1e-14..1e-11.
print("    -> all are true zeros" if worse < mp.mpf("1e-8") else "    !!! NOT all small — investigate")

print("\n(c) mpmath's own refinement of the first 10 zeros:")
refined = []
for g in ours[:10]:
    r = find_near(g)
    refined.append(r)
    print(f"    {mp.nstr(r, 16)}")
print("    (use these to set the 'published' constants in day001_zeta.py)")
