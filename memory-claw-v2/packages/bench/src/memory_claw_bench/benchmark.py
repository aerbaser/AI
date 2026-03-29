from __future__ import annotations

from collections import defaultdict


def summarize_results(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["candidate_id"]].append(row)

    summary: list[dict] = []
    for candidate_id, candidate_rows in grouped.items():
        cases = len(candidate_rows)
        total_recall = sum(float(row.get("recall_score", 0.0)) for row in candidate_rows)
        total_tokens = sum(
            float(row.get("prompt_tokens", 0.0)) + float(row.get("background_tokens", 0.0))
            for row in candidate_rows
        )
        total_latency = sum(float(row.get("latency_ms", 0.0)) for row in candidate_rows)
        summary.append(
            {
                "candidate_id": candidate_id,
                "cases": cases,
                "avg_recall_score": round(total_recall / cases, 4),
                "avg_total_tokens": round(total_tokens / cases, 4),
                "avg_latency_ms": round(total_latency / cases, 4),
            }
        )

    return sorted(
        summary,
        key=lambda item: (-item["avg_recall_score"], item["avg_total_tokens"], item["avg_latency_ms"]),
    )
