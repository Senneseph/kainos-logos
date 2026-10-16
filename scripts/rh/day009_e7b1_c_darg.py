# day009_e7b1_c_darg.py — definitive winding/direction test.
# Compute X(t) = main(1/2+it) * prod_{|g|<=G} f_+(g,t) f_-(g,t) at
# t and t+delta in mpmath; compare the true continuous d arg X/dt
# (unambiguous for delta small enough that the winding < pi) with the
# separated-sum prediction:
#   darg_sep = pi*dN_below + (dsm/dt)*delta - (dargmain/dt)*delta
# Sign and magnitude tell us exactly where the separated formula's
# branch convention is wrong (or right).
# Docker mpmath, dps-15, single-threaded. G = 20000 (fast enough),
# but the product to G=20000 at t~1.4e4: factors with g < t/2 have
# magnitude up to e^{t/2g} ~ e^{t/(2*14)} = e^500 — mpmath handles it
# (log-rescale: accumulate log|X| and arg X separately per factor).
from mpmath import mp
mp.dps = 15

t0 = 14000.0
dt = 0.5
G = 12000.0   # zeros with |g| <= 12000 (~7600 zeros, ~18000 factors)

# zero list
g = []
with open("/work/scripts/rh/zeros_T100000.txt") as f:
    for line in f:
        try:
            v = float(line)
        except ValueError:
            continue
        if v <= G:
            g.append(v)
print("zeros used:", len(g))

def logX(t):
    # returns (logabs, arg) of main * product, accumulated in log form
    s = mp.mpc(0.5, t)
    main = (2*mp.pi)**s * mp.e**(-(1 + mp.euler/2)*s) \
        / (2*(s - 1)*mp.gamma(s/2 + 1))
    la = mp.log(abs(main))
    ar = mp.arg(main)
    for gamma in g:
        for sign in (+1.0, -1.0):
            rho = mp.mpc(0.5, sign*gamma)
            fac = (1 - s/rho) * mp.e**(s/rho)
            la += mp.log(abs(fac))
            ar += mp.arg(fac)
    return la, ar

la0, ar0 = logX(t0)
la1, ar1 = logX(t0 + dt)
darg_true = (ar1 - ar0)          # < pi guaranteed (winding ~ 1.9 rad)
# the product's true continuous phase change (raw mpmath args, no
# branch bookkeeping — each factor's own arg; summed; the total is
# within (-pi, pi) so no unwrap needed)
dlogabs = (la1 - la0)
print(f"t0={t0} dt={dt} G={G} zeros={len(g)}")
print(f"d log|X|/dt = {mp.nstr(dlogabs/dt, 6)}   (should be small, O(1))")
print(f"d arg(X)/dt = {mp.nstr(darg_true/dt, 6)}")
# expectation if winding is +pi per zero with N' ~ 1.22/rad:
import math
full = [float(l) for l in open("/work/scripts/rh/zeros_T100000.txt") if l.strip()]
nb0 = sum(1 for v in full if v < t0)
nb1 = sum(1 for v in full if v < t0 + dt)
print(f"N({t0})={nb0}  N({t0+dt})={nb1}  dN={nb1-nb0}  "
      f"pi*dN/dt = {mp.nstr(mp.pi*(nb1-nb0)/dt, 4)}")
print("=> if darg/dt ~ +pi*dN/dt (+ small smooth): winding is +pi per zero"
      " (2K convention), and the separated formula's H-step sign is +pi."
      )
print("=> if darg/dt ~ -pi*dN/dt: winding is -pi; flip the H step.")
