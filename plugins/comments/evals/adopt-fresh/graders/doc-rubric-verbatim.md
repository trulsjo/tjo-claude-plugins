---
type: regex
target: {source: file, path: docs/agents/comment-standards.md}
pattern: '\n# Coding standard: comments\r?\n[\s\S]*\n\| 7 \| Commented-out code \| Code disabled by commenting it out\. \| Delete; git keeps it\. \| trivial \|\r?\n[\s\S]*\n- \*\*ADR\*\*: a decision to record\. Offered as a drafted ADR plus the one-line pointer that replaces the comment\.\r?\n'
---
