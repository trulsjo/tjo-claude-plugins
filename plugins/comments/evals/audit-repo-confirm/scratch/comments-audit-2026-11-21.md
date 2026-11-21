# Comments audit — 2026-11-21

Scope: whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1.
By class: class 1: 2, class 2: 1, class 3: 1, class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2.

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: Delete the comment.

- `shop/src/cart.ts:24` - class 10 (API doc that repeats the signature)
  > /** Formats cents. @param cents the cents @returns the string */
  Fix: Delete the doc comment, or rewrite it to state the output format (locale, separators, decimal places).

- `shop/src/cart.ts:30` - class 7 (commented-out code)
  > // const euros = Math.floor(cents / 100);
  > // return euros + "," + (cents % 100);
  Fix: Delete both lines. Git keeps the history.

- `shop/src/dates.ts:8` - class 4 (workaround — missing upstream link)
  > // Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.
  Fix: Append a link to the Node.js issue tracker or the ECMA-262 / ECMA-402 spec section documenting this behaviour. The comment text stays as-is.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > // Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.
  Fix: Delete. Version history belongs in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > // Returns the flat rate for parcels over 20 kg.
  Fix: Delete. The function applies per-zone per-kg rates for all weights; there is no flat rate or 20 kg threshold. This comment describes the pre-v2.3 implementation.

- `tools/report.py:4` - class 10 (API doc that repeats the signature)
  > """Builds report.\n\n:param rows: the rows\n:param path: the path\n"""
  Fix: Delete the docstring or rewrite it to state the expected shape of each row dict, the output format, and behaviour on empty input.

- `tools/report.py:12` - class 7 (commented-out code)
  > # print(rows)
  Fix: Delete the line. Git keeps it if ever needed.

- `config/app.yaml:3` - class 8 (history or changelog)
  > # Timeout raised from 30 to 60 seconds by Kim in March.
  Fix: Delete. The fact the value changed, when, and by whom belongs in the commit message.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > # copy the build output to the server with rsync
  Fix: Delete. The rsync command itself states this.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > // d is the discount as a fraction between 0 and 1
  Fix: Rename `d` to `discountFraction`, then delete the comment.

```diff
-  // d is the discount as a fraction between 0 and 1
-  const d = discountPct / 100;
   // Round to whole cents: the payment provider rejects fractional amounts.
-  return Math.round(t * (1 - d));
+  const discountFraction = discountPct / 100;
+  // Round to whole cents: the payment provider rejects fractional amounts.
+  return Math.round(t * (1 - discountFraction));
```

---

### Ticket

- `shop/src/coupon.ts:4` - class 3 (workaround in our own code)
  > // checkout.ts retries the payment step and calls applyCoupon a second time,
  > // so remember applied codes here and skip them on the second call.
  Fix: Refactor the checkout retry path so it does not re-apply coupons, then remove the deduplication guard and `applied` set from `coupon.ts`.

  **Ticket draft**
  Title: `applyCoupon deduplication guard can be removed once checkout no longer retries it`
  Body: `applyCoupon` maintains a module-level `applied` set solely because `checkout.ts` calls it a second time during payment retries. This couples two unrelated modules and makes the coupon module stateful across requests. Refactor the checkout retry path so it does not re-apply coupons, then remove the guard and the `applied` set from `coupon.ts`. See `shop/src/coupon.ts:4`.
  Files to: No tracker found — draft stays in report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > // TODO: support express shipping
  Fix: File a ticket and replace with `// TODO(#NNN): support express shipping`, or delete the TODO.

  **Ticket draft**
  Title: `shippingCents: add express shipping option`
  Body: `shippingCents` only supports standard zone-based rates from the zone table. Add an express shipping function or an `options` parameter that applies a separate express-rate table. Tracked from `shop/src/shipping.ts:3`.
  Files to: No tracker found — draft stays in report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > # TODO: retry the upload when the network drops
  Fix: File a ticket and replace with `# TODO(#NNN): retry the upload when the network drops`, or delete the TODO.

  **Ticket draft**
  Title: `deploy.sh: retry rsync upload on transient network failure`
  Body: The rsync step in `scripts/deploy.sh` has no retry logic. A transient network drop fails the entire deploy. Add retry with backoff (e.g. a loop or `--partial --append-verify`) so short interruptions are tolerated. Tracked from `scripts/deploy.sh:7`.
  Files to: No tracker found — draft stays in report.

---

### ADR

- `shop/src/shipping.ts:9` - class 5 (records a decision)
  > // We chose a static zone table over the carrier's rate API because the API
  > // took two seconds per call and blocked checkout, and rates change once a year.
  Fix: Move to an ADR and replace the two comment lines with a one-line pointer.

  **ADR draft** — `docs/adr/0001-static-shipping-zone-table.md` (waiting: `docs/adr/` does not exist)

  ```md
  # Use a static zone table for shipping rates instead of the carrier rate API

  The carrier rate API added approximately 2 seconds of latency per checkout call.
  Shipping rates change at most once a year, making live lookups unnecessary; a
  static zone table in the codebase was chosen instead.
  ```

  Pointer to replace the two comment lines:
  ```
  // Decision: docs/adr/0001-static-shipping-zone-table.md
  ```

---

Report only: no source files were changed.
