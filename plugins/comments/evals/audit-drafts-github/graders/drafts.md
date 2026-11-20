---
type: llm
weight: 2
---

The response is a comment audit of a small TypeScript repo. The repo is a git clone whose `origin` remote is `https://github.com/example/shop.git`. It has no issue-tracker doc and no ADR folder.

PASS only when all of these hold:

1. The "TODO: support express shipping" comment in `src/shipping.ts` has a ticket draft with a title and a body (the body is at least one sentence of its own, not just the quoted comment).
2. That draft says it would be filed as a GitHub issue (via `gh`, or in `example/shop`). It applies no label unconditionally: either no label, or `needs-triage` only if that label exists in the repo.
3. The "We chose a static zone table over the carrier's rate API ..." comment has an ADR draft with a title, the decision with its reason, and a one-line pointer comment that would replace the original comment.
4. The response notes that the repo has no ADR folder and asks the user whether to create one (for example `docs/adr/`).
5. The response presents the ticket and the ADR as not yet created (for example "would be filed", "draft", "Report only: no files were changed").

Otherwise FAIL. Name each condition that fails.
