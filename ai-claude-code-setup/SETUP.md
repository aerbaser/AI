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
