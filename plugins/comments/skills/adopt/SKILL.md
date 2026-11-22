---
name: adopt
description: Install the comment rubric in a repo as its coding standard for comments - a versioned copy at docs/agents/comment-standards.md, linked from CLAUDE.md, so code reviews enforce it. Use when the user wants comment standards or comment rules set up or updated in a repo.
---

# adopt

Installs the plugin's rubric into the current repo as a **coding standard** that reviews can apply with no plugin installed: `mattpocock-skills:code-review` finds it in its standards search, and the built-in `/code-review` can reach it through the link in CLAUDE.md. The run is **idempotent**: a repo already on this version comes out byte-identical.

Two files are in play, both at the repo root's paths:

- **The doc**: `docs/agents/comment-standards.md`. Its first line is the stamp, then the rubric verbatim, then `## Local rules`. Everything from `## Local rules` to the end of the file belongs to the repo: adopt carries it over unchanged and never edits it.
- **The entry**: one line in `CLAUDE.md`, under a `## Coding standards` heading.

## Steps

1. **Read the sources.** Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` for `version` and `${CLAUDE_PLUGIN_ROOT}/rubric.md` in full. Done when you hold the version string and the whole rubric text.

2. **Read the repo's state.** Read `docs/agents/comment-standards.md` and `CLAUDE.md` if they exist. From the doc, take the installed version from the stamp and the local part (the `## Local rules` line through the end of the file). Done when you know, for each file, whether it exists, and for the doc, its installed version and local part.

3. **Write the doc**, by the installed version:

   | Doc state | Action |
   |---|---|
   | missing | Write stamp + blank line + rubric + blank line + `## Local rules` (heading only, nothing under it). |
   | same version as the plugin | Leave it untouched. |
   | older version | Rewrite everything above `## Local rules` as stamp + blank line + rubric + blank line; append the local part exactly as it was. |
   | newer version than the plugin | Leave it untouched and tell the user the plugin is older than the installed doc. |
   | exists with no stamp | Leave it untouched and ask the user before replacing it. |

   Write every file of this skill, the doc and `CLAUDE.md`, with the Write or Edit tool alone: Write creates `docs/agents/` when it is missing. Never run `mkdir` or any other shell command to make a folder or a file.

   The rubric goes in **verbatim**: copied character for character from `rubric.md`, from its first line to its last, never summarised or reflowed. Done when the doc matches the table's row and a fresh read shows the stamp's version equal to the plugin's (or the row said to leave it).

4. **Link it from CLAUDE.md.** When `CLAUDE.md` already mentions `docs/agents/comment-standards.md`, leave it untouched. Otherwise add the entry under the first heading whose text is `Coding standards` (any level, any case); with no such heading, append `## Coding standards` at the end of `CLAUDE.md`, after its last line and below every section it has, never before an existing heading: an Edit whose `old_string` is the file's last line, and whose `new_string` is that line, a blank line, the heading, a blank line and the entry; with no `CLAUDE.md`, create it with that heading. Existing content stays as it was. Done when `CLAUDE.md` mentions the doc on exactly one line, and that line sits under the coding-standards heading.

5. **Report** in chat: the plugin version, and for each file one of `created`, `updated from <old version>`, `unchanged`. Done when both files are named.

## Formats

Stamp, the doc's first line (`<version>` from `plugin.json`):

```
<!-- Installed by comments:adopt from the comments plugin, version <version>. Re-running adopt with a newer version replaces everything above "## Local rules"; add this repo's own rules under that heading. -->
```

Entry, placed directly under the coding-standards heading's existing lines:

```
- Comments: follow [docs/agents/comment-standards.md](docs/agents/comment-standards.md), the coding standard for code comments (say what, not how; what to keep, delete, refactor or move to an ADR).
```
