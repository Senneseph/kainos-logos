"""day006 oracle: the five-phase width table c_r(s) of the chi_5 missing tail.

Identity (exact, zero-mean periodic A = cumulative of chi_5, period 5):
  G(N) := L(s,chi_5) - P_N(s) = -P(r) N^{-s} + c_r(s) N^{-s-1} + O(N^{-s-2})
with r = N mod 5, P(r) the band cumulative (P(0..4) = 0,1,0,-1,0 — wait,
P(r) = sum of chi over residues 1..r: P(0)=0, P(1)=1, P(2)=0, P(3)=-1, P(4)=0).

c_r(s) is the first cell-moment ("Lebesgue width") coefficient; the phase
table r = 0..4 is what the Lebesgue-cell-width reading predicts to exist.
This oracle computes c_r(s) at dps=40 two ways per (r,s):
  (i)  from G(N) + P(r)N^{-s} at a large N (direct),
  (ii) stability re-check at N x 10.
L(s,chi_5) = 5^{-s} sum_j chi(j) zeta_H(s, j/5)   (mpmath hurwitz, exact).
s = 0.5 + i t, t in {1, 10, 100, 1000}; N0 = 1e4 + r (and 1e5 + r).
"""
import mpmath as mp

mp.mp.dps = 40

CHI = {1: 1, 2: -1, 3: -1, 4: 1}
P_RES = [0, 1, 0, -1, 0]  # P(r) = sum_{1..r} chi


def l5_hurwitz(s: mp.mpc) -> mp.mpc:
    return mp.mpf(1) / (5 ** s) * sum(CHI[j] * mp.hurwitz(s, mp.mpf(j) / 5) for j in (1, 2, 3, 4))


def partial_sums_up_to(n: int, s: mp.mpc):
    acc = mp.mpc(0)
    for m in range(1, n + 1):
        c = CHI.get(m % 5, 0)
        acc += c * m ** (-s)
    return acc


def main() -> None:
    print("chi_5 five-phase width table c_r(s), s = 0.5 + i t  (dps = 40)")
    print("c_r(s) := lim_N (G(N) + P(r) N^{-s}) * N^{s+1},  r = N mod 5")
    print()
    header = "r |   t   |   |c_r| (N=1e4)   arg(c_r) (N=1e4)   |c_r| (N=1e5)   arg (N=1e5)   N1-vs-N2 |dc|"
    print(header)
    for t in (1, 10, 100, 1000):
        s = mp.mpc(0.5, t)
        l5 = l5_hurwitz(s)
        for r in range(5):
            row = []
            for scale in (10_000, 100_000):
                n = scale + r
                pn = partial_sums_up_to(n, s)
                g = l5 - pn
                c = (g + P_RES[r] * n ** (-s)) * n ** (s + 1)
                row.append((abs(c), mp.arg(c)))
            dc = abs(abs(row[0][0]) - abs(row[1][0]))
            print(
                "%d | %5d | %14.7f   %14.7f   %14.7f   %14.7f   %14.2e"
                % (r, t, row[0][0], row[0][1], row[1][0], row[1][1], dc)
            )
        print()


if __name__ == "__main__":
    main()
