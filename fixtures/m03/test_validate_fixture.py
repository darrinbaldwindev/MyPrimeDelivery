#!/usr/bin/env python3
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("mpd_fixture_validator", HERE / "validate_fixture.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
BASE = json.loads((HERE / "prime-discovery.synthetic.json").read_text(encoding="utf-8"))


class FixtureValidationTests(unittest.TestCase):
    def validate_data(self, data):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "fixture.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            validator.validate(path)

    def assert_rejected(self, mutate):
        data = copy.deepcopy(BASE)
        mutate(data)
        with self.assertRaises(AssertionError):
            self.validate_data(data)

    def test_baseline_fixture_passes(self):
        self.validate_data(copy.deepcopy(BASE))

    def test_live_affiliate_url_is_rejected(self):
        def mutate(data):
            data["products"][0]["outbound_url"] = "https://www.amazon.com/example?tag=live-tag"
        self.assert_rejected(mutate)

    def test_commercial_field_leak_is_rejected(self):
        def mutate(data):
            data["products"][0]["price"] = "19.99"
        self.assert_rejected(mutate)

    def test_ranking_without_evidence_is_rejected(self):
        def mutate(data):
            data["products"][0]["ranking_evidence_source"] = ""
        self.assert_rejected(mutate)

    def test_invalid_category_reference_is_rejected(self):
        def mutate(data):
            data["products"][1]["category_id"] = "OTHER-CATEGORY"
        self.assert_rejected(mutate)

    def test_verified_prime_without_verified_evidence_is_rejected(self):
        def mutate(data):
            data["products"][2]["prime_state"] = "VERIFIED"
        self.assert_rejected(mutate)

    def test_non_fixture_marketplace_is_rejected(self):
        def mutate(data):
            data["products"][0]["marketplace"] = "AU"
        self.assert_rejected(mutate)

    def test_duplicate_asin_is_rejected(self):
        def mutate(data):
            data["products"][1]["asin"] = data["products"][0]["asin"]
        self.assert_rejected(mutate)

    def test_wrong_ranking_positions_are_rejected(self):
        def mutate(data):
            data["products"][2]["ranking_position"] = 2
        self.assert_rejected(mutate)


if __name__ == "__main__":
    unittest.main()
