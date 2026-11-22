# Comment audit — 2026-11-22

Whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`

  Fix: delete the comment.

- `shop/src/cart.ts:25-28` - class 10 (API doc repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`

  Fix: delete the doc comment. `formatCents(cents: number): string` already carries every fact these lines state.

- `shop/src/cart.ts:30-31` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`

  Fix: delete both lines.

- `shop/src/dates.ts:8` - class 4 (workaround outside our control, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`

  Fix: append a link to the upstream Node.js or V8 issue tracking this Intl DST behaviour. The repo does not hold a URL for it; the link should point to the relevant report on the Node.js GitHub issue tracker or the V8 bug tracker. Leave the comment's text as it is.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`

  Fix: delete the comment.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`

  Fix: delete the comment. The function computes `rate * Math.ceil(weightGrams / 1000)` — a per-kilogram charge for any parcel weight, not a flat rate and not restricted to parcels over 20 kg.

- `tools/report.py:5-9` - class 10 (API doc repeats the signature)
  > `"""Builds report.`
  > `:param rows: the rows`
  > `:param path: the path`
  > `"""`

  Fix: delete the docstring. `build_report(rows, path)` already carries every fact these lines state.

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`

  Fix: delete the line.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`

  Fix: delete the comment.

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

- `shop/src/coupon.ts:4-5` - class 3 (workaround in our own code; cause is outside the files in scope)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time,`
  > `// so remember applied codes here and skip them on the second call.`

  Fix: file a ticket to fix the retry logic in `checkout.ts` so it calls `applyCoupon` at most once per checkout, then remove the `applied` Set and its guard from `coupon.ts`.

  **Draft ticket**
  Title: Remove double-apply guard in `applyCoupon` after fixing retry in `checkout.ts`
  Body: `shop/src/coupon.ts` holds a module-level `applied` Set that silently skips a second `applyCoupon` call with the same coupon code. This workaround exists because `checkout.ts` retries the payment step and calls `applyCoupon` twice per checkout. The guard masks the root cause and could hide legitimate double-apply bugs. Work: (1) fix the retry logic in `checkout.ts` so it calls `applyCoupon` at most once per checkout; (2) remove the `applied` Set and the `if (applied.has(code)) return totalCents;` guard from `shop/src/coupon.ts`.
  Files to: no tracker found — draft stays in report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`

  Fix: file a ticket for express-shipping support and link it from the TODO (`TODO(#N): support express shipping`).

  **Draft ticket**
  Title: Support express shipping in `shippingCents`
  Body: `shop/src/shipping.ts:3` contains `// TODO: support express shipping`. The `shippingCents` function only computes standard zone-rate shipping via `ZONE_RATES`; there is no express tier. File a ticket to track the design and implementation of express shipping support, then update the TODO to reference the ticket number.
  Files to: no tracker found — draft stays in report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`

  Fix: file a ticket for upload retry logic and link it from the TODO (`# TODO(#N): retry the upload when the network drops`).

  **Draft ticket**
  Title: Retry rsync upload on network failure in `scripts/deploy.sh`
  Body: The deploy script's upload step has no retry logic. If the network drops mid-deployment, the script fails with no recovery. The work is to add retry logic (e.g. a loop or a `--retries`-style wrapper) around the `rsync` call in `scripts/deploy.sh`. Location: `scripts/deploy.sh:7` — `# TODO: retry the upload when the network drops`.
  Files to: no tracker found — draft stays in report.

---

### ADR

- `shop/src/shipping.ts:9-10` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API`
  > `// took two seconds per call and blocked checkout, and rates change once a year.`

  Fix: move into `docs/adr/0001-static-zone-rate-table.md` and replace lines 9-10 with `// Decision: docs/adr/0001-static-zone-rate-table.md`.

  **Draft ADR** (`docs/adr/0001-static-zone-rate-table.md`) — waiting (folder does not exist)
  ```md
  # Static zone rate table over carrier rate API

  We chose a static zone table over the carrier's rate API because the API
  took two seconds per call and blocked checkout, and rates change once a year.
  ```
  Pointer to replace lines 9-10: `// Decision: docs/adr/0001-static-zone-rate-table.md`

---

Report only: no source files were changed.
