# Setup Guide

Step-by-step install guide for the Claude Code environment captured in this repository.

## 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

## 2. Create the workspace layout

```bash
mkdir -p ~/Desktop/AI/{Web2,Web3,.claude}
mkdir -p ~/.claude
```

## 3. Install GSD

```bash
cd ~/Desktop/AI
npx get-shit-done-cc --claude --local
```

This machine is running GSD version `1.29.0`.

## 4. Configure global `CLAUDE.md`

Copy `claude/CLAUDE.md` to:

```bash
cp ai-claude-code-setup/claude/CLAUDE.md ~/.claude/CLAUDE.md
```

## 5. Configure Claude settings

Copy `claude/settings.json` to:

```bash
cp ai-claude-code-setup/claude/settings.json ~/.claude/settings.json
```

Then review:
- hooks
- enabled plugins
- status line
- any redacted tokens or keys

## 6. Install LSP and helper plugins

See `claude/plugins.md`, then run:

```bash
claude plugins install typescript-lsp@claude-plugins-official
claude plugins install pyright-lsp@claude-plugins-official
claude plugins install rust-analyzer-lsp@claude-plugins-official
claude plugins install gopls-lsp@claude-plugins-official
claude plugins marketplace add ~/.claude/plugins-marketplace
claude plugins install solidity-lsp@local-lsp
claude plugins install flutter-lsp@local-lsp
claude plugins marketplace add thedotmack/claude-mem
claude plugins install claude-mem@thedotmack
```

## 7. Configure MCP servers

- Copy `mcp/global.json` into the `mcpServers` section of `~/.claude.json`
- Copy `mcp/web2.json` to `~/Desktop/AI/Web2/.mcp.json`
- Copy `mcp/web3.json` to `~/Desktop/AI/Web3/.mcp.json`

Details: `mcp/README.md`

## 8. Set required environment variables

Add the required variables from `env/README.md` to both:
- `~/.zshrc`
- `~/.zprofile`

Reload your shell:

```bash
source ~/.zshrc
source ~/.zprofile
```

## 9. Configure shared workspace hooks

Copy `workspace/settings.json` to:

```bash
mkdir -p ~/Desktop/AI/.claude
cp ai-claude-code-setup/workspace/settings.json ~/Desktop/AI/.claude/settings.json
```

This enables shared `SessionStart`, `PreToolUse`, `PostToolUse`, and `statusLine` hooks for the AI workspace.

## 10. Configure GSD per project

Use `gsd/project-config-example.json` as a starting point for project-level planning config:

```bash
mkdir -p ~/Desktop/AI/Web3/<project>/.planning
cp ai-claude-code-setup/gsd/project-config-example.json ~/Desktop/AI/Web3/<project>/.planning/config.json
```

## Verification checklist

- `claude --version`
- `claude plugins list`
- `cat ~/Desktop/AI/Web2/.mcp.json`
- `cat ~/Desktop/AI/Web3/.mcp.json`
- `test -f ~/.claude/CLAUDE.md && echo ok`
- `test -f ~/.claude/settings.json && echo ok`
- `test -f ~/Desktop/AI/.claude/settings.json && echo ok`

## Included files

- `claude/` — global Claude config snapshot
- `mcp/` — MCP server definitions
- `gsd/` — GSD global and project config snapshot
- `workspace/` — shared workspace-level Claude settings
- `env/` — required environment variables and tool install list

---

## Memory: OpenClaw + Engram setup

This environment uses **OpenClaw** as the AI agent runtime with **Engram** as the persistent memory backend. This is separate from Claude Code itself — it provides long-term memory across sessions.

### What it is

- **OpenClaw** — self-hosted AI agent gateway (Node.js daemon, runs locally)
- **Engram** (`@joshuaswarren/openclaw-engram`) — memory plugin for OpenClaw
- **Engram MCP** — exposes memory over HTTP at `http://127.0.0.1:4318/mcp` so Claude Code can read/write long-term memory

### Install OpenClaw

```bash
npm install -g openclaw
openclaw setup
```

### Install Engram plugin

```bash
openclaw plugins install @joshuaswarren/openclaw-engram
```

Configure in `~/.openclaw/openclaw.json`:
```json
{
  "plugins": {
    "slots": {
      "memory": "openclaw-engram"
    }
  }
}
```

### Start Engram MCP HTTP server

```bash
openclaw engram access http-serve
```

Or use a LaunchAgent for persistence (recommended on macOS). Create `~/Library/LaunchAgents/com.openclaw.engram-mcp.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.openclaw.engram-mcp</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/openclaw</string>
    <string>engram</string>
    <string>access</string>
    <string>http-serve</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.engram-mcp.plist
```

### Connect Claude Code to Engram

Add to `~/.claude.json` under `mcpServers` (see `mcp/global.json`):

```json
{
  "mcpServers": {
    "engram": {
      "url": "http://127.0.0.1:4318/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_OPENCLAW_ENGRAM_ACCESS_TOKEN>"
      },
      "type": "http"
    }
  }
}
```

Get your token: `openclaw engram access token`

Set env var:
```bash
export OPENCLAW_ENGRAM_ACCESS_TOKEN=<your_token>
```

Restart Claude Code from a fresh terminal after setting env vars.

### Verify

```bash
openclaw status         # Memory: enabled (plugin openclaw-engram)
openclaw engram doctor  # All checks should pass
```

### QMD embeddings (optional — Qwen3 for multilingual)

For better multilingual recall, override the embedding model:

```bash
# Create wrapper
cat > ~/.openclaw/bin/qmd-qwen3 << 'EOF'
#!/bin/bash
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
exec qmd "$@"
EOF
chmod +x ~/.openclaw/bin/qmd-qwen3
```

Then point Engram's `qmdPath` to the wrapper in OpenClaw config.
