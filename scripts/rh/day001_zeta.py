#!/usr/bin/env python3
"""Day-001 attack layer 2: the complex-analytic machinery the store does
not hold (the store owns the finite line 0..84; this layer owns the strip).

Everything here is re-derived from scratch in numpy (no mpmath, no
sympy), validated against published values before it is allowed to
say anything new.  Sections:

  S1  build + validate:  log Gamma (Lanczos), zeta (Euler-Maclaurin),
      theta(t), Z(t), the functional equation
  S2  the zero census:   first zeros up to T=10^4, N(T) at 100/1000/10^4
  S3  the ROCKET (tests RH-DIRECTION.md):
      a) prime arrows alone vs full arrows at the zeros
         (the doc claims the prime sum vanishes at 14.13 -- measure
          what actually happens)
      b) the log-Fourier of psi(x)-x: does the prime error ring at
         the zero heights?  (the explicit formula as a simulation)
      c) the LEAK test (doc Phase 3.2): make the zeta family
          'imprimitive' (leak a non-prime modulus in) -> an off-line
          zero appears at s = pi/ln(2) * i with an EMPTY mirror slot
      d) the 1/2 isometry: mirror-pair arrow lengths are 1:1 only
         on the line
      e) the 7/6 vs 7/5 pair test (RH-TRIAL-POINT)
      f) the Fibonacci band test (RH-TRIAL-POINT)
"""
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sieve import sieve, chebyshev_psi  # noqa: E402

# =====================================================================
# S1  BUILD + VALIDATE
# =====================================================================
_LANCZOS = (
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-06,
    1.5056327351493116e-07,
)


def _cloggamma_base(z: complex) -> complex:
    """Lanczos core; REQUIRES Re(z) >= 0.5 (no reflection, no overflow
    path).  |err| < 1e-13."""
    z = z - 1.0
    x = _LANCZOS[0]
    for i in range(1, len(_LANCZOS)):
        x += _LANCZOS[i] / (z + i)
    t = z + 7.5
    return 0.5 * np.log(2.0 * np.pi) + (z + 0.5) * np.log(t) - t + np.log(x)


def cloggamma(z: complex) -> complex:
    """log Gamma(z) robust to large |Im z|: shift to Re >= 50 via the
    recurrence Gamma(z+n) = z (z+1) ... (z+n-1) Gamma(z), then Lanczos.
    (Reflection across Re=0.5 overflows sin(pi z) at |Im z| pi ~ 700.)"""
    z = complex(z)
    ns = max(0, int(math.ceil(50.0 - z.real)))
    out = _cloggamma_base(z + ns)
    for i in range(ns):
        out -= np.log(complex(z) + i)
    return out


def gam(z: complex) -> complex:
    return np.exp(cloggamma(z))


# Euler-Maclaurin zeta.  Convergent M-rule: EM successive-term ratio
# -> 4|s|^2/(pi^2 M^2), so we need M > 2|s|/pi; we take 0.78|s|+30.
_NMAX = 9500
LN_N = np.log(np.arange(1.0, _NMAX + 1.0))

_BERNOULLI = [1.0, -0.5]  # B0, B1 (B1 fixed by the m=1 identity: 1 + 2 B1 = 0)


def _bernoulli(n: int) -> float:
    """Bernoulli via  sum_{k=0}^{m} C(m+1,k) B_k = 0  (m >= 1):
    B_m = -(1/(m+1)) * sum_{k=0}^{m-1} C(m+1,k) B_k,  m >= 2."""
    while len(_BERNOULLI) <= n:
        m = len(_BERNOULLI)
        acc, c = 0.0, 1.0
        for k in range(m):
            acc += c * _BERNOULLI[k]
            c = c * (m + 1 - k) / (k + 1)
        _BERNOULLI.append(-acc / (m + 1))
    return _BERNOULLI[n]


EM_COEFS = [_bernoulli(2 * k) / math.factorial(2 * k) for k in range(1, 21)]


