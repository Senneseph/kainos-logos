# day009_e7b1_sep.py — host part (numpy, single-threaded): the separated
# zero-phase sum S_sep(t) for the E7b-1 grid, all k values.
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np

R = "/home/jsmille/Projects/kainos-logos/scripts/rh"
gammas = np.loadtxt(f"{R}/zeros_T100000.txt")
print("zeros:", len(gammas), gammas[0], gammas[-1])

tgrid = [10200.0 + (18500.0 - 10200.0)*i/159.0 for i in range(160)]
ks = [3.0, 5.0, 7.0, 10.0]

out = open(f"{R}/e7b1_sep.txt", "w")
for k in ks:
    for t in tgrid:
        gmax = min(k*t, gammas[-1])
        sel = gammas[gammas < gmax]
        term = np.pi/2 - np.arctan2(sel, 0.5) + (t - sel)/(2*(0.25 + sel**2))
        out.write(f"{k:.1f}\t{t:.6f}\t{term.sum():.9f}\t{sel.size}\n")
out.close()
print("sep table written:", 160*len(ks), "rows")
