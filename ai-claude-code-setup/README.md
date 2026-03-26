# Claude Code AI Development Setup

Complete, reproducible environment setup for Claude Code — Web2 + Web3 AI development on macOS.

> Copy of a working Mac environment. All secrets redacted. Follow SETUP.md in order.

---

## Full stack overview

```
Claude Code (editor AI)
├── Memory:    claude-mem plugin (primary)  ← hooks inject memory on every session
├── MCP:       Engram HTTP MCP (optional, OpenClaw-powered, cross-session memory)
├── Workflow:  GSD2 (gsd-pi) — standalone autonomous coding agent (Pi SDK)
├── Legacy:    GSD v1 (get-shit-done-cc) — prompt framework (still installed, parallel)
├── Docs:      Context7 (ctx7) — live library docs on demand
├── LSP:       TypeScript, Pyright, Rust Analyzer, gopls, Solidity, Flutter
└── Per-workspace MCP:
    ├── Web2/  → codebase-memory-mcp (auto-indexes repo)
    └── Web3/  → Serena (semantic Solidity/code nav)
```

## Workspace layout

```
~/Desktop/AI/
├── .claude/
│   ├── settings.json      # GSD v1 hooks (SessionStart, PreToolUse, PostToolUse, statusLine)
│   ├── hooks/             # GSD v1 hook scripts (auto-installed by GSD v1)
│   ├── agents/            # GSD v1 sub-agents
│   ├── get-shit-done/     # GSD v1 installation
│   └── commands/gsd/      # 57 GSD v1 slash commands (symlinked)
├── Web2/
│   ├── .mcp.json          # codebase-memory MCP (per project dir)
│   └── [projects]/
└── Web3/
    ├── .mcp.json          # Serena MCP (per project dir)
    └── [projects]/
        └── .planning/     # GSD v1 planning files (auto-created by /gsd:plan)
```

## What's in this folder

| Path | Source | Purpose |
|------|--------|---------|
| `claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | Global Claude instructions (Context7, defaults) |
| `claude/settings.json` | `~/.claude/settings.json` | Plugins, hooks, effortLevel, memory disabled |
| `claude/plugins.md` | manual | Plugin install commands |
| `claude/claude-mem-settings.json` | `~/.claude-mem/settings.json` | claude-mem config snapshot |
| `mcp/global.json` | `~/.claude.json` (mcpServers) | Engram MCP (global, optional) |
| `mcp/web2.json` | `~/Desktop/AI/Web2/.mcp.json` | codebase-memory MCP |
| `mcp/web3.json` | `~/Desktop/AI/Web3/.mcp.json` | Serena MCP |
| `gsd/README.md` | manual | GSD2 + GSD v1 setup guide |
| `gsd/settings.json` | `~/.gsd/agent/settings.json` | GSD global agent config (shared) |
| `gsd/project-config-example.json` | `.planning/config.json` | GSD v1 per-project config example |
| `workspace/settings.json` | `~/Desktop/AI/.claude/settings.json` | Shared workspace hooks (GSD v1) |

## Key notes

- **GSD2** (`gsd-pi`) is the primary workflow tool — standalone CLI agent with DB state, crash recovery, auto-advance.
- **GSD v1** (`get-shit-done-cc`) is still installed in parallel — its hooks remain active in Claude Code.
- **`claude/settings.json`** has `"memory": { "enabled": false }` — required to prevent conflict with claude-mem.
- **Engram MCP** is optional. Skip if you're not running OpenClaw.

## Quick start

```bash
# 1. Install Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Install GSD2 (primary workflow)
npm install -g gsd-pi@latest
gsd --version   # should show v2.x

# 3. Install GSD v1 (hooks + slash commands for Claude Code)
cd ~/Desktop/AI && npx get-shit-done-cc --claude --local

# 4. Workspace
mkdir -p ~/Desktop/AI/{Web2,Web3,.claude} ~/.claude

# 5. Copy configs
cp claude/CLAUDE.md ~/.claude/CLAUDE.md
cp claude/settings.json ~/.claude/settings.json
sed -i '' "s|\$HOME|$HOME|g" ~/.claude/settings.json

# 6. Install plugins
claude plugins marketplace add thedotmack/claude-mem
claude plugins install claude-mem@thedotmack
# ... see claude/plugins.md for full list

# 7. MCP servers
cp mcp/web2.json ~/Desktop/AI/Web2/.mcp.json
cp mcp/web3.json ~/Desktop/AI/Web3/.mcp.json

# 8. Restart Claude Code from a fresh terminal
```

See **SETUP.md** for full step-by-step with verification commands.
