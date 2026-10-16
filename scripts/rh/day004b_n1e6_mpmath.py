from mpmath import mp, pi
for dps, t in [(30, 100000), (50, 1000000)]:
    mp.dps = dps
    tv = t
    g = mp.arg(mp.gamma(0.25 + tv/2*mp.j)) - tv/2*mp.log(mp.pi)
    main_ = mp.floor(tv/(2*mp.pi)*mp.log(tv/(2*mp.pi)) - tv/(2*mp.pi) + 0.25)
    A = main_ - 1 + g/mp.pi
    frac = abs(A - mp.floor(A + mp.mpf("0.5")) + mp.mpf("0.5"))
    print("dps=%d t=%d: (main-1)+theta/pi = %s   dist-to-integer: %s"
          % (dps, t, mp.nstr(A, 25), mp.nstr(frac, 12)))
    if t == 1000000:
        zt = mp.zeta(0.5 + tv*mp.j)
        print("  |zeta(1/2+1e6 i)| = %s   arg zeta = %s" % (mp.nstr(mp.abs(zt), 15), mp.nstr(mp.arg(zt), 12)))
        # independent check of my CPU EM engine value is done on host; this is the ground truth
        # and a direct zero-free check: N(1e6) must equal round(A) with integer A (S=0) or A - S(1e6)
        # instead verify via arg Z directly:  arg Z(1e6) = g + arg|Z|... use day-003 2K at 1e6:
        # 2K = (N - main + 1) - g/pi must be even integer, N = N(1e6) unknown -> report A = main - 1 + g/pi
        # N(1e6) = A - S(1e6);  if I have candidate N from the walk, plug in:
print()
for Ncand in (1747104, 1398000):
    mp.dps = 50
    tv = 1000000
    g = mp.arg(mp.gamma(0.25 + tv/2*mp.j)) - tv/2*mp.log(mp.pi)
    main_ = mp.floor(tv/(2*mp.pi)*mp.log(tv/(2*mp.pi)) - tv/(2*mp.pi) + 0.25)
    twoK = (mp.mpf(Ncand) - main_ + 1) - g/mp.pi
    S = Ncand - (main_ - 1 + g/mp.pi)
    resid = twoK - 2*mp.floor(twoK/2 + 0.5)
    print("candidate N(1e6) = %d:  2K = %s  (dist to even integer: %s)  S(1e6) = %s"
          % (Ncand, mp.nstr(twoK, 20), mp.nstr(resid, 8), mp.nstr(S, 10)))
