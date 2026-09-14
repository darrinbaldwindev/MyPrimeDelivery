import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate_deal_fixture import validate
from render_deal_fixture import render

FIXTURE = Path(__file__).with_name("deal-evidence.synthetic.json")


class DealFixtureTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def validate_mutation(self, mutate):
        data = self.load()
        mutate(data)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            validate(path)

    def assert_rejected(self, mutate):
        with self.assertRaises(AssertionError):
            self.validate_mutation(mutate)

    def test_canonical_fixture_passes(self):
        validate(FIXTURE)

    def test_active_without_source_is_rejected(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"evidence_source": None}))

    def test_active_without_checked_at_is_rejected(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"checked_at": None}))

    def test_future_checked_at_is_rejected(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"checked_at": "2026-09-15T00:00:00Z"}))

    def test_expired_offer_cannot_remain_active(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"expires_at": "2026-09-13T23:59:00Z"}))

    def test_stale_offer_cannot_remain_active(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"checked_at": "2026-09-13T20:00:00Z"}))

    def test_discount_without_reference_price_is_rejected(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"reference_price": None}))

    def test_reference_price_must_exceed_current_price(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"reference_price": 70.0}))

    def test_duplicate_offer_identity_is_rejected(self):
        self.assert_rejected(lambda d: d["offers"][1].update({"offer_id": d["offers"][0]["offer_id"]}))

    def test_live_amazon_destination_is_rejected(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"outbound_url": "https://www.amazon.example/item?tag=fixture"}))

    def test_deal_state_does_not_promote_prime_state(self):
        self.assert_rejected(lambda d: d["offers"][0].update({"prime_state": "VERIFIED"}))

    def test_renderer_only_exposes_urgency_for_active_evidence(self):
        projection = render(FIXTURE)
        by_state = {item["deal_state"]: item for item in projection["offers"]}
        self.assertEqual(by_state["ACTIVE"]["sale_badge"], "SALE")
        self.assertEqual(by_state["ACTIVE"]["discount_percent"], 20.0)
        self.assertTrue(by_state["ACTIVE"]["urgency_visible"])
        for state in ("STALE", "EXPIRED", "UNKNOWN", "BLOCKED"):
            self.assertIsNone(by_state[state]["sale_badge"])
            self.assertIsNone(by_state[state]["discount_percent"])
            self.assertFalse(by_state[state]["urgency_visible"])
            self.assertEqual(by_state[state]["prime_state"], "UNKNOWN")
            self.assertFalse(by_state[state]["outbound_enabled"])


if __name__ == "__main__":
    unittest.main()
