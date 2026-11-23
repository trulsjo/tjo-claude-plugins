Whole repo, 10 files read, 15 findings: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > /**
  >  * Formats cents.
  >  * @param cents the cents
  >  * @returns the string
  >  */
  Fix: delete the doc comment. Every word in it (`Formats cents`, `the cents`, `the string`) is already expressed by the function name, the parameter name, and the return type.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  Fix: delete both lines; git keeps the history.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > // Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.
  Fix: delete the comment; history belongs in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > // Returns the flat rate for parcels over 20 kg.
  Fix: delete the comment. The function has no 20 kg threshold and does not return a flat rate; it returns `rate * Math.ceil(weightGrams / 1000)` for any weight.

- `shop/src/dates.ts:8` - class 4 (upstream workaround with no link)
  > // Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.
  Fix: append a link to the upstream bug report. The comment's text stays as-is; a link to the relevant Node.js or V8 issue (search `site:bugs.chromium.org` or `github.com/nodejs/node/issues` for "Intl DST") should be appended after the period.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > """Builds report.
  >
  >     :param rows: the rows
  >     :param path: the path
  >     """
  Fix: delete the docstring. "Builds report." restates the function name; `:param rows: the rows` and `:param path: the path` copy the parameter names as their own descriptions. Nothing beyond the signature is stated.

- `tools/report.py:12` - class 7 (commented-out code)
  > # print(rows)
  Fix: delete the line; git keeps the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > # Timeout raised from 30 to 60 seconds by Kim in March.
  Fix: delete the comment. What changed, when, and by whom belongs in the commit message.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > # copy the build output to the server with rsync
  Fix: delete the comment. The `rsync` command on the next line says this.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > // d is the discount as a fraction between 0 and 1
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

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code; cause is in `checkout.ts`, outside the files in scope)
  > // checkout.ts retries the payment step and calls applyCoupon a second time,
  > // so remember applied codes here and skip them on the second call.

  **Draft ticket**
  Title: Fix checkout double-call of `applyCoupon`
  Body: `applyCoupon` in `shop/src/coupon.ts` carries a workaround (lines 4–6) for a bug in `checkout.ts`: the payment step retries and calls `applyCoupon` a second time with the same coupon code. To compensate, `applyCoupon` keeps a module-level `applied` set and silently skips duplicate invocations. The correct fix is to stop `checkout.ts` from calling `applyCoupon` more than once per checkout, then remove the `applied` set and the guard from `applyCoupon`. Work: (1) fix `checkout.ts` so it does not call `applyCoupon` more than once per checkout flow; (2) remove the `applied` set and the early-return guard from `shop/src/coupon.ts`.
  Files to: no tracker was found, so this draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > // TODO: support express shipping

  **Draft ticket**
  Title: Support express shipping in `shippingCents`
  Body: `shippingCents` in `shop/src/shipping.ts` has an untracked TODO at line 3 for express shipping support. The function currently applies only the static zone-table rates with no express option. This work needs a ticket so it can be prioritised and the TODO updated to reference it (e.g. `TODO(#N): support express shipping`).
  Files to: no tracker was found, so this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > # TODO: retry the upload when the network drops

  **Draft ticket**
  Title: Retry rsync upload on network failure in deploy.sh
  Body: The deploy script (`scripts/deploy.sh:7`) has an untracked TODO to retry the `rsync` upload when the network drops. Currently a transient network failure causes the deploy to exit non-zero with no retry. Work: add retry logic (e.g. a loop with backoff) around the `rsync` call so that temporary connectivity issues do not leave the deployment incomplete.
  Files to: no tracker was found, so this draft stays in the report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > // We chose a static zone table over the carrier's rate API because the API
  > // took two seconds per call and blocked checkout, and rates change once a year.
  Fix: move into an ADR and replace the comment with a one-line pointer.

  **Draft ADR** (`docs/adr/0001-static-zone-rate-table.md` — _waiting_: `docs/adr/` does not exist)
  ```md
  # Static zone table over carrier rate API

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```

  Pointer to replace lines 9–10 in `shop/src/shipping.ts`:
  ```
  // Decision: docs/adr/0001-static-zone-rate-table.md
  ```

---

Report only: no source files were changed.
