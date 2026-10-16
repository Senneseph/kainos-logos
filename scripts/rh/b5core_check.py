# PROOF-OF-RECORD: B-5 core formula — exact R = off4/on2 (RH-PROOF-OUTLINE v0.5).
# dps-30; check vs direct 8-zero definition and vs the measured dps-15 56-pt table.
# gamma* = 999.791572 (certified zero nearest 1000, zeros_T300000_ext_full.txt).
# RUN: any mpmath >= 1.3 (no tail integrals); host ok.
# B-5 core formula check (dps-30): exact 4-factor ratio formula vs
# (a) direct 8-zero computation (definition)  (b) the measured |R-1| table
# (out_day010_d4farscale.txt @ dps-15, G=3e5 context; out_day010_d4d3.txt).
# PROOF-OF-RECORD for the B-5 core theorem of RH-PROOF-OUTLINE v0.5.
from mpmath import mp
mp.dps = 30
G = mp.mpf("999.791572")     # gamma* certified zero nearest 1000
def R_formula(t, d, g):
    A = mp.mpc(0.25) + g*g
    R4 = (1+2*d)/((mp.mpc(0.5)+d)**2 + g*g) + (1-2*d)/((mp.mpc(0.5)-d)**2 + g*g)
    w = R4 - 1/A
    pref = A * ((g-t)**2 + d*d) * ((g+t)**2 + d*d) / ((g*g - t*t) * ((mp.mpc(0.5)+d)**2 + g*g) * ((mp.mpc(0.5)-d)**2 + g*g))
    s = mp.mpc(0.5, mp.mpf(t))
    return pref * mp.e**(s*w)
def direct(t, d, g):
    zeros_on  = [mp.mpc(0.5, g), mp.mpc(0.5, -g)]
    zeros_off = [mp.mpc(0.5+d, g), mp.mpc(0.5+d, -g), mp.mpc(0.5-d, g), mp.mpc(0.5-d, -g)]
    s = mp.mpc(0.5, mp.mpf(t))
    def P(zs):
        acc = mp.mpc(1)
        for rho in zs:
            acc *= (1 - s/rho) * mp.e**(s/rho)
        return acc
    return P(zeros_off)/P(zeros_on)
meas = {(10, 0.005): 99.99998, (10, 0.5): 99.99993, (50, 0.005): 2499.999,
        (50, 0.5): 2499.998, (100, 0.005): 9999.998, (100, 0.5): 9999.993}
print("B5-CORE CHECK (dps-30; gamma*=%s)" % G, flush=True)
worst_fv, worst_fd = mp.mpf(0), mp.mpf(0)
for c in (10, 50, 100):
    for d in (0.005, 0.5):
        t = mp.mpf(c) * G
        rf = abs(R_formula(t, mp.mpf(d), G) - 1)
        rd = abs(direct(t, mp.mpf(d), G) - 1)
        m = meas[(c, d)]
        worst_fv = max(worst_fv, abs(rf - m))
        worst_fd = max(worst_fd, abs(rf - rd))
        print("far  c=%-3d d=%.3f: formula %.7f  direct %.7f  measured %.6f  %s"
              % (c, d, float(rf), float(rd), m, "OK" if abs(rf-rd) < 1e-5 else "FAIL"))
tmap = {"g-1.0": G-1, "g-0.25": G-mp.mpf("0.25"), "g+0.25": G+mp.mpf("0.25"),
        "g+1.0": G+1, "g+10": G+10, "2g": 2*G-mp.mpf("0.416856")}
near_meas = {"g-1.0": 0.9980, "g-0.25": 0.9995, "g+0.25": 1.0005,
             "g+1.0": 1.0020, "g+10": 1.0201, "2g": 4.0000}   # measured @ d=0.005 (4-6 digit)
for k in ("g-1.0", "g-0.25", "g+0.25", "g+1.0", "g+10", "2g"):
    t = tmap[k]
    rf = abs(R_formula(t, mp.mpf("0.005"), G) - 1)
    rd = abs(direct(t, mp.mpf("0.005"), G) - 1)
    m = near_meas[k]
    print("near %s d=0.005: formula %.7f  direct %.7f  measured %.4f  %s"
          % (k, float(rf), float(rd), m, "OK" if abs(rf-rd) < 1e-5 and abs(rf-m) < 0.01 else "FAIL"))
print("WORST |formula-measured| (far) = %.6f" % float(worst_fv), flush=True)
print("WORST |formula-direct|   (all) = %.3e" % float(worst_fd), flush=True)
print("B5-CORE CHECK " + ("PASS" if float(worst_fv) < 0.01 and float(worst_fd) < 1e-5 else "FAIL"), flush=True)
