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
    face_path_value = clean(row.get("reference_face_path")) or clean(row.get("reference_image_path"))
    full_path_value = clean(row.get("reference_full_path")) or face_path_value
    face_path = project_root / face_path_value
    full_path = project_root / full_path_value
    status = clean(row.get("status")).lower()
    if status != "approved":
        return {
            "ok": False,
            "message": f"Reference image for {model_id} is not approved: status={status or 'blank'}",
            "face_path": str(face_path),
            "full_path": str(full_path),
        }
    if not face_path.exists():
        return {
            "ok": False,
            "message": f"Reference face image file is missing for {model_id}: {face_path}",
            "face_path": str(face_path),
            "full_path": str(full_path),
        }
    if not full_path.exists():
        return {
            "ok": False,
            "message": f"Reference full-body image file is missing for {model_id}: {full_path}",
            "face_path": str(face_path),
            "full_path": str(full_path),
        }
    return {"ok": True, "message": "approved", "face_path": str(face_path), "full_path": str(full_path)}


def prompt_for(packet, profile, reference, variant):
    variant_scene = {
        "A": "safest full-body daily lifestyle image",
        "B": "movement or street-style variation",
        "C": "closer outfit-detail-friendly variation while keeping the outfit readable",
    }[variant]
    variant_direction = {
        "A": (
            "Use an asymmetric three-quarter standing pose with a natural weight shift. "
            "Keep the eyes attentive and add a restrained micro-smile or relaxed engaged expression. "
            "At least one hand should interact naturally with the bag, jacket, pocket, railing, or nearby object; "
            "do not leave both arms straight and symmetrical."
        ),
        "B": (
            "Capture a candid mid-step or turning moment with visible body movement. "
            "Use an off-camera gaze or a brief glance back toward camera, natural hair and fabric motion, "
            "and one hand adjusting the bag, scarf, sleeve, or hair. Do not repeat Candidate A's stance or expression."
        ),
        "C": (
            "Use a closer three-quarter or outfit-detail-friendly composition with a different camera height and body angle. "
            "The model may lean lightly, pause beside furniture, or turn across the frame while keeping the full outfit readable. "
            "Use a warm attentive expression different from A and B; avoid a centered passport-photo stance."
        ),
    }[variant]
    return f"""Candidate {variant}: {variant_scene}

Attach both reference start images to the image-generation request. File paths alone are not enough:
- Face anchor: {reference['face_path']}
- Full-body anchor: {reference['full_path']}
{"- Wardrobe-lock reference: accepted Candidate A from this same job" if variant in {"B", "C"} else "- Wardrobe-lock reference: Candidate A is created in this step"}

Create a realistic vertical 4:5 lifestyle fashion image for Mira, an AI fashion magazine brand.

Use internal model {packet['model_profile_id']} only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
{profile.get('visual_profile', '')}
Prompt visual age language: {profile.get('prompt_age_language', '')}

Reference-anchor use lock:
The face image locks identity, facial geometry, skin character, and hair baseline only. The full-body image locks identity and body proportions only. Do not copy the references' neutral expression, straight-on passport angle, centered stance, hand position, studio background, lighting, or reference outfit. Preserve identity while creating a genuinely new lifestyle photograph.

Age rendering rules:
{chr(10).join(AGE_RENDERING_RULES)}

Trend and outfit:
Global trend signal: {packet.get('trend_name', '')}
Clothing item: {packet.get('clothing_item', '')}
Palette: {packet.get('color_palette', '')}
Fabric: {packet.get('fabric', '')}
Fit: {packet.get('fit', '')}
Occasion: {packet.get('occasion', '')}
Styling rules: {packet.get('styling_rules', '')}

Outfit continuity lock:
Candidates A, B, and C are three photographs from the same outfit session. Keep the exact same top layers, neckline, sleeve length, trousers or skirt, hem length, fabric, palette, shoes, bag, jewelry, and scarf placement in all three candidates. Only pose, camera distance, and framing may change. Do not reinterpret the trend into a different outfit for B or C.

Scene:
Use a believable daily-life fashion magazine scene that fits the occasion and outfit. Existing scene hint: {packet.get('scene', '')}. Do not force Taiwan if another global daily setting better fits the trend, but keep the image wearable and relatable.

Lighting integration lock:
First establish one physically plausible key-light source inside the scene, such as daylight from a visible window or open street. Its direction and color temperature must affect the entire person consistently: forehead, cheeks, nose shadow, neck, arms, clothing folds, shoes, and bag. The side facing away from the source must be visibly darker and pick up the scene's ambient color. Add grounded contact shadows under both shoes and natural cast shadows on nearby surfaces. Match subject contrast, white balance, grain, depth of field, and edge softness to the background. The person must look photographed in the location, never cut out and pasted onto a background. No frontal beauty light, ring-light catchlights, shadowless face, studio fill, halo edges, or independent subject lighting.

Composition:
Full outfit readable within one second. Natural posture. Real skin texture. Clothes are clear. Face remains consistent with the attached face anchor, and body proportions remain consistent with the attached full-body anchor. Fill the full 4:5 frame edge to edge with no white border or letterboxing.

Candidate-specific direction:
{variant_direction}

Avoid:
supermodel proportions, runway pose, luxury hotel ad, resort fantasy, plastic skin, excessive filters, pasted-on subject, mismatched key light, shadowless face, missing contact shadows, outfit changes between candidates, repeated A/B/C pose, repeated expression, centered ID-photo stance, both arms hanging symmetrically, frozen face, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, visible logos, image text, watermark, wrinkle-based age cues, numeric true-age labels.
"""


