---
type: regex
pattern: '^[ \t]*#{1,6}[ \t]*(?:Trivial|Local refactor|Ticket|ADR|Applied)\b|^[ \t]*(?:[-*]|\d+[.)])[ \t]+(?:[*`]*[^\s`*]+:\d+[^\s`*]*[*`]*[ \t]*[-–—:][ \t]*)?\**class\s*\d+|^(?![^\n]*\bkept by\b)[ \t]*(?:[-*]|\d+[.)])[ \t]+[^\n]*\bclass\s*\d+\b'
flags: mi
match: not_contains
---
