# comments

Finds the code comments that do not earn their place and says what to do about each one.

- **`audit`** - audits the comments in a file, a folder or the whole repo against the rubric and reports each finding
  with its location, class, the quoted comment and a suggested fix, grouped by fix size (trivial,
  local refactor, ticket, ADR). It applies the trivial fixes only after a "yes" or with `--fix`, and
  files its drafted tickets or writes its drafted ADRs only after a yes to them.
- **`adopt`** - installs the rubric in a repo as its coding standard for comments, at
  `docs/agents/comment-standards.md`, and links it from CLAUDE.md, so code reviews enforce it.

Install:

```
claude plugin marketplace add trulsjo/tjo-claude-plugins
claude plugin install comments@tjo-claude-plugins
```

## The rubric

[`rubric.md`](rubric.md) is the one source of the rules: 10 comment classes with their default
action and fix size, the keep list (contract API docs, linked upstream workarounds, constraint-whys,
license headers, tool directives, ticketed TODOs) and the scope (any language's comments, shell and
config files; not Markdown). `audit` reads it at run time. Where a repo's own coding standards
disagree with it, the repo wins.

## audit

Ask "clean up the comments in src/" or "audit the comments in lib/parser.py", or run
`/comments:audit <path>`. A code review or bug hunt that does not mention comments does not fire it.

