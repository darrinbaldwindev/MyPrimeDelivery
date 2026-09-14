#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from validate_deal_fixture import validate


def project_offer(offer):
    active = offer.get("deal_state") == "ACTIVE"
    return {
        "offer_id": offer.get("offer_id"),
        "deal_state": offer.get("deal_state"),
        "sale_badge": "SALE" if active else None,
        "discount_percent": offer.get("discount_percent") if active else None,
        "urgency_visible": bool(active),
        "prime_state": offer.get("prime_state"),
        "outbound_enabled": False,
    }


def render(path: Path):
    validate(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "fixture_only": True,
        "as_of": data["as_of"],
        "offers": [project_offer(offer) for offer in data["offers"]],
    }


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("deal-evidence.synthetic.json")
    print(json.dumps(render(target), indent=2, sort_keys=True))
