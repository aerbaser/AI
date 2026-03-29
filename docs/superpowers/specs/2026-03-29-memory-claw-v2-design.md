# Memory Claw V2 Design

> Build a public-friendly memory toolkit for OpenClaw that keeps roles clean: `LCM` for session compaction, `Engram` for primary long-term memory, `QMD` for curated knowledge retrieval, and automatic ingestion instead of agent-only note taking.

## Scope
- Publish a new `memory-claw-v2/` product directory inside `AI`.
- Ship a universal benchmark package with anonymized examples and no private data.
- Ship OpenClaw integration templates and installers for `Linux` and `macOS`.
- Encode the recommended memory architecture and rollout plan in public documentation.

## Product Shape
- `memory-claw-v2/docs`: public architecture, benchmark findings, rollout docs, install guides.
- `memory-claw-v2/packages/core`: machine-readable policy and schemas for memory records and ingestion events.
- `memory-claw-v2/packages/bench`: reusable benchmark harness and tests.
- `memory-claw-v2/packages/integrations/openclaw`: config renderer and integration templates.
- `memory-claw-v2/packages/proxy`: local OpenAI-compatible Codex-backed proxy.
- `memory-claw-v2/packages/installers`: cross-platform bootstrap scripts.
- `memory-claw-v2/examples`: sanitized benchmark questions and corpus examples.

## Architecture

### 1. Session Layer
- Engine: `lossless-claw`
- Role: keep active and recent conversation continuity stable.
- Rules:
  - compaction only
  - recent summaries only
  - never canonical long-term truth

### 2. Primary Long-Term Memory
- Engine: `Engram`
- Role: durable semantic memory for agents.
- Rules:
  - automatic ingestion from events and conversations
  - shared/private scopes
  - write path via `gpt-5.4-mini`
  - embeddings via `Voyage`

### 3. Knowledge Layer
- Engine: `QMD`
- Role: retrieval over curated markdown and shared-memory docs.
- Rules:
  - runbooks
  - protocols
  - handoffs
  - postmortems
  - `MEMORY.md` style files
  - no raw session dumps as default corpus

### 4. Shared Operational Corpus
- Role: common truth layer across Socrates, Platon, and the rest.
- Stored separately from private overlays.
- Used for decisions, runbooks, handoffs, and operational facts.

### 5. Automatic Ingestion
- The system, not the agent, is responsible for remembering.
- Sources:
  - user/assistant messages
  - tool calls and outcomes
  - task state transitions
  - commits and PR events
  - explicit decisions and postmortems
  - shared-memory document updates
- Pipeline:
  - extract
  - classify
  - dedupe
  - summarize
  - embed
  - write to private/shared/docs target

## Constraints
- No private user transcripts or real corpus snapshots in the published toolkit.
- No committed secrets, auth tokens, or API keys.
- Keep the toolkit portable across `Linux` and `macOS`.
- Keep `graph-memory` present as an R&D track without making it the default runtime.

## Recommendation
- Publish `memory-claw-v2` as a modular monorepo-style toolkit directory.
- Default stack:
  - `LCM` for session continuity
  - `Engram` for primary long-term memory
  - `QMD` for curated docs
  - automatic ingestion
  - `Voyage` as canonical embedding space
- Keep `graph-memory` in the evaluation story, not the default product path.
