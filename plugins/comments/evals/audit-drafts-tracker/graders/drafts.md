---
type: llm
weight: 2
---

The response is a comment audit of a small TypeScript repo. The repo has an issue-tracker doc (GitHub via `gh`, repo `example/shop`, every new issue gets the label `triage/new`) and an ADR folder `docs/adr/` holding `0001-amounts-in-integer-cents.md`.

PASS only when all of these hold:

1. The "TODO: support express shipping" comment in `src/shipping.ts` has a ticket draft with a title and a body (the body is at least one sentence of its own, not just the quoted comment).
2. That ticket draft says where it would be filed in a way that follows the tracker doc: GitHub issues in `example/shop` (or via `gh`), with the label `triage/new`.
3. The "We chose a static zone table over the carrier's rate API ..." comment has an ADR draft: a file path `docs/adr/0002-<slug>.md`, a title, the decision with its reason, and a one-line pointer comment that would replace the original comment.
4. The response presents the ticket and the ADR as not yet created (for example "would be filed", "draft", "Report only: no files were changed") and offers to create them once the user confirms.

Otherwise FAIL. Name each condition that fails.
