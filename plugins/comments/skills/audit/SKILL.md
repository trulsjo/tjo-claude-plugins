---
name: audit
description: Comment hygiene audit - report which code comments in a file, a folder or the whole repo to delete, move or replace with code, by the comment rubric, grouped by fix size. Use only when the user's request names comments - auditing or cleaning up comments, comment noise, stale comments, untracked TODOs. Code reviews, bug hunts and refactoring requests that do not mention comments are out of scope.
---

# audit

A **read-only** audit: the report is the whole output. Every comment in scope is judged against the rubric, and each one that does not earn its place becomes a finding with a class and a fix. The user picks fixes from the report in a later turn; this run ends at the report, even when the request says "clean up". The only file it writes is a repo run's report under `.scratch/`.

## Steps

1. **Load the rubric.** Read `${CLAUDE_PLUGIN_ROOT}/rubric.md`. It holds the classes, the keep list, the fix sizes and the scope rules; it is the only source of the rules. Done when you have read the whole file.

2. **Fix the scope.** The target is the path the user named (a file or a folder, recursively), or the whole repo when the user asks for it; with neither, ask for a path. List the files in it that the rubric's scope covers, skipping dependency and build output (`node_modules`, `vendor`, `dist`, `build`, `.git`). Done when you have the file list. A whole-repo target, or a list of more than 20 files, makes this a **repo run**: after step 3, follow [Repo runs](#repo-runs) in place of steps 4 and 5.

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

## Repo runs

A repo run splits the judging across sub-agents and files the report instead of printing it.

4. **Fan out.** Split the file list into batches of up to 8 files, keeping a folder's files together. Start one sub-agent per batch, all in one message. Give each: the rubric path `${CLAUDE_PLUGIN_ROOT}/rubric.md`, its batch's file paths, the repo rules from step 3, and this task: read the rubric and each file in full, give every comment a verdict as in step 4, change no files, and return only the findings, each in the finding format above, or `No findings.` Done when every batch has returned.

5. **File the report.** Merge the batches' findings into one report in the format above; its opening line counts the whole run. Write it to `.scratch/comments-audit-<YYYY-MM-DD>.md` under the repo root, with today's date; when that file exists, add `-2`, `-3` and so on before `.md`. Done when the file holds every finding from every batch.

6. **Summarise in chat**, in this shape, with sizes and classes that have no findings left out; the findings themselves stay in the file:

   ```
   Report: `.scratch/comments-audit-2026-11-20.md` (12 files read, 15 findings)
   By fix size: trivial 10, local refactor 1, ticket 3, ADR 1
   By class: class 1: 2, class 2: 1, class 5: 1, class 7: 2, ...
   Report only: no source files were changed.
   ```
