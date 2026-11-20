export function availableUnits(onHand: number, reserved: number): number {
  // Units of the SKU that can be sold now: stock on hand minus reservations, never below 0.
  return Math.max(0, onHand - reserved);
}
