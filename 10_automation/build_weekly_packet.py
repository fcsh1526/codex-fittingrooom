import argparse
import csv
import re
from datetime import date, timedelta
from pathlib import Path

from generate_canva_handoff import write_canva_handoff
from generate_canva_placeholders import FIELDNAMES as CANVA_FIELDS
from generate_canva_placeholders import build_placeholders
from fashion_language_zh_tw import localize_packet_fields
from mira_models import load_model_roster, model_for_index


PACKET_FIELDS = [
    "week_id",
    "carousel_id",
    "market",
    "creator_name",
    "model_profile_id",
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
    "canva_template_key",
]


DAILY_QUEUE_FIELDS = [
    "date",
    "daily_id",
    "week_id",
    "carousel_id",
    "model_profile_id",
    "trend_name",
    "clothing_item",
    "occasion",
    "image_status",
    "canva_status",
    "publish_status",
    "notes",
]


IMAGE_REVIEW_FIELDS = [
    "carousel_id",
    "prompt_id",
    "model_profile_id",
    "candidate_file",
    "tool",
    "model_consistency",
    "reader_relatability",
    "outfit_clarity",
    "ai_realism",
    "scene_lighting_integration",
    "outfit_continuity",
    "expression_liveliness",
    "pose_variation",
    "commerce_value",
    "publishable",
    "status",
    "notes",
]