The report ends by offering the trivial fixes (deletions, added links, moves of *what* text into
the function's API doc). Reply "yes" to apply them all, or name the ones to apply. Run
`/comments:audit <path> --fix` to apply them without the offer. Neither applies local refactors,
files tickets or writes ADRs: those wait for a reply that names them (below). Applied fixes are
listed under `Applied`.

### Tickets and ADRs

Untracked TODOs and large own-code workarounds are drafted as tickets; decision comments as ADRs.
Nothing is created until you say yes, after the report or in the request ("audit src/ and write
the ADRs").

| Repo has | Tickets go to |
|---|---|
| an issue-tracker doc (e.g. `docs/agents/issue-tracker.md`) | the tracker it describes, labelled from its triage-label doc |
| no tracker doc, a GitHub remote | `gh issue create`, labelled `needs-triage` only if that label exists |
| neither | nowhere: the drafts stay in the report |

ADRs go to `docs/adr/NNNN-slug.md` (the next number), and the comment shrinks to a one-line
pointer to the file. With no ADR folder, `audit` asks before creating one.

A local refactor (a rename or extract that makes a comment unnecessary) comes with its patch, and
is applied only when you name it in your reply. The repo's typecheck and tests are run before the
first refactor and after each one, when the repo declares them (`package.json` scripts, `Makefile`,
`pyproject.toml`, `tox.ini`, CI workflows, README, CONTRIBUTING). A refactor that turns them red is
reverted, and the report says which check failed.

A whole-repo audit ("audit the comments in the whole repo"), or a path with more than 20 files,
splits the files into batches of up to 8, one sub-agent each. The merged report goes to
`.scratch/comments-audit-<YYYY-MM-DD>.md` in the repo, and chat shows the counts by class and fix
size with the file's path. That file is the only one the run writes; a repo run does not take
`--fix`, but a "yes" to its summary applies the report's trivial fixes.

## adopt

Ask "set up comment standards in this repo", or run `/comments:adopt`, from the repo root. It
writes two things:

- **`docs/agents/comment-standards.md`**: a line stamped with the plugin version, the rubric copied
  verbatim, and an empty `## Local rules` section. Add the repo's own comment rules under that
  heading; adopt never changes it.
- **One line in `CLAUDE.md`** under `## Coding standards` (the heading and the file are created when
  missing):

  ```
  - Comments: follow [docs/agents/comment-standards.md](docs/agents/comment-standards.md), the coding standard for code comments (say what, not how; what to keep, delete, refactor or move to an ADR).
  ```

The copy lives in the repo, so teammates and review tools get the rules without the plugin:
`mattpocock-skills:code-review` finds it in its standards search and the built-in `/code-review`
reads it through CLAUDE.md.

Running adopt again with the same plugin version changes nothing. With a newer version it replaces
everything above `## Local rules` and updates the stamp; the local rules stay as they were. A doc
stamped with a newer version than the plugin is left alone, and a doc at that path with no stamp is
replaced only after you confirm.

## Evals

The plugin is tested with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals.md).
Cases live in [`evals/`](evals); fixtures are plain files under `evals/fixtures/`, copied into each
run's workspace by the case's `scaffold.sh`.

| Case | Checks |
|---|---|
| `trigger-audit` | "clean up the comments in src/" fires `audit` |
| `trigger-unrelated` | a bug-review request fires no `comments` skill |
| `audit-ts-classes` | TypeScript fixture: no keep-list comment flagged, at least 85% of flagged comments classed right (class 1 vs 2 is a soft miss), at least 8 of 10 found, report grouped by fix size |
| `audit-negative` | every comment is on the keep list: `No findings.` |
| `audit-repo` | whole-repo run on a multi-folder fixture (TypeScript, shell, YAML, Python): merged report written to `.scratch/comments-audit-<date>.md` in the path-run format with findings from every folder, none from the clean folder or Markdown; chat shows counts by class and fix size and the path; no Edit, no Write outside `.scratch/` |
| `audit-safety` | "clean up" with Edit, Write and Bash granted: no Edit or Write call, no Bash call that files an issue or writes an ADR |
| `audit-drafts-tracker` | repo with a tracker doc, a triage-label doc and `docs/adr/`: the TODO's ticket draft follows the tracker doc and its label, the ADR draft is `docs/adr/0002-*.md`, nothing is filed or written |
| `audit-drafts-github` | GitHub remote, no tracker doc, no ADR folder: the ticket draft goes to `gh` with no forced label, the report asks before creating `docs/adr/`, nothing is filed or written |
| `audit-adr-yes` | the request says yes to the ADRs: `docs/adr/0002-*.md` is written, the decision comment becomes a pointer to it, the other findings stay unapplied, no issue is filed |
| `audit-adr-no-folder` | the request says yes to the ADRs but there is no ADR folder: it asks before creating one and writes nothing |
| `audit-fix` | `--fix`: the narrating and commented-out comments are deleted and a *what* comment moves into the API doc, without a question; refactor, ticket and ADR findings stay unapplied in the report; no issue, no ADR |
| `audit-confirm` | the same checks after a "yes" to the report's offer. Resumes `history.jsonl`; re-record it with `record-history.sh` (WSL2) after changing the skill or the rubric |
| `audit-refactor-green` | Python fixture with `make test`: naming the local refactor in the reply applies the rename and removes the comment, the tests run and pass, the change is listed under `Applied`, the tests are not edited. Resumes `history.jsonl`; re-record it with `record-history.sh` after changing the skill or the rubric |
| `audit-refactor-revert` | a rename that a dynamic lookup (`getattr(handlers, "on_" + type)`) depends on: the tests fail after it, the file is reverted, the tests and the caller are not edited, the report says `Not applied` with the failing check. Resumes `history.jsonl` like the case above |
| `trigger-adopt` | "set up comment standards in this repo" fires `adopt` |
| `adopt-fresh` | first adopt: the doc has the stamp, the whole rubric and an empty `## Local rules`; CLAUDE.md gains the heading and one entry and keeps its old content |
| `adopt-existing-heading` | the entry goes under CLAUDE.md's existing coding-standards heading; no second heading |
| `adopt-no-claude-md` | with no CLAUDE.md, adopt creates it with the heading and the entry |
| `adopt-same-version` | a repo already on this version: no Edit or Write call, no Bash call that writes the doc or CLAUDE.md |
| `adopt-newer-version` | a doc stamped 0.0.1: the rubric and stamp are replaced, `## Local rules` is kept as it was, CLAUDE.md keeps one entry |

Requirements: Claude Code 2.1.269 or later, Git 2.31 or later. Run from WSL2 (or Linux): granting
Bash needs the OS sandbox (`bubblewrap` and `socat`), which native Windows does not have, and the
scaffold scripts are Bash. Runs are local only; there is no CI.

In WSL2, trim `PATH` to Linux directories first. The Bash sandbox scans every `PATH` entry, and
the Windows entries WSL2 adds under `/mnt/c` make it give up after 5 s, which fails the run:

```
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
```

From the plugin folder (`/mnt/c/.../plugins/comments` in WSL2):

```
claude plugin eval . --runs 3 --threshold 0.8 --max-cost-usd 10 --ablation none \
  --model claude-sonnet-4-6 --judge-model claude-sonnet-4-6 \
  --scaffold --no-publish --allow-tools Edit Write Bash
```

- `--runs 3 --threshold 0.8`: a case passes when it scores at least 0.8 over three runs.
- `--max-cost-usd`: a cost cap for the whole run. A full run costs over $6 (measured 2026-11).
- `--ablation none`: skips the arm without the plugin, which halves the cost. Drop it to see each
  case's delta against no plugin.
- `--model`, `--judge-model`: pinned so results compare across runs.
- `--scaffold`: runs each case's `scaffold.sh`; without it the workspaces are empty.
- `--allow-tools Edit Write Bash`: the safety, fix and confirm cases need them granted. Run
  `audit-repo` on its own with `--allow-tools Edit Write`: with Bash granted, the model tries
  `mkdir .scratch` in the read-only Bash sandbox, fails, and files the report outside `.scratch/`.
- `--no-publish`: keeps the report local. Results go to `evals/results/` (git-ignored).

Add `--case <name> --runs 1` while working on one case. The first run in an untrusted folder asks to trust it; pass
`--trust-plugin` when running without a terminal.

## code-review integration check

Eval runs load only this plugin, so they cannot show that a real review picks up the adopted
doc. [`integration/code-review.sh`](integration/code-review.sh) does, with your normal Claude Code
config:

1. builds a temporary git repo (a TypeScript file, a spec, an issue-tracker doc),
2. runs `/comments:adopt` with this folder as `--plugin-dir` and commits the result on `main`,
3. adds a narrating (class 1) comment on a branch,
4. runs `/mattpocock-skills:code-review main` through `claude -p`,
5. passes when the `## Standards` section cites `comment-standards.md` for the planted comment.

```
plugins/comments/integration/code-review.sh            # exit 0 pass, 1 finding missing, 2 setup problem
plugins/comments/integration/code-review.sh --skip-adopt   # the same repo without adopt: must fail
```

It needs `mattpocock-skills` installed and enabled, and a claude.ai subscription login: it unsets
API-key, Bedrock, Vertex and Foundry variables and stops unless `claude auth status` reports a
claude.ai login. Both runs use `--model sonnet` (change with `--model`) and a budget cap; a run
takes a few minutes. `--keep` keeps the temporary repo and the two outputs. Runs from Git Bash on
Windows, WSL2 or Linux.

Without adopt, code-review may still flag the comment from its smell baseline, but it cites no
standard; the check requires the citation.

## Release checklist

1. Run the eval suite (above) and check every case scores at least the 0.8 threshold.
2. Run `integration/code-review.sh` and check it prints `PASS`.
3. Record the date, the plugin version and the `PASS` line in the release ticket.
