import argparse
import csv
from pathlib import Path


FIELDNAMES = [
    "carousel_id",
    "slide2_line",
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


def mood_line(row):
    clothing_item = value(row, "clothing_item", "")
    occasion = value(row, "occasion", "今天")
    trend_name = value(row, "trend_name", "")

    if clothing_item:
        base = f"{clothing_item}，讓{occasion}多一點記憶點。"
    elif trend_name:
        base = f"{occasion}，穿一點{trend_name}。"
    else:
        base = "今天，穿得簡單但有記憶點。"
    return compact(base, 24)


def build_placeholders(row):
    carousel_id = value(row, "carousel_id", "weekly-carousel")
    trend_name = value(row, "trend_name", "本週穿搭")
    clothing_item = value(row, "clothing_item", trend_name)
    occasion = value(row, "occasion", "日常")

    caption = (
        f"{compact(clothing_item, 24)}，給{occasion}一點生活感。\n\n"
        f"方向：{compact(trend_name, 28)}。\n\n"
        "相似單品放在個人頁連結。\n"
        "AI 生成虛擬造型影像。"
    )

    return {
        "carousel_id": carousel_id,
        "slide2_line": mood_line(row),
        "caption_short": caption,
        "hashtags": "#穿搭靈感 #女生穿搭 #日常穿搭 #AI造型 #虛擬造型 #Mira",
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
