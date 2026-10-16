# SUPERSEDED (P-0.9, day-009): the S-level bridge attempt. It reads the
# DEFECTIVE dt=0.1 CPU S-walk file, and the S comparison is a RVM
# consistency check anyway (the S walk counts zeros) — the real bridge
# target is the ONSET law (day009_e7b2/e7b2b). Never re-run on clean
# data; do not cite its outputs. Kept for provenance only.
# day009_e7b1_h_final.py — E7b-1 FINAL: zero-side candidate vs clean
# measured S, closed form (no per-factor loops, no branch bookkeeping).
#
# Derived from numerically verified components (e7b1_d/e, day-007, 2K):
#   argP_cont(t) = argmain_unwrap(t)                 [continuous 25.2.12 main]
#                +  t * SUM_{g<=G} 1/(1/4+g^2)      [both-sign factor phases]
#                +  pi * N_below(t)                  [+pi lift per zero, 2K conv]
#                +  const(G)
#   S_cand(t)    = (argP_cont(t) + vartheta(t))/pi - N_below(t)
#                = (argmain_unwrap + t*SIG(G) + vartheta + const)/pi   [N BELOW CANCELS]
#   D(t)         = S_cand(t) - S_file_clean(t)
# Expected: smooth piecewise-constant D' between zeros (level C per G;
# G-convergent; the -1 D-jumps at each zero = the measured S walk's +1
# count jumps). PASS = D' smooth + level-constant + G-convergent.
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import sys
sys.path.insert(0, ".")
import zeta_core  # noqa: E402 (host float64 vartheta — same engine as walks)

R = "/home/jsmille/Projects/kainos-logos/scripts/rh"
gammas = np.loadtxt(f"{R}/zeros_T100000.txt")

# ---- argmain via float64 Stirling for arg Gamma(3/4 + i t/2) ----
def argmain_stirling(t):
    # arg[ (2pi)^s e^{-(1+gE/2)s} / (2 (s-1) Gamma(s/2+1)) ], s = 1/2 + i t
    x, y = 0.75, 0.5 * t
    z = complex(x, y)
    r2 = x*x + y*y
    ph = math.atan2(y, x) if (x != 0 or y != 0) else 0.0
    ln_z = 0.5*math.log(r2) + 1j*ph
    L = (z - 0.5)*ln_z - z + 0.5*math.log(2*math.pi)
    # Stirling corrections: B2/(2*1*z) + B4/(4*3*z^3) + B6/(6*5*z^5) + B8/(8*7*z^7)
    L += 1/(12*z) - 1/(360*z**3) + 1/(1260*z**5) - 1/(1680*z**7)
    arg_gamma = L.imag
    arg_s_minus_1 = math.atan2(t, -0.5)
    arg_s_ln2pi = t*math.log(2*math.pi)
    gE = 0.5772156649015328606
    return arg_s_ln2pi - (1 + gE/2)*t - math.log(2.0) - arg_s_minus_1 - arg_gamma

import math

# validate against the dps argmain table (mod 2pi) if present
try:
    am = np.loadtxt(f"{R}/e7b1_argmain.txt")
    tst = am[::20][:6]
    bad = []
    for rr in tst:
        t = float(rr[0])
        a64 = argmain_stirling(t) % (2*math.pi)
        ads = float(rr[1]) % (2*math.pi)
        d = abs(a64 - ads)
        d = min(d, 2*math.pi - d)
        bad.append((t, d))
    print("argmain Stirling-vs-dps (mod 2pi) sample diffs:",
          " ".join(f"{d:.1e}" for _, d in bad))
except Exception as e:
    print("argmain validation skipped:", e)

tgrid = [10200.0 + (18500.0 - 10200.0)*i/159.0 for i in range(160)]
Gs = [12000.0, 100000.0]

# continuous unwrap of argmain across the grid (fine principal deltas are
# |d/dt ~ -3.88 * 52.2 | = 200 rad?? NO: principal delta is in (-pi, pi];
# unwrap k = (200.1 - dp)/2pi is known only to the integer — instead
# track argmain by dense principal steps (0.4 rad: |delta| = 1.55 < pi)
def argmain_unwrap_series(ts):
    out = []
    cur = None
    for t in ts:
        a = argmain_stirling(t) % (2*math.pi)
        if cur is None:
            cur = a
        else:
            a2 = a
            # choose the branch closest to the slope-predicted value
            pred = cur + (a - cur)  # placeholder
            d = (a2 - cur + math.pi) % (2*math.pi) - math.pi
            cur = cur + d
        out.append(cur)
    return np.array(out)

