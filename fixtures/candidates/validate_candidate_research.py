#!/usr/bin/env python3
import json
import re
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


def _candidate_number(candidate_id: str) -> int:
    match = re.fullmatch(r"cand-(\d+)", candidate_id or "")
    if not match:
        fail(f"{candidate_id}: candidate_id must use cand-NNN form")
    return int(match.group(1))


def validate_collection(paths: list[Path]) -> Counter:
    global_seen = set()
    cumulative = Counter()
    ordered_ids = []
    for path in paths:
        cumulative.update(validate(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data["candidates"]:
            cid = record["candidate_id"]
            if cid in global_seen:
                fail(f"{cid}: duplicate candidate_id across research tranches")
            global_seen.add(cid)
            ordered_ids.append(cid)

    numeric = [_candidate_number(cid) for cid in ordered_ids]
    if numeric != sorted(numeric) or len(numeric) != len(set(numeric)):
        fail("candidate ordering must be deterministic and globally increasing")
    missing = ALLOWED_CATEGORIES.difference(cumulative)
    if missing:
        fail("cumulative dataset missing launch categories: " + ", ".join(sorted(missing)))
    return cumulative


if __name__ == "__main__":
    targets = [Path(arg) for arg in sys.argv[1:]] or [Path(__file__).with_name("first-100-research.json")]
    if len(targets) == 1:
        counts = validate(targets[0])
        print(f"PASS: {targets[0]} candidate research dataset is fail-closed")
    else:
        counts = validate_collection(targets)
        print(f"PASS: {len(targets)} candidate research tranches are cross-validated fail-closed")
    print(json.dumps(dict(sorted(counts.items())), indent=2))
