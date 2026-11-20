---
name: audit
description: Comment hygiene audit - report which code comments in a file, a folder or the whole repo to delete, move or replace with code, by the comment rubric, grouped by fix size. Use only when the user's request names comments - auditing or cleaning up comments, comment noise, stale comments, untracked TODOs. Code reviews, bug hunts and refactoring requests that do not mention comments are out of scope.
---

# audit

A **report-first** audit. Every comment in scope is judged against the rubric, and each one that does not earn its place becomes a finding with a class and a fix. Files change, and tickets are filed, only through **Confirm and apply** below: after the user answers the report's offer with a yes, when the request carries `--fix`, or when the request itself says yes to the tickets or ADRs. Any other request, "clean up" included, ends at the report. The only other file a run writes is a repo run's report under `.scratch/`. Creating an ADR folder takes a yes of its own, to the question `Create docs/adr/ for these ADRs?`: **a yes to the ADRs never covers creating the folder.**

## Steps

1. **Load the rubric.** Read `${CLAUDE_PLUGIN_ROOT}/rubric.md`. It holds the classes, the keep list, the fix sizes and the scope rules; it is the only source of the rules. Done when you have read the whole file.

2. **Fix the scope.** The target is the path the user named (a file or a folder, recursively), or the whole repo when the user asks for it; with neither, ask for a path. List every file in it with the Glob tool (`**/*`), not a shell command or an extension list of your own. Drop only dependency and build output (`node_modules`, `vendor`, `dist`, `build`, `.git`), Markdown and other prose documents, and binary files; everything else stays, because the rubric's scope covers shell scripts and config files (`.sh`, `.yaml`, `.toml`, `.ini` and similar) as well as source code. Done when you have the file list. A whole-repo target, or a list of more than 20 files, makes this a **repo run**: after step 3, follow [Repo runs](#repo-runs) in place of steps 4 to 8.

3. **Read the repo's standards.** Search the repo for files that document how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, style guides under `docs/`). Note every rule that speaks about comments or API docs. Done when you can name each such rule, or know there are none.

4. **Judge every comment.** Read each file in full. For each comment, decide: on the keep list, or one class from the rubric. A comment that a repo rule from step 3 requires or allows is kept: the repo wins. Done when every comment in every listed file has a verdict.

5. **Apply with `--fix`.** When the request carries `--fix`, apply the trivial findings now, by **Confirm and apply**, without asking. Without `--fix`, skip this step. Done when every trivial finding is applied or marked why not, or the step was skipped.

