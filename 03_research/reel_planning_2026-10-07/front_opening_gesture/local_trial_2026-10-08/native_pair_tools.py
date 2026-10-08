"""Native source QA and isolated two-source composition for the 2026-10-08 trial.

This helper never generates motion, approves visual quality, uploads, or publishes.
Delivery frames remain their complete 720x1280 raster at the native 24 fps.
Only inspection head-window images are cropped; those never enter the video.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "10_automation").is_dir())
sys.path.insert(0, str(ROOT / "10_automation/.video_dependencies"))
from PIL import Image, ImageDraw
import imageio_ffmpeg

SIZE, FPS, OVERLAP = (720, 1280), 24, 18
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
NAME_RE = re.compile(r"[A-Za-z0-9_-]+\Z")


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path):
    with path.open("r", encoding="utf-8-sig") as stream:
        return json.load(stream)


def json_new(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def image_new(path, image):
    with path.open("xb") as stream:
        image.save(stream, format="JPEG" if path.suffix.lower() == ".jpg" else "PNG",
                   **({"quality": 95} if path.suffix.lower() == ".jpg" else {}))


def require_sha(value):
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        raise ValueError("Expected a 64-character lowercase SHA256")
    return value


def verified_source(raw_path, expected):
    source = Path(raw_path).resolve()
    require_sha(expected)
    if not source.is_file() or digest(source) != expected:
        raise ValueError(f"Source missing or hash differs: {source}")
    return source


def destination(raw_path):
    path = Path(raw_path)
    path = path.resolve() if path.is_absolute() else (HERE / path).resolve()
    if path == HERE or not path.is_relative_to(HERE):
        raise ValueError("Outputs must use a new child directory inside this local trial")
    if os.path.lexists(path):
        raise FileExistsError(f"Preserve existing output/QA: {path}")
    return path


def protected_inputs():
    """Read current exact stills and the eight historical protected-media hashes."""
    story = read_json(HERE.parent / "storyboard.json")
    historical = read_json(ROOT / "03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/M02_body_distance_review_v1.json")
    records = [{"path": item["source"], "sha256": item["sha256"], "role": item["role"]}
               for item in story["assets"]]
    records.extend({"path": item["path"], "sha256": item["sha256"], "role": "protected_historical_media"}
                   for item in historical["protected_media"])
    for item in records:
        path = (ROOT / item["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or digest(path) != item["sha256"]:
            raise ValueError(f"Protected input changed or missing: {item['path']}")
    return records


def require_native(meta):
    if tuple(meta.get("size", ())) != SIZE or tuple(meta.get("source_size", ())) != SIZE:
        raise ValueError("Require native unrotated 720x1280; never stretch or crop")
    rate = meta.get("fps")
    if not isinstance(rate, (int, float)) or not math.isclose(rate, FPS, abs_tol=1e-8, rel_tol=0):
        raise ValueError(f"Require native 24 fps; observed {rate!r}")


@contextmanager
def native_reader(path):
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt="rgb24")
    try:
        require_native(next(reader))
        yield reader
    finally:
        reader.close()


def full_decode(path):
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt="rgb24")
    try:
        meta = next(reader)
        require_native(meta)
        count = 0
        for raw in reader:
            if len(raw) != SIZE[0] * SIZE[1] * 3:
                raise ValueError("Unexpected native RGB frame byte count")
            count += 1
        if not count:
            raise ValueError("Source decoded zero frames")
    finally:
        reader.close()
    return {"metadata": meta, "decoded_frames": count, "full_decode_completed": True,
            "frame_count_over_fps_seconds": count / FPS,
            "individual_PTS_measured": False}


def require_interval(start, end, decoded, minimum=1):
    if not 0 <= start < end <= decoded or end - start < minimum:
        raise ValueError(f"Invalid native half-open interval [{start},{end}); decoded={decoded}")


def selected_frames(path, start, end):
    with native_reader(path) as reader:
        for index, raw in enumerate(reader):
            if index >= end:
                break
            if index >= start:
                yield Image.frombytes("RGB", SIZE, raw)


def uniform(start, end, requested):
    count = min(end - start, requested)
    if count == 1:
        return [start]
    return sorted({start + round(i * (end - start - 1) / (count - 1)) for i in range(count)})


def sheet(items, path, title, head=False):
    columns, tile_w, tile_h = 5, 208, (270 if head else 368)
    canvas = Image.new("RGB", (columns * tile_w, 30 + math.ceil(len(items) / columns) * (tile_h + 25)), "#f5f3ef")
    draw = ImageDraw.Draw(canvas)
    draw.text((6, 8), title, fill="black")
    for slot, (index, source) in enumerate(items):
        image = source.crop((158, 0, 562, 448)) if head else source.copy()
        image.thumbnail((tile_w - 8, tile_h - 6), Image.Resampling.LANCZOS)
        x, y = slot % columns * tile_w, 30 + slot // columns * (tile_h + 25)
        draw.text((x + 4, y + 5), f"f{index} / {index / FPS:.3f}s", fill="black")
        canvas.paste(image, (x + (tile_w - image.width) // 2, y + 25 + (tile_h - image.height) // 2))
    image_new(path, canvas)


def extract_boards(source, output, start, end, boundary=None):
    full = uniform(start, end, 25)
    face = uniform(start, end, 5)
    boundary = list(boundary or [])
    keep = set(full) | set(face) | set(boundary)
    full_items, face_items, boundary_items = [], [], []
    frames = output / "frames"
    frames.mkdir()
    with native_reader(source) as reader:
        for index, raw in enumerate(reader):
            if index >= end:
                break
            if index not in keep:
                continue
            image = Image.frombytes("RGB", SIZE, raw)
            image_new(frames / f"frame_{index:06d}.png", image)
            if index in full:
                full_items.append((index, image))
            if index in face:
                face_items.append((index, image))
            if index in boundary:
                boundary_items.append((index, image))
    if len(full_items) != len(full) or len(face_items) != len(face) or len(boundary_items) != len(boundary):
        raise ValueError("Native extraction did not produce all requested frames")
    sheet(full_items, output / "full_25_checkpoints.jpg", "Native full-frame samples; visual review pending")
    sheet(face_items, output / "face_5_checkpoints.jpg", "QA-only fixed head windows; no identity pass", head=True)
    if boundary:
        sheet(boundary_items, output / "transition_all_boundary_frames.jpg", "All 18 dissolve frames and eight frames each side")
        sheet(boundary_items, output / "transition_all_boundary_head_windows.jpg", "QA-only head windows for every boundary frame", head=True)
    return {"full_checkpoint_indices": full, "face_checkpoint_indices": face,
            "transition_boundary_indices": boundary,
            "head_window_native_xyxy": [158, 0, 562, 448],
            "head_window_is_inspection_only": True}


def base_receipt():
    return {"date": "2026-10-08", "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "execution": "local", "model": "M02",
            "look_ids": ["2026-W37-001-L01", "2026-W37-001-L02"],
            "text": "none", "audio": "none", "retime_freeze_reverse_replay": False,
            "forced_action_synchronization": False, "delivery_framing_transform": "none; entire native raster",
            "technical_checks_are_visual_approval": False,
            "assistant_continuous_visual_review": False, "user_video_approval": None,
            "publishable": False, "cloud_write": False, "publication": False}


def inspect(args):
    source = verified_source(args.source, args.sha)
    protected = protected_inputs()
    scan = full_decode(source)
    end = scan["decoded_frames"] if args.end is None else args.end
    require_interval(args.start, end, scan["decoded_frames"])
    output = destination(args.out_dir)
    output.mkdir(parents=True)
    samples = extract_boards(source, output, args.start, end)
    verified_source(source, args.sha)
    protected_inputs()
    receipt = base_receipt()
    receipt.update({"status": "source_QA_assets_ready_visual_review_pending",
                    "audio": "source audio streams unverified by this helper; inspect actual stream metadata separately",
                    "source": str(source), "source_sha256": args.sha,
                    "source_full_decode": scan, "selected_native_frames_half_open": [args.start, end],
                    "sample_assets": samples, "protected_inputs_verified": protected,
                    "approved_sampled_dynamic_qa": None,
                    "limitations": ["25 full/5 head samples do not establish all-frame hand-cloth contact or full normal-speed playback.",
                                    "Record actual dynamic review separately; this helper never declares a pass."]})
    json_new(output / "inspection_manifest.json", receipt)
    return {"output_QA": str(output), "status": receipt["status"]}


def read_gate(raw_path, source_sha):
    path = Path(raw_path).resolve()
    before = digest(path)
    gate = read_json(path)
    if gate.get("source_sha256") != source_sha or gate.get("approved_sampled_dynamic_qa") is not True:
        raise ValueError("Actual external sampled dynamic QA must explicitly pass the exact source SHA")
    interval = gate.get("reviewed_native_frames_half_open")
    if not isinstance(interval, list) or len(interval) != 2 or not all(type(v) is int for v in interval) or not 0 <= interval[0] < interval[1]:
        raise ValueError("QA gate must state reviewed_native_frames_half_open")
    return path, before, gate


def encode_new(path, images):
    fd, name = tempfile.mkstemp(prefix=".native_pair_", suffix=".mp4", dir=path.parent)
    os.close(fd)
    temporary = Path(name)
    writer = imageio_ffmpeg.write_frames(str(temporary), SIZE, fps=FPS, codec="libx264",
        pix_fmt_in="rgb24", pix_fmt_out="yuv420p", quality=None, macro_block_size=1,
        ffmpeg_log_level="error", output_params=["-crf", "18", "-preset", "medium", "-movflags", "+faststart"])
    try:
        writer.send(None)
        for image in images:
            writer.send(image.tobytes())
        writer.close()
        if not temporary.is_file() or not temporary.stat().st_size:
            raise ValueError("No encoded video produced")
        with temporary.open("rb") as source, path.open("xb") as target:
            shutil.copyfileobj(source, target, 1024 * 1024)
    finally:
        writer.close()
        temporary.unlink(missing_ok=True)


def compose(args):
    if not NAME_RE.fullmatch(args.name):
        raise ValueError("Candidate name must be one simple filename component")
    a, b = verified_source(args.a, args.a_sha), verified_source(args.b, args.b_sha)
    if a == b or args.a_sha == args.b_sha:
        raise ValueError("Two distinct actual look sources are required")
    protected = protected_inputs()
    gate_a, gate_a_sha, gate_a_value = read_gate(args.a_qa, args.a_sha)
    gate_b, gate_b_sha, gate_b_value = read_gate(args.b_qa, args.b_sha)
    a_scan, b_scan = full_decode(a), full_decode(b)
    for start, end, scanned, gate in ((args.a_start, args.a_end, a_scan, gate_a_value),
                                     (args.b_start, args.b_end, b_scan, gate_b_value)):
        require_interval(start, end, scanned["decoded_frames"], OVERLAP + 1)
        reviewed = gate["reviewed_native_frames_half_open"]
        if not reviewed[0] <= start < end <= reviewed[1]:
            raise ValueError("Selected source interval falls outside actual reviewed interval")
    output = destination(args.out_dir)
    output.mkdir(parents=True)
    video = output / f"{args.name}.mp4"
    a_count, b_count = args.a_end - args.a_start, args.b_end - args.b_start
    total, mapping = a_count + b_count - OVERLAP, []
    stream_a, stream_b = selected_frames(a, args.a_start, args.a_end), selected_frames(b, args.b_start, args.b_end)

    def composite_frames():
        for offset in range(a_count - OVERLAP):
            mapping.append({"output_frame": len(mapping), "A_native_frame": args.a_start + offset,
                            "B_native_frame": None, "B_alpha": 0})
            yield next(stream_a)
        for offset in range(OVERLAP):
            alpha = (offset + 1) / OVERLAP
            mapping.append({"output_frame": len(mapping), "A_native_frame": args.a_end - OVERLAP + offset,
                            "B_native_frame": args.b_start + offset, "B_alpha": alpha})
            yield Image.blend(next(stream_a), next(stream_b), alpha)
        for offset in range(OVERLAP, b_count):
            mapping.append({"output_frame": len(mapping), "A_native_frame": None,
                            "B_native_frame": args.b_start + offset, "B_alpha": 1})
            yield next(stream_b)

    images = composite_frames()
    try:
        encode_new(video, images)
    finally:
        images.close()
        stream_a.close()
        stream_b.close()
    scan = full_decode(video)
    if scan["decoded_frames"] != total or len(mapping) != total:
        raise ValueError("Output native frame clock/count differs")
    qa = output / "QA"
    qa.mkdir()
    boundary = range(max(0, a_count - OVERLAP - 8), min(total, a_count + 8))
    samples = extract_boards(video, qa, 0, total, boundary)
    json_new(qa / "frame_mapping.json", mapping)
    json_new(qa / "full_decode.json", scan)
    verified_source(a, args.a_sha)
    verified_source(b, args.b_sha)
    if digest(gate_a) != gate_a_sha or digest(gate_b) != gate_b_sha:
        raise ValueError("Actual source QA receipt changed during composition")
    protected_inputs()
    receipt = base_receipt()
    receipt.update({"status": "research_candidate_pending_combined_visual_review",
                    "output": str(video), "output_sha256": digest(video),
                    "native_size": list(SIZE), "fps": FPS, "frames": total, "seconds": total / FPS,
                    "nominal_144_plus_144_expected_frames": 270,
                    "sources": [{"role": "A", "source": str(a), "sha256": args.a_sha,
                                 "selected_native_frames_half_open": [args.a_start, args.a_end], "full_decode": a_scan},
                                {"role": "B", "source": str(b), "sha256": args.b_sha,
                                 "selected_native_frames_half_open": [args.b_start, args.b_end], "full_decode": b_scan}],
                    "external_source_QA": [{"path": str(gate_a), "sha256": gate_a_sha},
                                           {"path": str(gate_b), "sha256": gate_b_sha}],
                    "transition": {"type": "linear_cross_dissolve", "frames": OVERLAP,
                                   "seconds": OVERLAP / FPS, "output_frames_half_open": [a_count - OVERLAP, a_count],
                                   "B_weight": "(overlap_index+1)/18"},
                    "sample_assets": samples, "protected_inputs_verified": protected,
                    "combined_sampled_dynamic_qa": "pending", "combined_continuous_review": "pending",
                    "user_video_approval": None,
                    "limitations": ["Source QA does not approve the combined dissolve or complete film.",
                                    "Normal-speed full playback and user visual approval remain separate gates.",
                                    "Gesture visibility and readable neckline/color information require actual review."]})
    json_new(output / f"{args.name}_receipt.json", receipt)
    return {"output": str(video), "frames": total, "seconds": total / FPS, "status": receipt["status"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    source = commands.add_parser("inspect")
    source.add_argument("--source", required=True)
    source.add_argument("--sha", required=True)
    source.add_argument("--start", type=int, default=0)
    source.add_argument("--end", type=int)
    source.add_argument("--out-dir", required=True)
    pair = commands.add_parser("compose")
    for role in ("a", "b"):
        pair.add_argument(f"--{role}", required=True)
        pair.add_argument(f"--{role}-sha", required=True)
        pair.add_argument(f"--{role}-qa", required=True)
        pair.add_argument(f"--{role}-start", type=int, default=0)
        pair.add_argument(f"--{role}-end", type=int, default=144)
    pair.add_argument("--out-dir", required=True)
    pair.add_argument("--name", default="M02_front_opening_review_v1")
    args = parser.parse_args()
    try:
        result = inspect(args) if args.command == "inspect" else compose(args)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
