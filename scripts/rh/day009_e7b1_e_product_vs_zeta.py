# day009_e7b1_e_product_vs_zeta.py — the decisive value (not just arg)
# check of the 25.2.12 product against mpmath's zeta at a NON-zero
# height. If |X - zeta_mp| is small, the product's phase IS the zeta
# phase and e7b1_d's -3.8546 rad/rad is the true d arg zeta/dt there.
# Log-space accumulation (no overflow): la += Re log f, ar += arg f.
from mpmath import mp
mp.dps = 20

t0 = 14000.0
G = 100000.0  # all 138,065 zeros (both signs)
g = []
with open("/work/scripts/rh/zeros_T100000.txt") as f:
    for line in f:
        try:
            v = float(line)
        except ValueError:
            continue
        if v <= G:
            g.append(v)
print("zeros:", len(g))

def logX(t):
    s = mp.mpc(0.5, t)
    main = (2*mp.pi)**s * mp.e**(-(1 + mp.euler/2)*s) \
        / (2*(s - 1)*mp.gamma(s/2 + 1))
    la = mp.log(abs(main))
    ar = mp.arg(main)
    for gamma in g:
        for sgn in (1.0, -1.0):
            rho = mp.mpc(0.5, sgn*gamma)
            fac = (1 - s/rho) * mp.e**(s/rho)
            la += mp.log(abs(fac))
            ar += mp.arg(fac)
    return la, ar

la, ar = logX(t0)
X = mp.e**(mp.mpf(la)) * mp.mpc(mp.cos(ar), mp.sin(ar))
Z = mp.zeta(mp.mpc(0.5, t0))
print("X - Z =", mp.nstr(X - Z, 12))
print("|X-Z|/", "|Z| =", mp.nstr(abs((X - Z)/Z), 12))
print("arg X =", mp.nstr(mp.arg(X), 10), " arg Z =", mp.nstr(mp.arg(Z), 10))

# fine-epsilon arg rate of BOTH (must agree if values agree)
eps = 0.05
la1, ar1 = logX(t0 + eps)
X1 = mp.e**(mp.mpf(la1)) * mp.mpc(mp.cos(ar1), mp.sin(ar1))
Z1 = mp.zeta(mp.mpc(0.5, t0 + eps))
print("darg X/dt =", mp.nstr((ar1 - ar0 if False else mp.arg(X1) - mp.arg(X))/eps, 8))
print("darg Z/dt =", mp.nstr((mp.arg(Z1) - mp.arg(Z))/eps, 8))
print("|X1-Z1|/|Z1| =", mp.nstr(abs((X1 - Z1)/Z1), 12))
