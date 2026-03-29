# Memory Claw V2

Portable memory toolkit for OpenClaw agents.

`memory-claw-v2` packages the memory architecture that came out of the Socrates evaluation work:

- `LCM` for session continuity and compaction
- `Engram` as the primary long-term memory layer
- `QMD` for curated markdown and shared-memory retrieval
- automatic ingestion so the system remembers even when agents forget
- `Voyage` as the canonical embedding space
- a local OpenAI-compatible proxy backed by Codex for `gpt-5.4-mini`

## Why V2 exists

The core lesson from the benchmark work was not “install one more memory plugin”.

The winning pattern was:

1. separate roles cleanly
2. stop treating raw sessions as the default semantic corpus
3. stop relying on agents to remember to write important things down
4. keep one shared operational corpus across agents
5. budget retrieval for latency and tokens

This toolkit turns that architecture into a reusable product.

## What is included

- public architecture docs
- sanitized benchmark findings
- machine-readable memory policy and schemas
- reusable benchmark harness
- OpenClaw config renderer
- local Codex-backed OpenAI-compatible proxy
- `Linux` and `macOS` bootstrap scripts
- anonymized examples

## What is not included

- private user transcripts
- real memory databases
- API keys or auth tokens
- host-specific absolute paths

## Repository layout

- `docs/`: architecture, rollout, install, benchmark summary
- `examples/`: anonymized sample gold sets and corpus structure
- `packages/core/`: policy and schema files
- `packages/bench/`: public benchmark package and tests
- `packages/integrations/openclaw/`: config renderer and templates
- `packages/proxy/`: local OpenAI-compatible Codex proxy
- `packages/installers/`: `Linux` and `macOS` bootstrap scripts

## Recommended stack

- session layer: `lossless-claw`
- primary long-term memory: `Engram`
- docs/knowledge layer: `QMD`
- shared operational corpus: `shared-memory`
- embeddings: `Voyage`
- extraction/write path: `gpt-5.4-mini`
- graph experimentation: optional `graph-memory`, not the default runtime

## Quick start

```bash
cd memory-claw-v2
python3 -m pytest packages/bench/tests packages/integrations/openclaw/tests -q
./packages/installers/linux/bootstrap.sh
```

For `macOS`, use:

```bash
./packages/installers/macos/bootstrap.sh
```

## Status

This is a toolkit and reference implementation. It is designed to be portable, auditable, and safe to publish.
