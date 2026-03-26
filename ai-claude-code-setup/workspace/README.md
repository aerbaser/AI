# Workspace Layout

This setup separates projects by lane while keeping one shared Claude/GSD control plane.

## Root

```text
~/Desktop/AI/
├── .claude/
├── Web2/
└── Web3/
```

## Why this layout works

- `~/Desktop/AI/.claude/` holds shared hooks and status line config.
- `~/Desktop/AI/Web2/` holds Web2 repos and the `codebase-memory` MCP config.
- `~/Desktop/AI/Web3/` holds Web3 repos and the `serena` MCP config.
- Each project can still carry its own `.planning/` folder for GSD.

## Included snapshot files

- `settings.json` — shared workspace Claude hooks config
- `AI-folder-structure.md` — visual structure reference
