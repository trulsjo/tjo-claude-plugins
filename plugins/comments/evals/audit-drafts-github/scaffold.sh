#!/usr/bin/env bash
set -euo pipefail
cp -R "$(dirname "$0")/../fixtures/ts-mixed/." .
git init -q
git remote add origin https://github.com/example/shop.git
