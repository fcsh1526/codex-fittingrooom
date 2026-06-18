import argparse
import csv
from pathlib import Path


FIELDNAMES = [
    "carousel_id",
    "slide1_title",
    "slide1_subtitle",
    "slide1_disclosure",
    "slide2_kicker",
    "slide2_title",
    "slide2_body",
    "slide3_kicker",
    "slide3_title",
    "slide3_body",
    "slide4_kicker",
    "slide4_title",
    "slide4_body",
    "slide5_title",
    "slide5_cta",
    "slide5_note",
    "slide5_disclosure",
    "caption_short",
    "hashtags",
]


def value(row, key, fallback=""):
    return (row.get(key) or fallback).strip()


def compact(text, limit=34):
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def build_placeholders(row):
    carousel_id = value(row, "carousel_id", "weekly-carousel")
    trend_name = value(row, "trend_name", "本週穿搭")
    clothing_item = value(row, "clothing_item", trend_name)
    occasion = value(row, "occasion", "日常")
    color_palette = value(row, "color_palette", "")
    fabric = value(row, "fabric", "")
    fit = value(row, "fit", "")
    styling_rules = value(row, "styling_rules", "")

    title = compact(f"{color_palette} {clothing_item}".strip(), 14)
    if not title:
        title = compact(trend_name, 14)

    cta_keyword = compact(clothing_item.replace(" ", ""), 8) or "同風格"

    caption = (
        f"這套想測「{trend_name}」方向。\n\n"
        f"重點是 {compact(clothing_item, 24)}，適合 {occasion}。\n\n"
        f"想看同風格單品清單，可以留言「{cta_keyword}」。\n\n"
        "AI 虛擬穿搭示意，非真人試穿。"
    )

    return {
        "carousel_id": carousel_id,
        "slide1_title": title,
        "slide1_subtitle": compact(f"{occasion}穿搭靈感", 18),
        "slide1_disclosure": "AI 虛擬穿搭示意",
        "slide2_kicker": "LOOK 01",
        "slide2_title": compact(clothing_item, 18),
        "slide2_body": compact(fit or "比例乾淨，日常好搭", 26),
        "slide3_kicker": "FABRIC",
        "slide3_title": compact(fabric or "材質重點", 16),
        "slide3_body": compact(styling_rules or "保留乾淨輪廓，避免過度裝飾", 30),
        "slide4_kicker": "STYLING",
        "slide4_title": "搭配重點",
        "slide4_body": compact(styling_rules or "鞋包用同色系，讓整套更完整", 32),
        "slide5_title": "想看同風格清單？",
        "slide5_cta": f"留言「{cta_keyword}」",
        "slide5_note": "我整理平價 / 質感 / 替代款",
        "slide5_disclosure": "AI 虛擬穿搭示意",
        "caption_short": caption,
        "hashtags": "#通勤穿搭 #上班穿搭 #女生穿搭 #穿搭靈感 #AI穿搭 #虛擬穿搭",
    }


def main():
    parser = argparse.ArgumentParser(description="Generate Canva placeholder values from a weekly content packet CSV.")
    parser.add_argument("--input", required=True, help="Input weekly content packet CSV.")
    parser.add_argument("--output", required=True, help="Output Canva placeholder CSV.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("Input CSV has no rows.")

    output_rows = [build_placeholders(row) for row in rows]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {len(output_rows)} row(s) to {output_path}")


if __name__ == "__main__":
    main()

