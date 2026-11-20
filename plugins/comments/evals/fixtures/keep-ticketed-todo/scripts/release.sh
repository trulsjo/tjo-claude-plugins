#!/usr/bin/env bash
set -euo pipefail
# TODO https://github.com/example-shop/web/issues/77 sign the release tarball
tar -czf release.tar.gz dist/
