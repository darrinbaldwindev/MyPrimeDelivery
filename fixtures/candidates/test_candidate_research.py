#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from validate_candidate_research import validate, validate_collection

FIXTURE = Path(__file__).with_name("first-100-research.json")
TRANCHE = Path(__file__).with_name("research-tranche-004.json")


class CandidateResearchValidationTests(unittest.TestCase):
    def load(self, path=FIXTURE):
        return json.loads(path.read_text(encoding="utf-8"))

    def write_temp(self, data, directory, name="candidate.json"):
        path = Path(directory) / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def assert_invalid(self, data):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_temp(data, td)
            with self.assertRaises(AssertionError):
                validate(path)

    def test_canonical_fixture_passes(self):
        counts = validate(FIXTURE)
        self.assertEqual(sum(counts.values()), 30)

    def test_canonical_collection_covers_all_launch_categories(self):
        counts = validate_collection([FIXTURE, TRANCHE])
        self.assertEqual(sum(counts.values()), 40)
        self.assertEqual(len(counts), 12)

    def test_cross_tranche_duplicate_candidate_id_fails(self):
        first = self.load()
        second = self.load(TRANCHE)
        second["candidates"][0]["candidate_id"] = first["candidates"][0]["candidate_id"]
        with tempfile.TemporaryDirectory() as td:
            p1 = self.write_temp(first, td, "a.json")
            p2 = self.write_temp(second, td, "b.json")
            with self.assertRaises(AssertionError):
                validate_collection([p1, p2])

    def test_non_deterministic_cross_tranche_order_fails(self):
        second = self.load(TRANCHE)
        second["candidates"][0], second["candidates"][1] = second["candidates"][1], second["candidates"][0]
        with tempfile.TemporaryDirectory() as td:
            p2 = self.write_temp(second, td, "b.json")
            with self.assertRaises(AssertionError):
                validate_collection([FIXTURE, p2])

    def test_missing_cumulative_category_fails(self):
        first = self.load()
        second = self.load(TRANCHE)
        for dataset in (first, second):
            dataset["candidates"] = [r for r in dataset["candidates"] if r["category_id"] != "cat-automotive"]
        with tempfile.TemporaryDirectory() as td:
            p1 = self.write_temp(first, td, "a.json")
            p2 = self.write_temp(second, td, "b.json")
            with self.assertRaises(AssertionError):
                validate_collection([p1, p2])

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
