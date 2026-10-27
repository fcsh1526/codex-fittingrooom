"""Existing-source reorder/dwell trial only; no new motion or camera claim.

Creates five_look_review_v2_refined once; preserves the original v2 trial. Does not update shared project state, replace
publishing files, or infer that viewer-purpose and pacing feedback is resolved.
"""
from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / "10_automation").is_dir())
HELPER = ROOT / "03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py"
spec = importlib.util.spec_from_file_location("inspiration_v2_refined_native_primitives", HELPER)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
from PIL import Image

FPS, OVERLAP, TOTAL = 24, 18, 474
SELECTION = [("S04", 72, 180), ("S01", 120, 234), ("S05", 84, 192),
             ("S02", 84, 180), ("S03", 72, 192)]
V1_SHA = "ccbbe61977fc61c7850ec994018411f5d5a463209916bd46a18ab5387e38c345"
PAIR_SHA = "d25ad7a1ecdc7fc9dcafa18295aa201e1e7ca466e09e763d7553bc943efacc8b"
V2_SHA = "05cf662b8b6190d7318a298c596dca9df96c7e926df6256f1cb788d63e806839"


def relative(path):
    return path.relative_to(ROOT).as_posix()


def verify_protected(records):
    for path, digest in records.items():
        if native.digest(path) != digest:
            raise ValueError(f"Protected file changed: {path}")


def mapping_row(number, contributors, join=None):
    return {"output_frame": number, "join": join,
            "sources": [{"shot": shot, "native_frame": frame, "alpha": alpha}
                        for shot, frame, alpha in contributors]}


def plan_mapping():
    mapping, joins = [], []
    for index, (shot, start, end) in enumerate(SELECTION):
        pure_start = start + (OVERLAP if index else 0)
        pure_end = end - (OVERLAP if index < len(SELECTION) - 1 else 0)
        for frame in range(pure_start, pure_end):
            mapping.append(mapping_row(len(mapping), [(shot, frame, 1)]))
        if index < len(SELECTION) - 1:
            next_shot, next_start, _ = SELECTION[index + 1]
            join = f"J{index + 1}{index + 2}_{shot}_{next_shot}"
            begin = len(mapping)
            for offset in range(OVERLAP):
                alpha = (offset + 1) / OVERLAP
                mapping.append(mapping_row(len(mapping), [
                    (shot, end - OVERLAP + offset, 1 - alpha),
                    (next_shot, next_start + offset, alpha)], join))
            joins.append({"join": join, "from_shot": shot, "to_shot": next_shot,
                          "type": "linear_cross_dissolve", "frames": OVERLAP,
                          "seconds": OVERLAP / FPS,
                          "output_frames_half_open": [begin, len(mapping)],
                          "output_seconds_half_open": [begin / FPS, len(mapping) / FPS],
                          "new_shot_alpha": "(index+1)/18", "sampled_visual_review": "pending",
                          "user_join_approval": None})
    if len(mapping) != TOTAL:
        raise ValueError(f"Incorrect planned length: {len(mapping)}")
    return mapping, joins


def streamed_frames(sources):
    tail = []
    try:
        for index, (source, selection) in enumerate(zip(sources, SELECTION)):
            _, start, end = selection
            stream = native.selected_frames(source, start, end)
            try:
                consumed = 0
                if index:
                    if len(tail) != OVERLAP:
                        raise ValueError("Previous segment lacks exactly 18 tail frames")
                    for offset in range(OVERLAP):
                        incoming = next(stream)
                        previous = tail[offset]
                        blended = Image.blend(previous, incoming, (offset + 1) / OVERLAP)
                        previous.close()
                        incoming.close()
                        tail[offset] = None
                        consumed += 1
                        yield blended
                    tail = []
                visible_end = end - start - (OVERLAP if index < len(sources) - 1 else 0)
                for _ in range(consumed, visible_end):
                    yield next(stream)
                if index < len(sources) - 1:
                    tail = [next(stream) for _ in range(OVERLAP)]
                try:
                    next(stream)
                except StopIteration:
                    pass
                else:
                    raise ValueError("Selected reader exceeded interval")
            finally:
                stream.close()
    finally:
        for image in tail:
            if image is not None:
                image.close()


