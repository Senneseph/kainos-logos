# day009_e7b1_g_s2.py — test 25.2.12 at s = 2 where zeta(2) = pi^2/6
# is known exactly and the product converges fast (no e^{t/gamma} blowup).
from mpmath import mp
mp.dps = 30
pi = mp.pi

g = []
with open("/work/scripts/rh/zeros_T100000.txt") as f:
    for line in f:
        try:
            v = float(line)
        except ValueError:
            continue
        g.append(v)

s = mp.mpf(2)
main = (2*pi)**s * mp.e**(-(1 + mp.euler/2)*s) / (2*(s - 1)*mp.gamma(s/2 + 1))
print("main(2) =", mp.nstr(main, 12))

# log-space, chunked fsum-like (mp.fsum over the log terms for safety)
terms_la = []
terms_ar = []
for gamma in g:
    for sgn in (1.0, -1.0):
        rho = mp.mpc(0.5, sgn*gamma)
        fac = (1 - s/rho) * mp.e**(s/rho)
        terms_la.append(mp.log(abs(fac)))
        terms_ar.append(mp.arg(fac))
la = mp.fsum(terms_la)
ar = mp.fsum(terms_ar) + mp.arg(main)
X = mp.e**la * mp.mpc(mp.cos(ar), mp.sin(ar))
Ztrue = mp.zeta(2)
print("zeta(2) =", mp.nstr(Ztrue, 14))
print("X(2)    =", mp.nstr(X, 14))
print("X-Z     =", mp.nstr(X - Ztrue, 8))
print("|X-Z|   =", mp.nstr(abs(X - Ztrue), 8))
print("la =", mp.nstr(la, 12))