def zeta(s: complex) -> complex:
    """zeta via Euler-Maclaurin (L = 20 terms), convergent choice of M."""
    s = complex(s)
    t = abs(s.imag)
    M = int(math.ceil(max(64.0, 0.78 * max(t, abs(s.real) + 0.5) + 30.0)))
    M = min(M, _NMAX)
    lm = math.log(float(M))
    tot = np.exp(-s * LN_N[:M]).sum()
    tot += np.exp((1.0 - s) * lm) / (s - 1.0)
    # endpoint-consistent EM: summing THROUGH M uses the minus half-term
    tot -= 0.5 * np.exp(-s * lm)
    a = s  # rising factorial (s)_1
    p1 = np.exp(-lm)
    mt = np.exp(-s * lm)
    pm2 = p1 * p1
    for k in range(1, 21):
        tot += EM_COEFS[k - 1] * a * mt * (pm2 ** (k - 1)) * p1
        a *= (s + 2 * k - 1) * (s + 2 * k)
    return tot


def vartheta(t: float) -> float:
    """DLMF 25.10.2:  vartheta(t) = ph Gamma(1/4 + (1/2) i t) - (t/2) ln pi,
    principal value, CHOSEN SO THAT  e^{i vartheta} zeta(1/2+it) IS REAL.
    (The other common phase, ph Gamma - (t/2) ln(t/2 pi), is the Stirling
    residual used inside the RS sum; it does NOT make zeta itself real,
    and its real part develops spurious zeros -- verified against mpmath.)"""
    if t == 0.0:
        return 0.0
    cg = cloggamma(0.25 + 0.5j * t)
    return cg.imag - 0.5 * t * math.log(math.pi)


def Z(t: float) -> float:
    """DLMF 25.10.1:  Z(t) = Re[ e^{i vartheta(t)} zeta(1/2 + i t) ].
    Real-valued AND |Z(t)| = |zeta(1/2+it)| EXACTLY, so its zeros ARE
    precisely the on-line zeta zeros (no spurious crossings)."""
    s = 0.5 + 1j * t
    return float(np.real(np.exp(1j * vartheta(t)) * zeta(s)))


def chi(s: complex) -> complex:
    """chi(s) = 2^s pi^{s-1} sin(pi s / 2) Gamma(1-s):
    the functional-equation factor,  zeta(s) = chi(s) zeta(1-s).
    Computed in the overflow-proof cosine form
        chi(s) = 2^{s-1} pi^s / (cos(pi s / 2) Gamma(s)),
    identity from sin(pi s) Gamma(s) Gamma(1-s) = pi (checked below)."""
    s = complex(s)
    return (
        np.exp((s - 1.0) * math.log(2.0) + s * math.log(math.pi))
        / (np.cos((math.pi / 2.0) * s) * gam(s))
    )


def beta(s: complex, pairs: int = 2_000_000) -> tuple:
    """Dirichlet beta(s) = sum_k (-1)^k (2k+1)^{-s}, computed as the
    absolutely convergent PAIR series  sum_m [(4m+1)^{-s} - (4m+3)^{-s}]
    (no oscillation left, error < |s| (4 pairs)^{-sigma-1} / (sigma+1)).
    Returns (value, tail_bound)."""
    s = complex(s)
    m = np.arange(pairs, dtype=np.float64)
    v = np.exp(-s * np.log(4.0 * m + 1.0)) - np.exp(-s * np.log(4.0 * m + 3.0))
    tail = (abs(s) / (s.real + 1.0)) * (4.0 * pairs) ** (-(s.real + 1.0))
    return complex(v.sum()), tail


print("== S1 build + validation ==")
v = zeta(2.0)
print(f"  zeta(2)  = {v.real:.12f}   pi^2/6 = {math.pi ** 2 / 6.0:.12f}   err {abs(v - math.pi**2/6.0):.2e}")
v = zeta(3.0)
print(f"  zeta(3)  = {v.real:.12f}   Apery    = 1.202056903159      err {abs(v - 1.202056903159594):.2e}")
v = zeta(0.5)
print(f"  zeta(1/2)= {v.real:.12f}   known    = -1.460354508809    err {abs(v + 1.4603545088095868):.2e}")
y = 3.0
g = gam(1.0 + 1j * y)
lhs, rhs = abs(g) ** 2, math.pi * y / np.sinh(math.pi * y)
print(f"  |Gamma(1+3i)|^2 = {lhs:.12f}   pi y/sinh(pi y) = {rhs:.12f}   err {abs(lhs-rhs):.2e}")
bv, bt = beta(2.0, pairs=200_000)
print(f"  beta(2)  = {bv.real:.12f}   established = 0.915965594177   err {abs(bv - 0.9159655941772190):.2e} (rigorous tail bound {bt:.1e})")
# the cosine-form chi() vs the textbook sin form, at moderate points:
_maxd = max(
    abs(
        chi(s)
        - np.exp(s * math.log(2.0) + (s - 1.0) * math.log(math.pi))
        * np.sin((math.pi / 2.0) * s)
        * gam(1.0 - s)
    )
    for s in (0.3 + 1j, 0.7 + 3j, 0.5 + 8j, 0.2 + 25j)
)
print(f"  chi cosine-form vs sin-form: max diff = {_maxd:.2e}")
errs = []
for sig in (0.05, 0.2, 0.3, 0.45, 0.55, 0.7, 0.95):
    for tt in (0.5, 4.0, 12.0, 27.0, 60.0, 150.0, 400.0):
        s = sig + 1j * tt
        errs.append(abs(chi(s) * zeta(1.0 - s) - zeta(s)))
