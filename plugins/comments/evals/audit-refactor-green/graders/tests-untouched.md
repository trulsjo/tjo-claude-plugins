---
type: regex
target: {source: file, path: tests/test_pricing.py}
pattern: '^(?=[\s\S]*with_tax\(1000, 25\), 1250\))(?=[\s\S]*with_tax\(999, 15\), 1149\))'
---
