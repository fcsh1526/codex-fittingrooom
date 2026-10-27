"""Build a new native-speed five-look research preview, never a publishing replacement.

Usage: python build_five_look_preview.py --starts S03_START S04_START S05_START
Starts are zero-based native 24 fps frame numbers, not seconds. Each selected
interval is 156 frames. S01/S02 and the existing accepted first-pair edit remain
immutable. This program records technical evidence; it never grants visual QA.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / "10_automation").is_dir())
HELPER = ROOT / "03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py"
spec = importlib.util.spec_from_file_location("five_look_native_primitives", HELPER)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
from PIL import Image

FPS, LENGTH, OVERLAP, TOTAL = 24, 156, 18, 708
SHOTS = [f"S{number:02d}" for number in range(1, 6)]
IMMUTABLE_PAIR_SHA = "d25ad7a1ecdc7fc9dcafa18295aa201e1e7ca466e09e763d7553bc943efacc8b"
IMMUTABLE_SOURCE_SHA = [
    "499fa888e084649a4988ede3f0469619e2313456f4bd5035338f4d57bb9f3d04",
    "a8f9fc6e9019c23433c855e3d108d97d3236c05f76fa30b02b6b0fcdc97c6ec0",
]


def relative(path):
    return path.relative_to(ROOT).as_posix()


def nonnegative(value):
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("Start frame must be a non-negative integer")
    return parsed


def mapping_row(output_frame, contributions, join=None):
    row = {"output_frame": output_frame}
    row.update({f"{shot}_frame": None for shot in SHOTS})
    row.update({f"{shot}_alpha": 0 for shot in SHOTS})
    for shot, frame, alpha in contributions:
        row[f"{shot}_frame"] = frame
        row[f"{shot}_alpha"] = alpha
    row["join"] = join
    return row


def frame_mapping(starts):
    """Use the same (offset+1)/18 blend weights as the accepted first pair."""
    rows = []
    for shot_index, (shot, start) in enumerate(zip(SHOTS, starts)):
        head = OVERLAP if shot_index else 0
        tail = LENGTH - OVERLAP if shot_index < len(SHOTS) - 1 else LENGTH
        for offset in range(head, tail):
            rows.append(mapping_row(len(rows), [(shot, start + offset, 1)]))
        if shot_index < len(SHOTS) - 1:
            following = SHOTS[shot_index + 1]
            join = f"J{shot_index + 1}{shot_index + 2}"
            for offset in range(OVERLAP):
                alpha = (offset + 1) / OVERLAP
                rows.append(mapping_row(len(rows), [
                    (shot, start + LENGTH - OVERLAP + offset, 1 - alpha),
                    (following, starts[shot_index + 1] + offset, alpha),
                ], join))
    if len(rows) != TOTAL:
        raise ValueError(f"Unexpected planned frame count: {len(rows)}")
    return rows


def pair_projection(row):
    return {key: row[key] for key in ("output_frame", "S01_frame", "S02_frame", "S02_alpha")}


def streamed_images(sources, starts):
    """Retain only the preceding 18 RGB frames, never five full RGB segments."""
    tail = []
    for shot_index, (source, start) in enumerate(zip(sources, starts)):
        stream = native.selected_frames(source, start, start + LENGTH)
        try:
            consumed = 0
            if shot_index:
                if len(tail) != OVERLAP:
                    raise ValueError("Previous segment did not provide exactly 18 tail frames")
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
            visible_end = LENGTH if shot_index == len(sources) - 1 else LENGTH - OVERLAP
            for _ in range(consumed, visible_end):
                yield next(stream)
            if shot_index < len(sources) - 1:
                tail = [next(stream) for _ in range(OVERLAP)]
            try:
                next(stream)
            except StopIteration:
                pass
            else:
                raise ValueError("Selected stream exceeds its planned interval")
        finally:
            stream.close()
    for image in tail:
        if image is not None:
            image.close()


def build(remaining_starts):
    output = HERE / "five_look_review_v1"
    if output.resolve().parent != HERE or os.path.lexists(output):
        raise FileExistsError(f"Preserve existing output; require a new child directory: {output}")
    sources = [HERE / "motion_attempt_01" / f"{shot}_source.mp4" for shot in SHOTS[:2]]
    sources += [HERE / "motion_attempt_02" / f"{shot}_source.mp4" for shot in SHOTS[2:]]
    starts = [0, 60, *remaining_starts]
    pair_video = HERE / "first_pair_review_v1/M03_commute_first_pair_review_v1.mp4"
    pair_mapping_path = HERE / "first_pair_review_v1/QA/frame_mapping.json"
    pair_receipt_path = HERE / "first_pair_review_v1/edit_receipt.json"
    protected = {path: native.digest(path) for path in [pair_video, pair_mapping_path, pair_receipt_path, HELPER]}
    if protected[pair_video] != IMMUTABLE_PAIR_SHA:
        raise ValueError("Accepted first-pair video hash differs")
    source_hashes = [native.digest(path) for path in sources]
    if source_hashes[:2] != IMMUTABLE_SOURCE_SHA:
        raise ValueError("Immutable S01/S02 source hashes differ")
    scans = [native.full_decode(path) for path in sources]
    for start, scan in zip(starts, scans):
        native.require_interval(start, start + LENGTH, scan["decoded_frames"], LENGTH)
    pair_scan = native.full_decode(pair_video)
    if pair_scan["decoded_frames"] != 294:
        raise ValueError("Accepted first pair no longer has 294 frames")
    pair_mapping = native.read_json(pair_mapping_path)
    pair_receipt = native.read_json(pair_receipt_path)
    if pair_receipt.get("sha256") != IMMUTABLE_PAIR_SHA or len(pair_mapping) != 294:
        raise ValueError("Accepted first-pair receipt/mapping is inconsistent")
    mapping = frame_mapping(starts)
    prefix = 2 * (LENGTH - OVERLAP)
    if [pair_projection(row) for row in mapping[:prefix]] != pair_mapping[:prefix]:
        raise ValueError("First 276 frame source/blend mapping differs from the accepted first pair")
    for path, expected in protected.items():
        if native.digest(path) != expected:
            raise ValueError(f"Protected input changed during preflight: {path}")
    if [native.digest(path) for path in sources] != source_hashes:
        raise ValueError("A source changed during preflight")

    output.mkdir()
    video = output / "M03_commute_five_look_review_v1.mp4"
    images = streamed_images(sources, starts)
    try:
        native.encode_new(video, images)
    finally:
        images.close()
    decoded = native.full_decode(video)
    if decoded["decoded_frames"] != TOTAL or decoded["metadata"].get("audio_codec") is not None:
        raise ValueError("Output must have 708 native frames and no audio stream")
    qa = output / "QA"
    qa.mkdir()
    overall_boards = native.extract_boards(video, qa, 0, TOTAL)
    joins = []
    for join_index in range(4):
        begin = (join_index + 1) * (LENGTH - OVERLAP)
        end = begin + OVERLAP
        join_id = f"J{join_index + 1}{join_index + 2}"
        join_qa = qa / join_id
        join_qa.mkdir()
        boundary = list(range(begin - 8, end + 8))
        boards = native.extract_boards(video, join_qa, boundary[0], boundary[-1] + 1, boundary)
        joins.append({
            "join": join_id, "from_shot": SHOTS[join_index], "to_shot": SHOTS[join_index + 1],
            "type": "linear_cross_dissolve", "frames": OVERLAP, "seconds": OVERLAP / FPS,
            "output_frames_half_open": [begin, end],
            "output_seconds_half_open": [begin / FPS, end / FPS],
            "new_shot_alpha": "(index+1)/18", "QA_directory": relative(join_qa),
            "QA_samples": boards, "sampled_visual_review": "pending", "user_join_approval": None,
        })
    native.json_new(qa / "frame_mapping.json", mapping)
    native.json_new(qa / "full_decode.json", decoded)
    native.json_new(qa / "source_full_decodes.json", [
        {"shot": shot, "path": relative(path), "sha256": digest, "scan": scan}
        for shot, path, digest, scan in zip(SHOTS, sources, source_hashes, scans)
    ])
    for path, expected in protected.items():
        if native.digest(path) != expected:
            raise ValueError(f"Protected input changed: {path}")
    if [native.digest(path) for path in sources] != source_hashes:
        raise ValueError("A source changed during composition/QA")
    receipt = {
        "date": "2026-10-15", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "technical_decode_complete_sampled_visual_and_full_playback_review_pending",
        "model": "M03", "output": relative(video), "sha256": native.digest(video),
        "native_size": [720, 1280], "native_fps": FPS, "decoded_frames": TOTAL,
        "seconds": TOTAL / FPS, "metadata": decoded["metadata"],
        "sources": [{
            "shot": shot, "path": relative(path), "sha256": digest,
            "selected_frames_half_open": [start, start + LENGTH],
            "seconds_half_open": [start / FPS, (start + LENGTH) / FPS],
            "clear_outfit_frames": LENGTH - OVERLAP * (1 if index in (0, 4) else 2),
            "clear_outfit_seconds": 5.75 if index in (0, 4) else 5.0,
        } for index, (shot, path, digest, start) in enumerate(zip(SHOTS, sources, source_hashes, starts))],
        "transitions": joins, "overall_QA_samples": overall_boards,
        "accepted_first_pair": {
            "path": relative(pair_video), "sha256": IMMUTABLE_PAIR_SHA,
            "source_hashes": IMMUTABLE_SOURCE_SHA,
            "mapping_path": relative(pair_mapping_path), "mapping_sha256": protected[pair_mapping_path],
            "source_blend_mapping_identical_output_frames_half_open": [0, prefix],
            "identical_mapping_verified": True,
            "J23_starts_at_output_frame": prefix,
            "previous_pair_final_18_frames_now_blend_into_S03": True,
            "encoded_pixel_identity_claimed": False,
            "note": "Re-encoding can alter decoded pixels; verified identity concerns source frames and blend weights only.",
        },
        "protected_inputs": [{"path": relative(path), "sha256": digest} for path, digest in protected.items()],
        "source_hashes_preserved": True, "audio": False, "baked_text": False,
        "retiming": False, "freeze": False, "reverse": False, "replay": False,
        "crop": False, "scaling": False, "delivery_framing_transform": "none; entire native raster",
        "image_operation": "PIL blend of 18 corresponding native RGB frames at each of four joins only",
        "encoding": "native RGB sequence, h264 CRF18, 24fps, no audio",
        "streaming": "At most one source reader and 18 previous tail frames retained, plus current blend",
        "technical_checks_are_visual_approval": False, "combined_sampled_visual_review": "pending",
        "assistant_continuous_playback": False, "user_film_approval": None,
        "publishable": False, "publishing_files_replaced": [], "publishing_changed": [],
        "cloud_write": False, "publication": False,
        "helper_note": "Imported only native read/encode/QA primitives; did not execute prior study main or its approval gates.",
    }
    native.json_new(output / "edit_receipt.json", receipt)
    print(json.dumps({"output": str(video), "frames": TOTAL, "seconds": TOTAL / FPS,
                      "audio": False, "status": receipt["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starts", nargs=3, required=True, type=nonnegative,
                        metavar=("S03_START", "S04_START", "S05_START"),
                        help="Native zero-based source start frames for the remaining three looks")
    build(parser.parse_args().starts)