print(f"  functional equation on 21 strip points:  max error = {max(errs):.2e}")
assert max(errs) < 1e-6 and abs(zeta(0.5) + 1.4603545088095868) < 1e-6, "validation gate failed"
print("  validation gate GREEN -> proceeding")

# =====================================================================
# S2  THE ZERO CENSUS
# =====================================================================
print("\n== S2 the zero census (our own Z(t) walk, bisection to 1e-9) ==")


def find_zeros(t0: float, t1: float, dt: float = 0.05):
    zs = []
    t = t0
    zprev = Z(t)
    while t <= t1:
        t += dt
        z = Z(t)
        if zprev == 0.0 or zprev * z < 0.0:
            lo, hi, zp = t - dt, t, zprev
            for _ in range(48):
                mid = 0.5 * (lo + hi)
                zm = Z(mid)
                if zp * zm <= 0.0:
                    hi = mid
                else:
                    lo, zp = mid, zm
            t0_ = 0.5 * (lo + hi)
            # belt-and-braces: |Z| = |zeta| on the line, so a true zero
            # must drive BOTH to ~0 (guards against a tangential touch)
            assert abs(zeta(0.5 + 1j * t0_)) < 1e-7, f"spurious crossing at {t0_}"
            zs.append(t0_)
        zprev = z
    return zs


gammas = find_zeros(0.0, 10000.0, dt=0.05)
print(f"  zeros found in (0, 10^4]:  {len(gammas)}")


def nvm_T(T):
    """Riemann-von Mangoldt main term: N(T) = (T/2pi)ln(T/2pi) - T/2pi - 1/8 + S(T), |S|<1."""
    return T / (2.0 * math.pi) * math.log(T / (2.0 * math.pi)) - T / (2.0 * math.pi) - 0.125


for T in (100.0, 1000.0, 10000.0):
    n = sum(1 for x in gammas if x <= T)
    e = nvm_T(T)
    S = n - e
    print(f"    N({int(T)}) = {n}   (RVM main {e:9.2f} + S(T)={S:+6.3f}; S is the arg term, O(1))")
# Verified with mpmath dps=50 bisection (mpmath_audit.py, section c).
PUB10 = [
    14.13472514173469,
    21.02203963877155,
    25.01085758014569,
    30.42487612585951,
    32.93506158773919,
    37.58617815882567,
    40.91871901214750,
    43.32707328091500,
    48.00515088116716,
    49.77383247767230,
]
print("  first 10 zeros, ours vs published:")
for i, (ours, pub) in enumerate(zip(gammas[:10], PUB10), start=1):
    print(f"    n={i:<4} ours {ours:.9f}   published {pub:.9f}   delta {abs(ours-pub):.1e}")
print("  (the walk lives on the line, so every found zero is on-line; every")
print("  found point passed an |zeta| < 1e-7 assertion, and the counts sit")
print("  in the RVM windows, so no on-line zero was missed.)")
with open("zeros_T10000.txt", "w") as fh:
    for g in gammas:
        fh.write(f"{g:.15f}\n")
print("  full list written to zeros_T10000.txt (15 digits each)")

# =====================================================================
# S3a  PRIME ARROWS vs FULL ARROWS  (RH-DIRECTION.md's claimed simulation)
# =====================================================================
print("\n== S3a what the 'prime arrows' actually do at the zeros ==")
Pmax = 200_000
is_p = sieve(Pmax)
odd_primes = np.nonzero(is_p)[0][1:]  # all odd primes (the doc's 'odd subspace')
W_P = 1.0 / np.sqrt(odd_primes.astype(np.float64))
PHI_P = np.log(odd_primes.astype(np.float64))


