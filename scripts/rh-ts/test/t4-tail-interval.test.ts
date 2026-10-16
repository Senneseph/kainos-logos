import { test } from "node:test";
import assert from "node:assert/strict";
import { t4TailIntervalAt } from "../src/t4-tail-interval.ts";

// Goldens: computed (not copied) in the independent float64 oracle
// (scripts/rh/day018_t4_pregate.py, host python3, 2026-09-12) — full
// repr printed by the oracle for these five (t, n) points.

test("t4TailIntervalAt goldens (python float64 oracle)", () => {
  const golden: [t: number, n: number, lo: number, center: number, hi: number, err: number][] = [
    [0.0, 1, 0.22615963401463737, 0.25, 0.27384036598536265, 0.023840365985362634],
    [1.0, 1, 0.43362033650068477, 0.5590169943749475, 0.6844136522492101, 0.12539665787426266],
    [100.0, 1000, 0.04915917158544117, 0.0500006249960938, 0.05084207840674643, 0.0008414534106526319],
    [1000.0, 1000, 0.40863993283180833, 0.5000000624999961, 0.5913601921681838, 0.09136012966818774],
    [2000.0, 1000, 0.6024845661423494, 1.0000000312499995, 1.3975154963576495, 0.3975154651076501],
  ];
  let gi: number = 0;
  const checkGolden = (): void => {
    const [t, n, lo, center, hi, err] = golden[gi]!;
    const got = t4TailIntervalAt(t, n);
    assert.ok(
      Math.abs(got.lo - lo) < 1e-15,
      `lo mismatch at t=${t}, n=${n}: ${got.lo} vs ${lo}`
    );
    assert.ok(
      Math.abs(got.center - center) < 1e-15,
      `center mismatch at t=${t}, n=${n}: ${got.center} vs ${center}`
    );
    assert.ok(
      Math.abs(got.hi - hi) < 1e-15,
      `hi mismatch at t=${t}, n=${n}: ${got.hi} vs ${hi}`
    );
    assert.ok(
      Math.abs(got.err - err) < 1e-15,
      `err mismatch at t=${t}, n=${n}: ${got.err} vs ${err}`
    );
    gi += 1;
  };
  while (gi < golden.length) checkGolden();
});

test("t4TailIntervalAt: the five measured onset ratios sit inside their disks", () => {
  // Measured C/|I| from scripts/rh/out_day004b_onset.txt (day-04b), n = 1000 row.
  const measured: [frac: number, ratio: number][] = [
    [0.1, 0.05],
    [0.2, 0.1],
    [0.5, 0.2509],
    [1.0, 0.5071],
    [2.0, 1.062],
  ];
  let mi: number = 0;
  const checkMeasured = (): void => {
    const [frac, ratio] = measured[mi]!;
    const interval = t4TailIntervalAt(1000 * frac, 1000);
    assert.ok(interval.lo <= ratio && ratio <= interval.hi, `ratio ${ratio} at frac ${frac} outside [${interval.lo}, ${interval.hi}]`);
    mi += 1;
  };
  while (mi < measured.length) checkMeasured();
});