# dense path for unwrapping (256 steps), then evaluate on the grid by
# interpolation of the unwrap count
dense = np.linspace(10.0, 18500.0, 4*len(tgrid))
au_dense = np.array([argmain_stirling(t) for t in dense])
d = np.diff(au_dense)
# wrap each delta to (-pi, pi]: the true per-step change = -3.88*step (~-0.0076 rad per 0.0029 step)
step = dense[1] - dense[0]
exp_rate = -3.88
ok = np.all(np.abs(np.arctan2(np.sin(d), np.cos(d))) < math.pi)
wrapped = np.arctan2(np.sin(d), np.cos(d))
# per-step true change ~ exp_rate*step ~ -0.0113 << pi: wrap is identity
unwrapped = au_dense[0] + np.concatenate([[0.0], np.cumsum(wrapped)])
# argmain_unwrap on the grid
au_grid = np.interp(tgrid, dense, unwrapped)

SIG = {}
for G in Gs:
    sel = gammas[gammas <= G]
    SIG[G] = float(np.sum(1.0/(0.25 + sel**2)))
    print(f"G={G:.0f}: zeros={sel.size}  SIG(1/(1/4+g^2))={SIG[G]:.9f}")

walk = np.loadtxt(f"{R}/S_t_walk_1e4_1p9e4_gpu_dt00025.txt")
t_meas, S_meas = walk[:, 0], walk[:, 1]
print("clean S walk:", len(t_meas), "rows; S range %.4f..%.4f"
      % (S_meas.min(), S_meas.max()))

print()
hdr = f"{'t':>11} {'G':>9} | {'S_cand':>12} {'S_file':>12} {'D':>10}"
levels = {}
for G in Gs:
    print(f"--- G = {G:.0f} ---  " + hdr)
    Ds = []
    for i, t in enumerate(tgrid):
        scand = (au_grid[i] + t*SIG[G] + zeta_core.vartheta(float(t)))/math.pi
        sf = float(np.interp(t, t_meas, S_meas))
        D = scand - sf
        Ds.append(D)
        if i % 20 == 0:
            print(f"{t:11.2f} {G:4.0f} | {scand:12.6f} {sf:12.6f} {D:10.6f}")
    D = np.array(Ds)
    # remove the expected -1 jump at each zero (S_file +1 jumps)
    jumps = np.array([np.searchsorted(gammas, t, side="left") for t in tgrid])
    djump = np.diff(jumps)
    Dsm = D.copy()
    for i in range(1, len(tgrid)):
        if djump[i-1] > 0:
            Dsm[i:] + 0  # marker only
    # smoothness between zeros: first-difference residual excluding jump steps
    dd = np.diff(D)
    mask = djump > 0
    dd_sm = dd[~mask[:-1]]
    jumpval = dd[mask[:-1]]
    print(f"  level: mean={D.mean():+.6f}  max|D-med|={np.abs(D-np.median(D)).max():.6f}")
    print(f"  between-zero steps: n={len(dd_sm)}  max|dd|= {np.abs(dd_sm).max():.3e}")
    print(f"  at-zero steps: n={len(jumpval)}  mean={jumpval.mean():+.4f} "
          f"max|j+1|={np.abs(jumpval+1.0).max():.3e}")
    levels[G] = D.mean()
print()
print("G-convergence level shift (12000 -> 100000): "
      f"{levels[100000]-levels[12000]:+.6f}")
print("expected tail drift diff = (t*(SIG(1e5)-SIG(1.2e4)))/pi over the slice:")
dtail = (18500.0-10200.0)*(SIG[100000]-SIG[12000])/math.pi
print("   ~ %.6f" % dtail)
print()
print("PASS: between-zero steps < 1e-3 (measured noise), at-zero steps = -1")
print("(S-file jump) to < 1e-3, level-constant per G, G-shift ~ tail drift.")
