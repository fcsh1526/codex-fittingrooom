"""Persist actual rejected still-generation results; never grants approval."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import json
import native_pair_tools as native

ROOT, HERE = native.ROOT, native.HERE
assets = ROOT / "10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/front_opening_matched_start_v1"
before = native.protected_inputs()
face = ROOT / "02_brand/reference_models/M02_start_v3_face.png"
full = ROOT / "02_brand/reference_models/M02_start_v3_full.png"
a = HERE / "QA_join_A126_B0_2026-10-08/native_pairs/A_000116.png"
b = ROOT / "10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/paired_scene_v1/2026-W37-001-L02_M02_reel_proof_candidate_v1.png"
v1 = assets / "2026-W37-001-L02_M02_front_opening_matched_start_candidate_v1.png"
v2 = assets / "2026-W37-001-L02_M02_front_opening_matched_start_candidate_v2.png"

def ref(path, role):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": native.digest(path), "role": role}

rows = []
for variant, target, inputs, prompt, elapsed, original in (
    ("v1", v1, [ref(a, "actual_A_f116_composition_edit_canvas"), ref(b, "approved_L02_wardrobe_only"), ref(face, "approved_v3_identity"), ref(full, "approved_v3_proportions")], "prompt.txt", None, "exec-7c312a3c-2b99-491e-abb3-3906a5fb705e.png"),
    ("v2", v2, [ref(v1, "v1_edit_canvas_preserve_L02_wardrobe"), ref(a, "authoritative_actual_A_f116_composition"), ref(face, "approved_v3_identity"), ref(full, "approved_v3_proportions")], "targeted_edit_prompt_v2.txt", 47.736, "exec-139b6138-eda0-4a1c-90f3-9117cc2d0624.png"),
):
    with native.Image.open(target) as im:
        size = list(im.size)
    value = {
        "date": "2026-10-08", "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": "M02", "look_id": "2026-W37-001-L02", "method": "built_in_image_gen",
        "status": "rejected_for_matched_start_continuity_purpose", "asset": ref(target, "new_research_still"),
        "actual_size": size, "requested_format": "native portrait 9:16", "post_generation_delivery_transform": "none",
        "generation_count_cumulative": 1 if variant == "v1" else 2,
        "base_generations": 1, "targeted_edits_cumulative": 0 if variant == "v1" else 1,
        "prompt_file": prompt, "inputs_in_tool_order": inputs,
        "original_generated_filename_preserved": original,
        "measured_tool_call_elapsed_seconds": elapsed, "active_production_seconds": None,
        "timing_limit": "Tool-call elapsed includes image-generation wait; active production time was not measured. v1 exact elapsed not retained in this receipt.",
        "root_static_review": "Wardrobe, grey tote/strap and visible stud broadly preserved. Matching A f116 is unsuccessful: native-canvas QA blend retains separated eye/mouth features. v2 changes mouth/shoulder details but not enough of head projection/location.",
        "root_QA_boards_reviewed": ["QA/head_comparison.jpg", "QA/half_blend_head.jpg", "QA/full_comparison.jpg"] if variant == "v1" else ["QA_v2/half_blend_head.jpg"],
        "independent_review": "independent_static_review.md" if variant == "v1" else "independent_static_review_v2.md",
        "user_visual_approval": None, "submitted_for_user_approval": False,
        "uploaded_to_Grok": False, "motion_generated_from_this_still": False,
        "publishable": False, "text": "none", "original_assets_overwritten": False,
        "further_targeted_edits_planned": False,
        "limit": "A single half-blend is a static continuity diagnostic; no dynamic 18-frame join or complete-film pass is inferred.",
    }
    native.json_new(assets / f"generation_receipt_{variant}.json", value)
    rows.append({"filename": target.name, "publishable": "no", "status": value["status"], "notes": value["root_static_review"]})

fields = "filename,model_consistency,body_proportion_consistency,reader_relatability,outfit_clarity,ai_realism,commerce_value,scene_lighting_integration,outfit_continuity,expression_liveliness,pose_variation,canva_frame_fit,publishable,status,notes".split(",")
with (assets / "review_sheet.csv").open("x", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

story_path = HERE / "execution_storyboard.json"
story = native.read_json(story_path)
story["new_stills"] = 2
story["new_still_requirement_count"] = 1
story["new_still_generation"] = {"base_count": 1, "targeted_edit_count": 1, "selected": None, "status": "both_rejected_for_continuity_purpose", "folder": assets.relative_to(ROOT).as_posix(), "Grok_submitted": False, "user_approval": None}
story["native_join_second"]["result"] = "rejected"
story["native_join_second"]["reason"] = "Independent all18-pair/16-boundary QA finds clear separated eye and mouth features in central five overlaps."
story["native_join_third"] = {"first_role": "B", "second_role": "A", "first": [108,126], "second": [0,18], "seconds": 0.75, "result": "pending", "purpose": "One reordered deep-to-light gesture comparison using actual relaxed B ending and A beginning; no source reversal or speed change."}
with story_path.open("w", encoding="utf-8") as stream:
    json.dump(story, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
after = native.protected_inputs()
if after != before:
    raise ValueError("Protected input records unexpectedly changed")
native.json_new(assets / "protected_inputs_after_generation.json", {"date": "2026-10-08", "verified_inputs": after, "all_hashes_match": True, "user_approval": None})
print(json.dumps({"still_results": "two_continuity_rejections_recorded", "protected_inputs": len(after), "further_edits": False}))
