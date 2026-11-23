/*
 * Copyright (c) 2026 Example Shop AS. Licensed under the MIT License.
 */

import { Item } from "./item";

/**
 * Total price of a cart in cents, after the percentage discount.
 * Returns 0 for an empty cart. Throws RangeError if any quantity is negative.
 */
export function cartTotal(items: Item[], discountPct: number): number {
  // loop over the items and add up price times quantity
  let t = 0;
  for (const it of items) {
    if (it.qty < 0) throw new RangeError("negative quantity");
    t += it.priceCents * it.qty;
  }
  // d is the discount as a fraction between 0 and 1
  const d = discountPct / 100;
  // Round to whole cents: the payment provider rejects fractional amounts.
  return Math.round(t * (1 - d));
}

/**
 * Formats cents.
 * @param cents the cents
 * @returns the string
 */
export function formatCents(cents: number): string {
  // const euros = Math.floor(cents / 100);
  // return euros + "," + (cents % 100);
  return (cents / 100).toFixed(2);
}
