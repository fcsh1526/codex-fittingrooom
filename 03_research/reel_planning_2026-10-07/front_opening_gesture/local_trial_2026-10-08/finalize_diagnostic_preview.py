"""Save a diagnostic preview with known residuals, never a visual pass."""
from datetime import datetime, timezone
import json
import native_pair_tools as native

HERE, ROOT = native.HERE, native.ROOT
folder = HERE / "review_deep_to_light_v1"
movie = folder / "M02_front_opening_deep_to_light_review_v1.mp4"
receipt_path = folder / "M02_front_opening_deep_to_light_review_v1_receipt.json"
receipt = native.read_json(receipt_path)
if receipt["output_sha256"] != native.digest(movie):
    raise ValueError("Encoded diagnostic differs from saved receipt")
streams = native.read_json(folder / "actual_streams.json")
if streams["audio_stream_count"] != 0:
    raise ValueError("Unexpected diagnostic audio")
protected = native.protected_inputs()
root_review = {
    "date": "2026-10-08", "status": "diagnostic_preview_with_known_transition_residuals_pending_user_playback",
    "output_sha256": native.digest(movie),
    "actual": {"size": [720,1280], "fps": 24, "frames": 204, "seconds": 8.5, "audio_streams": 0},
    "look_order": ["2026-W37-001-L02", "2026-W37-001-L01"],
    "selection": [{"original_role": "B", "look_id": "2026-W37-001-L02", "frames_half_open": [24,126]}, {"original_role": "A", "look_id": "2026-W37-001-L01", "frames_half_open": [0,120]}],
    "root_reviewed": {"output_full_samples": 25, "output_head_samples": 5, "output_transition_and_boundary_frames": 34, "pre_encode_native_pairs": 18, "pre_encode_pure_boundary_frames": 16, "native_half_blend_full": "QA_join_B126_A0_2026-10-08/native_pairs/blend_output_000092.png"},
    "finding": "Deep-to-light order has closer eye/head placement than the rejected light-to-deep joins. The central dissolve still has visible eyebrow/eye-edge, mouth-corner, cheek/hair and hand/bag/background double outlines; not a clean no-ghost pass. No major new discontinuity identified in inspected pure-output checkpoints.",
    "decision": "Present a clearly labelled isolated diagnostic for normal-speed user comfort review; do not label accepted, ready or publishable. Source actions and native timing remain unchanged.",
    "independent_native_join_review": "../QA_join_B126_A0_2026-10-08/independent_review.md",
    "independent_encoded_output_review": "independent_output_review.md",
    "continuous_normal_speed_assistant_review": False, "clean_transition_QA_pass": False,
    "user_video_approval": None, "publishable": False,
    "retime_freeze_reverse_replay": False, "framing_transform": "none", "text": "none",
    "formal_full_outfit_delivery": False, "first_wave_modified": False,
    "cloud_task_messaged": False, "drive_write": False, "instagram_publication": False, "github_push": False,
}
native.json_new(folder / "root_output_review.json", root_review)
receipt["status"] = root_review["status"]
receipt["composition_role_mapping"] = {"compositor_A": "original_B_L02_first", "compositor_B": "original_A_L01_second"}
receipt["look_order"] = root_review["look_order"]
receipt["combined_sampled_dynamic_qa"] = "known_transition_residuals; no_clean_transition_pass"
receipt["actual_audio_stream_count"] = 0
receipt["root_review"] = "root_output_review.json"
with receipt_path.open("w", encoding="utf-8") as stream:
    json.dump(receipt, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
story_path = HERE / "execution_storyboard.json"
story = native.read_json(story_path)
story["native_join_third"]["result"] = "diagnostic_with_known_residuals_not_clean_QA_pass"
story["native_join_third"]["reason"] = "Closer overall eye/head placement; still visible eyebrow/eye, mouth-corner, cheek/hair outlines in central overlap. Normal-speed user comfort pending."
story["actual_selection_and_output"] = {"path": movie.relative_to(ROOT).as_posix(), "sha256": native.digest(movie), "size": [720,1280], "fps": 24, "frames": 204, "seconds": 8.5, "look_order": root_review["look_order"], "selection": root_review["selection"], "status": root_review["status"], "user_approval": None, "publishable": False}
with story_path.open("w", encoding="utf-8") as stream:
    json.dump(story, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
summary = {"date": "2026-10-08", "recorded_at_utc": datetime.now(timezone.utc).isoformat(), "environment": "user_local_in_app_browser", "human_verification": "user_replied_completed", "new_motion_sources": [{"role": "distance_matched_B", "path": "03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/matched_B_attempt_01/source.mp4", "sha256": "ee829f278e30de0a0e0db1d8aa8bc11d258c50a8475044d5320e1cdae07673c8"}, {"role": "gesture_A", "path": (HERE / "A_attempt_01/source.mp4").relative_to(ROOT).as_posix(), "sha256": "5baaa223b437e6fde482545cc64a0d2b8c85dffec14df6397735b71c7e0b7d49"}, {"role": "gesture_B", "path": (HERE / "B_attempt_01/source.mp4").relative_to(ROOT).as_posix(), "sha256": "25b8bd59b95c46dcef8c30ca9847ca4fcdc892581899aea0f804c8375d388a54"}], "distance_native_joins_rejected": 3, "gesture_light_to_deep_joins_rejected": 2, "new_still_generations": {"base": 1, "targeted_edit": 1, "both_continuity_purpose_rejected": True, "Grok_submitted": False}, "new_composite": story["actual_selection_and_output"], "protected_inputs_verified": protected, "first_wave_modified": False, "cloud_packet_modified": False, "cloud_task_messaged": False, "Drive_write": False, "Instagram_publication": False, "GitHub_push": False, "user_video_approval": None, "audience_performance": None, "next_gate": "User normal-speed full diagnostic playback and transition/gesture judgement; no additional automatic generation queued."}
for source in summary["new_motion_sources"]:
    native.verified_source(ROOT / source["path"], source["sha256"])
native.json_new(ROOT / "03_research/local_resume_2026-10-08/execution_receipt.json", summary)
print(json.dumps({"output_sha256": native.digest(movie), "status": root_review["status"], "protected_inputs_match": len(protected)}))
