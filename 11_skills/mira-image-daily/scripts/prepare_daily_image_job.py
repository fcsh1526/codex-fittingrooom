import argparse
import csv
import json
from pathlib import Path


REVIEW_FIELDS = [
    "carousel_id",
    "look_id",
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


REEL_FRAME_TARGETS = {
    "A": {"slot_id": "reel_hero", "width": 1080, "height": 1920, "aspect_ratio": 0.5625, "composition": "vertical_hero"},
    "B": {"slot_id": "reel_motion", "width": 1080, "height": 1920, "aspect_ratio": 0.5625, "composition": "vertical_motion"},
    "C": {"slot_id": "reel_detail", "width": 1080, "height": 1920, "aspect_ratio": 0.5625, "composition": "vertical_detail"},
}


def clean(value):
    return " ".join((value or "").split()).strip()


def first_clause(value):
    value = clean(value)
    for separator in ["；", ";", "。", "."]:
        if separator in value:
            return value.split(separator, 1)[0].strip()
    return value


def dressing_decision_for(packet):
    explicit = clean(packet.get("dressing_decision"))
    if explicit:
        return explicit
    occasion = clean(packet.get("occasion")) or "daily wear"
    trend = clean(packet.get("trend_name")) or "the selected fashion direction"
    styling = first_clause(packet.get("styling_rules"))
    return f"{occasion} — {trend}" + (f": {styling}" if styling else "")


def visible_action_for(packet):
    explicit = clean(packet.get("visible_action"))
    if explicit:
        return explicit
    context = " ".join([clean(packet.get("occasion")), clean(packet.get("scene"))]).lower()
    if any(token in context for token in ["通勤", "上班", "office", "mrt", "捷運", "walkway", "騎樓"]):
        return "already mid-step toward her destination, looking ahead, with one hand naturally adjusting her bag or outer layer"
    if any(token in context for token in ["咖啡", "cafe", "早午餐"]):
        return "just setting down a coffee cup, looking toward the window, with her other hand resting naturally near her bag"
    if any(token in context for token in ["市集", "展覽", "shopping", "逛街", "旅行", "travel"]):
        return "walking and briefly looking toward her surroundings while naturally carrying her bag"
    return "walking naturally, looking away from the camera, with one believable hand interaction with her bag or clothing"


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


def find_look(run_dir, look_id):
    path = run_dir / "weekly_look_plan.csv"
    if not path.exists():
        raise SystemExit(f"weekly_look_plan.csv is missing; cannot resolve look_id: {look_id}")
    for row in read_csv(path):
        if clean(row.get("look_id")) == look_id:
            return row
    raise SystemExit(f"look_id not found in weekly_look_plan.csv: {look_id}")


def packet_for_look(packet, look):
    """Overlay one approved look on its parent theme packet."""
    carousel_id = clean(packet.get("carousel_id"))
    if clean(look.get("carousel_id")) != carousel_id:
        raise SystemExit(f"{look.get('look_id')}: look and parent carousel_id do not match.")
    packet_model = clean(packet.get("model_profile_id"))
    look_model = clean(look.get("model_profile_id"))
    if look_model and look_model != packet_model:
        raise SystemExit(
            f"{look.get('look_id')}: look model {look_model} does not match theme model {packet_model}."
        )

    merged = dict(packet)
    for field in [
        "opening_hook",
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
    ]:
        value = clean(look.get(field))
        if value:
            merged[field] = value
    merged["trend_name"] = clean(look.get("theme_name")) or clean(packet.get("trend_name"))
    merged["look_id"] = clean(look.get("look_id"))
    merged["look_name"] = clean(look.get("look_name"))
    merged["frame_plan"] = clean(look.get("frame_plan"))
    merged["required_frames"] = clean(look.get("required_frames")) or "2"
    return merged


def planned_variants(look, surface="carousel"):
    """Return the fixed asset roles for the requested delivery surface."""
    return ["A"] if surface == "reel" else ["A", "B", "C"]


def write_planning_stub(run_dir, look):
    carousel_id = clean(look.get("carousel_id"))
    look_id = clean(look.get("look_id"))
    job_root = run_dir / "generated_images" / carousel_id / "looks" / look_id
    job_root.mkdir(parents=True, exist_ok=True)
    variants = planned_variants(look, "carousel")
    lines = [
        "# Mira Look Image Job",
        "",
        f"- carousel_id: `{carousel_id}`",
        f"- look_id: `{look_id}`",
        f"- model_profile_id: `{clean(look.get('model_profile_id'))}`",
        f"- theme: {clean(look.get('theme_name'))}",
        f"- look_name: {clean(look.get('look_name'))}",
        f"- dressing_decision: {clean(look.get('dressing_decision'))}",
        f"- clothing_item: {clean(look.get('clothing_item'))}",
        f"- scene: {clean(look.get('scene'))}",
        f"- visible_action: {clean(look.get('visible_action'))}",
        f"- frame_plan: {clean(look.get('frame_plan'))}",
        f"- carousel_variants: `{', '.join(variants)}`",
        "- required_surface_jobs: `reel, carousel`",
        "- reel_plan: `A = native 9:16 full-person source`",
        "- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`",
        "- status: `waiting_for_both_surface_jobs`",
        "",
        "Run both surface jobs before marking the look asset-complete: "
        f"`prepare_daily_image_job.py --look-id {look_id} --surface reel`, then repeat with `--surface carousel`.",
        "Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.",
    ]
    (job_root / "look_plan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(job_root)
    return job_root


def find_carousel_id(run_dir, carousel_id=None, daily_id=None):
    if carousel_id:
        return carousel_id
    if not daily_id:
        raise SystemExit("Provide --look-id, --carousel-id or --daily-id.")
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


def prompt_for(packet, profile, reference, template, variant, surface):
    if surface == "reel":
        target = REEL_FRAME_TARGETS[variant]
        slot_id = target["slot_id"]
    else:
        slot_id = {"A": "cover_image", "B": "motion_crop", "C": "detail_image"}[variant]
        target = template["slot_geometry"][slot_id]
    target_width = int(target["width"])
    target_height = int(target["height"])
    target_ratio = float(target.get("aspect_ratio") or (target_width / target_height))
    composition = clean(target.get("composition"))
    decision = dressing_decision_for(packet)
    action = visible_action_for(packet)
    if surface == "reel":
        target_block = (
            "Composition: native 9:16 vertical frame for 1080x1920 delivery. "
            "Keep the full figure, complete hairstyle and both shoes visible with enough real environment to establish the location."
        )
    else:
        target_block = (
            f"Composition: create specifically for the v3-{template['key']} {slot_id} frame, "
            f"{target_width}x{target_height} ({target_ratio:.4f}:1), role {composition}. "
            "Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop."
        )

    if variant == "A":
        return f"""Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: {decision}.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at {packet.get('scene', '')}, for {packet.get('occasion', '')}. She is {action}. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: {packet.get('clothing_item', '')}. Palette: {packet.get('color_palette', '')}. Materials: {packet.get('fabric', '')}. Fit: {packet.get('fit', '')}. Styling direction: {packet.get('styling_rules', '')}. Do not add or substitute garments.

Visual proof to preserve: {packet.get('visual_proof', '')}. Practical styling rule: {packet.get('practical_rule', '')}.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

{target_block}

No readable text, logos or watermark. Avoid studio polish and catalog posing.
"""

    if variant == "B":
        edit_direction = (
            "Create the Carousel scene-application frame for the same complete outfit, not the next moment in a continuous action. "
            "Show how the outfit works in the intended occasion through a different corner or wider environmental view of the location, "
            "or another believable setting for the same occasion. Keep the styling readable while giving the place a clear editorial role."
        )
        continuity_rule = (
            "Preserve the same woman, exact garments and styling placement, body build, season, color treatment and documentary camera character. "
            "If the location changes, rebuild its available light and contact shadows naturally instead of copying the Hero background lighting."
        )
    else:
        edit_direction = (
            "Create the Carousel accessory-detail frame. Move closer to the one accessory that carries the styling decision, such as the bag, shoes, scarf, belt or jewelry, "
            "while retaining enough garment context to understand how it works with the outfit. Use a physically simple pose; do not invent a difficult grip or make fingers the focal point."
        )
        continuity_rule = (
            "Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism."
        )
    return f"""Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

{edit_direction} {continuity_rule} Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

{target_block}

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.
"""


def write_job(project_root, run_dir, carousel_id, tool, version_tag="", surface="carousel", look=None):
    roster = load_roster(project_root)
    packet = find_packet(run_dir, carousel_id)
    if look:
        packet = packet_for_look(packet, look)
    look_id = clean(packet.get("look_id"))
    model_id = clean(packet.get("model_profile_id"))
    profile = roster.get(model_id)
    if not profile:
        raise SystemExit(f"Unknown model_profile_id: {model_id}")
    ref = reference_status(project_root, model_id)
    if not ref["ok"]:
        raise SystemExit(ref["message"])

    base_job_dir = run_dir / "generated_images" / carousel_id
    if look_id:
        job_dir = base_job_dir / "looks" / look_id / surface
    else:
        job_dir = base_job_dir / "reel" if surface == "reel" else base_job_dir
    job_dir.mkdir(parents=True, exist_ok=True)

    variants = planned_variants(look, surface)

    template = None if surface == "reel" else template_for_packet(project_root, packet)
    prompts_by_variant = {
        variant: prompt_for(packet, profile, ref, template, variant, surface)
        for variant in variants
    }
    prompts = [prompts_by_variant[variant] for variant in variants]
    sequence_note = (
        "Generate and review the native 9:16 full-person Reel A. This look also needs a reviewed styling-proof view; reuse suitable material or generate the missing view. Each weekly Reel keeps one model and its two looks."
        if surface == "reel"
        else "Generate and review Carousel Hero A first. After A is accepted, create B Scene Application and C Accessory Detail from the same identity and exact outfit lock. These are required publishing assets, not A/B tests."
    )
    (job_dir / "hero_A_prompt.md").write_text(
        "# Hero A Production Prompt\n\n" + sequence_note + "\n\n```text\n" + prompts_by_variant["A"] + "```\n",
        encoding="utf-8",
    )
    derivative_text = (
        "# Carousel Derivative Edit Prompt Templates\n\n"
        "Use both templates only after Carousel Hero A is accepted.\n\n"
        "## B Scene Application\n\n```text\n"
        + prompts_by_variant["B"]
        + "```\n\n## C Accessory Detail\n\n```text\n"
        + prompts_by_variant["C"]
        + "```\n"
        if surface == "carousel"
        else "# Reel Styling-Proof View\n\nSelect one vertical, clear view that demonstrates this look's dressing decision. Reuse reviewed imagery only when framing and resolution are adequate; otherwise derive a dedicated proof view from accepted Reel A with the same identity, wardrobe and lighting. Keep original A unchanged. Link full/proof assets in reels/production_manifest.json.\n"
    )
    (job_dir / "derivative_edit_prompt_templates.md").write_text(derivative_text, encoding="utf-8")
    (job_dir / "candidate_prompts.md").write_text(
        "# Production Prompts (compatibility file)\n\n"
        + sequence_note
        + "\n\n---\n\n".join(["", *prompts]),
        encoding="utf-8",
    )

    asset_id = look_id or carousel_id
    if look_id:
        file_stem = f"{asset_id}_{model_id}_{surface}{f'_{version_tag}' if version_tag else ''}"
    else:
        file_stem = f"{asset_id}_{model_id}{'_reel' if surface == 'reel' else ''}{f'_{version_tag}' if version_tag else ''}"
    handoff_lines = [
        f"# Codex Generation Handoff - {asset_id} / {model_id}",
        "",
        f"Use this file to generate the {surface} image candidates inside Codex.",
        "",
        "## Reference Images",
        "",
        "For Hero A, attach the approved references in this order: Image 1 = face/hairstyle identity; Image 2 = loose body proportion.",
        "",
        "```text",
        f"{ref['face_path']}",
        f"{ref['full_path']}",
        "```",
        "",
        (
            "For required Carousel B/C edits after Hero approval: Image 1 = accepted Carousel Hero A; Image 2 = face/hairstyle identity; Image 3 = loose body proportion."
            if surface == "carousel"
            else "After accepted Reel A, review a vertical styling-proof view; reuse a clear approved source or generate the missing view. Each Reel combines this model's two weekly looks."
        ),
        "",
        "## Output Filenames",
        "",
        "Save generated candidates as:",
        "",
        "```text",
        *[f"{file_stem}_candidate_{variant}.png" for variant in variants],
        "```",
        "",
        "## Candidate Prompts",
        "",
        sequence_note,
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

    if surface == "reel":
        reel_targets = {
            "carousel_id": carousel_id,
            "look_id": look_id,
            "model_profile_id": model_id,
            "delivery_surface": "reel",
            "direct_generation_required": True,
            "canva_crop_limit_applies": False,
            "frames": {variant: REEL_FRAME_TARGETS[variant] for variant in variants},
        }
        (job_dir / "reel_frame_targets.json").write_text(
            json.dumps(reel_targets, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        slot_targets = {
            "carousel_id": carousel_id,
            "look_id": look_id,
            "model_profile_id": model_id,
            "delivery_surface": "carousel",
            "canva_template_key": template["key"],
            "canva_template_name": template["name"],
            "canva_design_id": template["design_id"],
            "canva_crop_limit": 0.15,
            "slots": {
                variant: {"slot_id": slot_id, **template["slot_geometry"][slot_id]}
                for variant, slot_id in {"A": "cover_image", "B": "motion_crop", "C": "detail_image"}.items()
            },
        }
        (job_dir / "canva_slot_targets.json").write_text(
            json.dumps(slot_targets, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    job_lines = [
        "# Mira Daily Image Job",
        "",
        f"- carousel_id: `{carousel_id}`",
        f"- look_id: `{look_id or 'legacy_theme_job'}`",
        f"- look_name: {packet.get('look_name', '')}",
        f"- model_profile_id: `{model_id}`",
        f"- delivery_surface: `{surface}`",
        f"- reference_face_image: `{ref['face_path']}`",
        f"- reference_full_image: `{ref['full_path']}`",
        "- attach_reference_images: `required`",
        f"- trend: {packet.get('trend_name', '')}",
        f"- clothing_item: {packet.get('clothing_item', '')}",
        f"- occasion: {packet.get('occasion', '')}",
        f"- frame_plan: {packet.get('frame_plan', '')}",
        f"- required_frames: {packet.get('required_frames', '')}",
        *(
            ["- direct_reel_frame: `1080x1920` / `9:16`", "- reel_frame_targets: `reel_frame_targets.json`", "- canva_crop_limit_applies: `no`"]
            if surface == "reel"
            else [f"- canva_template: `v3-{template['key']}` / {template['name']}", "- canva_slot_targets: `canva_slot_targets.json`", "- canva_crop_limit: `15%`"]
        ),
        "",
        (
            "Generate and review the native 9:16 full-person Reel A; it is the only still required for this surface."
            if surface == "reel"
            else "Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required."
        ),
        "Do not reuse one surface's crop as the other surface's source.",
        "Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.",
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
        row["look_id"] = look_id
        row["prompt_id"] = look_id or clean(packet.get("prompt_id"))
        row["model_profile_id"] = model_id
        row["tool"] = clean(row.get("tool")) or tool
    existing_files = {clean(row.get("candidate_file")) for row in rows}
    for variant in variants:
        file_name = f"{file_stem}_candidate_{variant}.png"
        if file_name in existing_files:
            continue
        rows.append(
            {
                "carousel_id": carousel_id,
                "look_id": look_id,
                "prompt_id": look_id or clean(packet.get("prompt_id")),
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
    parser.add_argument("--look-id", help="Approved look_id from weekly_look_plan.csv. Overrides --carousel-id/--daily-id.")
    parser.add_argument("--tool", default="Codex")
    parser.add_argument("--version-tag", default="", help="Optional filename tag such as v2 for a non-destructive regeneration.")
    parser.add_argument("--plan-only", action="store_true", help="Create a look planning stub without choosing a delivery surface or composing prompts.")
    parser.add_argument("--surface", choices=["carousel", "reel"], help="Delivery surface. Required unless --plan-only is used.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    run_dir = (project_root / args.run_dir).resolve() if not Path(args.run_dir).is_absolute() else Path(args.run_dir)
    look = find_look(run_dir, clean(args.look_id)) if clean(args.look_id) else None
    if args.plan_only:
        if not look:
            raise SystemExit("--plan-only requires --look-id.")
        write_planning_stub(run_dir, look)
        return
    if not args.surface:
        raise SystemExit("Choose --surface carousel or --surface reel. Run both surface jobs before marking the look asset-complete.")
    carousel_id = (
        clean(look.get("carousel_id"))
        if look
        else find_carousel_id(run_dir, carousel_id=args.carousel_id, daily_id=args.daily_id)
    )
    write_job(
        project_root,
        run_dir,
        carousel_id,
        args.tool,
        version_tag=clean(args.version_tag),
        surface=args.surface,
        look=look,
    )


if __name__ == "__main__":
    main()
