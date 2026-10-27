"""Create a new native 9.25s U01/U02 review pair after root's source-motion QA.

python build_first_urban_pair.py --starts A B --source-shas SHA_A SHA_B

Starts are native zero-based 24fps frames, not seconds. This builder does not
judge gait or camera performance. Root must first review both selected source
intervals and decide that they are suitable for a pair review. It never creates
motion, changes prior artifacts, grants approval, uploads or publishes.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / "10_automation").is_dir())
HELPER = ROOT / "03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py"
spec = importlib.util.spec_from_file_location("urban_pair_native_primitives", HELPER)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
from PIL import Image

FPS, LENGTH, OVERLAP, TOTAL = 24, 120, 18, 222
APPROVED_STILLS = [
    {
        "shot": "U01", "look_id": "ED-W42-COMMUTE-V1-L01",
        "receipt": "U01_user_still_approval_2026-10-15.json",
        "receipt_sha256": "bbe9fb065b16b615af57e9761e2ed4a05ba18cd5ef315d718987a46d5c61f3e3",
        "image": "starting_images/U01_M03_L01_candidate_A.png",
        "image_sha256": "8fdead57f123626181cc67d74eeee3dfabc175fe641afefd917e27498048656e",
    },
    {
        "shot": "U02", "look_id": "ED-W42-COMMUTE-V1-L04",
        "receipt": "U02_user_still_approval_2026-10-15.json",
        "receipt_sha256": "a8759fad46415907835c07290653d1dce7ebbb0c6a7131984b5ef64fcba39057",
        "image": "starting_images/U02_M03_L04_candidate_A_refined_v2.png",
        "image_sha256": "99beee1fe695fa295db579e43320964133ebeb6d7c5eca2862640d4344dfdd1e",
    },
]


def relative(path):
    return path.relative_to(ROOT).as_posix()


def nonnegative(value):
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("Start frames must be non-negative integers")
    return parsed


def verify(records):
    for path, digest in records.items():
        if native.digest(path) != digest:
            raise ValueError(f"Protected input hash changed: {path}")


def verify_still_approvals():
    records, evidence = {}, []
    for expected in APPROVED_STILLS:
        receipt_path = HERE / expected["receipt"]
        image_path = HERE / expected["image"]
        actual_receipt_sha = native.digest(receipt_path)
        if actual_receipt_sha != expected["receipt_sha256"]:
            raise ValueError(f"Exact still approval receipt changed: {receipt_path}")
        receipt = native.read_json(receipt_path)
        if (receipt.get("shot_id") != expected["shot"] or receipt.get("model_id") != "M03"
                or receipt.get("look_id") != expected["look_id"]
                or receipt.get("grok_generation_allowed_for_exact_still") is not True
                or receipt.get("user_quote") != "兩張可以，沿用"):
            raise ValueError(f"Receipt is not the expected exact still authorization: {receipt_path}")
        if (ROOT / receipt["file"]).resolve() != image_path.resolve():
            raise ValueError("Still receipt points to a different image")
        actual_image_sha = native.digest(image_path)
        if receipt.get("sha256") != expected["image_sha256"] or actual_image_sha != expected["image_sha256"]:
            raise ValueError(f"Approved still SHA differs: {image_path}")
        with Image.open(image_path) as image:
            actual_pixels = list(image.size)
        if receipt.get("pixels") != actual_pixels:
            raise ValueError("Approved image pixel dimensions differ from its receipt")
        records[receipt_path] = actual_receipt_sha
        records[image_path] = actual_image_sha
        evidence.append({"shot": expected["shot"], "look_id": expected["look_id"],
                         "approval_receipt": relative(receipt_path), "receipt_actual_sha256": actual_receipt_sha,
                         "image": relative(image_path), "image_actual_sha256": actual_image_sha,
                         "actual_pixels": actual_pixels, "user_quote": receipt["user_quote"],
                         "scope": "Exact still only; does not grant source-motion, pair or whole-film approval."})
    return records, evidence


def planned_mapping(starts):
    mapping = []
    for offset in range(LENGTH - OVERLAP):
        mapping.append({"output_frame": len(mapping), "U01_frame": starts[0] + offset,
                        "U02_frame": None, "U02_alpha": 0})
    for offset in range(OVERLAP):
        mapping.append({"output_frame": len(mapping), "U01_frame": starts[0] + LENGTH - OVERLAP + offset,
                        "U02_frame": starts[1] + offset, "U02_alpha": (offset + 1) / OVERLAP})
    for offset in range(OVERLAP, LENGTH):
        mapping.append({"output_frame": len(mapping), "U01_frame": None,
                        "U02_frame": starts[1] + offset, "U02_alpha": 1})
    if len(mapping) != TOTAL:
        raise ValueError("Incorrect planned pair length")
    return mapping


def streamed_images(sources, starts):
    stream_a = native.selected_frames(sources[0], starts[0], starts[0] + LENGTH)
    stream_b = native.selected_frames(sources[1], starts[1], starts[1] + LENGTH)
    tail = []
    try:
        for _ in range(LENGTH - OVERLAP):
            yield next(stream_a)
        tail = [next(stream_a) for _ in range(OVERLAP)]
        stream_a.close()
        for offset in range(OVERLAP):
            incoming = next(stream_b)
            previous = tail[offset]
            blended = Image.blend(previous, incoming, (offset + 1) / OVERLAP)
            previous.close()
            incoming.close()
            tail[offset] = None
            yield blended
        for _ in range(OVERLAP, LENGTH):
            yield next(stream_b)
    finally:
        stream_a.close()
        stream_b.close()
        for image in tail:
            if image is not None:
                image.close()


def build(starts, source_shas):
    output = HERE / "first_pair_review_v1"
    if output.resolve().parent != HERE or os.path.lexists(output):
        raise FileExistsError(f"Preserve existing output; require a new child folder: {output}")
    sources = [HERE / "motion_attempt_01" / f"{shot}_source.mp4" for shot in ("U01", "U02")]
    if len(set(source_shas)) != 2:
        raise ValueError("Two distinct independent motion sources are required")
    for path, expected in zip(sources, source_shas):
        native.require_sha(expected)
        if native.digest(path) != expected:
            raise ValueError(f"Actual source hash differs from --source-shas: {path}")
    protected, still_evidence = verify_still_approvals()
    protected[HELPER] = native.digest(HELPER)
    agent_prompt_path = HERE / "motion_attempt_01/agent_generation_prompt.txt"
    protected[agent_prompt_path] = native.digest(agent_prompt_path)
    generation_receipt = HERE / "motion_attempt_01/generation_receipt.json"
    if generation_receipt.is_file():
        protected[generation_receipt] = native.digest(generation_receipt)
    scans = [native.full_decode(path) for path in sources]
    for start, scan in zip(starts, scans):
        native.require_interval(start, start + LENGTH, scan["decoded_frames"], LENGTH)
    mapping = planned_mapping(starts)
    verify(protected)
    for path, expected in zip(sources, source_shas):
        if native.digest(path) != expected:
            raise ValueError(f"Source changed during preflight: {path}")

    output.mkdir()
    entry = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(), "execution": "local",
        "command_line_arguments": sys.argv[1:], "model": "M03", "shots": ["U01", "U02"],
        "starts_native_frames": starts, "source_shas_supplied_by_caller": source_shas,
        "exact_still_approvals_verified": still_evidence,
        "submitted_generation_prompt": {"path": relative(agent_prompt_path), "sha256": protected[agent_prompt_path],
                                        "role": "saved submitted text; not independent confirmation of actual tool parameters"},
        "source_generation_receipt": ({"path": relative(generation_receipt), "sha256": protected[generation_receipt]}
                                      if generation_receipt in protected else None),
        "actual_UI_settings_independently_verified_by_builder": None,
        "source_motion_QA": "External prerequisite: root must first find the selected gait/camera/source intervals suitable for review. Technical decoding does not establish this.",
        "source_motion_QA_inferred_from_still_or_decode": False,
        "source_full_decodes": [{"shot": shot, "path": relative(path), "sha256": digest, "scan": scan}
                                for shot, path, digest, scan in zip(("U01", "U02"), sources, source_shas, scans)],
    }
    native.json_new(output / "entry_receipt.json", entry)
    video = output / "M03_urban_commute_first_pair_review_v1.mp4"
    images = streamed_images(sources, starts)
    try:
        native.encode_new(video, images)
    finally:
        images.close()
    decoded = native.full_decode(video)
    if decoded["decoded_frames"] != TOTAL or decoded["metadata"].get("audio_codec") is not None:
        raise ValueError("Output must contain exactly 222 native frames and no audio stream")
    qa = output / "QA"
    qa.mkdir()
    samples = native.extract_boards(video, qa, 0, TOTAL, range(94, 128))
    native.json_new(qa / "frame_mapping.json", mapping)
    native.json_new(qa / "full_decode.json", decoded)
    native.json_new(qa / "source_full_decodes.json", entry["source_full_decodes"])
    verify(protected)
    for path, expected in zip(sources, source_shas):
        if native.digest(path) != expected:
            raise ValueError(f"Source changed during composition or QA: {path}")
    receipt = {
        "date": "2026-10-15", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "technical_decode_complete_pair_visual_and_user_review_pending",
        "model": "M03", "output": relative(video), "sha256": native.digest(video),
        "native_size": [720, 1280], "native_fps": FPS, "decoded_frames": TOTAL,
        "seconds": TOTAL / FPS, "metadata": decoded["metadata"],
        "entry_receipt": relative(output / "entry_receipt.json"),
        "sources": [{"shot": shot, "path": relative(path), "sha256": digest,
                     "selected_frames_half_open": [start, start + LENGTH],
                     "seconds_half_open": [start / FPS, (start + LENGTH) / FPS],
                     "clear_outfit_frames": LENGTH - OVERLAP, "clear_outfit_seconds": 4.25}
                    for shot, path, digest, start in zip(("U01", "U02"), sources, source_shas, starts)],
        "transition": {"type": "linear_cross_dissolve", "frames": OVERLAP, "seconds": 0.75,
                       "output_frames_half_open": [102, 120], "output_seconds_half_open": [4.25, 5.0],
                       "new_shot_alpha": "(index+1)/18", "user_join_approval": None},
        "QA_samples": samples,
        "protected_inputs": [{"path": relative(path), "sha256": digest} for path, digest in protected.items()],
        "protected_inputs_preserved": True, "source_hashes_preserved": True,
        "audio": False, "baked_text": False, "retiming": False, "freeze": False, "reverse": False,
        "replay": False, "crop": False, "scaling": False,
        "delivery_framing_transform": "none; entire native raster",
        "image_operation": "18 corresponding native RGB frame blends only",
        "encoding": "native RGB sequence, h264 CRF18, 24fps, no audio",
        "streaming": "At most 18 outgoing RGB tail frames plus the current incoming/blended frame",
        "technical_checks_are_visual_approval": False, "combined_sampled_visual_review": "pending",
        "assistant_continuous_playback": False, "user_film_approval": None,
        "normal_speed_full_playback_user_self_report": None, "complete_five_look_film_approval": None,
        "publishable": False, "account_wide_adoption": None,
        "publishing_files_replaced": [], "publishing_changed": [], "shared_state_changed": [],
        "cloud_write": False, "publication": False,
        "limitations": ["Source gait, camera language, commuter trajectories and background geometry require external actual visual QA.",
                        "25 full/5 face checkpoints and 34 join frames do not establish complete normal-speed comfort.",
                        "A new pair and old exact still approvals do not approve the full five-look film or a permanent series."],
        "helper_note": "Imported read/encode/QA primitives only; did not execute prior study main or its approval gates.",
    }
    native.json_new(output / "edit_receipt.json", receipt)
    print(json.dumps({"output": str(video), "sha256": receipt["sha256"], "frames": TOTAL,
                      "seconds": TOTAL / FPS, "audio": False, "status": receipt["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starts", nargs=2, type=nonnegative, required=True, metavar=("A", "B"))
    parser.add_argument("--source-shas", nargs=2, required=True, metavar=("SHA_A", "SHA_B"))
    args = parser.parse_args()
    build(args.starts, args.source_shas)
