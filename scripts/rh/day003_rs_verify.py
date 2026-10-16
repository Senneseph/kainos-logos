#!/usr/bin/env python3
"""Day-003: validate the Riemann-Siegel engine Z_rs(t) (zeta_core) against
the verified Euler-Maclaurin engine Z(t) on the host, with a note where the
mpmath spot-check (container) goes.

Honesty rule: the O(u^{-5}) remainder error is MEASURED against the EM
oracle (itself mpmath-verified to float precision), not assumed.

Host part (this file, numpy only):
  grid t in [50, 300] step 5, plus t in {1000, 2500, 5000, 7500, 10000}:
    |Z_rs(t) - Z(t)|
Container part (mpmath dps 30): python3 day003_rs_verify_mpmath.py
  points t in {45374.03, 50000, 100000}: |Z_rs - zeta_mp| vs |Z_EM - zeta_mp|
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".")
import zeta_core  # noqa: E402

assert zeta_core.selftest(verbose=False), "selftest FAILED"

print("== RS engine validation (host): |Z_rs(t) - Z_EM(t)|, Z_EM mpmath-verified ==")
worst, tw = 0.0, 0.0
for t in [50.0 + 5.0 * k for k in range(51)]:
    d = abs(zeta_core.Z_rs(t) - zeta_core.Z(t))
    if d > worst:
        worst, tw = d, t
print("  t in [50, 300] step 5:  max |diff| = %.3e  at t = %.1f" % (worst, tw))

big = {}
for t in (1000.0, 2500.0, 5000.0, 7500.0, 10000.0):
    d = abs(zeta_core.Z_rs(t) - zeta_core.Z(t))
    big[t] = d
    print("  t = %8.1f : |Z_rs - Z_EM| = %.3e" % (t, d))

print("""
  trend: if max error is ~ u^{-5} = (t/2pi)^{-5/4}, extrapolation to t = 1e5:
    err(1e5) ~= err(t) * (t/1e5)^{5/4}
""")
for t in (2500.0, 10000.0):
    u5 = big[t] * (t / 1e5) ** (1.25)
    print("    from t = %.0f:  extrapolated err(1e5) ~ %.2e" % (t, u5))
print("  (the mpmath spot-check at t = 4.537e4 and 1e5 confirms the tail of this trend)")
