# Coding standard: comments

A comment earns its place when it tells the reader something the code cannot: **what** a unit does and promises, or **why** a constraint exists. Comments that say **how** the next lines work, prop up a weak name, or record history belong in the code, the commit log, a ticket or an ADR instead. Most comments that stay live in API docs.

Where this repo's own documented coding standards disagree with this rubric, the repo's standard wins.

## Scope

- Every language's comment syntax: line and block comments, and the doc-comment conventions Javadoc, Doxygen, JSDoc/TSDoc, Python docstrings, C# XML doc comments and rustdoc.
- Shell scripts and config files (YAML, TOML, INI and similar) are in scope.
- Markdown and other documentation prose are out of scope.
- A public API with no doc comment is not a finding. This rubric judges the comments that exist.

## Keep list

These are never findings:

- **Contract API docs**: a doc comment that says what the unit does and promises (inputs, outputs, errors, units, side effects).
- **Upstream workarounds with a link**: class 4 comments that cite the upstream issue, version or spec section.
- **Constraint-whys**: a reason the code cannot express ("the provider rejects fractional cents", "must run before X is loaded"). A requirement set outside our code that holds by design (hardware, a protocol, a provider's rules, a resource limit) is a constraint-why and needs no link; class 4 is only for a workaround to a defect or quirk that upstream could fix.
- **License and copyright headers.**
- **Tool directives**: `eslint-disable`, `#pragma`, `# type: ignore`, `// nolint`, `# shellcheck disable` and the like.
- **Ticketed TODOs**: a TODO or FIXME that names a ticket (`TODO(#142)`, `FIXME JIRA-881`, a tracker URL).

## Classes

Each finding gets exactly one class. When a comment fits several, pick the lowest-numbered class that names its main problem.

| # | Class | Recognise it by | Default action | Fix size |
|---|---|---|---|---|
| 1 | Narrates the how | Restates what the next lines plainly do ("loop over the items and add them up"). | Delete. | trivial |
| 2 | Compensates for naming or structure | Explains what a variable, function or block means, because its name or shape does not ("d is the discount as a fraction"). | Rename or extract so the code says it, then delete. | local refactor |
| 3 | Workaround in our own code | Explains code that exists to work around another part of this codebase ("checkout retries and calls this twice, so skip duplicates"). | Refactor the cause away; a ticket when the refactor is large. | local refactor, or ticket |
| 4 | Workaround for something outside our control | Explains a workaround for an upstream bug, platform quirk or spec oddity. | Keep. Flag only when it has no link to the upstream issue, version or spec; the fix is to add one. | trivial |
| 5 | Records a decision | Says why one option was chosen over another ("we chose X over Y because ..."). | Move into an ADR and leave a one-line pointer to it. | ADR |
| 6 | Stale or lying | No longer matches the code next to it. | Fix it to match, or delete it. | trivial |
| 7 | Commented-out code | Code disabled by commenting it out. | Delete; git keeps it. | trivial |
| 8 | History or changelog | Says what changed, when or by whom ("changed in v2", "now uses X instead of Y", "added by Kim"). | Delete; history lives in commit messages. | trivial |
| 9 | TODO or FIXME with no ticket | Planned work that no ticket tracks. | File a ticket and link it from the TODO, or delete the TODO. | ticket |
| 10 | API doc that repeats the signature | A doc comment whose text adds nothing to the names and types (`@param cents the cents`). | Delete the noise, or rewrite it with what the reader cannot see. | trivial |

A comment whose real content is *what* the function does, sitting inline in the body, is moved into the function's API doc. That move is its fix, not a missing-docs finding.

## Fix sizes

- **trivial**: delete, add a link, or move text into an API doc. No behaviour changes.
- **local refactor**: rename, extract or restructure within a few functions, then delete the comment. Offered as a patch.
- **ticket**: work too large for the current change. Offered as a drafted ticket.
- **ADR**: a decision to record. Offered as a drafted ADR plus the one-line pointer that replaces the comment.
