---
type: regex
pattern: '//[^\n]*docs/adr/0002-[\w-]+\.md[^\n]*\n(//[^\n]*\n)?const ZONE_RATES'
target:
  source: file
  path: src/shipping.ts
---
