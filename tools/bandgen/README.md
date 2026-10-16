# bandgen — the band compiler (v0.1)

The per-band source of truth for the tutor curriculum is a **spec**
(`bands/spec-*.json`, schema `specs/band_spec.schema.json`). bandgen
turns a spec into a **frozen-shape table** and reports the diff
between what the spec declares/predicts and what the **mechanism**
does. The compiler automates production; it never edits the
mechanism and never replaces the official gate (pinned image, twin,
P0–P8). The store speaks, not the hand — including here: every
captured byte in the control is the mechanism's; the compiler only
reports.

## Why it exists

In the hand-built era (S11–S13), each band's frozen constants were
assembled across five modules plus tmp scratch, and the deviations all
lived in the transcription:

- **D-e6h(b):** a bed computed by hand came out as a reciprocal
  product; the limit cross-check caught it.
- **D-e6h(d):** three hand-letter predictions (U) disagreed with the
  mechanism (F/H) at build time, plus a 31-vs-32 letter-count slip.
- **D-e6h(e):** hand-built draft counts (84 pre-states vs the
  mechanism's 88, 10 carry refs vs 7, 54 derived rows) had to be
  corrected to the mechanism's tables.

Every one of those is now a **spec-time, diff-reporting, exact-message
issue** — or simply absent, because the value was never hand-written
in the first place.

## The model

```
spec (the training data)            bandgen                          artifacts
─────────────────────────           ─────────                        ─────────
concepts + canonical statements  ─►  C0 structural          ─►  control report
lessons, theorems + parts           C1 seed (identity/      (md + json:
the labeled turn script (+kind)      total/line end,           diffs, or CLEAN)
walls + honest words +               computed from the        ready to freeze
  articulations                       file)                    ──► freeze: the table
beds as COMPUTATION (ref + args)   ─►  C2 beds            ─►  becomes the band's
carry + off-script sources          (reference registry       FROZEN dict; the
predictions (letters, mastery,      vs declared)              official gate (P0–P8,
  totals, seam, offline watch)                              pinned image, twin)
                                                              confirms and freezes
```

The compiler **computes** (never hand-writes): the numeric beds
(reference registry → brainstem's own `_s11_py_*`/`_s13_py_*`
functions, the same ones P4 cross-checks against), the carry bytes
(seed-only runtime, exactly P6's mechanic), the pre-states (a runtime
boot over the seed — replacing the hand-built E616_FROZEN chain), the
letters (the e614 mapping over the captured turns), the mastery
census (pre/post, no-regressions, the D-e6y drill census), and the
store totals (delta accounting, line census, the determinism twin).

The compiler **declares** (the human-authored part that SHOULD take
time): the canonical statements verbatim (house rule), the walls'
honest words, the curriculum (concepts, prereqs, the turn script),
the beds' *computations* (what to compute, not the value), and the
predictions (letters, mastery, seam) — which the control diffs
against the mechanism at SPEC time. That diff file is the D-e6z
deviation class, caught before any code is frozen.

## Workflow (a new band)

1. **Author the spec** `bands/spec-e6.XX.json` (the training data).
   Schema: `specs/band_spec.schema.json`. The band's brainstem module
   (concepts/lessons/theorems/walls/modes) must be merged first —
   the dry-run boots the mechanism's own registry, and the compiler
   REFUSES (it does not special-case) a band whose concepts are not
   in it.
2. `make band-validate NAME=e6.XX` — fast: schema + structural checks
   (prereq graphs point down, part sets are subsets of taught
   lessons, refs unique/padded, wall articulations name the line
   end, the carried S9 denylist scan over the whole script + every
   declared byte).
3. `make band-dryrun NAME=e6.XX` — the full control in the pinned
   image: seed checks, computed beds, the 85-turn labeled dry-run
   x2 (the determinism twin), the seed-only carry run, mastery
   pre/post, totals, the unconditional/conditional discipline +
   off-line hygiene. Exit 0 = **CLEAN — ready to freeze**.
4. Resolve every DIFF in the SPEC (the mechanism governs — if the
   mechanism's letters differ from your prediction, your prediction
   was wrong; same for counts and counts-of-counts).
5. **Freeze**: the control report's `table` IS the frozen-shape
   FROZEN dict (key-for-key with the experiments' tables — proven on
   S13 by `tests/tools/test_bandgen.py`). The experiment module
   carries it; the official gate (pinned image, `--user 1000:1000`,
   twin, P0–P8) is unchanged and remains the referee.

## The checks (and the house rules they enforce)

| check | enforces |
|-------|----------|
| C0 structural | the curriculum's own logic (above) |
| C1 seed | identity/total/line-end computed from the seed file, not believed |
| C2 beds | beds are reference-evaluated (D-e6h(b) bug class impossible) |
| C4 letters | the author's predicted letter sequences vs the e614 mapping over the captured turns (D-e6h(d) class, at spec time) |
| C5 kinds | per-kind semantics: gap naming, teach slots, derive T + facts stored, scaffold/missing honesty (needs_info, named part, no fabricated evidence, no store write), wall byte + articulation + line-end naming, the zero-derive RESPONSE-TEXT rule, carry membership, bed grounding in the final store, theorem cites in the captured grounded set |
| C6 carry | the seed-only runtime re-answers the seam carries byte-identically (P6 mechanic) + off-script derivations grounded |
| C7 mastery | pre-states COMPUTED from the seed (D-e6h(e) class removed), no regressions on carried concepts, new concepts at declared band-end, the D-e6y drill census |
| C8 totals | final = seed + facts + events, line end kept, successors exactly 1..end, every new fact present, the determinism twin (dump + store identity) |
| C9 discipline | the marker ABSENT on band facts when the band is unconditional, PRESENT on the kept facts (no drift), and the declared off-line witness literals never floating into on-line answers (D-e6z hygiene) |

## Reference case (the acceptance contract)

`bands/spec-e6.17.json` (S13) was backfilled once from the official
S13 artifacts, and `tests/tools/test_bandgen.py` proves the compiler
reproduces `e617.FROZEN` **exactly, key by key** (84-table scale:
letters, all derived bytes, beds, walls, carries, 88 pre-states,
mastery, the theorem DAG, totals) and that the computed beds equal
brainstem's `S13_BEDS`. If the compiler lies, that test is the
trip-wire — before any future band trusts a CLEAN report.

## Scope notes (v0.1)

- Template shape: the FUNDAMENTALS/SAVANT/RH recurring form
  (S11–S13). A spec that does not fit the closed turn-kind set
  fails validation rather than being special-cased — that is by
  design; odd one-off bands (e6.5–e6.11 era) stay hand-built.
- Code generation (emitting the experiment module + tests +
  registration from a CLEAN report) is **Phase 2**. Until then the
  control report's `table` is the frozen input, pasted/generated by
  the usual hand — but every value in it was either declared or
  computed, never transcribed.
