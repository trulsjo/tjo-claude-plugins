# comments

Finds the code comments that do not earn their place and says what to do about each one.

- **`audit`** - audits the comments in a file, a folder or the whole repo against the rubric and reports each finding
  with its location, class, the quoted comment and a suggested fix, grouped by fix size (trivial,
  local refactor, ticket, ADR). It only reports; it changes no source files.

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

A whole-repo audit ("audit the comments in the whole repo"), or a path with more than 20 files,
splits the files into batches of up to 8, one sub-agent each. The merged report goes to
`.scratch/comments-audit-<YYYY-MM-DD>.md` in the repo, and chat shows the counts by class and fix
size with the file's path. That file is the only one the run writes.

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
