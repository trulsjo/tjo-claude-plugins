---
type: regex
target: {source: file, path: scripts/deploy.sh}
pattern: '^(?=[\s\S]*TODO: retry the upload when the network drops)(?=[\s\S]*copy the build output to the server with rsync)'
---
