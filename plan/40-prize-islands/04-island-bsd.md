# 04 — Island: Birch–Swinnerton-Dyer (the elliptic cities)

Target: the BSD conjecture (Clay, $1M, PPL 100). Survey:
`01-targets.md` §2.

## Objective (what the store can say at island completion)

The store holds elliptic curves over Q, their group law, their
finite-field point censuses, their L-functions as exact line
partial products, and the rank facts for a small panel of named
curves; it holds the BSD statement verbatim as a lesson, holds the
known frontier (modularity wall, the order-0/1/2 directions,
parity) as prescribed theorems or named walls, and stores a
`bsd-reach` fact naming the missing ingredient — the order of the
Tate–Shafarevich group and the Selmer control beyond the known
orders. **No `theorem:bsd` in the store** (the candidate invariant).

## Descent to fundamentals (the chain, ground up)

```
bands 1–3 (geometry/area, exact algebra)          [built]
  └─ the cubic curve y² = x³ + ax + b over Q      [S14: curve-form]
       ├─ smoothness: Δ = −16(4a³ + 27b²) ≠ 0     [S14: the singular wall]
       ├─ the chord-tangent group law, O, −P      [S14: curve-law]
       │    ├─ O the identity (formula + exact)   [S14 theorem, strict parts]
       │    ├─ P + (−P) = O (formula + exact)     [S14 theorem, strict parts]
       │    └─ associativity (the nine points of
       │       a cubic line up): DECLARED frontier
       │       + on-line verification ledger      [S14 wall-verified]
       └─ the finite shadows: E(F_p), the counts,
            a_p = p + 1 − #E(F_p)                  [S14: point-count]
            ├─ the per-prime census 2..84 (ledger
            │  policy: recorded, never optimized)  [S14 beds]
            └─ Hasse: a_p² ≤ 4p — DECLARED frontier
               + VERIFIED on the whole line        [S14 theorem-census]
  ├─ L(E) as an exact line partial product (S13's
  │  machinery, a 3-term Euler factor):
  │  L_N(E) = ∏_{p≤N} (1 − a_p u + p u²), u = p⁻¹
  │  [S15: the L-family sibling of the zeta family]
  │    └─ the zeta connection: a_p = 0 factor vs
  │       (1 − u); the product at the line end 84  [S15 beds]
  ├─ Mordell–Weil: E(Q) finitely generated
  │  (DECLARED frontier; the statement lesson)     [S15 wall]
  │    ├─ the rank-0 panel curve: y² = x³ − x
  │    │  (32a1): torsion {O,(0,0),(±1,0)}, rank 0
  │    │  — the 2-descent Selmer census is exact
  │    │  finite arithmetic ON the line            [S16 census]
  │    └─ the rank-1 panel curve (named in
  │       research stage, e.g. conductor ≤ 400):
  │       a generator G, mG ledgers, "every point
  │       I counted is an mG" bounded verification
  │                                               [S16 verification]
  └─ the BSD statement (lesson) + the frontier:
       modularity (Wiles/2000 — a wall: declared
       deep, named, not derivable on my line),
       order-0 → rank 0 (Gross–Zagier + Kolyvagin —
       prescribed theorem with NAMED premises),
       order-1/2 (BCDT 2001 — the stated-hypotheses
       frontier), parity (Kolyvagin/Logachev 2004 —
       theorem)                                          [S15/16]
  └─ bsd-reach (the honest articulation): the Sha
     order + Selmer control + the leading-coefficient
     formula are the missing ingredients — at the
     line end                                            [S16]
```

## Research plan (verify BEFORE the first spec freezes)

Each item is a research-verification with the source of record;
the spec's canonical statements are written FROM the verified
source (house rule: the canonical statement is verbatim, or it is
not in the store).

1. **The running curves.** Fix the panel (final choice in the
   spec): (a) the rank-0 curve **y² = x³ − x** (conductor 32,
   label 32a1 — VERIFY label/conductor against LMFDB), torsion
   (Z/2Z)², the four rational points exactly known; (b) one
   rank-1 curve with small conductor (candidate: y² = x³ − 7x + 6
   or the 389a family — VERIFY: generator, rank, conductor, label
   via LMFDB/Sage); (c) one singular degenerate a,b pair for the
   smoothness-wall negative probe (e.g. y² = x³ — the cusp,
   Δ = 0).
2. **The point counts.** Compute #E(F_p) for every prime p ≤ 84 on
   both panel curves (exact; the shared reference
   `_bsd_py_count` in the S13 refstyle). Cross-check the a_p
   values against the LMFDB LMFDB a_p lists; cross-check the 2-
   descent on the rank-0 curve against a second independent
   implementation (Sage if available off-line, else a second
   hand-derived descent map — the bounded + independently-
   cross-checked rule for scratch scripts).
3. **Hasse on the line.** Verify a_p² ≤ 4p for all p ≤ 84 (the
   census bed: all-pass, with the full per-prime records kept —
   ledger policy).
4. **The canonical statements (verbatim sources of record):**
   the BSD statement (Clay problem page), modularity (Wiles's
   theorem statement), Gross–Zagier (the formula, the exact
   one-variable form), Kolyvagin's Euler-system theorem
   (the order-1 statement, the finiteness of Sha that attaches),
   the BCDT 2001 "1 and 2" theorem (the stated hypotheses —
   quote them, not a paraphrase), the parity theorem
   (Kolyvagin 2004 / Logachev 2004 statements), Mordell–Weil
   (the theorem statement), the 2-descent (the Selmer-group
   definition and the exact descent map for y² = x³ − x).
