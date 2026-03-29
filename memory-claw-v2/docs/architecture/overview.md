# Architecture Overview

`memory-claw-v2` uses four layers with hard role boundaries.

## 1. Session Layer

- Engine: `lossless-claw`
- Purpose: keep the active conversation coherent
- Responsibilities:
  - summarize old turns
  - preserve continuity
  - shrink hot context

This layer is not the source of truth for durable memory.

## 2. Primary Long-Term Memory

- Engine: `Engram`
- Purpose: durable semantic memory
- Responsibilities:
  - store persistent user and agent facts
  - store task summaries and lessons learned
  - separate `private` and `shared` scopes
  - serve semantic recall for the agent

This is the only primary long-term memory layer in the recommended stack.

## 3. Knowledge Layer

- Engine: `QMD`
- Purpose: retrieve curated markdown knowledge
- Responsibilities:
  - runbooks
  - handoffs
  - protocols
  - postmortems
  - curated memory files
  - shared operational docs

This layer should not default to raw session dumps.

## 4. Shared Operational Corpus

- Path shape: `shared-memory`
- Purpose: keep all agents on the same operational truth
- Responsibilities:
  - decisions
  - handoffs
  - runbooks
  - cross-agent rules
  - shared incidents and fixes
- Delivery path:
  - stable source docs live in `shared-memory`
  - a generated `roundtable` snapshot feeds `Engram sharedContext`
  - live inboxes, raw logs, and append-only spools stay outside the prompt path

## Design Rules

- only one primary long-term memory engine
- `LCM` is session memory, not canonical truth
- `QMD` is docs retrieval, not conversational memory
- shared-memory is common truth, not a scratchpad
- automatic ingestion is required because agents miss important facts
- retrieval must be budgeted for latency and token size
- operational truth should be synthesized automatically into a compact shared snapshot
- do not inject live inbox files or noisy append-only logs directly into the recall path
