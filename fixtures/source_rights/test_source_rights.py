import unittest

from validate_source_rights import validate_source_rights


OFFICIAL = {
    "source_class": "OFFICIAL_PROVIDER",
    "claim_type": "PRIME_ELIGIBILITY",
    "rights_to_use": "PROVEN",
    "provider_authority": "PROVEN",
    "evidence_id": "SYNTHETIC-EVIDENCE-001",
}


class SourceRightsTests(unittest.TestCase):
    def test_official_provider_can_supply_advisory_evidence_only(self):
        result = validate_source_rights(OFFICIAL)
        self.assertEqual(result.disposition, "EVIDENCE_ACCEPTABLE")
        self.assertFalse(result.publication_authority)
        self.assertFalse(result.network_io)

    def test_public_discovery_cannot_prove_prime(self):
        case = {**OFFICIAL, "source_class": "PUBLIC_DISCOVERY"}
        self.assertEqual(validate_source_rights(case).reason, "SOURCE_NOT_AUTHORITATIVE_FOR_CLAIM")

    def test_editorial_source_cannot_prove_rank(self):
        case = {**OFFICIAL, "source_class": "EDITORIAL", "claim_type": "RANK"}
        self.assertEqual(validate_source_rights(case).disposition, "HOLD")

    def test_unknown_reuse_rights_fail_closed(self):
        case = {**OFFICIAL, "rights_to_use": "UNKNOWN"}
        self.assertEqual(validate_source_rights(case).reason, "RIGHTS_TO_USE_UNPROVEN")

    def test_provider_authority_must_be_proven(self):
        case = {**OFFICIAL, "provider_authority": "UNKNOWN"}
        self.assertEqual(validate_source_rights(case).reason, "PROVIDER_AUTHORITY_UNPROVEN")

    def test_missing_evidence_identity_fails_closed(self):
        case = {**OFFICIAL, "evidence_id": ""}
        self.assertEqual(validate_source_rights(case).reason, "MISSING_EVIDENCE_ID")

    def test_discovery_only_stays_research_only(self):
        case = {
            "source_class": "PUBLIC_DISCOVERY",
            "claim_type": "DISCOVERY_ONLY",
            "rights_to_use": "PROVEN",
            "provider_authority": "UNKNOWN",
            "evidence_id": "PUBLIC-001",
        }
        result = validate_source_rights(case)
        self.assertEqual(result.disposition, "RESEARCH_ONLY")
        self.assertFalse(result.publication_authority)


if __name__ == "__main__":
    unittest.main()
