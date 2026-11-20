#!/usr/bin/env bash
# CLAUDE.md already has a coding-standards heading (title case, not the last section).
set -euo pipefail
cp -R "$(dirname "$0")/../fixtures/ts-mixed/." .
cat > CLAUDE.md <<'EOF'
# Shop

## Coding Standards

- TypeScript: strict mode, no `any`.

## Agent skills

Issues live in GitHub Issues.
EOF
