#!/usr/bin/env bash
# Builds a git repo in the current directory. main holds src/pricing.ts with two
# narrating comments; branch feature (checked out) changes applyDiscount and adds
# one more narrating comment. formatPrice is not touched by the diff.
set -euo pipefail
g() { git -c user.name=Eval -c user.email=eval@example.com "$@"; }
g init -q -b main
mkdir -p src
cat > src/pricing.ts <<'TS'
export function applyDiscount(total: number, rate: number): number {
  // multiply the total by one minus the rate
  return total * (1 - rate);
}

export function formatPrice(cents: number): string {
  // divide by 100 and print two decimals
  return `$${(cents / 100).toFixed(2)}`;
}
TS
g add -A
g commit -q -m "pricing helpers"
g checkout -q -b feature
cat > src/pricing.ts <<'TS'
export function applyDiscount(total: number, rate: number): number {
  // multiply the total by one minus the rate
  // clamp the rate so it stays between zero and one
  const r = Math.min(Math.max(rate, 0), 1);
  return total * (1 - r);
}

export function formatPrice(cents: number): string {
  // divide by 100 and print two decimals
  return `$${(cents / 100).toFixed(2)}`;
}
TS
g commit -q -am "clamp the discount rate"
