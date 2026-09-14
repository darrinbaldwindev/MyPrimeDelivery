#!/usr/bin/env python3
import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate_provisional_ranking import validate

FIXTURE = Path(__file__).with_name("provisional-ranking.synthetic.json")


class ProvisionalRankingTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def write_temp(self, data):
        td = tempfile.TemporaryDirectory()
        path = Path(td.name) / "ranking.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return td, path

    def test_fixture_passes(self):
        self.assertEqual(validate(FIXTURE), ["prod-b", "prod-a", "prod-e"])

    def test_unknown_prime_cannot_be_marked_eligible(self):
        data = self.load()
        data["products"][2]["eligible"] = True
        td, path = self.write_temp(data)
        try:
            with self.assertRaises(AssertionError):
                validate(path)
        finally:
            td.cleanup()

    def test_stale_product_cannot_be_marked_eligible(self):
        data = self.load()
        data["products"][3]["eligible"] = True
        td, path = self.write_temp(data)
        try:
            with self.assertRaises(AssertionError):
                validate(path)
        finally:
            td.cleanup()

    def test_score_over_max_fails(self):
        data = self.load()
        data["products"][0]["deal_relevance"] = 11
        td, path = self.write_temp(data)
        try:
            with self.assertRaises(AssertionError):
                validate(path)
        finally:
            td.cleanup()

    def test_tie_break_is_stable_product_id(self):
        data = self.load()
        self.assertEqual(data["products"][0]["selection_strength"], data["products"][4]["selection_strength"])
        self.assertEqual(data["products"][0]["evidence_confidence"], data["products"][4]["evidence_confidence"])
        self.assertEqual(data["products"][0]["freshness_strength"], data["products"][4]["freshness_strength"])
        self.assertEqual(validate(FIXTURE)[1:], ["prod-a", "prod-e"])


if __name__ == "__main__":
    unittest.main()
