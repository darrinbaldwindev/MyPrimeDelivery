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
        self.assertTrue(all(not p["show_prime_positive_claim"] for p in model["products"]))
        self.assertTrue(all(not p["show_outbound_cta"] for p in model["products"]))
        self.assertTrue(all(not p["show_local_checkout"] for p in model["products"]))
        self.assertTrue(all(p["commercial_fields"] == {} for p in model["products"]))

    def test_disabled_destination_never_renders_cta(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["outbound_destination_state"] = "DISABLED"
        data["products"][0]["outbound_url"] = None
        model = project_render_model(data)
        first = model["products"][0]
        self.assertFalse(first["show_outbound_cta"])

    def test_stale_product_suppresses_positive_prime_claim(self):
        data = copy.deepcopy(BASE)
        data["products"][0]["prime_state"] = "STALE"
        data["products"][0]["evidence_status"] = "STALE"
        data["products"][0]["freshness_state"] = "STALE"
        model = project_render_model(data)
        first = model["products"][0]
        self.assertEqual(first["evidence_badge"], "STALE")
        self.assertFalse(first["show_prime_positive_claim"])


if __name__ == "__main__":
    unittest.main()
