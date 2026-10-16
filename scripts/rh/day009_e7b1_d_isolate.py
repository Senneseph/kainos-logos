# day009_e7b1_d_isolate.py — locate the +8.71 vs -3.87 discrepancy.
# Fine-epsilon (0.05) principal-arg differences, no branch ambiguity:
#  A) d/dt arg main(1/2+it)  (Stirling predicted -3.88)
#  B) d/dt arg product (sum of principal args of all factors)
#  C) per-factor slopes for selected gammas (14, 100, 1000, 11999)
# plus the sum-model: sum of C-style slopes over all factors.
from mpmath import mp
mp.dps = 20

t0 = 14000.0
eps = 0.05
G = 12000.0
g = []
with open("/work/scripts/rh/zeros_T100000.txt") as f:
    for line in f:
        try:
            v = float(line)
        except ValueError:
            continue
        if v <= G:
            g.append(v)

def main(s):
    return (2*mp.pi)**s * mp.e**(-(1 + mp.euler/2)*s) \
        / (2*(s - 1)*mp.gamma(s/2 + 1))

def facslo(gamma):
    rho = mp.mpc(0.5, gamma)
    s0 = mp.mpc(0.5, t0)
    s1 = mp.mpc(0.5, t0 + eps)
    f0 = (1 - s0/rho) * mp.e**(s0/rho)
    f1 = (1 - s1/rho) * mp.e**(s1/rho)
    return (mp.arg(f1) - mp.arg(f0)) / eps

# A
a0 = mp.arg(main(mp.mpc(0.5, t0)))
a1 = mp.arg(main(mp.mpc(0.5, t0 + eps)))
print("A: d arg main/dt =", mp.nstr((a1 - a0)/eps, 8))

# C selected
for gamma in [14.134725, 100.0, 1000.0, 11999.0]:
    # use nearest actual zero for 100/1000/11999
    near = min(g, key=lambda v: abs(v - gamma))
    print(f"C: d arg factor/dt (g~{near:.1f}) = "
          f"{mp.nstr(facslo(near), 8)}")

# B: full sum (25038 factors) — but accumulate in mpf at high dps;
# do it in two eps passes
def sumparg(t):
    s = mp.mpc(0.5, t)
    tot = mp.mpf(0)
    for gamma in g:
        for sgn in (1.0, -1.0):
            rho = mp.mpc(0.5, sgn*gamma)
            tot += mp.arg((1 - s/rho) * mp.e**(s/rho))
    return tot

b0 = sumparg(t0)
b1 = sumparg(t0 + eps)
print("B: d arg product/dt =", mp.nstr((b1 - b0)/eps, 8))
print("B+A total =", mp.nstr(((b1 - b0) + (a1 - a0))/eps, 8))
print("(e7b1_c measured 8.71178)")
