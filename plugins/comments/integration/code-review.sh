#!/usr/bin/env bash
# Integration check for the comments plugin: after comments:adopt, does
# mattpocock-skills:code-review report a narrating (class 1) comment under
# Standards, citing the adopted doc? Run by hand before each release.
#
# Usage: plugins/comments/integration/code-review.sh [--skip-adopt] [--model <model>] [--keep]
#   --skip-adopt  build the repo without running adopt (the check should then fail)
#   --model       model for both claude -p runs (default: sonnet, to keep the run cheap)
#   --keep        keep the temporary repo and logs
#   --check FILE  only judge a saved code-review answer: exit 0 when it holds the finding
#
# Exit codes: 0 finding reported, 1 finding missing, 2 setup or environment problem.
# Bills the Claude Code subscription login only; stops if an API key, Bedrock,
# Vertex or Foundry would be used.
set -euo pipefail

model=sonnet
skip_adopt=0
keep=0
check=
while [ $# -gt 0 ]; do
  case "$1" in
    --skip-adopt) skip_adopt=1 ;;
    --model) model="$2"; shift ;;
    --keep) keep=1 ;;
    --check) check="${2:-}"; [ -n "$check" ] || { echo "--check needs a file" >&2; exit 2; }; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

die() { echo "SETUP: $*" >&2; exit 2; }

# Reads a code-review answer on stdin and prints the first finding under its Standards heading
# that cites comment-standards, names the planted comment's kind ("loop over", "narrat" or
# class 1, not class 10), points at the planted comment (src/cart.ts:12 or its words "loop over
# every item") and does not
# say there is no violation; fails when there is none. A finding is a
# paragraph or a list item; the Standards section ends at the next heading.
standards_finding() {
  awk '
    /^#+ / { on = ($0 ~ /^#+ *Standards/); flush(); next }
    !on { next }
    /^[[:space:]]*$/ { flush(); next }
    /^[ \t]*([-*]|[0-9]+[.)]) / { flush() }
    { block = block $0 "\n" }
    END { flush(); exit !found }
    function flush() {
      if (!found && block ~ /comment-standards/ && tolower(block) ~ /loop over|narrat|class 1([^0-9]|$)/ \
          && (block ~ /cart\.ts:12([^0-9]|$)/ || tolower(block) ~ /loop over every item/) \
          && tolower(block) !~ /no (violation|finding|issue)s?|nothing to report/) {
        printf "%s", block; found = 1
      }
      block = ""
    }'
}

if [ -n "$check" ]; then
  [ -f "$check" ] || die "no such file: $check"
  standards_finding < "$check"
  exit
fi

# Subscription billing only: no key, token, gateway or cloud provider.
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS \
  ANTHROPIC_FOUNDRY_API_KEY ANTHROPIC_FOUNDRY_BASE_URL ANTHROPIC_FOUNDRY_RESOURCE \
  ANTHROPIC_VERTEX_PROJECT_ID ANTHROPIC_VERTEX_BASE_URL ANTHROPIC_BEDROCK_BASE_URL \
  CLAUDE_CODE_USE_BEDROCK CLAUDE_CODE_USE_VERTEX CLAUDE_CODE_USE_FOUNDRY \
  AWS_BEARER_TOKEN_BEDROCK AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_PROFILE \
  CLOUD_ML_REGION GOOGLE_APPLICATION_CREDENTIALS
# Run as a fresh top-level session, not as a child of the session that started the script.
unset CLAUDECODE CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_SESSION_ID CLAUDE_CODE_CHILD_SESSION \
  CLAUDE_CODE_CHILD_NOTES_DIR CLAUDE_CODE_SESSION_ATTENDED CLAUDE_CODE_MESSAGING_SOCKET \
  CLAUDE_CODE_MESSAGING_TOKEN CLAUDE_PID

command -v claude >/dev/null || die "claude not on PATH"
command -v git >/dev/null || die "git not on PATH"

