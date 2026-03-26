# MCP Servers

Three MCP layers for this environment. Each operates at a different scope.

---

## 1. Engram — global memory MCP (optional)

**Scope:** global (`~/.claude.json`)  
**Purpose:** Long-term memory across Claude Code sessions, powered by OpenClaw + Engram  
**Transport:** HTTP  
**Endpoint:** `http://127.0.0.1:4318/mcp`  
**Auth:** Bearer token via `OPENCLAW_ENGRAM_ACCESS_TOKEN`

Config file in this repo: `global.json` → merge into `~/.claude.json` under `mcpServers`

> ⚠️ Engram requires OpenClaw running with the Engram plugin. See SETUP.md memory section.  
> Skip this entirely if you're not using OpenClaw.

---

## 2. codebase-memory — Web2 projects

**Scope:** `~/Desktop/AI/Web2/.mcp.json`  
**Purpose:** Auto-indexes Web2 project codebases for context-aware retrieval  
**Transport:** stdio  
**Binary:** `~/.local/bin/codebase-memory-mcp`

Config file in this repo: `web2.json` → copy to `~/Desktop/AI/Web2/.mcp.json`

```bash
cp web2.json ~/Desktop/AI/Web2/.mcp.json
```

---

## 3. Serena — Web3 / Solidity projects

**Scope:** `~/Desktop/AI/Web3/.mcp.json`  
**Purpose:** Semantic code navigation for Solidity / Web3 projects  
**Transport:** stdio via uvx  
**Launch:** `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project-from-cwd`

Config file in this repo: `web3.json` → copy to `~/Desktop/AI/Web3/.mcp.json`

```bash
cp web3.json ~/Desktop/AI/Web3/.mcp.json
```

---

## Memory architecture

```
Claude Code session
        │
        ├─► claude-mem plugin (primary, automatic)
        │        └─► ~/.claude-mem/ (SQLite + ChromaDB local)
        │
        └─► Engram MCP HTTP (optional, OpenClaw)
                 └─► ~/.openclaw/workspace/memory/local/
                          └─► QMD vector index (Qwen3 embeddings)
```

- **claude-mem**: hooks into every session automatically, no manual calls needed
- **Engram**: explicit memory via MCP tools, shared across all agents in the OpenClaw system
- Both systems are independent. Do not enable both without understanding the overlap.
