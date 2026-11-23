Whole repo, 10 files read, 15 findings — trivial: 10, local refactor: 1, ticket: 3, ADR: 1
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2

### Trivial

- `shop/src/cart.ts:12` — class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: delete the comment.

- `shop/src/cart.ts:24` — class 10 (API doc repeats the signature)
  > `/**`
  > ` * Formats cents.`
  > ` * @param cents the cents`
  > ` * @returns the string`
  > ` */`
  Fix: delete the doc comment. "Formats cents" restates the function name; both tags add nothing to the names and types.

- `shop/src/cart.ts:30` — class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: delete both lines; git keeps the history.

- `shop/src/dates.ts:8` — class 4 (upstream workaround, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: append a link to the Node.js or V8 issue tracking this DST-skipping behavior in Intl date arithmetic (the link should point to the relevant issue on nodejs/node or the V8 bug tracker).

- `shop/src/shipping.ts:1` — class 8 (history/changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: delete the comment; version history belongs in commit messages.

- `shop/src/shipping.ts:4` — class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: delete the comment. The function applies `rate * ceil(weightGrams / 1000)` for all weights; there is no 20 kg threshold and no flat rate.

- `tools/report.py:5` — class 10 (API doc repeats the signature)
  > `"""Builds report.`
  > `    `
  > `    :param rows: the rows`
  > `    :param path: the path`
  > `    """`
  Fix: delete the docstring. "Builds report" restates `build_report`; both `:param` tags add nothing to the parameter names.

- `tools/report.py:12` — class 7 (commented-out code)
  > `# print(rows)`
  Fix: delete the line; git keeps the history.

- `config/app.yaml:3` — class 8 (history/changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: delete the comment; history belongs in commit messages.

- `scripts/deploy.sh:8` — class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: delete the comment.

### Local refactor

- `shop/src/cart.ts:18` — class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: rename `d` to `discountFraction`, then delete the comment.

  ```diff
  -  // d is the discount as a fraction between 0 and 1
  -  const d = discountPct / 100;
  +  const discountFraction = discountPct / 100;
     // Round to whole cents: the payment provider rejects fractional amounts.
  -  return Math.round(t * (1 - d));
  +  return Math.round(t * (1 - discountFraction));
  ```

### Ticket

- `shop/src/coupon.ts:4` — class 3 (workaround in our own code; cause is in `checkout.ts`, outside the files in scope)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: remove the double-call in `checkout.ts` first; then delete the guard. Ticket because the cause lies outside these files.

  **Title:** Remove double-application guard from `applyCoupon`

  **Body:** `applyCoupon` in `shop/src/coupon.ts` holds a module-level `applied` Set that silently ignores a coupon code the second time it appears. The guard exists because `checkout.ts` retries the payment step and calls `applyCoupon` a second time per checkout (lines 4–6, `shop/src/coupon.ts`). The guard is a symptom, not a fix: the Set accumulates codes for the lifetime of the module and will wrongly suppress a legitimate coupon on a later, independent checkout in a long-lived process. The correct fix is to call `applyCoupon` at most once per checkout. Step 1: remove the extra `applyCoupon` call from the payment-retry path in `checkout.ts`. Step 2: once that is done, delete the `applied` Set (line 1) and the guard block (lines 5–6) in `shop/src/coupon.ts`.

  Files to: no tracker was found, so this draft stays in the report.

- `shop/src/shipping.ts:3` — class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: file a ticket and link it from the TODO (`TODO(#N): support express shipping`), or delete the TODO.

  **Title:** Support express shipping in `shippingCents`

  **Body:** `shippingCents` in `shop/src/shipping.ts` (line 3) carries an untracked TODO to support express shipping. The current implementation selects a zone rate from a static table and multiplies by weight in whole kilograms; express shipping would require at minimum a second rate tier per zone and a service-level parameter on `shippingCents`. Without a ticket this work is unscheduled and invisible to planning.

  Files to: no tracker was found, so this draft stays in the report.

- `scripts/deploy.sh:7` — class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: file a ticket and link it from the TODO (`TODO(#N): retry the upload when the network drops`), or delete the TODO.

  **Title:** Add retry logic for rsync upload on network failure

  **Body:** The deploy script (`scripts/deploy.sh:7`) has no retry handling for transient network failures during the rsync upload step. A dropped connection causes the deploy to fail immediately, requiring a manual re-run. This work was noted inline but has never been tracked.

  Files to: no tracker was found, so this draft stays in the report.

### ADR

- `shop/src/shipping.ts:9` — class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: move into an ADR and replace with a one-line pointer.

  Draft ADR — `docs/adr/0001-static-zone-rate-table.md` (**waiting**: `docs/adr/` does not exist):

  ```md
  # Use a static zone rate table instead of the carrier's rate API

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```

  Pointer that replaces the two comment lines:
  `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
