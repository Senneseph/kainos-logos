"""P-W.2, 3-term fit (robust version).

Tail expansion: T(r,N) = D N^{-s} + E N^{-s-1} + F N^{-s-2} + O(N^{-s-3}).
c_tot(r,N) := T N^{s+1} = D N + E + F e^{-it ln N} / N + O(N^{-2} e^{-2it ln N}).
The 1/N term's phase rotates 2 t ln(Nmax/Nmin) rad across the cut window,
so a plain (D,E) fit absorbs it (the 1.4-vs-0.4 chi_5 r=1 artifact).
Here: subtract D = -P(r) (Abel identity, confirmed), 2-term complex LS
fit of  y_i := c_tot_i + P(r) N_i  ~  E + F z_i,  z_i = e^{-it ln N_i}/N_i.
Outputs per phase: E/s (-> rational M1: P-W.1/2), |F| (= |M2 s(s+1)|:
P-W.3, the second width moment, unmeasured before), and the D-residual
(max |y_i - E - F z_i| / N_i  ~  |D_true + P(r)|).
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
    return out  # out[r] = P(r) = sum_{j=1..r} chi(j), r = 0..q-1

def l_exact(s, q, chi):
    return q ** (-s) * sum(chi(j) * mp.zeta(s, j / q) for j in range(1, q))

def two_term_fit(y, z):
    # y_i = E + F z_i  (complex LS, 2 params, exact)
    n = len(y)
    sum_zz = sum(zc * zc for zc, z in [(mp.conj(zj), zj) for zj in z])
    sum_z = sum(z)
    sum_ym = sum(y)
    sum_my_z = sum(yj * mp.conj(zj) for yj, zj in zip(y, z))
    den = n * sum_zz - sum_z * mp.conj(sum_z)
    F = (n * sum_my_z - sum_z * sum_ym) / den
    E = (sum_ym - F * sum_z) / n
    return E, F

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
    print(f"q={q} t={t}  (E/s should be rational; |F| = |M2| |s(s+1)|; "
          f"last col = |D_true + P(r)| residual)")
    for r in range(q):
        c_tot, z = [], []
        for c in cuts:
            c_tot.append(mp.mpf(c) ** (s + 1) * (L - P_at[c][r]))
            z.append(mp.exp(-mp.j * t * mp.log(mp.mpf(c))) / mp.mpf(c))
        y = [cj + P[r] * mp.mpf(c) for cj, c in zip(c_tot, cuts)]
        E, F = two_term_fit(y, z)
        resid = max(abs(yi - E - F * zi) for yi, zi in zip(y, z))
        resid = resid / mp.mpf(cuts[0])
        qe = E / s
        fr = Fraction(mp.nstr(qe.real, 12)).limit_denominator(60)
        print(f"  r={r:2d}: P={P[r]:3d}  E/s = {mp.nstr(qe, 14)}  ~= {float(fr):.6f} ({fr})"
              f"   |E/s-fr|={mp.nstr(abs(qe - fr), 5)}"
              f"   |F|={mp.nstr(abs(F), 8)}   Dresid={mp.nstr(resid, 5)}")
    print()

chi5 = make_chi(5, [1, 4])
chi13 = make_chi(13, [1, 3, 4, 9, 10, 12])
print("=== chi_5 control (expect E/s in {+2/5, -3/5}, Dresid ~ 0) ===")
table(5, chi5, 10, [200000, 400000, 800000, 1600000])
print("=== chi_13 (P-W.2: is E/s rational per phase?) ===")
table(13, chi13, 10, [200000, 400000, 800000, 1600000])
