#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


HOME = Path.home()
OPENCLAW_DIR = HOME / ".openclaw"
LOG_DIR = OPENCLAW_DIR / "logs"
BACKUP_DIR = OPENCLAW_DIR / "backups"
OVERLAY_DIR = OPENCLAW_DIR / "overlays" / "qmd-voyage-runtime"
OVERLAY_STATE = OPENCLAW_DIR / "overlays" / "state" / "memory-overlay-state.json"
QMD_WRAPPER = OPENCLAW_DIR / "bin" / "qmd-voyage"
QMD_LEGACY_WRAPPER = OPENCLAW_DIR / "bin" / "qmd-qwen3"
UPSTREAM_QMD_DIR = Path("/usr/local/lib/node_modules/@tobilu/qmd")
ENGRAM_DIR = OPENCLAW_DIR / "extensions" / "openclaw-engram"
ENGRAM_INDEX = ENGRAM_DIR / "dist" / "index.js"
ENGRAM_QMD = ENGRAM_DIR / "dist" / "chunk-AHYRVKIJ.js"
LOSSLESS_DB_CONFIG = OPENCLAW_DIR / "extensions" / "lossless-claw" / "src" / "db" / "config.ts"
CONFIG_PATH = OPENCLAW_DIR / "openclaw.json"
OPENCLAW_BIN = Path("/usr/local/bin/openclaw")
NODE_BIN = Path("/usr/local/bin/node")
DEFAULT_PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

QMD_BIN = """#!/bin/sh
set -eu
DIR="$(cd -P "$(dirname "$0")/.." && pwd)"
export PATH="{default_path}"
exec "{node_bin}" "$DIR/dist/cli/qmd.js" "$@"
"""

QMD_WRAPPER_TEMPLATE = """#!/bin/sh
set -eu

CFG="{cfg}"
PACKAGE_DIR="{package_dir}"

if [ -z "${{QMD_VOYAGE_API_KEY:-}}" ] && [ -r "$CFG" ]; then
  QMD_VOYAGE_API_KEY="$(python3 - <<'PY'
import json
cfg = json.load(open("{cfg}"))
print(cfg["agents"]["defaults"]["memorySearch"]["remote"]["apiKey"])
PY
)"
  export QMD_VOYAGE_API_KEY
fi

export QMD_EMBED_PROVIDER="${{QMD_EMBED_PROVIDER:-voyage}}"
export QMD_VOYAGE_MODEL="${{QMD_VOYAGE_MODEL:-voyage-4-large}}"
export QMD_VOYAGE_BASE_URL="${{QMD_VOYAGE_BASE_URL:-https://api.voyageai.com/v1}}"

# Keep a local embedding model configured so QMD can still use a tokenizer/chunker
# while remote Voyage serves the actual vectors.
export QMD_EMBED_MODEL="${{QMD_EMBED_MODEL:-hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf}}"

exec "$PACKAGE_DIR/bin/qmd" "$@"
"""

ACCESS_GUARD_OPEN = """      const accessService = new EngramAccessService(orchestrator);\n      let accessCmd = null;\n      try {\n        accessCmd = cmd.command("access").description("Manage Engram HTTP and MCP access surfaces");\n      } catch {\n        accessCmd = null;\n      }\n      if (accessCmd) {\n"""
ACCESS_GUARD_CLOSE = """      }\n      const routeCmd = cmd.command("route").description("Manage custom memory routing rules");"""

