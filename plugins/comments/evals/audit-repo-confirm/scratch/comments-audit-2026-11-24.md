# Comment audit — 2026-11-24

Whole repo, 10 files read, 15 findings: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > ```
  > /**
  >  * Formats cents.
  >  * @param cents the cents
  >  * @returns the string
  >  */
  > ```
  Fix: delete the docstring. "Formats cents" restates `formatCents`; `@param cents the cents` and `@returns the string` add nothing beyond the names and the return type.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > ```
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  > ```
  Fix: delete; git keeps it.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: append a link to the Node.js or V8 issue tracking this DST behaviour; the comment's text stays as it is. The link should point to the relevant Node.js issue tracker entry or V8 bug report for this DST-skipping behaviour in `Intl` date math.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: delete; history lives in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: delete the comment. The function has no 20 kg threshold; it applies `rate * Math.ceil(weightGrams / 1000)` for any weight.

- `tools/report.py:5` - class 10 (API doc repeats the signature)
  > ```
  > """Builds report.
  > :param rows: the rows
  > :param path: the path
  > """
  > ```
  Fix: delete the docstring. The summary restates the function name, and each `:param` tag restates only its parameter name.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: delete the comment; git keeps the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: delete the comment; history belongs in commit messages.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: delete the comment.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming or structure)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: rename `d` to `discountFraction` and delete the comment.

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
  > ```
  > // checkout.ts retries the payment step and calls applyCoupon a second time,
  > // so remember applied codes here and skip them on the second call.
  > ```
  Fix: the cause (the double call) is in `checkout.ts`, which is outside the files in scope. Removing the guard while the cause stands re-enables double-applying coupons. File a ticket to fix the cause first, then remove the workaround.

  **Draft ticket**
  **Title:** Stop `checkout.ts` double-calling `applyCoupon` and remove the deduplication guard
  **Body:** `applyCoupon` in `shop/src/coupon.ts` holds a module-level `applied` Set to skip coupons on a second call, because `checkout.ts` retries the payment step and calls `applyCoupon` a second time (see the comment at `shop/src/coupon.ts:4–5`). This guard only works for the lifetime of the process; in a long-running server it will permanently block re-use of a coupon code across requests. First, fix `checkout.ts` to call `applyCoupon` at most once per checkout attempt; then remove the `applied` Set and its guard from `coupon.ts`.
  **Files to:** No tracker was found, so this draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: file a ticket and link it from the TODO.

  **Draft ticket**
  **Title:** Support express shipping in `shippingCents`
  **Body:** `shop/src/shipping.ts:3` has an untracked TODO: `// TODO: support express shipping`. `shippingCents` currently handles only standard zone-based rates applied per kilogram; express shipping would need a separate rate schedule or a carrier API call. This work cannot be scoped until the rate source is decided.
  **Files to:** No tracker was found, so this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: file a ticket and link it from the TODO.

  **Draft ticket**
  **Title:** Add retry logic to rsync upload in deploy script
  **Body:** The rsync command in `scripts/deploy.sh` has no retry logic. If the network drops mid-transfer, the deployment fails silently and the server may be left with a partial copy of the build output. This gap is noted in the code but is not tracked anywhere. The work is to add a retry loop around the rsync call (e.g. using `--partial` with a wrapper loop or a utility such as `retry`) so transient network failures recover automatically without manual intervention. Location: `scripts/deploy.sh:7`. Comment: `# TODO: retry the upload when the network drops`.
  **Files to:** No tracker was found, so this draft stays in the report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > ```
  > // We chose a static zone table over the carrier's rate API because the API
  > // took two seconds per call and blocked checkout, and rates change once a year.
  > ```
  Fix: move into an ADR and replace the comment with a one-line pointer.

  **Draft ADR** — `docs/adr/0001-static-zone-rate-table.md` (waiting: `docs/adr/` does not exist)
  ```md
  # Static zone rate table over carrier rate API

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```
  Pointer that replaces the two-line comment:
  `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
