---
name: audit
description: Comment hygiene audit - report which code comments in a file, a folder, the whole repo, a diff or a pull request to delete, move or replace with code, by the comment rubric, grouped by fix size. Use only when the user's request names comments - auditing or cleaning up comments, comment noise, stale comments, untracked TODOs.
---

# audit

A **report-first** audit. Every comment in scope is judged against the rubric, and each one that does not earn its place becomes a finding with a class and a fix. Files change, and tickets are filed, only through **Confirm and apply** below: after the user answers the report's offer with a yes, or when the request carries `--fix` on a diff run or after step 2 wrote `Run type: path run` (on a repo run `--fix` is not taken and nothing is edited this turn). Any other request, "clean up" included, ends at the report. Tickets and ADRs are created only after the user has seen their drafts, by [Tickets and ADRs](#tickets-and-adrs). The only other file a run writes is a repo run's report under `.scratch/`.

## Steps

1. **Load the rubric.** Read `${CLAUDE_PLUGIN_ROOT}/rubric.md`. It holds the classes, the keep list, the fix sizes and the scope rules; it is the only source of the rules. Done when you have read the whole file.

2. **Fix the scope.** The target is what the user named: a pull request (a number, `#12` or a PR URL), a path that exists (a file or a folder, recursively), the whole repo when the user asks for it, or else a git ref. For a PR or a ref, follow [Diff scope](#diff-scope) in place of the rest of this step. With no target, ask for a path. List every file in it with the Glob tool (`**/*`), not a shell command or an extension list of your own. Drop only dependency and build output (`node_modules`, `vendor`, `dist`, `build`, `.git`), Markdown and other prose documents, and binary files; everything else stays, because the rubric's scope covers shell scripts and config files (`.sh`, `.yaml`, `.toml`, `.ini` and similar) as well as source code. Then decide the run type and write it, before you read any file in the list. Take the target from the user's own message, not only from the skill's arguments, which may have dropped it. It is a **path run** only when the message names a path or file that exists and the list holds 20 files or fewer; a path written as a path counts, `.` and `./` included, even when it is the repo root. Everything else is a **repo run**: a request in words for the whole repo ("the whole repo", "the codebase", "everything"), however few files the repo holds, or a list of more than 20 files. Write exactly one of these lines as your first words to the user, quoting the target as the message names it:
   - `Run type: repo run (target: "<the user's words>", N files). The report goes to .scratch/; --fix is not taken.`
   - `Run type: path run (target: "<the path the user named>", N files).`

   A path-run line with no path quoted from the message is wrong: write the repo-run line instead.

   A repo run follows [Repo runs](#repo-runs) after step 3, in place of steps 4 to 7, whatever the repo's size: do not judge a small repo yourself instead of fanning out. Done when every file under the path is either on your list or dropped by one of these rules, and the run-type line is written.

3. **Read the repo's standards.** Search the repo for files that document how code should be written, with one Glob call per pattern, from the repo root, never several names in one pattern: `CODING_STANDARDS.md`, `CONTRIBUTING*`, `CLAUDE.md`, `AGENTS.md`, `docs/**/*.md`. Read each file found that documents how code should be written (under `docs/`, a style guide or coding standard, not an ADR). Do not say there are no repo standards until all five Globs have run. Note every rule that speaks about comments or API docs. Done when you can name each such rule, or know there are none.

4. **Judge every comment.** Read each file in full. For each comment, decide: on the keep list, or one class from the rubric. A comment that a repo rule from step 3 requires or allows is kept: the repo wins. When a rule requires doc comments, it keeps each such doc comment whole, its summary line included: do not split it into a required part that stays and a class-10 part that goes. A class 3 workaround whose cause lies outside the files in scope (a caller in another folder, or one this repo does not hold) is a **ticket**, never a local refactor: removing the workaround while its cause stands brings the bug back, so no patch is offered for it. Its draft names the cause, and the file that holds it when known, as the work to do first, and the workaround's removal as the step after. Done when every comment in every listed file has a verdict.

5. **Apply with `--fix`.** Only after a `Run type: path run` line, or on a diff run whose files are the working tree's (see [Diff scope](#diff-scope) for a PR). A repo run never reaches this step, so a whole-repo request with `--fix` edits nothing. When the request carries `--fix`, apply the trivial findings now, by **Confirm and apply**, without asking. Without `--fix`, skip this step. Done when every trivial finding is applied or marked why not, or the step was skipped.

6. **Place the drafts.** When step 4 found ticket or ADR findings, work out where each would go, by [Tickets and ADRs](#tickets-and-adrs). They stay drafts this turn, whatever the request said: a request that says "write the ADRs", "file the tickets" or "point the comments at them" gets the drafts and their offer, and this turn writes no ADR, creates no folder, files no ticket and edits no decision comment or TODO. The user asked before seeing the drafts, so that is not a yes to them. Done when every ticket draft names its tracker and labels (or says it stays in the report), and every ADR draft has its file path and one status, **ready** or **waiting**, by [The ADR folder](#the-adr-folder).

7. **Write the report** in chat, in the format below. Done when every finding from step 4 is in it, under `### Applied` or its fix size.

## Diff scope

A ref or a PR scopes the audit to the **changed comment lines**: comments on the `+` lines of the diff, in files the rubric's scope covers. Context lines and `-` lines are outside the scope, even inside a hunk. Steps 3 to 7 then run as usual, judging only the comments in scope; the rest of each file is context for the verdict. A diff run reports in chat whatever its size: it is never a repo run.

1. **Get the diff** from the one command for the target. When it fails, the audit ends there with that target's message, and nothing is classified: the user named this ref or PR, so no other base or local branch stands in for it, and the files are never read whole in the diff's place. A command fails when it exits non-zero, whatever it prints. Done when you hold the diff text, or have stopped.
   - Ref: `git rev-parse --verify --quiet "<ref>^{commit}"` checks it; on failure the message is `<ref> is not a ref in this repo; nothing was audited.` Then `git diff --merge-base <ref>`: the change since the branch left the ref, uncommitted edits included; when it fails, the message is `Could not get the diff since <ref>: <its error>. Nothing was audited.`
   - PR: the diff and the files come from one snapshot of the PR, so a push during the run cannot pair old hunks with a newer head. The PR's repository is the one its URL names (`https://github.com/<owner>/<repo>.git`) when the user gave a URL, else `origin`'s (`git remote get-url origin`); every command below uses that one repository, never another remote. Run, in order: `gh pr view <number> --repo <owner>/<repo> --json baseRefName --jq .baseRefName` for the base branch; `git fetch <repository> <base branch>`, then `git rev-parse FETCH_HEAD`, the **base commit**; `git fetch <repository> pull/<number>/head`, then `git rev-parse FETCH_HEAD`, the **head commit**. The diff is `git diff <base commit>...<head commit>`, and every later step names these two SHAs, never a ref that can move. When any of these commands fails, the message is `Could not fetch the diff of PR #<number>: <that command's error>. Nothing was audited.`
2. **Stop on an empty diff**: the diff command piped to `wc -l` prints `0`. An empty diff is the answer for this base: do not look for changes anywhere else (no `git log`, `git show`, other commits or the working tree). Stop with `The diff since <ref> is empty; nothing was audited.` (for a PR: `PR #<number> has an empty diff; nothing was audited.`). A diff with changes but no changed comment lines is not empty: it gets the normal report with `No findings.`
3. **Widen with `--touched`** when the user passes it or asks for touched code: the scope also takes every comment already inside a **touched function**: the innermost function or method that holds a `+` or `-` line, its doc comment included. Functions the diff does not touch stay outside. Done when you can name each touched function.

Locations in the report are line numbers in the new version of the file. For a PR, read that version at the head commit: `git show <head commit>:<path>`.

Edits go to the working tree, so a PR run takes `--fix` only when the checkout is the audited head: `git rev-parse HEAD` equals the head commit, and `git status --porcelain -- <each file to edit>` prints nothing, so the working tree holds the audited content. Otherwise step 5 is skipped, and the report offers nothing that would edit the working tree: the closing line carries no trivial offer, and the ticket and ADR offer leaves the ADRs out (their drafts stay in the report, and the offer speaks of the tickets alone). In the trivial offer's place stands `--fix was not taken: the checkout is not PR #<number>'s head, or has uncommitted changes to the files it would edit.` when the request carried `--fix`, and `No fixes are offered: the checkout is not PR #<number>'s head, or has uncommitted changes to the files it would edit.` when it did not. A yes to the trivial fixes, a local refactor or an ADR is refused with that line; a yes to the tickets is still taken, but only the issue is created: the TODO in the working tree is left as it is, and the report gives, for each ticket, the line to add on the PR's branch (`TODO(#57): support express shipping`). A ref run's files are the working tree's, so it takes `--fix` as a path run does.

## Report format

After the run-type line from step 2, the reply is the report alone (on a repo run, the summary alone): judge in silence, and once the last file is read, the first text you write is the report's opening line. No notes on the steps come before it, no step headings ("Step 3 — Repo rules"), no repo rules restated and no comment-by-comment verdicts ("class 10 under the rubric alone, but kept"). The report lists findings only: verdicts on kept comments stay silent, and a class is named only on a finding. One exception: when a repo rule from step 3 keeps comments the rubric alone would flag, a `Kept by repo rules` line follows the findings (or `No findings.`), then a bullet per such comment with its location and the rule's file, as ``- `lib/orders.rb:14` - kept by the rule in CONTRIBUTING.md``. Those bullets name no class, not even the one the rubric alone would give ("would be class 10", "class 10 on its own"): the location and the rule's file are the whole bullet. They are not findings and do not count in the opening line.

Groups in this order, each a heading, empty groups left out: `### Trivial`, `### Local refactor`, `### Ticket`, `### ADR`. Each finding:

```
- `src/cart.ts:12` - class 1 (narrates the how)
  > // loop over the items and add up price times quantity
  Fix: delete the comment.
```

- **Fix** follows the class's default action and names the concrete change: the new name for a rename, the function to extract, the link to add. For a move into the API doc, the Fix shows the doc comment it would write: the whole comment's words, only the markers changed (for `// Seats still free at the venue, never below 0.` the Fix reads ``Fix: move into the API doc as `/** Seats still free at the venue, never below 0. */`.``), never a part of it or a summary, so a yes applies exactly that text.
- A local refactor carries the patch as a diff block: the rename or extract, and the removal of the comment it makes unnecessary. Build it from the file as read: each `-` line is a line of the file copied character for character, never one written from memory, and the `+` lines change every use of a renamed name in the function, not only its declaration. Every line between the first and last changed line that stays as it is appears as a context line (a leading space), so the hunk matches the file line for line. Each changed line's `-` and `+` stand together at its place in the file, and each context line appears once:

  ```diff
  -  // s is the number of seats still free at the venue
  -  const s = maxSeats - booked;
  +  const freeSeats = maxSeats - booked;
     // The venue's fire permit caps the hall at maxSeats.
  -  return s > 0;
  +  return freeSeats > 0;
  ```

- Ticket and ADR findings carry the drafts described in [Tickets and ADRs](#tickets-and-adrs).

Open the report with one line: the scope, the number of files read, and the finding count per class. With no findings the report is that line, then `No findings.` on a line of its own, then the kept list if there is one:

```
`lib/`, 3 files read, 0 findings.

No findings.

Kept by repo rules
- `lib/orders.rb:14` - kept by the rule in CONTRIBUTING.md
```

When fixes were applied, an `### Applied` group comes first. Its entries keep the finding format with `Applied:` in place of `Fix:`, naming the change made: for an ADR the file written, for a ticket its number or URL. Findings not applied stay in their fix-size group; one that could not be applied says why on a `Not applied:` line.

Close with one line:

- Nothing applied: `Report only: no files were changed.` When trivial findings exist, add the offer: `Reply "yes" to apply the N trivial fixes, or name the ones to apply.`
- Fixes applied: `Applied N fixes in M files; nothing else was changed.`

When ticket or ADR drafts remain, follow it with their offer: how many tickets would be filed where, how many ADRs would be written, and that a yes to them creates them. With no tracker, the ticket part is this line, with N filled in: `No tracker was found, so the N ticket drafts stay in the report.` With a waiting ADR, the offer ends with the folder question from [The ADR folder](#the-adr-folder).

## Confirm and apply

How a finding goes from the report into the code. Two things start it: the user's reply to the report's offer, in a turn after the report, or `--fix` (step 5).

1. **Pick the findings.** A bare yes ("yes", "apply them", "go ahead") covers every trivial finding in the last report, and nothing else, even when the report's last line is the folder question: it creates no folder, writes no ADR and files no ticket. When the last report has no trivial finding, a bare yes covers nothing: change nothing, say so, and give the replies that would act on what the report offered, each one only when the report offered it: `create docs/adr/` (the folder question), `write the ADRs`, `file the tickets`, or a named refactor. A reply that names findings, by location, quoted comment or kind ("file the tickets", "write the ADRs"), covers those. `--fix` covers every trivial finding of this run. Other replies are not a yes: answer them and change nothing. Done when you have the list of findings to apply, each with its fix size.

2. **Apply each finding** by its fix size:

   | Fix size | How it is applied |
   |---|---|
   | trivial | The edit below. Comment text only, so no typecheck or test run. |
   | local refactor | The refactor below, one finding at a time, each guarded by the repo's checks. |
   | ticket | Filed by [On confirmation](#on-confirmation). |
   | ADR | Written by [On confirmation](#on-confirmation) when **ready**. A **waiting** ADR is not applied, by [The ADR folder](#the-adr-folder). |

   `--fix` and a bare yes reach the trivial row only. Any other row is reached only by a reply or request that names that finding or its kind.

   The trivial edit: re-read the file, then make one Edit per finding.
   - **Delete**: remove the comment's lines whole, leaving the code and its indentation as they were.
   - **Move into the API doc**: copy the comment's words into the function's doc comment word for word, changing only the comment markers (`//` becomes `/** ... */`, `#` becomes a docstring): do not shorten, reword or summarise them, so every fact it states (each input it names, each limit, each error) arrives intact. Use the file's doc-comment convention (JSDoc above a TypeScript function, a docstring in Python); create the doc comment when there is none. Then delete the inline comment.
   - **Rewrite** (class 6 fix, class 10 rewrite): replace the comment text with the fix the report gave.
   - A fix that needs a fact the code does not hold, such as the upstream link for class 4, is not applied: it stays in the report with `Not applied: needs <the fact>`.

   The local refactor:
   - **Find the checks**, once, before the first refactor: the repo's typecheck and test commands. Search for them with one Glob call per file, from the repo root, never several names in one pattern: `package.json`, `Makefile`, `pyproject.toml`, `tox.ini`, `.github/workflows/*.yml`, `README*`, `CONTRIBUTING*`. Read each file found for its typecheck and test commands (`package.json` scripts, `Makefile` targets, a `[tool.pytest...]` table). Do not say there are no checks until all seven Globs have run. Run the commands found. When they already fail, no refactor is applied: each stays in the report with `Not applied: the checks fail before any change (<command>)`. When there are none, refactors are applied unchecked and each `Applied:` line ends `unchecked: no typecheck or tests found`.
   - **Apply the patch**: re-read the file, make the report's patch with Edit, update every reference to the renamed or extracted name that a search of the repo finds, and remove the comment. Keep the original text of every line you change.
   - **Run the checks.** Green: the refactor stays, and its `Applied:` line names the commands that passed. Red: Edit every changed line back to its original text, re-read each file to confirm it matches its original, and leave the finding in its group with this line, word for word with the blanks filled: `Not applied: <command> failed after the change (<first failing test or error>); reverted.` Your own reading of why it failed may follow on the next line, never in its place. The checks are the guard: a red check is answered by reverting, never by editing tests or other code to make it pass.

   Done when every picked finding is applied or marked `Not applied` with its reason, and re-reading each changed file shows only comment lines changed, plus the patch and its references for each kept refactor.

3. **Report.** Under `--fix`, return to step 6. After a reply, write the report again in the format above, with the applied findings under `### Applied` and every other finding under its own fix-size heading, as in the last report: local refactors with their diffs, tickets and ADRs with their drafts. A sentence about them is not enough. Done when every finding of the last report appears once, applied or not.

## Tickets and ADRs

Ticket and ADR findings are **drafts** until the user confirms them by name or kind, in a reply to the report that showed them. On a repo run that report is the file under `.scratch/`, which holds every draft in full, and the summary names it. A yes the request already carried ("audit src/ and write the ADRs") comes before the user has seen any draft, so it confirms nothing: that turn files no ticket and writes no ADR, and the report shows the drafts with their offer. A yes covers only what it names: a yes to the ADRs files no ticket.

### Where a ticket goes

Take the first that applies:

1. **Tracker doc.** The repo documents its issue tracker (a doc such as `docs/agents/issue-tracker.md`, often named from `CLAUDE.md` or `AGENTS.md`). File the ticket the way it says. Labels come from its triage-label doc: the label it maps to the `needs-triage` role, under the repo's own name for it.
2. **GitHub remote.** No tracker doc, and `git remote -v` shows a `github.com` remote (without Bash, Read `.git/config`; never say there is no remote without having checked one of the two): file it with `gh issue create --title ... --body ...`. Add `--label needs-triage` only when `gh label list` shows the repo has that label.
3. **Neither.** The draft stays in the report; say no tracker was found.

A ticket draft has a title, a body of a few sentences (the work, why it matters, the location and the quoted comment), and a line naming the destination and labels, e.g. `Files to: GitHub example/shop via gh, label triage/new`.

### Where an ADR goes

The repo's ADR folder: `docs/adr/`, or the folder of numbered decision records the repo already keeps. Find it with Glob from the repo root (`docs/adr/*.md`, then `**/adr/*.md` and `**/decisions/*.md`); it exists when a pattern matches. Name the file `NNNN-<slug>.md`, one above the highest number there, and number a report's drafts on from there in report order, so no two drafts share a number. The content follows the domain-modeling ADR format:

```md
# {Short title of the decision}

{The decision comment's words, comment markers removed.}
```

The ADR keeps every fact of the decision comment it replaces: each option it names and each reason it gives, so the pointer loses nothing. It adds no fact of its own: every claim in it is stated by that comment, so no speed, cost or process the source does not give. So the ADR's text under its title is the decision comment itself: its words copied as they stand, only the comment markers removed and its lines joined into sentences, as the move into an API doc copies them. Do not recast it ("X was chosen over Y", "Y took two seconds, so X"), change a number's form ("two seconds" stays "two seconds", not "2 seconds") or summarise it. Nothing follows that text: no `## Considered Options` or other section, as the comment already names each option and its reasons.

The draft also shows the pointer that replaces the decision comment: one line in the file's comment syntax, e.g. `// Decision: docs/adr/0002-static-zone-rate-table.md`.

### The ADR folder

An ADR draft is **ready** when the ADR folder exists and **waiting** when it does not. Waiting drafts take the paths `docs/adr/0001-<slug>.md`, `docs/adr/0002-<slug>.md` and on, in report order, and the report's offer ends with the question `Create docs/adr/ for these ADRs?`

**A yes to the ADRs never covers creating the folder.** Where decisions live is the user's choice of repo structure, so only a yes to that question creates `docs/adr/`, and only a reply that names the folder ("create the folder", "yes, create docs/adr/") is one: a bare yes answers the trivial offer, by [Confirm and apply](#confirm-and-apply). Until that yes, a waiting ADR's folder, file and decision comment stay untouched: no `mkdir`, no file written, no edit. After it, create the folder; the drafts are then ready, and a yes to the ADRs, in the same reply or a later one, writes them.

### On confirmation

- **ADR**: a ready ADR: write the file, then replace the decision comment with its pointer. Report the path. A waiting ADR stays a draft, by [The ADR folder](#the-adr-folder).
- **Ticket**: create it at its destination, then add its reference to the TODO (`TODO(#57): support express shipping`), except on a PR run whose checkout is not the audited head: `git rev-parse HEAD` is not the head commit, or `git status --porcelain -- <the TODO's file>` prints a line (see [Diff scope](#diff-scope)). There the TODO stays as it is and the report gives the line to add. Report the number or URL. When creation fails (no login, no network), keep the draft in the report with the error, and leave the TODO as it was.

## Repo runs

A repo run splits the judging across sub-agents and files the report instead of printing it. It does not take `--fix`: it ends at the summary, and a yes to the summary's offer applies the filed report's findings it names (a bare yes: the trivial ones) by **Confirm and apply**.

R1. **Fan out.** Split the file list into batches of up to 8 files, keeping a folder's files together. Start one sub-agent per batch, all in one message. Give each: the rubric path `${CLAUDE_PLUGIN_ROOT}/rubric.md`, this skill's path `${CLAUDE_PLUGIN_ROOT}/skills/audit/SKILL.md`, its batch's file paths relative to the repo root (`shop/src/dates.ts`), the repo rules from step 3, and this task: read the rubric, then this skill's Report format and Tickets and ADRs sections, then each file in full; give every comment a verdict as in step 4, change no files, and return only the findings, each built as Report format says (its Fix, a local refactor's patch by the patch rules and their example, a ticket's or ADR's draft by Tickets and ADRs), each finding's file named by its path exactly as given, or `No findings.`; then, when a repo rule keeps comments in its batch that the rubric alone would flag, the `Kept by repo rules` line and a bullet per such comment, as Report format says. Point to those sections by the path rather than restating them: a restatement in the prompt drops their rules (a lead that wrote "include a diff block" left out the patch rules, and the sub-agent's patch moved the `+` lines past the line kept between the changes). Done when every batch has returned.

R2. **File the report.** Merge the batches' findings into one report in the format above; its opening line counts the whole run. Merge the batches' kept bullets too, under one `Kept by repo rules` line after the findings (or `No findings.`), each as its batch gave it; they are not findings and do not count in the opening line. Place its ticket and ADR drafts as step 6 does. Write it to `.scratch/comments-audit-<YYYY-MM-DD>.md` under the repo root, with today's date; when that file exists, add `-2`, `-3` and so on before `.md`. Create the file with the Write tool alone: Write creates `.scratch/` when it is missing. Never run `mkdir` or any other shell command to make the folder, and never write the report anywhere outside `.scratch/`. Done when the file holds every finding and every kept bullet from every batch.

R3. **Summarise in chat**, in this shape, with sizes and classes that have no findings left out. The findings themselves stay in the file: the chat reply has no finding lines, no `Fix:` lines, no diffs and no draft text, however few the findings are.

   ```
   Report: `.scratch/comments-audit-2026-11-20.md` (12 files read, 15 findings)
   By fix size: trivial 10, local refactor 1, ticket 3, ADR 1
   By class: class 1: 2, class 2: 1, class 5: 1, class 7: 2, ...
   Report only: no source files were changed.
   ```

   The reply after the run-type line is these parts, in this order, each left out when it has nothing to say:
   1. The four lines above. When the request carried `--fix`, the fourth reads, word for word: `Report only: no source files were changed. A repo run does not take --fix, so nothing was applied.` Keep it even though the run-type line said so at the start: the summary is what the user reads when the run ends.
   2. The trivial offer, word for word with N filled in: `Reply "yes" to apply the N trivial fixes, or name the ones to apply.`
   3. The ticket and ADR offer, as the report format gives it: where the tickets would be filed (or that no tracker was found), how many ADRs would be written, that their drafts are in the report file, and that a yes to them creates them.
   4. For a waiting ADR, the folder question, word for word: `Create docs/adr/ for these ADRs?` It is the reply's last line.
