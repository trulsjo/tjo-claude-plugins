---
name: audit
description: Comment hygiene audit - report which code comments in a file or folder to delete, move or replace with code, by the comment rubric, grouped by fix size. Use only when the user's request names comments - auditing or cleaning up comments, comment noise, stale comments, untracked TODOs. Code reviews, bug hunts and refactoring requests that do not mention comments are out of scope.
---

# audit

A **report-first** audit. Every comment in scope is judged against the rubric, and each one that does not earn its place becomes a finding with a class and a fix. Files change only through **Confirm and apply** below: after the user answers the report's offer with a yes, or when the request carries `--fix`. Any other request, "clean up" included, ends at the report.

## Steps

1. **Load the rubric.** Read `${CLAUDE_PLUGIN_ROOT}/rubric.md`. It holds the classes, the keep list, the fix sizes and the scope rules; it is the only source of the rules. Done when you have read the whole file.

2. **Fix the scope.** The target is the path the user named (a file or a folder, recursively); with no path, ask for one. List the files in it that the rubric's scope covers, skipping dependency and build output (`node_modules`, `vendor`, `dist`, `build`, `.git`). Done when you have the file list.

3. **Read the repo's standards.** Search the repo for files that document how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, style guides under `docs/`). Note every rule that speaks about comments or API docs. Done when you can name each such rule, or know there are none.

4. **Judge every comment.** Read each file in full. For each comment, decide: on the keep list, or one class from the rubric. A comment that a repo rule from step 3 requires or allows is kept: the repo wins. Done when every comment in every listed file has a verdict.

5. **Apply with `--fix`.** When the request carries `--fix`, apply the trivial findings now, by **Confirm and apply**, without asking. Without `--fix`, skip this step. Done when every trivial finding is applied or marked why not, or the step was skipped.

6. **Write the report** in chat, in the format below. Done when every finding from step 4 is in it, under `### Applied` or its fix size.

## Report format

Groups in this order, each a heading, empty groups left out: `### Trivial`, `### Local refactor`, `### Ticket`, `### ADR`. Each finding:

```
- `src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: delete the comment.
```

- **Fix** follows the class's default action and names the concrete change: the new name for a rename, the function to extract, the link to add.
- A local refactor carries the patch as a diff block. A ticket carries a draft (title and two-line body). An ADR carries a draft (title and the decision in one to three sentences) and the one-line pointer that replaces the comment.

Open the report with one line: the scope, the number of files read, and the finding count per class. With no findings the report is that line and `No findings.`

When fixes were applied, an `### Applied` group comes first. Its entries keep the finding format with `Applied:` in place of `Fix:`, naming the change made. Findings not applied stay in their fix-size group; one that could not be applied says why on a `Not applied:` line.

Close with one line:

- Nothing applied: `Report only: no files were changed.` When trivial findings exist, add the offer: `Reply "yes" to apply the N trivial fixes, or name the ones to apply.`
- Fixes applied: `Applied N fixes in M files; nothing else was changed.`

## Confirm and apply

How a finding goes from the report into the code. Two things start it: the user's reply to the report's offer, or `--fix` (step 5).

1. **Pick the findings.** A bare yes ("yes", "apply them", "go ahead") covers every trivial finding in the last report. A reply that names findings, by location or quoted comment, covers those. `--fix` covers every trivial finding of this run. Other replies are not a yes: answer them and change nothing. Done when you have the list of findings to apply, each with its fix size.

2. **Apply each finding** by its fix size:

   | Fix size | How it is applied |
   |---|---|
   | trivial | The edit below. Comment text only, so no typecheck or test run. |
   | local refactor | Not applied: stays in the report. |
   | ticket | Not applied: stays in the report. |
   | ADR | Not applied: stays in the report. |

   `--fix` and a bare yes reach the trivial row only. Any other row is reached only by a reply that names that finding.

   The trivial edit: re-read the file, then make one Edit per finding.
   - **Delete**: remove the comment's lines whole, leaving the code and its indentation as they were.
   - **Move into the API doc**: put the comment's *what* into the function's doc comment, in the file's doc-comment convention (JSDoc above a TypeScript function, a docstring in Python); create the doc comment when there is none. Then delete the inline comment.
   - **Rewrite** (class 6 fix, class 10 rewrite): replace the comment text with the fix the report gave.
   - A fix that needs a fact the code does not hold, such as the upstream link for class 4, is not applied: it stays in the report with `Not applied: needs <the fact>`.

   Done when every picked finding is applied or marked `Not applied` with its reason, and re-reading each changed file shows only comment lines changed.

3. **Report.** Under `--fix`, return to step 6. After a reply, write the report again in the format above, with the applied findings under `### Applied`. Done when every finding of the last report appears once, applied or not.
