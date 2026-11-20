#!/usr/bin/env bash
# Records history.jsonl for this case: a default audit of the case's fixture, which ends at the
# report with its local-refactor finding and patch. The case then names that finding as the next
# turn. The history holds the audit skill's text as it was when recorded: re-run this after
# changing the skill or the rubric. Uses your Claude Code login; run it from WSL2 or Linux.
#
# The transcript is cut down to the conversation: user and assistant entries, plus the date
# attachment. Every other attachment is dropped, because they carry account data: ids, the
# account's email, the org's connector setup (MCP instructions), its skill listing, local paths.
# Thinking blocks are dropped from assistant entries (their signature encodes the org id).
# The parent links are rejoined around the dropped entries. The repo is public: keep this an
# allowlist.
set -euo pipefail
audit_prompt="Audit the comments in shop/pricing.py."
case_dir="$(cd "$(dirname "$0")" && pwd)"
plugin_dir="$(cd "$case_dir/../.." && pwd)"
work="$(mktemp -d /tmp/audit-refactor.XXXXXX)"
cd "$work"
bash "$case_dir/scaffold.sh"
session="$(cat /proc/sys/kernel/random/uuid)"
claude -p "$audit_prompt" --session-id "$session" \
  --plugin-dir "$plugin_dir" --add-dir "$plugin_dir" --setting-sources project \
  --model claude-sonnet-4-6 --tools Read Glob Grep Skill >/dev/null
transcript="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects" -name "$session.jsonl" | head -n 1)"
python3 - "$transcript" "$case_dir/history.jsonl" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
entries = [json.loads(line) for line in open(src, encoding="utf-8")]
kept_attachments = {"date"}
# Thinking blocks go too: their base64 signature encodes the account's organization id.
thinking = {"thinking", "redacted_thinking"}
for e in entries:
    content = (e.get("message") or {}).get("content")
    if isinstance(content, list):
        e["message"]["content"] = [c for c in content if not (isinstance(c, dict) and c.get("type") in thinking)]
def kept(e):
    if e["type"] in ("user", "assistant"):
        return bool((e.get("message") or {}).get("content"))
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
rm -rf "$work"
echo "wrote $case_dir/history.jsonl"
