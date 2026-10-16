import mpmath as mp
mp.mp.dps = 45
Q = 5
CHI = {0:0, 1:1, 2:-1, 3:-1, 4:1}
def chi(n): return CHI[n % Q]
P = [0, 1, 0, -1, 0]
t = 10
s = mp.mpf("0.5") + mp.j * t
L = Q**(-s) * sum(chi(j) * mp.zeta(s, j/Q) for j in range(1, Q))
r = 1
targets = [10001, 20001, 50001, 100001, 200001, 500001, 1000001]
acc = mp.mpc(0); ti = 0
drift = {}
for k in range(1, max(targets) + 1):
    acc += chi(k) * mp.power(mp.mpf(k), -s)
    while ti < len(targets) and k == targets[ti]:
        T = L - acc
        c = (T + P[r] * mp.power(mp.mpf(k), -s)) * mp.power(mp.mpf(k), s + 1)
        drift[k] = mp.im(c / s)
        ti += 1
import math
pts = [(math.log(float(mp.log(mp.mpf(N)))),) for N in []]
lnN = [math.log(N) for N in targets]
lnD = [math.log(abs(drift[N])) for N in targets]
n = len(lnN)
sN = sum(lnN); sy = sum(lnD); sNN = sum(x*x for x in lnN); sNY = sum(x*y for x, y in zip(lnN, lnD))
slope = (n*sNY - sN*sy) / (n*sNN - sN*sN)
intercept = (sy - slope*sN) / n
print("drift(N) = |Im(c/s)|, r=1 (P=1), t=10: fit drift ~ A N^exp:")
for N in targets:
    print(f"  N={N:8d}: |drift| = {mp.nstr(abs(drift[N]), 6)}")
print(f"  exponent = {slope:.5f}   (candidates: 1/2=0.5, 2/5=0.4, 3/5=0.6, log? 0)")
print(f"  A = {math.exp(intercept):.6e}")
