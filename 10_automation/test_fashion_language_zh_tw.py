import unittest

from fashion_language_zh_tw import display_mood_line, localize_display_text, localize_packet_fields


class FashionLanguageZhTwTests(unittest.TestCase):
    def test_global_terms_are_localized_for_taiwan_display(self):
        self.assertEqual(localize_display_text("卡普里褲回歸（Capri Pants）"), "七分褲回歸")
        self.assertEqual(localize_display_text("Fisherman 涼鞋+寬褲"), "漁夫涼鞋＋寬褲")
        self.assertEqual(localize_display_text("絲巾腰帶/胯部綁法（Scarf-as-Belt）"), "絲巾腰帶與胯部綁法")

    def test_packet_fields_keep_display_language_consistent(self):
        localized = localize_packet_fields(
            {
                "trend_name": "Butter Yellow",
                "clothing_item": "Fisherman Sandals+wide trousers",
                "occasion": "旅行/戶外",
            }
        )
        self.assertEqual(localized["trend_name"], "奶油黃")
        self.assertEqual(localized["clothing_item"], "漁夫涼鞋＋寬褲")
        self.assertEqual(localized["occasion"], "旅行與戶外")

    def test_canva_line_is_english_editorial_copy_with_two_lines(self):
        line = display_mood_line({"clothing_item": "Fisherman 涼鞋+寬褲"})
        self.assertEqual(line, "Light Steps.\nOpen Roads.")
        self.assertEqual(len(line.splitlines()), 2)

    def test_w29_display_terms_are_localized_without_mixed_language(self):
        self.assertEqual(
            localize_display_text("sheer mesh long-sleeve top + satin cami + wide trousers"),
            "透膚網紗長袖上衣 ＋ 緞面細肩帶背心 ＋ 寬褲",
        )
        self.assertEqual(
            localize_display_text("浪漫 Boho-Romantic (Lace與Fringe與Embroidery)"),
            "浪漫波西米亞（蕾絲、流蘇與刺繡）",
        )
        self.assertEqual(
            localize_display_text("浪漫 Boho-Romantic (Lace/Fringe/Embroidery)"),
            "浪漫波西米亞（蕾絲、流蘇與刺繡）",
        )
        self.assertEqual(
            localize_display_text("deconstructed blazer + sheer top + straight trousers"),
            "解構西裝外套 ＋ 透膚上衣 ＋ 直筒長褲",
        )


if __name__ == "__main__":
    unittest.main()
