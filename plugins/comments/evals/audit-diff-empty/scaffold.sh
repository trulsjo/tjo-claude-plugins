#!/usr/bin/env bash
set -euo pipefail
bash "$(dirname "$0")/../fixtures/diff-repo/build.sh"
git tag v1.2
