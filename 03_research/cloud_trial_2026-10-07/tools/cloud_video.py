"""Portable, isolated M02 packet checks and native-frame candidate composition.

Run from any directory: python tools/cloud_video.py preflight --execution-label local
Then, only after a human/agent has actually reviewed the new source B:
python tools/cloud_video.py compose --b-sha <sha256> --execution-label cloud

The execution label is a declaration, never evidence of cloud execution. This
runner does not generate media, approve visual quality, upload, or publish.
It reads only packet-relative inputs and creates separate, non-overwriting outputs.
"""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
SIZE = (720, 1280)
FPS = 24
OVERLAP = 18
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")


def safe_path(relative):
    """Reject absolute/drive/parent paths and symlinks resolving outside packet."""
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise ValueError(f"Expected a portable packet-relative path: {relative!r}")
    clean = PurePosixPath(relative)
    if clean.is_absolute() or any(part in ("", ".", "..") for part in relative.split("/")):
        raise ValueError(f"Unsafe packet path: {relative!r}")
    path = ROOT.joinpath(*clean.parts)
    if not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError(f"Path escapes the packet: {relative!r}")
    return path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_sha(value):
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        raise ValueError("SHA256 must be exactly 64 lowercase hexadecimal characters")
    return value


def read_json(path):
    with path.open("r", encoding="utf-8-sig") as stream:
        return json.load(stream)


def verify_manifest(expected_manifest_sha=None):
    path = safe_path("inputs_manifest.json")
    before = sha256(path)
    if expected_manifest_sha is not None and before != expected_manifest_sha:
        raise ValueError("Input manifest changed during this operation")
    manifest = read_json(path)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list) or not manifest["files"]:
        raise ValueError("Manifest must contain a nonempty files list")
    checked, names, resolved = [], set(), set()
    for item in manifest["files"]:
        if not isinstance(item, dict) or not all(k in item for k in ("path", "sha256", "size_bytes", "role")):
            raise ValueError("Every manifest file needs path, sha256, size_bytes and role")
        relative, expected = item["path"], require_sha(item["sha256"])
        source = safe_path(relative)
        if relative in names or source.resolve() in resolved:
            raise ValueError(f"Duplicate manifest file: {relative}")
        names.add(relative)
        resolved.add(source.resolve())
        size = item["size_bytes"]
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ValueError(f"Invalid byte count: {relative}")
        if not isinstance(item["role"], str) or not item["role"]:
            raise ValueError(f"Missing file role: {relative}")
        if not source.is_file() or source.stat().st_size != size or sha256(source) != expected:
            raise ValueError(f"Missing, changed or wrong-size input: {relative}")
        checked.append(dict(item))
    if "inputs/source_A.mp4" not in names:
        raise ValueError("The exact inputs/source_A.mp4 must be declared in the manifest")
    if sha256(path) != before:
        raise ValueError("Input manifest changed while being read")
    return checked, before


def load_dependencies():
    modules, versions = {}, {}
    for name in ("PIL", "numpy", "imageio_ffmpeg"):
        try:
            module = importlib.import_module(name)
        except ImportError as error:
            raise RuntimeError(f"Missing dependency {name}; install tools/requirements.txt in this environment") from error
        modules[name] = module
        versions[name] = getattr(module, "__version__", "unknown")
    modules["Image"] = importlib.import_module("PIL.Image")
    modules["ImageDraw"] = importlib.import_module("PIL.ImageDraw")
    modules["imageio_ffmpeg"].get_ffmpeg_exe()
    return modules, versions


def require_native(metadata):
    if tuple(metadata.get("size", ())) != SIZE or tuple(metadata.get("source_size", ())) != SIZE:
        raise ValueError("Source/output must be native 720x1280 without rotation or resizing")
    rate = metadata.get("fps")
    if not isinstance(rate, (int, float)) or not math.isclose(rate, FPS, abs_tol=1e-8, rel_tol=0):
        raise ValueError(f"Source/output must be native 24 fps; observed {rate!r}")


def full_decode(path, ffmpeg):
    reader = ffmpeg.read_frames(str(path), pix_fmt="rgb24")
    try:
        metadata = next(reader)
        require_native(metadata)
        count = 0
        for raw in reader:
            if len(raw) != SIZE[0] * SIZE[1] * 3:
                raise ValueError("Decoded frame has unexpected byte count")
            count += 1
        if not count:
            raise ValueError("Video decoded no frames")
        return {"metadata": metadata, "decoded_frames": count,
                "native_duration_from_frame_count_seconds": count / FPS,
                "full_decode_completed": True}
    finally:
        reader.close()


