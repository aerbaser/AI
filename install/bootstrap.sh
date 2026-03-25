#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

HOME_DIR=${HOME:?HOME is required}
OPENCLAW_HOME=${OPENCLAW_HOME:-"$HOME_DIR/.openclaw"}
OPENCLAW_CONFIG=${OPENCLAW_CONFIG:-"$OPENCLAW_HOME/openclaw.json"}
TOOLKIT_ROOT=${TOOLKIT_ROOT:-"$OPENCLAW_HOME/toolkit/openclaw-engram-memory-toolkit"}
LAUNCH_AGENTS_DIR=${LAUNCH_AGENTS_DIR:-"$HOME_DIR/Library/LaunchAgents"}
VOYAGE_API_KEY=${VOYAGE_API_KEY:-}
CODEX_MODEL=${CODEX_MODEL:-gpt-5.4-mini}
MODEL_LABEL=${MODEL_LABEL:-"openai-codex/$CODEX_MODEL"}
PROXY_HOST=${PROXY_HOST:-127.0.0.1}
PROXY_PORT=${PROXY_PORT:-4321}
PROXY_URL="http://$PROXY_HOST:$PROXY_PORT"
MEMORY_OVERLAY_LABEL=${MEMORY_OVERLAY_LABEL:-local.openclaw-memory-overlay}
CODEX_PROXY_LABEL=${CODEX_PROXY_LABEL:-local.engram-codex-proxy}
PATH_DEFAULT=${PATH_DEFAULT:-/usr/local/bin:/usr/local/opt/node/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin}

if [ ! -f "$OPENCLAW_CONFIG" ]; then
  echo "openclaw config not found at $OPENCLAW_CONFIG" >&2
  exit 1
fi

if [ -z "$VOYAGE_API_KEY" ]; then
  echo "VOYAGE_API_KEY is required" >&2
  exit 1
fi

mkdir -p "$TOOLKIT_ROOT" "$OPENCLAW_HOME/bin" "$OPENCLAW_HOME/logs" "$LAUNCH_AGENTS_DIR"
rm -rf "$TOOLKIT_ROOT/proxy"
cp -R "$REPO_DIR/proxy" "$TOOLKIT_ROOT/proxy"
cp "$REPO_DIR/overlay/apply_memory_overlay.py" "$OPENCLAW_HOME/bin/apply-memory-overlay.py"
chmod 755 "$OPENCLAW_HOME/bin/apply-memory-overlay.py"

export OPENCLAW_CONFIG VOYAGE_API_KEY MODEL_LABEL PROXY_URL OPENCLAW_HOME
/usr/bin/python3 - <<'PY'
import json
import os
import secrets
from pathlib import Path

cfg_path = Path(os.environ["OPENCLAW_CONFIG"])
cfg = json.loads(cfg_path.read_text())

engram = (
    cfg.setdefault("plugins", {})
    .setdefault("entries", {})
    .setdefault("openclaw-engram", {})
    .setdefault("config", {})
)
auth = engram.setdefault("agentAccessHttp", {})
auth["enabled"] = True
auth["host"] = "127.0.0.1"
auth["port"] = 4318
auth["authToken"] = auth.get("authToken") or secrets.token_urlsafe(32)
engram["memoryOsPreset"] = "balanced"
engram["qmdEnabled"] = True
engram["qmdDaemonEnabled"] = True
engram["qmdCollection"] = "openclaw-engram"
engram["qmdPath"] = str(Path(os.environ["OPENCLAW_HOME"]) / "bin" / "qmd-voyage")
engram["nativeKnowledge"] = {
    "enabled": True,
    "includeFiles": [
        "MEMORY.md",
        "IDENTITY.md",
        "USER.md",
        "SOUL.md",
        "AGENTS.md",
        "TOOLS.md",
        "HEARTBEAT.md",
    ],
    "maxResults": 6,
    "maxChars": 5000,
}
engram["fileHygiene"] = {
    "enabled": True,
    "lintEnabled": True,
    "lintBudgetBytes": 12288,
    "lintWarnRatio": 0.85,
    "lintPaths": [
        "MEMORY.md",
        "IDENTITY.md",
        "USER.md",
        "SOUL.md",
        "AGENTS.md",
        "TOOLS.md",
        "HEARTBEAT.md",
    ],
    "warningsLogEnabled": True,
    "warningsLogPath": "memory/local/state/file-hygiene-warnings.log",
}
engram["lcmEnabled"] = False
engram["localLlmEnabled"] = True
engram["localLlmUrl"] = os.environ["PROXY_URL"]
engram["localLlmModel"] = os.environ["MODEL_LABEL"]
engram["debug"] = False
engram["captureMode"] = "hybrid"
engram["recallBudgetChars"] = 80000
engram["conversationIndexEnabled"] = True

