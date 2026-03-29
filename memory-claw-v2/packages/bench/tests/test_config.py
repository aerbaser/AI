from pathlib import Path

import pytest

from memory_claw_bench.config import load_candidates


def test_load_candidates_reads_enabled_entries(tmp_path: Path) -> None:
    config_path = tmp_path / "candidates.json"
    config_path.write_text(
        """
        {
          "candidates": [
            {"id": "current-prod", "enabled": true, "runner": "current_prod"},
            {"id": "graph-memory", "enabled": false, "runner": "graph_memory"}
          ]
        }
        """.strip(),
        encoding="utf-8",
    )

    candidates = load_candidates(config_path)

    assert [candidate.id for candidate in candidates] == ["current-prod"]
    assert candidates[0].runner == "current_prod"


def test_load_candidates_rejects_missing_runner(tmp_path: Path) -> None:
    config_path = tmp_path / "candidates.json"
    config_path.write_text(
        """
        {
          "candidates": [
            {"id": "broken", "enabled": true}
          ]
        }
        """.strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="runner"):
        load_candidates(config_path)