def selected_frames(path, count, ffmpeg):
    reader = ffmpeg.read_frames(str(path), pix_fmt="rgb24")
    try:
        require_native(next(reader))
        for _ in range(count):
            try:
                raw = next(reader)
            except StopIteration as error:
                raise ValueError("Source ended before the selected native frame interval") from error
            if len(raw) != SIZE[0] * SIZE[1] * 3:
                raise ValueError("Decoded frame has unexpected byte count")
            yield raw
    finally:
        reader.close()


def require_absent(paths):
    for path in paths:
        if os.path.lexists(path):
            raise FileExistsError(f"Preserve prior output; refusing overwrite: {path.relative_to(ROOT)}")


def save_json(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def save_image(path, image, kind="PNG"):
    with path.open("xb") as stream:
        image.save(stream, format=kind, **({"quality": 95} if kind == "JPEG" else {}))


@contextmanager
def operation_lock(name):
    outputs = safe_path("outputs")
    outputs.mkdir(parents=True, exist_ok=True)
    lock = safe_path(f"outputs/.{name}.lock")
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(f"{os.getpid()}\n")
    try:
        yield
    finally:
        lock.unlink()


def encode_new(path, frames, ffmpeg):
    """Encode to an owned temporary file, then publish through exclusive creation."""
    require_absent([path])
    fd, name = tempfile.mkstemp(prefix=".m02_encode_", suffix=".mp4", dir=path.parent)
    os.close(fd)
    temp = Path(name)
    writer = ffmpeg.write_frames(
        str(temp), SIZE, fps=FPS, codec="libx264", pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p", quality=None, macro_block_size=1,
        ffmpeg_log_level="error", output_params=["-crf", "18", "-preset", "medium", "-movflags", "+faststart"],
    )
    try:
        writer.send(None)
        for raw in frames:
            writer.send(raw)
        writer.close()
        if not temp.is_file() or temp.stat().st_size == 0:
            raise ValueError("Encoder did not produce a usable file")
        with temp.open("rb") as source, path.open("xb") as target:
            shutil.copyfileobj(source, target, 1024 * 1024)
    finally:
        writer.close()
        temp.unlink(missing_ok=True)


def execution_receipt(label, versions):
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_label_declared_by_operator": label,
        "execution_environment_independently_verified": False,
        "cloud_execution_verified": False,
        "host_platform": platform.system(), "python_version": platform.python_version(),
        "dependency_versions": versions,
        "technical_checks_are_visual_approval": False,
        "user_visual_approval": None, "publishable": False,
        "cloud_generation_login_download_upload_and_publication_tested": False,
    }


def preflight(args, modules, versions):
    checked, manifest_sha = verify_manifest()
    ffmpeg = modules["imageio_ffmpeg"]
    source = safe_path("inputs/source_A.mp4")
    decoded = full_decode(source, ffmpeg)
    if decoded["decoded_frames"] < FPS:
        raise ValueError("Preflight requires at least 24 native frames")
    output = safe_path("outputs/preflight_A_1s.mp4")
    receipt = safe_path("outputs/preflight_A_1s_receipt.json")
    with operation_lock("preflight"):
        require_absent([output, receipt])
        selected = selected_frames(source, FPS, ffmpeg)
        try:
            encode_new(output, selected, ffmpeg)
        finally:
            selected.close()
        round_trip = full_decode(output, ffmpeg)
        if round_trip["decoded_frames"] != FPS:
            raise ValueError("Preflight round-trip frame count mismatch")
        verify_manifest(manifest_sha)
        info = execution_receipt(args.execution_label, versions)
        info.update({
            "status": "preflight_technical_checks_passed_cloud_execution_unproven",
            "verified_manifest_sha256": manifest_sha, "verified_input_files": checked,
            "source_A_full_decode": decoded,
            "selected_A_native_frames_half_open": [0, FPS],
            "output": output.relative_to(ROOT).as_posix(), "output_sha256": sha256(output),
            "round_trip_full_decode": round_trip,
            "round_trip_check_scope": "dimensions, native fps and decoded frame count; H264 is lossy, not pixel-identical",
            "framing_transform": "none", "source_retime": False,
            "text": "none", "audio": "none; video frames only",
            "input_hashes_and_sizes_reverified_after_encode": True,
        })
        save_json(receipt, info)
    return {"receipt": receipt.relative_to(ROOT).as_posix(), "output": info["output"],
            "status": info["status"], "cloud_execution_verified": False}


