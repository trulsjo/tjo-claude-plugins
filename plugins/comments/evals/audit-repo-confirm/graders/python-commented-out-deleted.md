---
type: regex
target: {source: file, path: tools/report.py}
pattern: '#\s*print\(rows\)'
match: not_contains
---
