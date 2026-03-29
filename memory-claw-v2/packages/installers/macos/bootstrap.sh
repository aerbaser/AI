#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)

HOME_DIR=${HOME:?HOME is required}
OPENCLAW_HOME=${OPENCLAW_HOME:-"$HOME_DIR/.openclaw"}
OPENCLAW_CONFIG=${OPENCLAW_CONFIG:-"$OPENCLAW_HOME/openclaw.json"}
TOOLKIT_ROOT=${TOOLKIT_ROOT:-"$OPENCLAW_HOME/toolkit/memory-claw-v2"}
QMD_WRAPPER=${QMD_WRAPPER:-"$OPENCLAW_HOME/bin/qmd-voyage"}
PROXY_DIR="$TOOLKIT_ROOT/proxy"
CODEX_MODEL=${CODEX_MODEL:-gpt-5.4-mini}
MODEL_LABEL=${MODEL_LABEL:-"openai-codex/$CODEX_MODEL"}
PROXY_HOST=${PROXY_HOST:-127.0.0.1}
PROXY_PORT=${PROXY_PORT:-4321}
PROXY_URL="http://$PROXY_HOST:$PROXY_PORT"
VOYAGE_MODEL=${VOYAGE_MODEL:-voyage-3-large}
LAUNCH_AGENTS_DIR=${LAUNCH_AGENTS_DIR:-"$HOME_DIR/Library/LaunchAgents"}
PLIST_PATH="$LAUNCH_AGENTS_DIR/local.memory-claw-v2-proxy.plist"
LABEL=${LABEL:-local.memory-claw-v2-proxy}

if [ ! -f "$OPENCLAW_CONFIG" ]; then
  echo "openclaw config not found at $OPENCLAW_CONFIG" >&2
  exit 1
fi

mkdir -p "$TOOLKIT_ROOT" "$OPENCLAW_HOME/bin" "$LAUNCH_AGENTS_DIR"
rm -rf "$PROXY_DIR"
cp -R "$REPO_DIR/proxy" "$PROXY_DIR"

cat > "$QMD_WRAPPER" <<EOF
#!/bin/sh
set -eu
PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:\${PATH:-}"
export QMD_EMBED_PROVIDER="\${QMD_EMBED_PROVIDER:-voyage}"
export QMD_VOYAGE_MODEL="\${QMD_VOYAGE_MODEL:-$VOYAGE_MODEL}"
exec qmd "\$@"
EOF
chmod 755 "$QMD_WRAPPER"

python3 "$REPO_DIR/integrations/openclaw/bin/render_openclaw_overlay.py" \
  --config "$OPENCLAW_CONFIG" \
  --proxy-url "$PROXY_URL" \
  --proxy-model "$MODEL_LABEL" \
  --qmd-command "$QMD_WRAPPER" \
  --shared-memory-path "$OPENCLAW_HOME/shared-memory" \
  --voyage-model "$VOYAGE_MODEL"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>node</string>
    <string>$PROXY_DIR/server.mjs</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOST</key>
    <string>$PROXY_HOST</string>
    <key>PORT</key>
    <string>$PROXY_PORT</string>
    <key>CODEX_MODEL</key>
    <string>$CODEX_MODEL</string>
    <key>MODEL_LABEL</key>
    <string>$MODEL_LABEL</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH" || true
launchctl kickstart -k "gui/$(id -u)/$LABEL" || true

echo "memory-claw-v2 installed for macOS."
echo "Proxy: $PROXY_URL"
