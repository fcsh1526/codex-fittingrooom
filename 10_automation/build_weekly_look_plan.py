import argparse
import csv
from collections import Counter
from pathlib import Path


LOOK_FIELDS = [
    "week_id",
    "carousel_id",
    "model_profile_id",
    "look_id",
    "look_order",
    "theme_name",
    "opening_hook",
    "look_name",
    "dressing_decision",
    "occasion",
    "clothing_item",
    "color_palette",
    "fabric",
    "fit",
    "styling_rules",
    "visual_proof",
    "practical_rule",
    "scene",
    "visible_action",
    "frame_plan",
    "required_frames",
    "status",
    "next_action",
]


def clean(value):
    return " ".join(str(value or "").split()).strip()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOOK_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def integer(value, label):
    try:
        return int(clean(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be an integer: {value}") from exc


def build_look_plan(packet_path, source_path, output_path, min_looks=2, max_looks=2):
    packets = read_csv(packet_path)
    source_rows = read_csv(source_path)
    packet_by_id = {clean(row.get("carousel_id")): row for row in packets}
    if not packet_by_id:
        raise ValueError("weekly_content_packet.csv has no rows.")
    if not source_rows:
        raise ValueError("Editor-approved look source has no rows.")

    rows = []
    seen_look_ids = set()
    seen_orders = set()
    for source in source_rows:
        carousel_id = clean(source.get("carousel_id"))
        packet = packet_by_id.get(carousel_id)
        if not packet:
            raise ValueError(f"Unknown carousel_id in look source: {carousel_id}")

        look_order = integer(source.get("look_order"), f"{carousel_id} look_order")
        order_key = (carousel_id, look_order)
        if order_key in seen_orders:
            raise ValueError(f"Duplicate look_order for {carousel_id}: {look_order}")
        seen_orders.add(order_key)

        source_model = clean(source.get("model_profile_id"))
        packet_model = clean(packet.get("model_profile_id"))
        if source_model and source_model != packet_model:
            raise ValueError(
                f"{carousel_id} look model {source_model} does not match theme model {packet_model}."
            )

        look_id = clean(source.get("look_id")) or f"{carousel_id}-L{look_order:02d}"
        if look_id in seen_look_ids:
            raise ValueError(f"Duplicate look_id: {look_id}")
        seen_look_ids.add(look_id)

        source_required_frames = integer(source.get("required_frames") or 3, f"{look_id} required_frames")
        if source_required_frames not in {2, 3}:
            raise ValueError(f"{look_id} required_frames must be 2 or 3.")
        required_frames = 3

        clothing_item = clean(source.get("clothing_item"))
        scene = clean(source.get("scene"))
        visible_action = clean(source.get("visible_action"))
        if not clothing_item or not scene or not visible_action:
            raise ValueError(f"{look_id} requires clothing_item, scene, and visible_action.")

        frame_plan = "carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16"

        row = {
            "week_id": clean(packet.get("week_id")),
            "carousel_id": carousel_id,
            "model_profile_id": packet_model,
            "look_id": look_id,
            "look_order": look_order,
            "theme_name": clean(packet.get("trend_name")),
            "opening_hook": clean(source.get("opening_hook")) or clean(packet.get("opening_hook")),
            "look_name": clean(source.get("look_name")) or f"Look {look_order}",
            "dressing_decision": clean(source.get("dressing_decision"))
            or clean(packet.get("editorial_answer"))
            or clean(packet.get("dressing_decision")),
            "occasion": clean(source.get("occasion")) or clean(packet.get("occasion")),
            "clothing_item": clothing_item,
            "color_palette": clean(source.get("color_palette")),
            "fabric": clean(source.get("fabric")),
            "fit": clean(source.get("fit")),
            "styling_rules": clean(source.get("styling_rules")),
            "visual_proof": clean(source.get("visual_proof")) or clean(packet.get("visual_proof")),
            "practical_rule": clean(source.get("practical_rule")) or clean(packet.get("practical_rule")),
            "scene": scene,
            "visible_action": visible_action,
            "frame_plan": frame_plan,
            "required_frames": required_frames,
            "status": clean(source.get("status")) or "editorial_approved",
            "next_action": "Prepare both surface jobs: Reel A, then Carousel A/B/C",
        }
        rows.append(row)

    counts = Counter(row["carousel_id"] for row in rows)
    missing = sorted(set(packet_by_id) - set(counts))
    if missing:
        raise ValueError(f"Look source is missing theme(s): {', '.join(missing)}")
    for carousel_id, count in sorted(counts.items()):
        if not min_looks <= count <= max_looks:
            raise ValueError(
                f"{carousel_id} must have {min_looks}-{max_looks} looks; found {count}."
            )

    rows.sort(key=lambda row: (row["carousel_id"], int(row["look_order"])))
    write_csv(output_path, rows)
    return rows


def main():
    parser = argparse.ArgumentParser(description="Build a model-locked weekly Mira look plan.")
    parser.add_argument("--packet", required=True, help="weekly_content_packet.csv path")
    parser.add_argument("--source", required=True, help="Editor-approved look source CSV")
    parser.add_argument("--output", required=True, help="weekly_look_plan.csv output path")
    parser.add_argument("--min-looks", type=int, default=2)
    parser.add_argument("--max-looks", type=int, default=2)
    args = parser.parse_args()

    rows = build_look_plan(
        packet_path=args.packet,
        source_path=args.source,
        output_path=args.output,
        min_looks=args.min_looks,
        max_looks=args.max_looks,
    )
    print(f"Wrote {len(rows)} look row(s) to {args.output}")


if __name__ == "__main__":
    main()
