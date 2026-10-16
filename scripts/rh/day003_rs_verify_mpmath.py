"""mpmath spot-check of the RS engine at large t (container, dps 30).
Reads host values from out_day003_host_values.json (written by the host run
of day003_census_1e5.py's prep, or by:
  cd scripts/rh && python3 -c "import json,sys; sys.path.insert(0,'.'); import zeta_core; print(json.dumps({t:[zeta_core.Z_rs(t), zeta_core.Z(t)] for t in (45374.03, 50000.0, 100000.0)}))" > out_day003_host_values.json
then:
  docker run --rm -i -v "$PWD":/work kainos-dev:dev sh -c "pip -q install mpmath 2>/dev/null; cd /work && python3 day003_rs_verify_mpmath.py"
"""
import json

import mpmath as mp

mp.mp.dps = 30


def Zmp(t):
    t = mp.mpf(t)
    s = mp.mpf("0.5") + 1j * t
    theta = mp.im(mp.log(mp.gamma(mp.mpf("0.25") + 0.5j * t))) - 0.5 * t * mp.log(mp.pi)
    return mp.re(mp.exp(1j * theta) * mp.zeta(s))


HOST = {float(k): (float(a), float(b)) for k, (a, b) in json.load(open("out_day003_host_values.json")).items()}
for t in (45374.03, 50000.0, 100000.0):
    zmp = Zmp(t)
    zrs, zem = HOST[t]
    print("t = %10.2f :  |Z_mp| = %.6e" % (t, abs(zmp)))
    print("          |Z_rs - Z_mp| = %.3e   |Z_EM - Z_mp| = %.3e   (Z_rs = fast RS engine)" % (
        abs(zrs - zmp), abs(zem - zmp)))
    print("          Z_mp          = %.12f" % float(mp.re(zmp)))
