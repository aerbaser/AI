# Setup Guide

Step-by-step install for the full Claude Code AI development environment.

---

## Prerequisites

- macOS
- Node.js 18+ (`brew install node`)
- Python 3.10+ (`brew install python`)
- Go (`brew install go`) — for gopls
- `brew` (Homebrew)

---

## Step 1 — Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

---

## Step 2 — Create workspace layout

```bash
mkdir -p ~/Desktop/AI/{Web2,Web3,.claude}
mkdir -p ~/.claude
```

---

## Step 3 — Copy global Claude config

```bash
cp ai-claude-code-setup/claude/CLAUDE.md ~/.claude/CLAUDE.md
```

Review `claude/CLAUDE.md` — it sets defaults for Context7 and working style.

---

## Step 4 — Copy Claude settings (plugins + hooks + memory off)

```bash
cp ai-claude-code-setup/claude/settings.json ~/.claude/settings.json
```

> ⚠️ The settings file has `"memory": { "enabled": false }`. This is intentional — it disables Claude Code's built-in memory so it doesn't conflict with claude-mem.

> ⚠️ Hook paths use `$HOME` — Claude Code requires absolute paths. After copy, run:
```bash
# Replace $HOME with your actual home dir in the hooks
sed -i '' "s|\$HOME|$HOME|g" ~/.claude/settings.json
```

---

## Step 5 — Install GSD2 + GSD v1

### GSD2 (primary — standalone autonomous agent)

```bash
npm install -g gsd-pi@latest
gsd --version   # v2.50.0+
```

GSD2 runs as its own CLI process, independent of Claude Code. See `gsd/README.md` for usage.

### GSD v1 (hooks + slash commands for Claude Code)

```bash
cd ~/Desktop/AI
npx get-shit-done-cc --claude --local
```

This installs:
- `~/Desktop/AI/.claude/` — GSD v1 workspace with hooks, agents, commands
- `~/.claude/hooks/*.js` — GSD v1 hooks (SessionStart, PreToolUse, PostToolUse, statusLine)
- `~/.claude/commands/gsd/` — 57 GSD v1 slash commands

> ✅ After this, `workspace/settings.json` in this repo matches `~/Desktop/AI/.claude/settings.json` exactly.

Copy the workspace-level settings:
```bash
cp ai-claude-code-setup/workspace/settings.json ~/Desktop/AI/.claude/settings.json
```

---

## Step 6 — Install LSP and memory plugins

```bash
# Official LSP plugins
claude plugins install typescript-lsp@claude-plugins-official
claude plugins install pyright-lsp@claude-plugins-official
claude plugins install rust-analyzer-lsp@claude-plugins-official
claude plugins install gopls-lsp@claude-plugins-official

# Local marketplace (Solidity, Flutter)
# First create ~/.claude/plugins-marketplace with solidity-lsp and flutter-lsp plugin dirs
# (download from their repos or copy from another machine)
claude plugins marketplace add ~/.claude/plugins-marketplace
claude plugins install solidity-lsp@local-lsp
claude plugins install flutter-lsp@local-lsp

# Memory plugin (primary memory system)
claude plugins marketplace add thedotmack/claude-mem
claude plugins install claude-mem@thedotmack
```

**claude-mem requires a fresh terminal restart after install** — hooks only activate in new sessions.

Configure claude-mem:
```bash
# Copy settings snapshot (review and adjust)
cp ai-claude-code-setup/claude/claude-mem-settings.json ~/.claude-mem/settings.json
# Or configure interactively:
claude mcp settings claude-mem
```

Key settings in `claude-mem-settings.json`:
- `CLAUDE_MEM_MODEL` — model for memory extraction (e.g. `claude-sonnet-4-6`)
- `CLAUDE_MEM_MODE` — `code` for development workflows
- `CLAUDE_MEM_CHROMA_ENABLED` — `true` for vector search (requires ChromaDB running)
- `CLAUDE_MEM_CONTEXT_SESSION_COUNT` — how many past sessions to inject

---

## Step 7 — Set up MCP servers

### Web2 projects (codebase-memory)

Install binary:
```bash
# Download from https://github.com/shaneholloman/codebase-memory-mcp/releases
# or build from source, place at:
~/.local/bin/codebase-memory-mcp
chmod +x ~/.local/bin/codebase-memory-mcp
```

Copy config:
```bash
cp ai-claude-code-setup/mcp/web2.json ~/Desktop/AI/Web2/.mcp.json
```

### Web3 projects (Serena)

Install uvx:
```bash
pip install uv
# uvx is available as uv tool run or install uv globally
pip install uvx   # or: curl -LsSf https://astral.sh/uv/install.sh | sh
# Binary should be at ~/.local/bin/uvx
```

Copy config:
```bash
cp ai-claude-code-setup/mcp/web3.json ~/Desktop/AI/Web3/.mcp.json
```

### Engram MCP (optional — OpenClaw memory)