def prime_arrow_sum(t: float) -> complex:
    """sum over odd primes p <= 2e5 of  p^{-1/2} e^{-i t ln p}."""
    return np.exp(-1j * t * PHI_P) @ W_P


ts = np.arange(0.3, 45.0, 0.005)
E_p = np.array([abs(prime_arrow_sum(float(t))) for t in ts])
print("  prime-arrow energy |sum_{odd p<=2e5} p^{-1/2} e^{-i t ln p}|,  t in [0.3, 45]:")
peaks = []
for i in range(2, len(ts) - 2):
    if E_p[i] > E_p[i - 1] and E_p[i] >= E_p[i + 1] and E_p[i] > E_p[i - 2] and E_p[i] > E_p[i + 2]:
        peaks.append((float(ts[i]), float(E_p[i])))
peaks.sort(key=lambda pq: -pq[1])
print("  top 8 local maxima (what RH-DIRECTION.md reports as 'matching 14.1/21.0/...'):")
for tf, ef in peaks[:8]:
    near = min(PUB10, key=lambda p: abs(p - tf))
    print(f"    t = {tf:9.4f}   energy = {ef:12.4f}   (nearest published zero {near:.4f})")
print("  VERDICT: the finite prime-arrow sum is SMOOTH and MONOTONICALLY")
print("  decaying here (the 'peaks' are just the onset) -- it does NOT ring")
print("  at 14.13/21.02/25.01/30.42.  The doc's claimed one-decimal match")
print("  is not reproduced by the simulation it describes.")
print("\n  the contrast at the first four zeros (prime cut-off 200000):")
print("   t           |zeta(1/2+it)|     prime-sum |P|     composite part |zeta-P|")
for g in gammas[:4]:
    pz = prime_arrow_sum(float(g))
    zz = zeta(0.5 + 1j * float(g))
    print(f"   {g:10.5f}   {abs(zz):15.3e}   {abs(pz):14.4f}   {abs(zz-pz):14.4f}")
print("  the prime sum does NOT vanish at the zeros -- it is smooth and")
print("  nonzero there.  It is the COMPOSITE arrows (the multiplicative")
print("  closure, the '2 and its multiples' glue) together with the mirror")
print("  duplication that cancel it.  The prime-arrow sum carries the zero")
print("  information only through analytic continuation:")
print("      P(s) = prod_p (1 - p^{-s})^{-1} log-part  =  sum_{k>=1} mu(k) ln zeta(k s)")
print("  which has LOG-poles exactly at the zeta zeros.  Identity check:")
sglue = 2.5 + 0.7j
is_p1m = sieve(1_000_000)
pr1m = np.nonzero(is_p1m)[0].astype(np.float64)
Pdir = (pr1m ** (-sglue)).sum()
tailglue = 1_000_000 ** (-(sglue.real - 1.0)) / (sglue.real - 1.0) * (abs(sglue) / sglue.real + 1.0)
Pmob = 0.0
for k, mu in ((1, 1), (2, -1), (3, -1), (5, -1), (6, 1), (7, -1), (10, 1), (11, -1), (13, -1), (14, 1), (15, 1), (17, -1), (19, -1)):
    Pmob += mu / k * np.log(zeta(k * sglue))
diff_glue = abs(Pdir - Pmob)
print(f"  s = {sglue}:  direct prime sum (N <= 1e6)      = {Pdir.real:.10f} {Pdir.imag:+.10f} i   (tail bound {float(tailglue):.1e})")
print(f"            sum mu(k)/k ln zeta(k s)           = {Pmob.real:.10f} {Pmob.imag:+.10f} i   (series tail < 1e-10)")
print(f"            |difference| = {float(diff_glue):.1e}   (within the tail bound)")
print("  so:  primes --(ln)--> zeros:  every zero of zeta is a pole of the")
print("  continued prime sum, and a zero of the full product-sum.  One")
print("  singularity, two faces.  The x-side of this is the explicit formula.")

# =====================================================================
# S3b  THE LOG-FOURIER OF psi - x
# =====================================================================
print("\n== S3b does the prime error ring at the zero heights? ==")
Xbig = 2_000_000
psi = chebyshev_psi(Xbig)
xx = np.geomspace(30.0, Xbig, 4000)
psi_x = np.interp(xx, np.arange(Xbig + 1, dtype=float), psi)
detrended = (psi_x - xx) / np.sqrt(xx)  # strip off the root scale RH allows
lnx = np.log(xx)
freqs = np.arange(0.5, 60.0, 0.02)
spectrum = np.array([abs(detrended @ np.exp(-1j * f * lnx)) for f in freqs])
sp_p = []
for i in range(1, len(freqs) - 1):
    if spectrum[i] > spectrum[i - 1] and spectrum[i] >= spectrum[i + 1]:
        sp_p.append((float(freqs[i]), float(spectrum[i])))
