#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the memory-claw-v2 OpenClaw config overlay.")
    parser.add_argument("--config", required=True, help="Path to the input openclaw.json")
    parser.add_argument("--output", help="Optional output path. Defaults to in-place.")
    parser.add_argument("--proxy-url", default="http://127.0.0.1:4321")
    parser.add_argument("--proxy-model", default="openai-codex/gpt-5.4-mini")
    parser.add_argument("--qmd-command", default="~/.openclaw/bin/qmd-voyage")
    parser.add_argument("--shared-memory-path", default="~/.openclaw/shared-memory")
    parser.add_argument("--voyage-model", default="voyage-3-large")
    parser.add_argument("--voyage-api-key-env", default="VOYAGE_API_KEY")
    return parser.parse_args(argv)


def expand(value: str) -> str:
    return str(Path(value).expanduser())


def apply_overlay(cfg: dict, args: argparse.Namespace) -> dict:
    qmd_command = expand(args.qmd_command)
    shared_memory_path = expand(args.shared_memory_path)
    voyage_api_key = os.environ.get(args.voyage_api_key_env, "").strip()

    plugins = cfg.setdefault("plugins", {})
    plugins["allow"] = ["lossless-claw", "openclaw-engram"]
    entries = plugins.setdefault("entries", {})
    entries.setdefault("lossless-claw", {})["enabled"] = True
    entries.setdefault("memos-capture", {})["enabled"] = False
    engram = entries.setdefault("openclaw-engram", {}).setdefault("config", {})
    engram["memoryOsPreset"] = "balanced"
    engram["qmdEnabled"] = True
    engram["qmdDaemonEnabled"] = True
    engram["qmdPath"] = qmd_command
    engram["lcmEnabled"] = False
    engram["localLlmEnabled"] = True
    engram["localLlmUrl"] = args.proxy_url
    engram["localLlmModel"] = args.proxy_model
    engram["captureMode"] = "hybrid"
    engram["recallBudgetChars"] = 32000
    engram["conversationIndexEnabled"] = True
    engram["sharedContextEnabled"] = True
    engram["sharedContextDir"] = shared_memory_path
    engram["sharedContextMaxInjectChars"] = 8000
    engram["modelSource"] = "plugin"

    memory = cfg.setdefault("memory", {})
    memory["backend"] = "qmd"
    memory["citations"] = "auto"
    memory_qmd = memory.setdefault("qmd", {})
    memory_qmd["command"] = qmd_command
    memory_qmd["searchMode"] = "search"
    memory_qmd["includeDefaultMemory"] = False
    memory_qmd["paths"] = [
        {
            "path": shared_memory_path,
            "name": "shared-memory",
            "pattern": "**/*.md",
        }
    ]
    memory_qmd["sessions"] = {"enabled": False}
    memory_qmd["update"] = {
        "interval": "15m",
        "debounceMs": 10000,
        "onBoot": True,
        "waitForBootSync": False,
    }
    memory_qmd["limits"] = {"maxResults": 8, "timeoutMs": 15000}

    agents = cfg.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    model = defaults.setdefault("model", {})
    model.setdefault("primary", args.proxy_model)
    defaults.setdefault("models", {}).setdefault(args.proxy_model, {})
    memory_search = defaults.setdefault("memorySearch", {})
    memory_search["enabled"] = True
    memory_search["sources"] = ["memory"]
    memory_search["extraPaths"] = [shared_memory_path]
    memory_search["provider"] = "voyage"
    memory_search["model"] = args.voyage_model
    memory_search["fallback"] = "local"
    remote = memory_search.setdefault("remote", {})
    if voyage_api_key:
        remote["apiKey"] = voyage_api_key
    memory_search["sync"] = {
        "onSessionStart": True,
        "onSearch": True,
        "watch": True,
        "intervalMinutes": 15,
    }
    memory_search["experimental"] = {"sessionMemory": False}
    return cfg


def main() -> int:
    args = parse_args()
    input_path = Path(args.config).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve() if args.output else input_path
    cfg = json.loads(input_path.read_text(encoding="utf-8"))
    rendered = apply_overlay(cfg, args)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(rendered, indent=2) + "\n", encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
