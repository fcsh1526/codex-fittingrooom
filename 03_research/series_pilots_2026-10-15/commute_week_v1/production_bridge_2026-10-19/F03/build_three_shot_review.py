"""Build a new, isolated F01/F02/F03 research preview after exact F03 source review.

Run only after the operator has inspected F03_source.mp4; --f03-sha is mandatory.
F01 [0,78), corrected F02 [0,145), and all F03 native frames are joined by two
18-frame linear dissolves. Native 720x1280/24fps, full raster, original speed,
no text or audio. Existing sources, accepted pair and outputs are never changed.
This technical builder does not grant visual approval or make media publishable.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent
HELPER = BRIDGE / "F02/build_first_pair_review.py"
spec = importlib.util.spec_from_file_location("mira_f01_f02_native_builder", HELPER)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load native pair helper: {HELPER}")
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)

SIZE, FPS, OVERLAP = native.SIZE, native.FPS, native.OVERLAP
F01_COUNT, F02_COUNT = 78, 145
JOIN_12 = F01_COUNT - OVERLAP  # output60..77
PAIR_COUNT = F01_COUNT + F02_COUNT - OVERLAP  #205
JOIN_23 = PAIR_COUNT - OVERLAP  # output187..204
F01 = BRIDGE / "F01/F01_source.mp4"
F02 = BRIDGE / "F02/motion_retry_01/F02_source.mp4"
F03 = HERE / "F03_source.mp4"
ACCEPTED_PAIR = BRIDGE / "F02/motion_retry_01/F01_F02_gait_fix_review_v1.mp4"
F01_SHA = "6a9bf3204aadad28dc710aa914592e26851a03e47209c5bd9b682286b184fa50"
F02_SHA = "cc23a3e22b5d51b2db42cc87b33371f73189b25b101cc37fff3a070dd68800b0"
ACCEPTED_PAIR_SHA = "54da666276fd89fc93461fc25bbe2aa805e565beff8f708bf071b78118a462dd"


def encode_new(path: Path, images) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=".three_shot_", suffix=".mp4", dir=path.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    writer = native.imageio_ffmpeg.write_frames(
        str(temporary), SIZE, fps=FPS, codec="libx264", pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p", quality=None, macro_block_size=1,
        ffmpeg_log_level="error",
        output_params=["-crf", "18", "-preset", "medium", "-movflags", "+faststart", "-an"],
    )
    try:
        writer.send(None)
        for frame in images:
            writer.send(frame.tobytes())
        writer.close()
        if not temporary.is_file() or not temporary.stat().st_size:
            raise ValueError("Encoder produced no video")
        with temporary.open("rb") as source, path.open("xb") as target:
            shutil.copyfileobj(source, target, 1024 * 1024)
    finally:
        writer.close()
        temporary.unlink(missing_ok=True)


def extract_boards(path: Path, total: int, qa: Path) -> dict:
    full = native.uniform_indices(total)
    joins = {
        "J12": list(range(max(0, JOIN_12 - 8), min(total, F01_COUNT + 8))),
        "J23": list(range(max(0, JOIN_23 - 8), min(total, PAIR_COUNT + 8))),
    }
    keep = set(full) | set(joins["J12"]) | set(joins["J23"])
    frames_dir = qa / "frames"
    frames_dir.mkdir()
    found = {}
    with native.native_reader(path) as reader:
        for index, raw in enumerate(reader):
            if index not in keep:
                continue
            frame = native.Image.frombytes("RGB", SIZE, raw)
            native.image_new(frames_dir / f"frame_{index:06d}.png", frame)
            found[index] = frame
    if set(found) != keep:
        raise ValueError("Not every requested full/native QA frame was extracted")
    native.contact_sheet([(index, found[index]) for index in full],
                         qa / "full_25_checkpoints.png", "Full-raster samples; visual review pending")
    for label, indices in joins.items():
        native.contact_sheet([(index, found[index]) for index in indices],
                             qa / f"{label}_all_boundary_frames.png",
                             f"{label}:18 dissolve frames +8 each side; review pending")
    return {
        "full_checkpoint_indices": full,
        "J12_boundary_indices": joins["J12"], "J23_boundary_indices": joins["J23"],
        "J12_all_18_transition_frames_extracted": all(index in found for index in range(JOIN_12, F01_COUNT)),
        "J23_all_18_transition_frames_extracted": all(index in found for index in range(JOIN_23, PAIR_COUNT)),
        "individual_QA_frames_size": list(SIZE),
        "QA_contact_sheets_are_reduced_full_raster_thumbnails": True,
        "QA_frame_crop": False,
    }


def build(f03_sha: str, version: str = "v1") -> dict:
    if not re.fullmatch(r"v[1-9][0-9]*", version):
        raise ValueError("Version must be v1, v2, ...; no arbitrary output path")
    destination = HERE / f"three_shot_review_{version}"
    if os.path.lexists(destination):
        raise FileExistsError(f"Preserve existing/partial output; select a new --version: {destination}")
    expected_sources = [(F01, F01_SHA), (F02, F02_SHA), (F03, f03_sha), (ACCEPTED_PAIR, ACCEPTED_PAIR_SHA)]
    for path, digest in expected_sources:
        native.verified_source(path, digest)
    scans = [native.full_decode(path) for path in (F01, F02, F03)]
    if scans[0]["decoded_frames"] < F01_COUNT:
        raise ValueError("F01 does not contain required native [0,78)")
    if scans[1]["decoded_frames"] != F02_COUNT:
        raise ValueError("Corrected exact F02 must have145 native frames")
    f03_count = scans[2]["decoded_frames"]
    if f03_count <= OVERLAP:
        raise ValueError("F03 needs more than18 native frames")
    total = F01_COUNT + F02_COUNT + f03_count - 2 * OVERLAP
    destination.mkdir()  # Exclusive directory allocation; partial failures remain reviewable.
    output = destination / f"F01_F02_F03_native_soft_review_{version}.mp4"
    receipt = destination / "edit_receipt.json"
    qa = destination / "QA_three_shot"
    mapping = []
    a = native.selected_frames(F01, F01_COUNT)
    b = native.selected_frames(F02, F02_COUNT)
    c = native.selected_frames(F03, f03_count)

    def mapped(frame, f01=None, f02=None, f03=None, alpha=None, join=None):
        mapping.append({"output_frame": len(mapping), "F01_native_frame": f01,
                        "F02_native_frame": f02, "F03_native_frame": f03,
                        "join": join, "incoming_alpha": alpha})
        return frame

    def composite():
        for index in range(JOIN_12):
            yield mapped(next(a), f01=index)
        # This is exactly the accepted pair builder's linear blend algorithm.
        for index in range(OVERLAP):
            alpha = (index + 1) / OVERLAP
            yield mapped(native.Image.blend(next(a), next(b), alpha),
                         f01=JOIN_12 + index, f02=index, alpha=alpha, join="J12")
        for index in range(OVERLAP, F02_COUNT - OVERLAP):
            yield mapped(next(b), f02=index)
        for index in range(OVERLAP):
            alpha = (index + 1) / OVERLAP
            yield mapped(native.Image.blend(next(b), next(c), alpha),
                         f02=F02_COUNT - OVERLAP + index, f03=index, alpha=alpha, join="J23")
        for index in range(OVERLAP, f03_count):
            yield mapped(next(c), f03=index)

    frames = composite()
    try:
        encode_new(output, frames)
    finally:
        frames.close()
        a.close()
        b.close()
        c.close()
    output_scan = native.full_decode(output)
    if output_scan["decoded_frames"] != total or len(mapping) != total:
        raise ValueError("Output count does not equal78+145+F03_N-36")
    inventory = native.stream_inventory(output)
    if inventory["audio_stream_present"]:
        raise ValueError("Unexpected audio stream in clean research preview")
    qa.mkdir()
    samples = extract_boards(output, total, qa)
    native.json_new(qa / "frame_mapping.json", mapping)
    native.json_new(qa / "full_decode.json", output_scan)
    for path, digest in expected_sources:
        native.verified_source(path, digest)
    artifacts = [{"path": str(path.relative_to(destination)), "sha256": native.sha256(path)}
                 for path in sorted(qa.rglob("*")) if path.is_file()]
    value = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "research_three_shot_candidate_pending_visual_review",
        "execution": "local", "model": "M03", "look_ids": ["L01", "L05", "L03"],
        "purpose": "First three connected segments of the company-front commute research pilot",
        "builder_sha256": native.sha256(Path(__file__).resolve()),
        "native_helper": str(HELPER), "native_helper_sha256": native.sha256(HELPER),
        "sources": [
            {"role": role, "path": str(path), "sha256": digest,
             "selected_native_frames_half_open": [0, count], "full_decode": scan}
            for role, path, digest, count, scan in zip(
                ["F01_L01", "F02_L05_corrected", "F03_L03"],
                [F01, F02, F03], [F01_SHA, F02_SHA, f03_sha],
                [F01_COUNT, F02_COUNT, f03_count], scans)
        ],
        "accepted_pair_reference": {"path": str(ACCEPTED_PAIR), "sha256": ACCEPTED_PAIR_SHA,
                                    "used_as_media_input": False, "modified": False},
        "output": str(output), "output_sha256": native.sha256(output),
        "native_size": list(SIZE), "fps": FPS, "frames": total, "seconds": total / FPS,
        "frame_count_formula": "78 +145 +F03_decoded_frames -18 -18",
        "output_full_decode": output_scan, "output_stream_inventory": inventory,
        "transitions": [
            {"id": "J12", "type": "linear_cross_dissolve", "frames": OVERLAP,
             "seconds": OVERLAP / FPS, "output_frames_half_open": [JOIN_12, F01_COUNT],
             "output_seconds_half_open": [JOIN_12 / FPS, F01_COUNT / FPS],
             "outgoing_F01_native_frames_half_open": [60, 78],
             "incoming_F02_native_frames_half_open": [0, 18]},
            {"id": "J23", "type": "linear_cross_dissolve", "frames": OVERLAP,
             "seconds": OVERLAP / FPS, "output_frames_half_open": [JOIN_23, PAIR_COUNT],
             "output_seconds_half_open": [JOIN_23 / FPS, PAIR_COUNT / FPS],
             "outgoing_F02_native_frames_half_open": [127, 145],
             "incoming_F03_native_frames_half_open": [0, 18]},
        ],
        "incoming_blend_weight": "(overlap_index +1)/18; overlap_index=0..17",
        "first_join_algorithm_matches_accepted_pair_builder": True,
        "first_205_encoded_frames_byte_or_pixel_identical_to_accepted_pair": False,
        "speed": {"F01_factor": 1.0, "F02_factor": 1.0, "F03_factor": 1.0,
                  "output_clock_fps": FPS, "native_frame_order_preserved": True,
                  "retime": False, "freeze_reverse_repeat_interpolation": False,
                  "individual_source_PTS_measured": False},
        "framing_transform": "none; complete native720x1280 raster",
        "text": "none", "audio": "none; encoded stream inspection confirms no Audio stream",
        "sample_assets": samples, "QA_artifacts": artifacts,
        "sources_and_accepted_pair_verified_unchanged_after_encode": True,
        "technical_checks_are_visual_approval": False,
        "assistant_continuous_visual_review": None, "combined_dynamic_QA": "pending",
        "user_video_approval": None, "publishable": False,
        "cloud_write": False, "publication": False,
        "limitations": [
            "Invocation follows operator review of exact F03; the builder does not perform source visual QA.",
            "All three native sources are decoded and recomposited; first join math is unchanged, but the new video is re-encoded.",
            "Full decode, sampled boards and mapping do not approve identity, clothing, gait, scene continuity or joins.",
            "Normal-speed continuous visual review and user approval remain separate; no full five-look approval is inferred.",
            "Decoded native frame order stays on a24fps clock; individual source PTS were not measured.",
        ],
    }
    native.json_new(receipt, value)
    return {"output": str(output), "sha256": value["output_sha256"], "frames": total,
            "seconds": total / FPS, "receipt": str(receipt), "QA": str(qa)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f03-sha", required=True, help="Exact lowercase SHA256 after operator source inspection")
    parser.add_argument("--version", default="v1", help="New output directory version:v1,v2,...; never reuse an existing one")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.f03_sha, args.version), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False),
              file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
