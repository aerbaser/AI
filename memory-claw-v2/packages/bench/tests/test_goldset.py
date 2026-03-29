from memory_claw_bench.goldset import build_gold_set


def test_build_gold_set_assigns_stable_ids() -> None:
    rows = [
        {
            "question": "What should memorySearch.sources contain by default?",
            "expected_facts": ["memory only"],
            "tags": ["memory"],
        },
        {
            "question": "Why are raw sessions dangerous?",
            "expected_facts": ["noise", "latency"],
            "tags": ["sessions"],
        },
    ]

    gold_set = build_gold_set(rows)

    assert [entry["id"] for entry in gold_set] == ["mem-001", "mem-002"]
    assert gold_set[0]["question"].startswith("What should")
    assert gold_set[1]["expected_facts"] == ["noise", "latency"]


def test_build_gold_set_rejects_missing_expected_facts() -> None:
    rows = [{"question": "broken", "tags": ["memory"]}]

    try:
        build_gold_set(rows)
    except ValueError as exc:
        assert "expected_facts" in str(exc)
    else:
        raise AssertionError("expected ValueError")