auth=$(claude auth status 2>/dev/null) || die "claude auth status failed; run claude and log in"
grep -q '"loggedIn": *true' <<<"$auth" || die "not logged in"
grep -q '"authMethod": *"claude.ai"' <<<"$auth" || die "not a claude.ai subscription login (an API key or provider would be billed)"
grep -q '"apiProvider": *"firstParty"' <<<"$auth" || die "API provider is not firstParty"

plugins=$(claude plugin list 2>/dev/null) || die "claude plugin list failed"
mattpocock_entry=$(grep -A3 'mattpocock-skills@' <<<"$plugins" || true)
grep -q 'enabled' <<<"$mattpocock_entry" || die "mattpocock-skills is not installed and enabled in the user config"
mattpocock_version=$(sed -n 's/.*Version: *//p' <<<"$mattpocock_entry" | head -1)

script_dir=$(cd "$(dirname "$0")" && pwd)
plugin_dir=$(cd "$script_dir/.." && pwd)
plugin_version=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$plugin_dir/.claude-plugin/plugin.json")
path_for_claude() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else echo "$1"; fi; }

work=$(mktemp -d)
repo="$work/repo"
cleanup() { if [ "$keep" = 0 ]; then rm -rf "$work"; else echo "kept: $work"; fi; }
trap cleanup EXIT

echo "comments $plugin_version, mattpocock-skills $mattpocock_version, model $model, $(date +%Y-%m-%d)"

mkdir -p "$repo/src" "$repo/docs/agents" "$repo/docs/specs"
cd "$repo"
git init -q -b main
git config user.name "integration check"
git config user.email "check@example.invalid"
git config commit.gpgsign false

cat > src/cart.ts <<'EOF'
export interface LineItem {
  price: number;
  quantity: number;
}

export function itemCount(items: LineItem[]): number {
  return items.reduce((n, item) => n + item.quantity, 0);
}
EOF
cat > docs/agents/issue-tracker.md <<'EOF'
# Issue tracker

This repo has no issue tracker. Specs live in `docs/specs/`, one file per branch, named after the branch.
EOF
cat > docs/specs/order-total.md <<'EOF'
# order-total

Add `orderTotal(items: LineItem[]): number` to `src/cart.ts`. It returns the sum of price times
quantity over all items, and 0 for an empty list.
EOF
git add -A
git commit -q -m "Cart line items and item count"

if [ "$skip_adopt" = 0 ]; then
  echo "running comments:adopt ..."
  claude -p "/comments:adopt" --model "$model" --plugin-dir "$(path_for_claude "$plugin_dir")" \
    --add-dir "$(path_for_claude "$plugin_dir")" --permission-mode acceptEdits \
    --allowedTools Read Glob Grep Skill Write Edit --max-budget-usd 1 \
    > "$work/adopt.txt" 2>&1 || die "adopt run failed; see $work/adopt.txt (use --keep)"
  [ -f docs/agents/comment-standards.md ] || die "adopt wrote no docs/agents/comment-standards.md"
  grep -q 'docs/agents/comment-standards.md' CLAUDE.md 2>/dev/null || die "adopt added no CLAUDE.md entry"
  git add -A
  git commit -q -m "Adopt the comment standards"
fi

git checkout -q -b order-total
cat >> src/cart.ts <<'EOF'

export function orderTotal(items: LineItem[]): number {
  let total = 0;
  // Loop over every item and add its price times its quantity to the total.
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total;
}
EOF
git commit -q -am "Add orderTotal"

echo "running mattpocock-skills:code-review main ..."
claude -p "/mattpocock-skills:code-review main" --model "$model" \
  --allowedTools "Bash(git:*)" Read Glob Grep Agent Task Skill --max-budget-usd 3 \
  > "$work/review.txt" 2>&1 || die "code-review run failed; see $work/review.txt (use --keep)"

if finding=$(standards_finding < "$work/review.txt"); then
  echo "PASS: code-review reported the comment under Standards:"
  echo "$finding" | head -8
  exit 0
fi
echo "FAIL: no finding citing comment-standards.md for the planted comment under Standards." >&2
echo "--- code-review output ---" >&2
cat "$work/review.txt" >&2
exit 1
