"""Read one source; save separate decode evidence and native-frame QA images.

No video is rendered, retimed, cropped for delivery or changed. Contact windows
are inspection-only crops, not a footwear/body detector or a visual pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "10_automation").is_dir())
sys.path.insert(0, str(ROOT / "10_automation"))
sys.path.insert(0, str(ROOT / "10_automation/.video_dependencies"))

import imageio_ffmpeg
from scan_reel_video import scan


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def uniform_indices(count, requested):
    actual = min(count, requested)
    if actual == 1:
        return [0]
    return sorted({round(index * (count - 1) / (actual - 1)) for index in range(actual)})


def parse_roi(value):
    try:
        rect = tuple(int(part.strip()) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use native-pixel x,y,width,height") from exc
    if len(rect) != 4 or min(rect[:2]) < 0 or min(rect[2:]) <= 0:
        raise argparse.ArgumentTypeError("Use nonnegative x,y and positive width,height")
    return rect


def crop(frame, roi):
    x, y, width, height = roi
    return frame.crop((x, y, x + width, y + height))


def board(samples, path, fps, tile, columns, title):
    tile_width, tile_height = tile
    label_height, header_height = 25, 30
    rows = math.ceil(len(samples) / columns)
    canvas = Image.new("RGB", (tile_width * columns, header_height + rows * (tile_height + label_height)), "#f5f3ef")
    draw = ImageDraw.Draw(canvas)
    draw.text((7, 8), title, fill="black")
    for slot, (index, frame) in enumerate(samples):
        picture = frame.copy()
        picture.thumbnail((tile_width - 8, tile_height - 6), Image.Resampling.LANCZOS)
        x, y = (slot % columns) * tile_width, header_height + (slot // columns) * (tile_height + label_height)
        draw.text((x + 4, y + 6), f"f{index} / nominal {index / fps:.3f}s", fill="black")
        canvas.paste(picture, (x + (tile_width - picture.width) // 2,
                              y + label_height + (tile_height - picture.height) // 2))
    canvas.save(path, quality=95)


def inspect(source, output, label, face_roi, contact_roi, contact_until):
    before = sha256(source)
    analysis = scan(source)
    meta = analysis["metadata"]
    fps = float(meta["fps"])
    count = int(analysis["decoded_frames"])
    width, height = map(int, meta["size"])
    if fps <= 0 or not math.isfinite(fps) or count <= 0:
        raise ValueError("Source has no positive observed frame count/fps")

    full_indices = uniform_indices(count, 25)
    face_indices = uniform_indices(count, 5)
    # The default head window is deliberately broader than a detected face.
    face_roi = face_roi or (round(width * 0.22), 0, round(width * 0.56), round(height * 0.32))
    # Lower central window retains floor, both feet and lower dress motion.
    contact_y = round(height * 0.60)
    contact_roi = contact_roi or (round(width * 0.13), contact_y, round(width * 0.74), height - contact_y)
    for role, roi in (("face", face_roi), ("contact", contact_roi)):
        if roi[0] + roi[2] > width or roi[1] + roi[3] > height:
            raise ValueError(f"{role} inspection window exceeds actual {width}x{height}")
    last_contact = min(count - 1, math.floor(contact_until * fps + 1e-9))
    contact_indices = list(range(last_contact + 1))
    selected = set(full_indices) | set(face_indices) | set(contact_indices)

    output.mkdir(parents=True)
    for name in ("full", "face", "contact"):
        (output / name).mkdir()
    save_json(output / "decode_scan.json", analysis)
    save_json(output / "actual_metadata.json", {
        "source": str(source), "source_sha256": before, "source_bytes": source.stat().st_size,
        "metadata": meta, "native_size": [width, height], "observed_fps": fps,
        "complete_decoded_frames": count, "frame_count_over_fps_seconds": count / fps,
        "native_timestamp_limit": "Time labels are frame index / observed fps; individual PTS not measured.",
    })

    reader = imageio_ffmpeg.read_frames(str(source), pix_fmt="rgb24")
    extraction_meta = next(reader)
    if tuple(extraction_meta["size"]) != (width, height) or not math.isclose(float(extraction_meta["fps"]), fps, rel_tol=1e-9):
        raise ValueError("Decode and extraction metadata differ")
    full_samples, face_samples, contact_samples, records = [], [], [], []
    extracted_count = 0
    for index, raw in enumerate(reader):
        extracted_count = index + 1
        if index not in selected:
            continue
        frame = Image.frombytes("RGB", (width, height), raw)
        row = {"native_frame_index": index, "nominal_seconds_from_fps": index / fps}
        if index in full_indices:
            name = f"full/frame_{index:06d}.png"
            frame.save(output / name)
            row["native_full_image"] = name
            full_samples.append((index, frame))
        if index in face_indices:
            face = crop(frame, face_roi)
            name = f"face/window_{index:06d}.png"
            face.save(output / name)
            row["face_inspection_image"] = name
            face_samples.append((index, face))
        if index in contact_indices:
            contact = crop(frame, contact_roi)
            name = f"contact/window_{index:06d}.png"
            contact.save(output / name)
            row["contact_inspection_image"] = name
            contact_samples.append((index, contact))
        records.append(row)

    if extracted_count != count or len(full_samples) != len(full_indices) or len(face_samples) != len(face_indices) or len(contact_samples) != len(contact_indices):
        raise ValueError("Not all requested native images extracted, or full decode counts differ")
    if sha256(source) != before:
        raise ValueError("Source hash changed during read-only inspection")

    board(full_samples, output / "full_25_checkpoints.jpg", fps, (208, 368), 5,
          f"{label} native full frames; sampled QA, not continuous visual review")
    board(face_samples, output / "face_5_checkpoints.jpg", fps, (285, 330), 5,
          f"{label} fixed head windows; not face detection, no identity pass implied")
    contact_boards = []
    # Three sheets for a usual six-second/24fps source (73 early-frame windows).
    per_sheet = 25
    for start in range(0, len(contact_samples), per_sheet):
        name = f"contact_sequence_{start // per_sheet + 1:02d}.jpg"
        board(contact_samples[start:start + per_sheet], output / name, fps, (246, 238), 5,
              f"{label} consecutive native foot/floor inspection; no interpolated frames")
        contact_boards.append(name)

    receipt = {
        "status": "qa_assets_ready_independent_visual_review_pending",
        "label": label, "source": str(source), "source_sha256": before,
        "native_size": [width, height], "observed_fps": fps, "decoded_frames": count,
        "decoded_seconds": count / fps,
        "full_checkpoint_indices": full_indices, "face_checkpoint_indices": face_indices,
        "contact_consecutive_indices": contact_indices,
        "contact_requested_end_seconds": contact_until,
        "contact_actual_last_nominal_seconds": last_contact / fps,
        "face_roi_native_xywh": list(face_roi), "contact_roi_native_xywh": list(contact_roi),
        "roi_method": "explicit or broad fixed native-pixel QA windows; no face/body detection",
        "boards": {"full": "full_25_checkpoints.jpg", "face": "face_5_checkpoints.jpg", "contact": contact_boards},
        "images": records, "source_mutated": False, "video_rendered": False,
        "native_speed_changed": False, "native_frame_extraction": True,
        "camera_fixed_observed": None, "backward_step_observed": None,
        "cloth_information_gain": None, "continuous_visual_review": "not_claimed", "user_approval": None,
        "limits": [
            "Complete decode only confirms decoding and technical signals, not visual quality.",
            "25 full frames and 5 head windows are samples, not a normal-speed complete watch.",
            "The early contact sequence covers consecutive native frames only through the selected endpoint.",
            "Nominal labels are native frame index / observed fps, not measured individual PTS.",
            "Prompts/settings do not establish that the camera stayed fixed or a step occurred.",
        ],
    }
    save_json(output / "inspection_manifest.json", receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--label", default="A")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--face-roi", type=parse_roi)
    parser.add_argument("--contact-roi", type=parse_roi)
    parser.add_argument("--contact-until", type=float, default=3.0)
    args = parser.parse_args()
    source, output = args.source.resolve(), args.out_dir.resolve()
    if not source.is_file():
        parser.error("Source file missing; do not inspect a pending download")
    if not output.is_relative_to(HERE) or output == HERE or output.exists():
        parser.error("Choose a new QA subdirectory inside backward_step_trial")
    if not math.isfinite(args.contact_until) or args.contact_until < 0:
        parser.error("Contact endpoint must be a finite nonnegative second value")
    receipt = inspect(source, output, args.label, args.face_roi, args.contact_roi, args.contact_until)
    print(json.dumps({key: receipt[key] for key in (
        "status", "source", "source_sha256", "native_size", "observed_fps", "decoded_frames",
        "decoded_seconds", "full_checkpoint_indices", "face_checkpoint_indices", "contact_actual_last_nominal_seconds"
    )}, ensure_ascii=False))


if __name__ == "__main__":
    main()
