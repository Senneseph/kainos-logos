"""P-W.2, 3-point exact elimination (no LS).

y_i := c_tot_i + P(r) N_i  =  E + F z_i,   z_i = e^{-it ln N_i} / N_i.
From one triple (i, i+1, i+2):
    F = (y_i - y_{i+1}) / (z_i - z_{i+1})     [F cancels in ratios]
    E = y_i - F z_i
Two disjoint triples -> F_a, E_a, F_b, E_b; spreads = O(N^-2) diagnostic.
6 cuts, single forward pass for P, t = 10.
D-residual: max_i |y_i - E_avg - F_avg z_i| / N_0  ~  |D_true + P(r)|.
"""
import mpmath as mp
from fractions import Fraction

mp.mp.dps = 45

def make_chi(q, residues):
    sym = {j % q: (1 if j in residues else -1) for j in range(1, q)}
    sym[0] = 0
    return (lambda n: sym[n % q])

def p_cumul_table(chi, q):
    out = [0]
    a = 0
    for r in range(1, q):
        a += chi(r)
        out.append(a)
    return out

def l_exact(s, q, chi):
    return q ** (-s) * sum(chi(j) * mp.zeta(s, j / q) for j in range(1, q))

def table(q, chi, t, cuts):
    s = mp.mpf("0.5") + mp.j * t
    L = l_exact(s, q, chi)
    P = p_cumul_table(chi, q)
    xmax = max(cuts) + q
    acc = mp.mpc(0)
    P_at = {cut: {} for cut in cuts}
    for k in range(1, xmax + 1):
        acc += chi(k) * mp.power(mp.mpf(k), -s)
        for cut in cuts:
            if cut <= k < cut + q:
                P_at[cut][k - cut] = acc
    print(f"q={q} t={t}")
    for r in range(q):
        y, z = [], []
        for c in cuts:
            c_tot = mp.mpf(c) ** (s + 1) * (L - P_at[c][r])
            y.append(c_tot + P[r] * mp.mpf(c))
            z.append(mp.exp(-mp.j * t * mp.log(mp.mpf(c))) / mp.mpf(c))
        Fa = (y[0] - y[1]) / (z[0] - z[1]); Ea = y[0] - Fa * z[0]
        Ea2 = y[2] - Fa * z[2]
        Fb = (y[2] - y[3]) / (z[2] - z[3]); Eb = y[2] - Fb * z[2]
        Eb2 = y[4] - Fb * z[4]
        Favg = (Fa + Fb) / 2; Eavg = (Ea + Ea2 + Eb + Eb2) / 4
        resid = max(abs(yi - Eavg - Favg * zi) for yi, zi in zip(y, z)) / mp.mpf(cuts[0])
        qe = Eavg / s
        fr = Fraction(mp.nstr(qe.real, 12)).limit_denominator(60)
        print(f"  r={r:2d}: P={P[r]:3d}  E/s={mp.nstr(qe, 14)} ~= {float(fr):.6f} ({fr})"
              f"  |E/s-fr|={mp.nstr(abs(qe - fr), 5)}")
        print(f"        |F_a|={mp.nstr(abs(Fa), 7)} |F_b|={mp.nstr(abs(Fb), 7)}"
              f"  Fspread={mp.nstr(abs(Fa - Fb), 5)}  Esprad={mp.nstr(abs(Ea - Eb), 5)}"
              f"  Dresid={mp.nstr(resid, 5)}")
    print()

def cut_chain(base, steps):
    out = []
    n = base
    for _ in range(steps):
        out.append(n)
        n = n * 6 // 5
    return out

chi5 = make_chi(5, [1, 4])
chi13 = make_chi(13, [1, 3, 4, 9, 10, 12])
cuts5 = cut_chain(50_000, 5)   # 50000..103680, all * 5
cuts13 = cut_chain(65_000, 5)  # 65000..134784, all * 13
print("cuts5:", cuts5, "mod 5:", [c % 5 for c in cuts5])
print("cuts13:", cuts13, "mod 13:", [c % 13 for c in cuts13])
print("=== chi_5 control (expect E/s in {+2/5, -3/5}, Dresid ~ 0) ===")
table(5, chi5, 10, cuts5)
print("=== chi_13 ===")
table(13, chi13, 10, cuts13)
