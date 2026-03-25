#!/bin/sh
set -eu

HOME_DIR=${HOME:?HOME is required}
OPENCLAW_HOME=${OPENCLAW_HOME:-"$HOME_DIR/.openclaw"}
TOOLKIT_ROOT=${TOOLKIT_ROOT:-"$OPENCLAW_HOME/toolkit/openclaw-engram-memory-toolkit"}
LAUNCH_AGENTS_DIR=${LAUNCH_AGENTS_DIR:-"$HOME_DIR/Library/LaunchAgents"}
MEMORY_OVERLAY_LABEL=${MEMORY_OVERLAY_LABEL:-local.openclaw-memory-overlay}
CODEX_PROXY_LABEL=${CODEX_PROXY_LABEL:-local.engram-codex-proxy}

UID_NUMBER=$(id -u)
launchctl bootout "gui/$UID_NUMBER/$MEMORY_OVERLAY_LABEL" >/dev/null 2>&1 || true
launchctl bootout "gui/$UID_NUMBER/$CODEX_PROXY_LABEL" >/dev/null 2>&1 || true
rm -f "$LAUNCH_AGENTS_DIR/$MEMORY_OVERLAY_LABEL.plist"
rm -f "$LAUNCH_AGENTS_DIR/$CODEX_PROXY_LABEL.plist"
rm -rf "$TOOLKIT_ROOT"
rm -f "$OPENCLAW_HOME/bin/apply-memory-overlay.py"

echo "Toolkit files removed."
echo "openclaw.json was left in place intentionally."

