# Comment audit — 2026-11-24

Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: delete the comment.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control — no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: append a link to the Node.js issue tracker or the relevant V8/ECMA-402 spec section documenting this Intl DST-skipping behaviour. The repo holds no such URL, so the link should point to the Node.js GitHub issues or Chromium bug tracker entry that records the DST gap.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: delete the comment. The function returns `rate * Math.ceil(weightGrams / 1000)` for all weights — there is no flat rate and no 20 kg threshold.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: delete both lines; git keeps them.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: delete the comment; history lives in commit messages.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > `/**`
  > ` * Formats cents.`
  > ` * @param cents the cents`
  > ` * @returns the string`
  > ` */`
  Fix: delete the entire doc comment. "Formats cents." adds nothing to `formatCents`; `@param cents the cents` adds nothing to `cents: number`; `@returns the string` adds nothing to `: string`.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: delete the comment.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: delete the comment.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: delete the comment.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > `"""Builds report.`
  > ` `
  > `    :param rows: the rows`
  > `    :param path: the path`
  > `    """`
  Fix: delete the docstring. "Builds report." restates `build_report`; `:param rows: the rows` and `:param path: the path` each restate the parameter name and add nothing.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
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

---

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`
  Fix: refactor `checkout.ts` to stop calling `applyCoupon` more than once per checkout, then remove the deduplication guard from `coupon.ts`. The cause lives in `checkout.ts` (outside the files in scope), so this is a ticket.

  **Draft ticket**
  Title: `Fix checkout.ts to not call applyCoupon twice, then remove deduplication workaround in coupon.ts`
  Body: `checkout.ts` retries the payment step and, as a side effect, calls `applyCoupon` a second time per checkout. As a workaround, `shop/src/coupon.ts` tracks every applied coupon code in a module-level `Set` and silently skips the second call. This hides the double-call bug in `checkout.ts` and means the `Set` is never cleared between runs in test environments, making isolated test cases unreliable. Step 1: fix `checkout.ts` so it does not call `applyCoupon` more than once per checkout flow. Step 2: remove the `applied` Set and the early-return guard from `coupon.ts` (lines 1 and 4–6).
  Files to: No tracker was found, so this draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: file a ticket and replace the comment with `TODO(#N): support express shipping`, or delete the comment.

  **Draft ticket**
  Title: `Support express shipping in shippingCents`
  Body: `shop/src/shipping.ts` has an untracked TODO (line 3) to add express shipping support. The current `shippingCents` implementation covers only standard zone-based rates. Express shipping options, their pricing, and any required zone entries need to be designed and implemented. Once a ticket is filed, the comment should be updated to `TODO(#N): support express shipping`.
  Files to: No tracker was found, so this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO or FIXME with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: file a ticket and replace the comment with `TODO(#N): retry the upload when the network drops`, or delete the comment.

  **Draft ticket**
  Title: `Add retry logic for network failures during rsync upload in deploy script`
  Body: The deploy script copies the build output to the server with a single rsync call (`scripts/deploy.sh:9`) but has no retry logic. A transient network drop during the transfer will leave the deployment failed with no automatic recovery, potentially leaving the server in a partial state. The work is to add a retry loop with backoff around the rsync command in `scripts/deploy.sh`.
  Files to: No tracker was found, so this draft stays in the report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: move into an ADR and replace with a one-line pointer.

  **Draft ADR** — `docs/adr/0001-static-zone-rate-table.md` (waiting: `docs/adr/` does not exist)

  ```md
  # Static zone table over the carrier rate API

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```

  Pointer that replaces the comment: `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
