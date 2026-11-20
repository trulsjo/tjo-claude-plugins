---
type: regex
target: {source: file, path: CLAUDE.md}
pattern: '^#{1,6} Coding standards[\s\S]*^#{1,6} Coding standards'
flags: mi
match: not_contains
---
