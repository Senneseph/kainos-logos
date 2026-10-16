#!/usr/bin/env python3
"""Day-005: Fibonacci primitive-prime band density (the owner's 12/24 thread,
made quantitative).  For each n, factor F_n (fast doubling, Miller-Rabin,
Pollard rho), collect the PRIMITIVE prime divisors (ord_p(phi) = n), and
measure the band reciprocal sum B[n] = sum_{p primitive for n} 1/p.
Benchmarks: (a) cumulative S(N) = sum_{n<=N} B[n] — log-divergent
(c * ln N, L-layer pole behavior) vs saturated (collective constant);
(b) Frobenius AP picture: primitive primes of F_n sit in the classes
ord_p(phi) = n (i.e. p ≡ 1 mod n, up to the (5/p) split), so
B[n] ~ (2/phi(5n)) * ln(ln F_n) ~ (2/phi(5n)) * (ln n - .73).
Zsigmondy exceptions (no primitive prime): n = 1, 2, 6, 12 (F_6 = 8,
F_12 = 144) — expect B = 0 there.  Run: python3 day005_band_density.py
"""
import math
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(10000)
t_start = time.time()
PHI = (1 + math.sqrt(5)) / 2

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return (n, 1)   # fib(0) = (F_0, F_1) = (0,1); fib(1) = (F_1, F_2) = (1,1)
    a, b = fib(n >> 1)
    c = a * (2 * b - a)
    d = a * a + b * b
    if n & 1:
        return d, c + d
    return c, d


def F(n):
    return fib(n)[0]


def is_prime(n):
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n):
    if n % 2 == 0:
        return 2
    while True:
        x, y, c, d = 2, 2, 1, 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d
        c += 1


def factor(n):
    out = []
    stack = [n]
    ps = [p for p in range(3, 2000, 2) if is_prime(p)]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        # trial division by small primes first
        for p in ps:
            if p * p > m:
                break
            while m % p == 0:
                out.append(p); m //= p
        if m > 1:
            if is_prime(m):
                out.append(m)
            else:
                d = pollard_rho(m)
                stack += [d, m // d]
    return out


def order_of_phi(p, n):
    """ord_p(phi) assuming p | F_n; returns the exact order (a divisor of n)."""
    def fibmod(n_, p_):
        a_, b_ = 0, 1
        for bit in bin(n_)[2:]:
            c = a_ * (2 * b_ - a_) % p_
            d = (a_ * a_ + b_ * b_) % p_
            if bit == '0':
                a_, b_ = c, d
            else:
                a_, b_ = d, (c + d) % p_
        return a_
    if fibmod(n, p) != 0:
        return None
    # ord divides n: check proper divisors via prime factors of n
    def psf(m):
        rs = []
        q = 2
        while q * q <= m:
            if m % q == 0:
                rs.append(q)
                while m % q == 0:
                    m //= q
            q += 1 if q == 2 else 2
        if m > 1:
            rs.append(m)
        return rs
    ord_ = n
    for q in psf(n):
        while ord_ % q == 0 and fibmod(n // q, p) % p == 0:
            ord_ //= q
    return ord_


def phi_func(n):
    r, m = n, n
    q = 2
    while q * q <= m:
        if m % q == 0:
            r = r // q * (q - 1)
            while m % q == 0:
                m //= q
        q += 1 if q == 2 else 2
    if m > 1:
        r = r // m * (m - 1)
    return r


NMAX = 100
bands = {}     # n -> list of primitive primes
total = 0.0
print("n   digits(F_n)  #fac  #prim   B[n]=sum 1/p     phi(5n)  B*phi(5n)/2   ln n - 0.73")
for n in range(3, NMAX + 1):
    fn = F(n)
    fs = sorted(set(factor(fn)))
    prims = []
    for p in fs:
        if p in (2, 5):
            continue
        o = order_of_phi(p, n)
        if o == n:
            prims.append(p)
    if prims:
        bands[n] = prims
    B = sum(1.0 / p for p in prims)
    total += B
    ph = phi_func(5 * n)
    bench = math.log(n) - 0.73
    print("%3d   %11d   %3d   %5d   %.6e   %6d    %10.4f      %9.4f%s"
          % (n, len(str(fn)), len(fs), len(prims), B, ph, B * ph / 2, bench,
             "   <== Zsigmondy exception" if n in (6, 12) else ""))
    if n % 10 == 0:
        print("    [cumulative S(%d) = %.5f]" % (n, total))
# cumulative growth exponent fit: S(N) ~ N^alpha (alpha 0 = log-ish divergence)
import numpy as np
Ns = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
Ss = [sum(1.0 / p for k in range(3, N + 1) for p in bands.get(k, [])) for N in Ns]
bl = [math.log(x) for x in Ns]
br = [math.log(x) for x in Ss]
a, b = float(np.polyfit(bl, br, 1)[0]), float(np.polyfit(bl, br, 1)[1])
print("\ncumulative S(N): exponent fit S ~ N^a:  a = %.4f  (a = 0 -> log-divergent L-layer; a < 0 -> saturated)" % a)
for N, S in zip(Ns, Ss):
    r = math.log(S / math.log(N)) / math.log(N) if S > 0 else float('nan')
    print("  S(%3d) = %.5f   S/ln N = %.5f   local ratio d S/d ln N / S = %.3f" % (N, S, S / math.log(N), r))
print("\ntotal %.0f s" % (time.time() - t_start))
