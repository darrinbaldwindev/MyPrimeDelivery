#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")
ALLOWED_POLICIES = {"ALLOWED_CURRENT", "ALLOWED_WITH_EXPIRY", "HOLD_RIGHTS_UNKNOWN", "HOLD_UNSUPPORTED"}
EXPECTED_PROFILE = "amazon-creators-api-au-v1"
EXPECTED_MARKETPLACE = "www.amazon.com.au"


def fail(msg: str):
    raise AssertionError(msg)


def stable_payload(snapshot: dict) -> dict:
    return {k: v for k, v in snapshot.items() if k not in {"snapshot_id", "replay_of", "expected_disposition"}}


def fingerprint(snapshot: dict) -> str:
    body = json.dumps(stable_payload(snapshot), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def project(snapshot: dict, policies: dict) -> dict:
    card = {
        "component": "mpd-product-card",
        "marketplace": snapshot["marketplace"],
        "asin": snapshot["asin"],
        "title": snapshot["title"],
        "prime_state": "UNKNOWN",
        "deal_state": "ACTIVE" if (snapshot.get("deal_details") or {}).get("present") else "UNKNOWN",
        "availability_state": (snapshot.get("availability") or {}).get("type", "UNKNOWN"),
        "publication_authority": False,
        "outbound_enabled": False,
        "network_io": False,
    }
    if policies.get("price") in {"ALLOWED_CURRENT", "ALLOWED_WITH_EXPIRY"} and snapshot.get("price"):
        card["price_observation"] = snapshot["price"]
    if policies.get("image") not in {"ALLOWED_CURRENT", "ALLOWED_WITH_EXPIRY"}:
        card["image_url"] = None
    return card


def validate(data: dict) -> list[dict]:
    if data.get("research_only") is not True:
        fail("research_only must be true")
    if data.get("provider_profile_id") != EXPECTED_PROFILE:
        fail("unexpected provider profile")
    policies = data.get("field_policies") or {}
    if not policies or any(v not in ALLOWED_POLICIES for v in policies.values()):
        fail("invalid field policy")
    if policies.get("prime") != "HOLD_UNSUPPORTED":
        fail("Prime must remain unsupported in this profile")

    latest_version = {}
    latest_fingerprint = {}
    accepted = []
    by_snapshot = {}

    for s in data.get("snapshots") or []:
        sid = s.get("snapshot_id")
        if not sid or sid in by_snapshot:
            fail("snapshot_id must be present and unique")
        by_snapshot[sid] = s
        expected = s.get("expected_disposition")

        if s.get("marketplace") != EXPECTED_MARKETPLACE or s.get("x_marketplace") != s.get("marketplace"):
            actual = "MARKETPLACE_MISMATCH"
        elif not ASIN_RE.fullmatch(s.get("asin") or ""):
            actual = "INVALID_ASIN"
        elif not isinstance(s.get("provider_version"), int) or s["provider_version"] <= 0:
            actual = "INVALID_PROVIDER_VERSION"
        elif not isinstance(s.get("title"), str) or not s["title"].strip():
            actual = "MISSING_TITLE"
        else:
            replay_of = s.get("replay_of")
            asin = s["asin"]
            version = s["provider_version"]
            fp = fingerprint(s)
            if replay_of:
                original = by_snapshot.get(replay_of)
                if original is None or fingerprint(original) != fp:
                    actual = "REPLAY_MISMATCH"
                else:
                    actual = "IDEMPOTENT_REPLAY"
            elif asin in latest_version and version < latest_version[asin]:
                actual = "STALE_VERSION_REJECTED"
            elif asin in latest_version and version == latest_version[asin] and fp != latest_fingerprint[asin]:
                actual = "VERSION_CONFLICT"
            else:
                latest_version[asin] = version
                latest_fingerprint[asin] = fp
                actual = "ACCEPT"
                accepted.append({
                    "snapshot_id": sid,
                    "provider_version": version,
                    "evidence_fingerprint": fp,
                    "wordpress_projection": project(s, policies),
                })

        if actual != expected:
            fail(f"{sid}: {actual} != {expected}")

    if not accepted:
        fail("fixture must contain accepted snapshots")
    for item in accepted:
        card = item["wordpress_projection"]
        if card["publication_authority"] or card["outbound_enabled"] or card["network_io"]:
            fail("staging projection must not grant authority")
        if card["prime_state"] != "UNKNOWN":
            fail("Creators API profile must not infer Prime")
    return accepted


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("creators_api_au.synthetic.json")
    accepted = validate(json.loads(path.read_text(encoding="utf-8")))
    print("PASS: Creators API AU mapping/lineage is deterministic and fail-closed")
    print(json.dumps(accepted, indent=2, sort_keys=True))
