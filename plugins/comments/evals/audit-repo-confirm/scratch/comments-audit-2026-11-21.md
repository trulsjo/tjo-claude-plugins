# Comments audit — 2026-11-21

10 files read, 15 findings. By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: Delete the comment.

- `shop/src/cart.ts:25` - class 10 (API doc that repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`
  Fix: Delete the doc comment. "Formats cents" mirrors the function name; `@param cents the cents` and `@returns the string` mirror the names and types and add nothing the signature does not already convey.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: Delete both lines. Git retains the history.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control — missing link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: Append a link to the Node.js issue or ICU bug that tracks this DST behaviour in Intl date math. The repo holds no existing URL; find the relevant issue on the Node.js tracker or the ICU bug database and append it. Leave the comment text as-is.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: Delete. History belongs in the commit message, not the source file.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: Replace with `// Rounds weight up to the nearest kilogram and charges the zone rate per kg.`

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > `"""Builds report.\n\n    :param rows: the rows\n    :param path: the path\n    """`
  Fix: Delete the entire docstring. "Builds report" restates the function name; `:param rows: the rows` and `:param path: the path` add nothing beyond the parameter names.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: Delete. Git preserves the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: Delete. The who and when belong in the commit message.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: Delete. The rsync command is self-explanatory.

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming or structure)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: Rename `d` to `discountFraction`, then delete the comment.

```diff
-  // d is the discount as a fraction between 0 and 1
-  const d = discountPct / 100;
   // Round to whole cents: the payment provider rejects fractional amounts.
-  return Math.round(t * (1 - d));
+  const discountFraction = discountPct / 100;
+  // Round to whole cents: the payment provider rejects fractional amounts.
+  return Math.round(t * (1 - discountFraction));
```

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: Refactor `checkout.ts` to apply coupons once, outside the retry loop; then remove the `applied` Set from `coupon.ts`. The refactor spans two files; a ticket is appropriate.

  Draft ticket:
  **Title:** Remove coupon-deduplication workaround in applyCoupon
  **Body:** `applyCoupon` (`shop/src/coupon.ts`) maintains a module-level `applied` Set to prevent double-application caused by `checkout.ts` retrying the payment step and calling `applyCoupon` a second time. Move the coupon-application call in `checkout.ts` to before the retry loop so it runs exactly once. Once that is done, remove the `applied` Set and its guard from `coupon.ts`. Location: `shop/src/coupon.ts:4`.
  Files to: no tracker found — draft stays in report.

- `shop/src/shipping.ts:3` - class 9 (TODO or FIXME with no ticket)
  > `// TODO: support express shipping`
  Fix: File a ticket and replace with `// TODO(#N): support express shipping`.

  Draft ticket:
  **Title:** Add express shipping option to shippingCents
  **Body:** `shippingCents` (`shop/src/shipping.ts`) currently supports only standard zone-based rates. Add an express tier: define express rates per zone in `ZONE_RATES` (or a parallel `ZONE_EXPRESS_RATES` table) and extend the function signature to accept a shipping-speed parameter. Acceptance: `shippingCents` accepts `'standard' | 'express'`; express rates are defined and tested; existing callers default to `'standard'` with no behaviour change. Location: `shop/src/shipping.ts:3`.
  Files to: no tracker found — draft stays in report.

- `scripts/deploy.sh:7` - class 9 (TODO or FIXME with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: File a ticket and replace with `# TODO(#N): retry the upload when the network drops`.

  Draft ticket:
  **Title:** Add retry logic to rsync upload in deploy.sh
  **Body:** The deploy script (`scripts/deploy.sh`) runs rsync with `set -euo pipefail`, so a transient network drop fails the entire deploy with no recovery. Add a retry loop with backoff around the rsync call (e.g. 3 attempts with exponential delay) so a brief network interruption does not require a manual re-deploy. Location: `scripts/deploy.sh:7`.
  Files to: no tracker found — draft stays in report.

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: Move into an ADR and replace with a one-line pointer.

  Draft ADR (`docs/adr/0001-static-zone-table-for-shipping-rates.md`):
  ```markdown
  # Static zone table for shipping rates

  The carrier's rate API added ~2 s of latency per checkout request and was
  blocking the purchase flow. Rates change at most once a year. A static zone
  table in ZONE_RATES was chosen over the live API to eliminate the latency at
  the cost of manual annual updates.
  ```

  Pointer to replace the two comment lines:
  ```typescript
  // Shipping-rate strategy: see docs/adr/0001-static-zone-table-for-shipping-rates.md
  ```
  Files to: `docs/adr/` does not exist — ADR is waiting.

---

Report only: no source files were changed.
No tracker was found, so the 3 ticket drafts stay in the report.
Create docs/adr/ for these ADRs?