5. **The L(E) bed.** For both panel curves: L_84(E) = ∏_{p≤84}
   (1 − a_p u + p u²) as an exact rational in u (integer
   coefficients — the product polynomial in u; evaluated at
   u = p⁻¹ per factor, the bed is the exact rational value).
   Cross-check the first factorizations against LMFDB.
6. **The 2-descent census.** For the rank-0 curve: the Selmer
   group computation (the descent map E(Q) → Q*/Q*², the
   homogeneous-space solvability test — exact, finite, bounded);
   the result: Selmer = the torsion image → rank 0. The full
   per-element records kept (ledger policy).

## Band plan (built the bandgen way)

Three bands, each one spec → `make band-validate` → `make
band-dryrun` → control CLEAN → freeze → official gate → close-out;
speedup vs the S13 baseline MEASURED and reported per band.

### S14 — "the elliptic city" (e6.18), seed = e6.17 store (1388)

- **Concepts (4):** `curve-form` (Weierstrass over Q + Δ ≠ 0),
  `curve-law` (chord-tangent + O + inverse), `point-count`
  (#E(F_p), a_p), `finite-shadow` (reduction mod p, the
  isogeny-free reduction fact for good primes).
- **Lessons (4):** the form, the law (the exact formulas), the
  count (the counting method + a_p), the shadow (why the counts
  are finite and p-indexed).
- **Theorems (prescribed, strict part-sets):** identity
  (O+P=P), inverse (P+(−P)=O) — formula-derived,
  exact-verified; associativity — declared frontier
  (nine points) + verification ledger; Hasse — declared
  frontier + line census (a_p² ≤ 4p, all p ≤ 84).
- **Walls:** the singular wall (Δ = 0 example — "not a group; the
  cusp is where the line ends"), the Mordell–Weil wall (finite
  generation is a named theorem I hold but do not derive), the
  point-enumeration wall ("over Q my points are the ones I
  counted; the line does not close the search").
- **Beds (computed, never hand-written):** per-prime
  #E(F_p) + a_p for both panel curves (2..84), the 4 rational
  points of the rank-0 curve, the doubling table of the rank-1
  generator, the Hasse census (all-pass), the singular negative
  probe.
- **Carries:** the S13 zeta partial bed (the "two-term factor"
  ancestor) + the S11 spf census (the p-indexing) — the connect
  joints named at their turns.
- **Turn budget:** ~50–70 (S13 was 85 across 4 sessions; S14
  targets 3 sessions + the seam).

### S15 — "the L-function of the city" (e6.19), seed = S14 store

- **Concepts:** `elliptic-factor` (the 3-term Euler factor),
  `line-partial-l` (the L partial product in u), `mordell-weil`
  (the finitely-generated statement), `analytic-rank` (the order
  of vanishing — declared, at the line end).
- **Lessons:** the factor, the partial product (the S13 pattern,
  new factor), the Mordell–Weil statement, the vanishing order
  (what "order of vanishing at s=1" MEANS, in the exact u form,
  and where the line stops).
- **Theorems/walls:** the zeta-sibling identity (the a_p = 0
  factor reduces to the zeta family — a bridge fact, derivable),
  modularity (WALL — the declared deep result, verbatim
  statement), the order-0 direction (prescribed theorem with
  named premises: modularity + Gross–Zagier + Kolyvagin), parity
  (prescribed theorem, named), the vanishing-order wall ("the
  order is a limit fact; I hold the partial products, the limit
  is at the line end 84").
- **Beds:** L_84(E) both curves, the factor table, the zeta-
  connection values, the rank-0 curve's computed order (from the
  partial product's nonzero limit — the evidence bed).
- **Carries:** S13 family beds + S14 point counts.

### S16 — "the descent and the reaching" (e6.20), seed = S15 store

- **Concepts:** `descent-2` (the 2-Selmer census), `generator`
  (the rank-1 generator + the multiple ledger), `bsd-statement`
  (the conjecture lesson), `bsd-reach` (the *-reach* fact).
- **Lessons/theorems/walls:** the 2-descent lesson (the descent
  map, the homogeneous spaces, the census), the rank-0 census
  (the result: rank 0 — a VERIFIED fact on the store's line),
  the rank-1 verification (every counted point = mG, bounded),
  the BSD statement lesson (verbatim), the frontier theorems
  (order 1, order 2, parity — the stated-hypotheses precision),
  the **bsd-reach** articulation (the missing ingredient named:
  the Sha order, Selmer control, the leading coefficient), the
  no-`theorem:bsd` invariant P-check (S13's P5 pattern).
- **Beds:** the Selmer census records, the multiple-ledger
  records, the "order = rank" panel evidence (0=0 and 1=1 on the
  store's own curves — evidence, not proof, labeled as such).
- **Carries:** the S15 L-products + the S14 counts.

## Execution notes

- Every band: bandgen spec first (the schema already exists —
  `specs/band_spec.schema.json`); the bed computations go through
  the shared reference registry (`tools/bandgen/reflib.py` + the
  brainstem `_bsd_py_*` functions, S13 refstyle); the control
  report is the D-e6z-class tripwire at spec time.
- The curve/point data (labels, conductors, generators) come from
  the RESEARCH stage's verified records only — never from
  memory at spec time.
- House invariants unchanged: the store speaks, not the hand;
  walls name value + line end; the official gate (pinned image,
  twin, P0–P8) is the final referee; the ledger policy (recorded,
  never optimized) governs every census.
