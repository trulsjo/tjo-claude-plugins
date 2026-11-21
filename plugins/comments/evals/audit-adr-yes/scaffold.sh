#!/usr/bin/env bash
set -euo pipefail
cp -R "$(dirname "$0")/../fixtures/ts-mixed/." .
mkdir -p docs/adr
cat > docs/adr/0001-amounts-in-integer-cents.md <<'MD'
# Amounts in integer cents

All money is held as integer cents, never floats, because the payment provider rejects fractional amounts and float sums drift.
MD
git init -q
git remote add origin https://github.com/example/shop.git
