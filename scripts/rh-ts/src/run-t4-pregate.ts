// Day-018 T4 pre-gate (TS side).
//
// Checks, in float64, that the 15 MEASURED onset ratios from
// scripts/rh/out_day004b_onset.txt (day-04b, N in {1e3, 1e4, 1e5} x
// t/N in {0.1, 0.2, 0.5, 1, 2}) sit inside the explicit P4 spec T4
// disk [0.5*||s||/n - err, 0.5*||s||/n + err], and cross-checks the
// interval arithmetic line-for-line against the independent oracle
// run (scripts/rh/day018_t4_pregate.py -> out_day018_t4_pregate.txt).
//
// Output: per-point PASS/FAIL + summary lines, e.g.
//   T4-CONTAINMENT PASS 15/15   ORACLE-CROSS-CHECK PASS 15/15

import { readFileSync, existsSync } from "node:fs";
import { t4TailIntervalAt } from "./t4-tail-interval.ts";

const onsetPath: string = new URL("../../rh/out_day004b_onset.txt", import.meta.url).pathname;
const oraclePath: string = new URL("../../rh/out_day018_t4_pregate.txt", import.meta.url).pathname;

const nValues: readonly number[] = [1000, 10000, 100000];
const fracs: readonly number[] = [0.1, 0.2, 0.5, 1.0, 2.0];

interface OnsetRow {
  n: number;
  t: number;
  ratio: number;
}

// Columns of out_day004b_onset.txt: N, t, |I|, C, C/|I|, r.
const parseOnsetTable = (text: string): OnsetRow[] =>
  text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .filter((line) => {
      const parts: string[] = line.split(/\s+/);
      return (
        parts.length >= 5 &&
        Number.isFinite(Number(parts[0])) &&
        Number.isFinite(Number(parts[1])) &&
        Number.isFinite(Number(parts[4])) &&
        Number(parts[0]) >= 1
      );
    })
    .map((line) => {
      const parts: string[] = line.split(/\s+/);
      return { n: Number(parts[0]), t: Number(parts[1]), ratio: Number(parts[4]) };
    });

const isMeasuredRow = (row: OnsetRow, n: number, frac: number): boolean =>
  row.n === n && Math.abs(row.t / row.n - frac) < 1e-12;

// Oracle data rows look like:
//   1000 0.1 100.0 0.0500 0.050001 8.415e-04 1.68%  PASS
const parseOracleRows = (text: string): { n: number; frac: number; t: number; center: number; err: number }[] =>
  text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .filter((line) => /^\d/.test(line))
    .map((line) => {
      const parts: string[] = line.split(/\s+/);
      return { n: Number(parts[0]), frac: Number(parts[1]), t: Number(parts[2]), center: Number(parts[4]), err: Number(parts[5]) };
    })
    .filter(
      (row) =>
        row.n > 0 &&
        Number.isFinite(row.frac) &&
        Number.isFinite(row.t) &&
        Number.isFinite(row.center) &&
        Number.isFinite(row.err) &&
        row.frac <= 2.0
    );

const relativeDifference = (a: number, b: number): number =>
  Math.abs(a - b) / Math.max(Math.abs(a), Math.abs(b), 1e-300);

interface GatePoint {
  n: number;
  frac: number;
  t: number;
  ratio: number;
  found: boolean;
  inside: boolean;
  marginPct: number;
}

const evaluatePoint = (rows: readonly OnsetRow[], n: number, frac: number): GatePoint => {
  const row = rows.find((r) => isMeasuredRow(r, n, frac));
  const found: boolean = row !== undefined;
  const t: number = row !== undefined ? row.t : 0;
  const ratio: number = row !== undefined ? row.ratio : Number.NaN;
  const interval = t4TailIntervalAt(t, n);
  const inside: boolean = found && interval.lo <= ratio && ratio <= interval.hi;
  const marginPct: number =
    found && interval.center > 0
      ? (100 * Math.min(ratio - interval.lo, interval.hi - ratio)) / interval.center
      : Number.NaN;
  return { n, frac, t, ratio, found, inside, marginPct };
};

const pointLine = (point: GatePoint): string => {
  const interval = t4TailIntervalAt(point.t, point.n);
  const verdict: string = point.inside ? "PASS" : "*** FAIL ***";
  return `T4   n=${point.n}  t=${point.t}  meas=${point.ratio}  center=${interval.center}  err=${interval.err}  margin=${point.marginPct}%  ${verdict}`;
};

const main = (): number => {
  const rows: OnsetRow[] = parseOnsetTable(readFileSync(onsetPath, "utf8"));
  const points: GatePoint[] = [];
  let ni: number = 0;
  while (ni < nValues.length) {
    let fi: number = 0;
    while (fi < fracs.length) {
      const point = evaluatePoint(rows, nValues[ni]!, fracs[fi]!);
      points.push(point);
      fi += 1;
    }
    ni += 1;
  }
  const oracleRows: { n: number; frac: number; t: number; center: number; err: number }[] = existsSync(oraclePath)
    ? parseOracleRows(readFileSync(oraclePath, "utf8"))
    : [];
  const crossChecks: boolean[] = oracleRows.map((row) => {
    const interval = t4TailIntervalAt(row.t, row.n);
    return relativeDifference(interval.center, row.center) < 1e-12 && relativeDifference(interval.err, row.err) < 1e-12;
  });
  const contained: number = points.filter((p) => p.inside).length;
  const crossPass: number = crossChecks.filter((x) => x).length;
  let pi: number = 0;
  const printPoint = (): void => {
    console.log(pointLine(points[pi]!));
    pi += 1;
  };
  while (pi < points.length) printPoint();
  console.log("# width per t/N at n=1000 (spec hand-claim: 0.09% / 0.34% / 2.2% / 9.1% / 40%):");
  let wi: number = 0;
  const printWidth = (): void => {
    const frac = fracs[wi]!;
    const interval = t4TailIntervalAt(1000 * frac, 1000);
    const pct: number = 100 * interval.err;
    const found: boolean = points.some((p) => p.n === 1000 && p.frac === frac);
    console.log(`  t/N=${frac}  err_pct_of_ratio=${pct}% (absolute, percentage points)  (measured row found: ${found ? "yes" : "no"})`);
    wi += 1;
  };
  while (wi < fracs.length) printWidth();
  const allContained: boolean = contained === points.length;
  const allCross: boolean = crossPass === crossChecks.length && crossChecks.length > 0;
  console.log(`T4-CONTAINMENT ${allContained ? "PASS" : "FAIL"} ${contained}/${points.length}`);
  console.log(
    crossChecks.length > 0
      ? `ORACLE-CROSS-CHECK ${allCross ? "PASS" : "FAIL"} ${crossPass}/${crossChecks.length}`
      : "ORACLE-CROSS-CHECK SKIP (out_day018_t4_pregate.txt absent — run scripts/rh/day018_t4_pregate.py)"
  );
  return allContained && (crossChecks.length === 0 || allCross) ? 0 : 1;
};

process.exitCode = main();
