from __future__ import annotations


def run_case(case: dict, context: dict) -> dict:
    return {
        "candidate_id": context["candidate_id"],
        "case_id": case["id"],
        "recall_score": 0.0,
        "prompt_tokens": 0,
        "background_tokens": 0,
        "latency_ms": 0,
        "status": "ok",
        "notes": "No retrieval performed.",
    }
