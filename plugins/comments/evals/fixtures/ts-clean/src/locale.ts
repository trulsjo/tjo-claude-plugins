export function formatNok(cents: number): string {
  // Chrome before 110 renders the NOK symbol as "NOK" in the nb-NO locale instead of "kr".
  // https://bugs.chromium.org/p/chromium/issues/detail?id=1381996
  return (cents / 100).toLocaleString("nb-NO", { style: "currency", currency: "NOK" }).replace("NOK", "kr");
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function parseAmount(input: any): number {
  // TODO(#311): accept amounts with a thousands separator
  return Math.round(Number(String(input).replace(",", ".")) * 100);
}
