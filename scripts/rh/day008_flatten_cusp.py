# day-008 / P-W.7 (the flattening, from the owner's 24-cardioid image):
# denser cells to resolve the cusp — circle-pinched vs. true cardioid.
#
# Generalizes the E2-exact M1 machinery (day006_chi17_exact.py) to an
# arbitrary real primitive character, then flattens:
#     w(r) = M1(r) * exp(2 pi i r / q)
# and compares two shape fits on the closed loop (cusp excluded from the
# fits; its polar phase is ambiguous — instead we test whether the fitted
# curve passes through the center):
#   (i)  Cartesian circle fit over non-cusp points:
#            origin_gap = 0  => circle passes through the center
#   (ii) polar limacon  rho(phi) = a + b cos(phi - phi0):
#            |a/b| ~ 0  => circle through the center (pinched circle)
#            |a/b| ~ 1  => cardioid
#            cusp_dir_rho = a - b = 0  => curve passes through the center
# Reading these on a FINER grid (q = 12 -> q = 24) tests whether the cusp
# resolves toward a cardioid or stays a pinched circle.
#
# Characters (computed FROM DEFINITION, no recall):
#   tau_12 (q=12) = (3/n)             real primitive, conductor 12 (re-check)
#   chi_24 (q=24) = (2/n)*(3/n)       real primitive, conductor 24 (= 8*3)
# (Kronecker symbols via residue-class rules; tables asserted below.)
from mpmath import mp

mp.dps = 35
N0 = 10 ** 6


def kr2(n):  # (2/n)
    if n % 2 == 0:
        return 0
    return 1 if (n % 8) in (1, 7) else -1


def kr3(n):  # (3/n)
    if n % 3 == 0:
        return 0
    return 1 if (n % 12) in (1, 11) else -1


def kr7odd(n):  # (7/n) for odd n:  (n/7) * (-1)^{(n-1)/2}  (7 = 3 mod 4)
    qr = (n % 7) in (1, 2, 4)          # QRs mod 7 = {1,2,4}
    val = 1 if qr else -1
    return val if (n - 1) % 4 == 0 else -val


def period_table(q, fn):
    # Real primitive Dirichlet character of conductor q:
    # tab[r] = fn(r) on the UNITS (gcd(r,q)=1), 0 off them (a character
    # vanishes on residues not coprime to the modulus).
    import math

    tab = [0] * q
    for r in range(1, q):
        if math.gcd(r, q) == 1:
            tab[r] = fn(r)
    return tab


TAU12 = period_table(12, kr3)                        # (12/n)=(3/n) on units, cond 12
CHI24 = period_table(24, lambda r: kr2(r) * kr3(r))  # (24/n)=(2/n)(3/n) on units, cond 24
TAU28 = period_table(28, kr7odd)                     # (28/n)=(7/n) on units, cond 28
CHI56 = period_table(56, lambda r: kr2(r) * kr7odd(r))  # (56/n)=(2/n)(7/n) on units, cond 56

# provenance: tables computed above (from definition); must be non-principal real characters:
assert TAU12 == [0, 1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 1] and sum(TAU12) == 0
assert sum(CHI24) == 0 and all(v in (-1, 0, 1) for v in CHI24)
assert sum(TAU28) == 0 and sum(CHI56) == 0
assert all(v in (-1, 0, 1) for v in TAU28 + CHI56)
assert TAU28[1] == 1 and TAU28[7] == 0 and TAU28[2] == 0


def band_cumul(tab, q):
    P = [0] * q
    for r in range(1, q):
        P[r] = P[r - 1] + tab[r]
    return P


