#!/usr/bin/env python3
import json
from pathlib import Path


def project_render_model(data):
    category = data["category"]
    products = []
    for product in sorted(data["products"], key=lambda p: p["ranking_position"]):
        destination_state = product["outbound_destination_state"]
        products.append({
            "component": "mpd-product-card",
            "product_id": product["product_id"],
            "asin": product["asin"],
            "title": product["title"],
            "prime_state": product["prime_state"],
            "ranking_position": product["ranking_position"],
            "evidence_badge": product["freshness_state"],
            "show_prime_positive_claim": product["prime_state"] == "VERIFIED" and product["evidence_status"] == "VERIFIED",
            "show_ranking": bool(product.get("ranking_evidence_source")),
            "show_outbound_cta": destination_state == "VERIFIED" and bool(product.get("outbound_url")),
            "show_local_checkout": False,
            "commercial_fields": {},
        })
    return {
        "component": "mpd-category-view",
        "category_id": category["category_id"],
        "category_name": category["name"],
        "marketplace": category["marketplace"],
        "ranking_evidence_badge": category["freshness_state"],
        "products": products,
    }


def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    print(json.dumps(project_render_model(data), indent=2))


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("prime-discovery.synthetic.json")
    main(target)
