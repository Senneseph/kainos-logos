# Prize-Islands — the $1M+ curriculum initiative

Owner-directed 2026-08-24 (the large initiative after the bandgen
v0.1 compiler landed, commit 49d9a7f). The owner's words set the
pipeline: **research the targets (prize problems) → plan the
objectives for each → plan the research → develop the lessons and
execute.** The islands are set out so that *everything should
connect from some fundamental relationships* — the ground floor is
shared, the islands are the destinations.

## What gets in (the scope filter, owner's words)

> all outstanding mathematics challenges … that offer a **$1 million
> dollar prize or more** for their solution, requiring **the type of
> analysis our tool is doing**

Two filters, both applied per target and documented in
`02-scope.md`:

1. **Prize ≥ $1,000,000.** Audited against the Prize Problem Ledger
   (prizeproblems.org, 177 numbered targets) plus direct sources:
   the complete list is 6 unsolved Clay Millennium Problems + the
   Beal Conjecture + the IUT Challenger Prize. Full survey with
   verbatim statements in `01-targets.md`.
2. **Our type of analysis.** The store's analysis is *exact,
   discrete, finite*: rational/integer arithmetic, prime structure,
   finite products over the line, scaffolding of prescribed
   theorems from strict part-sets, and honest walls where the
   mechanism's limits are named. Targets that need continuous
   analysis (PDE, constructive QFT) or machinery the store does not
   hold (sheaf cohomology, adversarial proof-refutation) are ruled
   declared-but-not-built, not silently dropped.

## The island map

| Island | Target | Prize | Scope | Status |
|--------|--------|-------|-------|--------|
| **Riemann** | RH (Clay) | $1M | in-scope | **CLOSED** (RH-TRACK S8–S10 + fundamentals S11–S13; the reference island: the *-reach* fact, the missing ingredient articulated, no `theorem:riemann`) |
| **BSD** (elliptic cities) | Birch–Swinnerton-Dyer (Clay) | $1M | in-scope | **CLOSED** (S14–S16 = E6.18–E6.20; summit filed on the two-member panel, `theorem:bsd-panel-satisfaction`) |
| **Beal** (Diophantine triples) | Beal conjecture (AMS/Beal) | $1M | in-scope | **CLOSED** (S17 = E6.21; summit filed on the whole census box, `theorem:beal-line-satisfaction`) |
| **Complexity** | P versus NP (Clay) | $1M | in-scope (epistemic register) | **CLOSED** (S18–S19 = E6.22–E6.23; summit declared open of record, the difficulty filed as `theorem:parity-blowup-filed`) |
| **The connecting work** (this synthesis) | — | — | in-scope (synthesis over the four closed islands) | **OFFICIAL** (S20 = E6.24 "the weaving line", build+freeze `75a0520`, 2026-08-25) — the synthesis band is a band of the course; the four island statements stay open of record, the queue stands intact |
| Navier–Stokes | NS existence & smoothness (Clay) | $1M | OUT (continuous PDE) | declared, not built |
| Yang–Mills | YM existence & mass gap (Clay) | $1M | OUT (constructive QFT) | declared, not built |
| Hodge | Hodge conjecture (Clay) | $1M | OUT (cohomology machinery) | declared, not built |
| IUT | IUT Challenger Prize | $1M | OUT (adversarial refutation meta-problem) | declared; ABC soil shared with Beal/BSD |
| (Certicom ECC-163, Proximity pool shares, 1B-digit prime) | computational challenges | $/$250k | OUT (not open math / below threshold) | noted in the survey |

## The ground floor (where the islands connect)

The owner's requirement — *everything connects from fundamental
relationships* — is the architecture: the islands hang off the
bands, and the bands hang off the same line:

- **the line 0..84** (successor, pi, spf, ledger — bands 1–3 + S11):
  every island's finite machinery is a census over this line.
- **prime multiplicative structure** (S11 spf/sieve; the planned
  CRYPTO-TRACK R0–R4): BSD's point counts live in (F_p)^*; Beal's
  valuations are v_p compositions of the spf chain; P/NP's
  difficulty epistemics ride the same "the door holds" soil the RSA
  destination uses.
