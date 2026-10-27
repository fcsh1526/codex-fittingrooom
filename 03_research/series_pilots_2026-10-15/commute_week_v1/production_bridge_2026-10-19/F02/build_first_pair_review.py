"""Build the isolated F01/F02 research preview after the source review.

Run only after an operator has inspected the exact F02_source.mp4. Supply its
SHA256 using --f02-sha. This script does not establish visual approval.

F01 native frames [0,78) + all F02 native frames, one 18-frame cross-dissolve.
Native 720x1280 / 24 fps; no crop, scale, speed change, new motion, text or audio.
Existing sources are read-only; an existing output, receipt or QA folder aborts.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "10_automation").is_dir())
sys.path.insert(0, str(ROOT / "10_automation/.video_dependencies"))
import imageio_ffmpeg
from PIL import Image, ImageDraw

SIZE = (720, 1280)
FPS = 24
A_COUNT = 78
OVERLAP = 18
JOIN_START = A_COUNT - OVERLAP
F01_SHA = "6a9bf3204aadad28dc710aa914592e26851a03e47209c5bd9b682286b184fa50"
F01 = HERE.parent / "F01/F01_source.mp4"
F02 = HERE / "F02_source.mp4"
OUTPUT = HERE / "F01_F02_soft_join_review_v1.mp4"
RECEIPT = HERE / "F01_F02_soft_join_review_v1_receipt.json"
QA = HERE / "QA_pair"


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verified_source(path: Path, expected_sha: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
        raise ValueError("Expected a lowercase 64-character source SHA256")
    if not path.is_file() or sha256(path) != expected_sha:
        raise ValueError(f"Source missing or exact SHA256 differs: {path}")
    return path


def json_new(path: Path, value) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def image_new(path: Path, value: Image.Image) -> None:
    with path.open("xb") as stream:
        value.save(stream, format="PNG")


def require_native(metadata: dict) -> None:
    if tuple(metadata.get("size", ())) != SIZE or tuple(metadata.get("source_size", ())) != SIZE:
        raise ValueError("Require native, unrotated 720x1280; do not crop, scale or stretch")
    rate = metadata.get("fps")
    if not isinstance(rate, (int, float)) or not math.isclose(rate, FPS, abs_tol=1e-8, rel_tol=0):
        raise ValueError(f"Require native 24 fps, observed {rate!r}")


@contextmanager
def native_reader(path: Path):
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt="rgb24")
    try:
        require_native(next(reader))
        yield reader
    finally:
        reader.close()


def full_decode(path: Path) -> dict:
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt="rgb24")
    try:
        metadata = next(reader)
        require_native(metadata)
        count = 0
        for raw in reader:
            if len(raw) != SIZE[0] * SIZE[1] * 3:
                raise ValueError("Unexpected native RGB frame size")
            count += 1
        if count == 0:
            raise ValueError("Video decoded zero frames")
    finally:
        reader.close()
    return {
        "metadata": metadata,
        "decoded_frames": count,
        "full_decode_completed": True,
        "decoded_frames_over_native_fps_seconds": count / FPS,
        "individual_source_PTS_measured": False,
    }


def selected_frames(path: Path, end: int):
    with native_reader(path) as reader:
        for index, raw in enumerate(reader):
            if index >= end:
                break
            yield Image.frombytes("RGB", SIZE, raw)


def encode_new(path: Path, images) -> None:
    descriptor, name = tempfile.mkstemp(prefix=".F01_F02_", suffix=".mp4", dir=HERE)
    os.close(descriptor)
    temporary = Path(name)
    writer = imageio_ffmpeg.write_frames(
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
            raise ValueError("Encoder did not produce a video")
        # Exclusive creation prevents even a concurrent run from overwriting media.
        with temporary.open("rb") as source, path.open("xb") as target:
            shutil.copyfileobj(source, target, 1024 * 1024)
    finally:
        writer.close()
        temporary.unlink(missing_ok=True)


def stream_inventory(path: Path) -> dict:
    result = subprocess.run(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-i", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    # ffmpeg's input inspection exits nonzero without an output; inspect stream lines.
    lines = [line.strip() for line in result.stderr.splitlines() if "Stream #" in line]
    if not any("Video:" in line for line in lines):
        raise ValueError("Unable to inspect encoded output streams")
    return {"streams": lines, "audio_stream_present": any("Audio:" in line for line in lines)}


def uniform_indices(total: int, requested: int = 25) -> list[int]:
    count = min(total, requested)
    return [0] if count == 1 else sorted({round(i * (total - 1) / (count - 1)) for i in range(count)})


def contact_sheet(items, path: Path, title: str) -> None:
    columns, cell_width, cell_height = 5, 216, 408
    sheet = Image.new("RGB", (columns * cell_width, 30 + math.ceil(len(items) / columns) * cell_height), "#f5f3ef")
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 8), title, fill="black")
    for slot, (index, frame) in enumerate(items):
        tile = frame.copy()
        tile.thumbnail((cell_width - 8, cell_height - 30), Image.Resampling.LANCZOS)
        x, y = slot % columns * cell_width, 30 + slot // columns * cell_height
        draw.text((x + 4, y + 4), f"f{index} / {index / FPS:.3f}s", fill="black")
        sheet.paste(tile, (x + (cell_width - tile.width) // 2, y + 25))
    image_new(path, sheet)


def extract_boards(path: Path, total: int) -> dict:
    full = uniform_indices(total)
    boundary = list(range(max(0, JOIN_START - 8), min(total, A_COUNT + 8)))
    keep = set(full) | set(boundary)
    frames_dir = QA / "frames"
    frames_dir.mkdir()
    found = {}
    with native_reader(path) as reader:
        for index, raw in enumerate(reader):
            if index not in keep:
                continue
            frame = Image.frombytes("RGB", SIZE, raw)
            image_new(frames_dir / f"frame_{index:06d}.png", frame)
            found[index] = frame
    if set(found) != keep:
        raise ValueError("Not all requested QA checkpoints were extracted")
    contact_sheet([(index, found[index]) for index in full], QA / "full_25_checkpoints.png", "Full-raster samples; visual review pending")
    contact_sheet([(index, found[index]) for index in boundary], QA / "transition_all_boundary_frames.png", "18 dissolve frames + 8 frames each side; review pending")
    return {
        "full_checkpoint_indices": full,
        "transition_boundary_indices": boundary,
        "all_18_transition_frames_extracted": all(index in found for index in range(JOIN_START, A_COUNT)),
        "individual_QA_frames_size": list(SIZE),
        "QA_contact_sheets_are_reduced_full_raster_thumbnails": True,
        "QA_frame_crop": False,
    }


def build(f02_sha: str) -> dict:
    # Check every destination before any write. Preserve partial output after failure.
    for path in (OUTPUT, RECEIPT, QA):
        if os.path.lexists(path):
            raise FileExistsError(f"Preserve existing output or QA; choose a new version manually: {path}")
    verified_source(F01, F01_SHA)
    verified_source(F02, f02_sha)
    a_scan, b_scan = full_decode(F01), full_decode(F02)
    if a_scan["decoded_frames"] < A_COUNT or b_scan["decoded_frames"] <= OVERLAP:
        raise ValueError("F01 must contain [0,78); F02 needs more than 18 native frames")
    b_count = b_scan["decoded_frames"]
    total = A_COUNT + b_count - OVERLAP
    mapping = []
    a_stream = selected_frames(F01, A_COUNT)
    b_stream = selected_frames(F02, b_count)

    def composite():
        for index in range(JOIN_START):
            mapping.append({"output_frame": index, "F01_native_frame": index, "F02_native_frame": None, "F02_alpha": 0})
            yield next(a_stream)
        for index in range(OVERLAP):
            alpha = (index + 1) / OVERLAP
            mapping.append({"output_frame": JOIN_START + index, "F01_native_frame": JOIN_START + index,
                            "F02_native_frame": index, "F02_alpha": alpha})
            yield Image.blend(next(a_stream), next(b_stream), alpha)
        for index in range(OVERLAP, b_count):
            mapping.append({"output_frame": JOIN_START + index, "F01_native_frame": None,
                            "F02_native_frame": index, "F02_alpha": 1})
            yield next(b_stream)

    frames = composite()
    try:
        encode_new(OUTPUT, frames)
    finally:
        frames.close()
        a_stream.close()
        b_stream.close()
    output_scan = full_decode(OUTPUT)
    if output_scan["decoded_frames"] != total or len(mapping) != total:
        raise ValueError("Encoded count does not equal 78 + F02_N - 18")
    inventory = stream_inventory(OUTPUT)
    if inventory["audio_stream_present"]:
        raise ValueError("Silent research preview unexpectedly contains an audio stream")
    QA.mkdir()
    samples = extract_boards(OUTPUT, total)
    json_new(QA / "frame_mapping.json", mapping)
    json_new(QA / "full_decode.json", output_scan)
    verified_source(F01, F01_SHA)
    verified_source(F02, f02_sha)
    qa_artifacts = [{"path": str(path.relative_to(HERE)), "sha256": sha256(path)}
                    for path in sorted(QA.rglob("*")) if path.is_file()]
    value = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "research_pair_candidate_pending_visual_review",
        "execution": "local", "model": "M03", "look_ids": ["L01", "L05"],
        "purpose": "First two segments of the continuous company-front commute research pilot",
        "builder_sha256": sha256(Path(__file__).resolve()),
        "sources": [
            {"role": "F01_L01", "path": str(F01), "sha256": F01_SHA,
             "selected_native_frames_half_open": [0, A_COUNT], "full_decode": a_scan},
            {"role": "F02_L05", "path": str(F02), "sha256": f02_sha,
             "selected_native_frames_half_open": [0, b_count], "full_decode": b_scan},
        ],
        "output": str(OUTPUT), "output_sha256": sha256(OUTPUT),
        "native_size": list(SIZE), "fps": FPS, "frames": total,
        "seconds": total / FPS, "frame_count_formula": "78 + F02_decoded_frames - 18",
        "output_full_decode": output_scan, "output_stream_inventory": inventory,
        "transition": {
            "type": "single_linear_cross_dissolve", "frames": OVERLAP, "seconds": OVERLAP / FPS,
            "output_frames_half_open": [JOIN_START, A_COUNT],
            "output_seconds_half_open": [JOIN_START / FPS, A_COUNT / FPS],
            "F01_native_frames_half_open": [JOIN_START, A_COUNT],
            "F02_native_frames_half_open": [0, OVERLAP],
            "F02_weight": "(overlap_index + 1) / 18; overlap_index = 0..17",
        },
        "speed": {"F01_factor": 1.0, "F02_factor": 1.0, "output_clock_fps": FPS,
                  "native_frame_order_preserved": True, "retime": False,
                  "freeze_reverse_repeat_interpolation": False,
                  "individual_source_PTS_measured": False},
        "framing_transform": "none; complete native 720x1280 raster",
        "text": "none", "audio": "none; output stream inspection confirms no Audio stream",
        "sample_assets": samples, "QA_artifacts": qa_artifacts,
        "sources_verified_unchanged_after_encode": True,
        "technical_checks_are_visual_approval": False,
        "assistant_continuous_visual_review": None, "combined_dynamic_QA": "pending",
        "user_video_approval": None, "publishable": False,
        "cloud_write": False, "publication": False,
        "limitations": [
            "Invocation is for the root-reviewed exact F02 source; this builder does not perform visual source QA.",
            "Full decode, checkpoints and exact frame mapping do not approve identity, clothing, gait, scene continuity or the dissolve.",
            "Normal-speed complete playback and user review remain separate; no final five-look film acceptance is inferred.",
            "Decoded native frame order is retained on a 24fps output clock; individual source presentation timestamps were not measured.",
        ],
    }
    json_new(RECEIPT, value)
    return {"output": str(OUTPUT), "sha256": value["output_sha256"],
            "frames": total, "seconds": total / FPS, "receipt": str(RECEIPT), "QA": str(QA)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f02-sha", required=True, help="Exact SHA256 of F02_source.mp4 after the root's source inspection")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.f02_sha), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
