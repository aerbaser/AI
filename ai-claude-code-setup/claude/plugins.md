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
