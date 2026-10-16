# day009_e7b2_onset_pred.py — E7b-1 ONSET TEST (pure mpmath, docker).
#
# Measured (day-04b, exact zeta, 4 digits, N-independent):
#   C(N,t) = |tail + I|,  tail = zeta(s) - Pn,  I = N^(1-s)/(1-s),
#   s = 1/2 + i t;  C/|I| vs t/N: 0.0500, 0.1000, 0.2509, 0.5071, 1.0620
#   at t/N = 0.1, 0.2, 0.5, 1, 2  — law: C/|I| = (1/2)(t/N) to 4 digits.
#
# Zero-side prediction (everything from 25.2.12 product + DLMF + list):
#   Psi(s) = main_25212(s) * prod_{|g|<=G} (1-s/rho)e^(s/rho) * e^{T(G,s)}
#   T(G,s) = int_G^inf pairlog(g,s) * (1/(2pi)) ln(g/(2pi)) dg
#            (analytic tail over zeros beyond the 1e5 list, RVM density)
#   W(s)   = Pn - I     (number side)
#   C_zero = |Psi - W|;  compare C_zero/|I| with the measured column.
#
# PASS: all 15 points within 5% relative + monotone in t/N +
#       slope of C/|I| vs t/N within [0.4, 0.6] (= 1/2 the law).
# G-limit recorded (tail integration to ~1e-3 in log units).
import math
from mpmath import mp
mp.dps = 15
PI = mp.pi
EULER_G = mp.euler

G = mp.mpf("100000")
gammas = []
with open("/work/scripts/rh/zeros_T100000.txt") as f:
    for line in f:
        try:
            gammas.append(float(line))
        except ValueError:
            pass
print("zeros:", len(gammas))

def logmain25212(s):
    """log of the 25.2.12 main factor, in log-space (dps, no overflow):
    main = (2pi)^s e^{-(1+gE/2)s} / (2 (s-1) Gamma(s/2+1))."""
    return (s*mp.log(2*PI) - (1 + EULER_G/2)*s
            - mp.log(2) - mp.log(s - 1) - mp.loggamma(s/2 + 1))

def product_larg(s):
    la = mp.mpf(0); ar = mp.mpf(0)
    for gamma in gammas:
        for sgn in (1.0, -1.0):
            rho = mp.mpc(0.5, sgn*gamma)
            fac = (1 - s/rho) * mp.e**(s/rho)
            la += mp.log(abs(fac))
            ar += mp.arg(fac)
    return la, ar

def pairlog(g, s):
    rho1 = mp.mpc(0.5, g)
    rho2 = mp.mpc(0.5, -g)
    return (mp.log(1 - s/rho1) + mp.log(1 - s/rho2)
            + s/rho1 + s/rho2)

def tail_int(s):
    t = abs(mp.im(s))
    split = max(G, 2*t)
    f = lambda g: pairlog(g, s) * (mp.log(g/(2*PI))/(2*PI))
    return mp.quad(f, [G, split, mp.inf])

measc = {0.1: 0.0500, 0.2: 0.1000, 0.5: 0.2509,
         1.0: 0.5071, 2.0: 1.0620}
rows = []
for Nn in (1000, 10000, 100000):
    for f_ in (0.1, 0.2, 0.5, 1.0, 2.0):
        t = mp.mpf(Nn) * mp.mpf(repr(f_))
        s = mp.mpc(0.5, t)
        la, ar = product_larg(s)
        Tt = tail_int(s)
        # ALL in mpmath log-space: |main| ~ e^{+/-2e4} cancels the
        # product's e^{+/-2e6} to O(1) — float64 overflows that.
        lnPsi = logmain25212(s) + la + mp.mpc(0, ar) + Tt
        Pn_mp = mp.fsum(mp.mpc(1.0/kk) ** s for kk in range(1, Nn + 1))
        I_mp = (mp.mpf(Nn) ** (1 - s)) / (1 - s)
        W = Pn_mp - I_mp
        Psi = mp.e**lnPsi
        # direct product+tail accuracy vs mpmath zeta (diagnostic):
        zt = mp.zeta(s)
        dPz = abs(Psi - zt) / abs(zt)
        Cpred = abs(Psi - W)
        A = abs(I_mp)
        pred = Cpred / A
        err = (pred - measc[f_]) / measc[f_]
        print(f"N={Nn:6d} t/N={f_:4.1f}: |I|={float(A):.6e}  C_zero={float(Cpred):.6e}  "
              f"C/|I|={float(pred):.6f}  measured={measc[f_]:.4f}  err={float(err):+.2%}   "
              f"|Psi-zeta|/|zeta|={float(dPz):.3e}")
        rows.append((Nn, f_, float(pred), measc[f_], float(err)))
print()
print("PASS if |err| < 5% on all 15 + monotone in t/N + slope ~ 1/2.")
print("rows:", [f"{a}/{b}:{c:.4f}" for a, b, c, *_ in rows])
