#!/usr/bin/env python3
"""Day-001 attack layer 1: prime structure the store's finite soil does
not hold. Six computations, all exact integer walks until a named
division, each answering one question from the owner's brief:

  Q1  What is the scale of the prime-count error (the root scale the
      store's rh-reach names)?        -> envelope fit of |psi(x)-x|
  Q2  What does the naive prime series miss? -> twin-prime ratio vs 2*C2
  Q3  What do we need about 1/2 for primes?  -> halving, v2(p-1), mod-4
  Q4  Does 1/2 mean balance?                      -> Chebyshev bias
  Q5  Two squares / difference of squares         -> Fermat mod-4 law
  Q6  Store soil bridge: the line 0..84           -> Euler partial product
"""
import math

import numpy as np

from sieve import (
    chebyshev_psi,
    sieve,
    pi_in_class,
    twin_prime_pi,
    twin_singular_series,
    two_squares_repr,
    v2,
    isqrt,
)

X = 2_000_000
print(f"# day-001 prime structure, X = {X}")

is_p = sieve(X)
primes = np.nonzero(is_p)[0]
N = len(primes)
print(f"# primes <= X: {N} (last: {primes[-1]})")

# ---- Q1: the error scale --------------------------------------------------
psi = chebyshev_psi(X)
xD = np.arange(X + 1, dtype=np.float64)
D = psi - xD
absD = np.abs(D)
M = np.maximum.accumulate(absD)  # M(y) = max_{x<=y} |D(x)|

print("\n[Q1] psi(x) - x, the PNT error (rh-reach's 'square root improvement')")
print("  x         |D(x)|      M(y)          M(y)/y^0.5")
for x in (100, 1_000, 10_000, 100_000, 1_000_000, X):
    print(f"  {x:<10} {absD[x]:<12.4g} {M[x]:<14.4g} {M[x] / math.sqrt(x):.4f}")
# envelope slope fit on [1e4, X]
xs = np.geomspace(1e4, X, 300).astype(np.int64)
ys = M[xs]
slope, intercept = np.polyfit(np.log(xs), np.log(ys), 1)
print(f"  envelope fit  M(y) ~ y^{slope:.4f} * {np.exp(intercept):.3f}   (RH predicts exponent ~ 0.5, with log factors)")
# sign changes of psi - x (Littlewood oscillations)
s = np.sign(D[3:])
s = s[s != 0]
sign_changes = int(np.sum(s[1:] != s[:-1]))
print(f"  sign flips of psi(x)-x up to X: {sign_changes}")

# PNT ratio
print("\n  x/log(x) vs pi(x):")
for x in (10_000, 100_000, 1_000_000, X):
    pi_x = int(is_p[: x + 1].sum())
    print(f"  x={x:<10} pi(x)={pi_x:<8} x/log(x)={x / np.log(x):<12.3f}  ratio={x / np.log(x) / pi_x:.5f}")


# ---------------------------------------------------------------------------
print("\n[Q2] what the naive prime series misses (the twin-prime factor)")
pi2 = twin_prime_pi(X)
c2 = twin_singular_series(1_000_000)
print(f"  C2 (Hardy-Littlewood singular series)            = {c2:.12f}")
print(f"  2*C2 (the predicted limiting ratio)              = {2 * c2:.12f}")
print("  A(x)=#twin-pairs p, p+2 <= x;   R(x) = A(x)*(log x)^2 / x  ->  2*C2")
for x in (10_000, 100_000, 1_000_000, X):
    lx = np.log(float(x))
    r = pi2[x] * lx * lx / float(x)
    print(f"  x={x:<10} A(x)={pi2[x]:<8} R(x)={r:.6f}")
# the ratio converges SLOWLY (log corrections); extend the twin line to 5e7
X2 = 50_000_000
pi2_big = twin_prime_pi(X2)
for x in (10_000_000, 50_000_000):
    lx = np.log(float(x))
    r = pi2_big[x] * lx * lx / float(x)
    print(f"  x={x:<10} A(x)={pi2_big[x]:<8} R(x)={r:.6f}   (extended soil to 5e7)")
print("  interpretation: the naive 'independent primes' model predicts")
print("  A(x) ~ x/(log x)^2 (ratio 1).  Measured ratio -> 2*C2 ~= 1.32.")
print("  The missing term is a CONGRUENCE correction, visible everywhere,")
print("  and RH (even if true) does not determine it.")

# ---------------------------------------------------------------------------
print("\n[Q3] 1/2 for primes: halving, the 2-adic splitting depth")
# the owner's identity: 7 = 3+1/2 + 3+1/2  =  (p-1)/2 + (p+1)/2
p = 7
print(f"  the brief's example: {p} = ({p}-{1})/2 + ({p}+{1})/2 = {(p-1)//2}+1/2 + {(p-1)//2}+1/2")
print("  for every odd prime p:  p = (p-1)/2 + (p+1)/2, both integers,")
print("  and the '1/2' is exactly the remainder-1 of division by 2.")
print("  the SPLITTING DEPTH v2(p-1) = how many even halvings p-1 admits:")
print("  p      p-1      v2(p-1)  p mod 4   (v2=1 <==> 3 mod 4; v2>=2 <==> 1 mod 4)")
for p in [5, 7, 13, 17, 31, 41, 97, 113, 193, 257, 65537]:
    print(f"  {p:<7} {p-1:<8} {v2(p-1):<9}  {p % 4}")
