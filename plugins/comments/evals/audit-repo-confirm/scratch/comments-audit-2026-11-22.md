# Comment audit — 2026-11-22

the whole repo, 10 files read, 15 findings.
By fix size: trivial 10, local refactor 1, ticket 3, ADR 1
By class: class 1: 2, class 2: 1, class 3: 1 (ticket), class 4: 1, class 5: 1, class 6: 1, class 7: 2, class 8: 2, class 9: 2, class 10: 2

---

### Trivial

- `shop/src/cart.ts:12` - class 1 (narrates the how)
  > `// loop over the items and add up price times quantity`
  Fix: delete the comment.

- `shop/src/cart.ts:25-29` - class 10 (API doc repeats the signature)
  > `/** Formats cents. @param cents the cents @returns the string */`
  Fix: delete the entire doc block; every word is already in the name and types. If contract details exist (output format, rounding, locale), rewrite with those instead.

- `shop/src/cart.ts:30-31` - class 7 (commented-out code)
  > `// const euros = Math.floor(cents / 100);`
  > `// return euros + "," + (cents % 100);`
  Fix: delete both lines; git keeps the history.

- `shop/src/dates.ts:8` - class 4 (upstream workaround, no link)
  > `// Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.`
  Fix: append a link to the upstream Node.js or V8/ICU issue tracking this behaviour; leave the comment text unchanged. Cite a URL only when the repo already holds it; otherwise say what the link should point to.

- `shop/src/shipping.ts:1` - class 8 (history or changelog)
  > `// Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.`
  Fix: delete; history belongs in commit messages.

- `shop/src/shipping.ts:4` - class 6 (stale or lying)
  > `// Returns the flat rate for parcels over 20 kg.`
  Fix: delete or rewrite. The code applies a per-kg rate to parcels of any weight; there is no 20 kg threshold and no flat rate.

- `tools/report.py:5` - class 10 (API doc repeats the signature)
  > `"""Builds report.\n\n    :param rows: the rows\n    :param path: the path\n    """`
  Fix: delete the docstring, or replace with what the reader cannot see (e.g., what `rows` must contain, what file format is written, what exceptions can propagate).

- `tools/report.py:12` - class 7 (commented-out code)
  > `# print(rows)`
  Fix: delete; git keeps it.

- `config/app.yaml:3` - class 8 (history or changelog)
  > `# Timeout raised from 30 to 60 seconds by Kim in March.`
  Fix: delete; history belongs in commit messages.

- `scripts/deploy.sh:8` - class 1 (narrates the how)
  > `# copy the build output to the server with rsync`
  Fix: delete the comment.

---

### Local refactor

- `shop/src/cart.ts:18` - class 2 (compensates for naming)
  > `// d is the discount as a fraction between 0 and 1`
  Fix: rename `d` to `discountFraction`, then delete the comment.

  ```diff
  - const d = coupon.value / 100;
  - // d is the discount as a fraction between 0 and 1
  + const discountFraction = coupon.value / 100;
  ```

---

### Ticket

- `shop/src/coupon.ts:4-5` - class 3 (workaround in our own code; cause is outside this repo)
  > `// checkout.ts retries the payment step and calls applyCoupon a second time, so remember applied codes here and skip them on the second call.`
  Fix: ticket — the cause (`checkout.ts`) is not in this repo, so the workaround cannot safely be removed here first.

  **Draft ticket**
  Title: Remove duplicate-call guard in `applyCoupon` once `checkout.ts` retry is fixed
  Body: `shop/src/coupon.ts:4-5` holds a workaround for `checkout.ts` calling `applyCoupon` a second time during the payment retry step. Because `checkout.ts` is not in this repo, the workaround cannot be removed safely until its cause is gone. Work: (1) fix the retry logic in `checkout.ts` to call `applyCoupon` at most once per checkout; (2) remove the module-level `applied` set and this comment from `coupon.ts`.
  Files to: no tracker was found, so this draft stays in the report.

- `shop/src/shipping.ts:3` - class 9 (TODO with no ticket)
  > `// TODO: support express shipping`
  Fix: file a ticket and replace with `// TODO(#<n>): support express shipping`, or delete if not planned.

  **Draft ticket**
  Title: Support express shipping
  Body: `shop/src/shipping.ts:3` has an untracked TODO for express shipping support. File a ticket to track this work, then update the comment to `// TODO(#<n>): support express shipping`.
  Files to: no tracker was found, so this draft stays in the report.

- `scripts/deploy.sh:7` - class 9 (TODO with no ticket)
  > `# TODO: retry the upload when the network drops`
  Fix: file a ticket and replace with `# TODO(#<n>): retry the upload when the network drops`, or delete if not planned.

  **Draft ticket**
  Title: Retry rsync upload on network failure in deploy.sh
  Body: `scripts/deploy.sh:7` has an untracked TODO for retrying the upload when the network drops. File a ticket to track this reliability improvement, then update the comment to `# TODO(#<n>): retry the upload when the network drops`.
  Files to: no tracker was found, so this draft stays in the report.

---

### ADR

- `shop/src/shipping.ts:9-10` - class 5 (records a decision)
  > `// We chose a static zone table over the carrier's rate API because the API took two seconds per call and blocked checkout, and rates change once a year.`
  Fix: move into an ADR and leave a one-line pointer.

  **Draft ADR** — `docs/adr/0001-static-zone-table.md` (waiting: folder does not exist)

  ```md
  # Static zone rate table over carrier rate API

  The carrier's live rate API took two seconds per call and blocked checkout, so we chose a static zone table instead; rates change once a year, making the trade-off acceptable.
  ```

  Pointer to replace the comment:
  `// Decision: docs/adr/0001-static-zone-table.md`

---

Report only: no source files were changed.
