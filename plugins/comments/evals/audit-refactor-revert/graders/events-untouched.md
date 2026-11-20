---
type: regex
target: {source: file, path: shop/events.py}
pattern: 'getattr\(handlers, "on_" \+ event\["type"\]\)\(event\)'
---
