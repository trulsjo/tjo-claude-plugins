`the whole repo`, 10 files read, 15 findings
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2

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

  Fix: delete the doc comment. "Formats cents" restates `formatCents`; both `@param` and `@returns` tags repeat the name and type verbatim with no added fact.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > ```
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  > ```

  Fix: delete both lines; git keeps them.

- `lib/src/dates.ts:8` - class 4 (workaround for something outside our control, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`

  Fix: append a link to the upstream Node.js / V8 issue tracking this DST-handling quirk in `Intl` date arithmetic. The repo does not already hold the URL; the link should point to the relevant Node.js issue tracker entry or the V8 bug for incorrect DST-aware `Intl` date math.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`

  Fix: delete the comment; history lives in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`

  Fix: delete the comment. The function applies to all weights (no 20 kg threshold) and the return value scales with weight, so neither claim matches the code.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > ```
  > """Builds report.
  >
  >     :param rows: the rows
  >     :param path: the path
  >     """
  > ```

  Fix: delete the docstring. "Builds report" restates `build_report`; `:param rows: the rows` and `:param path: the path` each copy the parameter name and add no fact.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`

  Fix: delete the line; git keeps it.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`

  Fix: delete the comment. History lives in commit messages.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`

  Fix: delete the comment. The rsync command and its arguments state this plainly.

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`

  Fix: rename `d` to `discountFraction` throughout `cartTotal`, then delete the comment.

  ```diff
  -  // d is the discount as a fraction between 0 and 1
  -  const d = discountPct / 100;
  +  const discountFraction = discountPct / 100;
     // Round to whole cents: the payment provider rejects fractional amounts.
  -  return Math.round(t * (1 - d));
  +  return Math.round(t * (1 - discountFraction));
  ```

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code; cause is outside the files in scope)
  > ```
  > // checkout.ts retries the payment step and calls applyCoupon a second time,
  > // so remember applied codes here and skip them on the second call.
  > ```

  **Draft ticket:**
  Title: `Remove duplicate-call guard in applyCoupon by fixing the retry logic in checkout.ts`

  Body: `applyCoupon` in `shop/src/coupon.ts` holds a module-level `applied` Set that silently skips a coupon code when `checkout.ts` calls the function a second time during a payment-step retry. The workaround masks the real defect: `checkout.ts` applies the coupon on every retry attempt rather than once per checkout session.

  Work to do, in order:
  1. Find the retry path in `checkout.ts` and prevent it from calling `applyCoupon` more than once per session (for example, guard the call site or move the coupon step outside the retry loop).
  2. Once the caller is fixed, remove the `applied` Set and the early-return branch from `applyCoupon` in `shop/src/coupon.ts` lines 1 and 5–6.

  Location: `shop/src/coupon.ts`, lines 4–5.
  Files to: no tracker was found; this draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`

  **Draft ticket:**
  Title: `Add express-shipping support to shippingCents`

  Body: `shippingCents` in `shop/src/shipping.ts` returns only standard rates from the static zone table. The untracked TODO at line 3 notes that express shipping is not yet supported. Add express-shipping rate logic — a separate rate table, a service-level parameter, or a multiplier — so callers can request express delivery and receive a correctly priced result.

  Location: `shop/src/shipping.ts`, line 3.
  Files to: no tracker was found; this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`

  **Draft ticket:**
  Title: `Add network-drop retry to rsync upload in deploy.sh`

  Body: The rsync upload in `scripts/deploy.sh` (line 9) has no retry on network failure. If the connection drops mid-transfer the deployment silently fails with a non-zero exit, leaving the server in a partially updated state. The TODO at line 7 flags this as known but untracked. Add retry logic (a loop around the rsync call, or `--partial` with a re-invocation) so transient network errors do not permanently fail a deploy.

  Location: `scripts/deploy.sh`, line 7.
  Files to: no tracker was found; this draft stays in the report.

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > ```
  > // We chose a static zone table over the carrier's rate API because the API
  > // took two seconds per call and blocked checkout, and rates change once a year.
  > ```

  **Draft ADR** (waiting — `docs/adr/` does not exist):

  File: `docs/adr/0001-static-zone-rate-table.md`

  ```md
  # Static zone rate table over carrier rate API

  We chose a static zone table over the carrier's rate API because the API
  took two seconds per call and blocked checkout, and rates change once a year.
  ```

  Pointer that replaces the decision comment in `shop/src/shipping.ts`:
  `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
Reply "yes" to apply the 10 trivial fixes, or name the ones to apply.

No tracker was found, so the 3 ticket drafts stay in the report. 1 ADR would be written to `docs/adr/0001-static-zone-rate-table.md`; its draft is above, and a yes to it creates the file and replaces the decision comment with its pointer.

Create docs/adr/ for these ADRs?
