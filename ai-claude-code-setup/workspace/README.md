# Workspace Settings

Files in this folder relate to the shared `~/Desktop/AI/` workspace.

## workspace/settings.json

**Source:** `~/Desktop/AI/.claude/settings.json`  
**Purpose:** GSD hooks for all sessions opened inside the AI workspace

This is the workspace-level Claude settings file. It uses **relative paths** for hooks (e.g. `node .claude/hooks/gsd-check-update.js`) and is effective when Claude Code is opened from anywhere inside `~/Desktop/AI/`.

The global `~/.claude/settings.json` has the same hooks with absolute paths — both are needed.

## How to use

```bash
cp ai-claude-code-setup/workspace/settings.json ~/Desktop/AI/.claude/settings.json
```

After this, open Claude Code from inside `~/Desktop/AI/` and GSD hooks will activate.
