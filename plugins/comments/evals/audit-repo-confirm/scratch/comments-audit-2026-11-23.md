Whole repo, 10 files read, 15 findings: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > `/** * Formats cents. * @param cents the cents * @returns the string */`
  Fix: delete the doc comment. Every word it says (`Formats cents`, `the cents`, `the string`) is already expressed by the name `formatCents`, the parameter name `cents`, and the TypeScript return type `string`. Rewrite only if the calling convention, edge cases, or format details are added.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: delete both lines; git keeps them.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: append a link to the upstream Node.js or V8 issue that tracks this behaviour. The link should point to the relevant Node.js issue tracker entry or the ECMA-262 / ECMA-402 spec section that permits this platform-specific behaviour, depending on which best describes the root cause.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: delete the comment; this information belongs in the commit message.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: delete the comment. The code applies `rate * Math.ceil(weightGrams / 1000)` for all weights — there is no flat rate and no 20 kg threshold. The comment does not match the code.

- `tools/report.py:5` - class 10 (API doc that repeats the signature)
  > ```
  > """Builds report.
  >
  > :param rows: the rows
  > :param path: the path
  > """
  > ```
  Fix: delete the docstring. "Builds report." restates the function name; `:param rows: the rows` and `:param path: the path` each just echo the parameter name with no added meaning.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: delete the line; git keeps the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: delete the comment. What changed, when, and by whom belongs in commit messages.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: delete the comment. The rsync command and its arguments say exactly that.

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming: `d` does not say it is a discount fraction)
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

- `shop/src/coupon.ts:4` - class 3 (workaround for a caller in another file — `checkout.ts` — outside this repo's listed files)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`

  **Ticket draft**
  Title: Remove the duplicate-call guard in `applyCoupon` by fixing the retry in `checkout.ts`
  Body: `applyCoupon` in `shop/src/coupon.ts` keeps a module-level `applied` set so a coupon code is only deducted once. The comment at line 4 explains why: `checkout.ts` retries the payment step and calls `applyCoupon` a second time. The guard is a symptom, not a fix. The right remedy is to stop `checkout.ts` from applying the coupon on a payment retry (or to pass the deduction into the payment step only after the payment succeeds), then remove the `applied` set and its guard from `coupon.ts`. First step: locate the retry logic in `checkout.ts` and prevent it from re-entering `applyCoupon`. Second step: delete the guard.
  Files to: No tracker was found (no git remote) — this draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`

  **Ticket draft**
  Title: Support express shipping in `shippingCents`
  Body: `shippingCents` in `shop/src/shipping.ts` (line 3) has an untracked TODO for express shipping support. The current implementation covers only zone-based standard rates. File a ticket to scope the work (new zone entries, a separate rate table, or a flag on the function), then update the TODO to reference it.
  Files to: No tracker was found (no git remote) — this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`

  **Ticket draft**
  Title: Retry rsync upload on network failure in deploy script
  Body: `scripts/deploy.sh` calls `rsync` with no retry handling. When the network drops mid-transfer, the deployment fails and the operator must re-run it manually. This was noted at `scripts/deploy.sh:7`. The work is to add a retry loop or use `rsync --partial` with backoff so transient drops do not require manual intervention.
  Files to: No tracker was found (no git remote) — this draft stays in the report.

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: move into an ADR and replace with a one-line pointer.

  **ADR draft** — waiting (no `docs/adr/` folder found)
  File path: `docs/adr/0001-static-zone-rate-table.md`

  ```md
  # Static zone rate table over carrier rate API

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```

  Pointer that replaces the two comment lines in `shop/src/shipping.ts`:
  `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
Reply "yes" to apply the 10 trivial fixes, or name the ones to apply.
No tracker was found, so the 3 ticket drafts stay in the report.
1 ADR would be written once the folder exists. Create docs/adr/ for these ADRs?
