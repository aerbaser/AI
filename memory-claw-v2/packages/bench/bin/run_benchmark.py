#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from memory_claw_bench.benchmark import summarize_results
from memory_claw_bench.config import load_candidates
from memory_claw_bench.goldset import build_gold_set
from memory_claw_bench.runners import get_runner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", help="candidate id to run")
    parser.add_argument(
        "--gold-set",
        default=str(Path(__file__).resolve().parents[3] / "examples" / "benchmark" / "gold-set.template.json"),
    )
    parser.add_argument(
        "--config",
        default=str(ROOT / "config" / "candidates.json"),
    )
    parser.add_argument(
        "--results-dir",
        default=str(ROOT / "results"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gold_set = json.loads(Path(args.gold_set).read_text(encoding="utf-8"))
    if gold_set and "id" not in gold_set[0]:
        gold_set = build_gold_set(gold_set)
    candidates = load_candidates(Path(args.config))
    if args.candidate:
        candidates = [candidate for candidate in candidates if candidate.id == args.candidate]
    if not candidates:
        raise SystemExit("no matching candidates")

    all_rows: list[dict] = []
    for candidate in candidates:
        runner = get_runner(candidate.runner)
        context = {"candidate_id": candidate.id, "candidate_label": candidate.label}
        for case in gold_set:
            all_rows.append(runner(case, context))

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    raw_path = results_dir / "latest-raw.json"
    summary_path = results_dir / "latest-summary.json"
    raw_path.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary_path.write_text(
        json.dumps(summarize_results(all_rows), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
