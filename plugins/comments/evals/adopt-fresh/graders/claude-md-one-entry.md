---
type: regex
target: {source: file, path: CLAUDE.md}
pattern: 'comment-standards\.md[^\n]*\n[\s\S]*comment-standards\.md'
match: not_contains
---
