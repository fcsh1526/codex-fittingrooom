import csv
import unittest
from pathlib import Path

from build_weekly_look_plan import build_look_plan


def write_rows(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class BuildWeeklyLookPlanTests(unittest.TestCase):
    def test_builds_two_looks_and_inherits_theme_model(self):
        test_tmp_root = Path(__file__).resolve().parents[1] / "tmp"
        test_tmp_root.mkdir(parents=True, exist_ok=True)
        packet_path = test_tmp_root / "unit_weekly_look_packet.csv"
        source_path = test_tmp_root / "unit_weekly_look_source.csv"
        output_path = test_tmp_root / "unit_weekly_look_output.csv"
        for path in [packet_path, source_path, output_path]:
            self.addCleanup(path.unlink, missing_ok=True)

        write_rows(
            packet_path,
            [
                "week_id",
                "carousel_id",
                "model_profile_id",
                "trend_name",
                "opening_hook",
                "editorial_answer",
                "occasion",
                "visual_proof",
                "practical_rule",
            ],
            [
                {
                    "week_id": "2026-W34",
                    "carousel_id": "2026-W34-001",
                    "model_profile_id": "M03",
                    "trend_name": "牛津襯衫",
                    "opening_hook": "牛津襯衫不紮，也能穿得俐落",
                    "editorial_answer": "使用寬版襯衫",
                    "occasion": "通勤",
                    "visual_proof": "看見完整下擺",
                    "practical_rule": "寬版搭直筒",
                }
            ],
        )
        write_rows(
            source_path,
            [
                "carousel_id",
                "look_order",
                "look_name",
                "clothing_item",
                "color_palette",
                "fabric",
                "fit",
                "styling_rules",
                "scene",
                "visible_action",
                "required_frames",
            ],
            [
                {
                    "carousel_id": "2026-W34-001",
                    "look_order": "1",
                    "look_name": "Look One",
                    "clothing_item": "襯衫；牛仔褲",
                    "color_palette": "藍；白",
                    "fabric": "棉；丹寧",
                    "fit": "寬版；直筒",
                    "styling_rules": "下擺不紮",
                    "scene": "書店入口",
                    "visible_action": "推門",
                    "required_frames": "2",
                },
                {
                    "carousel_id": "2026-W34-001",
                    "look_order": "2",
                    "look_name": "Look Two",
                    "clothing_item": "襯衫；短褲",
                    "color_palette": "藍；黑",
                    "fabric": "棉；西裝料",
                    "fit": "寬版；直筒",
                    "styling_rules": "袖口捲起",
                    "scene": "有棚人行道",
                    "visible_action": "把書放進包裡",
                    "required_frames": "2",
                },
            ],
        )

        rows = build_look_plan(packet_path, source_path, output_path)

        self.assertEqual(len(rows), 2)
        self.assertEqual({row["model_profile_id"] for row in rows}, {"M03"})
        self.assertEqual([row["look_id"] for row in rows], ["2026-W34-001-L01", "2026-W34-001-L02"])
        self.assertEqual({row["opening_hook"] for row in rows}, {"牛津襯衫不紮，也能穿得俐落"})
        self.assertEqual(
            {row["frame_plan"] for row in rows},
            {"carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16"},
        )
        self.assertEqual({row["required_frames"] for row in rows}, {3})


if __name__ == "__main__":
    unittest.main()
