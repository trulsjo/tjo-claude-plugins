# comments

Finds the code comments that do not earn their place and says what to do about each one.

- **`audit`** - audits the comments in a file or folder against the rubric and reports each finding
  with its location, class, the quoted comment and a suggested fix, grouped by fix size (trivial,
  local refactor, ticket, ADR). It only reports; it changes no files.
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
| `audit-safety` | "clean up" with Edit, Write and Bash granted: no Edit or Write call, no Bash call that files an issue or writes an ADR |
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
- `--max-cost-usd`: a cost cap for the whole run. A full run costs about $2.50 (measured 2026-11).
- `--ablation none`: skips the arm without the plugin, which halves the cost. Drop it to see each
  case's delta against no plugin.
- `--model`, `--judge-model`: pinned so results compare across runs.
- `--scaffold`: runs each case's `scaffold.sh`; without it the workspaces are empty.
- `--allow-tools Edit Write Bash`: the safety case needs them granted; the other cases pass with them too.
- `--no-publish`: keeps the report local. Results go to `evals/results/` (git-ignored).

Add `--case <name> --runs 1` while working on one case. The first run in an untrusted folder asks to trust it; pass
`--trust-plugin` when running without a terminal.
