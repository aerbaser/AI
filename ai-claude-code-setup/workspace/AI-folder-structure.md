# AI Workspace Structure

```
~/Desktop/AI/
│
├── .claude/                              # GSD workspace (auto-created by GSD)
│   ├── settings.json                     # Workspace-level hooks (relative paths)
│   ├── hooks/                            # GSD hook scripts (JS)
│   │   ├── gsd-check-update.js
│   │   ├── gsd-context-monitor.js
│   │   ├── gsd-prompt-guard.js
│   │   ├── gsd-statusline.js
│   │   └── gsd-workflow-guard.js
│   ├── agents/                           # GSD sub-agents (planner, executor, etc.)
│   ├── commands/
│   │   └── gsd -> ../get-shit-done/commands/gsd/  # symlink to 57 GSD slash commands
│   └── get-shit-done/                    # GSD installation
│       ├── commands/gsd/                 # actual command files
│       └── ...
│
├── Web2/                                 # Web2 / traditional web projects
│   ├── .mcp.json                         # codebase-memory MCP (active for all projects here)
│   └── [project-name]/
│       └── ...
│
└── Web3/                                 # Web3 / Solidity / blockchain projects
    ├── .mcp.json                         # Serena MCP (active for all projects here)
    └── [project-name]/
        ├── .planning/                    # GSD planning files (auto-created by /gsd:plan)
        │   ├── config.json               # GSD project config (verification_commands etc)
        │   ├── phases/                   # phase definitions
        │   └── state.json                # current GSD state
        └── ...
```

## MCP scope rules

Claude Code applies `.mcp.json` from the current working directory upward. This means:

- Open Claude Code from `~/Desktop/AI/Web2/my-project/` → `Web2/.mcp.json` is active → codebase-memory enabled
- Open from `~/Desktop/AI/Web3/dao-project/` → `Web3/.mcp.json` is active → Serena enabled
- Global `~/.claude.json` → Engram MCP active in all sessions (if configured)

## Key principle

Each "lane" (Web2 / Web3) has its own MCP config and project type. Don't mix them — Serena is Solidity-aware and useless for Web2 projects; codebase-memory is generic and works anywhere.