QMD_EXIT_HOOK = """  constructor(qmdPath) {\n    this.qmdPath = qmdPath;\n    if (!globalThis.__openclawEngramQmdExitHookBound) {\n      const cleanupOnExit = () => {\n        try {\n          _sharedDaemonSession?.cleanup({ killChild: true });\n        } catch {\n        }\n      };\n      process.once(\"beforeExit\", cleanupOnExit);\n      process.once(\"exit\", cleanupOnExit);\n      globalThis.__openclawEngramQmdExitHookBound = true;\n    }\n  }\n"""
ORPHAN_REAPER = """var ENGRAM_ORPHAN_REAPER = \"__openclawEngramOrphanReaper\";\nif (!globalThis[ENGRAM_ORPHAN_REAPER]) {\n  const orphanReaper = setInterval(() => {\n    if (process.title === \"openclaw-engram\" && process.ppid === 1) {\n      process.exit(0);\n    }\n  }, 2e3);\n  orphanReaper.unref?.();\n  globalThis[ENGRAM_ORPHAN_REAPER] = orphanReaper;\n}\n"""
CLI_EXIT_HELPER = """function scheduleEngramCliExit() {\n  if (!process.argv.includes(\"engram\")) {\n    return;\n  }\n  if (globalThis.__openclawEngramCliExitScheduled) {\n    return;\n  }\n  globalThis.__openclawEngramCliExitScheduled = true;\n  const timer = setTimeout(() => {\n    process.exit(process.exitCode ?? 0);\n  }, 0);\n  timer.unref?.();\n}\n"""

VOYAGE_HELPERS = """/**
 * Detect if embeddings should be served by Voyage instead of a local GGUF model.
 * This is activated explicitly via QMD_EMBED_PROVIDER=voyage so tokenization can
 * still rely on the local embedding model configured in QMD_EMBED_MODEL.
 */
export function isVoyageEmbeddingMode(modelUri) {
    const provider = process.env.QMD_EMBED_PROVIDER?.trim().toLowerCase();
    if (provider === "voyage")
        return true;
    const uri = modelUri ?? process.env.QMD_EMBED_MODEL ?? DEFAULT_EMBED_MODEL;
    return /^voyage(?::|\\/|-)/i.test(uri);
}
function normalizeVoyageModel(modelUri) {
    const explicit = modelUri?.trim();
    if (explicit && /^voyage(?::|\\/|-)/i.test(explicit)) {
        return explicit.replace(/^voyage[:/]/i, "");
    }
    return process.env.QMD_VOYAGE_MODEL?.trim() || "voyage-4-large";
}
function getVoyageBaseUrl() {
    return (process.env.QMD_VOYAGE_BASE_URL?.trim() || "https://api.voyageai.com/v1").replace(/\\/$/, "");
}
function getVoyageApiKey() {
    const apiKey = process.env.QMD_VOYAGE_API_KEY?.trim();
    if (!apiKey) {
        throw new Error("QMD_VOYAGE_API_KEY is required when QMD_EMBED_PROVIDER=voyage");
    }
    return apiKey;
}
function sanitizeEmbeddingVector(values) {
    return values.map((value) => Number.isFinite(value) ? Number(value) : 0);
}
async function fetchVoyageEmbeddings(input, options = {}) {
    if (input.length === 0)
        return [];
    const body = {
        model: normalizeVoyageModel(options.model),
        input
    };
    if (options.inputType) {
        body.input_type = options.inputType;
    }
    const response = await fetch(`${getVoyageBaseUrl()}/embeddings`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${getVoyageApiKey()}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        const text = await response.text();
        throw new Error(`Voyage embeddings failed: ${response.status} ${text}`);
    }
    const payload = await response.json();
    const rows = Array.isArray(payload?.data) ? payload.data : [];
    return rows.map((row) => Array.isArray(row?.embedding) ? sanitizeEmbeddingVector(row.embedding) : null);
}
"""

VOYAGE_EMBED_SINGLE = """        if (isVoyageEmbeddingMode(options.model)) {\n            try {\n                const [embedding] = await fetchVoyageEmbeddings([text], {\n                    model: options.model,\n                    inputType: options.isQuery ? \"query\" : \"document\"\n                });\n                if (!embedding)\n                    return null;\n                return {\n                    embedding,\n                    model: normalizeVoyageModel(options.model),\n                };\n            }\n            catch (error) {\n                console.error(\"Voyage embedding error:\", error);\n                return null;\n            }\n        }\n"""

