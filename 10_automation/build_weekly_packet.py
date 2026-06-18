import argparse
import csv
from pathlib import Path

from generate_canva_placeholders import FIELDNAMES as CANVA_FIELDS
from generate_canva_placeholders import build_placeholders


PACKET_FIELDS = [
    "week_id",
    "carousel_id",
    "market",
    "creator_name",
    "trend_name",
    "content_bucket",
    "audience",
    "occasion",
    "prompt_id",
    "clothing_item",
    "color_palette",
    "fabric",
    "fit",
    "styling_rules",
    "scene",
    "cover_asset",
    "detail_asset",
    "drive_folder_url",
    "canva_design_url",
    "ig_post_url",
    "status",
    "next_action",
]


DEFAULT_SCENES = [
    "Taipei office lobby with soft daylight",
    "simple studio wall with neutral shadows",
    "department store fitting area",
    "MRT-adjacent weekday walkway",
    "quiet cafe street in Taipei",
]


def read_rows(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clean(value):
    return (value or "").strip()


def choose_rows(rows, week=None, limit=2):
    if week:
        matched = [row for row in rows if clean(row.get("week")) == week]
    else:
        matched = rows

    usable = []
    for row in matched:
        if clean(row.get("clothing_item")) and clean(row.get("trend_name")):
            usable.append(row)

    return usable[:limit]


def infer_bucket(row):
    occasion = clean(row.get("occasion")).lower()
    trend = clean(row.get("trend_name")).lower()
    item = clean(row.get("clothing_item")).lower()
    text = " ".join([occasion, trend, item])

    if any(word in text for word in ["office", "commute", "通勤", "上班", "西裝"]):
        return "office_capsule"
    if any(word in text for word in ["date", "約會"]):
        return "date_outfit"
    if any(word in text for word in ["weekend", "週末", "咖啡"]):
        return "weekend_daily"
    if any(word in text for word in ["rain", "雨"]):
        return "rainy_day"
    return "daily_style"


def to_packet_row(row, week_id, index):
    prompt_id = clean(row.get("id") or row.get("prompt_id") or f"P{index:03d}")
    return {
        "week_id": week_id,
        "carousel_id": f"{week_id}-{index:03d}",
        "market": "Taiwan Traditional Chinese",
        "creator_name": "Mika Lin",
        "trend_name": clean(row.get("trend_name")),
        "content_bucket": infer_bucket(row),
        "audience": clean(row.get("audience")),
        "occasion": clean(row.get("occasion")),
        "prompt_id": prompt_id,
        "clothing_item": clean(row.get("clothing_item")),
        "color_palette": clean(row.get("color_palette")),
        "fabric": clean(row.get("fabric")),
        "fit": clean(row.get("fit")),
        "styling_rules": clean(row.get("styling_rules")),
        "scene": clean(row.get("background")) or DEFAULT_SCENES[(index - 1) % len(DEFAULT_SCENES)],
        "cover_asset": "",
        "detail_asset": "",
        "drive_folder_url": "",
        "canva_design_url": "",
        "ig_post_url": "",
        "status": "draft",
        "next_action": "Generate Grok images",
    }


def grok_prompt(packet):
    return f"""## {packet['carousel_id']} - {packet['trend_name']}

Prompt ID: `{packet['prompt_id']}`

```text
Using the attached fictional AI virtual creator reference image as the subject, keep the same fictional identity, face, hairstyle, skin tone, body proportions, calm expression, and realistic Taiwan city style. Only replace the outfit.

Dress Mika Lin in {packet['clothing_item']}, color palette {packet['color_palette']}, fabric {packet['fabric']}, fit {packet['fit']}.

Styling rules: {packet['styling_rules']}.

Scene: {packet['scene']}. Use a practical Taiwan daily-life setting, realistic natural light, no luxury logos, no brand signage.

Camera: vertical fashion social media image, clear full outfit from head to shoes, clean composition, outfit easy to inspect on a phone screen.

Output 3-5 variations.
```

Negative prompt:

```text
AI virtual outfit only; fictional person; no real person likeness; no celebrity; no childlike appearance; no school uniform; no nudity; no sexualized pose; no visible brand logos; no luxury logo; no fake endorsement; no distorted hands; no extra fingers; no unreadable text; no watermark.
```
"""


def write_grok_prompts(path, packets):
    body = [
        "# Weekly Grok Prompts",
        "",
        "Use these prompts in Grok Imagine with the Mika Lin reference image.",
        "",
    ]
    for packet in packets:
        body.append(grok_prompt(packet))
    Path(path).write_text("\n".join(body), encoding="utf-8")


def platform_hashtags(packet):
    bucket = packet.get("content_bucket", "")
    base = [
        "#穿搭靈感",
        "#女生穿搭",
        "#AI穿搭",
        "#虛擬穿搭",
        "#MikaLin",
    ]
    if bucket == "office_capsule":
        base = ["#通勤穿搭", "#上班穿搭", "#小資穿搭", "#西裝外套"] + base
    elif bucket == "date_outfit":
        base = ["#約會穿搭", "#週末穿搭", "#質感穿搭"] + base
    elif bucket == "rainy_day":
        base = ["#雨天穿搭", "#機能穿搭", "#日常穿搭"] + base
    else:
        base = ["#日常穿搭", "#簡約穿搭", "#質感穿搭"] + base
    return " ".join(base[:10])


def comment_keyword(packet):
    item = clean(packet.get("clothing_item")) or clean(packet.get("trend_name")) or "同風格"
    trend = clean(packet.get("trend_name"))
    for candidate in [item, trend]:
        compacted = candidate.replace(" ", "")
        if any("\u4e00" <= char <= "\u9fff" for char in compacted):
            return compacted[:8]
    return "同風格"


def instagram_caption(packet):
    keyword = comment_keyword(packet)
    trend = clean(packet.get("trend_name")) or "本週穿搭"
    item = clean(packet.get("clothing_item")) or trend
    occasion = clean(packet.get("occasion")) or "日常"

    return f"""這套想測「{trend}」方向。

重點是 {item}，適合 {occasion}。

你會把這套穿去{occasion}嗎？
留言 1 = 會
留言 2 = 不會

想看同風格單品清單，也可以留言「{keyword}」。

AI 虛擬穿搭示意，非真人試穿。

{platform_hashtags(packet)}"""


def first_comment(packet):
    keyword = comment_keyword(packet)
    return f"""AI 虛擬穿搭示意，非真人試穿。
如果想看同風格清單，可以留言「{keyword}」，我會整理平價 / 質感 / 替代款。"""


def threads_copy(packet):
    trend = clean(packet.get("trend_name")) or "本週穿搭"
    item = clean(packet.get("clothing_item")) or trend
    occasion = clean(packet.get("occasion")) or "日常"
    return f"""這套 {item} 適合{occasion}嗎？

我在測 AI 虛擬穿搭帳號的「{trend}」方向。你會穿嗎？留言 1=會，2=不會。

AI 虛擬穿搭示意，非真人試穿。"""


def pinterest_copy(packet):
    trend = clean(packet.get("trend_name")) or "Weekly outfit idea"
    item = clean(packet.get("clothing_item")) or trend
    palette = clean(packet.get("color_palette")) or "neutral palette"
    occasion = clean(packet.get("occasion")) or "daily wear"
    return {
        "title": f"{trend} outfit idea",
        "description": (
            f"AI virtual outfit inspiration featuring {item}, {palette}, for {occasion}. "
            "Save this for outfit planning. AI virtual outfit, not a real try-on."
        ),
    }


def write_post_drafts(path, packets):
    lines = [
        "# Weekly Platform Post Drafts",
        "",
        "Use these drafts after the image assets and Canva carousel are ready.",
        "",
    ]
    for packet in packets:
        pinterest = pinterest_copy(packet)
        lines.extend(
            [
                f"## {packet['carousel_id']} - {packet['trend_name']}",
                "",
                "### Instagram Caption",
                "",
                "```text",
                instagram_caption(packet),
                "```",
                "",
                "### Instagram First Comment",
                "",
                "```text",
                first_comment(packet),
                "```",
                "",
                "### Threads Copy",
                "",
                "```text",
                threads_copy(packet),
                "```",
                "",
                "### Pinterest Pin",
                "",
                f"Title: `{pinterest['title']}`",
                "",
                "Description:",
                "",
                "```text",
                pinterest["description"],
                "```",
                "",
            ]
        )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_publish_checklist(path, week_id, packets):
    lines = [
        f"# Publish Checklist - {week_id}",
        "",
        "Use this checklist for each carousel before publishing.",
        "",
        "## Before Canva",
        "",
        "- Grok output folder is in Google Drive.",
        "- Best cover image is selected.",
        "- Best full-body detail image is selected.",
        "- Image passes AI quality review: identity, outfit clarity, hands/body, no logos.",
        "",
        "## Canva",
        "",
        "- Replace all placeholders from `canva_placeholder_values.csv`.",
        "- Confirm text is readable on mobile.",
        "- Export 5 slides at 1080 x 1350.",
        "- Do not export the full 5400 x 1350 master canvas as slide 1.",
        "",
        "## Instagram",
        "",
        "- Publish as carousel only after account visibility is confirmed.",
        "- Add first comment immediately.",
        "- Share once to Story.",
        "- Send to 3 trusted people for clean manual seed traffic if reach is still low.",
        "",
        "## Metrics",
        "",
        "- Record 6-hour metrics.",
        "- Record 24-hour metrics.",
        "- If reach is 0, run `09_sops/instagram_zero_reach_recovery.md`.",
        "",
        "## Carousel Candidates",
        "",
    ]
    for packet in packets:
        lines.append(f"- `{packet['carousel_id']}`: {packet['trend_name']} / {packet['clothing_item']}")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_manifest(path, week_id, packets):
    lines = [
        f"# Weekly Run Manifest - {week_id}",
        "",
        "Generated artifacts:",
        "",
        "- `weekly_content_packet.csv`",
        "- `grok_prompts.md`",
        "- `canva_placeholder_values.csv`",
        "- `post_drafts.md`",
        "- `publish_checklist.md`",
        "",
        "Selected carousel candidates:",
        "",
    ]
    for packet in packets:
        lines.append(f"- `{packet['carousel_id']}` / `{packet['prompt_id']}` / {packet['trend_name']} / {packet['clothing_item']}")
    lines.extend(
        [
            "",
            "Next user action:",
            "",
            "1. Generate 3-5 Grok images for each prompt.",
            "2. Put outputs in Google Drive.",
            "3. Provide the Drive folder and Canva design URL to Codex.",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Build a weekly Mika Lin carousel packet from item_prompt_database.csv.")
    parser.add_argument("--source", default="04_prompts/item_prompt_database.csv")
    parser.add_argument("--week", required=True, help="Week id to filter, e.g. 2026-W21-test or 2026-W25.")
    parser.add_argument("--limit", type=int, default=2)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = read_rows(args.source)
    selected = choose_rows(rows, week=args.week, limit=args.limit)
    if not selected:
        raise SystemExit(f"No usable rows found for week: {args.week}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    packets = [to_packet_row(row, args.week, index) for index, row in enumerate(selected, start=1)]
    canva_rows = [build_placeholders(packet) for packet in packets]

    write_csv(out_dir / "weekly_content_packet.csv", PACKET_FIELDS, packets)
    write_csv(out_dir / "canva_placeholder_values.csv", CANVA_FIELDS, canva_rows)
    write_grok_prompts(out_dir / "grok_prompts.md", packets)
    write_post_drafts(out_dir / "post_drafts.md", packets)
    write_publish_checklist(out_dir / "publish_checklist.md", args.week, packets)
    write_manifest(out_dir / "README.md", args.week, packets)

    print(f"Wrote {len(packets)} carousel packet(s) to {out_dir}")


if __name__ == "__main__":
    main()
