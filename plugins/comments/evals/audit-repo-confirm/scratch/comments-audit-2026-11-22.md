Whole repo, 10 files read, 15 findings: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: Delete. The loop body is self-evident.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > `/** * Formats cents. * @param cents the cents * @returns the string */`
  Fix: Delete the entire doc block. "Formats cents." mirrors the function name; both tags restate the parameter name and return type with no added information.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: Delete both lines; git keeps the history.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: Delete. This belongs in the commit message or git log.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: Delete. The function applies a per-kg rate to all weights with no 20 kg threshold; the comment describes neither what the code does nor a special case that exists.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: Append a link to the upstream Node.js / V8 issue tracking this `Intl` DST behaviour (the link should point to the relevant issue in `nodejs/node` on GitHub or the V8 bug tracker). Leave the comment text as-is.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > `"""Builds report.\n\n:param rows: the rows\n:param path: the path\n"""`
  Fix: Delete the docstring. "Builds report." echoes `build_report`; both `:param` lines copy the parameter names with no added information.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: Delete; git keeps it.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: Delete. Records what changed, when, and by whom — belongs in the commit message.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: Delete. The rsync command itself states what it does; the comment adds nothing.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: Rename `d` to `discountFraction` and delete the comment.

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

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: The root cause is in `checkout.ts`. File a ticket to scope the payment retry so it does not re-call `applyCoupon`, then remove the `applied` Set and the guard in `coupon.ts`.

  Draft ticket —
  **Title:** Fix `checkout.ts` payment retry to not re-apply coupons
  **Body:** `coupon.ts` maintains a module-level `applied` Set because `checkout.ts` calls `applyCoupon` a second time when it retries the payment step. This workaround is stateful across requests (the Set is never reset) and hides a scoping problem in the retry logic. The fix is to restructure the payment retry in `checkout.ts` so only the payment call is retried, not the coupon step. Once that is done, `applyCoupon` can be made stateless and the guard removed. Location: `shop/src/coupon.ts:4`.
  Files to: no tracker was found; draft stays in this report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: File a ticket and replace the comment with a ticketed reference.

  Draft ticket —
  **Title:** Add express shipping option to `shippingCents`
  **Body:** `shippingCents` in `shop/src/shipping.ts` only supports standard zone-based rates. Express shipping is not implemented. Decide on the interface (a new zone key, a separate rate table, or an `express: boolean` parameter), add the rate entries, and wire the option into the checkout flow. Location: `shop/src/shipping.ts:3`.
  Files to: no tracker was found; draft stays in this report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: File a ticket and replace the comment with a ticketed reference.

  Draft ticket —
  **Title:** Add retry logic to deploy rsync upload on network failure
  **Body:** The rsync upload in `scripts/deploy.sh` has no retry mechanism. A transient network drop fails the entire deploy. Implement retry logic (e.g. exponential backoff with a configurable attempt count) around the rsync call so deploys survive brief connectivity interruptions. Location: `scripts/deploy.sh:7`.
  Files to: no tracker was found; draft stays in this report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: Move into an ADR and replace with a one-line pointer.

  Draft ADR (`docs/adr/0001-static-zone-rate-table.md`, status: **waiting** — `docs/adr/` does not exist) —

  ```markdown
  # Static zone rate table for shipping costs

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.

  ## Considered Options

  - Carrier's rate API: returns current prices at request time; rejected because it took two seconds per call and blocked checkout.
  - Static zone table (chosen): maintained in-repo; rates updated manually, which is acceptable because they change once a year.
  ```

  Pointer line (replaces lines 9–10 in `shop/src/shipping.ts`):
  `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
Reply "yes" to apply the 10 trivial fixes, or name the ones to apply.
No tracker was found, so the 3 ticket drafts stay in the report.
1 ADR would be written once the folder exists. Its draft is above.
Create docs/adr/ for these ADRs?
