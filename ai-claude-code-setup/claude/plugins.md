# Claude Code Plugins

Snapshot of installed plugins and how to install them.

## Plugins in use

| Plugin | Marketplace | Version | Purpose |
|--------|-------------|---------|---------|
| `typescript-lsp` | `claude-plugins-official` | 1.0.0 | TypeScript LSP |
| `pyright-lsp` | `claude-plugins-official` | 1.0.0 | Python LSP |
| `rust-analyzer-lsp` | `claude-plugins-official` | 1.0.0 | Rust LSP |
| `gopls-lsp` | `claude-plugins-official` | 1.0.0 | Go LSP |
| `solidity-lsp` | `local-lsp` | 1.0.0 | Solidity LSP (local marketplace) |
| `flutter-lsp` | `local-lsp` | 1.0.0 | Flutter/Dart LSP (local marketplace) |
| `claude-mem` | `thedotmack` | 10.6.2 | **Primary memory system** |

## Install commands

```bash
# Official LSP plugins (no setup needed)
claude plugins install typescript-lsp@claude-plugins-official
claude plugins install pyright-lsp@claude-plugins-official
claude plugins install rust-analyzer-lsp@claude-plugins-official
claude plugins install gopls-lsp@claude-plugins-official

# Solidity + Flutter: local marketplace
# Requires ~/.claude/plugins-marketplace/ with solidity-lsp/ and flutter-lsp/ dirs
claude plugins marketplace add ~/.claude/plugins-marketplace
claude plugins install solidity-lsp@local-lsp
claude plugins install flutter-lsp@local-lsp

# Primary memory plugin
claude plugins marketplace add thedotmack/claude-mem
claude plugins install claude-mem@thedotmack
```

---

## claude-mem — primary memory (required)

claude-mem hooks into every Claude Code session and automatically extracts + injects memory.

### How it works
- `SessionStart` hook → injects N recent session memories into context
- `PostToolUse` hook → extracts new facts after each tool use
- Data: SQLite (`~/.claude-mem/claude-mem.db`) + ChromaDB vector index (`~/.claude-mem/chroma/`)

### After install: restart from fresh terminal
```bash
# claude-mem hooks only activate in new sessions
# Open a new terminal, then:
claude
```

### Config file: `~/.claude-mem/settings.json`
See `claude-mem-settings.json` in this repo for a full snapshot. Key settings:

```json
{
  "CLAUDE_MEM_MODEL": "claude-sonnet-4-6",
  "CLAUDE_MEM_PROVIDER": "claude",
  "CLAUDE_MEM_CLAUDE_AUTH_METHOD": "cli",
  "CLAUDE_MEM_MODE": "code",
  "CLAUDE_MEM_CONTEXT_SESSION_COUNT": "10",
  "CLAUDE_MEM_CHROMA_ENABLED": "true",
  "CLAUDE_MEM_CHROMA_MODE": "local"
}
```

### ⚠️ Disable Claude Code's built-in memory

Claude Code has its own built-in memory that conflicts with claude-mem. The `settings.json` in this repo already has it disabled:

```json
{
  "memory": {
    "enabled": false
  }
}
```

If you need to set it manually:
```bash
claude config set --global memory.enabled false
```

Without this, both systems write simultaneously → duplicate/conflicting memory.
