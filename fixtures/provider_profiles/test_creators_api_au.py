import copy
import json
import unittest
from pathlib import Path

from validate_creators_api_au import validate

FIXTURE = Path(__file__).with_name("creators_api_au.synthetic.json")


class CreatorsApiAuProfileTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_fixture_passes(self):
        accepted = validate(self.load())
        self.assertEqual(len(accepted), 2)
        self.assertEqual(accepted[-1]["provider_version"], 2)

    def test_prime_policy_cannot_be_promoted(self):
        d = self.load()
        d["field_policies"]["prime"] = "ALLOWED_CURRENT"
        with self.assertRaises(AssertionError):
            validate(d)

    def test_marketplace_header_mismatch_fails(self):
        d = self.load()
        case = copy.deepcopy(d["snapshots"][0])
        case["snapshot_id"] = "snap-extra"
        case["x_marketplace"] = "www.amazon.com"
        case["expected_disposition"] = "MARKETPLACE_MISMATCH"
        d["snapshots"] = [case]
        with self.assertRaises(AssertionError):
            validate(d)

    def test_replay_content_change_fails(self):
        d = self.load()
        replay = d["snapshots"][1]
        replay["title"] = "Mutated replay"
        replay["expected_disposition"] = "REPLAY_MISMATCH"
        accepted = validate(d)
        self.assertEqual(len(accepted), 2)

    def test_wordpress_projection_stays_nonpublishing(self):
        accepted = validate(self.load())
        card = accepted[0]["wordpress_projection"]
        self.assertFalse(card["publication_authority"])
        self.assertFalse(card["outbound_enabled"])
        self.assertFalse(card["network_io"])
        self.assertEqual(card["prime_state"], "UNKNOWN")
        self.assertIsNone(card["image_url"])


if __name__ == "__main__":
    unittest.main()
