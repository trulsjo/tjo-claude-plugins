#!/usr/bin/env bash
# Records history.jsonl with the shared ../record-history.sh: a default audit of the case's
# fixture, which ends at the report and its offer to apply the trivial fixes. The case then sends
# "yes" as the next turn.
set -euo pipefail
case_dir="$(dirname "$0")"
exec bash "$case_dir/../record-history.sh" "$case_dir" scaffold.sh \
  "Audit the comments in src/." Read Glob Grep Skill
