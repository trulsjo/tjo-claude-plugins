# Comments audit — 2026-11-21

Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 2, ticket 2, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: Delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`
  Fix: Delete the doc comment, or rewrite with what the reader cannot see (the format produced, e.g. "1234 → '12.34'").

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: Delete both lines; git keeps them.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control — no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: Append a link to the upstream Node.js or V8 issue that tracks this behaviour. (No URL found in this repo; link should point to the relevant Node.js/V8 issue tracker entry.)

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: Delete; history lives in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: Delete or rewrite to match the actual behaviour (weight-based rate that applies at any weight, with no 20 kg threshold).

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > `"""Builds report. :param rows: the rows :param path: the path """`
  Fix: Delete the noise, or rewrite with what the reader cannot see (expected row schema, CSV column layout, file-creation side effect).

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: Delete the line; git keeps it.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: Delete; history lives in commit messages.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: Delete the comment.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming or structure)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: Rename `d` to `discountFraction`, then delete the comment.

  ```diff
  --- a/shop/src/cart.ts
  +++ b/shop/src/cart.ts
  @@ -18,5 +18,4 @@
  -  // d is the discount as a fraction between 0 and 1
  -  const d = discountPct / 100;
  +  const discountFraction = discountPct / 100;
     // Round to whole cents: the payment provider rejects fractional amounts.
  -  return Math.round(t * (1 - d));
  +  return Math.round(t * (1 - discountFraction));
  ```

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: Fix checkout.ts to stop calling applyCoupon twice, then remove the deduplication guard and the `applied` set from coupon.ts. File a ticket if the caller fix is out of scope.

  ```diff
  --- a/shop/src/coupon.ts
  +++ b/shop/src/coupon.ts
  @@ -1,9 +1,5 @@
  -const applied = new Set<string>();
  -
   export function applyCoupon(code: string, totalCents: number): number {
  -  // checkout.ts retries the payment step and calls applyCoupon a second time,
  -  // so remember applied codes here and skip them on the second call.
  -  if (applied.has(code)) return totalCents;
  -  applied.add(code);
     return Math.max(0, totalCents - 500);
   }
  ```
  Note: checkout.ts is not in this repo; the caller fix must land first.

---

### Ticket

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: File a ticket and replace with `TODO(#<n>): support express shipping`, or delete.

  **Draft ticket**
  Title: Add express shipping support
  Body: `shop/src/shipping.ts:3` holds an untracked TODO for express shipping. The current `shippingCost` function covers only standard zone-based rates; express rates and delivery-time logic are not implemented. This ticket tracks that work.
  Files to: no tracker found — draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: File a ticket and replace with `# TODO(#<n>): retry the upload when the network drops`, or delete.

  **Draft ticket**
  Title: Add network-retry logic to the deploy script upload step
  Body: `scripts/deploy.sh:7` holds an untracked TODO for retrying the rsync upload on network failure. Currently the script will silently fail or exit if the network drops mid-transfer. A retry loop or rsync flags such as `--partial` would make the deploy more resilient.
  Files to: no tracker found — draft stays in the report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: Move into an ADR; replace the comment with a one-line pointer.

  **Draft ADR** — `docs/adr/0001-static-zone-rate-table.md` *(waiting: `docs/adr/` does not exist)*

  ```markdown
  # Static zone rate table over carrier's rate API

  The shipping cost function uses a static zone rate table rather than calling the
  carrier's rate API. The carrier API took two seconds per call and blocked checkout;
  since rates change only once a year, a static table was chosen for its performance
  benefit.
  ```

  Pointer that replaces the comment: `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
