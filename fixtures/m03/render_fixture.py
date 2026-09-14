#!/usr/bin/env python3
import json
from pathlib import Path


NON_CURRENT_STATES = {"STALE", "UNKNOWN", "BLOCKED"}


def _ranking_position(product):
    value = product.get("ranking_position")
    if not isinstance(value, int) or value < 1:
        raise ValueError(f"{product.get('asin', '<unknown>')}: invalid ranking_position")
    return value


def project_render_model(data):
    category = data["category"]
    category_freshness = category["freshness_state"]
    category_current = category_freshness not in NON_CURRENT_STATES
    products = []
    for product in sorted(data["products"], key=_ranking_position):
        destination_state = product["outbound_destination_state"]
        freshness_state = product["freshness_state"]
        evidence_current = freshness_state not in NON_CURRENT_STATES
        fixture_disclosure = bool(data.get("fixture_only"))
        products.append({
            "component": "mpd-product-card",
            "product_id": product["product_id"],
            "asin": product["asin"],
            "title": product["title"],
            "prime_state": product["prime_state"],
            "ranking_position": product["ranking_position"],
            "evidence_badge": freshness_state,
            "fixture_disclosure": fixture_disclosure,
            "show_prime_positive_claim": (
                product["prime_state"] == "VERIFIED"
                and product["evidence_status"] == "VERIFIED"
                and freshness_state == "CURRENT"
            ),
            "show_ranking": bool(product.get("ranking_evidence_source")) and evidence_current and category_current,
            "show_outbound_cta": destination_state == "VERIFIED" and bool(product.get("outbound_url")) and evidence_current,
            "show_local_checkout": False,
            "commercial_fields": {},
        })
    return {
        "component": "mpd-category-view",
        "category_id": category["category_id"],
        "category_name": category["name"],
        "marketplace": category["marketplace"],
        "ranking_evidence_badge": category_freshness,
        "fixture_disclosure": bool(data.get("fixture_only")),
        "products": products,
    }


def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    print(json.dumps(project_render_model(data), indent=2))


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("prime-discovery.synthetic.json")
    main(target)
