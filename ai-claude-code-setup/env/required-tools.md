# Required Tools

Install the following tools to reproduce this environment.

- Claude Code
  - `npm install -g @anthropic-ai/claude-code`
- GSD
  - `npx get-shit-done-cc --claude --local`
- Context7
  - `npm install -g ctx7`
- uv / uvx (for Serena MCP)
- codebase-memory-mcp
  - binary expected at `~/.local/bin/codebase-memory-mcp`
- gopls
  - `go install golang.org/x/tools/gopls@latest`
- typescript-language-server
  - `npm install -g typescript-language-server`
- pyright
  - `npm install -g pyright`
- rust-analyzer
- Dart SDK + Flutter
  - `brew install --cask flutter`
- Hammerspoon
  - `brew install --cask hammerspoon`

## Memory / Agent Runtime

- **OpenClaw** — `npm install -g openclaw`
- **Engram plugin** — `openclaw plugins install @joshuaswarren/openclaw-engram`
- **QMD** — installed automatically by Engram; for Qwen3 embeddings set `QMD_EMBED_MODEL`
- **lossless-claw** (optional, context compaction) — `openclaw plugins install @martian-engineering/lossless-claw`
