import mpmath as mp
mp.mp.dps = 45
Q = 5
CHI = {0:0, 1:1, 2:-1, 3:-1, 4:1}
def chi(n): return CHI[n % Q]
P = [0, 1, 0, -1, 0]
for t in (10, 100):
    s = mp.mpf("0.5") + mp.j * t
    L = Q**(-s) * sum(chi(j) * mp.zeta(s, j/Q) for j in range(1, Q))
    print(f"--- t={t}: c_r(1, N) = (T + P(1) N^-s) N^(s+1), r=1 ---")
    r = 1
    targets = [10001, 20001, 50001, 100001, 200001, 500001]
    acc = mp.mpc(0)
    ti = 0
    out = {}
    for k in range(1, max(targets) + 1):
        acc += chi(k) * mp.power(mp.mpf(k), -s)
        while ti < len(targets) and k == targets[ti]:
            T = L - acc
            c = (T + P[r] * mp.power(mp.mpf(k), -s)) * mp.power(mp.mpf(k), s + 1)
            out[k] = c
            ti += 1
    for N in targets:
        print(f"  N={N:7d}: |c| = {mp.nstr(abs(out[N]), 12)}  c/s = {mp.nstr(out[N]/s, 12)}")
