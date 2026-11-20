#!/usr/bin/env bash
# Records a case's history.jsonl: the first turn of a conversation that the case resumes with its
# own prompt.md as the next turn. Each history case calls this from its record-history.sh; re-run
# that after changing the skill or the rubric, since the history holds their text as it was.
#
#   record-history.sh [--keep-scratch] <case-dir> <scaffold> <prompt> <tool>...
#
# <scaffold> is the case's scaffold script, relative to <case-dir>; <prompt> is the first turn;
# the tools are the ones that turn may use. --keep-scratch copies the reports the turn filed under
# .scratch/ into <case-dir>/scratch/, for a scaffold that puts them back.
# Uses your Claude Code login (claude -p, model claude-sonnet-4-6); run it from WSL2 or Linux.
#
# Privacy: the repo is public, and a raw transcript carries account data: ids, the account's
# email, the org's connector setup (MCP instructions), its skill listing, and local paths.
# Thinking blocks carry it too: their base64 signature encodes the organization id. So the filter
# is an allowlist, never a blocklist: it keeps user and assistant entries and the date attachment,
# and in their messages only text, tool_use and tool_result blocks. Paths under the run's work
# directory become repo-relative, which the eval also needs, because it resumes in another
# directory. Parent links are rejoined around the dropped entries.
set -euo pipefail
keep_scratch=0
if [ "${1:-}" = "--keep-scratch" ]; then keep_scratch=1; shift; fi
[ "$#" -ge 4 ] || { echo "usage: $0 [--keep-scratch] <case-dir> <scaffold> <prompt> <tool>..." >&2; exit 2; }
case_dir="$(cd "$1" && pwd)"; scaffold="$2"; prompt="$3"; shift 3
plugin_dir="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d "/tmp/$(basename "$case_dir").XXXXXX")"
trap 'rm -rf "$work"' EXIT
cd "$work"
bash "$case_dir/$scaffold"
session="$(cat /proc/sys/kernel/random/uuid)"
claude -p "$prompt" --session-id "$session" \
  --plugin-dir "$plugin_dir" --add-dir "$plugin_dir" --setting-sources project \
  --model claude-sonnet-4-6 --tools "$@" --permission-mode acceptEdits >/dev/null
if [ "$keep_scratch" = 1 ]; then
  reports=("$work"/.scratch/*.md)
  [ -f "${reports[0]}" ] || { echo "the run filed no report under .scratch/" >&2; exit 1; }
  rm -rf "$case_dir/scratch"
  mkdir -p "$case_dir/scratch"
  cp "${reports[@]}" "$case_dir/scratch/"
fi
transcript="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects" -name "$session.jsonl" | head -n 1)"
python3 - "$transcript" "$case_dir/history.jsonl" "$work" <<'PY'
import json, sys
src, dst, work = sys.argv[1], sys.argv[2], sys.argv[3]
entries = [json.loads(line) for line in open(src, encoding="utf-8")]
for e in entries:
    for field in e:
        if field != "cwd":
            text = json.dumps(e[field], ensure_ascii=False)
            e[field] = json.loads(text.replace(work + "/", "").replace(work, "."))
kept_attachments = {"date"}
kept_blocks = {"text", "tool_use", "tool_result"}
for e in entries:
    content = e.get("message", {}).get("content") if e["type"] in ("user", "assistant") else None
    if isinstance(content, list):
        e["message"]["content"] = [b for b in content if b.get("type") in kept_blocks]
def kept(e):
    if e["type"] in ("user", "assistant"):
        content = e["message"]["content"]
        return isinstance(content, str) or len(content) > 0
    return e["type"] == "attachment" and e["attachment"].get("type") in kept_attachments
parent = {e["uuid"]: e.get("parentUuid") for e in entries if "uuid" in e}
keep = {e["uuid"] for e in entries if "uuid" in e and kept(e)}
def kept_parent(uuid):
    while uuid is not None and uuid not in keep:
        uuid = parent.get(uuid)
    return uuid
with open(dst, "w", encoding="utf-8") as out:
    for e in entries:
        if "uuid" in e and e["uuid"] in keep:
            e["parentUuid"] = kept_parent(e.get("parentUuid"))
            out.write(json.dumps(e, ensure_ascii=False) + "\n")
PY
echo "wrote $case_dir/history.jsonl"
