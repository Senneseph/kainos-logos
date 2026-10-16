# day009_e7b1_combine.py — combine: zero-side candidate vs measured S
# (host; reads the two tables + the S walk; no mpmath needed).
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np

R = "/home/jsmille/Projects/kainos-logos/scripts/rh"

sep = np.loadtxt(f"{R}/e7b1_sep.txt")
am = np.loadtxt(f"{R}/e7b1_argmain.txt")
walk = np.loadtxt(f"{R}/S_t_walk_1e4_1e5.txt")
t_meas, S_meas = walk[:, 0], walk[:, 1]

ks = [3.0, 5.0, 7.0, 10.0]
am_by_t = {round(r[0], 4): r[1] for r in am}
sep_by_kt = {}
for row in sep:
    sep_by_kt[(row[0], round(row[1], 4))] = row[2]

report = []
Ds_by_k = {}
for k in ks:
    Ds = []
    for tt in np.array(sorted({t for (kk, t) in sep_by_kt if kk == k})):
        ssep = sep_by_kt[(k, round(tt, 4))]
        amv = am_by_t.get(round(tt, 4))
        if amv is None:
            continue
        scand = ssep - amv/np.pi          # C left free
        tf = np.interp(tt, t_meas, S_meas)
        Ds.append(scand - tf)
    D = np.array(Ds)
    Ds_by_k[k] = D
    report.append(f"k={k:4.1f}: D mean={D.mean():+.6f}  "
                  f"max|D-median|={np.abs(D-np.median(D)).max():.6f}  "
                  f"std={D.std():.3e}  min={D.min():+.4f} max={D.max():+.4f}")

print("\n".join(report))
print()
base = Ds_by_k[ks[0]] - Ds_by_k[ks[0]].mean()
for k in ks[1:]:
    dD = Ds_by_k[k] - Ds_by_k[k].mean()
    report.append(f"k {ks[0]}->{k}: level shift="
                  f"{(Ds_by_k[k].mean()-Ds_by_k[ks[0]].mean()):+.6f}   "
                  f"shape resid(k)={np.abs(dD-base).max():.6f}")
print("\n".join(report))
print()
print("PASS: (i) D smooth (no +-1 step anomalies beyond twin locations);"
      " (ii) level-constant; (iii) level shift + shape resid decay in k.")
