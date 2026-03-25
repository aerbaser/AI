# OpenClaw Engram Memory Toolkit

Public toolkit for deploying the memory stack described in this workspace:

- `openclaw-engram` for memory capture and retrieval
- upstream `qmd` with a thin Voyager embeddings overlay
- a local OpenAI-compatible proxy backed by `codex exec`
- macOS `launchd` automation for the proxy and overlay auto-apply path

This repository does not ship any personal `Engram/QMD` memory state. It only ships the toolkit required to reproduce the stack on another machine.

## What this installs

- Codex-backed chat/completions proxy on `127.0.0.1:4321`
- `Voyager` embeddings for QMD
- upstream-first `openclaw-engram` / `qmd` overlay patching
- quality-first memory defaults:
  - `gpt-5.4-mini` for Engram write-path
  - `Voyager voyage-4-large` for embeddings
  - `lcmEnabled = false`
  - `qmdEnabled = true`
  - `qmdDaemonEnabled = true`
  - `captureMode = hybrid`
  - `recallBudgetChars = 80000`

## Quick start

```bash
git clone https://github.com/aerbaser/AI.git
cd AI/openclaw-engram-memory-toolkit

export VOYAGE_API_KEY="your-voyage-key"
export CODEX_MODEL="gpt-5.4-mini"

./install/bootstrap.sh
./install/verify.sh
```

If you want the exact recommended settings used in this rollout, read [docs/llm-recommendations.md](docs/llm-recommendations.md) first.

## Repository layout

- `proxy/`: Codex-backed OpenAI-compatible proxy
- `overlay/`: Voyager/QMD/OpenClaw overlay script
- `install/`: bootstrap, update, verify, uninstall
- `templates/`: launchd templates and config snippets
- `docs/`: architecture, installation, troubleshooting, LLM guidance

This toolkit now lives as a subdirectory inside the `AI` repository rather than as a standalone branch root.

## Requirements

- macOS with `launchd`
- `openclaw` already installed
- `codex` CLI already installed and authenticated
- Node.js available at `/usr/local/bin/node`
- Python 3 available at `/usr/bin/python3`
- `Voyager` API key

## Security model

This repository is intentionally public-friendly:

- no private memory state
- no personal transcripts
- no real auth tokens in committed files
- no live API keys

The installer generates local auth tokens and writes host-specific values into `~/.openclaw/openclaw.json`.

## Install/update flow

- First install: [docs/install-macos.md](docs/install-macos.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- LLM settings: [docs/llm-recommendations.md](docs/llm-recommendations.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
