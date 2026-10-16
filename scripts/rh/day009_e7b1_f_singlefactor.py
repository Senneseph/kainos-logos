from mpmath import mp
mp.dps = 60
t = mp.mpf("14000")
for gamma in [mp.mpf("14.134725141734694"), mp.mpf("98.8"), mp.mpf("1000")]:
    for sgn in (1, -1):
        rho = mp.mpc(0.5, sgn*gamma)
        s = mp.mpc(0.5, t)
        fac = (1 - s/rho) * mp.e**(s/rho)
        direct = mp.re(mp.log(fac))
        two_way = mp.log(abs(fac))
        parts = mp.log(abs(1 - s/rho)) + mp.re(s/rho)
        print(f"sgn={sgn} g={mp.nstr(gamma,6)}: direct={mp.nstr(direct,12)} "
              f"two_way={mp.nstr(two_way,12)} parts={mp.nstr(parts,12)}")
