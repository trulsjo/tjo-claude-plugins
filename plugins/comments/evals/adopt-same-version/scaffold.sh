#!/usr/bin/env bash
# A repo already adopted at the plugin's current version, with a local rule of its own.
set -euo pipefail
plugin="$(dirname "$0")/../.."
version="$(sed -n 's/^ *"version": *"\([^"]*\)".*/\1/p' "$plugin/.claude-plugin/plugin.json")"
cp -R "$(dirname "$0")/../fixtures/ts-mixed/." .
mkdir -p docs/agents
{
  echo "<!-- Installed by comments:adopt from the comments plugin, version $version. Re-running adopt with a newer version replaces everything above \"## Local rules\"; add this repo's own rules under that heading. -->"
  echo
  tr -d '\r' < "$plugin/rubric.md"
  echo
  echo '## Local rules'
  echo
  echo '- Money helpers keep a comment naming the rounding mode.'
} > docs/agents/comment-standards.md
cat > CLAUDE.md <<'EOF'
# Shop

## Coding standards

- TypeScript: strict mode, no `any`.
- Comments: follow [docs/agents/comment-standards.md](docs/agents/comment-standards.md), the coding standard for code comments (say what, not how; what to keep, delete, refactor or move to an ADR).
EOF
