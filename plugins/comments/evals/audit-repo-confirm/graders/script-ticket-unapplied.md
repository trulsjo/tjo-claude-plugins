---
type: regex
target: {source: file, path: scripts/deploy.sh}
pattern: '^(?=[\s\S]*TODO: retry the upload)(?=[\s\S]*shellcheck disable=SC2086)'
---
