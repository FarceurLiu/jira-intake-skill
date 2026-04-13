#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${1:-${CODEX_HOME:-$HOME/.codex}/skills/jira-intake}"

mkdir -p "$TARGET_DIR"

rsync -a --delete \
  --exclude='.git/' \
  --exclude='.local-archive/' \
  --exclude='config/.env' \
  --exclude='config/team-config.private.json' \
  --exclude='*.private.json' \
  "$SOURCE_DIR/" "$TARGET_DIR/"

printf 'synced jira-intake skill to %s\n' "$TARGET_DIR"
