import re
import unittest

from prepare_daily_image_job import packet_for_look, planned_variants, prompt_for


class PrepareDailyImageJobPromptTests(unittest.TestCase):
    def setUp(self):
        self.packet = {
            "model_profile_id": "M05",
            "trend_name": "輕量防護外層",
            "occasion": "通勤／城市旅行",
            "dressing_decision": "雨天通勤，外套不必厚重",
            "visible_action": "已經向出口跨出一步，視線看向街道，一手輕扶肩背包帶",
            "scene": "台灣街邊辦公大樓入口，夏季雨後",
            "clothing_item": "橄欖綠短版無內裡薄風衣；奶油白無袖上衣；深海軍藍高腰九分直筒褲；米白低筒鞋；深棕肩背包",
            "color_palette": "奶油白／深海軍藍／橄欖綠／深棕",
            "fabric": "霧面輕量尼龍／透氣棉質",
            "fit": "薄風衣短版微寬肩並敞開；直筒褲自然合身",
            "styling_rules": "外套必須薄、無內裡、無鋪棉，適合夏季雨天",
        }
        self.profile = {"prompt_age_language": "around 20, youthful adult"}
        self.reference = {"face_path": "face.png", "full_path": "full.png"}
        self.template = {
            "key": "B",
            "name": "Cross-Boundary Symmetric",
            "slot_geometry": {
                "cover_image": {"width": 1240, "height": 1350, "aspect_ratio": 0.9185, "composition": "portrait_hero"},
                "motion_crop": {"width": 1140, "height": 560, "aspect_ratio": 2.0357, "composition": "horizontal_motion"},
                "detail_image": {"width": 1180, "height": 1350, "aspect_ratio": 0.8741, "composition": "portrait_detail"},
            },
        }

    def test_hero_prompt_is_concise_and_uses_new_structure(self):
        prompt = prompt_for(self.packet, self.profile, self.reference, self.template, "A", "reel")
        english_words = re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", prompt)

        self.assertGreaterEqual(len(english_words), 120)
        self.assertLessEqual(len(english_words), 220)
        self.assertIn("雨天通勤，外套不必厚重", prompt)
        self.assertIn("已經向出口跨出一步", prompt)
        self.assertIn("Full-frame mirrorless", prompt)
        self.assertIn("50mm", prompt)
        self.assertNotIn("f/4", prompt)
        self.assertNotIn("ISO", prompt)
        self.assertNotIn("5200", prompt)
        self.assertNotIn("central 70", prompt)
        self.assertNotIn("smooth and well-maintained", prompt)

    def test_carousel_derivatives_are_edits_from_accepted_hero(self):
        for variant in ["B", "C"]:
            prompt = prompt_for(self.packet, self.profile, self.reference, self.template, variant, "carousel")
            self.assertIn("Edit the accepted Hero A", prompt)
            self.assertIn("do not generate an independent reinterpretation", prompt)
            self.assertIn("Preserve the same woman, exact garments", prompt)
            self.assertNotIn("f/4", prompt)
            self.assertNotIn("ISO", prompt)

        scene_prompt = prompt_for(self.packet, self.profile, self.reference, self.template, "B", "carousel")
        detail_prompt = prompt_for(self.packet, self.profile, self.reference, self.template, "C", "carousel")
        self.assertIn("scene-application frame", scene_prompt)
        self.assertIn("not the next moment", scene_prompt)
        self.assertIn("accessory-detail frame", detail_prompt)
        self.assertIn("do not invent a difficult grip", detail_prompt)

    def test_each_look_has_one_reel_frame_and_three_carousel_frames(self):
        self.assertEqual(planned_variants({}, "reel"), ["A"])
        self.assertEqual(planned_variants({}, "carousel"), ["A", "B", "C"])

    def test_look_overrides_outfit_but_keeps_theme_model(self):
        packet = {
            **self.packet,
            "carousel_id": "2026-W34-001",
            "prompt_id": "W34-001",
        }
        look = {
            "carousel_id": "2026-W34-001",
            "look_id": "2026-W34-001-L02",
            "model_profile_id": "M05",
            "theme_name": "一件襯衫，兩種夏日比例",
            "look_name": "條紋襯衫與西裝短褲",
            "clothing_item": "藍白條紋寬鬆襯衫；深藍西裝短褲；咖啡色平底鞋",
            "scene": "台北巷弄花店外",
            "visible_action": "接過一小束花後轉身離開",
            "required_frames": "2",
            "frame_plan": "hero+detail",
        }

        merged = packet_for_look(packet, look)

        self.assertEqual(merged["model_profile_id"], "M05")
        self.assertEqual(merged["look_id"], "2026-W34-001-L02")
        self.assertIn("西裝短褲", merged["clothing_item"])
        self.assertEqual(planned_variants(look, "reel"), ["A"])
        self.assertEqual(planned_variants(look, "carousel"), ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
