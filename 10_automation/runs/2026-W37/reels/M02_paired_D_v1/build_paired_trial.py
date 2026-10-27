"""Build a review-only two-source Mira trial at unchanged source speed.

Default selections are A2[0:144] and B1[0:144] at 24fps. Their single
18-frame dissolve yields 270 frames / 11.25 seconds. Running this script
does not grant visual approval; every QA state remains pending.
"""

import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
FPS = 24
SIZE = (720, 1280)


def relative(path):
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_runtime():
    # Reuse existing project dependencies. No installs or permission changes.
    sys.path.insert(0, str(ROOT / "10_automation/.video_dependencies"))
    sys.path.insert(0, str(ROOT / "10_automation"))
    import imageio_ffmpeg
    from scan_reel_video import scan
    return imageio_ffmpeg.get_ffmpeg_exe(), scan


def run_ffmpeg(binary, args):
    subprocess.run([binary, "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def selection_graph(start, end):
    # xfade requires an explicit CFR marker after trim. Feed one following
    # frame only as the endpoint timestamp, label the already24fps input at
    # the same24fps, then exclude that endpoint. Frame hashes are verified
    # against the original selection before rendering; no duplicates or
    # omitted selected frames are permitted.
    return (f"trim=start_frame={start}:end_frame={end + 1},"
            "setpts=PTS-STARTPTS,fps=24,settb=expr=1/24,setsar=1,"
            f"trim=end_frame={end - start}")


def verify_selected_frame_preservation(binary, source, start, end, folder):
    folder.mkdir(parents=True, exist_ok=True)
    original = folder / "original_selection.framemd5"
    normalized = folder / "same_rate_selection.framemd5"
    original_graph = f"trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS"
    for graph, output in ((original_graph, original), (selection_graph(start, end), normalized)):
        run_ffmpeg(binary, ["-i", str(source), "-vf", graph, "-an",
                            "-fps_mode", "passthrough", "-f", "framemd5", str(output)])
    def hashes(path):
        return [line.rsplit(",", 1)[-1].strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line and not line.startswith("#")]
    original_hashes, normalized_hashes = hashes(original), hashes(normalized)
    if len(original_hashes) != end - start or original_hashes != normalized_hashes:
        raise ValueError("Same-rate normalization changed selected frame count/order/pixels")
    record = dict(original_framemd5=relative(original), same_rate_framemd5=relative(normalized),
                  selected_frames=end - start, identical_frame_hash_sequence=True,
                  note="This verifies decoded source-frame timing/order before any optional fixed spatial framing, dissolve or output encoding; it does not compare final encoded-video pixels.")
    save_json(folder / "preservation_result.json", record)
    return record


def extract_checkpoints(binary, source, folder, indices, total_frames, board_name):
    """Select exact decoded frame numbers in one pass, then build a QA board."""
    folder.mkdir(parents=True, exist_ok=True)
    indices = sorted(set(indices))
    if not indices or min(indices) < 0 or max(indices) >= total_frames:
        raise ValueError("Checkpoint frame is outside the actual decoded output")
    expression = "+".join(f"eq(n,{index})" for index in indices)
    pattern = folder / "checkpoint_%03d.png"
    run_ffmpeg(binary, ["-i", str(source), "-vf", f"select='{expression}'",
                       "-fps_mode", "passthrough", "-an", "-start_number", "0", str(pattern)])
    columns, cell_w, cell_h = 4, 216, 408
    board = Image.new("RGB", (columns * cell_w, math.ceil(len(indices) / columns) * cell_h), "white")
    draw = ImageDraw.Draw(board)
    frames = []
    for ordinal, index in enumerate(indices):
        image_path = folder / f"checkpoint_{ordinal:03d}.png"
        if not image_path.is_file():
            raise RuntimeError(f"Missing extracted checkpoint {image_path}")
        x, y = ordinal % columns * cell_w, ordinal // columns * cell_h
        with Image.open(image_path) as checkpoint:
            if checkpoint.size != SIZE:
                raise ValueError(f"Checkpoint changed size: {checkpoint.size}")
            checkpoint.thumbnail((cell_w, cell_h - 24))
            board.paste(checkpoint, (x, y + 24))
        draw.text((x + 5, y + 5), f"f{index} / {index / FPS:.4f}s", fill="black")
        frames.append(dict(frame=index, seconds=index / FPS, path=relative(image_path)))
    board_path = folder / board_name
    board.save(board_path, quality=95)
    record = dict(source=relative(source), fps=FPS, frame_indices=indices,
                  frames=frames, board=relative(board_path), sampled_visual_review="pending",
                  continuous_review="pending")
    save_json(folder / "metadata.json", record)
    return record


def validate_source(source, start, end, scan, qa_folder, label):
    if not source.is_file():
        raise FileNotFoundError(source)
    if start < 0 or end <= start:
        raise ValueError(f"{label}: use a nonempty [start,end) frame range")
    result = scan(source)
    save_json(qa_folder / f"{label}_source_decode_scan.json", result)
    meta = result["metadata"]
    if tuple(meta["size"]) != SIZE or tuple(meta["source_size"]) != SIZE:
        raise ValueError(f"{label}: source must already be720x1280; no resizing is allowed")
    if not math.isclose(meta["fps"], FPS, abs_tol=1e-9) or meta.get("rotate", 0) != 0:
        raise ValueError(f"{label}: source must be unrotated24fps; no retiming is allowed")
    if end > result["decoded_frames"]:
        raise ValueError(f"{label}: range ends after decoded source footage")
    if end == result["decoded_frames"]:
        raise ValueError(f"{label}: retain one following timestamp frame outside the selected range; do not select the final source frame")
    selected_black = [frame for frame in result["black_candidate_frames"] if start <= frame < end]
    selected_still = [pair for pair in result["near_identical_frame_pairs"]
                      if start <= pair[0] and pair[1] < end]
    if selected_black or selected_still:
        raise ValueError(f"{label}: selected range has a technical signal requiring separate inspection")
    return dict(label=label, path=relative(source), sha256=sha256(source),
                look_id="2026-W37-001-L01" if label == "A" else "2026-W37-001-L02",
                start_frame=start, end_frame_exclusive=end, selected_frames=end - start,
                unused_before_frames=start, unused_after_frames=result["decoded_frames"] - end,
                start_seconds=start / FPS, end_seconds_exclusive=end / FPS,
                speed="unchanged", resize="none", crop="none", decode=result,
                selected_interval_visual_approval="pending")


def build(args):
    started = time.monotonic()
    a_source, b_source, output = args.a.resolve(), args.b.resolve(), args.output.resolve()
    if not output.is_relative_to(HERE):
        raise ValueError("Store the trial output inside M02_paired_D_v1")
    if output.exists() and not args.force:
        raise FileExistsError(f"Output exists; use a new filename or explicit--force: {output}")
    a_count, b_count = args.a_end - args.a_start, args.b_end - args.b_start
    overlap_frames = args.transition_frames
    if overlap_frames <= 0 or overlap_frames >= min(a_count, b_count):
        raise ValueError("Transition frames must be positive and shorter than both selections")
    output_frames = a_count + b_count - overlap_frames
    overlap_start = a_count - overlap_frames
    overlap_end_exclusive = a_count
    output.parent.mkdir(parents=True, exist_ok=True)
    qa_folder = output.parent / f"{output.stem}_qa"
    qa_folder.mkdir(parents=True, exist_ok=True)
    binary, scan = load_runtime()
    records = [validate_source(a_source, args.a_start, args.a_end, scan, qa_folder, "A"),
               validate_source(b_source, args.b_start, args.b_end, scan, qa_folder, "B")]
    for record, source, start, end in ((records[0], a_source, args.a_start, args.a_end),
                                       (records[1], b_source, args.b_start, args.b_end)):
        record["selected_frame_preservation"] = verify_selected_frame_preservation(
            binary, source, start, end, qa_folder / f"preservation_{record['label']}")
    a_graph = selection_graph(args.a_start, args.a_end)
    fixed_a_framing = None
    if args.a_match_framing:
        a_graph += ",scale=747:1328:flags=lanczos,crop=720:1280:14:44,setsar=1"
        fixed_a_framing = dict(type="fixed_proportional_scale_and_fixed_crop",
                              scale_factor=1.0375, intermediate_dimensions=[747, 1328],
                              crop_dimensions=[720, 1280], crop_x=14, crop_y=44,
                              scale_interpolation="lanczos", camera_window_motion="none",
                              source_speed="unchanged", source_frame_range="unchanged",
                              top_margin_note="Opening top margin is reduced; every selected head/shoe/bag safety check remains pending.")
        records[0]["resize"] = "fixed1.0375proportional scale to747x1328"
        records[0]["crop"] = "fixed720x1280atx14y44"
        records[0]["fixed_framing"] = fixed_a_framing
    graph = (f"[0:v]{a_graph}[a];"
             f"[1:v]{selection_graph(args.b_start, args.b_end)}[b];"
             f"[a][b]xfade=transition=fade:duration={overlap_frames / FPS:.9f}:"
             f"offset={overlap_start / FPS:.9f},format=yuv420p[v]")
    command_args = ["-i", str(a_source), "-i", str(b_source), "-filter_complex", graph,
                    "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "18",
                    "-preset", "medium", "-fps_mode", "passthrough", "-frames:v", str(output_frames),
                    "-movflags", "+faststart", str(output)]
    run_ffmpeg(binary, command_args)
    decoded = scan(output)
    save_json(qa_folder / "output_decode_scan.json", decoded)
    if decoded["decoded_frames"] != output_frames:
        raise ValueError(f"Expected{output_frames} frames, decoded{decoded['decoded_frames']}; do not extend or freeze")
    if tuple(decoded["metadata"]["size"]) != SIZE or decoded["metadata"]["fps"] != FPS:
        raise ValueError("Output dimensions or timing changed")
    if decoded["black_candidate_frames"] or decoded["near_identical_frame_pairs"]:
        raise ValueError("Output has a technical signal; keep it unapproved for inspection")
    key_frames = sorted({0, output_frames - 1, round((output_frames - 1) / 4),
                         round((output_frames - 1) / 2), round(3 * (output_frames - 1) / 4),
                         max(0, overlap_start - 1), overlap_start,
                         overlap_start + overlap_frames // 2,
                         overlap_end_exclusive - 1, overlap_end_exclusive,
                         min(output_frames - 1, overlap_end_exclusive + 1)})
    key_frames = sorted(set(key_frames + args.extra_checkpoint_frames))
    output_checkpoints = extract_checkpoints(binary, output, qa_folder / "keypoints",
                                            key_frames, output_frames, "keypoints.jpg")
    # All18 default overlap frames, plus the final pre-overlap and first
    # post-overlap frames. The end endpoint at6.000s is included explicitly.
    overlap_indices = list(range(overlap_start, overlap_end_exclusive))
    boundary_indices = [max(0, overlap_start - 1), overlap_end_exclusive]
    overlap_checkpoints = extract_checkpoints(binary, output, qa_folder / "complete_overlap",
                                              overlap_indices + boundary_indices, output_frames,
                                              "complete_overlap_with_endpoints.jpg")
    for record, source, start, end in ((records[0], a_source, args.a_start, args.a_end),
                                       (records[1], b_source, args.b_start, args.b_end)):
        count = end - start
        indices = sorted({start, end - 1, start + round((count - 1) / 4),
                          start + round((count - 1) / 2), start + round(3 * (count - 1) / 4)})
        record["selected_source_checkpoints"] = extract_checkpoints(
            binary, source, qa_folder / f"source_{record['label']}", indices,
            record["decode"]["decoded_frames"], "selected_source_checkpoints.jpg")
    overlap_pairs = [dict(output_frame=overlap_start + i,
                          output_seconds=(overlap_start + i) / FPS,
                          a_source_frame=args.a_end - overlap_frames + i,
                          b_source_frame=args.b_start + i)
                     for i in range(overlap_frames)]
    now = datetime.now(timezone(timedelta(hours=8), name="Asia/Taipei"))
    receipt = dict(trial_id="M02_paired_D_v1", created_at_local=now.isoformat(),
                   status="candidate_pending_user_review", output_path=relative(output),
                   output_sha256=sha256(output), sources=records,
                   information_order=["L01_proof", "L01_full", "L02_full", "L02_proof"],
                   theoretical_frames=output_frames, theoretical_seconds=output_frames / FPS,
                   actual_frames=decoded["decoded_frames"], actual_seconds=decoded["decoded_seconds"],
                   fps=FPS, resolution=list(SIZE), audio="none", baked_text="none",
                   timing_marker="same24fps CFR; selected decoded frame hashes verified identical",
                   character_speed="unchanged",
                   resize=("A fixed1.0375proportional scale; B none" if fixed_a_framing else "none"),
                   crop=("A fixed720x1280atx14y44; B none" if fixed_a_framing else "none"),
                   fixed_a_framing=fixed_a_framing,
                   freeze_frames="none", source_extension="none",
                   default_frame_ranges_used=(args.a_start == args.b_start == 0 and
                                              args.a_end == args.b_end == 144),
                   final_source_frame_removed_only=(all(record["unused_before_frames"] == 0 and
                                                         record["unused_after_frames"] == 1
                                                         for record in records)),
                   transition=dict(type="cross_dissolve", count=1, frames=overlap_frames,
                                   seconds=overlap_frames / FPS,
                                   start_output_frame=overlap_start,
                                   end_output_frame_exclusive=overlap_end_exclusive,
                                   start_output_seconds=overlap_start / FPS,
                                   end_output_seconds_exclusive=overlap_end_exclusive / FPS,
                                   source_frame_pairs=overlap_pairs),
                   filter_graph=graph, technical_scan=decoded,
                   keypoints=output_checkpoints, complete_overlap=overlap_checkpoints,
                   sampled_visual_review="pending", assistant_continuous_review=False,
                   user_visual_approval="pending", global_format_adoption="not_inferred",
                   audience_performance=None, publishable=False,
                   processing_wall_seconds=time.monotonic() - started)
    receipt_path = output.with_suffix(".json")
    save_json(receipt_path, receipt)
    print(json.dumps(dict(output=str(output), receipt=str(receipt_path), frames=output_frames,
                         seconds=output_frames / FPS, status=receipt["status"],
                         overlap_checkpoints=len(overlap_checkpoints["frame_indices"])), ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", type=Path, default=HERE / "grok_A_attempt_02/source.mp4")
    parser.add_argument("--b", type=Path, default=HERE / "grok_B_attempt_01/source.mp4")
    parser.add_argument("--a-start", type=int, default=0, help="Inclusive A source frame")
    parser.add_argument("--a-end", type=int, default=144, help="Exclusive A source frame")
    parser.add_argument("--b-start", type=int, default=0, help="Inclusive B source frame")
    parser.add_argument("--b-end", type=int, default=144, help="Exclusive B source frame")
    parser.add_argument("--transition-frames", type=int, default=18, help="Default18 frames equals0.75s")
    parser.add_argument("--a-match-framing", action="store_true",
                        help="A only: fixed1.0375proportional scale747x1328, crop720x1280atx14y44")
    parser.add_argument("--extra-checkpoint-frames", type=int, nargs="+", default=[],
                        help="Additional exact output frames for disclosed framing-safety checks")
    parser.add_argument("--output", type=Path,
                        default=HERE / "review/M02_paired_D_v1_review_v1.mp4")
    parser.add_argument("--force", action="store_true", help="Explicitly permit overwriting the named review output")
    args = parser.parse_args()
    build(args)


if __name__ == "__main__":
    main()
