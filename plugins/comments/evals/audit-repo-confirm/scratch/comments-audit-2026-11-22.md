# Comment audit — 2026-11-22

Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc repeats the signature)
  > `/**`
  > ` * Formats cents.`
  > ` * @param cents the cents`
  > ` * @returns the string`
  > ` */`
  Fix: delete the comment. "Formats cents" restates the function name; both tags add nothing to the names and types.

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: delete; git keeps it.

- `shop/src/dates.ts:8` - class 4 (workaround with no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: append a link to the upstream Node.js or V8 issue documenting the DST-skipping behaviour. The repo does not hold such a URL; the link should point to the relevant Node.js GitHub issue (https://github.com/nodejs/node/issues) or V8 bug report for Intl timezone/DST handling.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: delete; history lives in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: delete the comment. The code returns `rate * Math.ceil(weightGrams / 1000)` — a per-kilogram weighted rate for any weight — with no 20 kg threshold and no flat rate.

- `tools/report.py:5` - class 10 (API doc repeats the signature)
  > `"""Builds report.`
  > ` `
  > `    :param rows: the rows`
  > `    :param path: the path`
  > `    """`
  Fix: delete the doc comment. The summary restates the function name; both `:param` lines add nothing to the parameter names.

- `tools/report.py:13` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: delete; git keeps it.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: delete the comment. History lives in commit messages.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: delete the comment.

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
  The cause lies in `checkout.ts`, which is outside the files in scope; removing the guard while the retry remains would reintroduce the bug.

  **Draft ticket**
  Title: `Remove coupon deduplication guard from applyCoupon`
  Body: `applyCoupon` in `shop/src/coupon.ts` maintains a module-level `applied` Set (lines 1–8) to guard against double-application when `checkout.ts` retries the payment step and calls `applyCoupon` a second time. The workaround is at lines 4–6. The root cause is in `checkout.ts`: the payment retry path re-invokes `applyCoupon` instead of skipping the coupon step. Work: (1) fix `checkout.ts` so payment retries do not call `applyCoupon` again; (2) once that is done, remove the `applied` Set and its guard from `coupon.ts`.
  Files to: no tracker was found, so this draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: file a ticket and link it from the TODO.

  **Draft ticket**
  Title: `Support express shipping in shippingCents`
  Body: `shippingCents` in `shop/src/shipping.ts` does not handle express shipping; a TODO at line 3 notes this but names no ticket. The current implementation only supports zone-based ground rates from `ZONE_RATES`. Work: decide on an express-shipping rate model, add it to `shippingCents`, and update the TODO to reference this ticket (`TODO(#N): support express shipping`), or delete the TODO if the work is not planned.
  Files to: no tracker was found, so this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: file a ticket and link it from the TODO.

  **Draft ticket**
  Title: `Add retry logic to rsync upload in deploy.sh when network drops`
  Body: The deploy script's rsync call has no retry on network failure. A transient drop will abort the deployment with no recovery. This work is tracked by an unlinked TODO at `scripts/deploy.sh:7`: `# TODO: retry the upload when the network drops`. Once a ticket is filed, link it in the TODO (`TODO(#N): retry the upload when the network drops`).
  Files to: no tracker was found, so this draft stays in the report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: move into an ADR and leave a one-line pointer.

  **Draft — `docs/adr/0001-static-zone-rate-table.md`**:
  ```md
  # Use a static zone table instead of the carrier's rate API

  We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.
  ```
  Pointer that replaces the comment: `// Decision: docs/adr/0001-static-zone-rate-table.md`
  Status: **waiting** — no `docs/adr/` folder found.

---

Report only: no source files were changed.
