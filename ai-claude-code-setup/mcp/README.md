# MCP Servers

This environment uses three MCP layers.

## 1. `engram` (global)

- Purpose: memory / knowledge system
- Endpoint: `http://127.0.0.1:4318/mcp`
- Auth: `OPENCLAW_ENGRAM_ACCESS_TOKEN`
- Config file in this repo: `global.json`
- Target location: `~/.claude.json` → `mcpServers`

## 2. `codebase-memory` (Web2 projects)

- Purpose: auto-indexes and recalls codebase context for Web2 repos
- Transport: stdio
- Binary: `~/.local/bin/codebase-memory-mcp`
- Config file in this repo: `web2.json`
- Target location: `~/Desktop/AI/Web2/.mcp.json`

## 3. `serena` (Web3 projects)

- Purpose: semantic code navigation for Web3 / Solidity projects
- Transport: stdio via `uvx`
- Launch command: `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project-from-cwd`
- Config file in this repo: `web3.json`
- Target location: `~/Desktop/AI/Web3/.mcp.json`

## Notes

- `global.json` contains only the `mcpServers` section extracted from `~/.claude.json`.
- Secret-bearing values are redacted when necessary.
- Web2 and Web3 MCP files are directory-specific and meant to live at the workspace root for each lane.

---

## Memory architecture overview

```
Claude Code session
       │
       ▼
  Engram MCP (http://127.0.0.1:4318/mcp)
       │
       ▼
  OpenClaw + Engram plugin
       │
       ▼
  QMD (local vector index, Qwen3 embeddings)
       │
       ▼
  ~/.openclaw/workspace/memory/local/
```

- Session memory is persisted across restarts
- Works offline (local embeddings, no external API needed for memory)
- Engram token rotates — update `OPENCLAW_ENGRAM_ACCESS_TOKEN` if memory stops working
