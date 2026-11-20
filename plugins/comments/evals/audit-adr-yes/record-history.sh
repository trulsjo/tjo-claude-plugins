#!/usr/bin/env bash
# Records history.jsonl with the shared ../record-history.sh: an audit whose request already asks
# for the ADRs, which ends at the report with the ADR draft and its offer (audit-yes-in-request
# checks that turn). The case then says yes to the ADRs as the next turn.
set -euo pipefail
case_dir="$(dirname "$0")"
exec bash "$case_dir/../record-history.sh" "$case_dir" scaffold.sh \
  "Audit the comments in src/. Yes, write the ADRs you draft and point the comments at them. Leave everything else in the report." \
  Read Glob Grep Skill
