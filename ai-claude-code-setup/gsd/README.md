# GSD — Get Shit Done

Two versions are installed in parallel. GSD2 is the primary tool; GSD v1 provides Claude Code hooks.

---

## GSD2 (primary — `gsd-pi`)

Standalone autonomous coding agent built on the Pi SDK. Runs as its own CLI, not inside Claude Code.

- **Package:** `gsd-pi` (npm)
- **Binary:** `gsd`
- **Version:** 2.50.0
- **Repo:** [gsd-build/gsd-2](https://github.com/gsd-build/gsd-2)

### Key differences from v1

| | GSD v1 (`get-shit-done-cc`) | GSD2 (`gsd-pi`) |
|---|---|---|
| Architecture | Prompt framework injected via Claude Code slash commands | Standalone CLI agent with own runtime (Pi SDK) |
| State | File-based `.planning/` | DB-backed with state machine guards |
| Context | Hopes LLM follows instructions | Direct control over context window, sessions |
| Recovery | Manual | Crash recovery, auto-advance, worktree lifecycle |
| Execution | Inside Claude Code | Independent process |

### Install

```bash
npm install -g gsd-pi@latest
gsd --version
```

### Usage

```bash
# Interactive mode (TUI)
cd ~/Desktop/AI/Web3/my-project
gsd

# Single-shot
gsd -p "describe the task"

# Resume last session
gsd -c

# Worktree isolation
gsd -w

# Specific model
gsd --model claude-opus-4-6

# Headless (no TUI)
gsd headless auto "build the feature"
```

### Config

GSD2 uses `~/.gsd/agent/settings.json` (shared with v1):

```json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-sonnet-4-6",
  "defaultThinkingLevel": "high"
}
```

### Global knowledge

`~/.gsd/agent/KNOWLEDGE.md` is injected into every GSD2 system prompt — use for cross-project rules/context.

### Sessions

```bash
gsd sessions          # list past sessions
gsd -c                # resume most recent
```

### Worktrees

```bash
gsd worktree list     # list active worktrees
gsd worktree merge    # merge completed worktree
gsd worktree clean    # cleanup stale worktrees
```

---

## GSD v1 (legacy — `get-shit-done-cc`)

Prompt framework for Claude Code. Still provides hooks and 57 slash commands.

- **Package:** `get-shit-done-cc` (npx)
- **Version:** 1.29.0
- **Repo:** [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

### Install

```bash
cd ~/Desktop/AI
npx get-shit-done-cc --claude --local
```

This installs:
- `~/.claude/hooks/*.js` — 4 hooks (SessionStart, PreToolUse, PostToolUse, statusLine)
- `~/.claude/commands/gsd/` — 57 slash commands for Claude Code
- `~/Desktop/AI/.claude/` — workspace-level hooks and agents

### Hooks (auto-installed, do NOT copy manually)

| Hook | Trigger | Purpose |
|------|---------|---------|
| `gsd-check-update.js` | SessionStart | Check for GSD updates |
| `gsd-context-monitor.js` | PostToolUse | Warn when context is filling up |
| `gsd-prompt-guard.js` | PreToolUse (Write/Edit) | Detect prompt injection in .planning/ |
| `gsd-statusline.js` | statusLine | Show model, task, context % in status bar |

### Per-project config

Each project: `.planning/config.json` (see `project-config-example.json`):

```json
{
  "mode": "yolo",
  "verification_commands": ["forge test -vvv", "pnpm test"],
  "verification_auto_fix": true,
  "verification_max_retries": 2,
  "git": { "isolation": "worktree" }
}
```

### Slash commands in Claude Code

```
/gsd:plan "describe what to build"
/gsd:execute-phase 1
/gsd:autonomous
/gsd:status
/gsd:verify
```

---

## Which to use when

| Scenario | Tool |
|----------|------|
| Autonomous multi-phase build | **GSD2** (`gsd`) |
| Quick Claude Code task with context monitoring | **GSD v1** (hooks + `/gsd:*`) |
| Long-running build, walk away | **GSD2** (`gsd headless auto`) |
| One-shot code task | **GSD2** (`gsd -p "..."`) |
