# RH-TRACK — canonical reference set (the "source material" for the Riemann Hypothesis track)

Owner mandate (2026-08-23): "We'll throw as much as we think is
important at it." Unlike the unit-distance track, there is NO single
paper — the corpus is the STANDARD THEORY of RH. This file is the
canonical artifact the transcription audit (house standing rule,
inherited from SAVANT-TRACK) runs against.

## Primary references (canonical monographs / surveys)

- **R1** — Riemann, B. "Über die Anzahl der Primzahlen unter einer
  gegebenen Größe" (1859). Source of: ζ and the Euler product
  (statement), the functional equation (statement), the counting
  formula for zeros (statement), the trivial zeros. (Canonical
  statement source; the English translation "On the Number of Primes
  Less Than a Given Magnitude" is the standard rendering.)
- **R2** — Titchmarsh, E. C. *The Theory of the Riemann Zeta
  Function*, 2nd ed., Oxford, 1986. (Canonical source for the
  analytic statements: continuation + pole, the zero-free region,
  Hardy's theorem, the S(T) bounds, the zero-density estimates,
  RH ⇔ error bounds.)
- **R3** — Edwards, H. M. *Richard Riemann's "Funktion (s)"*,
  Princeton, 1974. (Canonical source for the 1859 paper's content:
  the explicit formulas, the first-zero remarks, the "probably not
  easy" note on the ψ error equivalence — the origin of the
  Pringsheim equivalence.)
- **R4** — Davenport, H. *Multiplicative Number Theory*, 3rd ed.,
  Springer, 2000. (Canonical source for PNT statements, Chebyshev's
  ψ/θ, the Mertens function, the zero-free region in its safe
  classical form.)
- **R5** — Lagarias, J. C. "The Riemann Hypothesis: Arithmetic and
  Geometry" (2002 lecture notes; Mt. Holyoke). Canonical source for
  the criterion family (RH ⇔ λ_n > 0 positivity, stated there in
  full).

## Fetched verifications (pinned 2026-08-23, this session — the
fetched-text audit class, per the standing rule)

- **F1** — Wikipedia, "Li's criterion" (en.wikipedia.org/wiki/Li%27s_criterion),
  fetched 2026-08-23. Pinned statements:
  - λ_n = (1/(n−1)!) · dⁿ/dsⁿ [ s^{n−1} log ξ(s) ] evaluated at s = 1
    (Keiper–Li coefficients);
  - **RH ⇔ λ_n > 0 for every positive integer n ≥ 1**;
  - zero-sum form: λ_n = Σ_ρ [1 − (1 − 1/ρ)^n], the sum over the
    nontrivial zeros in the symmetric sense Σ_ρ = lim_{N→∞}
    Σ_{|Im(ρ)| ≤ N};
  - the criterion was presented by Xian-Jin Li in 1997
    (Bombieri–Lagarias 1999 complemented it); positivity verified
    up to n = 10^5 (a numerical check, quoted as such).
- **F2** — Wikipedia, "Riemann–von Mangoldt formula", fetched
  2026-08-23. Pinned statements:
  - N(T) = (T/2π) log(T/2π) − T/(2π) + O(log T), N(T) = the number
    of zeros with 0 < Im(ρ) ≤ T;
  - stated by Riemann (1859), proved by Mangoldt (1905);
  - Backlund's explicit form: |N(T) − (T/2π log(T/2πe) − 7/8)| <
    0.137 log T + 0.443 log log T + 4.350, T > 2 (the 0.137 constant
    is a denylist term — the student's statement carries only the
    classical form).
- **F3** — Andromath theorem pages (androma.org/theorems/10402 and
  /1693), fetched 2026-08-23 (via search). Pinned statements:
  - **RH ⇔ ψ(x) = x + O(x^{1/2+ε}) for every ε > 0** as x → ∞
    (the Pringsheim/ψ equivalence — classical: Riemann 1859 noted
    the equivalence is "probably not easy to prove"; the formal
    proof is Pringsheim, late 1890s);
  - **RH ⇔ |π(x) − li(x)| = O(√x log x)** for all x ≥ 2
    (Littlewood, 1924).
- **F4** — Bost–Connes / Connes primary sources (numdam EDP preprint
  abstract + alainconnes.org; Wikipedia "Hilbert–Pólya conjecture"),
  fetched 2026-08-23 (via search). Pinned statements:
  - Polya–Hilbert program: find a self-adjoint operator whose
    spectrum is {Im(ρ)} for the nontrivial zeros (Hilbert's 6th
    problem, 1900; Polya from c. 1912);
  - Bost–Connes (1995): a quantum dynamical system (the C*-algebra
    ℂ*(ℚ/ℤ) ⋊ ℕ*) whose partition function is ζ(β);
  - Connes (1999, "Trace formula in noncommutative geometry and the
    zeros of the Riemann zeta function"): explicit formulas
    interpreted as a trace formula on the noncommutative space of
    Adele classes; the paper's own framing: "This reduces the Riemann
    hypothesis to the validity of the trace formula." **Honest split
    (frozen):** the reformulations are theorems; the RH step itself
    is NOT — the self-adjoint route stays an OPEN PROGRAM in the
    store (the student must say exactly that; it is a confounder /
    honesty probe, never a derivation ingredient).
- **F5** — K. Kedlaya, "Error bounds in the prime number theorem"
  (kskedlaya.org/ant, chapter 8), fetched 2026-08-23 (via search).
  Pinned statement: under RH, ψ(x) − x = O(x^{1/2} log^2 x) (the
  zero-boundary error formula), i.e. RH ⇒ the ψ-equivalence error
  term; the zero-free-region side gives ψ(x) = x + O(x exp(−c√log x))
  from the classical region.

## Monograph-citation class (audit by reference, per the owner's
accepted residual-risk clause of the transcription audit)

Every formula-level claim in the frozen scripts that is NOT covered
by F1–F5 cites its canonical reference here by (R#, §) — e.g. the
zero-free region ζ(σ+it) ≠ 0 for σ ≥ 1 − c/log|t| (R4, ch. 30 / R2,
ch. V); Hardy's theorem T(t) → ∞ (R2, ch. XI); the mean square
∫₀^T |ζ(1/2+it)|² dt = T log(T/2π) + (2γ−1)T + O(log T) (R2, ch.
VII); RH ⇔ S(T) = o(log T) (R2, ch. XI — Littlewood 1924); the
Lindelöf hypothesis ζ(1/2+it) = O^ε(1) and RH ⇒ LH (R2, ch. IV);
Littlewood's zero-density bound N(σ,T) = O(T^{3(1−σ)/(2−σ)} log^A
T) (R2, ch. X / R4). Where a reference is listed here, the frozen
script carries the (R#, §) pair as its `source_lines`-slot value
(monograph citations instead of paper line numbers — the audit
adaptation for a non-paper corpus, frozen by this file).

## What is NOT in the store (frozen scope)

- No proof of RH exists in any reference; the track does not pretend
  to "train on the proof". The corpus is the theory AROUND the
  hypothesis: its equivalent formulations, its partial results, its
  numerical evidence.
- No book text reaches the student (house invariant): the student
  sees our canonical one-line statements (the standard names and
  attributions only, as any mathematician's vocabulary carries
  them); the denylist blocks book- and paper-characteristic strings
  (the 0.137 constant, "Platt", "Odlyzko", the 1859 paper title, …).
- The numerical zero-verification record (first 10^13 on the line)
  enters ONLY as a declared numerical fact with the honest
  "verification is not proof" split (W-RH-1).
