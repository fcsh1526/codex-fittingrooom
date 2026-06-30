import argparse
import csv
import json
from pathlib import Path


REVIEW_FIELDS = [
    "carousel_id",
    "prompt_id",
    "model_profile_id",
    "candidate_file",
    "tool",
    "model_consistency",
    "reader_relatability",
    "outfit_clarity",
    "ai_realism",
    "commerce_value",
    "publishable",
    "status",
    "notes",
]


def clean(value):
    return " ".join((value or "").split()).strip()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def load_roster(project_root):
    path = project_root / "02_brand" / "mira_model_roster.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {row["model_profile_id"]: row for row in data.get("profiles", [])}


def load_reference_manifest(project_root):
    path = project_root / "02_brand" / "mira_reference_images.csv"
    if not path.exists():
        return {}, path
    rows = read_csv(path)
    return {clean(row.get("model_profile_id")): row for row in rows}, path


def find_packet(run_dir, carousel_id):
    rows = read_csv(run_dir / "weekly_content_packet.csv")
    for row in rows:
        if clean(row.get("carousel_id")) == carousel_id:
            return row
    raise SystemExit(f"carousel_id not found in weekly_content_packet.csv: {carousel_id}")


def find_carousel_id(run_dir, carousel_id=None, daily_id=None):
    if carousel_id:
        return carousel_id
    if not daily_id:
        raise SystemExit("Provide --carousel-id or --daily-id.")
    rows = read_csv(run_dir / "daily_queue.csv")
    for row in rows:
        if clean(row.get("daily_id")) == daily_id:
            return clean(row.get("carousel_id"))
    raise SystemExit(f"daily_id not found in daily_queue.csv: {daily_id}")


def reference_status(project_root, model_id):
    manifest, manifest_path = load_reference_manifest(project_root)
    row = manifest.get(model_id)
    if not row:
        return {
            "ok": False,
            "message": f"Missing manifest row for {model_id} in {manifest_path}",
            "path": "",
        }
    ref_path = project_root / clean(row.get("reference_image_path"))
    status = clean(row.get("status")).lower()
    if status != "approved":
        return {
            "ok": False,
            "message": f"Reference image for {model_id} is not approved: status={status or 'blank'}",
            "path": str(ref_path),
        }
    if not ref_path.exists():
        return {
            "ok": False,
            "message": f"Reference image file is missing for {model_id}: {ref_path}",
            "path": str(ref_path),
        }
    return {"ok": True, "message": "approved", "path": str(ref_path)}


def prompt_for(packet, profile, reference_path, variant):
    variant_scene = {
        "A": "safest full-body daily lifestyle image",
        "B": "movement or street-style variation",
        "C": "closer outfit-detail-friendly variation while keeping the outfit readable",
    }[variant]
    return f"""Candidate {variant}: {variant_scene}

Use the attached reference start image as the identity anchor:
{reference_path}

Create a realistic vertical 4:5 lifestyle fashion image for Mira, an AI fashion magazine brand.

Use internal model {packet['model_profile_id']} only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
{profile.get('visual_profile', '')}

Trend and outfit:
Global trend signal: {packet.get('trend_name', '')}
Clothing item: {packet.get('clothing_item', '')}
Palette: {packet.get('color_palette', '')}
Fabric: {packet.get('fabric', '')}
Fit: {packet.get('fit', '')}
Occasion: {packet.get('occasion', '')}
Styling rules: {packet.get('styling_rules', '')}

Scene:
Use a believable daily-life fashion magazine scene that fits the occasion and outfit. Existing scene hint: {packet.get('scene', '')}. Do not force Taiwan if another global daily setting better fits the trend, but keep the image wearable and relatable.

Composition:
Full outfit readable within one second. Natural posture. Soft realistic light. Real skin texture. Clothes are clear. Face remains consistent with the reference start image.

Avoid:
supermodel proportions, runway pose, luxury hotel ad, resort fantasy, plastic skin, excessive filters, sexualized pose, childlike styling, celebrity likeness, visible logos, image text, watermark.
"""


def write_job(project_root, run_dir, carousel_id, tool):
    roster = load_roster(project_root)
    packet = find_packet(run_dir, carousel_id)
    model_id = clean(packet.get("model_profile_id"))
    profile = roster.get(model_id)
    if not profile:
        raise SystemExit(f"Unknown model_profile_id: {model_id}")
    ref = reference_status(project_root, model_id)
    if not ref["ok"]:
        raise SystemExit(ref["message"])

    job_dir = run_dir / "generated_images" / carousel_id
    job_dir.mkdir(parents=True, exist_ok=True)

    prompts = [prompt_for(packet, profile, ref["path"], variant) for variant in ["A", "B", "C"]]
    (job_dir / "candidate_prompts.md").write_text("# Candidate Prompts\n\n" + "\n\n---\n\n".join(prompts), encoding="utf-8")

    job_lines = [
        "# Mira Daily Image Job",
        "",
        f"- carousel_id: `{carousel_id}`",
        f"- model_profile_id: `{model_id}`",
        f"- reference_image: `{ref['path']}`",
        f"- trend: {packet.get('trend_name', '')}",
        f"- clothing_item: {packet.get('clothing_item', '')}",
        f"- occasion: {packet.get('occasion', '')}",
        "",
        "Generate 2-3 candidates, then score them before Canva.",
    ]
    (job_dir / "image_job.md").write_text("\n".join(job_lines), encoding="utf-8")

    rows = []
    for variant in ["A", "B", "C"]:
        file_name = f"{carousel_id}_{model_id}_candidate_{variant}.png"
        rows.append(
            {
                "carousel_id": carousel_id,
                "prompt_id": clean(packet.get("prompt_id")),
                "model_profile_id": model_id,
                "candidate_file": file_name,
                "tool": tool,
                "publishable": "pending",
                "status": "review",
                "notes": "Score after generation.",
            }
        )
    write_csv(job_dir / "review_sheet.csv", REVIEW_FIELDS, rows)
    print(job_dir)


def main():
    parser = argparse.ArgumentParser(description="Prepare a strict Mira daily image generation job.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--carousel-id")
    parser.add_argument("--daily-id")
    parser.add_argument("--tool", default="Codex")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    run_dir = (project_root / args.run_dir).resolve() if not Path(args.run_dir).is_absolute() else Path(args.run_dir)
    carousel_id = find_carousel_id(run_dir, carousel_id=args.carousel_id, daily_id=args.daily_id)
    write_job(project_root, run_dir, carousel_id, args.tool)


if __name__ == "__main__":
    main()