VOYAGE_EMBED_BATCH = """        if (isVoyageEmbeddingMode()) {\n            try {\n                const embeddings = await fetchVoyageEmbeddings(texts, {\n                    inputType: \"document\"\n                });\n                return embeddings.map((embedding) => embedding ? {\n                    embedding,\n                    model: normalizeVoyageModel(),\n                } : null);\n            }\n            catch (error) {\n                console.error(\"Voyage batch embedding error:\", error);\n                return texts.map(() => null);\n            }\n        }\n"""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str, executable: bool = False) -> None:
    ensure_parent(path)
    path.write_text(text)
    mode = 0o755 if executable else 0o644
    path.chmod(mode)


def backup_file(path: Path) -> None:
    if not path.exists():
        return
    stamp = sha256(path)[:12]
    target = BACKUP_DIR / "memory-overlay" / stamp / path.relative_to(HOME)
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"patch anchor missing for {label}")
    return text.replace(old, new, 1)


def patch_qmd_llm(text: str) -> str:
    if "QMD_VOYAGE_API_KEY is required when QMD_EMBED_PROVIDER=voyage" in text:
        return text
    text = replace_once(
        text,
        "export function formatQueryForEmbedding(query, modelUri) {\n    const uri = modelUri ?? process.env.QMD_EMBED_MODEL ?? DEFAULT_EMBED_MODEL;\n",
        "export function formatQueryForEmbedding(query, modelUri) {\n    const uri = modelUri ?? process.env.QMD_EMBED_MODEL ?? DEFAULT_EMBED_MODEL;\n    if (isVoyageEmbeddingMode(uri)) {\n        return query;\n    }\n",
        "formatQueryForEmbedding",
    )
    text = replace_once(
        text,
        "export function formatDocForEmbedding(text, title, modelUri) {\n    const uri = modelUri ?? process.env.QMD_EMBED_MODEL ?? DEFAULT_EMBED_MODEL;\n",
        "export function formatDocForEmbedding(text, title, modelUri) {\n    const uri = modelUri ?? process.env.QMD_EMBED_MODEL ?? DEFAULT_EMBED_MODEL;\n    if (isVoyageEmbeddingMode(uri)) {\n        return title ? `${title}\\n${text}` : text;\n    }\n",
        "formatDocForEmbedding",
    )
    text = replace_once(
        text,
        "export function isQwen3EmbeddingModel(modelUri) {\n    return /qwen.*embed/i.test(modelUri) || /embed.*qwen/i.test(modelUri);\n}\n",
        "export function isQwen3EmbeddingModel(modelUri) {\n    return /qwen.*embed/i.test(modelUri) || /embed.*qwen/i.test(modelUri);\n}\n" + VOYAGE_HELPERS,
        "voyage helpers",
    )
    text = replace_once(
        text,
        "    async embed(text, options = {}) {\n        // Ping activity at start to keep models alive during this operation\n        this.touchActivity();\n",
        "    async embed(text, options = {}) {\n        // Ping activity at start to keep models alive during this operation\n        this.touchActivity();\n" + VOYAGE_EMBED_SINGLE,
        "embed",
    )
    text = replace_once(
        text,
        "    async embedBatch(texts) {\n        if (this._ciMode)\n            throw new Error(\"LLM operations are disabled in CI (set CI=true)\");\n        // Ping activity at start to keep models alive during this operation\n        this.touchActivity();\n        if (texts.length === 0)\n            return [];\n",
        "    async embedBatch(texts) {\n        if (this._ciMode)\n            throw new Error(\"LLM operations are disabled in CI (set CI=true)\");\n        // Ping activity at start to keep models alive during this operation\n        this.touchActivity();\n        if (texts.length === 0)\n            return [];\n" + VOYAGE_EMBED_BATCH,
        "embedBatch",
    )
    return text


