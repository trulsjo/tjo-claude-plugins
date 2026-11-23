#!/usr/bin/env bash
set -euo pipefail
cp -R "$(dirname "$0")/../fixtures/ts-mixed/." .
cat > CLAUDE.md <<'EOF'
# Shop

## Agent skills

Issues live in GitHub Issues.
EOF
