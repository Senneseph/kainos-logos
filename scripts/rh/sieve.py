"""Shared exact soil for the rh-attack numerics (Day-001+).

The store owns the line 0..84 and reasons about zeta finitely. This
module is the *attack* layer: large-scale exact prime structure
(numpy int64), no float until a named division. Everything here is
independently re-walkable (the store's own discipline).
"""
import math

import numpy as np


def sieve(n: int) -> np.ndarray:
    """is_prime boolean array, 0..n (exact, classical sieve)."""
    is_p = np.ones(n + 1, dtype=bool)
    is_p[:2] = False
    for p in range(2, math.isqrt(n) + 1):
        if is_p[p]:
            is_p[p * p::p] = False
    return is_p


def spf(n: int) -> np.ndarray:
    """smallest prime factor for 0..n (int64; 0 where prime or < 2)."""
    sp = np.zeros(n + 1, dtype=np.int64)
    for p in range(2, math.isqrt(n) + 1):
        if sp[p] == 0:  # p is prime
            sl = sp[p * p::p]
            sl[sl == 0] = p
    rem = np.nonzero((sp[2:] == 0))[0] + 2
    sp[rem] = rem  # primes know themselves
    sp[0] = sp[1] = 0
    return sp


def von_mangoldt(n: int) -> np.ndarray:
    """Lambda(n): log(p) if n = p^k (k >= 1), else 0 (float64)."""
    is_p = sieve(n)
    lam = np.zeros(n + 1, dtype=np.float64)
    primes = np.nonzero(is_p)[0]
    lam[primes] = np.log(primes.astype(np.float64))
    for p in primes:
        pk = int(p * p)
        while pk <= n:
            lam[pk] = np.log(float(p))
            pk *= int(p)
    return lam


def chebyshev_psi(n: int) -> np.ndarray:
    """psi(x) = sum_{k <= x} Lambda(k), psi[0] = 0."""
    return von_mangoldt(n).cumsum()


def pi_in_class(n: int, mod: int, rem: int) -> np.ndarray:
    """pi(x; mod, rem) = count of primes <= x with x == rem (mod m).
    Proper prefix count at EVERY x (forward-filled across residues)."""
    is_p = sieve(n)
    mask = np.zeros(n + 1, dtype=bool)
    mask[rem::mod] = True
    return np.cumsum((is_p & mask).astype(np.int64))


def twin_prime_pi(n: int) -> np.ndarray:
    """pi_2(x) = count of primes p <= x with p + 2 also prime.
    twin[i] = # twin pairs whose SMALLER prime is <= i."""
    is_p = sieve(n)
    t = (is_p[:-2] & is_p[2:]).astype(np.int64)  # length n-1, index = smaller prime
    twin = np.zeros(n + 1, dtype=np.int64)
    twin[: n - 1] = np.cumsum(t)
    twin[n - 1] = twin[n - 2]
    twin[n] = twin[n - 1]
    return twin


def twin_singular_series(p_max: int) -> float:
    """C2 = prod_{p > 2} p(p-2)/(p-1)^2 (the Hardy-Littlewood
    twin-prime constant; the 'missing term' of the naive prime series)."""
    is_p = sieve(p_max)
    c = 1.0
    for p in np.nonzero(is_p)[0]:
        if int(p) <= 2:
            continue
        c *= (p * (p - 2)) / float((p - 1) * (p - 1))
    return c


def two_squares_repr(p: int):
    """a, b with a^2 + b^2 = p (a <= b), or None. Exact integer walk."""
    for a in range(isqrt(p) + 1):
        b2 = p - a * a
        b = isqrt(b2)
        if b * b == b2:
            return (a, b)
    return None


def isqrt(x: int) -> int:
    return math.isqrt(x)


def v2(x: int) -> int:
    """2-adic valuation: how many times x splits evenly (down to odd)."""
    k = 0
    while x % 2 == 0:
        x //= 2
        k += 1
    return k


def fib_bands(upper: int):
    """Fibonacci bands [F_k, F_{k+1}). 1,1,2,3,5,8,... (F_1=F_2=1)."""
    a, b = 1, 1
    bands = []
    seen = set()
    while a <= upper:
        if a != 1 or 1 not in seen:
            bands.append((a, b))
        seen.add(a)
        a, b = b, a + b
        if b > upper:
            break
    # unique-ify and sort
    out, _seen = [], set()
    for a, b in bands:
        if a not in _seen:
            out.append((a, b))
            _seen.add(a)
    return out
