# Comment audit — 2026-11-20

Scope: whole repo — 10 files read, 15 findings (trivial: 10, local refactor: 2, ticket: 2, ADR: 1)

---

### Trivial

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: Add a link to the upstream Node.js issue or spec section so the workaround can be verified and revisited, e.g. `// Node's Intl date math skips DST changes in some time zones — see https://github.com/nodejs/node/issues/<id> — so count in UTC milliseconds.`

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: Delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`
  Fix: Rewrite with what the reader cannot see from the signature, e.g. `/** Formats a cent amount as a decimal string with two fractional digits (e.g. 1099 → "10.99"). */`

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: Delete both lines. Git history preserves the previous implementation.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: Delete the comment. This belongs in commit messages or release notes.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: The code multiplies the zone rate by `Math.ceil(weightGrams / 1000)` for all weights — there is no 20 kg threshold and the rate is not flat. Delete or replace with: `// Rate is per kg (rounded up), applied to all parcel weights.`

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: Delete. The rsync command and its arguments make this self-evident.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > `"""Builds report.\n\n    :param rows: the rows\n    :param path: the path\n    """`
  Fix: Rewrite with what the reader cannot see, e.g.:
  ```python
  """Write rows to a CSV file at path.

  Each row must contain 'sku', 'qty', and 'total_cents' keys.
  Overwrites the file if it already exists.
  """
  ```

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: Delete. Git history preserves it.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: Delete. The change, its author, and the date belong in the commit message.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: Rename `d` to `discountFraction` and delete the comment.

  ```diff
  -  // d is the discount as a fraction between 0 and 1
  -  const d = discountPct / 100;
     // Round to whole cents: the payment provider rejects fractional amounts.
  -  return Math.round(t * (1 - d));
  +  const discountFraction = discountPct / 100;
  +  // Round to whole cents: the payment provider rejects fractional amounts.
  +  return Math.round(t * (1 - discountFraction));
  ```

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: Fix `checkout.ts` so it does not call `applyCoupon` more than once per checkout session, then remove the `applied` set and the deduplication guard. If the checkout refactor is large, file a ticket and reference it in the interim.

  ```diff
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

---

### Ticket

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: File a ticket and replace with a ticketed TODO, or delete.

  **Draft ticket**
  Title: `Add express shipping option to shippingCents`
  Body: The `shippingCents` function in `shop/src/shipping.ts` only calculates standard shipping via the zone table. Add support for an express tier with its own rate table or multiplier.
  Files to: no tracker found — stays as draft.
  Pointer: `// TODO(#<issue>): support express shipping`

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: File a ticket for the retry logic and link it from the TODO.

  **Draft ticket**
  Title: `Add network-drop retry to deploy rsync upload`
  Body: The deploy script (`scripts/deploy.sh` line 9) runs rsync once with no retry. When the network drops mid-transfer the deploy silently fails. Add retry logic (e.g. a loop with backoff, or `--partial --append-verify`) so a transient outage does not require a manual re-run.
  Files to: no tracker found — stays as draft.
  Pointer: `# TODO(#<issue>): retry the upload when the network drops`

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: Move rationale to an ADR and leave a one-line pointer comment.

  **Draft ADR** — `docs/adr/0001-static-zone-rate-table.md` (waiting: folder does not exist)

  ```markdown
  # Use a static zone rate table instead of the carrier rate API

  Shipping costs are calculated at checkout. The carrier provides a live rate API,
  but it added ~2 s per call and blocked the checkout flow. Because rates change
  approximately once a year, a static zone table maintained in source code was chosen.

  ## Considered Options

  - **Live carrier API** — exact rates, but ~2 s latency blocks checkout.
  - **Static zone table** — approximate rates, zero latency, manual update once a year.
  ```

  Pointer (replace lines 9-10 of `shipping.ts`):
  `// See docs/adr/0001-static-zone-rate-table.md for why we use a table over the carrier API.`

---

Report only: no source files were changed.
Reply "yes" to apply the 10 trivial fixes, or name the ones to apply.

No tracker was found (no tracker doc and no GitHub remote detected), so the 2 ticket drafts stay in this report. Reply "file the tickets" once you have pointed me at a tracker.
Create docs/adr/ for these ADRs?
