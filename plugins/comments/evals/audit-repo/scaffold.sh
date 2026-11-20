#!/usr/bin/env bash
set -euo pipefail
fixtures="$(dirname "$0")/../fixtures"
mkdir -p shop/src lib/src
cp -R "$fixtures/ts-mixed/src/." shop/src/
cp -R "$fixtures/ts-clean/src/." lib/src/
cp -R "$fixtures/repo-extra/." .
