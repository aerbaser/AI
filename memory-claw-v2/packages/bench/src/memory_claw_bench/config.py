from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Candidate:
    id: str
    runner: str
    enabled: bool = True
    label: str | None = None
    notes: str | None = None


def load_candidates(config_path: Path) -> list[Candidate]:
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    entries = raw.get("candidates", [])
    if not isinstance(entries, list):
        raise ValueError("candidates must be a list")

    loaded: list[Candidate] = []
    for entry in entries:
        if not entry.get("enabled", True):
            continue
        candidate_id = entry.get("id")
        runner = entry.get("runner")
        if not candidate_id:
            raise ValueError("candidate id is required")
        if not runner:
            raise ValueError(f"candidate {candidate_id!r} is missing runner")
        loaded.append(
            Candidate(
                id=candidate_id,
                runner=runner,
                enabled=bool(entry.get("enabled", True)),
                label=entry.get("label"),
                notes=entry.get("notes"),
            )
        )
    return loaded
