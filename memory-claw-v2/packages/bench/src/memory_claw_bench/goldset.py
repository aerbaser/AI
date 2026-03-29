from __future__ import annotations


def build_gold_set(rows: list[dict]) -> list[dict]:
    gold_set: list[dict] = []
    for index, row in enumerate(rows, start=1):
        question = row.get("question")
        expected_facts = row.get("expected_facts")
        tags = row.get("tags", [])
        if not question:
            raise ValueError("question is required")
        if not expected_facts:
            raise ValueError("expected_facts is required")
        gold_set.append(
            {
                "id": f"mem-{index:03d}",
                "question": question,
                "expected_facts": list(expected_facts),
                "tags": list(tags),
            }
        )
    return gold_set
