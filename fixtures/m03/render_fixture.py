#!/usr/bin/env python3
import json
from pathlib import Path


NON_CURRENT_STATES = {"STALE", "UNKNOWN", "BLOCKED"}
CURRENT_EVIDENCE_STATUSES = {"VERIFIED", "FIXTURE"}


def _ranking_position(product):
    value = product.get("ranking_position")
    if not isinstance(value, int) or value < 1:
        raise ValueError(f"{product.get('asin', '<unknown>')}: invalid ranking_position")
    return value


def _require_unique(products, field):
    values = [product.get(field) for product in products]
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(f"missing or invalid {field}")
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {field}")


def project_render_model(data):
    if data.get("fixture_only") is not True:
        raise ValueError("synthetic renderer requires fixture_only=true")

    category = data["category"]
    products_input = data["products"]
    _require_unique(products_input, "product_id")
    _require_unique(products_input, "asin")

    category_id = category.get("category_id")
    ranking_method_id = category.get("ranking_method_id")
    if not category_id or not ranking_method_id:
        raise ValueError("category identity/ranking method is incomplete")

    category_freshness = category["freshness_state"]
    category_current = (
        category_freshness not in NON_CURRENT_STATES
        and category.get("evidence_status") in CURRENT_EVIDENCE_STATUSES
    )

    positions = [_ranking_position(product) for product in products_input]
    if len(positions) != len(set(positions)):
        raise ValueError("duplicate ranking_position")

    products = []
    for product in sorted(products_input, key=_ranking_position):
        if product.get("category_id") != category_id:
            raise ValueError(f"{product.get('asin')}: category_id mismatch")
        if product.get("ranking_method_id") != ranking_method_id:
            raise ValueError(f"{product.get('asin')}: ranking_method_id mismatch")

        destination_state = product["outbound_destination_state"]
        freshness_state = product["freshness_state"]
        evidence_status = product.get("evidence_status")
        evidence_current = (
            freshness_state not in NON_CURRENT_STATES
            and evidence_status in CURRENT_EVIDENCE_STATUSES
        )
        fixture_disclosure = True
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
                and evidence_status == "VERIFIED"
                and freshness_state == "CURRENT"
            ),
            "show_ranking": bool(product.get("ranking_evidence_source")) and evidence_current and category_current,
            "show_outbound_cta": (
                destination_state == "VERIFIED"
                and evidence_status == "VERIFIED"
                and bool(product.get("outbound_url"))
                and evidence_current
            ),
            "show_local_checkout": False,
            "commercial_fields": {},
        })
    return {
        "component": "mpd-category-view",
        "category_id": category_id,
        "category_name": category["name"],
        "marketplace": category["marketplace"],
        "ranking_evidence_badge": category_freshness,
        "fixture_disclosure": True,
        "products": products,
    }


def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    print(json.dumps(project_render_model(data), indent=2))


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("prime-discovery.synthetic.json")
    main(target)