AGE_RENDERING_RULES = [
    "Express age through styling and presence, NOT wrinkles.",
    "East Asian women look significantly younger than Western age norms.",
    "Skin is smooth and well-maintained.",
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
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


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
    row = localize_packet_fields(row)
    prompt_id = clean(row.get("id") or row.get("prompt_id") or f"P{index:03d}")
    bucket = infer_bucket(row)
    model_profile_id = model_for_index(index, week_id=week_id)
    # Intentionally ignore source model_identity/model_profile_id. Perplexity
    # controls outfit topics; Codex controls the weekly M01-M05 production roster.
    return {
        "week_id": week_id,
        "carousel_id": f"{week_id}-{index:03d}",
        "market": "Taiwan Traditional Chinese",
        "creator_name": "Mira",
        "model_profile_id": model_profile_id,
        "trend_name": clean(row.get("trend_name")),
        "content_bucket": bucket,
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
        "next_action": "Prepare Codex image brief",
    }


def model_context(packet, roster):
    profile = roster.get(clean(packet.get("model_profile_id")), {})
    if not profile:
        return "Use the Mira magazine internal model assigned to this content bucket."
    return (
        f"Internal model {profile.get('model_profile_id')} ({profile.get('internal_label')}): "
        f"{profile.get('visual_profile')} Prompt visual age language: {profile.get('prompt_age_language')}. "
        f"{' '.join(AGE_RENDERING_RULES)} Style range: {profile.get('style_range')} "
        f"Scenes: {profile.get('daily_scenes')} Avoid: {profile.get('avoid')}"
    )


def grok_prompt(packet, roster=None):
    roster = roster or {}
    return f"""## {packet['carousel_id']} - {packet['trend_name']}

Prompt ID: `{packet['prompt_id']}`
Internal model: `{packet['model_profile_id']}`

```text
Using the attached fictional AI virtual creator reference image as the subject, keep the same fictional identity, face, hairstyle, skin tone, body proportions, calm expression, and realistic Taiwan city style. Only replace the outfit.

{model_context(packet, roster)}

Dress the internal Mira magazine model in {packet['clothing_item']}, color palette {packet['color_palette']}, fabric {packet['fabric']}, fit {packet['fit']}.

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
    roster = load_model_roster()
    body = [
        "# Legacy Backup Image Prompts",
        "",
        "Historical filename: `grok_prompts.md`. The active workflow uses Codex image briefs and internal Mira model profiles.",
        "",
    ]
    for packet in packets:
        body.append(grok_prompt(packet, roster=roster))
    Path(path).write_text("\n".join(body), encoding="utf-8")


def week_start_date(week_id):
    match = re.match(r"^(\d{4})-W(\d{2})", clean(week_id))
    if not match:
        return None
    try:
        return date.fromisocalendar(int(match.group(1)), int(match.group(2)), 1)
    except ValueError:
        return None


def daily_queue_rows(week_id, packets, days=5):
    start = week_start_date(week_id)
    rows = []
    if not packets:
        return rows
    for offset in range(max(0, days)):
        packet = packets[offset % len(packets)]
        item_date = (start + timedelta(days=offset)).isoformat() if start else ""
        rows.append(
            {
                "date": item_date,
                "daily_id": f"{week_id}-D{offset + 1:02d}",
                "week_id": week_id,
                "carousel_id": packet["carousel_id"],
                "model_profile_id": packet["model_profile_id"],
                "trend_name": packet["trend_name"],
                "clothing_item": packet["clothing_item"],
                "occasion": packet["occasion"],
                "image_status": "needs_codex_image",
                "canva_status": "not_started",
                "publish_status": "not_published",
                "notes": "Use Codex image brief, then review candidates before Canva.",
            }
        )
    return rows


def write_image_generation_briefs(path, packets):
    roster = load_model_roster()
    lines = [
        "# Codex Image Generation Briefs",
        "",
        "Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.",
        "",
    ]
    for packet in packets:
        profile = roster.get(packet["model_profile_id"], {})
        lines.extend(
            [
                f"## {packet['carousel_id']} / {packet['model_profile_id']} - {packet['trend_name']}",
                "",
                f"- Internal model role: {profile.get('internal_label', packet['model_profile_id'])}",
                f"- Reader projection: {profile.get('reader_projection', '')}",
                f"- Visual profile: {profile.get('visual_profile', '')}",
                f"- Prompt visual age language: {profile.get('prompt_age_language', '')}",
                f"- Outfit: {packet['clothing_item']}",
                f"- Palette / fabric / fit: {packet['color_palette']} / {packet['fabric']} / {packet['fit']}",
                f"- Occasion: {packet['occasion']}",
                f"- Scene: {packet['scene']}",
                "",
                "### Image Prompt",
                "",
                "```text",
                "Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.",
                f"Use internal model {packet['model_profile_id']} only as a private production profile; do not render or include the model ID or any text in the image.",
                profile.get("visual_profile", ""),
                f"Prompt visual age language: {profile.get('prompt_age_language', '')}.",
                " ".join(AGE_RENDERING_RULES),
                f"Outfit: {packet['clothing_item']}; palette {packet['color_palette']}; fabric {packet['fabric']}; fit {packet['fit']}.",
                f"Styling rules: {packet['styling_rules']}.",
                f"Scene: {packet['scene']}. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.",
                "Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only pose, camera distance, and framing.",
                "Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.",
                "Composition: full outfit readable within one second, natural posture, subtle real skin texture, edge-to-edge 4:5 frame, no visible logos, no text, no watermark.",
                "Avoid: supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.",
                "```",
                "",
            ]
        )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def image_review_rows(packets):
    rows = []
    for packet in packets:
        row = {field: "" for field in IMAGE_REVIEW_FIELDS}
        row.update(
            {
                "carousel_id": packet["carousel_id"],
                "prompt_id": packet["prompt_id"],
                "model_profile_id": packet["model_profile_id"],
                "tool": "Codex",
                "publishable": "pending",
                "status": "review",
            }
        )
        rows.append(row)
    return rows


def platform_hashtags(packet):
    bucket = packet.get("content_bucket", "")
    base = [
        "#穿搭靈感",
        "#女生穿搭",
        "#AI造型",
        "#虛擬造型",
        "#Mira",
    ]
    if bucket == "office_capsule":
        base = ["#通勤穿搭", "#上班穿搭", "#日常穿搭"] + base
    elif bucket == "date_outfit":
        base = ["#約會穿搭", "#週末穿搭", "#質感穿搭"] + base
    elif bucket == "rainy_day":
        base = ["#雨天穿搭", "#機能穿搭", "#日常穿搭"] + base
    else:
        base = ["#日常穿搭", "#簡約穿搭", "#質感穿搭"] + base
    return " ".join(base[:10])


def instagram_caption(packet):
    trend = clean(packet.get("trend_name")) or "本週穿搭"
    item = clean(packet.get("clothing_item")) or trend
    occasion = clean(packet.get("occasion")) or "日常"

    return f"""{item}，給{occasion}一點生活感。

方向：{trend}。

相似單品放在個人頁連結。
AI 生成虛擬造型影像。

{platform_hashtags(packet)}"""


def first_comment(packet):
    return "不使用固定首則留言。"


def threads_copy(packet):
    trend = clean(packet.get("trend_name")) or "本週穿搭"
    item = clean(packet.get("clothing_item")) or trend
    occasion = clean(packet.get("occasion")) or "日常"
    return f"""{occasion}想穿得有記憶點，可以從 {item} 開始。

方向：{trend}。
AI 生成虛擬造型影像。"""


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
        "- Codex image candidates are generated in the project workspace.",
        "- Best lifestyle image is selected.",
        "- Image feels candid enough for social browsing, not overly posed.",
        "- Outfit is readable in one second.",
        "- Image passes AI quality review: internal model consistency, reader relatability, outfit clarity, AI realism, no logos.",
        "",
        "## Canva",
        "",
        "- Use the 3-slide minimal panorama template.",
        "- Keep slides 1 and 3 image-led.",
        "- Put at most one short sentence on slide 2.",
        "- Export 3 slides at 1080 x 1350.",
        "- Do not export the full 3240 x 1350 master canvas as slide 1.",
        "",
        "## Instagram",
        "",
        "- Keep caption short.",
        "- Put shopping link direction in caption or profile link, not in the image.",
        "- Share once to Story if it feels natural.",
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
        lines.append(f"- `{packet['carousel_id']}` / `{packet['model_profile_id']}`: {packet['trend_name']} / {packet['clothing_item']}")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_manifest(path, week_id, packets):
    lines = [
        f"# Weekly Run Manifest - {week_id}",
        "",
        "Generated artifacts:",
        "",
        "- `weekly_content_packet.csv`",
        "- `daily_queue.csv`",
        "- `image_generation_briefs.md`",
        "- `image_review_template.csv`",
        "- `grok_prompts.md` legacy backup prompt file",
        "- `canva_placeholder_values.csv`",
        "- `canva_fill_guide.md`",
        "- `canva_placeholder_map.json`",
        "- `canva_asset_slots.csv`",
        "- `post_drafts.md`",
        "- `publish_checklist.md`",
        "",
        "Selected carousel candidates:",
        "",
    ]
    for packet in packets:
        lines.append(
            f"- `{packet['carousel_id']}` / `{packet['prompt_id']}` / `{packet['model_profile_id']}` / {packet['trend_name']} / {packet['clothing_item']}"
        )
    lines.extend(
        [
            "",
            "Next user action:",
            "",
            "1. Open `daily_queue.csv` and work on the first `needs_codex_image` row.",
            "2. Use `image_generation_briefs.md` to generate candidates inside the Codex workspace.",
            "3. Score candidates in `image_review_template.csv`, then select assets for Canva.",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Build a weekly Mira carousel packet from item_prompt_database.csv.")
    parser.add_argument("--source", default="04_prompts/item_prompt_database.csv")
    parser.add_argument("--week", required=True, help="Week id to filter, e.g. 2026-W21-test or 2026-W25.")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--daily-days", type=int, default=5)
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
    daily_rows = daily_queue_rows(args.week, packets, days=args.daily_days)

    write_csv(out_dir / "weekly_content_packet.csv", PACKET_FIELDS, packets)
    write_csv(out_dir / "canva_placeholder_values.csv", CANVA_FIELDS, canva_rows)
    write_csv(out_dir / "daily_queue.csv", DAILY_QUEUE_FIELDS, daily_rows)
    write_csv(out_dir / "image_review_template.csv", IMAGE_REVIEW_FIELDS, image_review_rows(packets))
    (out_dir / "generated_images").mkdir(exist_ok=True)
    write_image_generation_briefs(out_dir / "image_generation_briefs.md", packets)
    write_grok_prompts(out_dir / "grok_prompts.md", packets)
    write_post_drafts(out_dir / "post_drafts.md", packets)
    write_publish_checklist(out_dir / "publish_checklist.md", args.week, packets)
    write_canva_handoff(out_dir, canva_rows=canva_rows)
    write_manifest(out_dir / "README.md", args.week, packets)

    print(f"Wrote {len(packets)} carousel packet(s) and {len(daily_rows)} daily item(s) to {out_dir}")


if __name__ == "__main__":
    main()