- **the zeta family / L-functions** (S13: factors, index splits,
  line partials, removal): BSD's L(E,s) Euler product is the next
  sibling of the S13 family (Euler factors with three terms instead
  of S13's two — the Hasse-Weil factor (1 − a_p u + p u²)); the RH
  island's machinery (region, scale, route, relevance) is the
  exact template for reading L(E,s) at s=1.
- **scaffolded theorems + honest walls** (all tracks): every island
  ends where RH ended — the store holds the prescribed frontier
  theorems (derived from its own premises) and articulates, in
  its own words, the missing ingredient. *Reason about the problem,
  answer questions about it, refuse honestly* — the same contract
  the owner accepted for RH.

## Execution order (this initiative)

1. **Bands S14+ — the BSD island** (the elliptic city): strongest
   fit for existing machinery (S13 L-family + S11 census patterns),
   and the L-function connection is the "islands connect" spine for
   the RH island. See `04-island-bsd.md`.
2. **Bands — the Beal island** (Diophantine triples): valuations
   over the spf chain + an LTE verification ledger (S11-style
   record-don't-optimize); feeds the CRYPTO-TRACK's soil in turn.
   See `06-island-beal.md`.
3. **Bands — the P/NP island** (the logic register): the new
   register (decidable/undecidable, classes, reductions, the
   barriers as walls); the biggest register extension, so last.
   See `05-island-p-np.md`. **DONE (S18–S19, E6.22–E6.23; the
   island CLOSED 2026-08-25).**
4. **The connecting work (owner-directed 2026-08-25)** — the
   synthesis pass over the four closed islands: "the weaving
   line" (S20 = E6.24), research stage A committed in
   `connecting-research.md`. **DONE (E6.24, build+freeze
   `75a0520`, close-out 2026-08-25)**: the band is the course's
   synthesis band (48th experiment — `connecting-research.md` D8
   gate green at full width). It is a NEW owner-directed band,
   OUTSIDE the declared queue (`theorem:queue-declared` stands
   intact — the weaving adds no lot); the standing queues
   (condition-line lots; CRYPTO-TRACK R0–R4, declared not built)
   keep their slots behind it. The CRYPTO joints named under the
   connect requirement stay declared for that track.

All new bands are built **the bandgen way** (spec → validate →
dryrun control → freeze → official gate → close-out), with the
speedup over the S13 hand-built baseline (multi-band, ~7 sessions of
work to official PASS) MEASURED per band and reported — the owner's
"continue to improve where needed" clause applies to the compiler
itself as the bands are built.

The standing queues keep their slots; **FUNDAMENTALS LOT 1 the
condition line is now BUILT and OFFICIAL** (S21 = E6.25, 49th
experiment, close-out 2026-08-27 — `plan/30-phases/phase-6-tutor/
experiments.md` §E6.25 / `condition-line-research.md` Stage B: the
teachable hypothesis + the conditional consequences drilled and
filed as ONE line as `theorem:condition-line-filed`, final 1871 =
1823 + 3 facts + 45 events, line 0..84, seam 146, DAG 40, NO
`theorem:riemann`, the queue byte-intact — Lot 1 consumed in the
accounting of work, lots 2–4 keep their declared slots);
**CRYPTO R0–R4** remain declared, not built. The Beal
island's valuation machinery is declared a shared dependency for
R1–R2 (modular arithmetic over (Z/nZ)^* needs exactly the v_p +
CRT soil Beal builds).

## Document index

- `01-targets.md` — the prize targets (survey, verbatim statements, frontiers)
- `02-scope.md` — the scope rulings + reasoning
- `03-island-riemann.md` — the completed island (status map)
- `04-island-bsd.md` — BSD plan: objective, descent chain, research plan, band plan
- `05-island-p-np.md` — P/NP plan
- `06-island-beal.md` — Beal plan
- `connecting-research.md` — the connecting work, research stage A (2026-08-25)
- (cross-track) `../30-phases/phase-6-tutor/condition-line-research.md` — the forward-fan LOT 1 (the condition line), research stage A + stage B OFFICIAL (2026-08-27)
