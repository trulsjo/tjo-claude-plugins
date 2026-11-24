Whole repo, 10 files read, 15 findings.

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc repeats the signature)
  > ```
  > /**
  >  * Formats cents.
  >  * @param cents the cents
  >  * @returns the string
  >  */
  > ```
  Fix: delete the doc comment. "Formats cents" restates the function name; `@param cents the cents` and `@returns the string` add nothing beyond the names and types.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > ```
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  > ```
  Fix: delete both lines; git keeps the history.

- `shop/src/dates.ts:8` - class 4 (workaround for something outside our control, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: append a link to the upstream Node.js / V8 ICU bug tracking this DST-skip behaviour. The repo does not already hold the URL, so the link should point to the relevant V8 or Node.js issue tracker entry for Intl DST handling in affected time zones.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: delete the comment; history lives in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: delete the comment. The function applies `rate * Math.ceil(weightGrams / 1000)` for all weights with no 20 kg threshold and no flat-rate logic; the comment matches neither the behaviour nor the structure.

- `tools/report.py:4` - class 10 (API doc repeats the signature)
  > ```
  > """Builds report.
  > :param rows: the rows
  > :param path: the path
  > """
  > ```
  Fix: delete the entire docstring. The summary "Builds report." restates the function name, and both `:param` lines copy the parameter names verbatim. Nothing here is not already visible from the signature.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: delete the comment. Git keeps the history.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: delete the comment. What changed, who changed it and when belongs in the commit log.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: delete the comment. The `rsync` command and its destination already say this.

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: rename `d` to `discountFraction`; the comment is then unnecessary.

  ```diff
  -  // d is the discount as a fraction between 0 and 1
  -  const d = discountPct / 100;
  +  const discountFraction = discountPct / 100;
     // Round to whole cents: the payment provider rejects fractional amounts.
  -  return Math.round(t * (1 - d));
  +  return Math.round(t * (1 - discountFraction));
  ```

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > ```
  > // checkout.ts retries the payment step and calls applyCoupon a second time,
  > // so remember applied codes here and skip them on the second call.
  > ```
  Fix: the cause (`checkout.ts` calling `applyCoupon` twice) lies outside the files in scope; removing the guard while the cause stands would reintroduce the bug. File a ticket.

  **Draft ticket**
  Title: `Remove double-call guard in applyCoupon once checkout retry is fixed`
  Body: `applyCoupon` in `shop/src/coupon.ts` holds a module-level `applied` set that skips duplicate coupon applications. This workaround exists because `checkout.ts` retries the payment step and calls `applyCoupon` a second time per checkout. The fix has two steps: (1) update `checkout.ts` so it calls `applyCoupon` at most once per checkout session, then (2) remove the `applied` set and the early-return guard from `applyCoupon`. Location: `shop/src/coupon.ts`, lines 4–6.
  Files to: no tracker was found.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: file a ticket for express-shipping support and replace the bare TODO with a ticketed reference such as `TODO(#N): support express shipping`.

  **Draft ticket**
  Title: `Support express shipping in shippingCents`
  Body: An untracked TODO at `shop/src/shipping.ts` line 3 asks for express-shipping support. No ticket currently tracks this work. Once filed, the TODO in the source should be updated to reference the ticket number, e.g. `TODO(#N): support express shipping`.
  Files to: no tracker was found.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: file a ticket for retry logic and replace the bare TODO with a ticketed reference.

  **Draft ticket**
  Title: `Add retry logic to deploy upload on network failure`
  Body: `scripts/deploy.sh` line 7 has an untracked TODO: "retry the upload when the network drops". The rsync step currently has no retry, so a transient network drop fails the entire deploy. Add retry logic (e.g. a loop with backoff) or use rsync's built-in `--checksum`/`--partial` flags with a wrapper that retries on non-zero exit.
  Files to: no tracker was found.

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > ```
  > // We chose a static zone table over the carrier's rate API because the API
  > // took two seconds per call and blocked checkout, and rates change once a year.
  > ```
  Fix: move into an ADR and replace with a one-line pointer.

  **Draft ADR** — `docs/adr/0001-static-zone-rate-table.md` (waiting: `docs/adr/` does not exist)
  ```md
  # Static zone rate table

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```
  Pointer that replaces the comment: `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
