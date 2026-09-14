#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

from analyze_candidate_collection import normalize_title

QUALIFICATION_GATES = (
    "identity",
    "prime",
    "freshness",
    "ranking",
    "rights",
    "outbound_destination",
)


def _known(value):
    return value not in (None, "", "UNKNOWN", "UNVERIFIED", "RESEARCH_SNAPSHOT")


def analyze_funnel(paths: list[Path]) -> dict:
    rows = []
    seen_ids = set()
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("candidates", []):
            cid = record.get("candidate_id")
            if not cid or cid in seen_ids:
                raise AssertionError(f"duplicate or missing candidate_id: {cid}")
            seen_ids.add(cid)
            rows.append(record)

    by_title = {}
    for row in rows:
        key = normalize_title(row.get("title") or "")
        if not key:
            raise AssertionError(f"{row.get('candidate_id')}: empty normalized title")
        by_title.setdefault(key, []).append(row)

    gate_counts = Counter()
    blocked_by = Counter()
    qualified = []
    for key, observations in by_title.items():
        # Research observations may accumulate, but a gate is satisfied only by
        # explicit evidence on at least one observation. Unknowns never promote.
        gates = {
            "identity": any(_known(r.get("asin")) for r in observations),
            "prime": any(r.get("prime_evidence_state") in {"VERIFIED", "CURRENT_VERIFIED"} for r in observations),
            "freshness": any(r.get("freshness_state") in {"CURRENT", "FRESH", "VERIFIED_CURRENT"} for r in observations),
            "ranking": any(_known(r.get("ranking_method_id")) and _known(r.get("ranking_evidence_source")) for r in observations),
            "rights": any(r.get("source_rights_state") in {"VERIFIED", "PERMITTED"} for r in observations),
            "outbound_destination": any(r.get("outbound_destination_state") == "VERIFIED" for r in observations),
        }
        for gate, passed in gates.items():
            if passed:
                gate_counts[gate] += 1
            else:
                blocked_by[gate] += 1
        if all(gates.values()):
            qualified.append(key)

    return {
        "evidence_rows": len(rows),
        "distinct_concepts": len(by_title),
        "gate_pass_counts": {gate: gate_counts[gate] for gate in QUALIFICATION_GATES},
        "gate_blocked_counts": {gate: blocked_by[gate] for gate in QUALIFICATION_GATES},
        "qualified_concepts": len(qualified),
        "qualification_note": "Research breadth is not qualification. UNKNOWN or historical/editorial evidence fails closed and cannot establish Prime/rank/rights/publication authority.",
        "publication_authority": False,
        "network_io": False,
    }


if __name__ == "__main__":
    targets = [Path(arg) for arg in sys.argv[1:]]
    if not targets:
        base = Path(__file__).parent
        targets = [
            base / "first-100-research.json",
            base / "research-tranche-004.json",
            base / "research-tranche-005.json",
            base / "research-tranche-009.json",
        ]
    print(json.dumps(analyze_funnel(targets), indent=2, sort_keys=True))
