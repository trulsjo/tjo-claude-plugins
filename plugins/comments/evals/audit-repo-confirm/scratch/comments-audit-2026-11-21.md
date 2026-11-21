# Comments audit — 2026-11-21

Whole repo, 10 files read, 15 findings. By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: Delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`
  Fix: Delete the entire doc block; "Formats cents", "the cents", and "the string" add nothing beyond the function name and types.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: Delete both lines; git keeps the history.

- `shop/src/dates.ts:8` - class 4 (workaround with no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: Append a link to the Node.js issue or the relevant V8/ICU bug tracker entry. The comment text stays as-is.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: Delete; this belongs in the commit message or changelog.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: Delete or rewrite to match the code. The function applies a per-kg rate (`rate * Math.ceil(weightGrams / 1000)`) to all parcels with no 20 kg threshold; the description is false.

- `tools/report.py:5` - class 10 (API doc repeats the signature)
  > `"""Builds report. :param rows: the rows :param path: the path """`
  Fix: Delete the entire docstring; "Builds report", "the rows", and "the path" add nothing beyond the function name and parameter names.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: Delete; git keeps the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: Delete; records a past change with author and date, which belongs in the commit log.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: Delete; the rsync command on the next line makes this self-evident.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
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

---

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: Refactor `checkout.ts` to not call `applyCoupon` twice (make the call site idempotent); the deduplication set and this comment become unnecessary. Filed as a ticket because the fix is in `checkout.ts`, a file not in this batch.

  **Draft ticket**
  Title: `Refactor checkout retry to not call applyCoupon twice`
  Body: `applyCoupon in shop/src/coupon.ts carries a module-level deduplication Set to guard against checkout.ts calling it on retry. The root cause is in checkout.ts. Refactoring the retry path to call applyCoupon at most once makes the guard and its comment unnecessary. Location: shop/src/coupon.ts:4–6.`
  Files to: no tracker found (repo has no git remote).

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: File a ticket for express shipping support and replace with `TODO(#<ticket>): support express shipping`.

  **Draft ticket**
  Title: `Add express shipping support`
  Body: `shop/src/shipping.ts has an untracked TODO at line 3 to add express shipping. No ticket exists for this work. File one and link it from the TODO. Location: shop/src/shipping.ts:3.`
  Files to: no tracker found (repo has no git remote).

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: File a ticket for upload retry logic and replace with `TODO(#<ticket>): retry the upload when the network drops`.

  **Draft ticket**
  Title: `Add network-drop retry to deploy upload`
  Body: `scripts/deploy.sh has an untracked TODO at line 7 to retry the rsync upload when the network drops. No ticket exists for this work. File one and link it from the TODO. Location: scripts/deploy.sh:7.`
  Files to: no tracker found (repo has no git remote).

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: Move into an ADR and replace with a one-line pointer.

  **Draft ADR** — `docs/adr/0001-static-zone-table.md` (waiting: folder does not exist)
  ```markdown
  # Static zone table instead of carrier rate API

  We use a static zone table for shipping rates rather than calling the carrier's rate API. The API took two seconds per call and blocked checkout; shipping rates change at most once a year, so a static table is sufficient.
  ```

  Pointer that replaces the comment:
  ```
  // Decision: docs/adr/0001-static-zone-table.md
  ```

---

Report only: no source files were changed.
Reply "yes" to apply the 10 trivial fixes, or name the ones to apply.
No tracker was found, so the 3 ticket drafts stay in the report.
1 ADR would be written to `docs/adr/0001-static-zone-table.md`; its draft is above. Reply "yes to the ADR" to create it (a yes to the trivial fixes does not cover it).
Create `docs/adr/` for these ADRs?
