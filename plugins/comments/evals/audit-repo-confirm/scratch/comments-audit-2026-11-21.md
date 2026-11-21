Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 2, ticket 2, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: Delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > // * Formats cents.
  > // * @param cents the cents
  > // * @returns the string
  Fix: Delete `@param cents the cents` and `@returns the string`. Rewrite the summary to say what the reader cannot see, e.g. `Returns the cents value as a decimal string with two decimal places (e.g. 199 → "1.99").`

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  Fix: Delete both lines; git keeps the history.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control — no link)
  > // Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.
  Fix: Append a link to the upstream Node.js or V8 issue tracking this DST behaviour. The comment text is otherwise correct and stays.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > // Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.
  Fix: Delete; this belongs in git commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > // Returns the flat rate for parcels over 20 kg.
  Fix: Delete or replace with an accurate description: the function multiplies the zone rate by ceiling-kg for all weights; there is no 20 kg threshold and no flat rate.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > """Builds report.
  >
  >     :param rows: the rows
  >     :param path: the path
  >     """
  Fix: Delete the entire docstring. Rewrite if future readers need to know what columns are written or what happens on write failure.

- `tools/report.py:12` - class 7 (commented-out code)
  > # print(rows)
  Fix: Delete it; git retains the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > # Timeout raised from 30 to 60 seconds by Kim in March.
  Fix: Delete; who/when/what-changed belongs in the commit message.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > # copy the build output to the server with rsync
  Fix: Delete; the rsync command makes this self-evident.

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming or structure)
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

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > // checkout.ts retries the payment step and calls applyCoupon a second time,
  > // so remember applied codes here and skip them on the second call.
  Fix: Refactor `checkout.ts` to apply coupons exactly once — either move the deduplication guard to the checkout layer or redesign the retry to separate the discount step from the payment retry. Once the cause is removed, delete the comment and the module-level `applied` set.

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

### Ticket

- `shop/src/shipping.ts:3` - class 9 (TODO or FIXME with no ticket)
  > // TODO: support express shipping
  Fix: File a ticket and replace with `// TODO(#NNN): support express shipping`, or delete the TODO if the work is not being tracked.

  Files to: no tracker was found, so this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO or FIXME with no ticket)
  > # TODO: retry the upload when the network drops
  Fix: File a ticket and replace with `# TODO(#NNN): retry the upload when the network drops`, or delete the TODO if the work is not being tracked.

  Files to: no tracker was found, so this draft stays in the report.

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > // We chose a static zone table over the carrier's rate API because the API
  > // took two seconds per call and blocked checkout, and rates change once a year.
  Fix: Move the rationale into `docs/adr/0001-static-zone-rates.md` and replace the two-line comment with: `// Decision: docs/adr/0001-static-zone-rates.md`

  Draft ADR — `docs/adr/0001-static-zone-rates.md` (waiting: docs/adr/ does not exist):

  ```md
  # Static zone table instead of carrier rate API

  The shipping cost is calculated from a static zone table rather than calling the
  carrier's rate API. The API took two seconds per call and blocked checkout, and
  shipping rates change only once a year, making a static table both faster and
  sufficiently accurate.

  ## Considered Options

  - Carrier rate API: real-time rates, but 2 s per call blocked checkout and added
    an operational dependency.
  - Static zone table (chosen): sub-millisecond lookup, updated manually once a year
    when rates change.
  ```

  Pointer that replaces the comment: `// Decision: docs/adr/0001-static-zone-rates.md`

---

Report only: no source files were changed.
No tracker was found, so the 2 ticket drafts stay in the report.
1 ADR would be written to docs/adr/0001-static-zone-rates.md once confirmed; its draft is above.
Create docs/adr/ for these ADRs?
