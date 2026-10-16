# C6 — the audit-point margin wire (abstract spec)

Status: SPEC → implemented (day-021, after C1a)
Parent: `closure-module-abstract.md` (the §8 composition); C5b is the
conditional closure it serves.

## 0. Where C6 sits

C5b (`p9_closure_rh_of_margin`) proves §8 under one explicit
hypothesis: `hmargin` — the squeezed-margin predicate at every
off-line pair.  Its role by design: the squeezed margin enters as a
hypothesis whose real witnesses are the measurement constants (the
module does not re-measure in Lean).

C6 is the final composition step: it names the **audit-point
measurement package** — the three point-measured facts
(`hZero`, `hDef`, `hStrict`, below, each with its source tag) — and
shows they instantiate `hmargin`, so that §8 becomes one statement:

    RH q  ⟸  the point-measured audit package at every off-line pair.

After C6, the non-machine inputs of the whole §8 argument are exactly
three per point, all PINNED with script + record:
  hZero   (zero side)      — bridge §6 + detector §7 audit
  hDef    (definition side) — P8Floor A4.3 wiring at the Xval pin
  hStrict (the strict gap)  — the day-020 worstcase margin record

Everything else (C0 minimality, the C5 squeeze, the C5b closure, C1a
the own-height detector, C1-far) is machine-proven.

## 1. The audit formulas (from `scripts/rh/day020_worstcase.py`)

At a candidate pair height g and scan height t (the measured point):

    resid(t) = |zeta(1/2 + i t) - K_on(t)|      (= Q(t), the §10 LHS;
              A0 same-object: identically |W_n - (K_on - (P_n - I))|)
    dev(t)   = |K_on(t)| * min_d |R(g, d, t) - 1|   (kernel change,
              §7 detector; R the exact B5 closed form, spot-checked
              vs the direct 4-zero definition to ~1e-16)
    MARGIN(t) = dev / resid          (record: worst 112.6 over the
              4 candidate pairs x straddle windows [g-12, g+12],
              d_min = 0.005)

The day-020 worstcase record (`out_day020_worstcase.txt`) also
verified the closed-vs-direct R to 1e-16 at every candidate pair and
carried the Xval pin (|x| <= 3.9665418656908 at t = 1000.041572,
band (2t, 1e5], 206x headroom, `out_day020_xval_pin.txt`).

## 2. The formal atoms

C6 maps the audit package onto the C5b `hmargin` witness tuple
(Q, dev, flo, Mf, Bfloor, Mr), choosing the canonical instantiation
flo := dev, Mf := 0, (Bfloor, Mr) := (Q, 0) for the definition side:

  (i)  Q >= dev - Mf        becomes  Q >= dev       [hZero, Mf = 0]
  (ii) dev >= flo           becomes  dev >= dev     [rfl]
  (iii) Q <= Bfloor + Mr    becomes  Q <= Q         [hDef carried by
                                                     the measurement
                                                     of Q itself]
  (iv) Bfloor + Mr + Mf < flo becomes Q < dev       [hStrict]

i.e. the audit-point package IS (hZero, hDef, hStrict) mapped
straight onto the witness tuple — and that is exactly what C6 states.
(hDef is the third point-measured fact: the measured resid Q sits
below the A4.3-wired definition-side bound Bf + Mr at the Xval pin —
the same point values the audit computed.)

### C6.1 — `p9_audited_package_strict` (LEAN-PROVEN arithmetic)
Given a point with the point-measured facts
  hZero  : Q >= dev - Mf        (Mf the zero-side reduction error)
  hDef   : Q <= Bf + Mr         (A4.3 wiring at Xval)
  hStrict: Bf + Mr + Mf < dev   (the audited strict gap, 112.6x form)
exhibit the C5b hmargin witness tuple (flo := dev):
  exists Q' dev' flo' Mf' Bf' Mr',
    Q' >= dev' - Mf' /\ dev' >= flo' /\ Q' <= Bf' + Mr' /\
    Bf' + Mr' + Mf' < flo'

Body: the 6-tuple (Q, dev, dev, Mf, Bf, Mr) with the hypotheses,
le_rfl (for dev >= dev), and hStrict — no new mathematics; the value is the NAMED interface.

### C6.2 — `p9_closure_at_audit_point` (LEAN-PROVEN composition)
    theorem p9_closure_at_audit_point (q : ZeroSet)
      (hAudit : forall (t0 d0 : RR) (ht0 : 0 < t0) (hd0 : 0 < d0)
        (hpair : an off-line pair at (t0, d0) in q),
        exists (dev Q Mf Bf Mr : RR),
          Q >= dev - Mf and Q <= Bf + Mr and Bf + Mr + Mf < dev) :
      RH q
Body: C5b with hmargin := (hAudit mapped through C6.1) — i.e. the
§8 closure instantiated at the audit package.  One-line application;
the content is that the package IS the hypothesis C5b needs.

NOTE ON THE PACKAGE (honest split): the package drops `dev >= flo`
as a separate line because flo := dev absorbs it; the detector-scale
content (C1-far / A4.2 pin / C1a own-height positivity) lives in the
MEASUREMENT of dev (dev = |K_on| min_d |R-1|, the §7 detector), not
in the Lean statement.  C1a guarantees its own-height mass is
strictly positive — a structural guarantee on the measurement,
machine-proven — while the dev values themselves remain PINNED.

### C6.3 — `p9_zero_side_of_bridge` (CITED, documented in-module)
The zero-side identity behind hZero: at a candidate pair (g, d),
  Q = |zeta - K_on| >= |K_on| * |Ker - 1| - |W_n-side reduction error|
  =: dev0 - Mf,
with dev0 >= dev := |K_on| min_d |R(g,d,_) - 1|.  Basis: the bridge
identity zeta = K_on * (kernel) (DLMF 25.2.12 factorization, CITED;
E7b1 numerical audit, day-009 record) + the detector reduction
(day-010 d4d3 audit, the dev measurement).  Not re-proven in Lean
(the kernel product over n zeros with the P4 tail is the measurement
side).  Tagged on hZero in the module doc.

## 3. Sources (outline 11 + records)

  - day020_worstcase.py + out_day020_worstcase.txt (margin 112.6,
    closed-vs-direct 1e-16, d_min 0.005) — PINNED measurement.
  - day020_xval_pin.py + out_day020_xval_pin.txt (Xval =
    3.9665418656908, 206x, hS at both band endpoints) — PINNED.
  - DLMF 25.2.12 (the bridge kernel) — CITED.
  - E7b1 audit trail (day-009 records) — the kernel-product vs zeta
    numerical identity — PINNED/CITED.
  - P8Floor A4.3 / P4Limit L5 / B3 Sbar — the definition-side wiring
    — LEAN-PROVEN (imported).
  - C1a (this module) — own-height detector positivity — LEAN-PROVEN.

## 4. Acceptance

  [ ] C6.1 green in probe, ported to Closure.lean.
  [ ] C6.2 green in probe, ported to Closure.lean.
  [ ] C6.3 documented as a CITED line in the module header.
  [ ] Module header STATUS + HONEST SPLIT + COMPOSITION ROOT updated
      (C6 present; the §8 closure "at the audit point" stated).
  [ ] Full build 0 errors 0 sorry; b5core_check PASS; smoke PASS.
  [ ] README P9 row + outline P9 row + DISCOVERY_LOG 16; day-021 addendum.
  [ ] git commit + PUSH (owner: no more push gaps).
