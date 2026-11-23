---
type: regex
target: {source: file, path: CLAUDE.md}
pattern: '^#{1,6} Coding standards\s*\n(?:[^#\r\n][^\n]*\n|\r?\n)*[^#\r\n][^\n]*docs/agents/comment-standards\.md[^\n]*coding standard[^\n]*comments'
flags: mi
---
