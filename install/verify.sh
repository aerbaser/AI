#!/bin/sh
set -eu

HOME_DIR=${HOME:?HOME is required}
OPENCLAW_HOME=${OPENCLAW_HOME:-"$HOME_DIR/.openclaw"}
PATH_DEFAULT=${PATH_DEFAULT:-/usr/local/bin:/usr/local/opt/node/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin}
PROXY_HOST=${PROXY_HOST:-127.0.0.1}
PROXY_PORT=${PROXY_PORT:-4321}
PROXY_BASE_URL=${PROXY_BASE_URL:-"http://$PROXY_HOST:$PROXY_PORT"}

PATH="$PATH_DEFAULT"

curl -fsS "$PROXY_BASE_URL/health" >/tmp/openclaw-memory-health.json
curl -fsS "$PROXY_BASE_URL/v1/models" >/tmp/openclaw-memory-models.json
/usr/local/bin/openclaw config validate >/tmp/openclaw-memory-config.txt
/usr/local/bin/openclaw engram doctor --json >/tmp/openclaw-memory-doctor.json 2>/tmp/openclaw-memory-doctor.err
/usr/local/bin/openclaw engram search Voyager -n 3 >/tmp/openclaw-memory-search.txt 2>/tmp/openclaw-memory-search.err

if grep -q "database is locked" /tmp/openclaw-memory-doctor.json /tmp/openclaw-memory-doctor.err /tmp/openclaw-memory-search.txt /tmp/openclaw-memory-search.err; then
  echo "database lock detected during verification" >&2
  exit 1
fi

echo "== Proxy health =="
cat /tmp/openclaw-memory-health.json
echo
echo "== Models =="
cat /tmp/openclaw-memory-models.json
echo
echo "== Doctor stderr =="
cat /tmp/openclaw-memory-doctor.err
echo
echo "== Search stderr =="
cat /tmp/openclaw-memory-search.err
echo
echo "== LCM holders =="
lsof "$OPENCLAW_HOME/lcm.db" "$OPENCLAW_HOME/lcm.db-shm" "$OPENCLAW_HOME/lcm.db-wal" || true

