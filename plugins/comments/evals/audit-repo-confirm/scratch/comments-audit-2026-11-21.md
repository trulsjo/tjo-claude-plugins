# Comment audit — 2026-11-21

Scope: whole repo, 10 files read, 15 findings (trivial 10, local refactor 2, ticket 2, ADR 1)

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: Delete the comment.

- `shop/src/cart.ts:24-28` - class 10 (API doc that repeats the signature)
  > /** Formats cents. @param cents the cents @returns the string */
  Fix: Delete the `@param` and `@returns` lines; rewrite the summary to say what the reader cannot see, e.g. "Returns cents as a decimal string with two fractional digits (199 → "1.99").".

- `shop/src/cart.ts:30-31` - class 7 (commented-out code)
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  Fix: Delete both lines; git keeps the history.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control)
  > // Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.
  Fix: Append a link to the upstream Node.js / V8 issue or the relevant spec section so the workaround is traceable (e.g. the Node.js GitHub issue tracking this or the ECMA-262 reference for `Date.prototype.getTime`).

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > // Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.
  Fix: Delete; this belongs in the commit message, not the source file.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > // Returns the flat rate for parcels over 20 kg.
  Fix: The code calculates a per-kg rate and has no 20 kg threshold. Delete or rewrite with an accurate description of the calculation, and move an accurate summary into a JSDoc for `shippingCents`.

- `config/app.yaml:3` - class 8 (history or changelog)
  > # Timeout raised from 30 to 60 seconds by Kim in March.
  Fix: Delete; who changed it and when is in the commit history.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > # copy the build output to the server with rsync
  Fix: Delete; the rsync command on the next line makes this self-evident.

- `tools/report.py:5-9` - class 10 (API doc that repeats the signature)
  > """Builds report.
  >
  >     :param rows: the rows
  >     :param path: the path
  >     """
  Fix: Delete the `:param` lines or rewrite the whole docstring to say what the reader cannot see — e.g. what columns are written, the output format (CSV / JSON), file-creation behaviour, and any error conditions.

- `tools/report.py:12` - class 7 (commented-out code)
  > # print(rows)
  Fix: Delete; git keeps it.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming or structure)
  > // d is the discount as a fraction between 0 and 1
  Fix: Rename `d` to `discountFraction`, then delete the comment.

  ```diff
  -  // d is the discount as a fraction between 0 and 1
  -  const d = coupon.discountRate;
  +  const discountFraction = coupon.discountRate;
  -  total = total * (1 - d);
  +  total = total * (1 - discountFraction);
  ```

- `shop/src/coupon.ts:4-6` - class 3 (workaround in our own code)
  > // checkout.ts retries the payment step and calls applyCoupon a second time, so remember applied codes here and skip them on the second call.
  Fix: Refactor checkout.ts so it does not call `applyCoupon` more than once per checkout, then remove the module-level `applied` set and this comment. File a ticket if the refactor is large.

  ```diff
  -// checkout.ts retries the payment step and calls applyCoupon a second time,
  -// so remember applied codes here and skip them on the second call.
  -const applied = new Set<string>();
   export function applyCoupon(code: string): void {
  -  if (applied.has(code)) return;
  -  applied.add(code);
     // apply the coupon …
   }
  ```
  (Remove the guard after fixing checkout.ts to not call applyCoupon twice.)

---

### Ticket

- `shop/src/shipping.ts:3` - class 9 (TODO or FIXME with no ticket)
  > // TODO: support express shipping
  Fix: File a ticket for express-shipping support and replace with `// TODO(#<ticket>): support express shipping`, or delete if no longer planned.

  Draft — **Title**: Support express shipping
  **Body**: `shop/src/shipping.ts:3` contains `// TODO: support express shipping` with no associated ticket. Evaluate whether this is still planned; if so, file a ticket to track it. If not, delete the TODO.
  **Files to**: no tracker found (repo is not under a GitHub remote).

- `scripts/deploy.sh:7` - class 9 (TODO or FIXME with no ticket)
  > # TODO: retry the upload when the network drops
  Fix: File a ticket for upload retry logic and replace with `# TODO(#<ticket>): retry the upload when the network drops`, or delete if no longer planned.

  Draft — **Title**: Add upload retry on network failure in deploy script
  **Body**: `scripts/deploy.sh:7` contains `# TODO: retry the upload when the network drops` with no associated ticket. Evaluate whether this is still planned; if so, file a ticket to track it. If not, delete the TODO.
  **Files to**: no tracker found (repo is not under a GitHub remote).

---

### ADR

- `shop/src/shipping.ts:9-10` - class 5 (records a decision)
  > // We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  Fix: Move into an ADR and replace with a one-line pointer.

  Draft ADR — **Path**: `docs/adr/0001-static-zone-table.md` (**waiting**: `docs/adr/` does not exist)

  ```md
  # Use a static zone table for shipping rates

  Shipping rates are looked up from a static zone table rather than the carrier's
  rate API. The carrier API added two seconds of latency per checkout call and
  blocked the checkout flow; rates change approximately once a year, so the table
  is refreshed on each rate change with negligible overhead.

  ## Considered Options

  - Carrier rate API — rejected: 2 s per call, synchronous, blocked checkout.
  - Static zone table — chosen.
  ```

  Pointer replacing the comment: `// Decision: docs/adr/0001-static-zone-table.md`

---

Report only: no files were changed.
