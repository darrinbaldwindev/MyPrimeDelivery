from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

AUTHORITATIVE_CLAIMS = frozenset({"PRIME_ELIGIBILITY", "RANK", "DEAL"})
OFFICIAL_SOURCE_CLASS = "OFFICIAL_PROVIDER"


@dataclass(frozen=True)
class SourceDecision:
    disposition: str
    reason: str
    publication_authority: bool = False
    network_io: bool = False


def validate_source_rights(record: Mapping[str, Any]) -> SourceDecision:
    """Fail-closed source/right-to-use gate for research fixtures only."""
    source_class = record.get("source_class")
    claim = record.get("claim_type")

    if source_class not in {"OFFICIAL_PROVIDER", "PUBLIC_DISCOVERY", "EDITORIAL", "UNKNOWN"}:
        return SourceDecision("HOLD", "UNKNOWN_SOURCE_CLASS")
    if claim not in AUTHORITATIVE_CLAIMS | {"DISCOVERY_ONLY"}:
        return SourceDecision("HOLD", "UNKNOWN_CLAIM_TYPE")

    if record.get("rights_to_use") != "PROVEN":
        return SourceDecision("HOLD", "RIGHTS_TO_USE_UNPROVEN")

    if claim in AUTHORITATIVE_CLAIMS:
        if source_class != OFFICIAL_SOURCE_CLASS:
            return SourceDecision("HOLD", "SOURCE_NOT_AUTHORITATIVE_FOR_CLAIM")
        if record.get("provider_authority") != "PROVEN":
            return SourceDecision("HOLD", "PROVIDER_AUTHORITY_UNPROVEN")
        if not isinstance(record.get("evidence_id"), str) or not record["evidence_id"].strip():
            return SourceDecision("HOLD", "MISSING_EVIDENCE_ID")
        return SourceDecision("EVIDENCE_ACCEPTABLE", "OFFICIAL_PROVIDER_EVIDENCE")

    # Discovery-only evidence can be retained for research, but it never proves
    # Prime eligibility, Amazon rank, or a time-sensitive deal.
    return SourceDecision("RESEARCH_ONLY", "DISCOVERY_SOURCE_ONLY")
