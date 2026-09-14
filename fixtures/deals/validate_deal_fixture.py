#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_STATES = {"ACTIVE", "STALE", "EXPIRED", "UNKNOWN", "BLOCKED"}
ALLOWED_PRIME = {"VERIFIED", "NOT_VERIFIED", "UNKNOWN", "STALE"}


def fail(message: str) -> None:
    raise AssertionError(message)


def parse_ts(value):
    if value in (None, ""):
        return None
    if not isinstance(value, str) or not value.endswith("Z"):
        fail(f"invalid UTC timestamp: {value!r}")
    return datetime.fromisoformat(value[:-1] + "+00:00").astimezone(timezone.utc)


def derived_state(offer, as_of, stale_after_seconds):
    if offer.get("source_conflict") is True:
        return "BLOCKED"
    if not offer.get("evidence_source") or not offer.get("source_record_id") or not offer.get("checked_at"):
        return "UNKNOWN"
    checked_at = parse_ts(offer.get("checked_at"))
    expires_at = parse_ts(offer.get("expires_at"))
    if expires_at is not None and expires_at <= as_of:
        return "EXPIRED"
    age_seconds = (as_of - checked_at).total_seconds()
    if age_seconds < 0:
        fail(f"{offer.get('offer_id')}: checked_at is in the future")
    if age_seconds > stale_after_seconds:
        return "STALE"
    return "ACTIVE"


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("fixture_only") is not True:
        fail("fixture_only must be true")
    if data.get("schema") != "myprime.deal.fixture.v1":
        fail("unexpected fixture schema")

    as_of = parse_ts(data.get("as_of"))
    if as_of is None:
        fail("as_of is required")
    stale_after = data.get("stale_after_seconds")
    if not isinstance(stale_after, int) or stale_after <= 0:
        fail("stale_after_seconds must be a positive integer")

    offers = data.get("offers") or []
    if len(offers) < 5:
        fail("fixture must cover at least five representative offer states")

    seen_ids = set()
    seen_states = set()
    for offer in offers:
        offer_id = offer.get("offer_id")
        if not isinstance(offer_id, str) or not offer_id.startswith("FIXTURE-OFFER-"):
            fail("offer_id must be an obvious fixture identifier")
        if offer_id in seen_ids:
            fail(f"duplicate offer_id: {offer_id}")
        seen_ids.add(offer_id)

        asin = offer.get("asin")
        if not isinstance(asin, str) or not asin.startswith("TEST-ASIN-"):
            fail(f"{offer_id}: ASIN must be synthetic")
        if offer.get("marketplace") != "UNKNOWN":
            fail(f"{offer_id}: synthetic marketplace must remain UNKNOWN")
        if offer.get("prime_state") not in ALLOWED_PRIME:
            fail(f"{offer_id}: invalid prime_state")
        if offer.get("prime_state") != "UNKNOWN":
            fail(f"{offer_id}: deal fixture must not infer Prime state")
        if offer.get("outbound_url") not in (None, ""):
            fail(f"{offer_id}: fixture must not expose an outbound URL")

        declared = offer.get("deal_state")
        if declared not in ALLOWED_STATES:
            fail(f"{offer_id}: invalid deal_state")
        expected = derived_state(offer, as_of, stale_after)
        if declared != expected:
            fail(f"{offer_id}: declared {declared} but evidence derives {expected}")
        seen_states.add(declared)

        current = offer.get("current_price")
        reference = offer.get("reference_price")
        discount = offer.get("discount_percent")
        price_source = offer.get("price_evidence_source")

        if discount is not None:
            if declared != "ACTIVE":
                fail(f"{offer_id}: non-ACTIVE offer must not claim a discount")
            if current is None or reference is None or not price_source:
                fail(f"{offer_id}: discount requires current/reference price evidence")
            if not isinstance(current, (int, float)) or not isinstance(reference, (int, float)):
                fail(f"{offer_id}: prices must be numeric")
            if reference <= current:
                fail(f"{offer_id}: reference price must exceed current price")
            expected_discount = round((reference - current) / reference * 100, 2)
            if abs(float(discount) - expected_discount) > 0.01:
                fail(f"{offer_id}: discount_percent does not match evidence-backed prices")

        blob = json.dumps(offer, sort_keys=True).lower()
        if "amazon." in blob or "amzn.to" in blob or "tag=" in blob:
            fail(f"{offer_id}: possible live Amazon/affiliate destination leaked")

    missing = ALLOWED_STATES - seen_states
    if missing:
        fail(f"fixture does not cover states: {sorted(missing)}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("deal-evidence.synthetic.json")
    validate(target)
    print(f"PASS: {target} is a fail-closed synthetic deal evidence fixture")
