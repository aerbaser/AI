# Installers

This package provides bootstrap scripts for `Linux` and `macOS`.

Each bootstrap script:

- checks for a local OpenClaw config
- installs the local Codex-backed proxy files into `~/.openclaw/toolkit/memory-claw-v2`
- writes a simple `qmd-voyage` wrapper into `~/.openclaw/bin`
- renders the recommended OpenClaw memory overlay

The scripts do not commit secrets. Runtime secrets come from environment variables such as `VOYAGE_API_KEY`.
