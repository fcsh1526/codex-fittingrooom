"""Append an operator-reviewed F04 to the exact accepted phase+1 three-shot film.

The accepted331-frame composite is the media input; do not rebuild its earlier
joins. Keep [0,313), blend [313,331) with F04[0,18), then keep F04[18,N).
The only new dissolve is18 native24fps frames/0.75s. No retime, crop, text,
audio, freeze, reverse or interpolation. This builder never grants visual QA.
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
import sys
import tempfile

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent
HELPER = BRIDGE / "F02/build_first_pair_review.py"
spec = importlib.util.spec_from_file_location("mira_native_pair_f04", HELPER)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load helper: {HELPER}")
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)

SIZE, FPS, OVERLAP = native.SIZE, native.FPS, native.OVERLAP
PREFIX_COUNT = 331
JOIN_START = PREFIX_COUNT - OVERLAP
PREFIX = BRIDGE / "F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4"
PREFIX_SHA = "f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33"
SOURCE = HERE / "F04_source.mp4"
PROTECTED = [
    (PREFIX, PREFIX_SHA),
    (HERE / "F04_M03_L02_start_candidate_A.png", "98687eb8365828d67850ddc03d57e48d9d28ad4628f9f62c727bcb166e002457"),
    (HERE / "F04_M03_L02_end_candidate_A_footfix_v2.png", "78b0322f697806c8cf436a221a631e39e5d2f57a7e65df4044a2a27309a673ed"),
]


def encode_new(path: Path, frames) -> None:
    handle, name = tempfile.mkstemp(prefix=".four_shot_", suffix=".mp4", dir=path.parent)
    os.close(handle)
    temporary = Path(name)
    writer = native.imageio_ffmpeg.write_frames(
        str(temporary), SIZE, fps=FPS, codec="libx264", pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p", quality=None, macro_block_size=1,
        ffmpeg_log_level="error",
        output_params=["-crf", "18", "-preset", "medium", "-movflags", "+faststart", "-an"],
    )
    try:
        writer.send(None)
        for frame in frames:
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
    boundary = list(range(max(0, JOIN_START - 8), min(total, PREFIX_COUNT + 8)))
    keep = set(full) | set(boundary)
    frame_dir = qa / "frames"
    frame_dir.mkdir()
    found = {}
    with native.native_reader(path) as reader:
        for index, raw in enumerate(reader):
            if index in keep:
                frame = native.Image.frombytes("RGB", SIZE, raw)
                native.image_new(frame_dir / f"frame_{index:06d}.png", frame)
                found[index] = frame
    if set(found) != keep:
        raise ValueError("Not every requested full/native QA frame was extracted")
    native.contact_sheet([(index, found[index]) for index in full],
                         qa / "full_25_checkpoints.png", "Full-raster samples; visual review pending")
    native.contact_sheet([(index, found[index]) for index in boundary],
                         qa / "J34_all_boundary_frames.png", "J34:18 dissolve frames +8 each side; review pending")
    return {
        "full_checkpoint_indices": full, "J34_boundary_indices": boundary,
        "J34_all_18_transition_frames_extracted": all(index in found for index in range(JOIN_START, PREFIX_COUNT)),
        "individual_QA_frames_size": list(SIZE), "QA_frame_crop": False,
        "QA_contact_sheets_are_reduced_full_raster_thumbnails": True,
    }


def build(f04_sha: str, version: str = "v1") -> dict:
    if not re.fullmatch(r"v[1-9][0-9]*", version):
        raise ValueError("Version must be v1,v2,...; no arbitrary destination")
    destination = HERE / f"four_shot_review_{version}"
    if os.path.lexists(destination):
        raise FileExistsError(f"Preserve existing/partial output; select a new --version: {destination}")
    protected = [*PROTECTED, (SOURCE, f04_sha)]
    for path, digest in protected:
        native.verified_source(path, digest)
    prefix_scan, source_scan = native.full_decode(PREFIX), native.full_decode(SOURCE)
    if prefix_scan["decoded_frames"] != PREFIX_COUNT:
        raise ValueError("Exact accepted prefix must contain331 native frames")
    prefix_inventory = native.stream_inventory(PREFIX)
    if prefix_inventory["audio_stream_present"]:
        raise ValueError("Accepted clean prefix unexpectedly contains audio")
    count = source_scan["decoded_frames"]
    if count <= OVERLAP:
        raise ValueError("F04 needs more than18 native frames")
    total = PREFIX_COUNT + count - OVERLAP
    destination.mkdir()  # Exclusive allocation; keep partial failures for inspection.
    output = destination / f"F01_F02_F03_F04_native_soft_review_{version}.mp4"
    mapping = []
    outgoing = native.selected_frames(PREFIX, PREFIX_COUNT)
    incoming = native.selected_frames(SOURCE, count)

    def mapped(frame, prefix=None, f04=None, alpha=None):
        mapping.append({"output_frame": len(mapping), "accepted_prefix_native_frame": prefix,
                        "F04_native_frame": f04, "join": "J34" if alpha is not None else None,
                        "incoming_alpha": alpha})
        return frame

    def composite():
        for index in range(JOIN_START):
            yield mapped(next(outgoing), prefix=index)
        for index in range(OVERLAP):
            alpha = (index + 1) / OVERLAP
            yield mapped(native.Image.blend(next(outgoing), next(incoming), alpha),
                         prefix=JOIN_START + index, f04=index, alpha=alpha)
        for index in range(OVERLAP, count):
            yield mapped(next(incoming), f04=index)

    frames = composite()
    try:
        encode_new(output, frames)
    finally:
        frames.close()
        outgoing.close()
        incoming.close()
    output_scan = native.full_decode(output)
    if output_scan["decoded_frames"] != total or len(mapping) != total:
        raise ValueError("Output count must equal331 +F04_N -18")
    inventory = native.stream_inventory(output)
    if inventory["audio_stream_present"]:
        raise ValueError("Clean output unexpectedly contains audio")
    qa = destination / "QA_four_shot"
    qa.mkdir()
    samples = extract_boards(output, total, qa)
    native.json_new(qa / "frame_mapping.json", mapping)
    native.json_new(qa / "full_decode.json", output_scan)
    for path, digest in protected:
        native.verified_source(path, digest)
    artifacts = [{"path": str(path.relative_to(destination)), "sha256": native.sha256(path)}
                 for path in sorted(qa.rglob("*")) if path.is_file()]
    value = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "research_four_shot_candidate_pending_visual_review",
        "execution": "local", "model": "M03", "look_ids": ["L01", "L05", "L03", "L02"],
        "builder_sha256": native.sha256(Path(__file__).resolve()),
        "native_helper": str(HELPER), "native_helper_sha256": native.sha256(HELPER),
        "accepted_prefix": {"path": str(PREFIX), "sha256": PREFIX_SHA,
                            "used_as_media_input": True, "native_frames_half_open": [0, PREFIX_COUNT],
                            "earlier_joins_rebuilt": False, "full_decode": prefix_scan,
                            "stream_inventory": prefix_inventory, "modified": False},
        "incoming_source": {"path": str(SOURCE), "sha256": f04_sha,
                            "native_frames_half_open": [0, count], "full_decode": source_scan},
        "protected_inputs": [{"path": str(path), "sha256": digest} for path, digest in protected],
        "protected_inputs_verified_unchanged_after_encode": True,
        "output": str(output), "output_sha256": native.sha256(output),
        "native_size": list(SIZE), "fps": FPS, "frames": total, "seconds": total / FPS,
        "frame_count_formula": "331 +F04_decoded_frames -18",
        "output_full_decode": output_scan, "output_stream_inventory": inventory,
        "new_transition": {"id": "J34", "type": "linear_cross_dissolve", "frames": OVERLAP,
                           "seconds": OVERLAP / FPS, "output_frames_half_open": [JOIN_START, PREFIX_COUNT],
                           "output_seconds_half_open": [JOIN_START / FPS, PREFIX_COUNT / FPS],
                           "outgoing_accepted_prefix_native_frames_half_open": [313, 331],
                           "equivalent_original_F03_native_frames_half_open": [127, 145],
                           "incoming_F04_native_frames_half_open": [0, 18],
                           "incoming_weight": "(overlap_index +1)/18; overlap_index=0..17"},
        "speed": {"accepted_prefix_factor": 1.0, "F04_factor": 1.0, "output_clock_fps": FPS,
                  "native_frame_order_preserved": True, "retime": False,
                  "freeze_reverse_repeat_interpolation": False, "individual_source_PTS_measured": False},
        "framing_transform": "none; complete native720x1280 raster", "text": "none", "audio": "none",
        "sample_assets": samples, "QA_artifacts": artifacts,
        "technical_checks_are_visual_approval": False, "assistant_continuous_visual_review": None,
        "combined_dynamic_QA": "pending", "user_video_approval": None,
        "publishable": False, "cloud_write": False, "publication": False,
        "limitations": [
            "Invoke only after operator inspection of exact F04; this builder does not perform source visual QA.",
            "Accepted prefix pictures/order/joins are used as decoded media; output is re-encoded, not byte/pixel identical.",
            "New J34 necessarily blends the accepted prefix final18frames; no earlier transition is rebuilt.",
            "Full decode, sample boards and mapping do not establish identity, clothing, gait, site or transition acceptance.",
            "Normal-speed continuous review and exact user video approval remain separate; no five-look film approval inferred.",
            "24fps native frame sequence is retained; individual presentation timestamps were not measured.",
        ],
    }
    native.json_new(destination / "edit_receipt.json", value)
    return {"output": str(output), "sha256": value["output_sha256"], "frames": total,
            "seconds": total / FPS, "receipt": str(destination / "edit_receipt.json"), "QA": str(qa)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f04-sha", required=True, help="Exact lowercase SHA256 after operator source inspection")
    parser.add_argument("--version", default="v1", help="New exclusive output directory version:v1,v2,...")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.f04_sha, args.version), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
