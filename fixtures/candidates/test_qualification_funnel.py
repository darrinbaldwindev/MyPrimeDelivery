#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from qualification_funnel import analyze_funnel

BASE = Path(__file__).parent
PATHS = [
    BASE / "first-100-research.json",
    BASE / "research-tranche-004.json",
    BASE / "research-tranche-005.json",
    BASE / "research-tranche-009.json",
]


class QualificationFunnelTests(unittest.TestCase):
    def test_current_research_pool_remains_unqualified(self):
        result = analyze_funnel(PATHS)
        self.assertEqual(result["evidence_rows"], 101)
        self.assertEqual(result["distinct_concepts"], 100)
        self.assertEqual(result["qualified_concepts"], 0)
        self.assertFalse(result["publication_authority"])
        self.assertFalse(result["network_io"])

    def test_historical_prime_event_does_not_pass_prime_gate(self):
        payload = {"candidates": [{
            "candidate_id": "cand-900",
            "title": "Historical Event Product",
            "asin": "B000TEST01",
            "prime_evidence_state": "UNKNOWN",
            "selection_evidence_state": "OFFICIAL_AMAZON_EVENT_HISTORICAL",
            "freshness_state": "RESEARCH_SNAPSHOT",
            "ranking_method_id": "historical-event",
            "ranking_evidence_source": "official-event-page",
            "source_rights_state": "VERIFIED",
            "outbound_destination_state": "VERIFIED"
        }]}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "historical.json"
            p.write_text(json.dumps(payload), encoding="utf-8")
            result = analyze_funnel([p])
        self.assertEqual(result["gate_pass_counts"]["prime"], 0)
        self.assertEqual(result["gate_pass_counts"]["freshness"], 0)
        self.assertEqual(result["qualified_concepts"], 0)

    def test_only_all_explicit_gates_can_reach_qualified_count(self):
        payload = {"candidates": [{
            "candidate_id": "cand-901",
            "title": "Synthetic Fully Evidenced Product",
            "asin": "B000TEST02",
            "prime_evidence_state": "CURRENT_VERIFIED",
            "freshness_state": "CURRENT",
            "ranking_method_id": "owner-approved-v1",
            "ranking_evidence_source": "authorised-provider",
            "source_rights_state": "PERMITTED",
            "outbound_destination_state": "VERIFIED"
        }]}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "qualified.json"
            p.write_text(json.dumps(payload), encoding="utf-8")
            result = analyze_funnel([p])
        self.assertEqual(result["identity_conflict_concepts"], 0)
        self.assertEqual(result["qualified_concepts"], 1)
        self.assertFalse(result["publication_authority"])
        self.assertFalse(result["network_io"])

    def test_separate_observations_cannot_combine_into_qualification(self):
        payload = {"candidates": [
            {
                "candidate_id": "cand-902",
                "title": "Synthetic Split Evidence Product",
                "asin": "B000TEST03",
                "prime_evidence_state": "CURRENT_VERIFIED",
                "freshness_state": "CURRENT",
                "ranking_method_id": "UNKNOWN",
                "ranking_evidence_source": "UNKNOWN",
                "source_rights_state": "UNKNOWN",
                "outbound_destination_state": "UNKNOWN"
            },
            {
                "candidate_id": "cand-903",
                "title": "Synthetic Split Evidence Product",
                "asin": "UNKNOWN",
                "prime_evidence_state": "UNKNOWN",
                "freshness_state": "RESEARCH_SNAPSHOT",
                "ranking_method_id": "owner-approved-v1",
                "ranking_evidence_source": "authorised-provider",
                "source_rights_state": "PERMITTED",
                "outbound_destination_state": "VERIFIED"
            }
        ]}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "split.json"
            p.write_text(json.dumps(payload), encoding="utf-8")
            result = analyze_funnel([p])
        self.assertEqual(result["qualified_concepts"], 0)
        self.assertFalse(result["publication_authority"])
        self.assertFalse(result["network_io"])

    def test_conflicting_known_asins_fail_closed_even_if_one_observation_is_complete(self):
        payload = {"candidates": [
            {
                "candidate_id": "cand-904",
                "title": "Synthetic Identity Conflict Product",
                "asin": "B000TEST04",
                "prime_evidence_state": "CURRENT_VERIFIED",
                "freshness_state": "CURRENT",
                "ranking_method_id": "owner-approved-v1",
                "ranking_evidence_source": "authorised-provider",
                "source_rights_state": "PERMITTED",
                "outbound_destination_state": "VERIFIED"
            },
            {
                "candidate_id": "cand-905",
                "title": "Synthetic Identity Conflict Product",
                "asin": "B000TEST05",
                "prime_evidence_state": "UNKNOWN",
                "freshness_state": "RESEARCH_SNAPSHOT",
                "ranking_method_id": "UNKNOWN",
                "ranking_evidence_source": "UNKNOWN",
                "source_rights_state": "UNKNOWN",
                "outbound_destination_state": "UNKNOWN"
            }
        ]}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "identity-conflict.json"
            p.write_text(json.dumps(payload), encoding="utf-8")
            result = analyze_funnel([p])
        self.assertEqual(result["identity_conflict_concepts"], 1)
        self.assertEqual(result["qualified_concepts"], 0)
        self.assertFalse(result["publication_authority"])
        self.assertFalse(result["network_io"])


if __name__ == "__main__":
    unittest.main()
