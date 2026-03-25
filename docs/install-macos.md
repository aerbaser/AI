# Install on macOS

## Prerequisites

- `openclaw` installed and already working
- `codex` installed and authenticated
- `node` at `/usr/local/bin/node`
- `python3` at `/usr/bin/python3`
- valid `VOYAGE_API_KEY`

## 1. Clone the repository

```bash
git clone https://github.com/aerbaser/AI.git
cd AI
git checkout openclaw-engram-memory-toolkit
```

## 2. Export required variables

```bash
export VOYAGE_API_KEY="your-voyage-key"
export CODEX_MODEL="gpt-5.4-mini"
```

Optional overrides:

```bash
export OPENCLAW_HOME="$HOME/.openclaw"
export TOOLKIT_ROOT="$HOME/.openclaw/toolkit/openclaw-engram-memory-toolkit"
export PROXY_HOST="127.0.0.1"
export PROXY_PORT="4321"
```

## 3. Run bootstrap

```bash
./install/bootstrap.sh
```

Bootstrap will:

- copy proxy runtime into `~/.openclaw/toolkit/openclaw-engram-memory-toolkit`
- install `overlay/apply_memory_overlay.py` into `~/.openclaw/bin`
- patch `~/.openclaw/openclaw.json`
- write two LaunchAgents
- apply the memory overlay
- start the proxy and overlay services

## 4. Verify

```bash
./install/verify.sh
```

Expected outcomes:

- proxy health endpoint returns `ok: true`
- `openclaw config validate` passes
- `openclaw engram doctor --json` exits successfully
- `openclaw engram search Voyager -n 3` exits successfully
- no `database is locked` in verification output

## 5. Update later

```bash
git pull
./install/update.sh
```

## 6. Remove if needed

```bash
./install/uninstall.sh
```
