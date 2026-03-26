# GSD — get-shit-done-cc

Autonomous multi-phase development workflow for Claude Code. GSD turns Claude into a structured coding agent that plans → executes → verifies in phases.

## Version

`1.29.0` (installed on this machine)

## Install

```bash
# Run from your project's workspace root (e.g. ~/Desktop/AI)
cd ~/Desktop/AI
npx get-shit-done-cc --claude --local
```

This creates:
- `~/Desktop/AI/.claude/` — GSD workspace
- `~/Desktop/AI/.claude/hooks/` — hook scripts (SessionStart, PreToolUse, PostToolUse, statusLine)
- `~/Desktop/AI/.claude/commands/gsd/` — 57 slash commands
- `~/.gsd/agent/settings.json` — global agent config
- `~/.claude/hooks/*.js` — hooks registered in Claude Code global settings

## Global agent config

`~/.gsd/agent/settings.json` (see `settings.json` in this folder):

```json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-sonnet-4-6",
  "defaultThinkingLevel": "high",
  "quietStartup": true,
  "collapseChangelog": true
}
```

## Per-project config

Each project gets `.planning/config.json`. See `project-config-example.json` for a full example.

Key fields:
```json
{
  "mode": "yolo",                    // "yolo" = autonomous, "discuss" = interactive
  "verification_commands": [...],    // run after each phase (tests, linters, etc.)
  "verification_auto_fix": true,     // auto-retry on failure
  "verification_max_retries": 2,
  "git": {
    "isolation": "worktree"          // isolated git worktree per phase
  }
}
```

## Slash commands

After install, available as `/gsd:*` in Claude Code:

```
/gsd:plan "describe what to build"    # creates phased plan
/gsd:execute-phase 1                  # executes phase 1
/gsd:autonomous                       # run all phases without stopping
/gsd:status                           # show current state
/gsd:verify                           # run verification commands
```

## Hooks

GSD installs 4 hooks in `~/.claude/hooks/`:

| Hook | Trigger | Purpose |
|------|---------|---------|
| `gsd-check-update.js` | SessionStart | Check for GSD updates |
| `gsd-context-monitor.js` | PostToolUse | Warn when context is filling up |
| `gsd-prompt-guard.js` | PreToolUse (Write/Edit) | Detect prompt injection in .planning/ |
| `gsd-statusline.js` | statusLine | Show model, task, context % in status bar |

> ⚠️ These are auto-installed by GSD. Do not copy them manually — they'll be overwritten on GSD update.

## Workspace hooks vs global hooks

| File | Location | Scope |
|------|----------|-------|
| `workspace/settings.json` | `~/Desktop/AI/.claude/settings.json` | All sessions in AI workspace |
| `claude/settings.json` | `~/.claude/settings.json` | All Claude Code sessions globally |

Both reference the same hook scripts. The workspace-level file uses relative paths.
