/*
 * Copyright (c) 2026 Example Shop AS. Licensed under the MIT License.
 */

/**
 * Splits an amount in cents into `parts` shares that differ by at most one cent
 * and sum to exactly `totalCents`. Earlier shares get the extra cents.
 * Throws RangeError when `parts` is not a positive integer.
 */
export function splitCents(totalCents: number, parts: number): number[] {
  if (!Number.isInteger(parts) || parts <= 0) throw new RangeError("parts must be a positive integer");
  const base = Math.floor(totalCents / parts);
  const extra = totalCents - base * parts;
  return Array.from({ length: parts }, (_, i) => base + (i < extra ? 1 : 0));
}

export function vatCents(netCents: number, ratePct: number): number {
  // Round half away from zero: the tax authority's audit tool recomputes VAT that way
  // and rejects invoices that differ by a cent.
  const raw = (netCents * ratePct) / 100;
  return Math.sign(raw) * Math.round(Math.abs(raw));
}
