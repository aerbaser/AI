# OpenClaw Integration

This package renders the recommended `memory-claw-v2` policy into an `openclaw.json`.

Goals:

- no committed secrets
- no hardcoded personal paths
- safe defaults for `LCM + Engram + QMD`
- `memorySearch.sources=["memory"]` by default
- shared operational corpus via `shared-memory`

Use `bin/render_openclaw_overlay.py` to patch a config file in place or render to a new path.
