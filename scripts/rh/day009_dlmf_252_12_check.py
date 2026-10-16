# day009_dlmf_25_2_12_check.py — verify the read DLMF 25.2.12 product
# (verbatim READ recorded in READS-1859-GS25.md / FORMULAS.md):
#
#   zeta(s) = (2*pi)^s * exp(-(1 + gamma/2)*s) / (2*(s-1)*Gamma(s/2+1))
#             * prod_{rho: Re rho > 0} (1 - s/rho) * exp(s/rho)
#
# Two verifications, engine-first:
#   V1: numeric product convergence at s = 1/2 + 10 i (partial products
#       approach zeta; error decays with the number of zeros used).
#   V2: the main factor's phase at s = 1/2 + i t equals DLMF 25.10.2's
#       vartheta(t) = ph Gamma(1/4 + i t/2) - t ln(pi)/2  (mod 2 pi)
#       at several t — this fixes the "main phase = vartheta" used by
#       the E7b kernel.
# Host mpmath. Single-threaded.
from mpmath import mp
mp.dps = 30

pi = mp.pi
EULER_G = mp.euler

def main_factor(s):
    return (2*pi)**s * mp.e**(-(1 + EULER_G/2)*s) / (2*(s-1)*mp.gamma(s/2+1))

def vartheta(t):
    # DLMF 25.10.2: ph Gamma(1/4 + i t/2) - t ln(pi)/2 (principal value)
    return mp.arg(mp.gamma(mp.mpc(0.25, t/2))) - t*mp.log(pi)/2

# --- zero list (first 2000 nontrivial ordinates, from our certified file)
import io, os, re
cands = ["/work/scripts/rh/zeros_T100000.txt",            # docker
         "scripts/rh/zeros_T100000.txt",
         "/home/jsmille/Projects/kainos-logos/scripts/rh/zeros_T100000.txt"]
zpath = [p for p in cands if os.path.exists(p)]
zpath = zpath[0] if zpath else cands[1]
print("zero file:", zpath)
gammas = []
with open(zpath) as f:
    for line in f:
        toks = line.replace("=", " ").split()
        nums = [x for x in toks if re.fullmatch(r"-?\d+\.?\d*([eE][+-]?\d+)?", x)]
        if len(nums) >= 2:
            gammas.append(float(nums[0]))
        elif len(nums) == 1:
            gammas.append(float(nums[0]))
gammas = sorted(set(gammas))
print("zeros read:", len(gammas), " first:", gammas[0] if gammas else None)

def pair_zeros(n):
    # DLMF 25.2.12: product over zeros with Re rho > 0 — with our
    # certified on-line list that is BOTH signs: 1/2 +/- i*gamma
    out = []
    for g in gammas[:n]:
        out.append(mp.mpc(0.5, g))
        out.append(mp.mpc(0.5, -g))
    return out

# V1: product convergence at s = 1/2 + 10 i
s = mp.mpc(0.5, 10)
ztrue = mp.zeta(s)
for n in [10, 50, 200, 1000, 2000]:
    prod = mp.mpc(1)
    for rho in pair_zeros(n):
        prod *= (1 - s/rho) * mp.e**(s/rho)
    diff = abs(main_factor(s)*prod - ztrue)
    print(f"V1 n={n:5d}: |main*prod - zeta| = {diff}")

print()
# V2: reality of exp(i*vartheta)*main*prod (DLMF 25.10.1: Z real)
#     as n grows -> the imaginary share must go to 0
for t in [10.0, 14.134725142, 100.0, 1000.0]:
    var = vartheta(t)
    for n in [500, 1000, 1500]:
        x = main_factor(mp.mpc(0.5, t))
        for rho in pair_zeros(n):
            x *= (1 - mp.mpc(0.5, t)/rho) * mp.e**(mp.mpc(0.5, t)/rho)
        z = mp.e**(mp.j*var) * x
        print(f"V2 t={mp.nstr(t,10)} n={n:5d}: Im(e^i*var * main * prod)"
              f" = {mp.nstr(z.imag, 4)}   |x - zeta| = {mp.nstr(abs(x - mp.zeta(mp.mpc(0.5, t))), 4)}")
