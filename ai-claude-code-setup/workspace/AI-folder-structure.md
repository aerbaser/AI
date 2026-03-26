# AI Workspace Structure

```text
~/Desktop/AI/
├── .claude/
│   ├── settings.json     # GSD hooks (SessionStart, PostToolUse, PreToolUse)
│   ├── agents/           # GSD sub-agents (gsd-planner, gsd-executor, etc.)
│   ├── commands/gsd -> get-shit-done/commands/
│   └── get-shit-done/    # GSD installation
├── Web2/
│   ├── .mcp.json         # codebase-memory MCP
│   └── [projects]
└── Web3/
    ├── .mcp.json         # Serena MCP
    └── [projects]/
        └── .planning/    # GSD planning files per project
```