Only needed if you're running OpenClaw. Skip otherwise.

See **Memory section** below for full OpenClaw + Engram setup.

If setting up Engram:
```bash
# Get token after Engram is running:
openclaw engram access token

# Add to ~/.zshrc and ~/.zprofile:
export OPENCLAW_ENGRAM_ACCESS_TOKEN=<your_token>
```

Copy config to `~/.claude.json` (merge into existing `mcpServers`):
```bash
# Contents of mcp/global.json go into ~/.claude.json under "mcpServers"
```

---

## Step 8 — Set environment variables

Add to `~/.zshrc` AND `~/.zprofile`:

```bash
export ANTHROPIC_API_KEY=<your_anthropic_key>
export OPENCLAW_ENGRAM_ACCESS_TOKEN=<your_token>   # only if using Engram
```

Reload:
```bash
source ~/.zshrc && source ~/.zprofile
```

> ⚠️ Claude Code must be launched from a terminal that has sourced these files. If memory/MCP isn't working, restart from a fresh terminal.

---

## Step 9 — Install required language tools

```bash
# TypeScript LSP
npm install -g typescript typescript-language-server

# Python LSP
npm install -g pyright

# Go LSP
go install golang.org/x/tools/gopls@latest

# Rust analyzer
# macOS: brew install rust-analyzer
# or: rustup component add rust-analyzer

# Flutter / Dart
brew install --cask flutter
```

---

## Step 10 — Configure GSD per project

For each project that uses GSD:

```bash
mkdir -p ~/Desktop/AI/Web3/<project>/.planning
cp ai-claude-code-setup/gsd/project-config-example.json \
   ~/Desktop/AI/Web3/<project>/.planning/config.json
```

Edit the config — key fields:
- `verification_commands` — list of commands to run after each phase (forge, tsc, tests, etc.)
- `mode` — `yolo` for autonomous, `discuss` for interactive
- `git.isolation` — `worktree` for isolated branch per phase

Start GSD in project dir:
```bash
cd ~/Desktop/AI/Web3/<project>
/gsd:plan "describe what to build"
```

---

## Memory: OpenClaw + Engram (optional)

OpenClaw is a separate AI agent runtime. Engram is its memory plugin. Together they provide persistent memory across Claude Code sessions via MCP.

This is separate from claude-mem. Use if you want:
- Memory shared across multiple AI agents (not just Claude Code)
- Memory accessible via HTTP MCP from any client

### Install

```bash
npm install -g openclaw
openclaw setup
openclaw plugins install @joshuaswarren/openclaw-engram
```

Configure `~/.openclaw/openclaw.json`:
```json
{
  "plugins": {
    "slots": {
      "memory": "openclaw-engram"
    }
  }
}
```

### Start Engram MCP

```bash
openclaw engram access http-serve
# Runs at http://127.0.0.1:4318/mcp
```

For persistence (macOS LaunchAgent):
```bash
cat > ~/Library/LaunchAgents/com.openclaw.engram-mcp.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.openclaw.engram-mcp</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/openclaw</string>
    <string>engram</string><string>access</string><string>http-serve</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.openclaw.engram-mcp.plist
```

Verify:
```bash
openclaw status         # → Memory: enabled (plugin openclaw-engram)
openclaw engram doctor  # → all checks green
```

---

## Verification checklist

```bash
claude --version                                        # Claude Code installed
claude plugins list                                     # claude-mem, LSPs all enabled
cat ~/.claude/settings.json | grep '"enabled": false'  # memory disabled ✓
cat ~/.claude/CLAUDE.md                                 # instructions present
cat ~/Desktop/AI/Web2/.mcp.json                         # codebase-memory config
cat ~/Desktop/AI/Web3/.mcp.json                         # serena config
ls ~/Desktop/AI/.claude/hooks/                          # GSD hooks present
test -f ~/.gsd/agent/settings.json && echo ok           # GSD agent config
```

---

## What is auto-generated vs what to copy manually

| Item | How it appears |
|------|---------------|
| `~/.claude/hooks/*.js` | **Auto-installed by GSD** — do not copy manually |
| `~/.claude/commands/gsd/` | **Auto-installed by GSD** — symlinked |
| `~/.claude-mem/` (all) | **Auto-created by claude-mem** on first run |
| `~/.claude/settings.json` | **Copy from repo** → `claude/settings.json` |
| `~/.claude/CLAUDE.md` | **Copy from repo** → `claude/CLAUDE.md` |
| `~/Desktop/AI/Web2/.mcp.json` | **Copy from repo** → `mcp/web2.json` |
| `~/Desktop/AI/Web3/.mcp.json` | **Copy from repo** → `mcp/web3.json` |
| `~/Desktop/AI/.claude/settings.json` | **Copy from repo** → `workspace/settings.json` |
| `~/.gsd/agent/settings.json` | **Copy from repo** → `gsd/settings.json` |
| `.planning/config.json` | **Copy from repo** → `gsd/project-config-example.json` |