6. **Place the drafts.** When step 4 found ticket or ADR findings, work out where each would go, by [Tickets and ADRs](#tickets-and-adrs). Done when every ticket draft names its tracker and labels (or says it stays in the report), and every ADR draft has its file path and one status: **ready** (the ADR folder exists) or **waiting** (it does not; only a yes to `Create docs/adr/ for these ADRs?` makes it ready).

7. **Act on a yes in the request.** When the request itself says yes to the tickets or the ADRs, create them now by [On confirmation](#on-confirmation); otherwise skip this step. A yes to the ADRs writes the **ready** ADRs only. A **waiting** ADR stays a draft whatever the request said, because a yes to the ADRs never covers creating the folder: where decisions live is the user's choice of repo structure, which a yes to the ADRs does not make. For it this turn runs no `mkdir` and writes no file, and the report asks `Create docs/adr/ for these ADRs?`. Done when each confirmed ticket is filed, each ready ADR written, and each waiting ADR untouched, or the step was skipped.

8. **Write the report** in chat, in the format below. Done when every finding from step 4 is in it, under `### Applied` or its fix size, with what step 7 created.

## Report format

Groups in this order, each a heading, empty groups left out: `### Trivial`, `### Local refactor`, `### Ticket`, `### ADR`. Each finding:

```
- `src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: delete the comment.
```

- **Fix** follows the class's default action and names the concrete change: the new name for a rename, the function to extract, the link to add.
- A local refactor carries the patch as a diff block: the rename or extract, and the removal of the comment it makes unnecessary. Ticket and ADR findings carry the drafts described in [Tickets and ADRs](#tickets-and-adrs).

Open the report with one line: the scope, the number of files read, and the finding count per class. With no findings the report is that line and `No findings.`

When fixes were applied, an `### Applied` group comes first. Its entries keep the finding format with `Applied:` in place of `Fix:`, naming the change made: for an ADR the file written, for a ticket its number or URL. Findings not applied stay in their fix-size group; one that could not be applied says why on a `Not applied:` line.

Close with one line:

- Nothing applied: `Report only: no files were changed.` When trivial findings exist, add the offer: `Reply "yes" to apply the N trivial fixes, or name the ones to apply.`
- Fixes applied: `Applied N fixes in M files; nothing else was changed.`

When ticket or ADR drafts remain, follow it with their offer: how many tickets would be filed where, how many ADRs would be written, and that a yes to them creates them. With no ADR folder, the offer ends with the question `Create docs/adr/ for these ADRs?`

## Confirm and apply

How a finding goes from the report into the code. Three things start it: the user's reply to the report's offer, `--fix` (step 5), or a request that says yes to the tickets or ADRs (step 7).

1. **Pick the findings.** A bare yes ("yes", "apply them", "go ahead") covers every trivial finding in the last report. A reply that names findings, by location, quoted comment or kind ("file the tickets", "write the ADRs"), covers those. `--fix` covers every trivial finding of this run. Other replies are not a yes: answer them and change nothing. Done when you have the list of findings to apply, each with its fix size.

2. **Apply each finding** by its fix size:

   | Fix size | How it is applied |
   |---|---|
   | trivial | The edit below. Comment text only, so no typecheck or test run. |
   | local refactor | The refactor below, one finding at a time, each guarded by the repo's checks. |
   | ticket | Filed by [On confirmation](#on-confirmation). |
   | ADR | Written by [On confirmation](#on-confirmation), into an ADR folder that already exists. With none, not applied: the report asks `Create docs/adr/ for these ADRs?` and nothing is created. |

   `--fix` and a bare yes reach the trivial row only. Any other row is reached only by a reply or request that names that finding or its kind.

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

3. **Report.** Under `--fix` or a yes in the request, return to step 8. After a reply, write the report again in the format above, with the applied findings under `### Applied`. Done when every finding of the last report appears once, applied or not.

## Tickets and ADRs

Ticket and ADR findings are **drafts** until the user confirms them by name or kind. A yes covers only what it names: a yes to the ADRs files no ticket.

### Where a ticket goes

Take the first that applies:

1. **Tracker doc.** The repo documents its issue tracker (a doc such as `docs/agents/issue-tracker.md`, often named from `CLAUDE.md` or `AGENTS.md`). File the ticket the way it says. Labels come from its triage-label doc: the label it maps to the `needs-triage` role, under the repo's own name for it.
2. **GitHub remote.** No tracker doc, and `git remote -v` (or `.git/config`) shows a `github.com` remote: file it with `gh issue create --title ... --body ...`. Add `--label needs-triage` only when `gh label list` shows the repo has that label.
3. **Neither.** The draft stays in the report; say no tracker was found.

A ticket draft has a title, a body of a few sentences (the work, why it matters, the location and the quoted comment), and a line naming the destination and labels, e.g. `Files to: GitHub example/shop via gh, label triage/new`.

### Where an ADR goes

The repo's ADR folder: `docs/adr/`, or the folder of numbered decision records the repo already keeps. Find it with Glob from the repo root (`docs/adr/*.md`, then `**/adr/*.md` and `**/decisions/*.md`); it exists when a pattern matches. Name the file `NNNN-<slug>.md`, one above the highest number there. The content follows the domain-modeling ADR format:

```md
# {Short title of the decision}

{1-3 sentences: the context, what was decided, and why.}
```

Add a `## Considered Options` section only when the rejected option is worth remembering. The draft also shows the pointer that replaces the decision comment: one line in the file's comment syntax, e.g. `// Decision: docs/adr/0002-static-zone-rate-table.md`.

With no ADR folder, draft the path as `docs/adr/0001-<slug>.md` and ask whether to create `docs/adr/`. Only a yes to that question creates the folder; a yes to writing ADRs does not answer it.

### On confirmation

- **ADR**: with no ADR folder, the ADR waits: the folder, the file and the comment stay untouched until the user answers yes to creating the folder. With the folder in place, write the file, then replace the decision comment with its pointer. Report the path.
- **Ticket**: create it at its destination, then add its reference to the TODO (`TODO(#57): support express shipping`). Report the number or URL. When creation fails (no login, no network), keep the draft in the report with the error, and leave the TODO as it was.

## Repo runs

A repo run splits the judging across sub-agents and files the report instead of printing it. It does not take `--fix`: it ends at the summary, and a yes to the summary's offer applies the filed report's trivial findings by **Confirm and apply**.

R1. **Fan out.** Split the file list into batches of up to 8 files, keeping a folder's files together. Start one sub-agent per batch, all in one message. Give each: the rubric path `${CLAUDE_PLUGIN_ROOT}/rubric.md`, its batch's file paths, the repo rules from step 3, and this task: read the rubric and each file in full, give every comment a verdict as in step 4, change no files, and return only the findings, each in the finding format above, or `No findings.` Done when every batch has returned.

R2. **File the report.** Merge the batches' findings into one report in the format above; its opening line counts the whole run. Place its ticket and ADR drafts as step 6 does. Write it to `.scratch/comments-audit-<YYYY-MM-DD>.md` under the repo root, with today's date; when that file exists, add `-2`, `-3` and so on before `.md`. Create the file with the Write tool alone: Write creates `.scratch/` when it is missing. Never run `mkdir` or any other shell command to make the folder, and never write the report anywhere outside `.scratch/`. Done when the file holds every finding from every batch.

R3. **Summarise in chat**, in this shape, with sizes and classes that have no findings left out; the findings themselves stay in the file:

   ```
   Report: `.scratch/comments-audit-2026-11-20.md` (12 files read, 15 findings)
   By fix size: trivial 10, local refactor 1, ticket 3, ADR 1
   By class: class 1: 2, class 2: 1, class 5: 1, class 7: 2, ...
   Report only: no source files were changed.
   ```

   When trivial findings exist, end with the offer line from the report format.
