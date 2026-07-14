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
        self.assertEqual(localized["clothing_item"], "漁夫涼鞋＋wide trousers")
        self.assertEqual(localized["occasion"], "旅行與戶外")

    def test_canva_line_has_intentional_two_line_break(self):
        line = display_mood_line({"clothing_item": "Fisherman 涼鞋+寬褲"})
        self.assertEqual(line, "漁夫涼鞋搭寬褲\n旅行走路也輕盈")
        self.assertEqual(len(line.splitlines()), 2)


if __name__ == "__main__":
    unittest.main()