def patch_engram_index(text: str) -> str:
    if "ENGRAM_ORPHAN_REAPER" not in text:
        text = text.replace("// openclaw-engram: Local-first memory plugin\n", "// openclaw-engram: Local-first memory plugin\n" + ORPHAN_REAPER, 1)
    if "function scheduleEngramCliExit()" not in text:
        helper_anchor = "globalThis[ENGRAM_ORPHAN_REAPER] = orphanReaper;\n}\n"
        if helper_anchor in text:
            text = text.replace(helper_anchor, helper_anchor + CLI_EXIT_HELPER + "\n", 1)
        else:
            text = replace_once(
                text,
                "function formatTokenDelta(value) {\n",
                CLI_EXIT_HELPER + "\nfunction formatTokenDelta(value) {\n",
                "engram cli exit helper",
            )
    route_anchor = '      const routeCmd = cmd.command("route").description("Manage custom memory routing rules");'
    access_anchor = '      const accessService = new EngramAccessService(orchestrator);\n'
    body_anchor = '      accessCmd.command("http-serve").description("Start local authenticated HTTP access server")'
    start = text.find(access_anchor)
    route_idx = text.find(route_anchor)
    body_start = text.find(body_anchor)
    if start == -1 or route_idx == -1 or body_start == -1 or not (start < body_start < route_idx):
        raise RuntimeError("patch anchor missing for engram access block")
    body = text[body_start:route_idx]
    while body.endswith("      }\n"):
        body = body[:-8]
    rebuilt = ACCESS_GUARD_OPEN + body + "      }\n"
    text = text[:start] + rebuilt + text[route_idx:]
    text = text.replace(
        '      cmd.command("access").description("Show memory access statistics")',
        '      cmd.command("access-stats").description("Show memory access statistics")',
        1,
    )
    text = text.replace(
        "    if (isFirstRegistration) api.registerService({\n",
        "    const shouldRegisterBackgroundService = isFirstRegistration && !process.argv.includes(\"engram\");\n    if (shouldRegisterBackgroundService) api.registerService({\n",
        1,
    )
    text = text.replace(
        "        if (!setupReportPassed(report)) {\n          process.exitCode = 1;\n          return;\n        }\n        if (!reportHasMachineReadableOutput(options)) console.log(\"OK\");\n",
        "        if (!setupReportPassed(report)) {\n          process.exitCode = 1;\n          scheduleEngramCliExit();\n          return;\n        }\n        if (!reportHasMachineReadableOutput(options)) console.log(\"OK\");\n        scheduleEngramCliExit();\n",
        1,
    )
    text = text.replace(
        "        if (!report.ok) {\n          process.exitCode = 1;\n          return;\n        }\n        if (!reportHasMachineReadableOutput(options)) console.log(\"OK\");\n",
        "        if (!report.ok) {\n          process.exitCode = 1;\n          scheduleEngramCliExit();\n          return;\n        }\n        if (!reportHasMachineReadableOutput(options)) console.log(\"OK\");\n        scheduleEngramCliExit();\n",
        1,
    )
    text = text.replace(
        "        if (!report.ok) {\n          process.exitCode = 1;\n          return;\n        }\n        if (!reportHasMachineReadableOutput(options)) console.log(\"OK\");\n",
        "        if (!report.ok) {\n          process.exitCode = 1;\n          scheduleEngramCliExit();\n          return;\n        }\n        if (!reportHasMachineReadableOutput(options)) console.log(\"OK\");\n        scheduleEngramCliExit();\n",
        1,
    )
    text = text.replace(
        '        if (!query) {\n          console.log("Missing query. Usage: openclaw engram search <query>");\n          return;\n        }\n',
        '        if (!query) {\n          console.log("Missing query. Usage: openclaw engram search <query>");\n          scheduleEngramCliExit();\n          return;\n        }\n',
        1,
    )
    text = text.replace(
        '          if (results.length === 0) {\n            console.log(`No results for: "${query}"`);\n            return;\n          }\n',
        '          if (results.length === 0) {\n            console.log(`No results for: "${query}"`);\n            scheduleEngramCliExit();\n            return;\n          }\n',
        1,
    )
    text = text.replace(
        '          for (const r of results) {\n            console.log(`  ${r.path} (score: ${r.score.toFixed(3)})`);\n            if (r.snippet) {\n              console.log(\n                `    ${r.snippet.slice(0, 150).replace(/\\n/g, " ")}`\n              );\n            }\n            console.log();\n          }\n',
        '          for (const r of results) {\n            console.log(`  ${r.path} (score: ${r.score.toFixed(3)})`);\n            if (r.snippet) {\n              console.log(\n                `    ${r.snippet.slice(0, 150).replace(/\\n/g, " ")}`\n              );\n            }\n            console.log();\n          }\n          scheduleEngramCliExit();\n',
        1,
    )
    text = text.replace(
        '          if (matches.length === 0) {\n            console.log(\n              `No results for: "${query}" (QMD unavailable in this CLI process; text search fallback).`\n            );\n            console.log(`QMD status: ${qmdStatus}`);\n            return;\n          }\n',
        '          if (matches.length === 0) {\n            console.log(\n              `No results for: "${query}" (QMD unavailable in this CLI process; text search fallback).`\n            );\n            console.log(`QMD status: ${qmdStatus}`);\n            scheduleEngramCliExit();\n            return;\n          }\n',
        1,
    )
    text = text.replace(
        '          for (const m of matches.slice(0, maxResults)) {\n            console.log(`  [${m.frontmatter.category}] ${m.content.slice(0, 120)}`);\n          }\n',
        '          for (const m of matches.slice(0, maxResults)) {\n            console.log(`  [${m.frontmatter.category}] ${m.content.slice(0, 120)}`);\n          }\n          scheduleEngramCliExit();\n',
        1,
    )
    return text


