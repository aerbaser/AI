# Architecture

This toolkit packages the memory stack into four layers.

## 1. Engram

`openclaw-engram` is the memory orchestrator:

- buffers and extracts durable memories
- writes facts, entities, profile updates, and questions
- performs operator commands such as `doctor`, `config-review`, and `search`

Recommended Engram settings in this toolkit:

- `memoryOsPreset = balanced`
- `captureMode = hybrid`
- `qmdEnabled = true`
- `qmdDaemonEnabled = true`
- `lcmEnabled = false`
- `recallBudgetChars = 80000`

## 2. QMD + Voyager

The toolkit keeps upstream `qmd` as the base and applies a thin overlay:

- Voyager embeddings are added via wrapper/overlay instead of forking QMD outright
- the overlay re-applies cleanly after OpenClaw/QMD updates
- `qmd-voyage` becomes the single canonical QMD entrypoint for Engram and memory search

This is the part that prevents “custom fork drift” while still keeping high-quality embeddings.

## 3. Codex-backed proxy

Engram’s write/extraction path points at a local OpenAI-compatible server:

- endpoint: `http://127.0.0.1:4321/v1/chat/completions`
- implementation: `proxy/server.mjs`
- backend: `codex exec --model gpt-5.4-mini`

That gives Engram a normal OpenAI-style backend without requiring a direct OpenAI API key.

## 4. launchd automation

Two LaunchAgents keep the stack healthy:

- `local.engram-codex-proxy`
- `local.openclaw-memory-overlay`

The overlay agent re-applies patches after upstream package changes. The proxy agent keeps the Codex-backed local endpoint alive.

