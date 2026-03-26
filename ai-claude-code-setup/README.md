# Claude Code AI Development Setup

Complete, reproducible environment setup for Claude Code — Web2 + Web3 AI development on macOS.

> Copy of a working Mac environment. All secrets redacted. Follow SETUP.md in order.

---

## Full stack overview

```
Claude Code (editor AI)
├── Memory:    claude-mem plugin (primary)  ← hooks inject memory on every session
├── MCP:       Engram HTTP MCP (optional, OpenClaw-powered, cross-session memory)
├── Workflow:  GSD (get-shit-done-cc) — autonomous multi-phase development
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
│   ├── settings.json      # GSD hooks (SessionStart, PreToolUse, PostToolUse, statusLine)
│   ├── hooks/             # GSD hook scripts (auto-installed by GSD)
│   ├── agents/            # GSD sub-agents
│   ├── get-shit-done/     # GSD installation
│   └── commands/gsd/      # 57 GSD slash commands (symlinked)
├── Web2/
│   ├── .mcp.json          # codebase-memory MCP (per project dir)
│   └── [projects]/
└── Web3/
    ├── .mcp.json          # Serena MCP (per project dir)
    └── [projects]/
        └── .planning/     # GSD planning files (auto-created by GSD)
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
| `gsd/settings.json` | `~/.gsd/agent/settings.json` | GSD global agent config |
| `gsd/project-config-example.json` | `.planning/config.json` | GSD per-project config example |
| `workspace/settings.json` | `~/Desktop/AI/.claude/settings.json` | Shared workspace hooks |

## Key notes

- **GSD hooks** (`~/.claude/hooks/*.js`) are auto-installed when you run GSD — do NOT copy them manually.
- **`claude/settings.json`** has `"memory": { "enabled": false }` — required to prevent conflict with claude-mem.
- **Engram MCP** is optional. It's the OpenClaw AI agent's memory system. Skip if you're not running OpenClaw.
- **`~/.local/bin/uvx`** is installed via `pip install uv` → `uv tool install` or `pip install uvx`.
- **`~/.local/bin/codebase-memory-mcp`** — binary, see `env/required-tools.md` for install.

## Quick start

```bash
# 1. Install Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Workspace
mkdir -p ~/Desktop/AI/{Web2,Web3,.claude} ~/.claude

# 3. Copy configs
cp claude/CLAUDE.md ~/.claude/CLAUDE.md
cp claude/settings.json ~/.claude/settings.json   # review and replace $HOME placeholders

# 4. Install GSD (runs in your AI project root)
cd ~/Desktop/AI && npx get-shit-done-cc --claude --local

# 5. Install plugins
claude plugins marketplace add thedotmack/claude-mem
claude plugins install claude-mem@thedotmack
claude plugins install typescript-lsp@claude-plugins-official
# ... see claude/plugins.md for full list

# 6. MCP servers
cp mcp/web2.json ~/Desktop/AI/Web2/.mcp.json
cp mcp/web3.json ~/Desktop/AI/Web3/.mcp.json
# For Engram (optional): see SETUP.md memory section

# 7. Restart Claude Code from a fresh terminal
```

See **SETUP.md** for full step-by-step with verification commands.
