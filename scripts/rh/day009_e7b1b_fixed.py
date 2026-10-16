# day009_e7b1b_fixed.py — E7b-1 with the CORRECTED zero-side candidate.
#
# Full zero-side count from 25.2.12 (raw TeX, verified):
#   N_zero(t) = (1/pi) [ pi*N_below(t)                       (H steps)
#                          + SUM_{g<kt} (pi/2 - atan2(g,1/2) (smooth, low g)
#                                          + (t-g)/(2(1/4+g^2)))
#                          - arg main(1/2 + i t) ]  + C
#   S_cand(t)  = N_zero(t) - main(t) - C,
#   main(t) = (t/2pi)(ln(t/2pi)-1) + 7/8   (locked RVM main)
# Measured side: S_file(t) from the walk (NOTICE: the dt=0.1 cpu walk on
# [1e4,1.9e4] is defective — ~22 missed twins, S collapsed to ~-45;
# step anomalies in D are expected there and are the defect's signature).
# Host numpy, single-threaded; mpmath argmain read from table.
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np

R = "/home/jsmille/Projects/kainos-logos/scripts/rh"
gammas = np.loadtxt(f"{R}/zeros_T100000.txt")
walk = np.loadtxt(f"{R}/S_t_walk_1e4_1e5.txt")
t_meas, S_meas = walk[:, 0], walk[:, 1]
am = {round(r[0], 4): r[1] for r in np.loadtxt(f"{R}/e7b1_argmain.txt")}

def main_t(t):
    return t/(2*np.pi)*(np.log(t/(2*np.pi)) - 1.0) + 0.875

tgrid = [10200.0 + (18500.0 - 10200.0)*i/159.0 for i in range(160)]
ks = [3.0, 5.0, 10.0]
print(f"{'k':>4} {'D-mean':>12} {'max|D-med|':>12} {'std':>10} "
      f"{'nsteps>=0.7':>12}")
base = None
for k in ks:
    D = []
    for t in tgrid:
        gmax = min(k*t, gammas[-1])
        sel = gammas[gammas < gmax]
        sm = (np.pi/2 - np.arctan2(sel, 0.5)
              + (t - sel)/(2*(0.25 + sel**2))).sum()
        nb = np.searchsorted(gammas, t)
        N_zero = (nb + sm/np.pi - am[round(t, 4)]/np.pi)
        S_cand = N_zero - main_t(t)
        Sf = np.interp(t, t_meas, S_meas)
        D.append(S_cand - Sf)
    D = np.array(D)
    step = np.abs(np.diff(D))
    nbig = int((step > 0.7).sum())
    print(f"{k:4.1f} {D.mean():12.6f} {np.abs(D-np.median(D)).max():12.6f} "
          f"{D.std():10.3e} {nbig:12d}")
    if base is None:
        base = D
for k in ks[1:]:
    pass
# k-convergence on the zero side alone
Dz = {}
for k in ks:
    out = []
    for t in tgrid:
        gmax = min(k*t, gammas[-1])
        sel = gammas[gammas < gmax]
        sm = (np.pi/2 - np.arctan2(sel, 0.5)
              + (t - sel)/(2*(0.25 + sel**2))).sum()
        out.append(sm/np.pi - am[round(t, 4)]/np.pi)
    Dz[k] = np.array(out)
print()
for k in ks[1:]:
    dd = Dz[k] - Dz[ks[0]]
    print(f"zero-side k {ks[0]}->{k}: level shift={dd.mean():+.6f}  "
          f"shape resid={np.abs(dd-dd.mean()).max():.6f}")
print()
print("NOTE: D against the defective walk carries ~22 twin steps (~1.0 each);"
      " the step count above is the defect's fingerprint, not a kernel fail.")
