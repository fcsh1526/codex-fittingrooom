import argparse
import csv
import json
from pathlib import Path


PLACEHOLDER_FIELDS = [
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
        "slide_range": "1-2",
        "asset_type": "Grok image",
        "purpose": "strongest full-body image, used as the visual anchor",
        "recommended_file": "",
        "status": "needed",
        "notes": "Keep Mika Lin visible from head to shoes; avoid cropping across the slide boundary.",
    },
    {
        "slot_id": "detail_image",
        "slide_range": "3",
        "asset_type": "Grok image",
        "purpose": "alternate angle or outfit detail",
        "recommended_file": "",
        "status": "optional",
        "notes": "Use only if hands, face, and clothing structure are clean.",
    },
    {
        "slot_id": "texture_or_crop",
        "slide_range": "4-5",
        "asset_type": "crop / neutral background",
        "purpose": "quiet visual support for styling notes and CTA",
        "recommended_file": "",
        "status": "optional",
        "notes": "Prefer a soft crop from the same image or a clean neutral background.",
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
                "canvas_size": "5400 x 1350 px",
                "export": "5 slides, 1080 x 1350 px each",
                "slice_guides_x": [1080, 2160, 3240, 4320],
                "safe_margin_from_guides_px": 80,
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
        "Use this file after duplicating the 5400 x 1350 panorama Canva template.",
        "",
        "## Template Contract",
        "",
        "- Canvas: `5400 x 1350 px`",
        "- Export: `5 slides x 1080 x 1350 px`",
        "- Slice guides: `x = 1080, 2160, 3240, 4320`",
        "- Keep text at least `80 px` away from slice guides.",
        "- Keep the AI disclosure visible on slide 1 and slide 5.",
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
                "- Text does not cross slice boundaries.",
                "- Mika Lin remains visually consistent.",
                "- Outfit is readable on a phone screen.",
                "- AI disclosure is visible.",
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
