---
type: regex
pattern: '^[ \t]*#{1,6}[ \t]*(?:Trivial|Local refactor|Ticket|ADR|Applied)\b|^(?![^\n]*\b(?:kept|keeps|keep|would|otherwise|alone|candidates?)\b)[ \t]*(?:[-*]|\d+[.)])[ \t]+[^\n]*\bclass\s*\d+\b'
flags: mi
match: not_contains
---
