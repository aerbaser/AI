from __future__ import annotations

from . import baseline_none, current_clean, current_prod, engram_linux, graph_memory, memos_local


RUNNERS = {
    "baseline_none": baseline_none.run_case,
    "current_clean": current_clean.run_case,
    "current_prod": current_prod.run_case,
    "engram_linux": engram_linux.run_case,
    "graph_memory": graph_memory.run_case,
    "memos_local": memos_local.run_case,
}


def get_runner(name: str):
    try:
        return RUNNERS[name]
    except KeyError as exc:
        raise ValueError(f"unknown runner: {name}") from exc
