# Comment audit — 2026-11-22

Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: Delete. The `for` loop and accumulator are self-evident.

- `shop/src/cart.ts:24-28` - class 10 (API doc that repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`
  Fix: Delete the block, or rewrite it with what the reader cannot see, e.g. `/** Returns a two-decimal-place string (e.g. 1099 → "10.99"). */`

- `shop/src/cart.ts:30-31` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`  and  `// return euros + "," + (cents % 100);`
  Fix: Delete both lines. Git retains the history.

- `shop/src/dates.ts:8` - class 4 (workaround with no upstream link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: Append a link to the Node.js issue tracker or the ECMA-402 spec section that describes this behaviour. The comment text is correct and must stay; only the citation is missing.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: Delete. This changelog entry belongs in the commit message.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: Delete. The function computes `rate * Math.ceil(weightGrams / 1000)` for all weights; there is no branch for parcels over 20 kg.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > `"""Builds report.\n\n    :param rows: the rows\n    :param path: the path\n    """`
  Fix: Delete the docstring. "Builds report" restates the function name, and both `:param` tags copy the parameter names with no added information. If the contract is worth documenting, rewrite with what the reader cannot see — e.g. what columns are written, what `newline=""` means for the caller, what happens on write errors.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: Delete. Git retains the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: Delete. The who, what, and when belong in the commit message.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: Delete. The `rsync` command on the next line is self-evident.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: Rename `d` to `discountFraction`, then delete the comment.

  ```diff
  -  // d is the discount as a fraction between 0 and 1
  -  const d = discountPct / 100;
  +  const discountFraction = discountPct / 100;
     // Round to whole cents: the payment provider rejects fractional amounts.
  -  return Math.round(t * (1 - d));
  +  return Math.round(t * (1 - discountFraction));
  ```

---

### Ticket

- `shop/src/coupon.ts:4-6` - class 3 (workaround in our own code)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time, so remember applied codes here and skip them on the second call.`
  Fix: Refactor `checkout.ts` so the coupon is applied before the retry loop, or pass the already-discounted total into the retry, so `applyCoupon` is called exactly once per order. The refactor spans at least two files; file a ticket.

  **Draft ticket**
  Title: `Refactor checkout.ts to call applyCoupon exactly once per order`
  Body: `applyCoupon` in `shop/src/coupon.ts` maintains a module-level `applied` Set to guard against being called twice. The root cause is that `checkout.ts` retries its payment step and re-invokes `applyCoupon` on the retry path. This couples coupon state to checkout's retry behaviour and makes the function stateful in a surprising way. Refactor `checkout.ts` so the coupon is applied once before the retry loop, or pass the already-discounted total into the retry path. When the fix lands, remove the `applied` Set and its guard from `coupon.ts`.
  Files to: no tracker found — draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: File a ticket and replace the line with `// TODO(#NNN): support express shipping`, or delete it.

  **Draft ticket**
  Title: `Add express shipping option to shippingCents`
  Body: `shippingCents` in `shop/src/shipping.ts` only supports standard shipping via `ZONE_RATES`. Express shipping is not yet implemented. Add express-rate entries (by zone) and a shipping-method parameter or a separate `expressShippingCents` function so callers can request express delivery. Update callers and tests accordingly.
  Files to: no tracker found — draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: File a ticket and replace the line with `# TODO(#NNN): retry the upload when the network drops`, or delete it.

  **Draft ticket**
  Title: `deploy.sh: retry rsync upload on transient network failure`
  Body: The rsync step in `scripts/deploy.sh` (line 9) runs once with no retry. A transient network drop fails the entire deploy and requires a manual re-run. Add a retry loop with backoff (e.g. up to 3 attempts, 5 s between) around the rsync call so brief network outages are handled automatically.
  Files to: no tracker found — draft stays in the report.

---

### ADR

- `shop/src/shipping.ts:9-10` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: Move into an ADR and replace the two lines with a one-line pointer.

  **Pointer line** (replaces lines 9-10 in `shop/src/shipping.ts`):
  ```typescript
  // Decision: docs/adr/0001-static-zone-rate-table.md
  ```

  **Draft ADR** (`docs/adr/0001-static-zone-rate-table.md`) — waiting (folder does not exist):
  ```markdown
  # Static zone rate table for shipping

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```

---

Report only: no source files were changed.
