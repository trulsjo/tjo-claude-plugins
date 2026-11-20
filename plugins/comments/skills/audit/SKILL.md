---
name: audit
description: Comment hygiene audit - report which code comments in a file, a folder or the whole repo to delete, move or replace with code, by the comment rubric, grouped by fix size. Use only when the user's request names comments - auditing or cleaning up comments, comment noise, stale comments, untracked TODOs. Code reviews, bug hunts and refactoring requests that do not mention comments are out of scope.
---

# audit

A **report-first** audit. Every comment in scope is judged against the rubric, and each one that does not earn its place becomes a finding with a class and a fix. Files change only through **Confirm and apply** below: after the user answers the report's offer with a yes, or when the request carries `--fix`. Any other request, "clean up" included, ends at the report. The only other file a run writes is a repo run's report under `.scratch/`.

## Steps

1. **Load the rubric.** Read `${CLAUDE_PLUGIN_ROOT}/rubric.md`. It holds the classes, the keep list, the fix sizes and the scope rules; it is the only source of the rules. Done when you have read the whole file.

2. **Fix the scope.** The target is the path the user named (a file or a folder, recursively), or the whole repo when the user asks for it; with neither, ask for a path. List every file in it with the Glob tool (`**/*`), not a shell command or an extension list of your own. Drop only dependency and build output (`node_modules`, `vendor`, `dist`, `build`, `.git`), Markdown and other prose documents, and binary files; everything else stays, because the rubric's scope covers shell scripts and config files (`.sh`, `.yaml`, `.toml`, `.ini` and similar) as well as source code. Done when you have the file list. A whole-repo target, or a list of more than 20 files, makes this a **repo run**: after step 3, follow [Repo runs](#repo-runs) in place of steps 4 to 6.

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
- A local refactor carries the patch as a diff block: the rename or extract, and the removal of the comment it makes unnecessary. A ticket carries a draft (title and two-line body). An ADR carries a draft (title and the decision in one to three sentences) and the one-line pointer that replaces the comment.

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
   | local refactor | The refactor below, one finding at a time, each guarded by the repo's checks. |
   | ticket | Not applied: stays in the report. |
   | ADR | Not applied: stays in the report. |

   `--fix` and a bare yes reach the trivial row only. Any other row is reached only by a reply that names that finding.

   The trivial edit: re-read the file, then make one Edit per finding.
   - **Delete**: remove the comment's lines whole, leaving the code and its indentation as they were.
   - **Move into the API doc**: put the comment's *what* into the function's doc comment, in the file's doc-comment convention (JSDoc above a TypeScript function, a docstring in Python); create the doc comment when there is none. Then delete the inline comment.
   - **Rewrite** (class 6 fix, class 10 rewrite): replace the comment text with the fix the report gave.
   - A fix that needs a fact the code does not hold, such as the upstream link for class 4, is not applied: it stays in the report with `Not applied: needs <the fact>`.

   The local refactor:
   - **Find the checks**, once, before the first refactor: the repo's typecheck and test commands, where the repo declares them (`package.json` scripts, `Makefile`, `pyproject.toml`, `tox.ini`, CI workflows, README, CONTRIBUTING). Run them. When they already fail, no refactor is applied: each stays in the report with `Not applied: the checks fail before any change (<command>)`. When there are none, refactors are applied unchecked and each `Applied:` line ends `unchecked: no typecheck or tests found`.
   - **Apply the patch**: re-read the file, make the report's patch with Edit, update every reference to the renamed or extracted name that a search of the repo finds, and remove the comment. Keep the original text of every line you change.
   - **Run the checks.** Green: the refactor stays, and its `Applied:` line names the commands that passed. Red: Edit every changed line back to its original text, re-read each file to confirm it matches its original, and leave the finding in its group with `Not applied: <command> failed after the change (<first failing test or error>); reverted.` The checks are the guard: a red check is answered by reverting, never by editing tests or other code to make it pass.

   Done when every picked finding is applied or marked `Not applied` with its reason, and re-reading each changed file shows only comment lines changed, plus the patch and its references for each kept refactor.

3. **Report.** Under `--fix`, return to step 6. After a reply, write the report again in the format above, with the applied findings under `### Applied`. Done when every finding of the last report appears once, applied or not.

## Repo runs

A repo run splits the judging across sub-agents and files the report instead of printing it. It does not take `--fix`: it ends at the summary, and a yes to the summary's offer applies the filed report's trivial findings by **Confirm and apply**.

R1. **Fan out.** Split the file list into batches of up to 8 files, keeping a folder's files together. Start one sub-agent per batch, all in one message. Give each: the rubric path `${CLAUDE_PLUGIN_ROOT}/rubric.md`, its batch's file paths, the repo rules from step 3, and this task: read the rubric and each file in full, give every comment a verdict as in step 4, change no files, and return only the findings, each in the finding format above, or `No findings.` Done when every batch has returned.

R2. **File the report.** Merge the batches' findings into one report in the format above; its opening line counts the whole run. Write it to `.scratch/comments-audit-<YYYY-MM-DD>.md` under the repo root, with today's date; when that file exists, add `-2`, `-3` and so on before `.md`. Create the file with the Write tool alone: Write creates `.scratch/` when it is missing. Never run `mkdir` or any other shell command to make the folder, and never write the report anywhere outside `.scratch/`. Done when the file holds every finding from every batch.

R3. **Summarise in chat**, in this shape, with sizes and classes that have no findings left out; the findings themselves stay in the file:

   ```
   Report: `.scratch/comments-audit-2026-11-20.md` (12 files read, 15 findings)
   By fix size: trivial 10, local refactor 1, ticket 3, ADR 1
   By class: class 1: 2, class 2: 1, class 5: 1, class 7: 2, ...
   Report only: no source files were changed.
   ```

   When trivial findings exist, end with the offer line from the report format.
