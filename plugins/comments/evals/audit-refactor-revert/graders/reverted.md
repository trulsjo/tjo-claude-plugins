---
type: regex
target: {source: file, path: shop/handlers.py}
pattern: '^# ref = refund\r?\ndef on_ref\(event\):(?![\s\S]*on_refund)'
---
