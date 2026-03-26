# Environment Variables

Add to both `~/.zshrc` and `~/.zprofile` (Claude Code needs them in login shells):

```bash
# Required
export ANTHROPIC_API_KEY=<your_anthropic_api_key>

# Required for claude-mem (if using non-CLI auth)
# Not needed if CLAUDE_MEM_CLAUDE_AUTH_METHOD=cli (default in this setup)

# Optional: Engram MCP (only if running OpenClaw)
export OPENCLAW_ENGRAM_ACCESS_TOKEN=<your_engram_token>
# Get token: openclaw engram access token

# Optional: Context7
export CONTEXT7_API_KEY=<your_context7_key>
```

After editing:
```bash
source ~/.zshrc && source ~/.zprofile
```

## ⚠️ Fresh terminal rule

Claude Code hooks (claude-mem, GSD) only activate if launched from a terminal that has sourced the above files. If memory isn't working → restart from a fresh terminal.

## Token rotation

- `OPENCLAW_ENGRAM_ACCESS_TOKEN` can be rotated: `openclaw engram access token --rotate`
- Update the value in `~/.claude.json` → `mcpServers.engram.headers.Authorization`
