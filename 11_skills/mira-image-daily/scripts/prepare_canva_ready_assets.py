import argparse
import csv
import json
from pathlib import Path

from PIL import Image, ImageOps


VARIANT_SLOTS = {"A": "cover_image", "B": "motion_crop", "C": "detail_image"}


def clean(value):
    return " ".join(str(value or "").split()).strip()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_source(project_root, job_dir, value):
    path = Path(value)
    candidates = [path] if path.is_absolute() else [job_dir / path, project_root / path]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise SystemExit(f"Source image not found: {value}")


def packet_for(run_dir, carousel_id):
    for row in read_csv(run_dir / "weekly_content_packet.csv"):
        if clean(row.get("carousel_id")) == carousel_id:
            return row
    raise SystemExit(f"carousel_id not found: {carousel_id}")


def template_for(project_root, key):
    path = project_root / "10_automation" / "canva_template_registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    for template in registry.get("templates", []):
        if clean(template.get("key")).upper() == key:
            return template
    raise SystemExit(f"Canva template not found: {key}")


def center_crop_box(width, height, target_ratio):
    source_ratio = width / height
    if source_ratio > target_ratio:
        crop_width = round(height * target_ratio)
        left = (width - crop_width) // 2
        return (left, 0, left + crop_width, height), 1 - (target_ratio / source_ratio)
    crop_height = round(width / target_ratio)
    top = (height - crop_height) // 2
    return (0, top, width, top + crop_height), 1 - (source_ratio / target_ratio)


def prepare_asset(source, output, target, max_crop_fraction):
    target_width = int(target["width"])
    target_height = int(target["height"])
    target_ratio = target_width / target_height
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        crop_box, crop_fraction = center_crop_box(image.width, image.height, target_ratio)
        if crop_fraction > max_crop_fraction:
            raise SystemExit(
                f"{source.name}: required center crop {crop_fraction:.1%} exceeds "
                f"the {max_crop_fraction:.1%} safety limit for {target_width}x{target_height}. "
                "Generate a source composed for the assigned slot instead."
            )
        prepared = image.crop(crop_box).resize((target_width, target_height), Image.Resampling.LANCZOS)
        output.parent.mkdir(parents=True, exist_ok=True)
        prepared.save(output, format="PNG", optimize=True)
    return {
        "source_file": str(source),
        "output_file": str(output),
        "source_size": [image.width, image.height],
        "target_size": [target_width, target_height],
        "target_aspect_ratio": round(target_ratio, 4),
        "center_crop_fraction": round(crop_fraction, 4),
        "visual_status": "needs_canva_frame_review",
    }


def main():
    parser = argparse.ArgumentParser(description="Normalize approved Mira assets to exact Canva frame dimensions without stretching.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--carousel-id", required=True)
    parser.add_argument("--source-a")
    parser.add_argument("--source-b")
    parser.add_argument("--source-c")
    parser.add_argument("--max-crop-fraction", type=float, default=0.15)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    run_dir = (project_root / args.run_dir).resolve() if not Path(args.run_dir).is_absolute() else Path(args.run_dir)
    packet = packet_for(run_dir, args.carousel_id)
    template_key = clean(packet.get("canva_template_key")).upper() or "A"
    template = template_for(project_root, template_key)
    job_dir = run_dir / "generated_images" / args.carousel_id
    output_dir = job_dir / "canva_ready"
    model_id = clean(packet.get("model_profile_id"))

    sources = {
        variant: value
        for variant, value in {"A": args.source_a, "B": args.source_b, "C": args.source_c}.items()
        if clean(value)
    }
    if not sources:
        raise SystemExit("Provide at least one of --source-a, --source-b, or --source-c.")
    results = {}
    for variant in sources:
        slot_id = VARIANT_SLOTS[variant]
        target = template.get("slot_geometry", {}).get(slot_id)
        if not target:
            raise SystemExit(f"v3-{template_key} is missing geometry for {slot_id}")
        source = resolve_source(project_root, job_dir, sources[variant])
        output = output_dir / (
            f"{args.carousel_id}_{model_id}_canva_{variant}_{int(target['width'])}x{int(target['height'])}.png"
        )
        results[variant] = prepare_asset(source, output, target, args.max_crop_fraction)
        results[variant]["slot_id"] = slot_id

    manifest = {
        "carousel_id": args.carousel_id,
        "model_profile_id": model_id,
        "canva_template_key": template_key,
        "canva_template_name": template.get("name"),
        "status": "needs_canva_frame_review" if len(results) == 3 else "partial_needs_remaining_variants",
        "assets": results,
    }
    manifest_path = output_dir / "canva_ready_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(manifest_path)


if __name__ == "__main__":
    main()
