import argparse
import csv
import json
from pathlib import Path


def clean(value):
    return " ".join(str(value or "").split()).strip()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def slots_by_carousel(run_dir):
    slots = {}
    path = Path(run_dir) / "canva_asset_slots.csv"
    if not path.exists():
        return slots
    for row in read_csv(path):
        carousel_id = clean(row.get("carousel_id"))
        if carousel_id:
            slots.setdefault(carousel_id, []).append(row)
    return slots


def build_mapping(run_dir):
    run_dir = Path(run_dir)
    values = read_csv(run_dir / "canva_placeholder_values.csv")
    slot_map = slots_by_carousel(run_dir)
    mapping = {}
    for row in values:
        carousel_id = clean(row.get("carousel_id"))
        if not carousel_id:
            continue
        mapping[carousel_id] = {
            "placeholders": {
                "{{slide2_line}}": clean(row.get("slide2_line")),
            },
            "caption_short": clean(row.get("caption_short")),
            "hashtags": clean(row.get("hashtags")),
            "asset_slots": slot_map.get(carousel_id, []),
            "design_contract": {
                "canvas_size": "3240 x 1350 px",
                "export": "3 slides, 1080 x 1350 px each",
                "slice_guides_x": [1080, 2160],
                "text_rule": "Only slide 2 has one short line. Slides 1 and 3 are image-led.",
                "image_rule": "Use complete flat PNG/JPG Canva image assets only.",
            },
        }
    return mapping


def sync_map(run_dir, output=None):
    run_dir = Path(run_dir)
    output = Path(output) if output else run_dir / "canva_placeholder_map.json"
    mapping = build_mapping(run_dir)
    output.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    return output, mapping


def main():
    parser = argparse.ArgumentParser(description="Regenerate canva_placeholder_map.json from clean placeholder CSV and current asset slots.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    output, mapping = sync_map(args.run_dir, args.output)
    print(f"Wrote {output}")
    print(f"Carousel rows: {len(mapping)}")


if __name__ == "__main__":
    main()
