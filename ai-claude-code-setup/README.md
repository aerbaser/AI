# Claude Code AI Development Setup

Complete environment setup for Claude Code with Web2/Web3 AI development.

> This folder is a reproducible setup snapshot from a working Mac environment. JSON configs are redacted where secrets could exist.

## Workspace Structure

```text
~/Desktop/AI/
├── Web2/          # Web2 projects (codebase-memory MCP)
├── Web3/          # Web3/Solidity projects (Serena MCP)
└── .claude/       # Shared Claude hooks and settings
```

## Stack

- **Claude Code** — AI coding assistant
- **GSD (get-shit-done-cc)** — Autonomous development workflow
- **Context7** — Live library documentation
- **MCP Servers**: Engram (memory), Serena (Web3), codebase-memory (Web2)
- **LSP Plugins**: TypeScript, Pyright, Rust Analyzer, gopls, Solidity, Flutter

## Quick Start

1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`
2. Install GSD: `npx get-shit-done-cc --claude --local` (in project dir)
3. Copy `claude/CLAUDE.md` → `~/.claude/CLAUDE.md`
4. Copy `claude/settings.json` → `~/.claude/settings.json` (add your tokens if needed)
5. Set up MCP servers (see `mcp/README.md`)

See `SETUP.md` for the full step-by-step installation flow.
