import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "bin"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from render_openclaw_overlay import apply_overlay, parse_args


def test_apply_overlay_sets_safe_memory_defaults(monkeypatch) -> None:
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    args = parse_args(["--config", "ignored"])
    cfg = {}

    rendered = apply_overlay(cfg, args)

    assert rendered["plugins"]["allow"] == ["lossless-claw", "openclaw-engram"]
    assert rendered["plugins"]["entries"]["lossless-claw"]["enabled"] is True
    assert rendered["plugins"]["entries"]["memos-capture"]["enabled"] is False
    defaults = rendered["agents"]["defaults"]["memorySearch"]
    assert defaults["sources"] == ["memory"]
    assert defaults["extraPaths"] == [str(Path("~/.openclaw/shared-memory").expanduser())]
    assert defaults["provider"] == "voyage"
    assert defaults["fallback"] == "local"
    assert defaults["remote"]["apiKey"] == "test-key"
    assert rendered["plugins"]["entries"]["openclaw-engram"]["config"]["lcmEnabled"] is False
    assert rendered["plugins"]["entries"]["openclaw-engram"]["config"]["sharedContextEnabled"] is True
    assert rendered["plugins"]["entries"]["openclaw-engram"]["config"]["sharedContextDir"] == str(
        Path("~/.openclaw/shared-memory").expanduser()
    )
    assert rendered["memory"]["qmd"]["includeDefaultMemory"] is False
    assert rendered["memory"]["qmd"]["paths"] == [
        {
            "path": str(Path("~/.openclaw/shared-memory").expanduser()),
            "name": "shared-memory",
            "pattern": "**/*.md",
        }
    ]
    assert rendered["memory"]["qmd"]["sessions"]["enabled"] is False


def test_renderer_writes_json(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    source = tmp_path / "openclaw.json"
    source.write_text(json.dumps({"agents": {"defaults": {}}}), encoding="utf-8")
    output = tmp_path / "rendered.json"

    from render_openclaw_overlay import main

    argv = [
        "render_openclaw_overlay.py",
        "--config",
        str(source),
        "--output",
        str(output),
    ]
    monkeypatch.setattr(sys, "argv", argv)

    assert main() == 0
    rendered = json.loads(output.read_text(encoding="utf-8"))
    assert rendered["memory"]["backend"] == "qmd"
