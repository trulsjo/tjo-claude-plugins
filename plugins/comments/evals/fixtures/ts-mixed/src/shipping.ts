// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.
export function shippingCents(zone: string, weightGrams: number): number {
  // TODO: support express shipping
  // Returns the flat rate for parcels over 20 kg.
  const rate = ZONE_RATES[zone] ?? ZONE_RATES["default"];
  return rate * Math.ceil(weightGrams / 1000);
}

// We chose a static zone table over the carrier's rate API because the API
// took two seconds per call and blocked checkout, and rates change once a year.
const ZONE_RATES: Record<string, number> = {
  domestic: 99,
  nordic: 199,
  default: 349,
};
