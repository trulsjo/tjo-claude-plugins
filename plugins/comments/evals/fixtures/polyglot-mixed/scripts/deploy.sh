#!/usr/bin/env bash
# Added by Kim in March 2025: now uploads with aws s3 sync instead of rsync.
set -euo pipefail

BUILD_DIR="dist"
# shellcheck disable=SC2086
FLAGS=${DEPLOY_FLAGS:-}

# TODO: retry the upload when the network drops
# copy the build directory to the bucket
aws s3 sync "$BUILD_DIR" "s3://example-shop-web" $FLAGS

# TODO(#87): invalidate the CloudFront cache after the upload
echo "deployed $BUILD_DIR"
