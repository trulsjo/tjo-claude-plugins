#!/usr/bin/env bash
# shellcheck disable=SC2086
set -euo pipefail

BUILD_DIR=${BUILD_DIR:-dist}

# TODO: retry the upload when the network drops
# copy the build output to the server with rsync
rsync -az --delete $BUILD_DIR/ deploy@shop.example.com:/srv/shop/
