# Memory Claw V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a public-friendly `memory-claw-v2` toolkit inside the `AI` repo that documents the ideal memory stack, ships anonymized benchmark tooling, and provides portable OpenClaw integration/install artifacts for `Linux` and `macOS`.

**Architecture:** Build `memory-claw-v2` as a modular product directory with docs, `core` policies/schemas, a reusable benchmark package, a generic OpenClaw overlay renderer, a local Codex-compatible proxy, and cross-platform bootstrap scripts. Reuse only generic lessons and code from the older toolkit and memory lab, never private corpus data.

**Tech Stack:** Markdown, Python 3, Node.js, shell, OpenClaw JSON config, pytest.

---

### Task 1: Create the public product skeleton

**Files:**
- Create: `memory-claw-v2/README.md`
- Create: `memory-claw-v2/.gitignore`
- Create: `memory-claw-v2/SECURITY.md`
- Create: `memory-claw-v2/pyproject.toml`

- [ ] Add the top-level product docs and hygiene files.
- [ ] Keep the README explicit about the target stack and non-goals.
- [ ] Ignore generated state, env files, caches, and test output.

### Task 2: Publish the architecture and benchmark findings

**Files:**
- Create: `memory-claw-v2/docs/architecture/overview.md`
- Create: `memory-claw-v2/docs/architecture/automatic-ingestion.md`
- Create: `memory-claw-v2/docs/evaluation/benchmark-summary.md`
- Create: `memory-claw-v2/docs/rollout/openclaw-rollout.md`

- [ ] Describe the ideal stack and why each layer exists.
- [ ] Encode the “do not rely on agents to write memory” rule in public docs.
- [ ] Publish sanitized benchmark findings without raw private data.
- [ ] Write the production rollout plan for agents and shared-memory sync.

### Task 3: Publish machine-readable policy and schema files

**Files:**
- Create: `memory-claw-v2/packages/core/README.md`
- Create: `memory-claw-v2/packages/core/policies/default-memory-policy.json`
- Create: `memory-claw-v2/packages/core/schemas/memory-event.schema.json`
- Create: `memory-claw-v2/packages/core/schemas/memory-record.schema.json`

- [ ] Encode the recommended memory stack in policy JSON.
- [ ] Define a neutral event schema for automatic ingestion.
- [ ] Define a neutral record schema for durable memory entries.

### Task 4: Port the benchmark package

**Files:**
- Create: `memory-claw-v2/packages/bench/README.md`
- Create: `memory-claw-v2/packages/bench/src/memory_claw_bench/*.py`
- Create: `memory-claw-v2/packages/bench/src/memory_claw_bench/runners/*.py`
- Create: `memory-claw-v2/packages/bench/bin/run_benchmark.py`
- Create: `memory-claw-v2/packages/bench/tests/*.py`
- Create: `memory-claw-v2/examples/benchmark/gold-set.template.json`

- [ ] Port the generic benchmark helpers and tests.
- [ ] Keep candidate adapters scaffolded but honest about environment-specific work.
- [ ] Publish an anonymized example gold set.

### Task 5: Add generic OpenClaw integration

**Files:**
- Create: `memory-claw-v2/packages/integrations/openclaw/README.md`
- Create: `memory-claw-v2/packages/integrations/openclaw/bin/render_openclaw_overlay.py`
- Create: `memory-claw-v2/packages/integrations/openclaw/templates/openclaw.memory-claw-v2.example.json`
- Create: `memory-claw-v2/packages/integrations/openclaw/tests/test_render_openclaw_overlay.py`

- [ ] Create a renderer that applies the recommended memory policy to any OpenClaw config JSON.
- [ ] Keep secrets optional and injected only from runtime env.
- [ ] Ensure the renderer defaults to `sources=["memory"]` and avoids session-heavy semantic corpora.

### Task 6: Ship the proxy and installers

**Files:**
- Create: `memory-claw-v2/packages/proxy/*`
- Create: `memory-claw-v2/packages/installers/README.md`
- Create: `memory-claw-v2/packages/installers/linux/bootstrap.sh`
- Create: `memory-claw-v2/packages/installers/macos/bootstrap.sh`

- [ ] Port the Codex-backed OpenAI-compatible proxy into the new toolkit.
- [ ] Add Linux and macOS bootstrap scripts that copy the proxy, render config, and install a QMD wrapper.
- [ ] Keep the scripts generic and free of hardcoded personal paths.

### Task 7: Verify and publish

**Files:**
- Modify: `memory-claw-v2/**`

- [ ] Run pytest for the public Python package and integration renderer.
- [ ] Review the generated tree for secrets or private data leakage.
- [ ] Commit on `codex/memory-claw-v2`.
- [ ] Push the branch so the toolkit exists on GitHub inside `AI`.