def patch_engram_qmd(text: str) -> str:
    if "globalThis.__openclawEngramQmdExitHookBound" in text:
        return text
    text = replace_once(
        text,
        "  constructor(qmdPath) {\n    this.qmdPath = qmdPath;\n  }\n",
        QMD_EXIT_HOOK,
        "engram qmd exit hook",
    )
    return text


def patch_lossless_db_config(text: str) -> str:
    if "shouldUseEphemeralCliDatabase" not in text:
        text = replace_once(
            text,
            "function toNumber(value: unknown): number | undefined {\n",
            'function shouldUseEphemeralCliDatabase(env: NodeJS.ProcessEnv = process.env): boolean {\n'
            '  if (env.LCM_DATABASE_PATH !== undefined) {\n'
            '    return false;\n'
            '  }\n'
            '  const argv = process.argv.map((entry) => entry.trim()).filter(Boolean);\n'
            '  return argv.includes("engram");\n'
            '}\n\n'
            "function toNumber(value: unknown): number | undefined {\n",
            "lossless helper",
        )
    if "const useEphemeralCliDatabase = shouldUseEphemeralCliDatabase(env);" not in text:
        text = replace_once(
            text,
            "  const pc = pluginConfig ?? {};\n",
            "  const pc = pluginConfig ?? {};\n  const useEphemeralCliDatabase = shouldUseEphemeralCliDatabase(env);\n",
            "lossless config local",
        )
    if '?? (useEphemeralCliDatabase ? ":memory:" : undefined)' not in text:
        text = replace_once(
            text,
            "    databasePath:\n      env.LCM_DATABASE_PATH\n      ?? toStr(pc.dbPath)\n",
            "    databasePath:\n      env.LCM_DATABASE_PATH\n      ?? (useEphemeralCliDatabase ? \":memory:\" : undefined)\n      ?? toStr(pc.dbPath)\n",
            "lossless database path",
        )
    return text


