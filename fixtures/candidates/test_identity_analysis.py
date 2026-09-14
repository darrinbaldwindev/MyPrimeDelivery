#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from analyze_candidate_collection import analyze, normalize_title

BASE = Path(__file__).parent
PATHS = [BASE / "first-100-research.json", BASE / "research-tranche-004.json", BASE / "research-tranche-005.json"]


class IdentityAnalysisTests(unittest.TestCase):
    def test_normalizer_is_stable(self):
        self.assertEqual(normalize_title("Ninja Woodfire™ Outdoor Oven"), "ninja woodfire outdoor oven")

    def test_current_collection_detects_known_duplicate(self):
        result = analyze(PATHS)
        self.assertEqual(result["evidence_rows"], 58)
        self.assertEqual(result["unique_normalized_titles"], 57)
        self.assertEqual(result["duplicate_row_count"], 1)
        groups = {g["normalized_title"]: g for g in result["duplicate_groups"]}
        self.assertIn("ninja woodfire outdoor oven", groups)
        self.assertEqual(groups["ninja woodfire outdoor oven"]["candidate_ids"], ["cand-030", "cand-058"])

    def test_duplicate_candidate_id_fails(self):
        payload = json.loads(PATHS[1].read_text(encoding="utf-8"))
        payload["candidates"][1]["candidate_id"] = payload["candidates"][0]["candidate_id"]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "dup.json"
            p.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(AssertionError):
                analyze([p])

    def test_same_normalized_title_different_category_fails(self):
        a = {"candidates":[{"candidate_id":"cand-900","title":"Same Product","category_id":"cat-electronics"}]}
        b = {"candidates":[{"candidate_id":"cand-901","title":"Same Product","category_id":"cat-home-kitchen"}]}
        with tempfile.TemporaryDirectory() as td:
            p1 = Path(td) / "a.json"; p2 = Path(td) / "b.json"
            p1.write_text(json.dumps(a), encoding="utf-8"); p2.write_text(json.dumps(b), encoding="utf-8")
            with self.assertRaises(AssertionError):
                analyze([p1, p2])


if __name__ == "__main__":
    unittest.main()
