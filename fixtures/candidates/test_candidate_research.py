#!/usr/bin/env python3
import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate_candidate_research import validate

FIXTURE = Path(__file__).with_name("first-100-research.json")


class CandidateResearchValidationTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def assert_invalid(self, data):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "candidate.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                validate(path)

    def test_canonical_fixture_passes(self):
        counts = validate(FIXTURE)
        self.assertEqual(sum(counts.values()), 30)

    def test_duplicate_candidate_id_fails(self):
        d = self.load()
        d["candidates"][1]["candidate_id"] = d["candidates"][0]["candidate_id"]
        self.assert_invalid(d)

    def test_unsupported_category_fails(self):
        d = self.load()
        d["candidates"][0]["category_id"] = "cat-made-up"
        self.assert_invalid(d)

    def test_missing_provenance_fails(self):
        d = self.load()
        d["candidates"][0]["source_url"] = ""
        self.assert_invalid(d)

    def test_affiliate_tag_leak_fails(self):
        d = self.load()
        d["candidates"][0]["source_url"] = "https://example.com/item?tag=bad-22"
        d["candidates"][0]["source_domain"] = "example.com"
        self.assert_invalid(d)

    def test_fake_qualified_without_prime_evidence_fails(self):
        d = self.load()
        d["candidates"][0]["state"] = "QUALIFIED"
        self.assert_invalid(d)

    def test_prime_verified_without_authoritative_source_fails(self):
        d = self.load()
        d["candidates"][0]["prime_evidence_state"] = "VERIFIED"
        self.assert_invalid(d)

    def test_stale_candidate_fails_closed(self):
        d = self.load()
        d["candidates"][0]["freshness_state"] = "STALE"
        self.assert_invalid(d)


if __name__ == "__main__":
    unittest.main()
