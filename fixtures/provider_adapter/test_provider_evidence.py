import copy
import json
import unittest
from pathlib import Path

from validate_provider_evidence import adapt, validate_fixture

FIXTURE = Path(__file__).with_name("provider-evidence.synthetic.json")


class ProviderEvidenceAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.accepted = copy.deepcopy(cls.data["cases"][0]["record"])

    def test_fixture_passes(self):
        validate_fixture(FIXTURE)

    def test_accepted_packet_is_non_authoritative(self):
        result = adapt(copy.deepcopy(self.accepted))
        self.assertEqual(result.disposition, "EVIDENCE_ACCEPTABLE")
        self.assertFalse(result.packet["publication_authority"])
        self.assertFalse(result.packet["network_io"])
        self.assertEqual(result.packet["identity_state"], "ASIN_VERIFIED")

    def test_asin_mismatch_fails_closed(self):
        record = copy.deepcopy(self.accepted)
        record["identity"]["asin"] = "B0SYN99999"
        result = adapt(record)
        self.assertEqual(result.reason, "ASIN_MISMATCH")
        self.assertIsNone(result.packet)

    def test_marketplace_mismatch_fails_closed(self):
        record = copy.deepcopy(self.accepted)
        record["identity"]["marketplace"] = "US"
        self.assertEqual(adapt(record).reason, "MARKETPLACE_MISMATCH")

    def test_stale_provider_fails_closed_even_with_strong_claims(self):
        record = copy.deepcopy(self.accepted)
        record["freshness_state"] = "STALE"
        self.assertEqual(adapt(record).reason, "PROVIDER_EVIDENCE_NOT_CURRENT")

    def test_variant_requires_parent_and_variant_key(self):
        record = copy.deepcopy(self.accepted)
        record["identity"] = {
            "marketplace": "AU",
            "asin": "B0SYN00001",
            "product_kind": "VARIANT",
            "parent_asin": None,
            "variant_key": "SIZE-L",
        }
        self.assertEqual(adapt(record).reason, "VARIANT_IDENTITY_INCOMPLETE")

    def test_variant_parent_cannot_equal_variant_asin(self):
        record = copy.deepcopy(self.accepted)
        record["identity"] = {
            "marketplace": "AU",
            "asin": "B0SYN00001",
            "product_kind": "VARIANT",
            "parent_asin": "B0SYN00001",
            "variant_key": "SIZE-L",
        }
        self.assertEqual(adapt(record).reason, "VARIANT_PARENT_CONFLICT")

    def test_unproven_rights_fail_closed(self):
        record = copy.deepcopy(self.accepted)
        record["rights_to_use"] = "UNKNOWN"
        self.assertEqual(adapt(record).reason, "RIGHTS_TO_USE_UNPROVEN")

    def test_unproven_provider_authority_fails_closed(self):
        record = copy.deepcopy(self.accepted)
        record["provider_authority"] = "UNKNOWN"
        self.assertEqual(adapt(record).reason, "PROVIDER_AUTHORITY_UNPROVEN")

    def test_adapter_cannot_be_given_publication_authority(self):
        record = copy.deepcopy(self.accepted)
        record["publication_authority"] = True
        self.assertEqual(adapt(record).reason, "ADAPTER_AUTHORITY_ESCALATION_DENIED")

    def test_claim_newer_than_snapshot_fails(self):
        record = copy.deepcopy(self.accepted)
        record["prime"]["checked_at"] = "2026-09-14T13:01:00Z"
        self.assertEqual(adapt(record).reason, "CLAIM_NEWER_THAN_PROVIDER_SNAPSHOT")

    def test_prime_does_not_follow_deal_state(self):
        record = copy.deepcopy(self.accepted)
        record["prime"] = {"state": "UNKNOWN"}
        record["deal"]["state"] = "ACTIVE"
        result = adapt(record)
        self.assertEqual(result.disposition, "EVIDENCE_ACCEPTABLE")
        self.assertEqual(result.packet["prime_state"], "UNKNOWN")
        self.assertEqual(result.packet["deal_state"], "ACTIVE")

    def test_selection_requires_method_when_verified(self):
        record = copy.deepcopy(self.accepted)
        record["selection"]["method_id"] = ""
        self.assertEqual(adapt(record).reason, "MISSING_RANKING_METHOD_ID")

    def test_invalid_asin_is_rejected(self):
        record = copy.deepcopy(self.accepted)
        record["asin"] = "NOT-ASIN"
        record["identity"]["asin"] = "NOT-ASIN"
        self.assertEqual(adapt(record).reason, "INVALID_ASIN")


if __name__ == "__main__":
    unittest.main()
