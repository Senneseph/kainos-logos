# day009c_onset_pred_ext.py — E7b-1 onset rerun on the EXTENDED zero list
# (P-0.8: named constants; startup echo; host mpmath — no numpy needed).
#
# LIST_FILE: zeros up to G_MAX (from the day009b flip walk, dt/2 pass).
# G product = full list; density tail from G_MAX.
from mpmath import mp
import math
import numpy as np
PI = mp.pi
EULER_G = mp.euler

# ---------------- named constants (P-0.8) ----------------
import sys as _sys
LIST_FILE = _sys.argv[1] if len(_sys.argv) > 1 else \
    "zeros_T300000_ext_full.txt"
G_MAX = float(_sys.argv[2]) if len(_sys.argv) > 2 else 300_000.0   # list coverage (rad); argv override
S_PER_SEC = None           # n/a
DP = 15

gammas = []
with open(LIST_FILE) as f:
    for line in f:
        try:
            gammas.append(float(line))
        except ValueError:
            pass
n_under_G = sum(1 for g in gammas if g <= G_MAX)
print("list: %d zeros (<= %.0f: %d)  G_MAX from argv" % (len(gammas), G_MAX, n_under_G),
      flush=True)
GN = np.array(gammas[:n_under_G], dtype=np.float64)

def logmain25212(s):
    return (s*mp.log(2*PI) - (1 + EULER_G/2)*s
            - mp.log(2) - mp.log(s - 1) - mp.loggamma(s/2 + 1))

def product_larg(s, gam):
    la = mp.mpf(0); ar = mp.mpf(0)
    for gamma in gam:
        for sgn in (1.0, -1.0):
            rho = mp.mpc(0.5, sgn*gamma)
            fac = (1 - s/rho) * mp.e**(s/rho)
            la += mp.log(abs(fac))
            ar += mp.arg(fac)
    return la, ar

def product_on_line_vec(s, gv):
    # DAY-010: on-line pair product, vectorized float64 (exact per-pair algebra,
    # cross-validated below against the mp reference product_larg, P-0.9).
    # Pair at 1/2+/-i g, s = 1/2+i t  (rho*conj(rho) = 1/4+g^2, rho+conj(rho) = 1):
    #   (1-s/rho)(1-s/rho')     = (g^2-t^2)/(1/4+g^2)
    #   e^{s/rho} e^{s/rho'}    = exp( s/(1/4+g^2) )
    #   => la += log|(g^2-t^2)/(1/4+g^2)| + 1/(2(1/4+g^2))
    #      ar += t/(1/4+g^2) - pi*(g<t)   (sum of principal args; atan2 terms cancel in-pair)
    t = float(mp.im(s))
    A = t*t + 0.25
    Bv = 1.0 / (0.25 + gv * gv)
    inner = 1.0 - A * Bv
    if np.abs(inner).min() < 1e-13:
        return None, None          # SINGULAR: list zero numerically ON t (reported, never FAIL)
    la = float(np.sum(0.5 * Bv + np.log(np.abs(inner))))
    ar = t * float(np.sum(Bv)) - float(np.pi * np.sum(gv < t))
    return la, ar

def pairlog(g, s):
    rho1 = mp.mpc(0.5, g)
    rho2 = mp.mpc(0.5, -g)
    return (mp.log(1 - s/rho1) + mp.log(1 - s/rho2)
            + s/rho1 + s/rho2)

def tail_int(s, G):
    t = abs(mp.im(s))
    split = max(G, 2*t)
    f = lambda g: pairlog(g, s) * (mp.log(g/(2*PI))/(2*PI))
    return mp.quad(f, [G, split, mp.inf])

# --- DAY-010 cross-method validation (P-0.9): the vectorized on-line product
# --- must reproduce the mp reference (product_larg) on a 100k-pair prefix,
# --- at the two certified clean rows, before any G_MAX > 3e5 result is emitted.
_validate_G = min(100000.0, G_MAX)
gv_val = GN[GN <= _validate_G].tolist()
for _n, _f in ((1000, 1.0), (10000, 0.1)):
    _s = mp.mpc(0.5, mp.mpf(_n) * mp.mpf(repr(_f)))
    _la_mp, _ar_mp = product_larg(_s, gv_val)
    _la_v, _ar_v = product_on_line_vec(_s, np.array(gv_val))
    _dla = abs(mp.mpf(_la_v) - _la_mp)
    _dar = abs((mp.mpf(_ar_v) - _ar_mp) / mp.pi - (mp.floor((mp.mpf(_ar_v) - _ar_mp) / mp.pi + 0.5)))
    print("VAL(%d,%.1f): dLa=%.3e  dAr_mod2pi=%.3e  (mp default-dps reference, %d pairs)"
          % (_n, _f, float(_dla), float(_dar), len(gv_val)),
          flush=True)
    assert float(_dla) < 1e-6 and float(_dar) < 1e-9, \
        "vectorized on-line product != mp reference — abort (P-0.9)"

measc = {0.1: 0.0500, 0.2: 0.1000, 0.5: 0.2509,
         1.0: 0.5071, 2.0: 1.0620}
rows = []
for Nn in (1000, 10000, 100000):
    for f_ in (0.1, 0.2, 0.5, 1.0, 2.0):
        t = mp.mpf(Nn) * mp.mpf(repr(f_))
        s = mp.mpc(0.5, t)
        la, ar = product_on_line_vec(s, GN)
        if la is None:
            print("N=%6d t/N=%4.1f: SINGULAR (listed zero numerically ON height t) — reported, not FAIL"
                  % (Nn, f_), flush=True)
            continue
        Tt = tail_int(s, mp.mpf(G_MAX))
        lnPsi = logmain25212(s) + mp.mpf(la) + mp.mpc(0, mp.mpf(ar)) + Tt
        Pn_mp = mp.fsum(mp.mpc(1.0/kk) ** s for kk in range(1, Nn + 1))
        I_mp = (mp.mpf(Nn) ** (1 - s)) / (1 - s)
        W = Pn_mp - I_mp
        Psi = mp.e**lnPsi
        zt = mp.zeta(s)
        dPz = abs(Psi - zt) / abs(zt)
        Cpred = abs(Psi - W)
        A = abs(I_mp)
        pred = Cpred / A
        err = (pred - measc[f_]) / measc[f_]
        print("N=%6d t/N=%4.1f: C/|I|=%.6f measured=%.4f err=%+.2f%%   "
              "|Psi-zeta|/|zeta|=%.3e"
              % (Nn, f_, float(pred), measc[f_], float(err)*100.0,
                 float(dPz)), flush=True)
        rows.append((Nn, f_, float(pred), measc[f_], float(err)))
print("rows:", [f"{a}/{b}:{c:.4f}" for a, b, c, *_ in rows])
