#!/usr/bin/env bash
# A repo with no CLAUDE.md.
set -euo pipefail
cp -R "$(dirname "$0")/../fixtures/ts-mixed/." .
