# Comment audit — 2026-11-22

Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: Delete. The for loop is self-evident.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`
  Fix: Delete the entire doc block, or rewrite to state what the reader cannot infer (output format, currency symbol, locale assumed).

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: Delete both lines; git keeps the history.

- `shop/src/dates.ts:8` - class 4 (upstream workaround with no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: Append a link to the Node.js issue or V8/ICU tracker entry that tracks this behaviour; leave the comment text as-is.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: Delete; this belongs in the commit message or CHANGELOG.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: The code multiplies `rate * Math.ceil(weightGrams / 1000)` for every weight with no 20 kg threshold; delete this comment or replace with an accurate description of the per-kg ceiling calculation.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: Delete. The `rsync` command and its destination make the action plain.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: Delete; history belongs in commit messages.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: Delete; git keeps it.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > `"""Builds report.\n\n    :param rows: the rows\n    :param path: the path\n    """`
  Fix: Delete the noise, or rewrite with what the reader cannot infer — e.g., the expected shape of each row dict, the output file format (CSV), and what happens if `path` is not writable.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: Rename `d` to `discountFraction` (or `discountRatio`), then delete the comment.

  ```diff
  -  const d = coupon.value;              // d is the discount as a fraction between 0 and 1
  -  total = total * (1 - d);
  +  const discountFraction = coupon.value;
  +  total = total * (1 - discountFraction);
  ```

---

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code — cause outside audited files)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: File a ticket to fix the double-invocation in `checkout.ts`. The module-level `applied` Set is a side-effectful workaround that also leaks state across tests. Link the ticket from this comment until the root cause is resolved.

  **Draft ticket**
  Title: `Fix double-invocation of applyCoupon in checkout retry path`
  Body: `checkout.ts retries the payment step and calls applyCoupon a second time, causing duplicate coupon logic. coupon.ts works around this with a module-level Set of applied codes (coupon.ts:4–7), which is a side-effectful patch that leaks state across tests. The fix should be in checkout.ts (the retry logic) so the workaround in coupon.ts can be removed. Location: shop/src/coupon.ts lines 4–7.`
  Files to: no tracker found — draft stays in report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: File a ticket for express shipping support and replace with `// TODO(#<ticket>): support express shipping`, or delete if the work is not planned.

  **Draft ticket**
  Title: `Add express shipping support`
  Body: `A TODO comment in shop/src/shipping.ts:3 notes that express shipping is not yet supported. The current implementation returns only standard flat rates from the zone table. File this ticket to track the express shipping feature, then link it back to the TODO.`
  Files to: no tracker found — draft stays in report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: File a ticket for the retry logic and reference its ID in the comment, or delete the TODO.

  **Draft ticket**
  Title: `Add retry logic to deploy upload step`
  Body: `A TODO comment in scripts/deploy.sh:7 notes that the rsync upload has no retry on network failure. A transient drop will fail the deploy silently. File this ticket to track the retry work, then link it back to the TODO.`
  Files to: no tracker found — draft stays in report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: Move the rationale into an ADR and replace these two lines with a one-line pointer.

  **Draft ADR** — `docs/adr/0001-static-zone-rate-table.md` (waiting: `docs/adr/` does not exist)
  ```markdown
  # Use a static zone table for shipping rates

  The carrier's rate API added two seconds of latency per checkout call and blocked the checkout flow.
  Shipping rates change at most once a year, making a static lookup table a practical alternative.
  We chose the static table to eliminate that latency at the cost of a manual update when rates change.
  ```
  Pointer that replaces the two comment lines:
  `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
No tracker was found, so the 3 ticket drafts stay in the report.
1 ADR would be written to `docs/adr/0001-static-zone-rate-table.md` once the folder exists; its draft is in this report.
Create docs/adr/ for these ADRs?
