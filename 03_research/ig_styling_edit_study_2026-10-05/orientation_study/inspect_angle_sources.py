"""Read new angle sources and create separate QA images; never render a video.

Example (from the project root):
  python -X utf8 path/to/inspect_angle_sources.py --source-a path/to/A.mp4 \
      --source-b path/to/B.mp4 --out-dir path/to/orientation_study/qa/recovery_01

Inputs are read only. The QA directory must be new and remain inside this study.
Face windows are explicit fixed inspection regions, not detected face bounds.
"""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "10_automation"))
sys.path.insert(0, str(ROOT / "10_automation/.video_dependencies"))

import imageio_ffmpeg
from scan_reel_video import scan


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def uniform_indices(frame_count, desired_count):
    count = min(frame_count, desired_count)
    if count == 1:
        return [0]
    return sorted({round(i * (frame_count - 1) / (count - 1)) for i in range(count)})


def parse_roi(value):
    try:
        rect = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use native-pixel x,y,width,height.") from exc
    if len(rect) != 4 or min(rect[:2]) < 0 or min(rect[2:]) <= 0:
        raise argparse.ArgumentTypeError("Use nonnegative x,y and positive width,height.")
    return rect


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def checkpoint_board(samples, output, fps, tile_size, columns):
    tile_w, tile_h = tile_size
    label_h = 28
    rows = math.ceil(len(samples) / columns)
    board = Image.new("RGB", (columns * tile_w, rows * (tile_h + label_h)), "white")
    draw = ImageDraw.Draw(board)
    for position, (frame_index, frame) in enumerate(samples):
        item = frame.copy()
        item.thumbnail((tile_w - 8, tile_h - 8), Image.Resampling.LANCZOS)
        x = (position % columns) * tile_w
        y = (position // columns) * (tile_h + label_h)
        draw.text((x + 4, y + 5), f"f{frame_index} / {frame_index / fps:.3f}s", fill="black")
        board.paste(item, (x + (tile_w - item.width) // 2,
                          y + label_h + (tile_h - item.height) // 2))
    board.save(output, quality=95)


def inspect_source(label, source, qa_root, requested_face_roi):
    before_hash = sha256(source)
    analysis = scan(source)
    metadata = analysis["metadata"]
    fps = float(metadata["fps"])
    frame_count = int(analysis["decoded_frames"])
    width, height = map(int, metadata["size"])
    if not math.isfinite(fps) or fps <= 0 or frame_count <= 0:
        raise ValueError(f"{label}: source needs a positive observed fps/frame count")

    full_indices = uniform_indices(frame_count, 25)
    face_indices = uniform_indices(frame_count, 5)
    if requested_face_roi is None:
        # Broad central upper-quarter window: includes head motion for inspection.
        x = round(width * 0.25)
        roi = (x, 0, width - 2 * x, round(height * 0.25))
        roi_method = "fixed central upper-quarter inspection window; not face detection"
    else:
        roi = requested_face_roi
        roi_method = "explicit native-pixel inspection window; not face detection"
    x, y, roi_w, roi_h = roi
    if x + roi_w > width or y + roi_h > height:
        raise ValueError(f"{label}: face inspection ROI {roi} exceeds {width}x{height}")

    folder = qa_root / label
    folder.mkdir()
    full_samples, face_samples = [], []
    image_records = []
    target_indices = set(full_indices) | set(face_indices)
    reader = imageio_ffmpeg.read_frames(str(source), pix_fmt="rgb24")
    extracted_metadata = next(reader)
    if tuple(extracted_metadata["size"]) != (width, height):
        raise ValueError(f"{label}: extraction dimensions differ from scan")
    if not math.isclose(float(extracted_metadata["fps"]), fps, rel_tol=1e-9):
        raise ValueError(f"{label}: extraction fps differs from scan")

    extracted_count = 0
    for frame_index, raw in enumerate(reader):
        extracted_count = frame_index + 1
        if frame_index not in target_indices:
            continue
        frame = Image.frombytes("RGB", (width, height), raw)
        record = {"native_frame_index": frame_index,
                  "nominal_seconds_from_fps": frame_index / fps}
        if frame_index in full_indices:
            name = f"native_frame_{frame_index:06d}.png"
            frame.save(folder / name)
            full_samples.append((frame_index, frame))
            record["native_image"] = name
        if frame_index in face_indices:
            face = frame.crop((x, y, x + roi_w, y + roi_h))
            name = f"face_window_{frame_index:06d}.png"
            face.save(folder / name)
            face_samples.append((frame_index, face))
            record["face_window_image"] = name
        image_records.append(record)

    if extracted_count != frame_count:
        raise ValueError(f"{label}: scan/extraction frame counts differ")
    if len(full_samples) != len(full_indices) or len(face_samples) != len(face_indices):
        raise ValueError(f"{label}: requested native frames were not all extracted")
    if sha256(source) != before_hash:
        raise ValueError(f"{label}: source changed during read-only inspection")

    checkpoint_board(full_samples, folder / "native_25_checkpoints.jpg", fps, (184, 328), 5)
    checkpoint_board(face_samples, folder / "face_5_checkpoints.jpg", fps, (288, 328), 5)
    receipt = dict(
        label=label,
        source_path=str(source),
        source_sha256=before_hash,
        source_bytes=source.stat().st_size,
        scan=analysis,
        native_size=[width, height],
        observed_fps=fps,
        decoded_frames=frame_count,
        decoded_seconds=frame_count / fps,
        native_frame_indices=full_indices,
        native_checkpoint_count=len(full_samples),
        face_frame_indices=face_indices,
        face_checkpoint_count=len(face_samples),
        face_roi_native_xywh=list(roi),
        face_roi_method=roi_method,
        image_records=image_records,
        output_folder=str(folder),
        video_rendered=False,
        source_mutated=False,
        speed_changed=False,
        native_index_extraction=True,
        timestamps_note="Labels use frame index / observed fps; exact source PTS were not measured.",
        sampled_visual_review="pending",
        continuous_visual_review="not_claimed",
        user_approval=None,
        warning="Decode/signals and QA assets do not establish visual quality or approval.",
    )
    save_json(folder / "inspection_receipt.json", receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-a", type=Path, help="New A original; read only")
    parser.add_argument("--source-b", type=Path, help="New B original; read only")
    parser.add_argument("--out-dir", type=Path, required=True, help="New QA folder inside orientation_study")
    parser.add_argument("--face-roi-a", type=parse_roi, help="Optional native x,y,width,height")
    parser.add_argument("--face-roi-b", type=parse_roi, help="Optional native x,y,width,height")
    args = parser.parse_args()
    sources = [(label, path.resolve(), roi) for label, path, roi in (
        ("A", args.source_a, args.face_roi_a), ("B", args.source_b, args.face_roi_b)
    ) if path is not None]
    if not sources:
        parser.error("Supply --source-a and/or --source-b.")
    for label, source, _ in sources:
        if not source.is_file():
            parser.error(f"{label}: source is missing: {source}")

    output = args.out_dir.resolve()
    if not output.is_relative_to(HERE) or output == HERE:
        parser.error("QA output must stay in a new subdirectory of orientation_study.")
    if output.exists():
        parser.error("Preserve existing QA: choose a new output directory.")
    output.mkdir(parents=True)
    receipts = [inspect_source(label, source, output, roi) for label, source, roi in sources]
    manifest = dict(status="inspection_assets_ready_visual_review_pending",
                    sources=receipts, video_rendered=False, protected_outputs_written=False)
    save_json(output / "inspection_manifest.json", manifest)
    print(json.dumps({"qa_directory": str(output), "sources": [
        {key: item[key] for key in ("label", "native_size", "observed_fps", "decoded_frames",
                                   "native_checkpoint_count", "face_checkpoint_count", "source_sha256")}
        for item in receipts]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