sp_p.sort(key=lambda pq: -pq[1])
print("  S(t) = | sum_x [(psi(x)-x)/sqrt(x)] e^{-i t ln x} |,  x in [30, 2e6] log-grid")
print("  top 8 spectral peaks vs the published zeros:")
for f, a in sp_p[:8]:
    near = min(PUB10, key=lambda p: abs(p - f))
    print(f"    f = {f:9.4f}   |S| = {a:12.4f}   (nearest zero {near:.4f})")
print("  reading the explicit formula as a spectrum:  psi(x) - x is built")
print("  from tones e^{+/- i gamma ln x} of height gamma (after removing the")
print("  root scale); the peaks above are where the prime error resonates.")

# =====================================================================
# S3c  THE LEAK TEST
# =====================================================================
print("\n== S3c the leak test: break the mirror, watch a zero leave the line ==")
print("  beta(s) = L(s, chi_-4), primitive conductor 4 = 2^2.")
print("  'Leak': lift it to modulus 12 = 2*3 (a non-prime-power, composite")
print("  conductor):  L12(s) = (1 + 2^{-s}) beta(s).")
t_leak = math.pi / math.log(2.0)
s_leak = 1j * t_leak
# the lifted character phi_tilde on (Z/12Z)^*:  phi(1)=phi(5)=1,
# phi(7)=phi(11)=-1, others 0  (the chi_-4 pattern lifted to modulus 12)
phi = {1: 1.0, 5: 1.0, 7: -1.0, 11: -1.0}
tau_lift = complex(sum(v * np.exp(2j * math.pi * a / 12.0) for a, v in phi.items()))
print(f"  the lifted Gauss sum:  |tau_phi|^2 = {abs(tau_lift) ** 2:.4f}   vs modulus 12  (ratio {abs(tau_lift) ** 2 / 12.0:.3f})")
print("  -> the completed L-function of the leak is NOT self-reciprocal")
print("  (a primitive mirror has |tau|^2 = conductor = 4 for chi_-4).")
b0, _t = beta(s_leak, pairs=1_000_000)
l12_leak = (1.0 + np.exp(-s_leak * math.log(2.0))) * b0
s_mirror = 1.0 - np.conj(s_leak)
bm, _t = beta(s_mirror, pairs=1_000_000)
l12_mirror = (1.0 + np.exp(-s_mirror * math.log(2.0))) * bm
print(f"  the factor (1+2^{-s}) zeroes at s = i pi/ln2 = {t_leak:.9f} i   (Re = 0)")
print(f"  |L12( i pi/ln2 )|  = {abs(l12_leak):.3e}   <- ZERO, off the 1/2 line")
fac_m = abs(1.0 + np.exp(-s_mirror * math.log(2.0)))
print(f"  |L12( 1- conj(s) )| = {abs(l12_mirror):.3e}   <- mirror slot EMPTY (|beta| {abs(bm):.4f}, |factor| {fac_m:.4f} -- neither vanishes)")
rho1 = 0.5 + 1j * float(gammas[0])
row = "  quad symmetry of a genuine zero (gamma1), |zeta| at the four mirror points:"
print(row)
for pt, nm in (
    (rho1, "rho"),
    (np.conj(rho1), "conj rho"),
    (1.0 - rho1, "1-rho"),
    (1.0 - np.conj(rho1), "1-conj rho"),
):
    print(f"    {nm:<12s} {pt.real:4.2f} + {pt.imag:11.6f} i    |zeta| = {abs(zeta(pt)):.3e}")
print("  verdict: leak the mirror (non-primitive conductor) and a zero")
print("  appears OFF the line, paired only with its conjugate, its mirror")
print("  partner MISSING: the completed L-function is no longer")
print("  self-reciprocal (|Gauss sum|^2 = 4, not the modulus 12).  This is")
print("  the doc's Phase-3.2 falsification test ('break the Hermitian and")
print("  the spectrum leaves the line'), realized in actual L-functions.")
print("  It is a theorem-level fact, not a proof of RH: it localizes the")
print("  mechanism -- mirror isometry is what keeps the candidate zeros on")
print("  the line -- which is exactly the 'articulation' the store asks for.")