def build():
    output = HERE / "five_look_review_v2_refined"
    if output.resolve().parent != HERE or os.path.lexists(output):
        raise FileExistsError(f"Preserve existing v2 artifacts: {output}")
    v1_receipt_path = HERE / "five_look_review_v1/edit_receipt.json"
    v1 = native.read_json(v1_receipt_path)
    pair_receipt_path = HERE / "first_pair_review_v1/edit_receipt.json"
    pair = native.read_json(pair_receipt_path)
    v1_video = ROOT / v1["output"]
    pair_video = ROOT / pair["output"]
    if v1.get("sha256") != V1_SHA or pair.get("sha256") != PAIR_SHA:
        raise ValueError("Historical receipt identity differs from the expected pilot")
    v2_receipt_path = HERE / "five_look_review_v2/edit_receipt.json"
    v2 = native.read_json(v2_receipt_path)
    v2_video = ROOT / v2["output"]
    if v2.get("sha256") != V2_SHA or native.digest(v2_video) != V2_SHA:
        raise ValueError("Original v2 film/receipt hash differs")
    protected = {path: native.digest(path) for path in [v1_receipt_path, v1_video,
                pair_receipt_path, pair_video, v2_receipt_path, v2_video, HELPER]}
    if protected[v1_video] != V1_SHA or protected[pair_video] != PAIR_SHA:
        raise ValueError("Historical film hash changed")
    source_lookup = {item["shot"]: item for item in v1["sources"]}
    if set(source_lookup) != {"S01", "S02", "S03", "S04", "S05"}:
        raise ValueError("v1 must describe the same five distinct sources")
    sources, scans = [], []
    for shot, start, end in SELECTION:
        record = source_lookup[shot]
        source = (ROOT / record["path"]).resolve()
        if not source.is_relative_to(HERE) or native.digest(source) != record["sha256"]:
            raise ValueError(f"Source path/hash mismatch: {shot}")
        scan = native.full_decode(source)
        native.require_interval(start, end, scan["decoded_frames"], 2 * OVERLAP + 1)
        sources.append(source)
        scans.append(scan)
    mapping, joins = plan_mapping()
    verify_protected(protected)
    for source, (shot, _, _) in zip(sources, SELECTION):
        if native.digest(source) != source_lookup[shot]["sha256"]:
            raise ValueError(f"Source changed during preflight: {shot}")

    output.mkdir()
    video = output / "M03_commute_week_inspiration_v2_refined.mp4"
    images = streamed_frames(sources)
    try:
        native.encode_new(video, images)
    finally:
        images.close()
    decoded = native.full_decode(video)
    if decoded["decoded_frames"] != TOTAL or decoded["metadata"].get("audio_codec") is not None:
        raise ValueError("Expected exactly 474 native frames with no audio stream")
    qa = output / "QA"
    qa.mkdir()
    overall = native.extract_boards(video, qa, 0, TOTAL)
    for join in joins:
        begin, end = join["output_frames_half_open"]
        boundary = list(range(begin - 8, end + 8))
        join_qa = qa / join["join"]
        join_qa.mkdir()
        join["QA_directory"] = relative(join_qa)
        join["QA_samples"] = native.extract_boards(video, join_qa,
            boundary[0], boundary[-1] + 1, boundary)
    native.json_new(qa / "frame_mapping.json", mapping)
    native.json_new(qa / "full_decode.json", decoded)
    native.json_new(qa / "source_full_decodes.json", [
        {"shot": shot, "path": relative(source), "sha256": source_lookup[shot]["sha256"], "scan": scan}
        for (shot, _, _), source, scan in zip(SELECTION, sources, scans)])
    verify_protected(protected)
    for source, (shot, _, _) in zip(sources, SELECTION):
        if native.digest(source) != source_lookup[shot]["sha256"]:
            raise ValueError(f"Source changed during composition: {shot}")
    receipt = {
        "date": "2026-10-15", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "single_interval_refinement_pending_visual_and_user_review",
        "model": "M03", "output": relative(video), "sha256": native.digest(video),
        "native_size": [720, 1280], "native_fps": FPS, "decoded_frames": TOTAL,
        "seconds": TOTAL / FPS, "metadata": decoded["metadata"],
        "sources": [{"shot": shot, "path": relative(source), "sha256": source_lookup[shot]["sha256"],
                     "selected_frames_half_open": [start, end],
                     "seconds_half_open": [start / FPS, end / FPS],
                     "selected_frames": end - start,
                     "clear_outfit_frames": end - start - OVERLAP * (1 if index in (0, 4) else 2),
                     "clear_outfit_seconds": (end - start - OVERLAP * (1 if index in (0, 4) else 2)) / FPS}
                    for index, ((shot, start, end), source) in enumerate(zip(SELECTION, sources))],
        "transitions": joins, "overall_QA_samples": overall,
        "protected_inputs": [{"path": relative(path), "sha256": digest} for path, digest in protected.items()],
        "source_hashes_preserved": True, "protected_inputs_preserved": True,
        "audio": False, "baked_text": False, "retiming": False,
        "freeze": False, "reverse": False, "replay": False, "crop": False, "scaling": False,
        "delivery_framing_transform": "none; entire native raster",
        "image_operation": "Four 18-frame linear RGB cross dissolves, new alpha=(index+1)/18",
        "encoding": "native RGB sequence, h264 CRF18, 24fps, no audio",
        "streaming": "One source reader and 18 previous tail frames plus current blend",
        "technical_checks_are_visual_approval": False, "combined_sampled_visual_review": "pending",
        "assistant_continuous_playback": False, "user_film_approval": None,
        "registry_acceptance": "pending", "account_wide_adoption": None, "publishable": False,
        "publishing_files_replaced": [], "publishing_changed": [], "shared_state_changed": [],
        "cloud_write": False, "publication": False,
        "scope": "Single-source-interval refinement of v2 existing-source order/dwell trial only.",
        "refinement": {
            "baseline_v2_path": relative(v2_video), "baseline_v2_sha256": V2_SHA,
            "only_changed_shot": "S01", "previous_source_frames_half_open": [42, 156],
            "new_source_frames_half_open": [120, 234], "segment_frames_unchanged": 114,
            "purpose": "Use the observed later walking-direction gaze instead of the earlier opposite-direction smile.",
            "tradeoff": "S01 is more side-on; its return to the S05 three-quarter face remains a viewing tradeoff.",
            "comfort_improvement_accepted": None,
            "original_viewer_purpose_feedback_resolved_claimed": False,
            "original_pacing_feedback_resolved_claimed": False,
        },
        "new_motion_claimed": False, "new_camera_language_claimed": False,
        "viewer_purpose_feedback_resolved_claimed": False, "pacing_feedback_resolved_claimed": False,
        "limitations": ["Existing source motion and camera framing remain unchanged.",
                        "Later S01 is more side-on; the following S05 three-quarter face still changes viewing angle.",
                        "Shorter dwell and new order require actual full-playback judgement.",
                        "Existing texture, source deviations and cross-dissolve double outlines are not corrected by this edit.",
                        "Re-encoding does not preserve historical decoded pixels bit-for-bit."],
        "helper_note": "Used native read/encode/QA primitives only; did not execute prior study main or approval gates.",
    }
    native.json_new(output / "edit_receipt.json", receipt)
    print(json.dumps({"output": str(video), "sha256": receipt["sha256"], "metadata": decoded,
                      "clear_outfit_seconds": {item["shot"]: item["clear_outfit_seconds"] for item in receipt["sources"]},
                      "status": receipt["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    build()
