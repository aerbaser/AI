# Claude Code Plugins

Installed plugin snapshot from this Mac.

## Installed plugins

- `typescript-lsp@claude-plugins-official` (v1.0.0)
- `pyright-lsp@claude-plugins-official` (v1.0.0)
- `rust-analyzer-lsp@claude-plugins-official` (v1.0.0)
- `gopls-lsp@claude-plugins-official` (v1.0.0)
- `solidity-lsp@local-lsp` (v1.0.0)
- `flutter-lsp@local-lsp` (v1.0.0)
- `claude-mem@thedotmack` (v10.6.2)

## Install commands

```bash
# Official marketplace LSP plugins
claude plugins install typescript-lsp@claude-plugins-official
claude plugins install pyright-lsp@claude-plugins-official
claude plugins install rust-analyzer-lsp@claude-plugins-official
claude plugins install gopls-lsp@claude-plugins-official

# Local marketplace plugins (requires ~/.claude/plugins-marketplace)
claude plugins marketplace add ~/.claude/plugins-marketplace
claude plugins install solidity-lsp@local-lsp
claude plugins install flutter-lsp@local-lsp

# Community plugin
claude plugins marketplace add thedotmack/claude-mem
claude plugins install claude-mem@thedotmack
```

## Notes

- Official LSP plugins are sourced from `claude-plugins-official`.
- `local-lsp` points to `~/.claude/plugins-marketplace` on this machine.
- `claude-mem` comes from the `thedotmack/claude-mem` marketplace.

---

## Memory: claude-mem (primary)

**claude-mem** is the primary memory system for this setup. Engram (OpenClaw) is optional/separate.

### Install

```bash
claude plugins marketplace add thedotmack/claude-mem
claude plugins install claude-mem@thedotmack
```

Requires a fresh terminal restart after install so hooks activate.

### Config

Settings live at `~/.claude-mem/settings.json`. Key values used in this setup:

```json
{
  "CLAUDE_MEM_MODEL": "claude-sonnet-4-6",
  "CLAUDE_MEM_PROVIDER": "claude",
  "CLAUDE_MEM_CLAUDE_AUTH_METHOD": "cli",
  "CLAUDE_MEM_MODE": "code",
  "CLAUDE_MEM_CONTEXT_OBSERVATIONS": "50",
  "CLAUDE_MEM_CONTEXT_SESSION_COUNT": "10",
  "CLAUDE_MEM_CHROMA_ENABLED": "true",
  "CLAUDE_MEM_CHROMA_MODE": "local",
  "CLAUDE_MEM_FOLDER_CLAUDEMD_ENABLED": "false",
  "CLAUDE_MEM_SKIP_TOOLS": "ListMcpResourcesTool,SlashCommand,Skill,TodoWrite,AskUserQuestion"
}
```

Data stored at `~/.claude-mem/` (SQLite + Chroma vector DB).

### Disable Claude Code's built-in local memory

Claude Code has its own built-in memory that conflicts with claude-mem. Disable it in `~/.claude/settings.json`:

```json
{
  "memory": {
    "enabled": false
  }
}
```

Or via CLI:
```bash
claude config set --global memory.enabled false
```

> ⚠️ Without disabling the built-in memory, you'll get duplicate/conflicting memory writes from both systems.
