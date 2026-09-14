#!/usr/bin/env python3
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def normalize_title(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def analyze(paths: list[Path]) -> dict:
    rows = []
    seen_ids = set()
    by_title = defaultdict(list)
    categories = Counter()

    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("candidates", []):
            cid = record.get("candidate_id")
            if not cid or cid in seen_ids:
                raise AssertionError(f"duplicate or missing candidate_id: {cid}")
            seen_ids.add(cid)
            title = record.get("title") or ""
            key = normalize_title(title)
            if not key:
                raise AssertionError(f"{cid}: empty normalized title")
            item = {
                "candidate_id": cid,
                "title": title,
                "category_id": record.get("category_id"),
                "normalized_title": key,
                "source_file": path.name,
            }
            rows.append(item)
            by_title[key].append(item)
            categories[item["category_id"]] += 1

    duplicate_groups = []
    for key, items in sorted(by_title.items()):
        if len(items) < 2:
            continue
        cats = {item["category_id"] for item in items}
        if len(cats) != 1:
            raise AssertionError(f"category conflict for duplicate title '{key}': {sorted(cats)}")
        duplicate_groups.append({
            "normalized_title": key,
            "category_id": items[0]["category_id"],
            "candidate_ids": [item["candidate_id"] for item in items],
            "titles": [item["title"] for item in items],
        })

    return {
        "evidence_rows": len(rows),
        "unique_normalized_titles": len(by_title),
        "duplicate_groups": duplicate_groups,
        "duplicate_row_count": sum(len(g["candidate_ids"]) - 1 for g in duplicate_groups),
        "category_row_counts": dict(sorted(categories.items())),
        "identity_note": "Normalized-title equivalence is a review signal only; it does not prove ASIN equivalence or variant identity.",
    }


if __name__ == "__main__":
    targets = [Path(arg) for arg in sys.argv[1:]]
    if not targets:
        base = Path(__file__).parent
        targets = [
            base / "first-100-research.json",
            base / "research-tranche-004.json",
            base / "research-tranche-005.json",
        ]
    result = analyze(targets)
    print(json.dumps(result, indent=2, sort_keys=True))
