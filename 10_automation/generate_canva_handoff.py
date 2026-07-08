import argparse
import csv
import json
from pathlib import Path


PLACEHOLDER_FIELDS = [
    "slide2_line",
]


ASSET_SLOT_FIELDS = [
    "carousel_id",
    "slot_id",
    "slide_range",
    "asset_type",
    "purpose",
    "recommended_file",
    "status",
    "notes",
]


DEFAULT_ASSET_SLOTS = [
    {
        "slot_id": "cover_image",
        "slide_range": "1",
        "asset_type": "image",
        "purpose": "strongest lifestyle full-body image; visual hook",
        "recommended_file": "",
        "status": "needed",
        "notes": "Make the person and outfit dominant. Keep text off the image.",
    },
    {
        "slot_id": "motion_crop",
        "slide_range": "2",
        "asset_type": "crop / quiet design slide",
        "purpose": "minimal transition slide with one short line",
        "recommended_file": "",
        "status": "optional",
        "notes": "Use a soft crop, blurred background, or clean negative space. Only one short sentence.",
    },
    {
        "slot_id": "detail_image",
        "slide_range": "3",
        "asset_type": "image",
        "purpose": "second lifestyle image or reused hero crop",
        "recommended_file": "",
        "status": "optional",
        "notes": "Use a second image when available. If not, use a different crop of the hero image.",
    },
]


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clean(value):
    return " ".join((value or "").split()).strip()


def carousel_label(row):
    return clean(row.get("carousel_id")) or "weekly-carousel"


def placeholder_token(field):
    return "{{" + field + "}}"


def asset_slots_for_carousel(carousel_id):
    rows = []
    for slot in DEFAULT_ASSET_SLOTS:
        row = {"carousel_id": carousel_id}
        row.update(slot)
        rows.append(row)
    return rows


def build_placeholder_map(canva_rows):
    mapping = {}
    for row in canva_rows:
        carousel_id = carousel_label(row)
        mapping[carousel_id] = {
            "placeholders": {
                placeholder_token(field): clean(row.get(field))
                for field in PLACEHOLDER_FIELDS
            },
            "caption_short": clean(row.get("caption_short")),
            "hashtags": clean(row.get("hashtags")),
            "asset_slots": asset_slots_for_carousel(carousel_id),
            "design_contract": {
                "canvas_size": "3240 x 1350 px",
                "export": "3 slides, 1080 x 1350 px each",
                "slice_guides_x": [1080, 2160],
                "safe_margin_from_guides_px": 80,
                "text_rule": "Only slide 2 has one short line. Slides 1 and 3 are image-led.",
            },
        }
    return mapping


def markdown_table(rows):
    lines = ["| Placeholder | Value |", "|---|---|"]
    for field, value in rows:
        safe_value = value.replace("|", "/")
        lines.append(f"| `{placeholder_token(field)}` | {safe_value} |")
    return "\n".join(lines)


def write_fill_guide(path, canva_rows):
    lines = [
        "# Canva Fill Guide",
        "",
        "Use this file after duplicating the 3240 x 1350 minimal panorama Canva template.",
        "",
        "## Template Contract",
        "",
        "- Canvas: `3240 x 1350 px`",
        "- Export: `3 slides x 1080 x 1350 px`",
        "- Slice guides: `x = 1080, 2160`",
        "- Slide 1: image-led hook, no required text.",
        "- Slide 2: one short transition line only.",
        "- Slide 3: image-led ending, no CTA wall.",
        "- Keep disclosure in the caption, not on the image.",
        "",
    ]

    for row in canva_rows:
        carousel_id = carousel_label(row)
        lines.extend(
            [
                f"## {carousel_id}",
                "",
                "### Text Replacements",
                "",
                markdown_table([(field, clean(row.get(field))) for field in PLACEHOLDER_FIELDS]),
                "",
                "### Asset Slots",
                "",
                "| Slot | Slide Range | Purpose | Status |",
                "|---|---:|---|---|",
            ]
        )
        for slot in asset_slots_for_carousel(carousel_id):
            lines.append(
                f"| `{slot['slot_id']}` | `{slot['slide_range']}` | {slot['purpose']} | {slot['status']} |"
            )
        lines.extend(
            [
                "",
                "### Instagram Caption",
                "",
                "```text",
                clean(row.get("caption_short")),
                "",
                clean(row.get("hashtags")),
                "```",
                "",
                "### Before Saving",
                "",
                "- All placeholder braces are gone.",
                "- Slide 2 has only one short sentence.",
                "- Mira remains visually consistent.",
                "- Outfit is readable within one second.",
                "- The post feels like a lifestyle moment, not a sales flyer.",
                "",
            ]
        )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_placeholder_map(path, canva_rows):
    mapping = build_placeholder_map(canva_rows)
    Path(path).write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")


def write_asset_slots(path, canva_rows):
    rows = []
    for row in canva_rows:
        rows.extend(asset_slots_for_carousel(carousel_label(row)))
    write_csv(path, ASSET_SLOT_FIELDS, rows)


def write_canva_handoff(run_dir, canva_rows=None):
    run_dir = Path(run_dir)
    if canva_rows is None:
        canva_rows = read_csv(run_dir / "canva_placeholder_values.csv")
    write_fill_guide(run_dir / "canva_fill_guide.md", canva_rows)
    write_placeholder_map(run_dir / "canva_placeholder_map.json", canva_rows)
    write_asset_slots(run_dir / "canva_asset_slots.csv", canva_rows)


def main():
    parser = argparse.ArgumentParser(description="Generate Canva handoff files from Canva placeholder values.")
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    write_canva_handoff(args.run_dir)
    print(f"Wrote Canva handoff files to {args.run_dir}")


if __name__ == "__main__":
    main()