def new_board(indices, title, modules):
    Image, ImageDraw = modules["Image"], modules["ImageDraw"]
    columns, tile_w, tile_h = 5, 208, 393
    board = Image.new("RGB", (columns * tile_w, 30 + math.ceil(len(indices) / columns) * tile_h), "#f5f3ef")
    ImageDraw.Draw(board).text((5, 7), title, fill="black")
    return board, {frame: slot for slot, frame in enumerate(indices)}


def stamp_board(board, slot, frame, image, modules):
    thumb = image.copy()
    thumb.thumbnail((200, 362), modules["Image"].Resampling.LANCZOS)
    x, y = slot % 5 * 208, 30 + slot // 5 * 393
    modules["ImageDraw"].Draw(board).text((x + 4, y + 4), f"f{frame} / {frame / FPS:.3f}s", fill="black")
    board.paste(thumb, (x + (208 - thumb.width) // 2, y + 25 + (368 - thumb.height) // 2))


def compose(args, modules, versions):
    b_sha = require_sha(args.b_sha)
    checked, manifest_sha = verify_manifest()
    source_a, source_b = safe_path("inputs/source_A.mp4"), safe_path("outputs/source_B.mp4")
    qa_gate = safe_path("outputs/source_B_QA.json")
    if not source_b.is_file() or sha256(source_b) != b_sha:
        raise ValueError("New B source is missing or does not match --b-sha")
    if not qa_gate.is_file():
        raise ValueError("New B needs an actual external review in outputs/source_B_QA.json")
    gate_sha, gate = sha256(qa_gate), read_json(qa_gate)
    if not isinstance(gate, dict) or gate.get("approved_sampled_dynamic_qa") is not True or gate.get("source_sha256") != b_sha:
        raise ValueError("B sampled dynamic QA must be explicitly true and match the exact B SHA256")
    ffmpeg, Image = modules["imageio_ffmpeg"], modules["Image"]
    a_scan, b_scan = full_decode(source_a, ffmpeg), full_decode(source_b, ffmpeg)
    a_count, b_count = args.a_count, args.b_count
    if not OVERLAP < a_count <= a_scan["decoded_frames"] or not OVERLAP < b_count <= b_scan["decoded_frames"]:
        raise ValueError("Native frame selections must exceed 18 frames and fit decoded sources")
    total = a_count + b_count - OVERLAP
    if total < 25:
        raise ValueError("Candidate needs at least 25 native output frames for 25 distinct checkpoints")
    output = safe_path("outputs/M02_cloud_distance_candidate_v1.mp4")
    receipt = safe_path("outputs/M02_cloud_distance_candidate_v1_receipt.json")
    qa = safe_path("outputs/M02_cloud_distance_candidate_v1_QA")
    mapping = []
    with operation_lock("compose_v1"):
        require_absent([output, receipt, qa])
        a, b = selected_frames(source_a, a_count, ffmpeg), selected_frames(source_b, b_count, ffmpeg)

        def native_frames():
            for index in range(a_count - OVERLAP):
                mapping.append({"output_frame": len(mapping), "A_native_frame": index, "B_native_frame": None, "B_alpha": 0})
                yield next(a)
            for index in range(OVERLAP):
                alpha = (index + 1) / OVERLAP
                image_a = Image.frombytes("RGB", SIZE, next(a))
                image_b = Image.frombytes("RGB", SIZE, next(b))
                mapping.append({"output_frame": len(mapping), "A_native_frame": a_count - OVERLAP + index, "B_native_frame": index, "B_alpha": alpha})
                yield Image.blend(image_a, image_b, alpha).tobytes()
            for index in range(OVERLAP, b_count):
                mapping.append({"output_frame": len(mapping), "A_native_frame": None, "B_native_frame": index, "B_alpha": 1})
                yield next(b)

        frames = native_frames()
        try:
            encode_new(output, frames, ffmpeg)
        finally:
            frames.close()
            a.close()
            b.close()
        decoded = full_decode(output, ffmpeg)
        if decoded["decoded_frames"] != total or len(mapping) != total:
            raise ValueError("Candidate output or mapping frame count mismatch")
        points = sorted({round(i * (total - 1) / 24) for i in range(25)})
        boundary = list(range(max(0, a_count - OVERLAP - 8), min(total, a_count + 8)))
        full_board, full_slots = new_board(points, "25 output checkpoints; visual review pending", modules)
        join_board, join_slots = new_board(boundary, "Every dissolve frame plus eight frames each side", modules)
        qa.mkdir()
        frames_dir = qa / "frames"
        frames_dir.mkdir()
        reader = ffmpeg.read_frames(str(output), pix_fmt="rgb24")
        try:
            require_native(next(reader))
            for index, raw in enumerate(reader):
                if index not in full_slots and index not in join_slots:
                    continue
                image = Image.frombytes("RGB", SIZE, raw)
                save_image(frames_dir / f"frame_{index:06d}.png", image)
                if index in full_slots:
                    stamp_board(full_board, full_slots[index], index, image, modules)
                if index in join_slots:
                    stamp_board(join_board, join_slots[index], index, image, modules)
        finally:
            reader.close()
        save_image(qa / "full_25_checkpoints.jpg", full_board, "JPEG")
        save_image(qa / "transition_all_boundary_frames.jpg", join_board, "JPEG")
        save_json(qa / "frame_mapping.json", mapping)
        save_json(qa / "full_decode.json", decoded)
        verify_manifest(manifest_sha)
        if sha256(source_b) != b_sha or sha256(qa_gate) != gate_sha:
            raise ValueError("New B or its QA receipt changed during composition")
        info = execution_receipt(args.execution_label, versions)
        info.update({
            "status": "research_candidate_pending_combined_visual_review",
            "model": "M02", "look_ids": ["2026-W37-001-L01", "2026-W37-001-L02"],
            "verified_manifest_sha256": manifest_sha, "verified_input_files": checked,
            "source_A_full_decode": a_scan, "source_B_full_decode": b_scan,
            "source_B": "outputs/source_B.mp4", "source_B_sha256": b_sha,
            "external_source_B_sampled_dynamic_QA_receipt": "outputs/source_B_QA.json",
            "external_source_B_sampled_dynamic_QA_receipt_sha256": gate_sha,
            "external_source_B_sampled_dynamic_QA_gate_passed": True,
            "selected_native_frames_half_open": {"A": [0, a_count], "B": [0, b_count]},
            "output": output.relative_to(ROOT).as_posix(), "output_sha256": sha256(output),
            "frames": total, "fps": FPS, "native_size": list(SIZE), "seconds": total / FPS,
            "transition": {"type": "linear_cross_dissolve", "frames": OVERLAP, "seconds": OVERLAP / FPS,
                           "output_frames_half_open": [a_count - OVERLAP, a_count], "B_weight": "(overlap_index+1)/18"},
            "QA_directory": qa.relative_to(ROOT).as_posix(),
            "checkpoint_native_output_indices": points, "transition_boundary_native_output_indices": boundary,
            "source_retime_freeze_reverse_replay": False, "forced_action_synchronization": False,
            "framing_transform": "none; full native raster", "text": "none", "audio": "none; frame-only encode",
            "all_inputs_reverified_after_composition": True,
            "combined_sampled_visual_review": "pending", "combined_continuous_visual_review": "pending",
            "limitations": ["Source sampled QA does not approve the paired dissolve or complete film.",
                            "A declared cloud execution label is not proof of actual cloud execution.",
                            "Normal-speed complete playback and user review remain separate gates."],
        })
        save_json(receipt, info)
    return {"receipt": receipt.relative_to(ROOT).as_posix(), "output": info["output"],
            "frames": total, "seconds": total / FPS, "status": info["status"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "compose"):
        command = commands.add_parser(name)
        command.add_argument("--execution-label", choices=("local", "cloud", "unknown"), default="unknown")
        if name == "compose":
            command.add_argument("--b-sha", required=True)
            command.add_argument("--a-count", type=int, default=96)
            command.add_argument("--b-count", type=int, default=144)
    args = parser.parse_args()
    try:
        modules, versions = load_dependencies()
        result = preflight(args, modules, versions) if args.command == "preflight" else compose(args, modules, versions)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
