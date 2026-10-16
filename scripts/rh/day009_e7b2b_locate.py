# day009_e7b2b_locate.py — localize the ~7.8% relative error at t=1e4.
# (A) G=5e4 vs G=1e5 (dps-15): if both ~7.8% -> not the (5e4,1e5] tail.
# (B) G=1e5 at dps-30: if error collapses -> dps-15 precision; if not ->
#     a real model error (density/tail approximation).
from mpmath import mp
PI = mp.pi
EULER_G = mp.euler
gammas = []
with open("/work/scripts/rh/zeros_T100000.txt") as f:
    for line in f:
        try:
            gammas.append(float(line))
        except ValueError:
            pass

def run(dps, Glimit):
    mp.dps = dps
    s = mp.mpc(0.5, mp.mpf("10000"))
    G = mp.mpf(int(Glimit))
    la = mp.mpf(0); ar = mp.mpf(0)
    for gamma in gammas:
        if gamma > Glimit:
            break
        for sgn in (1.0, -1.0):
            rho = mp.mpc(0.5, sgn*gamma)
            fac = (1 - s/rho) * mp.e**(s/rho)
            la += mp.log(abs(fac))
            ar += mp.arg(fac)
    def pairlog(g):
        r1 = mp.mpc(0.5, g); r2 = mp.mpc(0.5, -g)
        return (mp.log(1 - s/r1) + mp.log(1 - s/r2) + s/r1 + s/r2)
    f = lambda g: pairlog(g) * (mp.log(g/(2*PI))/(2*PI))
    Tt = mp.quad(f, [G, max(G, 2*10000), mp.inf])
    lnPsi = (s*mp.log(2*PI) - (1 + EULER_G/2)*s - mp.log(2)
             - mp.log(s - 1) - mp.loggamma(s/2 + 1))
    lnPsi += la + mp.mpc(0, ar) + Tt
    Psi = mp.e**lnPsi
    zt = mp.zeta(s)
    rel = abs(Psi - zt) / abs(zt)
    print(f"dps={dps:3d} G={Glimit:9.0f} zeros_used={int(Glimit) and sum(1 for g in gammas if g <= Glimit):6d} "
          f"|Psi-zeta|/|zeta| = {float(rel):.6e}   [T={mp.nstr(Tt,7)}]")

run(15, 50000)
run(15, 100000)
run(30, 100000)
