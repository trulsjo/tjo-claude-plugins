---
name: audit
description: Comment hygiene audit - report which code comments in a file or folder to delete, move or replace with code, by the comment rubric, grouped by fix size. Use only when the user's request names comments - auditing or cleaning up comments, comment noise, stale comments, untracked TODOs. Code reviews, bug hunts and refactoring requests that do not mention comments are out of scope.
---

# audit

A **read-only** audit: the report is the whole output. Every comment in scope is judged against the rubric, and each one that does not earn its place becomes a finding with a class and a fix. The user picks fixes from the report in a later turn; this run ends at the report, even when the request says "clean up".

## Steps

1. **Load the rubric.** Read `${CLAUDE_PLUGIN_ROOT}/rubric.md`. It holds the classes, the keep list, the fix sizes and the scope rules; it is the only source of the rules. Done when you have read the whole file.

2. **Fix the scope.** The target is the path the user named (a file or a folder, recursively); with no path, ask for one. List the files in it that the rubric's scope covers, skipping dependency and build output (`node_modules`, `vendor`, `dist`, `build`, `.git`). Done when you have the file list.

3. **Read the repo's standards.** Search the repo for files that document how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, style guides under `docs/`). Note every rule that speaks about comments or API docs. Done when you can name each such rule, or know there are none.

4. **Judge every comment.** Read each file in full. For each comment, decide: on the keep list, or one class from the rubric. A comment that a repo rule from step 3 requires or allows is kept: the repo wins. Done when every comment in every listed file has a verdict.

5. **Write the report** in chat, in the format below. Done when every finding from step 4 is in it, under its fix size.

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

Close with: `Report only: no files were changed.`
