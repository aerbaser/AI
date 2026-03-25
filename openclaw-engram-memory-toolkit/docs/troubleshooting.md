# Troubleshooting

## `database is locked`

Root cause in this stack was CLI contention against the live `lcm.db`.

What this toolkit does:

- forces `openclaw engram ...` CLI-path to use `:memory:` for `lossless-claw`
- keeps the real `~/.openclaw/lcm.db` owned by the live gateway path

If you still see the error:

1. run `./install/update.sh`
2. run `./install/verify.sh`
3. inspect `lsof ~/.openclaw/lcm.db ~/.openclaw/lcm.db-wal ~/.openclaw/lcm.db-shm`

## `openclaw engram doctor` hangs

This toolkit patches operator/search CLI lifecycle so those commands exit after printing their result.

If they still hang:

1. re-apply the overlay with `~/.openclaw/bin/apply-memory-overlay.py`
2. restart LaunchAgents
3. check whether you are running an outdated Engram package that changed patch anchors

## Proxy health is down

Check:

```bash
launchctl print gui/$(id -u)/local.engram-codex-proxy
tail -n 200 ~/.openclaw/logs/engram-codex-proxy.log
curl -fsS http://127.0.0.1:4321/health
```

Common causes:

- `codex` binary missing
- Codex not authenticated
- wrong `CODEX_MODEL`
- wrong `PATH` in the launchd environment

## Voyager embeddings fail

Check:

- `VOYAGE_API_KEY` exists locally
- `agents.defaults.memorySearch.remote.apiKey` exists in `~/.openclaw/openclaw.json`
- `~/.openclaw/bin/qmd-voyage --version` works

## QMD drift after updates

That is exactly why the toolkit uses the overlay auto-apply agent.

Run:

```bash
~/.openclaw/bin/apply-memory-overlay.py --verify-fast
```

