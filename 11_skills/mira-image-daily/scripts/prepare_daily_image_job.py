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
    "body_proportion_consistency",
    "reader_relatability",
    "outfit_clarity",
    "ai_realism",
    "scene_lighting_integration",
    "outfit_continuity",
    "expression_liveliness",
    "pose_variation",
    "canva_frame_fit",
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


def load_template_registry(project_root):
    path = project_root / "10_automation" / "canva_template_registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        clean(row.get("key")).upper(): row
        for row in data.get("templates", [])
        if clean(row.get("key"))
    }


def template_for_packet(project_root, packet):
    templates = load_template_registry(project_root)
    key = clean(packet.get("canva_template_key")).upper() or "A"
    template = templates.get(key)
    if not template:
        raise SystemExit(f"Unknown or missing Canva template key: {key}")
    required = {"cover_image", "motion_crop", "detail_image"}
    missing = sorted(required - set(template.get("slot_geometry", {})))
    if missing:
        raise SystemExit(f"Canva template v3-{key} is missing slot geometry: {', '.join(missing)}")
    return template


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


def prompt_for(packet, profile, reference, template, variant):
    slot_id = {"A": "cover_image", "B": "motion_crop", "C": "detail_image"}[variant]
    target = template["slot_geometry"][slot_id]
    target_width = int(target["width"])
    target_height = int(target["height"])
    target_ratio = float(target.get("aspect_ratio") or (target_width / target_height))
    composition = clean(target.get("composition"))
    asset_role = {
        "A": "integrated-scene Hero and session lock",
        "B": "movement variation edited from the accepted Hero A",
        "C": "outfit-detail variation edited from the accepted Hero A",
    }[variant]
    direction = {
        "A": (
            "Show the full figure with surrounding environment. Use a relaxed asymmetric stance and one physically believable "
            "interaction with a foreground or scene object, including visible contact pressure and contact shadow."
        ),
        "B": (
            "Edit accepted Hero A into a candid three-quarter turn or small lateral movement. Change gaze and one hand action, "
            "but keep the same scene, outfit construction, identity, body build, light source, and camera treatment."
        ),
        "C": (
            "Edit accepted Hero A into a knees-up or waist-up outfit-detail composition. Preserve the exact neckline, layers, "
            "sleeves, fabric behavior, accessories, identity, scene, and lighting treatment."
        ),
    }[variant]
    if composition == "horizontal_motion":
        direction += (
            " Use a deliberately horizontal environmental composition with a readable face and torso/outfit gesture; "
            "do not squeeze a full standing figure into the shallow frame."
        )
    elif composition == "portrait_motion":
        direction += (
            " Use a vertical three-quarter or full-body movement composition with complete hair and plausible floor contact."
        )
    session_input = (
        "Accepted Hero A is created in this step."
        if variant == "A"
        else "Attach accepted Hero A as the edit target/session lock in addition to both model anchors. Do not generate an independent reinterpretation."
    )
    return f"""Asset {variant}: {asset_role}

Required image inputs:
- Face identity anchor: {reference['face_path']}
- Full-body proportion anchor: {reference['full_path']}
- Session rule: {session_input}

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model {packet['model_profile_id']} is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: {packet.get('trend_name', '')}
- Garments: {packet.get('clothing_item', '')}
- Palette: {packet.get('color_palette', '')}
- Fabric: {packet.get('fabric', '')}
- Fit: {packet.get('fit', '')}
- Occasion: {packet.get('occasion', '')}
- Styling: {packet.get('styling_rules', '')}

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: {packet.get('scene', '')}. Treat person and environment as one exposure captured in-camera with a normal 50mm full-frame-equivalent lens near chest height and a level optical axis. One visible or inferable light source must affect face, hair, garments, hands, shoes, foreground, floor, and background consistently. Include ambient color spill, natural contact shadows, shared depth of field, restrained grain, slight optical softness, natural skin texture, flyaway hairs, and small fabric wrinkles.

Canva frame target:
- Assigned master: v3-{template['key']} / {template['name']}
- Slot: {slot_id}
- Exact frame: {target_width} x {target_height} px
- Required width:height ratio: {target_ratio:.4f}:1
- Composition role: {composition}
Compose specifically for this frame ratio; do not reuse one narrow portrait composition for all A/B/C slots. Keep the entire hairstyle and head below an 8% top safe margin whenever the head appears. Keep the face and outfit focus inside the central 70%. For full-body views, leave real scene space above the hair and below the feet. No borders or letterboxing. The untouched Canva frame fill must remain publishable without manual focal-point adjustment.

Asset direction:
{direction}

Age rendering:
{chr(10).join(AGE_RENDERING_RULES)}

Avoid:
tiny head, fashion-elongated body, raised crotch, stretched legs, low or wide camera angle, mannequin posture, floating hands or feet, independent subject lighting, cutout edges, halo, plastic skin, plastic fabric, garment drift, celebrity likeness, sexualized or childlike styling, text, logos, and watermark.
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

    template = template_for_packet(project_root, packet)
    prompts = [prompt_for(packet, profile, ref, template, variant) for variant in ["A", "B", "C"]]
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

    slot_targets = {
        "carousel_id": carousel_id,
        "model_profile_id": model_id,
        "canva_template_key": template["key"],
        "canva_template_name": template["name"],
        "canva_design_id": template["design_id"],
        "slots": {
            variant: {
                "slot_id": slot_id,
                **template["slot_geometry"][slot_id],
            }
            for variant, slot_id in {"A": "cover_image", "B": "motion_crop", "C": "detail_image"}.items()
        },
    }
    (job_dir / "canva_slot_targets.json").write_text(
        json.dumps(slot_targets, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

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
        f"- canva_template: `v3-{template['key']}` / {template['name']}",
        "- canva_slot_targets: `canva_slot_targets.json`",
        "",
        "Generate and review Hero A first. After A passes, derive B Motion and C Detail from accepted A, then score the set before Canva.",
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
    for row in rows:
        row["carousel_id"] = carousel_id
        row["prompt_id"] = clean(packet.get("prompt_id"))
        row["model_profile_id"] = model_id
        row["tool"] = clean(row.get("tool")) or tool
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
