---
type: llm
weight: 2
---

The response is a comment audit of a small project in Python, C++, shell and YAML. Compare the findings it reports against this answer key. Identify each comment by its quoted text.

Comments that must NOT be reported as findings (keep list):

- K1 `src/billing.py`: the license header "Copyright (c) 2026 Example Shop AS. Licensed under the MIT License."
- K2 `src/billing.py`: the docstring of `invoice_total` ("Sum of the open invoices' amounts, in NOK. Paid invoices are skipped ... Raises ValueError ...").
- K3 `src/billing.py`: "type: ignore[index]".
- K4 `src/rate_limiter.cpp`: the "SPDX-License-Identifier: MIT" / "Copyright (c) 2026 Example Shop AS." header.
- K5 `src/rate_limiter.cpp`: the libstdc++ shared_mutex comment with the gcc.gnu.org bugzilla link.
- K6 `src/rate_limiter.cpp`: "NOLINT(cppcoreguidelines-avoid-non-const-global-variables)".
- K7 `src/rate_limiter.cpp`: the doc comment on `try_acquire` ("Takes one token from the bucket. @return true if a token was taken, false if the bucket is empty. Never blocks.").
- K8 `scripts/deploy.sh`: "shellcheck disable=SC2086" (the `#!/usr/bin/env bash` shebang is not a finding either).
- K9 `scripts/deploy.sh`: "TODO(#87): invalidate the CloudFront cache after the upload".
- K10 `config/app.yaml`: "Must stay below the load balancer's 60 s idle timeout, or it drops the connection mid-request."

Comments that should be reported, with their expected class:

- F1 `src/billing.py` "loop over the invoices and add up the open ones": class 1 (narrates the how).
- F2 `src/billing.py` `print("total", total)` commented out: class 7 (commented-out code).
- F3 `src/billing.py` the docstring of `get_customer` ("Gets the customer. :param customer_id: the customer id :returns: the customer"): class 10 (API doc repeats the signature).
- F4 `src/rate_limiter.cpp` "n is the number of tokens left in the bucket": class 2 (compensates for naming).
- F5 `src/rate_limiter.cpp` "Returns -1 when the bucket is empty.": class 6 (stale or lying; the code returns false).
- F6 `src/rate_limiter.cpp` "The scheduler in scheduler.cpp calls refill twice per tick, so only add half here.": class 3 (workaround in our own code).
- F7 `src/rate_limiter.cpp` the doc comment on `get_capacity` ("@brief Gets the capacity. @return the capacity"): class 10.
- F8 `scripts/deploy.sh` "Added by Kim in March 2025: now uploads with aws s3 sync instead of rsync.": class 8 (history).
- F9 `scripts/deploy.sh` "copy the build directory to the bucket": class 1.
- F10 `scripts/deploy.sh` "TODO: retry the upload when the network drops": class 9 (TODO with no ticket).
- F11 `config/app.yaml` "We chose Redis over Memcached for sessions ...": class 5 (records a decision).
- F12 `config/app.yaml` "ingress-nginx silently ignores proxy timeouts above 3600 s (an upstream bug) ...": class 4, flagged for a missing upstream link.
- F13 `config/app.yaml` "replicas: 4" commented out: class 7.

Scoring rules:

- A class 1 finding where the key says class 2, or class 2 where the key says class 1, counts as correct (soft miss).
- A comment the response explicitly lists as kept or not a finding is not a finding.
- Findings on comments not in this key count as flagged comments with a wrong class.

Count: flagged = number of distinct comments the response reports as findings; correct = flagged comments whose class matches the key (with the soft-miss rule); found = how many of F1-F13 are reported.

PASS only when all three hold:
1. None of K1-K10 is reported as a finding.
2. correct / flagged is at least 0.85.
3. found is at least 11.

Otherwise FAIL. State the three numbers and any K item that was flagged.
