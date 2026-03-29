from memory_claw_bench.benchmark import summarize_results


def test_summarize_results_groups_by_candidate() -> None:
    rows = [
        {
            "candidate_id": "current-prod",
            "recall_score": 0.9,
            "prompt_tokens": 100,
            "background_tokens": 40,
            "latency_ms": 1200,
        },
        {
            "candidate_id": "current-prod",
            "recall_score": 0.7,
            "prompt_tokens": 110,
            "background_tokens": 30,
            "latency_ms": 900,
        },
        {
            "candidate_id": "baseline-none",
            "recall_score": 0.2,
            "prompt_tokens": 180,
            "background_tokens": 0,
            "latency_ms": 300,
        },
    ]

    summary = summarize_results(rows)

    assert [entry["candidate_id"] for entry in summary] == [
        "current-prod",
        "baseline-none",
    ]
    assert summary[0]["cases"] == 2
    assert summary[0]["avg_recall_score"] == 0.8
    assert summary[0]["avg_total_tokens"] == 140.0


def test_summarize_results_sorts_by_recall_then_tokens() -> None:
    rows = [
        {
            "candidate_id": "a",
            "recall_score": 0.5,
            "prompt_tokens": 100,
            "background_tokens": 50,
            "latency_ms": 500,
        },
        {
            "candidate_id": "b",
            "recall_score": 0.5,
            "prompt_tokens": 90,
            "background_tokens": 20,
            "latency_ms": 600,
        },
    ]

    summary = summarize_results(rows)

    assert [entry["candidate_id"] for entry in summary] == ["b", "a"]
