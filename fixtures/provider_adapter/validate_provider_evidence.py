#!/usr/bin/env python3
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")
ALLOWED_KINDS = {"PRODUCT", "PARENT", "VARIANT"}
ALLOWED_FRESHNESS = {"CURRENT", "STALE", "EXPIRED", "UNKNOWN"}


@dataclass(frozen=True)
class AdapterDecision:
    disposition: str
    reason: str
    packet: dict[str, Any] | None = None


def _hold(reason: str) -> AdapterDecision:
    return AdapterDecision("HOLD", reason, None)


def _parse_ts(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        text = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            return None
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _valid_asin(value: Any) -> bool:
    return isinstance(value, str) and bool(ASIN_RE.fullmatch(value))


def _validate_claim_time(claim: dict[str, Any], provider_checked: datetime) -> str | None:
    checked = _parse_ts(claim.get("checked_at"))
    if checked is None:
        return "MALFORMED_CLAIM_CHECKED_AT"
    if checked > provider_checked:
        return "CLAIM_NEWER_THAN_PROVIDER_SNAPSHOT"
    return None


def adapt(record: dict[str, Any]) -> AdapterDecision:
    if record.get("publication_authority") is not False or record.get("network_io") is not False:
        return _hold("ADAPTER_AUTHORITY_ESCALATION_DENIED")
    if record.get("provider_authority") != "PROVEN":
        return _hold("PROVIDER_AUTHORITY_UNPROVEN")
    if record.get("rights_to_use") != "PROVEN":
        return _hold("RIGHTS_TO_USE_UNPROVEN")
    if not isinstance(record.get("provider_id"), str) or not record["provider_id"].strip():
        return _hold("MISSING_PROVIDER_ID")
    if not isinstance(record.get("evidence_id"), str) or not record["evidence_id"].strip():
        return _hold("MISSING_EVIDENCE_ID")
    if not isinstance(record.get("marketplace"), str) or not record["marketplace"].strip():
        return _hold("MISSING_MARKETPLACE")
    if not _valid_asin(record.get("asin")):
        return _hold("INVALID_ASIN")
    if not isinstance(record.get("canonical_title"), str) or not record["canonical_title"].strip():
        return _hold("MISSING_TITLE")

    provider_checked = _parse_ts(record.get("checked_at"))
    if provider_checked is None:
        return _hold("MALFORMED_PROVIDER_CHECKED_AT")
    freshness = record.get("freshness_state")
    if freshness not in ALLOWED_FRESHNESS:
        return _hold("UNKNOWN_FRESHNESS_STATE")
    if freshness != "CURRENT":
        return _hold("PROVIDER_EVIDENCE_NOT_CURRENT")

    identity = record.get("identity")
    if not isinstance(identity, dict):
        return _hold("MISSING_IDENTITY")
    if identity.get("marketplace") != record.get("marketplace"):
        return _hold("MARKETPLACE_MISMATCH")
    if identity.get("asin") != record.get("asin"):
        return _hold("ASIN_MISMATCH")
    kind = identity.get("product_kind")
    if kind not in ALLOWED_KINDS:
        return _hold("UNKNOWN_PRODUCT_KIND")
    parent_asin = identity.get("parent_asin")
    variant_key = identity.get("variant_key")
    if parent_asin is not None and not _valid_asin(parent_asin):
        return _hold("INVALID_PARENT_ASIN")
    if kind == "VARIANT":
        if not parent_asin or not isinstance(variant_key, str) or not variant_key.strip():
            return _hold("VARIANT_IDENTITY_INCOMPLETE")
        if parent_asin == record.get("asin"):
            return _hold("VARIANT_PARENT_CONFLICT")
    elif kind == "PARENT":
        if parent_asin is not None or variant_key is not None:
            return _hold("PARENT_IDENTITY_CONFLICT")
    else:
        if parent_asin is not None or variant_key is not None:
            return _hold("PRODUCT_IDENTITY_CONFLICT")

    evidence_refs = [record["evidence_id"]]
    prime_state = "UNKNOWN"
    selection_state = "UNKNOWN"
    ranking_method_id = None
    ranking_position = None
    deal_state = "UNKNOWN"

    prime = record.get("prime")
    if prime is not None:
        if not isinstance(prime, dict) or prime.get("state") not in {"VERIFIED", "NOT_VERIFIED", "UNKNOWN"}:
            return _hold("MALFORMED_PRIME_CLAIM")
        prime_state = prime["state"]
        if prime_state != "UNKNOWN":
            if not isinstance(prime.get("evidence_id"), str) or not prime["evidence_id"].strip():
                return _hold("MISSING_PRIME_EVIDENCE_ID")
            reason = _validate_claim_time(prime, provider_checked)
            if reason:
                return _hold(reason)
            evidence_refs.append(prime["evidence_id"])

    selection = record.get("selection")
    if selection is not None:
        if not isinstance(selection, dict) or selection.get("state") not in {"VERIFIED", "UNKNOWN", "NOT_APPLICABLE"}:
            return _hold("MALFORMED_SELECTION_CLAIM")
        selection_state = selection["state"]
        if selection_state == "VERIFIED":
            ranking_method_id = selection.get("method_id")
            if not isinstance(ranking_method_id, str) or not ranking_method_id.strip():
                return _hold("MISSING_RANKING_METHOD_ID")
            position = selection.get("position")
            if position is not None and (not isinstance(position, int) or position <= 0):
                return _hold("INVALID_RANKING_POSITION")
            ranking_position = position
            if not isinstance(selection.get("evidence_id"), str) or not selection["evidence_id"].strip():
                return _hold("MISSING_SELECTION_EVIDENCE_ID")
            reason = _validate_claim_time(selection, provider_checked)
            if reason:
                return _hold(reason)
            evidence_refs.append(selection["evidence_id"])

    deal = record.get("deal")
    if deal is not None:
        if not isinstance(deal, dict) or deal.get("state") not in {"ACTIVE", "INACTIVE", "UNKNOWN", "STALE", "EXPIRED"}:
            return _hold("MALFORMED_DEAL_CLAIM")
        deal_state = deal["state"]
        if deal_state != "UNKNOWN":
            if not isinstance(deal.get("evidence_id"), str) or not deal["evidence_id"].strip():
                return _hold("MISSING_DEAL_EVIDENCE_ID")
            reason = _validate_claim_time(deal, provider_checked)
            if reason:
                return _hold(reason)
            evidence_refs.append(deal["evidence_id"])

    packet = {
        "product_identity": {
            "marketplace": record["marketplace"],
            "asin": record["asin"],
            "product_kind": kind,
            "parent_asin": parent_asin,
            "variant_key": variant_key,
        },
        "provider_id": record["provider_id"],
        "marketplace": record["marketplace"],
        "asin": record["asin"],
        "title": record["canonical_title"],
        "identity_state": "ASIN_VERIFIED",
        "prime_state": prime_state,
        "selection_state": selection_state,
        "ranking_method_id": ranking_method_id,
        "ranking_position": ranking_position,
        "deal_state": deal_state,
        "freshness_state": freshness,
        "checked_at": record["checked_at"],
        "evidence_refs": evidence_refs,
        "publication_authority": False,
        "network_io": False,
    }
    return AdapterDecision("EVIDENCE_ACCEPTABLE", "NORMALIZED_PROVIDER_EVIDENCE", packet)


def validate_fixture(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("research_only") is not True:
        raise AssertionError("research_only must be true")
    cases = data.get("cases") or []
    if not cases:
        raise AssertionError("fixture must contain cases")
    seen = set()
    for case in cases:
        cid = case.get("case_id")
        if not cid or cid in seen:
            raise AssertionError("case_id must be present and unique")
        seen.add(cid)
        result = adapt(case.get("record") or {})
        expected_d = case.get("expected_disposition")
        expected_r = case.get("expected_reason")
        if (result.disposition, result.reason) != (expected_d, expected_r):
            raise AssertionError(
                f"{cid}: {(result.disposition, result.reason)} != {(expected_d, expected_r)}"
            )
        if result.disposition == "EVIDENCE_ACCEPTABLE":
            if result.packet is None:
                raise AssertionError(f"{cid}: accepted evidence must have packet")
            if result.packet["publication_authority"] or result.packet["network_io"]:
                raise AssertionError(f"{cid}: adapter must never grant authority")
        elif result.packet is not None:
            raise AssertionError(f"{cid}: HOLD must not emit packet")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("provider-evidence.synthetic.json")
    validate_fixture(target)
    print(f"PASS: {target} provider adapter fixture is fail-closed")