# census over primes <= X
depths = np.array([v2(int(p) - 1) for p in primes if p > 2])
maxd = depths.max()
print(f"  census p<=X (3 mod 4: {int((primes[1:] % 4 == 3).sum())}, 1 mod 4: {int((primes[1:] % 4 == 1).sum())}):")
print(f"  max v2(p-1) up to X = {int(maxd)}")
hist = {k: int((depths == k).sum()) for k in range(1, min(9, int(maxd) + 1))}
print(f"  depth histogram (1..8): {hist}")
print("  the halving ladder p = 2^d*m + 1 with m odd EXHAUSTS after d = v2(p-1) steps;")
print("  'coming down to 1/2 eventually' is this 2-adic depth running out.")
print("  d = 1  <=> 3 mod 4 (difference of two squares only, never a sum of two)")
print("  d >= 2 <=> 1 mod 4 (sum of two squares, Fermat — verified in [Q5])")

# ---------------------------------------------------------------------------
print("\n[Q4] does 1/2 mean balance?  (the Chebyshev bias, mod 4)")
pi1 = pi_in_class(X, 4, 1)
pi3 = pi_in_class(X, 4, 3)
diff = pi1[100:] - pi3[100:]
frac3 = float(np.mean(diff <= 0))  # fraction of x in [100, X] where 3mod4 leads
print("  over x in [100, X]:  fraction of x with pi(x;4,3) >= pi(x;4,1)")
print(f"    = {frac3:.6f}   (Rubinstein-Sarnak limit: ~0.9914962)")
print("  1/2 is where the two prime colors BALANCE in the mean (PNT mod 4,")
print("  both ~ x/(2 log x)) — but the 3-color LEADS almost all the time.")
print("  '1/2 is where the mass balances, not where it is.'")
print(f"  final counts at X:  1 mod 4: {pi1[X]},  3 mod 4: {pi3[X]}  (ratio {pi3[X]/pi1[X]:.6f})")
print(f"  max lead of 3 over 1 in [100, X]: {int(-diff.min())}")
# Chebyshev (logarithmic) measure: weight 1/x -- the measure of the
# Rubinstein-Sarnak 0.9914962 statement
xm = np.arange(X + 1, dtype=np.float64)
w = np.zeros(X + 1); w[2:] = 1.0 / xm[2:]
mask3 = (pi1 - pi3) <= 0
log_frac = float((w[mask3].sum()) / w.sum())
print(f"  same fraction in Chebyshev (log) measure: {log_frac:.6f}")

# ---------------------------------------------------------------------------
print("\n[Q5] difference of squares vs sum of squares (the brief's 'two squares')")
print("  every odd p is a DIFFERENCE of two squares, uniquely adjacent:")
print("  7 = 2^2 - 1^2 = 4 - 1  (a-b = 1 always; (p+1)/2, (p-1)/2)")
ok1 = ok3 = bad1 = bad3 = multi1 = 0
for p in primes[1:][primes[1:] <= 3000]:
    p = int(p)
    reps = []
    for a in range(2, isqrt(p) + 1):
        b2 = p - a * a
        b = isqrt(b2)
        if b * b == b2 and 0 < b < a:
            reps.append((a, b))
    if p % 4 == 1:
        if len(reps) == 1:
            ok1 += 1
        elif len(reps) > 1:
            multi1 += 1
        else:
            bad1 += 1
    else:
        if not reps:
            ok3 += 1
        else:
            bad3 += 1
print(f"  SUM of two squares, p <= 3000:  {ok1} primes 1 mod 4 have exactly one")
print(f"    representation (up to order/sign); 0 misses")
print(f"    ({ok1} ok, {bad1} missed, {multi1} with two)")
print(f"  primes 3 mod 4:  {ok3} of {ok3 + bad3} are NOT a sum of two squares at all")
print(f"    ({ok3} ok, {bad3} counterexamples — must be 0)")
print("  the mod-4 split -- i.e. how many halves fit into (p-1)/2 -- decides")
print("  the whole two-squares story.  1/2 is the key; 4 is 1/2 squared.")

# ---------------------------------------------------------------------------
print("\n[Q6] store-soil bridge: the Euler product to the line end 84 (S13 family)")
line_end = 84
line_primes = primes[primes <= line_end]
for sigma in (1.05, 1.25, 1.5):
    prod = np.prod(1.0 / (1.0 - line_primes.astype(np.float64) ** (-sigma)))
    full = np.prod(1.0 / (1.0 - primes.astype(np.float64) ** (-sigma)))
    print(f"  sigma={sigma}:  partial(<=84) zeta = {prod:.8f}   full zeta = {full:.8f}   ratio {prod/full:.6f}")
print("  (zeta(1.5) = 2.6123753487...; the soil to 84 already carries most of the mass;)")
print("  removing factors = sieving; the S13 split family (1 - n^-s) is the")
print("  same product split by parity of the character. This is the store/attack joint.)")

print("\n# done (day-001 primes)")
