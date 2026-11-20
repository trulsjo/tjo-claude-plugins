#!/usr/bin/env bash
set -euo pipefail
case_dir="$(dirname "$0")"
bash "$case_dir/../audit-repo/scaffold.sh"
mkdir -p .scratch
cp "$case_dir/scratch/"*.md .scratch/
