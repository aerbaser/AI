# GSD Setup

This machine uses **get-shit-done-cc** as the autonomous delivery workflow layer.

## Snapshot

- Version: `1.29.0`
- Settings file: `gsd/settings.json`
- Default provider: `anthropic`
- Default model: `claude-sonnet-4-6`
- Default thinking level: `high`
- Quiet startup: enabled

## Install

```bash
cd <project>
npx get-shit-done-cc --claude --local
```

## Files in this folder

- `settings.json` — global GSD agent settings from `~/.gsd/agent/settings.json`
- `project-config-example.json` — example project planning config from a live Web3 project

## Typical usage

1. Install GSD in the project.
2. Keep shared Claude hooks in `~/Desktop/AI/.claude/settings.json`.
3. Add project planning config under `.planning/config.json`.
4. Reuse the example config in this folder as a baseline.

## Example project config features

- balanced model profile
- parallelization enabled
- verifier / plan-check / research enabled
- auto-fix enabled for verification
- Web3 verification commands such as `forge test` and `slither .`
