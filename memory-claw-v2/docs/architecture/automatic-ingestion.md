# Automatic Ingestion

Agent discipline is not a reliable memory strategy.

Important facts must enter memory even when the agent forgets to write them down.

## Sources

`memory-claw-v2` assumes ingestion happens from system-observed events:

- user and assistant messages
- tool calls and tool results
- task state transitions
- code changes and commit events
- handoffs between agents
- explicit decisions and postmortems
- curated document updates

## Pipeline

Each event goes through the same path:

1. `extract`
   Pull candidate memory facts from the raw event.
2. `classify`
   Decide whether the fact belongs in:
   - `session`
   - `private`
   - `shared`
   - `docs`
   - `discard`
3. `dedupe`
   Merge with existing memory if the fact is already known.
4. `summarize`
   Create a short durable record.
5. `embed`
   Use the canonical embedding space.
6. `write`
   Store in the correct layer.

## Promotion rules

Facts should be promoted to `shared` when they affect more than one agent, for example:

- a production incident and fix
- a new protocol
- a deployment rule
- a tool or provider pitfall
- a stable user preference that affects multiple specialists

Facts stay `private` when they are local to one agent's style or unfinished reasoning.

## Anti-patterns

- relying on agents to “remember to write memory”
- dumping raw sessions into semantic memory by default
- storing the same fact in multiple active primary systems
- letting retrieval assemble unlimited context
