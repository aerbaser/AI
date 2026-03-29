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
SYSTEMD_USER_DIR=${SYSTEMD_USER_DIR:-"$HOME_DIR/.config/systemd/user"}

if [ ! -f "$OPENCLAW_CONFIG" ]; then
  echo "openclaw config not found at $OPENCLAW_CONFIG" >&2
  exit 1
fi

mkdir -p "$TOOLKIT_ROOT" "$OPENCLAW_HOME/bin" "$SYSTEMD_USER_DIR"
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

SERVICE_PATH="$SYSTEMD_USER_DIR/memory-claw-v2-proxy.service"
cat > "$SERVICE_PATH" <<EOF
[Unit]
Description=memory-claw-v2 Codex proxy
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROXY_DIR
Environment=HOST=$PROXY_HOST
Environment=PORT=$PROXY_PORT
Environment=CODEX_MODEL=$CODEX_MODEL
Environment=MODEL_LABEL=$MODEL_LABEL
ExecStart=/usr/bin/env node $PROXY_DIR/server.mjs
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

if command -v systemctl >/dev/null 2>&1; then
  systemctl --user daemon-reload || true
  systemctl --user enable --now memory-claw-v2-proxy.service || true
fi

echo "memory-claw-v2 installed for Linux."
echo "Proxy: $PROXY_URL"
