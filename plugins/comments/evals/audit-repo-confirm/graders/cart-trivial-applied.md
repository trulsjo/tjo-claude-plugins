---
type: regex
target: {source: file, path: shop/src/cart.ts}
pattern: 'loop over the items|//\s*(const|return) euros'
match: not_contains
---
