"""Smoke test for the keyless DDG floor.

Runs a known query and asserts the schema + shape. Marked as smoke (skips on
network-empty rather than failing) so a flaky DDG doesn't break the install.

Usage:
    python scripts/test_keyless_search.py            # smoke (default)
    python -m unittest scripts/test_keyless_search.py  # explicit unittest
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from lib.web_search_keyless import keyless_search  # noqa: E402

REQUIRED_KEYS = {
    "id",
    "title",
    "url",
    "source_domain",
    "snippet",
    "relevance",
    "why_relevant",
}


class KeylessSearchTests(unittest.TestCase):
    def test_ddg_returns_at_least_one_result_for_known_query(self):
        items, artifact = keyless_search(
            "Mamaearth India official site", count=3
        )
        self.assertIsInstance(items, list)
        self.assertIsInstance(artifact, dict)
        if not items:
            self.skipTest(
                f"DDG returned 0 results (network may be throttled): {artifact}"
            )
        self.assertGreaterEqual(len(items), 1)
        for required_key in REQUIRED_KEYS:
            self.assertIn(required_key, items[0])
        # schema-level checks
        self.assertTrue(items[0]["url"].startswith("http"))
        self.assertIsInstance(items[0]["relevance"], float)
        self.assertEqual(artifact.get("label"), "keyless")

    def test_artifact_carries_backend_label(self):
        _items, artifact = keyless_search("Mamaearth India", count=1)
        self.assertIn(artifact.get("keyless_backend"), {"ddg", "searxng"})

    def test_ddg_handles_total_failure_gracefully(self):
        # We can't reliably force DDG to return zero without a mock, but we
        # can confirm the call is non-raising for arbitrary input.
        items, artifact = keyless_search("nothing meaningful here", count=2)
        self.assertIsInstance(items, list)
        # result_count matches len(items); reason present iff empty.
        if items:
            self.assertEqual(artifact["result_count"], len(items))
        else:
            self.assertEqual(artifact.get("reason"), "keyless-search-unavailable")


if __name__ == "__main__":
    unittest.main()