def write_job(project_root, run_dir, carousel_id, tool, version_tag=""):
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

    prompts = [prompt_for(packet, profile, ref, variant) for variant in ["A", "B", "C"]]
    (job_dir / "candidate_prompts.md").write_text("# Candidate Prompts\n\n" + "\n\n---\n\n".join(prompts), encoding="utf-8")

    handoff_lines = [
        f"# Codex Generation Handoff - {carousel_id} / {model_id}",
        "",
        "Use this file to generate the carousel image candidates inside Codex.",
        "",
        "## Reference Images",
        "",
        "Attach both approved reference start images to the image-generation request:",
        "",
        "```text",
        f"{ref['face_path']}",
        f"{ref['full_path']}",
        "```",
        "",
        "## Output Filenames",
        "",
        "Save generated candidates as:",
        "",
        "```text",
        f"{carousel_id}_{model_id}{f'_{version_tag}' if version_tag else ''}_candidate_A.png",
        f"{carousel_id}_{model_id}{f'_{version_tag}' if version_tag else ''}_candidate_B.png",
        f"{carousel_id}_{model_id}{f'_{version_tag}' if version_tag else ''}_candidate_C.png",
        "```",
        "",
        "## Candidate Prompts",
        "",
        "\n\n---\n\n".join(prompts),
        "",
        "## After Generation",
        "",
        "Update:",
        "",
        "```text",
        f"{job_dir / 'review_sheet.csv'}",
        "```",
    ]
    (job_dir / "codex_generation_handoff.md").write_text("\n".join(handoff_lines), encoding="utf-8")

    job_lines = [
        "# Mira Daily Image Job",
        "",
        f"- carousel_id: `{carousel_id}`",
        f"- model_profile_id: `{model_id}`",
        f"- reference_face_image: `{ref['face_path']}`",
        f"- reference_full_image: `{ref['full_path']}`",
        "- attach_reference_images: `required`",
        f"- trend: {packet.get('trend_name', '')}",
        f"- clothing_item: {packet.get('clothing_item', '')}",
        f"- occasion: {packet.get('occasion', '')}",
        "",
        "Generate 2-3 candidates, then score them before Canva.",
        "",
        "Codex handoff:",
        "",
        "```text",
        str(job_dir / "codex_generation_handoff.md"),
        "```",
    ]
    (job_dir / "image_job.md").write_text("\n".join(job_lines), encoding="utf-8")

    review_path = job_dir / "review_sheet.csv"
    rows = read_csv(review_path) if review_path.exists() else []
    existing_files = {clean(row.get("candidate_file")) for row in rows}
    for variant in ["A", "B", "C"]:
        file_name = f"{carousel_id}_{model_id}{f'_{version_tag}' if version_tag else ''}_candidate_{variant}.png"
        if file_name in existing_files:
            continue
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
    write_csv(review_path, REVIEW_FIELDS, rows)
    print(job_dir)


def main():
    parser = argparse.ArgumentParser(description="Prepare a strict Mira daily image generation job.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--carousel-id")
    parser.add_argument("--daily-id")
    parser.add_argument("--tool", default="Codex")
    parser.add_argument("--version-tag", default="", help="Optional filename tag such as v2 for a non-destructive regeneration.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    run_dir = (project_root / args.run_dir).resolve() if not Path(args.run_dir).is_absolute() else Path(args.run_dir)
    carousel_id = find_carousel_id(run_dir, carousel_id=args.carousel_id, daily_id=args.daily_id)
    write_job(project_root, run_dir, carousel_id, args.tool, version_tag=clean(args.version_tag))


if __name__ == "__main__":
    main()
