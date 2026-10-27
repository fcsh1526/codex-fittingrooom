"""Record exact user picture acceptance without changing any media bytes."""
from datetime import datetime, timezone
from pathlib import Path
import json
import native_pair_tools as native

HERE, ROOT = native.HERE, native.ROOT
review = HERE / "review_deep_to_light_v1"
movie = review / "M02_front_opening_deep_to_light_review_v1.mp4"
expected = "568515694b7078f566a967c681aec5bd28d03d78d2038f2f2e7092fbab847df2"
native.verified_source(movie, expected)
protected = native.protected_inputs()
receipt_path = review / "M02_front_opening_deep_to_light_review_v1_receipt.json"
root_path = review / "root_output_review.json"
story_path = HERE / "execution_storyboard.json"
resume_path = ROOT / "03_research/local_resume_2026-10-08/execution_receipt.json"
receipt, root_review, story, resume = [native.read_json(p) for p in (receipt_path, root_path, story_path, resume_path)]
for record in (receipt, root_review):
    if record["output_sha256"] != expected:
        raise ValueError("Approval target differs from production record")
for record in (story["actual_selection_and_output"], resume["new_composite"]):
    if record["sha256"] != expected:
        raise ValueError("Approval target differs from storyboard/resume record")

approval_path = review / "user_picture_approval_2026-10-08.json"
status = "user_picture_accepted_with_dissolve_residuals"
approval = {
    "date": "2026-10-08", "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    "status": "accepted_as_research_picture_track", "model": "M02",
    "asset": movie.relative_to(ROOT).as_posix(), "sha256": expected,
    "seconds": 8.5, "frames": 204, "fps": 24, "size": [720,1280],
    "user_quote_verbatim": "這個很好，尤其重影更寫得專業影像編輯與柔化眼睛的感受",
    "context": "Direct favorable reply to the exact embedded8.5s deep-to-light preview and its transition-comfort question.",
    "approved_scope": "Exact research picture track and its soft0.75s dissolve; user explicitly values the visible overlap/softened visual feeling.",
    "editorial_inference": "Brief dissolve double outlines may contribute to the intended soft transition. Judge future joins by normal playback comfort, continuity and clothing readability, retaining single-source integrity checks.",
    "user_full_duration_normal_speed_self_report": None,
    "assistant_continuous_visual_review": False,
    "zero_ghost_technical_pass_inferred": False,
    "account_wide_fixed_format_adopted": False,
    "formal_full_outfit_delivery": False, "audience_performance": None,
    "new_rejected_stills_approved": False,
    "actions_and_speed": "unchanged", "transition_seconds": 0.75, "text": "none", "audio": "none",
    "media_modified": False, "first_wave_replacement_authorized": False,
    "Drive_write": False, "Instagram_publication": False, "GitHub_push": False,
}
native.json_new(approval_path, approval)
approval_ref = {"date": "2026-10-08", "status": approval["status"], "receipt": approval_path.relative_to(ROOT).as_posix(), "sha256": expected}

root_review["decision_before_user_approval"] = root_review["decision"]
root_review["decision"] = "Exact research picture accepted by user, explicitly valuing the dissolve's overlap and softened viewing feeling; preserve source speed/actions and media bytes."
root_review["status"] = status
root_review["user_video_approval"] = approval_ref
root_review["clean_transition_QA_pass_scope"] = "Historical no-visible-ghost diagnostic criterion remains unmet; separate from the user's positive aesthetic acceptance."
receipt["status"] = status
receipt["pre_approval_combined_sampled_dynamic_qa"] = receipt["combined_sampled_dynamic_qa"]
receipt["combined_sampled_dynamic_qa"] = "limited sample review preserved; known dissolve double outlines positively accepted by user"
receipt["combined_continuous_review"] = "assistant not performed; user full-duration normal-speed self-report unavailable"
receipt["user_video_approval"] = approval_ref
story["user_video_approval"] = approval_ref
story["native_join_third"]["pre_approval_result"] = story["native_join_third"]["result"]
story["native_join_third"]["result"] = "user_accepted_dissolve_residuals_for_exact_research_cut"
story["native_join_third"]["user_feedback"] = approval["user_quote_verbatim"]
story["actual_selection_and_output"]["status"] = status
story["actual_selection_and_output"]["user_approval"] = approval_ref
resume["user_video_approval"] = approval_ref
resume["new_composite"]["status"] = status
resume["new_composite"]["user_approval"] = approval_ref
resume["next_gate"] = "Exact research picture accepted; preserve it as a soft-transition reference. Future storyboard and any separate delivery/publication remain their own decisions."

for path, value in ((receipt_path, receipt), (root_path, root_review), (story_path, story), (resume_path, resume)):
    with path.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
native.verified_source(movie, expected)
if native.protected_inputs() != protected:
    raise ValueError("Protected media unexpectedly changed")
print(json.dumps({"status": status, "output_sha256": expected, "media_bytes_unchanged": True, "protected_input_hashes_verified": len(protected)}))