def build_qmd_overlay() -> None:
    if not UPSTREAM_QMD_DIR.exists():
        raise RuntimeError(f"upstream qmd not found at {UPSTREAM_QMD_DIR}")
    staging = OVERLAY_DIR.with_name(OVERLAY_DIR.name + ".tmp")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)
    shutil.copytree(UPSTREAM_QMD_DIR / "dist", staging / "dist")
    for rel in ["package.json", "LICENSE", "CHANGELOG.md"]:
        src = UPSTREAM_QMD_DIR / rel
        if src.exists():
            ensure_parent(staging / rel)
            shutil.copy2(src, staging / rel)
    upstream_node_modules = UPSTREAM_QMD_DIR / "node_modules"
    if upstream_node_modules.exists():
        os.symlink(upstream_node_modules, staging / "node_modules", target_is_directory=True)
    write_text(
        staging / "bin" / "qmd",
        QMD_BIN.format(default_path=DEFAULT_PATH, node_bin=NODE_BIN),
        executable=True,
    )
    llm_path = staging / "dist" / "llm.js"
    llm_path.write_text(patch_qmd_llm(llm_path.read_text()))
    if OVERLAY_DIR.exists():
        shutil.rmtree(OVERLAY_DIR)
    staging.rename(OVERLAY_DIR)


def write_qmd_wrapper() -> None:
    wrapper = QMD_WRAPPER_TEMPLATE.format(cfg=CONFIG_PATH, package_dir=OVERLAY_DIR)
    write_text(QMD_WRAPPER, wrapper, executable=True)


def patch_plugin_files() -> None:
    for path, patcher in (
        (ENGRAM_INDEX, patch_engram_index),
        (ENGRAM_QMD, patch_engram_qmd),
        (LOSSLESS_DB_CONFIG, patch_lossless_db_config),
    ):
        backup_file(path)
        path.write_text(patcher(path.read_text()))


def update_config() -> dict:
    backup_file(CONFIG_PATH)
    cfg = json.loads(CONFIG_PATH.read_text())
    plugins = cfg.setdefault("plugins", {}).setdefault("entries", {}).setdefault("openclaw-engram", {}).setdefault("config", {})
    plugins["qmdPath"] = str(QMD_WRAPPER)
    plugins["qmdEnabled"] = True
    plugins["qmdDaemonEnabled"] = True
    memory_qmd = cfg.setdefault("memory", {}).setdefault("qmd", {})
    memory_qmd["command"] = str(QMD_WRAPPER)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n")
    return cfg


def write_state() -> None:
    ensure_parent(OVERLAY_STATE)
    payload = {
        "qmdVersion": json.loads((UPSTREAM_QMD_DIR / "package.json").read_text()).get("version"),
        "engramVersion": json.loads((ENGRAM_DIR / "package.json").read_text()).get("version"),
        "wrapper": str(QMD_WRAPPER),
        "overlay": str(OVERLAY_DIR),
    }
    OVERLAY_STATE.write_text(json.dumps(payload, indent=2) + "\n")


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = DEFAULT_PATH
    return subprocess.run(cmd, text=True, capture_output=True, check=check, env=env)


def verify_fast() -> dict:
    results: dict[str, dict[str, object]] = {}
    commands = {
        "qmd_version": [str(QMD_WRAPPER), "--version"],
        "openclaw_config_validate": [str(OPENCLAW_BIN), "config", "validate"],
        "openclaw_engram_doctor": [str(OPENCLAW_BIN), "engram", "doctor", "--json"],
    }
    for name, cmd in commands.items():
        proc = run(cmd, check=False)
        results[name] = {
            "code": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    (LOG_DIR / "memory-overlay-verify.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-fast", action="store_true")
    args = parser.parse_args()

    build_qmd_overlay()
    write_qmd_wrapper()
    patch_plugin_files()
    update_config()
    write_state()
    if args.verify_fast:
        verify_fast()
    return 0


if __name__ == "__main__":
    sys.exit(main())
