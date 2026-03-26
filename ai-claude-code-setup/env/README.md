# Environment Variables

Required environment variables for this setup:

- `OPENCLAW_ENGRAM_ACCESS_TOKEN` — Engram MCP bearer token
- `ANTHROPIC_API_KEY` — Anthropic API key for Claude Code
- `CONTEXT7_API_KEY` — Context7 API key (if needed)

Set them in:
- `~/.zshrc`
- `~/.zprofile`

Example:

```bash
export OPENCLAW_ENGRAM_ACCESS_TOKEN=<YOUR_TOKEN_HERE>
export ANTHROPIC_API_KEY=<YOUR_TOKEN_HERE>
export CONTEXT7_API_KEY=<YOUR_TOKEN_HERE>
```

## OpenClaw / Engram specific

- `OPENCLAW_ENGRAM_ACCESS_TOKEN` — bearer token for Engram MCP HTTP server
  - Get with: `openclaw engram access token`
  - Required for Claude Code to access long-term memory