memory = cfg.setdefault("memory", {})
memory["backend"] = "qmd"
memory["citations"] = "auto"
memory_qmd = memory.setdefault("qmd", {})
memory_qmd["command"] = str(Path(os.environ["OPENCLAW_HOME"]) / "bin" / "qmd-voyage")
memory_qmd["searchMode"] = "query"
memory_qmd["includeDefaultMemory"] = True
memory_qmd["sessions"] = {"enabled": True, "retentionDays": 30}
memory_qmd["update"] = {
    "interval": "5m",
    "debounceMs": 15000,
    "onBoot": True,
    "waitForBootSync": False,
}
memory_qmd["limits"] = {"maxResults": 8, "timeoutMs": 180000}

defaults = cfg.setdefault("agents", {}).setdefault("defaults", {})
model = defaults.setdefault("model", {})
model.setdefault("primary", "openai-codex/gpt-5.4")
defaults.setdefault("models", {}).setdefault(os.environ["MODEL_LABEL"], {})
memory_search = defaults.setdefault("memorySearch", {})
memory_search["enabled"] = True
memory_search["sources"] = ["memory", "sessions"]
memory_search["experimental"] = {"sessionMemory": True}
memory_search["provider"] = "voyage"
memory_search["remote"] = {
    "apiKey": os.environ["VOYAGE_API_KEY"],
    "batch": {
        "enabled": False,
        "wait": True,
        "concurrency": 1,
        "pollIntervalMs": 5000,
        "timeoutMinutes": 120,
    },
}
memory_search["model"] = "voyage-4-large"
memory_search["sync"] = {
    "onSessionStart": True,
    "onSearch": True,
    "watch": True,
    "intervalMinutes": 5,
    "sessions": {
        "deltaBytes": 4096,
        "deltaMessages": 20,
    },
}

cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")
print(auth["authToken"])
PY

AUTH_TOKEN=$(/usr/bin/python3 - <<'PY'
import json
import os
from pathlib import Path

cfg = json.loads(Path(os.environ["OPENCLAW_CONFIG"]).read_text())
print(cfg["plugins"]["entries"]["openclaw-engram"]["config"]["agentAccessHttp"]["authToken"])
PY
)

render_template() {
  template_path=$1
  target_path=$2
  sed \
    -e "s|__HOME__|$HOME_DIR|g" \
    -e "s|__OPENCLAW_HOME__|$OPENCLAW_HOME|g" \
    -e "s|__TOOLKIT_ROOT__|$TOOLKIT_ROOT|g" \
    -e "s|__PATH_DEFAULT__|$PATH_DEFAULT|g" \
    -e "s|__MODEL_LABEL__|$MODEL_LABEL|g" \
    -e "s|__CODEX_MODEL__|$CODEX_MODEL|g" \
    -e "s|__PROXY_HOST__|$PROXY_HOST|g" \
    -e "s|__PROXY_PORT__|$PROXY_PORT|g" \
    -e "s|__AUTH_TOKEN__|$AUTH_TOKEN|g" \
    "$template_path" > "$target_path"
}

render_template "$REPO_DIR/templates/local.openclaw-memory-overlay.plist" "$LAUNCH_AGENTS_DIR/$MEMORY_OVERLAY_LABEL.plist"
render_template "$REPO_DIR/templates/local.engram-codex-proxy.plist" "$LAUNCH_AGENTS_DIR/$CODEX_PROXY_LABEL.plist"

PATH="$PATH_DEFAULT" /usr/bin/python3 "$OPENCLAW_HOME/bin/apply-memory-overlay.py"

UID_NUMBER=$(id -u)
launchctl bootout "gui/$UID_NUMBER/$MEMORY_OVERLAY_LABEL" >/dev/null 2>&1 || true
launchctl bootout "gui/$UID_NUMBER/$CODEX_PROXY_LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$UID_NUMBER" "$LAUNCH_AGENTS_DIR/$MEMORY_OVERLAY_LABEL.plist"
launchctl bootstrap "gui/$UID_NUMBER" "$LAUNCH_AGENTS_DIR/$CODEX_PROXY_LABEL.plist"
launchctl kickstart -k "gui/$UID_NUMBER/$MEMORY_OVERLAY_LABEL"
launchctl kickstart -k "gui/$UID_NUMBER/$CODEX_PROXY_LABEL"

echo "Toolkit installed."
echo "Proxy URL: $PROXY_URL"
echo "Run ./install/verify.sh next."

