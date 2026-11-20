#!/usr/bin/env bash
# Records history.jsonl with the shared ../record-history.sh: a default audit of
# shop/pricing.py, which ends at the report with its local-refactor finding and patch. The case
# then names that finding as the next turn.
set -euo pipefail
case_dir="$(dirname "$0")"
exec bash "$case_dir/../record-history.sh" "$case_dir" scaffold.sh \
  "Audit the comments in shop/pricing.py." Read Glob Grep Skill
