#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_EVIDENCE = {"FIXTURE", "UNKNOWN", "STALE", "BLOCKED", "VERIFIED"}
ALLOWED_PRIME = {"VERIFIED", "NOT_VERIFIED", "UNKNOWN", "STALE"}
ALLOWED_DEST = {"DISABLED", "FIXTURE_ONLY", "VERIFIED"}
FORBIDDEN_COMMERCIAL_FIELDS = {"price", "currency", "image_url", "rating", "review_count", "availability_state"}


def fail(message: str) -> None:
    raise AssertionError(message)


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("fixture_only") is not True:
        fail("fixture_only must be true")

    category = data.get("category") or {}
    ranking = data.get("ranking_method") or {}
    products = data.get("products") or []

    if len(products) != 3:
        fail("fixture must contain exactly three products")
    if category.get("marketplace") != "UNKNOWN":
        fail("synthetic category marketplace must remain UNKNOWN")
    if category.get("freshness_state") != "FIXTURE" or category.get("evidence_status") != "FIXTURE":
        fail("synthetic category must remain FIXTURE evidence")
    if ranking.get("status") != "FIXTURE" or ranking.get("source_type") != "synthetic_fixture":
        fail("ranking method must be explicit synthetic FIXTURE evidence")
    if category.get("ranking_method_id") != ranking.get("ranking_method_id"):
        fail("category ranking method must match fixture ranking method")

    seen_asins = set()
    positions = []
    for product in products:
        asin = product.get("asin")
        if not isinstance(asin, str) or not asin.startswith("TEST-ASIN-"):
            fail("all ASINs must be obviously synthetic TEST-ASIN identifiers")
        if asin in seen_asins:
            fail("duplicate fixture ASIN")
        seen_asins.add(asin)

        if product.get("category_id") != category.get("category_id"):
            fail(f"{asin}: invalid category reference")
        if product.get("marketplace") != "UNKNOWN":
            fail(f"{asin}: synthetic marketplace must remain UNKNOWN")
        if product.get("prime_state") not in ALLOWED_PRIME:
            fail(f"{asin}: invalid prime_state")
        if product.get("prime_state") == "VERIFIED":
            if not product.get("prime_evidence_source") or not product.get("prime_checked_at"):
                fail(f"{asin}: VERIFIED Prime state requires source and checked_at")
            if product.get("evidence_status") != "VERIFIED":
                fail(f"{asin}: VERIFIED Prime state requires VERIFIED evidence_status")
        if product.get("evidence_status") not in ALLOWED_EVIDENCE:
            fail(f"{asin}: invalid evidence_status")
        if product.get("freshness_state") != "FIXTURE":
            fail(f"{asin}: synthetic freshness_state must remain FIXTURE")
        if product.get("ranking_method_id") != ranking.get("ranking_method_id"):
            fail(f"{asin}: ranking method mismatch")
        if product.get("ranking_position") is not None and not product.get("ranking_evidence_source"):
            fail(f"{asin}: ranking position requires ranking evidence")
        positions.append(product.get("ranking_position"))

        destination = product.get("outbound_destination_state")
        if destination not in ALLOWED_DEST:
            fail(f"{asin}: invalid outbound_destination_state")
        if destination != "VERIFIED" and product.get("outbound_url") not in (None, ""):
            fail(f"{asin}: non-VERIFIED destination must not expose outbound_url")

        leaked = FORBIDDEN_COMMERCIAL_FIELDS.intersection(product.keys())
        if leaked:
            fail(f"{asin}: unsupported commercial fields present: {sorted(leaked)}")

        blob = json.dumps(product, sort_keys=True).lower()
        if "amazon.com" in blob or "amzn.to" in blob or "tag=" in blob:
            fail(f"{asin}: possible live Amazon/affiliate destination leaked")

    if sorted(positions) != [1, 2, 3]:
        fail("fixture ranking positions must be exactly 1, 2, 3")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("prime-discovery.synthetic.json")
    validate(target)
    print(f"PASS: {target} is a fail-closed MyPrimeDelivery M-03 synthetic fixture")
