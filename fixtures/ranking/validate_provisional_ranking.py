#!/usr/bin/env python3
import json
import sys
from pathlib import Path

MAXIMA = {
    "selection_strength": 40,
    "evidence_confidence": 25,
    "freshness_strength": 20,
    "deal_relevance": 10,
    "editorial_utility": 5,
}


def fail(message: str) -> None:
    raise AssertionError(message)


def score(record: dict) -> int:
    total = 0
    for field, maximum in MAXIMA.items():
        value = record.get(field)
        if not isinstance(value, int) or value < 0 or value > maximum:
            fail(f"{record.get('product_id')}: {field} outside 0-{maximum}")
        total += value
    return total


def is_eligible(record: dict) -> bool:
    return (
        record.get("identity_state") == "ASIN_VERIFIED"
        and record.get("marketplace") == "AU"
        and record.get("prime_state") == "VERIFIED"
        and record.get("freshness_state") == "CURRENT"
    )


def rank(data: dict) -> list[str]:
    seen = set()
    ranked = []
    for r in data.get("products", []):
        pid = r.get("product_id")
        if not pid or pid in seen:
            fail("product_id must be present and unique")
        seen.add(pid)
        computed = is_eligible(r)
        if r.get("eligible") is not computed:
            fail(f"{pid}: eligible flag disagrees with fail-closed gates")
        s = score(r)
        if computed:
            ranked.append((
                -s,
                -r["evidence_confidence"],
                -r["freshness_strength"],
                -r["selection_strength"],
                pid,
            ))
    ranked.sort()
    return [row[-1] for row in ranked]


def validate(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("research_only") is not True:
        fail("research_only must be true")
    if data.get("ranking_method_id") != "provisional-v1":
        fail("unexpected ranking_method_id")
    order = rank(data)
    if order != data.get("expected_order"):
        fail(f"ranking mismatch: {order} != {data.get('expected_order')}")
    return order


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("provisional-ranking.synthetic.json")
    order = validate(target)
    print("PASS: provisional ranking is deterministic and fail-closed")
    print(json.dumps(order))
