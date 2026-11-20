---
type: llm
weight: 2
---

The response is a comment audit of a small TypeScript project. Compare the findings it reports against this answer key. Identify each comment by its quoted text.

Comments that must NOT be reported as findings (keep list):

- K1 `src/cart.ts`: the license header "Copyright (c) 2026 Example Shop AS. Licensed under the MIT License."
- K2 `src/cart.ts`: the doc comment on `cartTotal` ("Total price of a cart in cents, after the percentage discount. Returns 0 for an empty cart. Throws RangeError ...").
- K3 `src/cart.ts`: "Round to whole cents: the payment provider rejects fractional amounts."
- K4 `src/dates.ts`: the Safari comment with the bugs.webkit.org link.
- K5 `src/dates.ts`: "eslint-disable-next-line @typescript-eslint/no-explicit-any".
- K6 `src/dates.ts`: "TODO(#142): accept Unix timestamps in seconds as well".

Comments that should be reported, with their expected class:

- F1 `src/cart.ts` "loop over the items and add up price times quantity": class 1 (narrates the how).
- F2 `src/cart.ts` "d is the discount as a fraction between 0 and 1": class 2 (compensates for naming).
- F3 `src/cart.ts` the doc comment on `formatCents` ("Formats cents. @param cents the cents @returns the string"): class 10 (API doc repeats the signature).
- F4 `src/cart.ts` the two commented-out lines `const euros = ...` / `return euros + ...`: class 7 (commented-out code).
- F5 `src/shipping.ts` "Changed in v2.3: now uses the zone table instead of the flat 499-cent rate.": class 8 (history).
- F6 `src/shipping.ts` "TODO: support express shipping": class 9 (TODO with no ticket).
- F7 `src/shipping.ts` "Returns the flat rate for parcels over 20 kg.": class 6 (stale or lying).
- F8 `src/shipping.ts` "We chose a static zone table over the carrier's rate API ...": class 5 (records a decision).
- F9 `src/coupon.ts` "checkout.ts retries the payment step and calls applyCoupon a second time ...": class 3 (workaround in our own code).
- F10 `src/dates.ts` "Node's Intl date math skips DST changes ...": class 4 flagged for a missing upstream link.

Scoring rules:

- A class 1 finding where the key says class 2, or class 2 where the key says class 1, counts as correct (soft miss).
- A comment the response explicitly lists as kept or not a finding is not a finding.
- Findings on comments not in this key count as flagged comments with a wrong class.

Count: flagged = number of distinct comments the response reports as findings; correct = flagged comments whose class matches the key (with the soft-miss rule); found = how many of F1-F10 are reported.

PASS only when all three hold:
1. None of K1-K6 is reported as a finding.
2. correct / flagged is at least 0.85.
3. found is at least 8.

Otherwise FAIL. State the three numbers and any K item that was flagged.