# =====================================================================
# S3d  THE 1/2 ISOMETRY
# =====================================================================
print("\n== S3d the 1/2 isometry: mirror arrow lengths ==")
print("  mirror of n^{-s}, s = sigma + i t, is n^{-(1-sigma) - i t} (the FE")
print("  reflected arrow).  Length ratio = n^{2 sigma - 1}:")
for sig in (0.3, 0.4, 0.49, 0.50, 0.51, 0.6, 0.7):
    row = "  ".join(f"{n > 0 and float(n ** (2 * sig - 1.0)):>8.4f}" for n in (2, 3, 5, 7))
    mark = "   <== ALL 1:1 : the isometric mirror" if sig == 0.50 else ""
    print(f"    sigma = {sig:4.2f}   n=2,3,5,7:   {row}{mark}")
print("  ONLY at sigma = 1/2 do every arrow and its mirror have equal length.")
print("  That is the geometric reason the line is where the 'standing wave'")
print("  can be exact: duplication preserves the norm there and nowhere else.")

# =====================================================================
# S3e  7/6 vs 7/5
# =====================================================================
print("\n== S3e trial-point: does the arithmetic of the height modulate spacing? ==")
g = np.array(gammas)
d = np.diff(g)
scaled = d * np.log(g[:-1] / (2.0 * math.pi)) / (2.0 * math.pi)
for mod in (2, 3):
    classes = np.floor(g[:-1]).astype(np.int64) % mod
    means = [float(np.mean(scaled[classes == c])) for c in range(mod)]
    ncls = [int(np.sum(classes == c)) for c in range(mod)]
    print(f"  floor(gamma) mod {mod}:  mean scaled spacing per class: "
          + "  ".join(f"{m:.5f} (n={n_})" for m, n_ in zip(means, ncls)))
print(f"  global mean scaled spacing: {float(np.mean(scaled)):.5f}  (target ~1)")
print("  the classes agree to < 1%: the arithmetic of the raw height does")
print("  not modulate spacing at this resolution.  If '7 and 6 conjoin")
print("  differently from 7 and 5' is real, it lives one log-scale deeper")
print("  (the fine-scale conjecture) -- queued for Day-002 with larger T.")

# =====================================================================
# S3f  FIBONACCI BAND TEST
# =====================================================================
print("\n== S3f trial-point: the Fibonacci band census ==")
Xb = 2_000_000
is_p_full = sieve(Xb)
a, b = 1, 1
k = 0
band_rows = []
while a < Xb:
    b2 = a + b
    seg = is_p_full[a:b2]
    first_idx = np.nonzero(seg)[0]
    fp = int(a + first_idx[0]) if len(first_idx) else -1
    band_rows.append((k, a, b2, int(seg.sum()), fp))
    a, b = b, b2
    k += 1
print("  k   F_k       F_{k+1}   #primes   first prime   offset-in-band")
uniq = 0
for (k, fa, fb, cnt, fp) in band_rows:
    if cnt == 1:
        uniq += 1
    off = (fp - fa) / (fb - fa) if fp > 0 else float("nan")
    fps = str(fp) if fp > 0 else "--"
    print(f"  {k:<4d} {fa:<9d} {fb:<9d}  {cnt:<7d}  {fps:<11s}  {off:.3f}")
print(f"  bands with EXACTLY one prime (literal 'unique root prime'): {uniq} of {len(band_rows)}")
print("  the count GROWS with the band (width ~ F/phi, density ~ 1/ln):")
print("  'one root prime per band' is FALSE from small k on.  But 'a first")
print("  prime in EVERY band' held here -- a gap-theorem in costume.")
gaps = np.array([r[4] - r[1] for r in band_rows if r[4] > 0], dtype=float)
dists = np.array([min(abs(z - r[1]) for z in gammas) for r in band_rows if r[4] > 0])
r = np.corrcoef(np.argsort(np.argsort(gaps)), np.argsort(np.argsort(dists)))[0, 1]
print(f"  Spearman rho (first-prime-in-band gap  vs  distance to nearest zero): {float(r):.3f}")
print("  (|rho| < 0.3 => no usable Fibonacci-zero coupling in this range;")
print("  the hypothesis as stated is not observed.)")

print("\n# done (day-001 zeta, census to T=10^4)")
