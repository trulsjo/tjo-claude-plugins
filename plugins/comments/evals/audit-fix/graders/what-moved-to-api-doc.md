---
type: regex
target: {source: file, path: src/stock.ts}
pattern: '^\s*/\*\*(?:(?!\*/)[\s\S])*Units[\s*]+of[\s*]+the[\s*]+SKU[\s*]+that[\s*]+can[\s*]+be[\s*]+sold[\s*]+now:[\s*]+stock[\s*]+on[\s*]+hand[\s*]+minus[\s*]+reservations,[\s*]+never[\s*]+below[\s*]+0\.(?:(?!\*/)[\s\S])*\*/\s*export function availableUnits[^{]*\{(?:(?!//)[\s\S])*$'
---
