# LLM Recommendations

These are the recommended settings for the memory stack validated in this rollout.

## Primary recommendation

### Engram write path

- Backend: local OpenAI-compatible proxy
- URL: `http://127.0.0.1:4321`
- Model label: `openai-codex/gpt-5.4-mini`
- Actual backend model: `gpt-5.4-mini` through `codex exec`

Why:

- strong extraction quality
- better reliability than a custom OpenAI API-key path in this setup
- much better quality than small local CPU-only models

### Embeddings

- Provider: `Voyager`
- Model: `voyage-4-large`

Why:

- better mixed-language retrieval quality
- cleaner than keeping a custom local embedding model as the primary path

## Main agent model

Recommended main runtime:

- `openai-codex/gpt-5.4`

This toolkit does not force the main agent model, but that is the quality-first baseline used in the validated server setup.

## Local fallback

Recommended local fallback:

- `qwen2.5:7b`

Reason:

- acceptable extraction quality as a backup
- slower than Codex-backed extraction on Intel Mac hardware
- still more useful than very small local models for durable memory writes

## Settings to keep

- `lcmEnabled = false`
- `captureMode = hybrid`
- `qmdEnabled = true`
- `qmdDaemonEnabled = true`
- `recallBudgetChars = 80000`
- `conversationIndexEnabled = true`

## Settings not recommended as default

- tiny local models as primary write-path
- direct public release of private memory state
- dual competing QMD paths
- custom long-lived fork of upstream QMD

