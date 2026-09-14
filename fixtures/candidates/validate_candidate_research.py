#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_STATES = {"DISCOVERED", "CANDIDATE", "QUALIFIED", "REJECTED", "STALE", "BLOCKED"}
ALLOWED_CATEGORIES = {
    "cat-home-kitchen", "cat-electronics", "cat-baby", "cat-pet-supplies",
    "cat-health-household", "cat-beauty-personal-care", "cat-tools-home-improvement",
    "cat-toys-games", "cat-sports-outdoors", "cat-office-products", "cat-automotive",
    "cat-garden-outdoors"
}


def fail(message: str) -> None:
    raise AssertionError(message)


def validate(path: Path) -> Counter:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("research_only") is not True:
        fail("research_only must be true")
    records = data.get("candidates") or []
    if not records:
        fail("candidate dataset must not be empty")

    seen = set()
    counts = Counter()
    for r in records:
        cid = r.get("candidate_id")
        if not cid or cid in seen:
            fail("candidate_id must be present and unique")
        seen.add(cid)
        if r.get("state") not in ALLOWED_STATES:
            fail(f"{cid}: invalid state")
        cat = r.get("category_id")
        if cat not in ALLOWED_CATEGORIES:
            fail(f"{cid}: unsupported category_id")
        counts[cat] += 1

        source_url = r.get("source_url")
        source_domain = r.get("source_domain")
        if not source_url or not source_domain:
            fail(f"{cid}: provenance required")
        parsed = urlparse(source_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            fail(f"{cid}: invalid source_url")
        if source_domain not in parsed.netloc:
            fail(f"{cid}: source_domain does not match source_url")

        blob = json.dumps(r, sort_keys=True).lower()
        if "tag=" in blob or "amzn.to" in blob:
            fail(f"{cid}: affiliate destination/tag leakage")

        if r.get("state") == "QUALIFIED":
            if r.get("prime_evidence_state") != "VERIFIED":
                fail(f"{cid}: QUALIFIED requires VERIFIED Prime evidence")
            if r.get("selection_evidence_state") != "VERIFIED":
                fail(f"{cid}: QUALIFIED requires VERIFIED selection/ranking evidence")
            if r.get("freshness_state") != "CURRENT":
                fail(f"{cid}: QUALIFIED requires CURRENT freshness")
            if not r.get("prime_evidence_source") or not r.get("prime_checked_at"):
                fail(f"{cid}: QUALIFIED requires authoritative Prime source + checked_at")

        if r.get("prime_evidence_state") == "VERIFIED":
            if not r.get("prime_evidence_source") or not r.get("prime_checked_at"):
                fail(f"{cid}: Prime VERIFIED requires source + checked_at")

        if r.get("freshness_state") == "STALE" and r.get("state") in {"QUALIFIED", "CANDIDATE"}:
            fail(f"{cid}: stale evidence cannot be presented as current candidate/qualified")

    return counts


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("first-100-research.json")
    counts = validate(target)
    print(f"PASS: {target} candidate research dataset is fail-closed")
    print(json.dumps(dict(sorted(counts.items())), indent=2))
