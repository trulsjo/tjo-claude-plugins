#!/usr/bin/env bash
# Records history.jsonl and scratch/ with the shared ../record-history.sh: a whole-repo audit of
# audit-repo's fixture, which files its report under .scratch/ (kept in scratch/, which
# scaffold.sh puts back) and ends at the summary and its offer. The case then sends "yes" as the
# next turn.
set -euo pipefail
case_dir="$(dirname "$0")"
exec bash "$case_dir/../record-history.sh" --keep-scratch "$case_dir" ../audit-repo/scaffold.sh \
  "Audit the comments in the whole repo." Read Glob Grep Skill Agent Write
