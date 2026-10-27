import json
import shutil
import unittest
import uuid
from pathlib import Path

from record_reel_metrics import latest_snapshots, read_csv, record_publication, record_snapshot


class ReelMetricsTest(unittest.TestCase):
    def setUp(self):
        # Python's Windows mode-0700 temporary directories are inaccessible to
        # this workspace sandbox; ordinary inherited permissions work normally.
        self.test_parent = Path(__file__).resolve().parent
        self.root = self.test_parent / ("_test_reel_metrics_" + uuid.uuid4().hex)
        self.root.mkdir()
        self.publication = dict(post_url="https://www.instagram.com/reel/TEST_123/?igsh=tracking", source="manual", observed_at="2026-09-15")
        record_publication(self.root, self.publication)
        self.observation = dict(post_id="TEST_123", checkpoint="lifetime_snapshot", observed_at="2026-09-15", source="instagram_web_insights", scope="instagram")

    def tearDown(self):
        self.assertEqual(self.root.resolve().parent, self.test_parent)
        self.assertTrue(self.root.name.startswith("_test_reel_metrics_"))
        shutil.rmtree(self.root)

    def rows(self):
        return read_csv(self.root / "07_metrics/reel_metric_snapshots.csv")

    def test_missing_is_distinct_from_confirmed_zero(self):
        row = record_snapshot(self.root, dict(self.observation, views=5, reach=4, saves=0))
        self.assertEqual(row["saves"], "0")
        self.assertEqual(row["saves_per_reach"], "0.00000000")
        for field in ("shares", "shares_per_reach", "average_watch_seconds", "skip_rate_percent"):
            self.assertEqual(row[field], "")

    def test_duplicate_is_idempotent_and_correction_preserves_history(self):
        first = record_snapshot(self.root, dict(self.observation, views=5, reach=4))
        self.assertEqual(first, record_snapshot(self.root, dict(self.observation, views=5, reach=4)))
        self.assertEqual(len(self.rows()), 1)
        corrected = record_snapshot(self.root, dict(self.observation, views=6, shares=1))
        self.assertEqual(corrected["revision"], "2")
        self.assertEqual(corrected["reach"], "4")
        self.assertEqual(corrected["shares_per_reach"], "0.25000000")
        self.assertEqual([row["views"] for row in self.rows()], ["5", "6"])
        self.assertEqual(latest_snapshots(self.rows()), [corrected])
        next_day = dict(self.observation, observed_at="2026-09-16", views=8)
        record_snapshot(self.root, next_day)
        self.assertEqual(len(latest_snapshots(self.rows())), 2)
        self.assertEqual(self.rows()[-1]["reach"], "")

    def test_zero_reach_has_no_defined_ratio(self):
        row = record_snapshot(self.root, dict(self.observation, reach=0, saves=0, shares=0, follows=0))
        self.assertEqual(row["reach"], "0")
        for field in ("saves_per_reach", "shares_per_reach", "follows_per_reach"):
            self.assertEqual(row[field], "")

    def test_bad_metrics_are_rejected_before_writing(self):
        for field, value in (("reach", -1), ("views", "1.5"), ("average_watch_seconds", "NaN"), ("skip_rate_percent", 101), ("total_watch_seconds", "Infinity")):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                record_snapshot(self.root, dict(self.observation, **{field: value}))
        self.assertEqual(self.rows(), [])

    def test_observation_scope_and_precision_are_preserved(self):
        record_snapshot(self.root, dict(self.observation, views=12))
        record_snapshot(self.root, dict(self.observation, views=10, scope="instagram_public_grid"))
        self.assertEqual(len(latest_snapshots(self.rows())), 2)
        self.assertTrue(all(row["observed_at"] == "2026-09-15" for row in self.rows()))
        with self.assertRaises(ValueError):
            record_snapshot(self.root, dict(self.observation, observed_at="2026-09-15T12:00:00"))

    def test_link_requires_matching_explicit_manifest_reel_id(self):
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps({"reels": [{"reel_id": "2026-W37-M02"}]}), encoding="utf-8")
        with self.assertRaises(ValueError):
            record_publication(self.root, dict(self.publication, reel_id="invented", production_manifest="manifest.json"))
        row = record_publication(self.root, dict(self.publication, reel_id="2026-W37-M02", production_manifest="manifest.json", cost_amount=12, cost_currency="TWD"))
        self.assertEqual(row["reel_id"], "2026-W37-M02")
        self.assertEqual(row["production_manifest"], "manifest.json")
        self.assertEqual(manifest.read_text(encoding="utf-8"), json.dumps({"reels": [{"reel_id": "2026-W37-M02"}]}))
        with self.assertRaises(ValueError):
            record_publication(self.root, dict(self.publication, production_minutes=-1))


if __name__ == "__main__":
    unittest.main()
