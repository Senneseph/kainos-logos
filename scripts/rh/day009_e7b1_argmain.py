# day009_e7b1_argmain.py — docker part: dps arg of the 25.2.12 main
# factor at s = 1/2 + i t over the E7b-1 grid. Single-threaded.
from mpmath import mp
mp.dps = 30

R = "/work/scripts/rh"
tgrid = [10200.0 + (18500.0 - 10200.0)*i/159.0 for i in range(160)]

with open(f"{R}/e7b1_argmain.txt", "w") as f:
    for t in tgrid:
        s = mp.mpc(0.5, t)
        main = (2*mp.pi)**s * mp.e**(-(1 + mp.euler/2)*s) \
            / (2*(s - 1)*mp.gamma(s/2 + 1))
        f.write(f"{t:.6f}\t{mp.nstr(mp.arg(main), 15)}\n")
print("argmain table written:", len(tgrid), "rows")
