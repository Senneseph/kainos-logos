# day009_e7b1_zero_phase_sum.py — E7b-1 execution (first slice)
#
# Test: does the ZERO-SIDE phase (read from 25.2.12, raw TeX, verified)
# reproduce the MEASURED prime-side S(t) on the full-coverage slice?
#
#   Zero side (25.2.12, both-sign canonical factors, s = 1/2 + i t,
#   on-line gamma):
#     dphi_gamma(t) = pi/2 + pi*H(t-gamma) - atan2(gamma, 1/2)
#                     + (t - gamma) / (2*(1/4 + gamma^2))
#     S_sep(t)      = sum_{gamma < k*t} dphi_gamma(t)  (+ tail via main)
#   Zero side main phase (25.2.12 main factor, dps arg):
#     argmain(t) = arg[ (2pi)^(1/2+it) e^{-(1+gE/2)(1/2+it)}
#                       / (2(i(t-1/2)) Gamma(1/4*2... = (s/2+1)) ]
#   Candidate:  S_cand(t) = S_sep(t) - argmain(t)/pi + C
#
#   Measured side (prime-side machinery, independent):
#     S_file(t) from the flip-walk (S_t_walk_1e4_1e5.txt, dt = 0.1).
#
# PASS (E7b-1): D(t) = S_cand - S_file is (i) smooth (branch correct),
# (ii) level-constant (C exists), (iii) k-convergent (residual of the
# truncated zero sum decays as k grows). The three together say the
# measured count-phase IS the zero-phase sum read from 25.2.12.
#
# Single-threaded numpy (BLAS pinned); mpmath only for the per-t main arg.
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np

R = "/home/jsmille/Projects/kainos-logos/scripts/rh"
gammas = np.loadtxt(f"{R}/zeros_T100000.txt")
print("zeros:", len(gammas), gammas[0], gammas[-1])

walk = np.loadtxt(f"{R}/S_t_walk_1e4_1e5.txt")
t_meas, S_meas = walk[:, 0], walk[:, 1]
print("walk rows:", len(t_meas), t_meas[0], t_meas[-1])

def S_sep(t, gmax):
    # separated phase sum over gammas < min(gmax, all)
    sel = gammas[gammas < gmax]
    term = np.pi/2 - np.arctan2(sel, 0.5) + (t - sel) / (2*(0.25 + sel**2))
    nbelow = np.searchsorted(gammas, t)  # count gamma < t (step part)
    return term.sum(), nbelow, len(sel)

def argmain(t):
    # dps arg of the 25.2.12 main factor at s = 1/2 + i t
    from mpmath import mp
    mp.dps = 30
    s = mp.mpc(0.5, t)
    main = (2*mp.pi)**s * mp.e**(-(1 + mp.euler/2)*s) \
        / (2*(s - 1)*mp.gamma(s/2 + 1))
    return mp.arg(main)

# grid
tgrid = np.linspace(1.02e4, 1.85e4, 160)
ks = [3.0, 5.0, 7.0, 10.0]

print(f"{'k':>5} {'t':>11} {'S_sep+main/pi':>16} {'S_file':>12} {'D':>14} {'nused':>8}")
results = {}
for k in ks:
    Ds = []
    for i, t in enumerate(tgrid):
        ss, nb, nn = S_sep(float(t), k*float(t))
        am = float(argmain(float(t)))
        scand = ss - am/np.pi  # C left free
        tf = np.interp(float(t), t_meas, S_meas)
        Ds.append(scand - tf)
        if i % 20 == 0:
            print(f"{k:5.1f} {t:11.2f} {scand:16.6f} {tf:12.6f} "
                  f"{scand-tf:14.6f} {nn:8d}")
    D = np.array(Ds)
    results[k] = D
    print(f"  k={k}: D mean={D.mean():+.6f}  max|D-median|="
          f"{np.abs(D - np.median(D)).max():.6f}  "
          f"std={D.std():.3e}")

# smoothness: first-difference scale vs the k-convergence of the level
print()
for k in ks[1:]:
    dD = results[k] - results[ks[0]]
    print(f"k={ks[0]}->{k}: level shift = {dD.mean():+.6f}  "
          f"shape resid = {np.abs(dD - dD.mean()).max():.6f}")
print()
print("PASS criteria: (i) D smooth at 0.1-rad scale; (ii) level-constant "
      "(max|D-median| small vs std of S walk noise); (iii) level shifts "
      "decay with k.")
