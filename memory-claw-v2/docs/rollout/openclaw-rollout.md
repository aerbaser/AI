# OpenClaw Rollout

This rollout is for teams that want all agents on one memory policy without depending on manual note taking.

## Target state

- one shared operational corpus
- one primary long-term memory engine
- one embedding space
- one automatic ingestion pipeline
- one OpenClaw policy for all agents

## Rollout phases

### Phase 1: Publish and validate the toolkit

- install the proxy
- render the OpenClaw config overlay
- verify benchmark tests
- verify the proxy and QMD wrapper work locally

### Phase 2: Apply the common policy

- preserve the enabled channel plugins when rendering `plugins.allow`
- set the same `memorySearch` policy for all agents
- disable session-heavy semantic memory defaults
- point all agents at the same `shared-memory` path
- keep `lossless-claw` only for session continuity
- keep `Engram` as the primary memory layer with `lcmEnabled=false`
- explicitly disable Engram rerank on the reply path unless a separate fast LLM queue is available

### Phase 3: Enable automatic ingestion

- subscribe to conversation, tool, and task events
- classify events into `private`, `shared`, `docs`, or `discard`
- promote operational facts into shared-memory automatically
- generate a compact `shared-memory/roundtable/*.md` snapshot from stable docs such as `decisions.md`, `handoffs.md`, `open-loops.md`, and `protocols/*`
- make the roundtable sync hash-gated so scheduled runs call the LLM only when source docs changed
- keep live inboxes, feedback spools, and raw communication logs out of the shared prompt path

### Phase 4: Reindex and validate

- rebuild the primary long-term memory index
- rebuild QMD docs index
- compare latency and token cost against the baseline
- verify that `sharedCtx` stays in a low-latency budget after the roundtable snapshot is added

### Phase 5: Bring the secondary agents onto the same corpus

- keep private overlays per agent
- keep the shared corpus identical for all agents
- validate that specialist agents can recall the same shared decisions as the main agent

## Hard rules

- do not let raw sessions become the default semantic corpus
- do not run multiple primary memory systems at once
- do not rely on agents to remember to write critical facts
- do not mix multiple embedding spaces in one primary index
- do not point shared-context recall directly at uncurated inboxes or append-only logs
