#!/usr/bin/env bash
# Records history.jsonl for this case: a whole-repo audit of audit-repo's fixture, which files its
# report under .scratch/ and ends at the summary and its offer to apply the trivial fixes. The
# filed report is kept in scratch/, which scaffold.sh puts back. The case then sends "yes" as the
# next turn. The history holds the audit skill's text as it was when recorded: re-run this after
# changing the skill or the rubric. Uses your Claude Code login; run it from WSL2 or Linux.
#
# The transcript is cut down to the conversation: user and assistant entries, plus the date
# attachment. Every other attachment is dropped, because they carry account data: ids, the
# account's email, the org's connector setup (MCP instructions), its skill listing, local paths.
# Thinking blocks are dropped too: their signatures encode the org's id. The parent links are
# rejoined around the dropped entries. The repo is public: keep this an allowlist.
set -euo pipefail
case_dir="$(cd "$(dirname "$0")" && pwd)"
plugin_dir="$(cd "$case_dir/../.." && pwd)"
work="$(mktemp -d /tmp/audit-repo-confirm.XXXXXX)"
cd "$work"
bash "$case_dir/../audit-repo/scaffold.sh"
session="$(cat /proc/sys/kernel/random/uuid)"
claude -p "Audit the comments in the whole repo." --session-id "$session" \
  --plugin-dir "$plugin_dir" --add-dir "$plugin_dir" --setting-sources project \
  --model claude-sonnet-4-6 --tools Read Glob Grep Skill Agent Write \
  --permission-mode acceptEdits >/dev/null
reports=("$work"/.scratch/*.md)
[ -f "${reports[0]}" ] || { echo "the run filed no report under .scratch/" >&2; exit 1; }
rm -rf "$case_dir/scratch"
mkdir -p "$case_dir/scratch"
cp "${reports[@]}" "$case_dir/scratch/"
transcript="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects" -name "$session.jsonl" | head -n 1)"
python3 - "$transcript" "$case_dir/history.jsonl" "$work" <<'PY'
import json, sys
src, dst, work = sys.argv[1], sys.argv[2], sys.argv[3]
entries = [json.loads(line) for line in open(src, encoding="utf-8")]
# The eval resumes in another directory, so paths in the messages are made relative to the repo.
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
rm -rf "$work"
echo "wrote $case_dir/history.jsonl"
