import unittest

from build_weekly_packet import choose_rows, to_packet_row


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

    def test_choose_rows_uses_only_editorial_approved_rows_when_present(self):
        rows = [
            {"week": "2026-W34", "trend_name": "Raw A", "clothing_item": "皮外套"},
            {"week": "2026-W34", "trend_name": "Raw B", "clothing_item": "卡布里褲"},
            {
                "week": "2026-W34",
                "trend_name": "Edited A",
                "clothing_item": "皮革鞋包",
                "status": "editorial_approved",
                "notes": "editorial_status=approved",
            },
            {
                "week": "2026-W34",
                "trend_name": "Edited B",
                "clothing_item": "吊帶洋裝",
                "notes": "editorial_status=approved",
            },
        ]

        selected = choose_rows(rows, week="2026-W34", limit=5)

        self.assertEqual([row["clothing_item"] for row in selected], ["皮革鞋包", "吊帶洋裝"])

    def test_packet_adds_one_decision_and_one_visible_action(self):
        packet = to_packet_row(
            {
                "id": "W33-P001",
                "trend_name": "輕量防護外層",
                "audience": "20–35 歲通勤族",
                "occasion": "通勤",
                "clothing_item": "薄風衣搭直筒褲",
                "styling_rules": "外套保持輕薄；下身用直筒褲平衡",
                "pose": "自然站姿，雙手自然垂放",
                "background": "辦公大樓入口",
            },
            "2026-W33",
            1,
        )

        self.assertEqual(packet["content_engine"], "utility_with_immersion")
        self.assertEqual(packet["dressing_decision"], "通勤如何穿出輕量防護外層：外套保持輕薄")
        self.assertIn("跨出一步", packet["visible_action"])

    def test_packet_carries_editorial_fields_from_notes(self):
        packet = to_packet_row(
            {
                "id": "W34-E001",
                "trend_name": "寬版牛津襯衫日常穿法",
                "audience": "20–35歲女性",
                "occasion": "通勤",
                "clothing_item": "牛津襯衫；直筒牛仔褲",
                "notes": (
                    "editorial_status=approved; audience_problem=襯衫容易像制服; "
                    "editorial_answer=選寬版襯衫並把下擺放在直筒褲外; "
                    "opening_hook=牛津襯衫不紮，也能穿得俐落; "
                    "visual_proof=完整看見襯衫下擺與直筒褲; "
                    "practical_rule=寬版上衣搭直筒下身"
                ),
            },
            "2026-W34",
            1,
        )

        self.assertEqual(packet["dressing_decision"], "選寬版襯衫並把下擺放在直筒褲外")
        self.assertEqual(packet["audience_problem"], "襯衫容易像制服")
        self.assertEqual(packet["opening_hook"], "牛津襯衫不紮，也能穿得俐落")
        self.assertEqual(packet["visual_proof"], "完整看見襯衫下擺與直筒褲")
        self.assertEqual(packet["practical_rule"], "寬版上衣搭直筒下身")


if __name__ == "__main__":
    unittest.main()
