// P4 spec T4 (spec/p4-tail-law-abstract.md): the explicit disk the measured
// onset ratio |W_n|/|I| must sit in, s = 1/2 + i t, n >= 1.
//   center = 0.5 * ||s|| / n,   ||s|| = sqrt(t^2 + 1/4)
//   err(t,n) = (t^2 + 1/4) / (12 n^2)
//            + (sqrt(3)/216) * (t^2 + 1/4) * (||s|| + 1) / n^3
// Every factor explicit (second-order EM form + OP2 remainder bound);
// disk, not point: no phase of the (s/12)-term is assumed.

export interface T4TailInterval {
  lo: number;
  center: number;
  hi: number;
  err: number;
}

export const t4TailIntervalAt = (t: number, n: number): T4TailInterval => {
  const normS: number = Math.sqrt(t * t + 0.25);
  const center: number = (0.5 * normS) / n;
  const err: number =
    (t * t + 0.25) / (12 * n * n) +
    (Math.sqrt(3) / 216) * (t * t + 0.25) * (normS + 1) / (n * n * n);
  return { lo: center - err, center, hi: center + err, err };
};
