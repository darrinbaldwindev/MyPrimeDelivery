#!/usr/bin/env python3
import copy
import json
import unittest
from pathlib import Path

from fixtures.m03.render_fixture import project_render_model

HERE = Path(__file__).resolve().parent
BASE = json.loads((HERE / "prime-discovery.synthetic.json").read_text(encoding="utf-8"))


class RenderFixtureTests(unittest.TestCase):
    def test_fixture_renders_three_products_without_positive_prime_claims(self):
        model = project_render_model(copy.deepcopy(BASE))
        self.assertEqual(len(model["products"]), 3)
        self.assertTrue(model["fixture_disclosure"])
        self.assertTrue(all(p["fixture_disclosure"] for p in model["products"]))
        self.assertTrue(all(not p["show_prime_positive_claim"] for p in model["products"]))
        self.assertTrue(all(not p["show_outbound_cta"] for p in model["products"]))
        self.assertTrue(all(not p["show_local_checkout"] for p in model["products"]))
        self.assertTrue(all(p["commercial_fields"] == {} for p in model["products"]))

    def test_disabled_destination_never_renders_cta(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["outbound_destination_state"] = "DISABLED"
        data["products"][0]["outbound_url"] = None
        model = project_render_model(data)
        self.assertFalse(model["products"][0]["show_outbound_cta"])

    def test_stale_product_suppresses_positive_prime_claim_and_ranking(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["prime_state"] = "VERIFIED"
        data["products"][0]["evidence_status"] = "VERIFIED"
        data["products"][0]["freshness_state"] = "STALE"
        model = project_render_model(data)
        first = model["products"][0]
        self.assertEqual(first["evidence_badge"], "STALE")
        self.assertFalse(first["show_prime_positive_claim"])
        self.assertFalse(first["show_ranking"])

    def test_category_stale_or_unknown_suppresses_positive_ranking(self):
        for state in ("STALE", "UNKNOWN", "BLOCKED"):
            data = copy.deepcopy(BASE)
            data["category"]["freshness_state"] = state
            model = project_render_model(data)
            self.assertTrue(all(not p["show_ranking"] for p in model["products"]))

    def test_category_evidence_status_contradiction_suppresses_ranking(self):
        data = copy.deepcopy(BASE)
        data["category"]["freshness_state"] = "CURRENT"
        data["category"]["evidence_status"] = "UNKNOWN"
        model = project_render_model(data)
        self.assertTrue(all(not p["show_ranking"] for p in model["products"]))

    def test_missing_ranking_evidence_suppresses_ranking(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["ranking_evidence_source"] = ""
        model = project_render_model(data)
        self.assertFalse(model["products"][0]["show_ranking"])

    def test_invalid_ranking_position_fails_closed_before_render(self):
        for bad in (None, 0, -1, "1"):
            data = copy.deepcopy(BASE)
            data["products"][0]["ranking_position"] = bad
            with self.assertRaises(ValueError):
                project_render_model(data)

    def test_duplicate_ranking_positions_fail_closed(self):
        data = copy.deepcopy(BASE)
        data["products"][1]["ranking_position"] = data["products"][0]["ranking_position"]
        with self.assertRaisesRegex(ValueError, "duplicate ranking_position"):
            project_render_model(data)

    def test_verified_destination_without_url_suppresses_cta(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["outbound_destination_state"] = "VERIFIED"
        data["products"][0]["evidence_status"] = "VERIFIED"
        data["products"][0]["outbound_url"] = None
        model = project_render_model(data)
        self.assertFalse(model["products"][0]["show_outbound_cta"])

    def test_verified_destination_requires_verified_evidence_status(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["outbound_destination_state"] = "VERIFIED"
        data["products"][0]["outbound_url"] = "https://example.invalid/fixture-only"
        data["products"][0]["freshness_state"] = "CURRENT"
        data["products"][0]["evidence_status"] = "FIXTURE"
        model = project_render_model(data)
        self.assertFalse(model["products"][0]["show_outbound_cta"])

    def test_stale_or_blocked_verified_destination_suppresses_cta(self):
        for state in ("STALE", "BLOCKED"):
            data = copy.deepcopy(BASE)
            data["products"][0]["outbound_destination_state"] = "VERIFIED"
            data["products"][0]["evidence_status"] = "VERIFIED"
            data["products"][0]["outbound_url"] = "https://example.invalid/fixture-only"
            data["products"][0]["freshness_state"] = state
            model = project_render_model(data)
            self.assertFalse(model["products"][0]["show_outbound_cta"])

    def test_fixture_disclosure_is_mandatory(self):
        for bad in (False, None):
            data = copy.deepcopy(BASE)
            data["fixture_only"] = bad
            with self.assertRaisesRegex(ValueError, "fixture_only=true"):
                project_render_model(data)

    def test_optional_commercial_input_is_not_projected(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["price"] = "999.99"
        data["products"][0]["stock"] = 999
        data["products"][0]["affiliate_tag"] = "fixture-only-tag"
        model = project_render_model(data)
        first = model["products"][0]
        self.assertEqual(first["commercial_fields"], {})
        self.assertNotIn("price", first)
        self.assertNotIn("stock", first)
        self.assertNotIn("affiliate_tag", first)

    def test_evidence_badge_maps_freshness_state_verbatim(self):
        data = copy.deepcopy(BASE)
        expected = ["CURRENT", "STALE", "UNKNOWN"]
        for product, state in zip(data["products"], expected):
            product["freshness_state"] = state
        model = project_render_model(data)
        badges = [product["evidence_badge"] for product in model["products"]]
        self.assertEqual(badges, expected)


if __name__ == "__main__":
    unittest.main()
