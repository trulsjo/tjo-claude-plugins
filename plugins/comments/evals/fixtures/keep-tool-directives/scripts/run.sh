#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC2086
exec python -m report $REPORT_ARGS
