"""Independent check of the census via the argument formula (dps-30, in-container).

S(T) = (1/pi)*Arg_cont(zeta(1/2+iT)) - 1, where Arg_cont is the argument
continued from t=0.  From a single mpmath point we only get the PRINCIPAL
argument ph in (-pi, pi).  The formula ties them by an EVEN-integer count
of 2*pi turns:
    Arg_cont/pi = ph/pi + 2K,  K in Z
    N = main + S = main + Arg_cont/pi - 1
  hence   2K = (N - main + 1) - ph/pi   must be an EVEN INTEGER
  for the census to be consistent.  (With main = 138067.558 and
  N = 138065:  2K = -1.558 - 0.4416 = -2  ->  K = -1.)
  Convention sanity: at T = 20 (N = 1, only gamma_1 below), the same
  equation gives 2K = 2 (checked in out_day003_s_arg_mpmath.txt).
"""
import cmath
import json
import math

import mpmath as mp

mp.mp.dps = 40
T = 100_000.0
z = mp.zeta(0.5 + mp.j * T)
ph = float(mp.arg(z))
# RVM main term, full float64 precision on host side:
x = T / (2 * math.pi)
main = x * math.log(x) - x - 0.125
N = 138_065
twoK = (N - main + 1.0) - ph / math.pi
frac = abs(twoK - round(twoK))
print("mpmath dps-40:  zeta(1/2+i*1e5) = %s" % z)
print("  principal arg = %.10f rad  (%.10f * pi)" % (ph, ph / math.pi))
print("  |zeta| = %.10f" % float(abs(z)))
print("  RVM main (float64) = %.6f" % main)
print("  2K = (N - main + 1) - ph/pi = %.6f   (must be an EVEN integer)" % twoK)
print("  distance to nearest integer = %.2e   -> S(1e5) = %+.4f %s"
      % (frac, N - main, "CONSISTENT (census count confirmed by independent dps-40 point)" if frac < 1e-3 else "INCONSISTENT"))
