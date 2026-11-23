#!/usr/bin/env bash
# A repo adopted at an older version (0.0.1): an older rubric with a rule since dropped and
# no "## Fix sizes" section, plus local rules of its own.
set -euo pipefail
plugin="$(dirname "$0")/../.."
cp -R "$(dirname "$0")/../fixtures/ts-mixed/." .
mkdir -p docs/agents
{
  echo "<!-- Installed by comments:adopt from the comments plugin, version 0.0.1. Re-running adopt with a newer version replaces everything above \"## Local rules\"; add this repo's own rules under that heading. -->"
  echo
  tr -d '\r' < "$plugin/rubric.md" | sed '/^## Fix sizes/,$d'
  echo '- OBSOLETE-RULE: every function needs a banner comment.'
  echo
  echo '## Local rules'
  echo
  echo '- Money helpers keep a comment naming the rounding mode.'
  echo
  echo '### Generated code'
  echo
  echo '- Files under src/gen/ are out of scope.'
} > docs/agents/comment-standards.md
cat > CLAUDE.md <<'EOF'
# Shop

## Coding standards

- Comments: follow [docs/agents/comment-standards.md](docs/agents/comment-standards.md), the coding standard for code comments (say what, not how; what to keep, delete, refactor or move to an ADR).
EOF
