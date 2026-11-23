---
type: regex
target: {source: file, path: src/cart.ts}
pattern: '//\s*(const|return) euros'
match: not_contains
---
