Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: Delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > /** Formats cents. @param cents the cents @returns the string */
  Fix: Delete the doc block, or replace it with what the reader cannot see from the signature — e.g. the returned format (two decimal places, no currency symbol).

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  Fix: Delete both lines; git keeps the history.

- `shop/src/dates.ts:8` - class 4 (workaround with no link)
  > // Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.
  Fix: Append a link to the upstream Node.js / V8 / ICU issue tracking this behaviour (e.g. a github.com/nodejs/node/issues/NNN or ICU bug URL). Leave the comment text as-is.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > // Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.
  Fix: Delete; history belongs in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > // Returns the flat rate for parcels over 20 kg.
  Fix: Replace with an accurate description, e.g. `// Per-kg rate, rounded up to the next whole kilogram.`

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > """Builds report.
  >
  >     :param rows: the rows
  >     :param path: the path
  >     """
  Fix: Delete the `:param rows:` and `:param path:` tags — they restate the parameter names and add nothing. Rewrite the summary to say what the function delivers, e.g. `"""Write rows as CSV to path, one row per line with fields sku, qty, total_cents."""`

- `tools/report.py:12` - class 7 (commented-out code)
  > # print(rows)
  Fix: Delete it; git history preserves it.

- `config/app.yaml:3` - class 8 (history or changelog)
  > # Timeout raised from 30 to 60 seconds by Kim in March.
  Fix: Delete; this belongs in the commit message.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > # copy the build output to the server with rsync
  Fix: Delete; the rsync command makes this self-evident.

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > // d is the discount as a fraction between 0 and 1
  Fix: Rename `d` to `discountFraction`, then delete the comment.

  ```diff
  -  // d is the discount as a fraction between 0 and 1
  -  const d = discountPct / 100;
  +  const discountFraction = discountPct / 100;
     // Round to whole cents: the payment provider rejects fractional amounts.
  -  return Math.round(t * (1 - d));
  +  return Math.round(t * (1 - discountFraction));
  ```

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > // checkout.ts retries the payment step and calls applyCoupon a second time,
  > // so remember applied codes here and skip them on the second call.
  Fix: Fix checkout.ts to call applyCoupon exactly once per checkout, then remove the `applied` Set and the guard from coupon.ts. checkout.ts is not in this repo's file list; removing the workaround while checkout.ts still double-calls would reintroduce the bug, so a ticket is required first. Its draft names checkout.ts as the work to do first, and the workaround's removal as the step after.

  **Draft ticket**
  Title: Fix checkout.ts to not call applyCoupon twice per checkout
  Body: `shop/src/coupon.ts` holds a module-level `applied` Set to guard against `checkout.ts` calling `applyCoupon` a second time during payment retries (see coupon.ts lines 1–6). This is a workaround for a double-call in checkout.ts. First, fix checkout.ts to call `applyCoupon` exactly once per checkout flow. Then remove the `applied` Set and the early-return guard from coupon.ts.
  Files to: no tracker found — draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > // TODO: support express shipping
  Fix: File a ticket and replace with `// TODO(#NNN): support express shipping`.

  **Draft ticket**
  Title: Support express shipping in shippingCents
  Body: `shop/src/shipping.ts` — `shippingCents()` currently supports only standard zone rates. Add an express-shipping option (e.g. a rate multiplier or separate zone entries) so callers can request expedited delivery.
  Files to: no tracker found — draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > # TODO: retry the upload when the network drops
  Fix: File a ticket and replace with `# TODO(#NNN): retry the upload when the network drops`.

  **Draft ticket**
  Title: Add retry logic to rsync upload in deploy.sh when network drops
  Body: The rsync step in `scripts/deploy.sh` has no retry on transient network failures. When the connection drops mid-upload, the deploy fails with no recovery. Add retry logic (e.g. a loop with backoff) so a temporary network blip does not require a manual re-run.
  Files to: no tracker found — draft stays in the report.

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > // We chose a static zone table over the carrier's rate API because the API
  > // took two seconds per call and blocked checkout, and rates change once a year.
  Fix: Move into an ADR and leave a one-line pointer.

  **Draft ADR** (`docs/adr/0001-shipping-zone-table.md`, status: waiting — docs/adr/ does not exist):

  ```markdown
  # Static zone table for shipping rates

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.

  ## Considered Options

  - Static ZONE_RATES table in source (chosen): eliminates the blocking network call; rates updated manually, acceptable given once-a-year cadence.
  - Carrier rate API: real-time accuracy, but adds two seconds of latency to every checkout request.
  ```

  Pointer to replace the two-line comment:
  ```typescript
  // Rates are static by design — see docs/adr/0001-shipping-zone-table.md.
  ```

---

Report only: no source files were changed. Reply "yes" to apply the 10 trivial fixes, or name the ones to apply.
No tracker was found, so the 3 ticket drafts stay in the report.
1 ADR would be written to docs/adr/0001-shipping-zone-table.md; a yes to the ADRs creates it.
Create docs/adr/ for these ADRs?
