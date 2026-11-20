---
type: regex
target: {source: file, path: src/stock.ts}
pattern: '^\s*/\*\*(?:(?!\*/)[\s\S])*reserv(?:(?!\*/)[\s\S])*\*/\s*export function availableUnits[^{]*\{(?:(?!//)[\s\S])*$'
---
