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
# is an allowlist, never a blocklist: it keeps user and assistant entries and the date attachment;
# of each entry only the fields a replay reads (type, uuid, parentUuid, isSidechain, isMeta,
# userType, sessionId, cwd, timestamp, version, message, attachment); of each message only role,
# content, and for an assistant model, type and stop_reason; and of the content only text,
# tool_use and tool_result blocks. Request, message and prompt ids, tool results' raw payloads
# and permission data go. The uuids and the session id stay, as a replay links entries by them;
# the recorder makes the session id itself, a random one. Paths under the run's work directory
# become repo-relative, which the eval also needs, because it resumes in another directory; the
# plugin's own path becomes ${CLAUDE_PLUGIN_ROOT}. Parent links are rejoined around the dropped
# entries.
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
# No MCP servers, the claude.ai connectors included: the turn has only the tools named here.
ENABLE_CLAUDEAI_MCP_SERVERS=false claude -p "$prompt" --session-id "$session" \
  --plugin-dir "$plugin_dir" --add-dir "$plugin_dir" --setting-sources project --strict-mcp-config \
  --model claude-sonnet-4-6 --tools "$@" --permission-mode acceptEdits >/dev/null
if [ "$keep_scratch" = 1 ]; then
  reports=("$work"/.scratch/*.md)
  [ -f "${reports[0]}" ] || { echo "the run filed no report under .scratch/" >&2; exit 1; }
fi
transcript="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects" -name "$session.jsonl" | head -n 1)"
[ -f "$transcript" ] || { echo "no transcript for session $session; nothing written" >&2; exit 1; }
# The history and the reports are a pair: both are written to $work first, and the case's copies
# are replaced only once the filter has accepted the run.
python3 - "$transcript" "$work/history.jsonl.new" "$work" "$plugin_dir" "$@" <<'PY'
import json, sys
src, dst, work, plugin_dir, tools = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], set(sys.argv[5:])
entries = [json.loads(line) for line in open(src, encoding="utf-8")]
used = {b.get("name") for e in entries if e.get("type") == "assistant"
        for b in e["message"].get("content", []) if isinstance(b, dict) and b.get("type") == "tool_use"}
if used - tools:
    sys.exit(f"the turn used tools it was not given: {sorted(used - tools)}; nothing written")
for e in entries:
    for field in e:
        if field != "cwd":
            text = json.dumps(e[field], ensure_ascii=False)
            text = text.replace(work + "/", "").replace(work, ".")
            e[field] = json.loads(text.replace(plugin_dir, "${CLAUDE_PLUGIN_ROOT}"))
kept_fields = {"type", "uuid", "parentUuid", "isSidechain", "isMeta", "userType", "sessionId",
               "cwd", "timestamp", "version", "message", "attachment"}
kept_message_fields = {"role", "content", "model", "type", "stop_reason"}
for e in entries:
    for field in set(e) - kept_fields:
        del e[field]
    if isinstance(e.get("message"), dict):
        for field in set(e["message"]) - kept_message_fields:
            del e["message"][field]
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
if [ "$keep_scratch" = 1 ]; then
  rm -rf "$case_dir/scratch"
  mkdir -p "$case_dir/scratch"
  cp "${reports[@]}" "$case_dir/scratch/"
fi
mv "$work/history.jsonl.new" "$case_dir/history.jsonl"
echo "wrote $case_dir/history.jsonl"
