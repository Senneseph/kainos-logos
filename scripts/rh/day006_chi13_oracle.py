"""P-W.2 falsifier: chi_13 missing-tail moment table M_1(r) = c_r/s.

c_r(s) := [ T(N,s) + P(r) N^{-s} ] N^{s+1},  T = sum_{n>N} chi13(n) n^{-s}
Exact L via Hurwitz: L(s, chi_13) = 13^{-s} sum_{j=1}^{12} chi(j) zeta_H(s, j/13).
T = L - P_N.  c_r should equal s * M_1(r, chi_13) + O(N^{-1}) with M_1 a
rational number (P-W.1/P-W.2(b)). Rationality test: reconstruct
c_r/s from the oracle value, limit_denominator(1000).
"""
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 40
Q = 13

def chi13(n: int) -> int:
    r = n % Q
    if r == 0:
        return 0
    return 1 if pow(r, (Q - 1) // 2, Q) == 1 else -1

def p_cumul(r: int) -> int:
    return sum(chi13(j) for j in range(1, r + 1))

def l13_exact(s):
    return Q ** (-s) * sum(
        chi13(j) * mp.zeta(s, j / Q) for j in range(1, Q)
    )

for t in (1, 10, 100):
    s = mp.mpf("0.5") + mp.j * t
    for nbase in (10_000, 40_000):
        print(f"t={t}  N={nbase}+r :")
        for r in range(Q):
            n = nbase + r
            # P_N direct (float-safe: chi values are small ints)
            p_n = sum(chi13(k) * mp.power(mp.mpf(k), -s) for k in range(1, n + 1))
            tail = l13_exact(s) - p_n
            c_r = (tail + p_cumul(r) * mp.power(mp.mpf(n), -s)) * mp.power(mp.mpf(n), s + 1)
            q = c_r / s
            fr = Fraction(mp.nstr(q.real, 12)).limit_denominator(1000)
            print(f"  r={r:2d}: |c|={mp.nstr(abs(c_r), 12):12s} arg={mp.nstr(mp.arg(c_r), 10):10s}"
                  f"   c/s = {mp.nstr(q.real, 12):12s} + {mp.nstr(q.imag, 8):8s} i"
                  f"   ~= {float(fr): .4f} ({fr})")
