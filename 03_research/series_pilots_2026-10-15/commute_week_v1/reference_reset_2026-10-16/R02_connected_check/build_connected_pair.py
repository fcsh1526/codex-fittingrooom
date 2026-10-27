"""New-only R01 -> R02 native connected-source diagnostic.

Run only after root reviews actual R02 motion:
python build_connected_pair.py --a-end 120 --b-start 0 --b-end 132 \
    --source-b-sha ACTUAL_SHA --output-dir connected_review_v1

All frame intervals are native, zero-based and half-open. A starts at48.
The example intervals are provisional, not actual usable-source claims.
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
PARENT = HERE.parent
ROOT = next(path for path in HERE.parents if (path / "10_automation").is_dir())
HELPER = ROOT / "03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py"
spec = importlib.util.spec_from_file_location("connected_pair_native_primitives", HELPER)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
from PIL import Image

FPS, OVERLAP, A_START = 24, 18, 48
A_SHA = "4bf0bdb9f4d547827fd36001da3c359eadcd2b7a2c053761b454effdc0ee4981"
ACCEPTED_FILM_SHA = "27fa4c9fcce685aaa247aa0f9dfb12fa4b311a26d56d81635c6254a8679be348"
STILL_B_SHA = "97cbeb0b9b91a8b9b1b3070665578ed664e64b357d1f4cd1046a7966ae895594"
LOCKED_DOCUMENTS = {
    PARENT / "R01_technical_scan.json": "38ed8a01c8976a17cae77cf97776dd0a54b7686f5b44a1679310d586421a66bb",
    PARENT / "R01_user_single_shot_direction_approval_2026-10-16.json": "7b25c22ef293c0f7a42494b2056f497941df26c23ded5d41184239cd68ba89da",
    PARENT / "selected_4s_edit_receipt.json": "a65e45d59a71220a314dc0abf940a1974a5f5d4c98c69b24630162394cc32299",
    HERE / "R02_user_still_approval_2026-10-16.json": "25a991cd671974cd087b441bf163683778aa477a05426c8345eef24578decc1d",
}


def relative(path):
    return path.relative_to(ROOT).as_posix()


def verify(records):
    for path, expected in records.items():
        if native.digest(path) != expected:
            raise ValueError(f"Protected source/approval/artifact hash differs: {path}")


def resolve_recorded_source(scan):
    value = scan.get("source")
    if not isinstance(value, str):
        return None
    path = Path(value)
    return (path if path.is_absolute() else ROOT / path).resolve()


def validated_scan(scan, source):
    native.require_native(scan["metadata"])
    count = scan.get("decoded_frames")
    if type(count) is not int or count <= 0:
        raise ValueError("Technical scan must have a positive decoded native frame count")
    recorded = resolve_recorded_source(scan)
    if recorded is not None and recorded != source.resolve():
        raise ValueError("Technical scan refers to a different source")
    return scan


def source_b_scan(source, expected_sha, protected):
    scan_path = HERE / "R02_technical_scan.json"
    if scan_path.is_file():
        scan = native.read_json(scan_path)
        # The generic scanner lacks an embedded source SHA; do not silently
        # treat that unbound cached count as validation of a replacement file.
        if scan.get("source_sha256") == expected_sha and resolve_recorded_source(scan) == source.resolve():
            protected[scan_path] = native.digest(scan_path)
            return validated_scan(scan, source), {
                "method": "reused_existing_source_SHA_bound_technical_scan",
                "path": relative(scan_path), "scan_sha256": protected[scan_path],
                "source_sha256": expected_sha, "fresh_full_decode_performed": False,
            }
    scan = native.full_decode(source)
    return scan, {"method": "fresh_full_decode_of_new_B_only",
                  "source_sha256": expected_sha, "fresh_full_decode_performed": True,
                  "reason": "No existing scan explicitly bound to this exact B source SHA was available."}


def verify_approvals(protected, source_a):
    verify(LOCKED_DOCUMENTS)
    protected.update(LOCKED_DOCUMENTS)
    film = PARENT / "R01_walk_past_4s_review_v2.mp4"
    protected[film] = ACCEPTED_FILM_SHA
    approval_a_path = PARENT / "R01_user_single_shot_direction_approval_2026-10-16.json"
    approval_a = native.read_json(approval_a_path)
    if (approval_a.get("sha256") != ACCEPTED_FILM_SHA or approval_a.get("single_shot_direction_accepted") is not True
            or approval_a.get("user_quote") != "更接近，可以往這個方向做"
            or (ROOT / approval_a["file"]).resolve() != film.resolve()
            or approval_a["source"].get("sha256") != A_SHA
            or (ROOT / approval_a["source"]["file"]).resolve() != source_a.resolve()
            or approval_a["source"].get("selected_frames_half_open") != [48, 144]):
        raise ValueError("R01 approval no longer identifies the accepted exact4s source interval")
    approval_b_path = HERE / "R02_user_still_approval_2026-10-16.json"
    approval_b = native.read_json(approval_b_path)
    still = HERE / "R02_M03_L02_medium_candidate_A.png"
    if (approval_b.get("sha256") != STILL_B_SHA or approval_b.get("grok_generation_allowed_for_exact_still") is not True
            or approval_b.get("shot_id") != "R02" or approval_b.get("model_id") != "M03"
            or (ROOT / approval_b["file"]).resolve() != still.resolve()
            or approval_b.get("user_quote") != "可以，沿用這張"):
        raise ValueError("R02 exact still approval differs")
    protected[still] = STILL_B_SHA
    verify(protected)
    with Image.open(still) as image:
        if list(image.size) != approval_b.get("pixels"):
            raise ValueError("R02 approved still dimensions differ")
    return [
        {"shot": "R01", "type": "partial_single_shot_direction_acceptance",
         "receipt": relative(approval_a_path), "receipt_sha256": protected[approval_a_path],
         "accepted_film": relative(film), "accepted_film_sha256": ACCEPTED_FILM_SHA,
         "accepted_source_frames_half_open": [48, 144], "scope": approval_a["scope"],
         "new_pair_approval_inferred": False},
        {"shot": "R02", "type": "exact_still_only", "receipt": relative(approval_b_path),
         "receipt_sha256": protected[approval_b_path], "still": relative(still), "still_sha256": STILL_B_SHA,
         "scope": approval_b["scope"], "motion_or_join_approval_inferred": False},
    ]


def image_stream(a, b, a_end, b_start, b_end):
    a_stream = native.selected_frames(a, A_START, a_end)
    b_stream = native.selected_frames(b, b_start, b_end)
    tail = []
    try:
        for _ in range(a_end - A_START - OVERLAP):
            yield next(a_stream)
        tail = [next(a_stream) for _ in range(OVERLAP)]
        a_stream.close()
        for offset in range(OVERLAP):
            incoming = next(b_stream)
            old = tail[offset]
            blended = Image.blend(old, incoming, (offset + 1) / OVERLAP)
            old.close()
            incoming.close()
            tail[offset] = None
            yield blended
        for _ in range(OVERLAP, b_end - b_start):
            yield next(b_stream)
    finally:
        a_stream.close()
        b_stream.close()
        for image in tail:
            if image is not None:
                image.close()


def mapping_for(a_end, b_start, b_end):
    rows = []
    for frame in range(A_START, a_end - OVERLAP):
        rows.append({"output_frame": len(rows), "R01_frame": frame, "R02_frame": None, "R02_alpha": 0})
    for offset in range(OVERLAP):
        rows.append({"output_frame": len(rows), "R01_frame": a_end - OVERLAP + offset,
                     "R02_frame": b_start + offset, "R02_alpha": (offset + 1) / OVERLAP})
    for frame in range(b_start + OVERLAP, b_end):
        rows.append({"output_frame": len(rows), "R01_frame": None, "R02_frame": frame, "R02_alpha": 1})
    return rows


def build(args):
    raw_output = Path(args.output_dir)
    output = (raw_output if raw_output.is_absolute() else HERE / raw_output).resolve()
    if output.parent != HERE or os.path.lexists(output):
        raise FileExistsError("--output-dir must name a new direct child directory; preserve all existing artifacts")
    a = PARENT / "R01_source.mp4"
    b = HERE / "R02_source.mp4"
    native.require_sha(args.source_b_sha)
    if args.source_b_sha == A_SHA:
        raise ValueError("Independent R02 motion must differ from R01")
    protected = {a: A_SHA, b: args.source_b_sha, HELPER: native.digest(HELPER)}
    approvals = verify_approvals(protected, a)
    scan_a_path = PARENT / "R01_technical_scan.json"
    scan_a = validated_scan(native.read_json(scan_a_path), a)
    if scan_a["decoded_frames"] != 145:
        raise ValueError("Hash-locked R01 technical scan no longer has145 native frames")
    scan_b, b_validation = source_b_scan(b, args.source_b_sha, protected)
    if not A_START < args.a_end <= 144:
        raise ValueError("A must stay within the accepted source interval[48,144)")
    for start, end, scan in ((A_START, args.a_end, scan_a), (args.b_start, args.b_end, scan_b)):
        # Eight inspection frames on either side of the dissolve require this
        # minimum; it is not a claim of enough clothing-reading time.
        native.require_interval(start, end, scan["decoded_frames"], OVERLAP + 8)
    total = args.a_end - A_START + args.b_end - args.b_start - OVERLAP
    mapping = mapping_for(args.a_end, args.b_start, args.b_end)
    if len(mapping) != total:
        raise ValueError("Frame mapping length differs from selected native intervals")
    verify(protected)

    output.mkdir()
    video = output / "M03_R01_R02_connected_review.mp4"
    images = image_stream(a, b, args.a_end, args.b_start, args.b_end)
    try:
        native.encode_new(video, images)
    finally:
        images.close()
    decoded = native.full_decode(video)
    if decoded["decoded_frames"] != total or decoded["metadata"].get("audio_codec") is not None:
        raise ValueError("New output frame count/audio differs from the native silent plan")
    qa = output / "QA"
    qa.mkdir()
    begin, end = args.a_end - A_START - OVERLAP, args.a_end - A_START
    samples = native.extract_boards(video, qa, 0, total, range(begin - 8, end + 8))
    native.json_new(qa / "frame_mapping.json", mapping)
    native.json_new(qa / "full_decode.json", decoded)
    validations = [
        {"shot": "R01", "method": "reused_exact_SHA_locked_existing_technical_scan",
         "path": relative(scan_a_path), "scan_sha256": protected[scan_a_path],
         "source_sha256": A_SHA, "scan": scan_a, "fresh_full_decode_performed": False},
        {"shot": "R02", **b_validation, "scan": scan_b},
    ]
    native.json_new(qa / "source_validation.json", validations)
    verify(protected)
    receipt = {
        "recorded_date": "2026-10-16", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "new_connected_pair_pending_sampled_visual_and_user_review", "model": "M03",
        "output": relative(video), "sha256": native.digest(video), "native_size": [720, 1280],
        "native_fps": FPS, "decoded_frames": total, "seconds": total / FPS, "metadata": decoded["metadata"],
        "command_line_arguments": sys.argv[1:], "source_validation": validations,
        "sources": [
            {"shot": "R01", "path": relative(a), "sha256": A_SHA,
             "selected_frames_half_open": [A_START, args.a_end],
             "selected_seconds_half_open": [A_START / FPS, args.a_end / FPS],
             "clear_outfit_seconds": (args.a_end - A_START - OVERLAP) / FPS},
            {"shot": "R02", "path": relative(b), "sha256": args.source_b_sha,
             "selected_frames_half_open": [args.b_start, args.b_end],
             "selected_seconds_half_open": [args.b_start / FPS, args.b_end / FPS],
             "clear_outfit_seconds": (args.b_end - args.b_start - OVERLAP) / FPS},
        ],
        "transition": {"type": "linear_cross_dissolve", "frames": OVERLAP, "seconds": 0.75,
                       "output_frames_half_open": [begin, end],
                       "output_seconds_half_open": [begin / FPS, end / FPS],
                       "new_shot_alpha": "(index+1)/18", "user_join_approval": None},
        "existing_approval_scopes": approvals, "QA_samples": samples,
        "protected_inputs": [{"path": relative(path), "sha256": digest} for path, digest in protected.items()],
        "protected_inputs_preserved": True, "audio": False, "baked_text": False,
        "retiming": False, "crop": False, "scaling": False, "freeze": False, "reverse": False, "replay": False,
        "image_operation": "18 native RGB frame blends only", "encoding": "h264 CRF18; native720x1280/24fps; no audio",
        "streaming": "18 outgoing tail frames plus current incoming/blended image",
        "technical_checks_are_visual_approval": False, "sampled_visual_review": "pending",
        "assistant_continuous_playback": False, "normal_speed_full_playback_user_self_report": None,
        "user_film_approval": None, "complete_five_look_film_approval": None, "publishable": False,
        "account_wide_adoption": None, "actual_UI_settings_verified_by_builder": None,
        "source_B_motion_QA": "External root review required before execution; not inferred from still approval or decode.",
        "publication": False, "cloud_write": False, "publishing_files_replaced": [], "shared_state_changed": [],
        "limitations": ["R01 acceptance concerns exact4s single-shot direction, not this modified selection or a new join.",
                        "R02 approval concerns its exact still, not generated motion or background continuity.",
                        "Adaptive source selections and cross-dissolve require actual normal-speed judgement.",
                        "Re-encoding does not preserve historical decoded pixels bit-for-bit."],
        "helper_note": "Reused read/encode/QA primitives only; did not invoke legacy main or protected_inputs.",
    }
    native.json_new(output / "edit_receipt.json", receipt)
    print(json.dumps({"output": str(video), "sha256": receipt["sha256"], "frames": total,
                      "seconds": total / FPS, "join_frames_half_open": [begin, end]}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a-end", type=int, required=True)
    parser.add_argument("--b-start", type=int, required=True)
    parser.add_argument("--b-end", type=int, required=True)
    parser.add_argument("--source-b-sha", required=True)
    parser.add_argument("--output-dir", required=True)
    build(parser.parse_args())