def tail_exact(tab, r, N, s, q):
    total = mp.mpc(0)
    qms = mp.power(mp.mpf(q), -s)
    for j in range(1, q + 1):
        cj = tab[j - 1]
        if cj == 0:
            continue
        n0 = q if j - 1 == 0 else j - 1
        k = max(0, -(-(N + 1 - n0) // q))
        n_first = n0 + k * q
        total += cj * qms * mp.zeta(s, mp.mpf(n_first) / q)
    return total


def m1_of_phase(tab, P, r, s, q):
    N1 = N0 + ((r - N0) % q)
    cuts = (N1, N1 + q, N1 + 4 * q)
    vs = [None] * 3
    for i, N in enumerate(cuts):
        t_ = tail_exact(tab, r, N, s, q)
        nsm = mp.power(mp.mpf(N), -s)
        vs[i] = (t_ + mp.mpf(P[r]) * nsm) * mp.power(mp.mpf(N), s + 1) / s
    c = (vs[0] - vs[1]) / (mp.mpf(1) / cuts[0] - mp.mpf(1) / cuts[1])
    M1_2 = vs[0] - c / cuts[0]
    c2 = (vs[1] - vs[2]) / (mp.mpf(1) / cuts[1] - mp.mpf(1) / cuts[2])
    M1_wide = vs[1] - c2 / cuts[1]
    return M1_2, abs(M1_2 - M1_wide)


def flatten_fit(M, q):
    import cmath
    import math

    w = [M[r] * complex(math.cos(2 * math.pi * r / q), math.sin(2 * math.pi * r / q)) for r in range(q)]
    rho = [abs(z) for z in w]
    arg = [cmath.phase(z) for z in w]
    xmax = max(rho)
    cusp = [r for r in range(q) if rho[r] < 1e-6 * xmax]
    keep = [r for r in range(q) if r not in cusp]
    # (i) Cartesian circle fit over non-cusp points:
    # minimize sum (x^2+y^2 - c1 x - c2 y - c3)^2  -> 3x3 normal system (Cramer)
    m11 = m12 = m13 = m14 = m22 = m23 = m24 = m33 = m34 = m44 = 0.0
    for r in keep:
        x, y = w[r].real, w[r].imag
        rr = x * x + y * y
        m11 += 1.0
        m12 += x
        m13 += y
        m14 += rr
        m22 += x * x
        m23 += x * y
        m24 += rr * x
        m33 += y * y
        m34 += rr * y
        m44 += rr * rr

    def det3(a, b, c, d, e, f, g, h, i):
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

    D = det3(m11, m12, m13, m12, m22, m23, m13, m23, m33)
    # NOTE column order (1, x, y):  x^2+y^2 = s1 + s2*x + s3*y
    s1 = det3(m14, m12, m13, m24, m22, m23, m34, m23, m33) / D
    s2 = det3(m11, m14, m13, m12, m24, m23, m13, m34, m33) / D
    s3 = det3(m11, m12, m14, m12, m22, m24, m13, m23, m34) / D
    cx, cy = s2 / 2, s3 / 2
    R = math.sqrt(max(cx * cx + cy * cy + s1, 0.0))
    circ_resid = max(abs(math.hypot(w[r].real - cx, w[r].imag - cy) - R) for r in keep)
    origin_gap = abs(math.hypot(cx, cy) - R)
    # (ii) polar limacon fit rho = a + b cos(phi - phi0) over non-cusp points,
    # phi0 by 1-degree grid search (each step a linear 2-param LLS) - robust
    # to tie-break noise in the dps data
    # cusp-corner angle: for each cusp cell, the smaller angle between the
    # two neighbouring points as seen from the origin
    corners = []
    for c in cusp:
        a1, a2 = arg[(c - 1) % q], arg[(c + 1) % q]
        d = abs(a1 - a2) % (2 * math.pi)
        corners.append(round(math.degrees(min(d, 2 * math.pi - d)), 2))
    best = None
    for deg in range(0, 180, 1):
        p0 = math.radians(deg)
        u = [math.cos(arg[r] - p0) for r in keep]
        ru = [u[i] * rho[r] for i, r in enumerate(keep)]
        uu = [v * v for v in u]
        su = sum(u)
        suu = sum(uu)
        srho = sum(rho[r] for r in keep)
        suru = sum(ru)
        detg = len(keep) * suu - su * su
        a = (srho * suu - su * suru) / detg
        b = (len(keep) * suru - su * srho) / detg
        res = max(abs(rho[r] - (a + b * u[i])) for i, r in enumerate(keep))
        if best is None or res < best[0]:
            best = (res, a, b, deg, p0)
    lim_resid, a, bb, deg0, phi0 = best
    cusp_dir_rho = a - bb  # model's radius in the cusp direction; 0 => through center
    ratio = abs(a / bb) if abs(bb) > 1e-9 else float("inf")
    lab = "pinched-circle" if ratio < 0.25 else ("cardioid-like" if ratio > 0.75 else "limacon-between")
    return {
        "n_cusp": len(cusp),
        "cusp_cells": cusp,
        "cusp_corner_deg": corners[:],
        "phi0_deg": deg0 % 360,
        "circle": {"cx": round(cx, 4), "cy": round(cy, 4), "R": round(R, 4),
                   "origin_gap": round(origin_gap, 4), "max_resid": round(circ_resid, 4)},
        "limacon": {"a": round(a, 4), "b": round(bb, 4), "abs_a_over_b": round(ratio, 4),
                    "cusp_dir_rho": round(cusp_dir_rho, 4), "max_resid": round(lim_resid, 4)},
        "verdict": lab,
    }


for label, tab, q in (("tau_12 re-check", TAU12, 12), ("chi_24 denser", CHI24, 24),
                      ("tau_28 denser", TAU28, 28), ("chi_56 densest", CHI56, 56)):
    P = band_cumul(tab, q)
    print("== %s (q=%d, dps-35, t=10, N~1e6) ==" % (label, q))
    print("   chi values (1..%d):" % (q - 1), [tab[r] for r in range(1, q)])
    s = mp.mpf("0.5") + 10 * mp.j
    M, spreads = {}, {}
    for r in range(q):
        M[r], spreads[r] = m1_of_phase(tab, P, r, s, q)
    mir = max(abs(M[r] - M[(-r) % q]) for r in range(q))
    tr = sum(M[r] for r in range(q))
    integ = max(abs(mp.re(M[r]) - mp.mpf(round(float(mp.re(M[r]))))) for r in range(q))
    semi = q // 2
    anti = max(abs(M[r] + M[(r + semi) % q]) for r in range(semi))
    print("   mirror max|M(r)-M(-r)| = %s | trace = %s | integer max|dInt| = %s"
          % (mp.nstr(mir, 5), mp.nstr(tr, 8), mp.nstr(integ, 4)))
    print("   antipode M(r)~-M(r+q/2) max|sum| = %s | worst 2-cut spread = %s"
          % (mp.nstr(anti, 5), mp.nstr(max(spreads.values()), 4)))
    Mf = {r: complex(float(mp.re(M[r])), float(mp.im(M[r]))) for r in range(q)}
    print("   Re M1:", [round(float(mp.re(M[r])), 3) for r in range(q)])
    import json

    print("   FLATTEN:", json.dumps(flatten_fit(Mf, q)))
    print("done", label)
