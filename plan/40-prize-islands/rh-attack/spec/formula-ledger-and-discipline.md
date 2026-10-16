# SPEC — formula-ledger-and-discipline (the memory layer)

PURPOSE. Make the project's knowledge external: no result, formula,
constant, or decision lives only in the working context.

COMPONENTS.
- FORMULAS.md — master formula ledger. Every formula used must exist
  here BEFORE use, labeled: VERBATIM / MEASURED (value+precision+file) /
  DERIVED (derivation file named) / CLASSICAL (author named) /
  READ-PENDING (read primary source first). Training-memory recall is
  a forbidden source. Section-number errors are expected and caught
  (25.11 ≠ counting formula; 25.2.11 = primes, 25.2.12 = zeros).
- READS-*.md — verbatim primary-source captures (1859, GS25, DLMF
  25.2/25.4, DLMF 25.10/25.11…). The ledger stands on these.
- THE-EULER-ACTION.md — the argument: recognition map, E7a/E7b,
  postulate-by-postulate argument, results sections.
- POSTULATES.md — P-W / P-G / P-Z / P-A / P-E (the claims) + P-0
  (the discipline).

P-0 DISCIPLINE (current numbered items).
1 constants computed, never recalled.
2 counts are resolution-limited (twin-floor + dt/2); 2K parity only.
3 two engines per measurement.
4 projections use measured per-eval cost at target scale.
5 2K is a per-height shadow, not conserved.
6 CPU walks single-threaded BLAS + captured output.
7 a port is a free re-audit (known-zero goldens required).
8 NAMED CONSTANTS, NO MAGIC NUMBERS + startup echo/invariant-asserts
   on long jobs (owner's hygiene regimen; the 1000× sizing incident).
9 A result is valid only for the code+data state that made it: bug
   found → earlier results invalid → re-run before citing; defective
   inputs renamed .DEFECTIVE; every cited result carries provenance
   (owner's anti-self-sabotage directive).

OPERATING LOOP (per turn).
recall (wiki) → act → observe (wiki_observe, atomic) → at task end
retro (wiki_retro) → commit exact rh-attack paths only (never e6.28) →
repo push at each certification (claim policy: certified numbers only).
