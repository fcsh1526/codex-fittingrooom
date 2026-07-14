import unittest

from build_weekly_packet import choose_rows


class BuildWeeklyPacketTests(unittest.TestCase):
    def test_choose_rows_prefers_distinct_trends(self):
        rows = [
            {"week": "2026-W29", "trend_name": "Trend A", "clothing_item": "A1"},
            {"week": "2026-W29", "trend_name": "Trend A", "clothing_item": "A2"},
            {"week": "2026-W29", "trend_name": "Trend B", "clothing_item": "B1"},
            {"week": "2026-W29", "trend_name": "Trend B", "clothing_item": "B2"},
            {"week": "2026-W29", "trend_name": "Trend C", "clothing_item": "C1"},
        ]

        selected = choose_rows(rows, week="2026-W29", limit=3)

        self.assertEqual([row["clothing_item"] for row in selected], ["A1", "B1", "C1"])

    def test_choose_rows_fills_remaining_slots_when_trends_are_fewer(self):
        rows = [
            {"week": "2026-W29", "trend_name": "Trend A", "clothing_item": "A1"},
            {"week": "2026-W29", "trend_name": "Trend A", "clothing_item": "A2"},
            {"week": "2026-W29", "trend_name": "Trend B", "clothing_item": "B1"},
        ]

        selected = choose_rows(rows, week="2026-W29", limit=3)

        self.assertEqual([row["clothing_item"] for row in selected], ["A1", "B1", "A2"])


if __name__ == "__main__":
    unittest.main()
