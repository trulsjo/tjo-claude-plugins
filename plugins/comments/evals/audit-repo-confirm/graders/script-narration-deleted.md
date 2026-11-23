---
type: regex
target: {source: file, path: scripts/deploy.sh}
pattern: 'copy the build output'
match: not_contains
---
