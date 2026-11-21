#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Example Shop AS
set -euo pipefail
tar -czf "backup-$(date +%F).tar.gz" data/
