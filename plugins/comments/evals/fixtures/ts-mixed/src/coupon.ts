const applied = new Set<string>();

export function applyCoupon(code: string, totalCents: number): number {
  // checkout.ts retries the payment step and calls applyCoupon a second time,
  // so remember applied codes here and skip them on the second call.
  if (applied.has(code)) return totalCents;
  applied.add(code);
  return Math.max(0, totalCents - 500);
}
