"""Extract exclusive F04 native source inspection boards; never declare a QA pass.

The expected F04 SHA256 is mandatory. Saves25 full frames,5 fixed head windows,
and dense first1.5s plus middle/late foot-ground windows for gait/turn inspection.
Only QA contact windows are cropped; they never enter delivery video.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "10_automation").is_dir())
HELPER = ROOT / "03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py"
spec = importlib.util.spec_from_file_location("mira_f04_inspection_helpers", HELPER)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load helper: {HELPER}")
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
builder_spec = importlib.util.spec_from_file_location("mira_f04_append_builder", HERE / "build_four_shot_review.py")
if builder_spec is None or builder_spec.loader is None:
    raise ImportError("Cannot load F04 builder protections")
builder = importlib.util.module_from_spec(builder_spec)
builder_spec.loader.exec_module(builder)


def inspect(f04_sha: str, version: str = "v1") -> dict:
    if not re.fullmatch(r"v[1-9][0-9]*", version):
        raise ValueError("Version must be v1,v2,...")
    output = HERE / f"source_inspection_{version}"
    if os.path.lexists(output):
        raise FileExistsError(f"Preserve existing/partial inspection; choose a new --version: {output}")
    source = native.verified_source(HERE / "F04_source.mp4", f04_sha)
    for path, digest in builder.PROTECTED:
        builder.native.verified_source(path, digest)
    scan = native.full_decode(source)
    count = scan["decoded_frames"]
    inventory = builder.native.stream_inventory(source)
    output.mkdir()
    samples = native.extract_boards(source, output, 0, count)
    #0.125s sample spacing through first1.5s; all selected frames retain their
    #full-resolution counterparts. The crops are inspection-only, not footage.
    early = list(range(0, min(count, 37), 3))
    middle_start = max(0, count // 2 - 12)
    middle = list(range(middle_start, min(count, middle_start + 25), 3))
    late = list(range(max(0, count - 25), count, 3))
    indices = sorted(set(early) | set(middle) | set(late))
    found = {}
    for index, frame in enumerate(native.selected_frames(source, 0, count)):
        if index in indices:
            path = output / "frames" / f"frame_{index:06d}.png"
            if not path.exists():
                native.image_new(path, frame)
            found[index] = frame
    if set(found) != set(indices):
        raise ValueError("Not every dense gait/turn checkpoint was extracted")
    crop = (0, 700, 720, 1280)
    native.sheet([(index, found[index].crop(crop)) for index in early],
                 output / "gait_first_1p5s_ground_windows.jpg", "QA-only foot/ground: first1.5s at0.125s intervals")
    native.sheet([(index, found[index].crop(crop)) for index in indices],
                 output / "gait_early_mid_late_ground_windows.jpg", "QA-only foot/ground windows; support contact not yet verified")
    native.sheet([(index, found[index]) for index in indices],
                 output / "dense_gait_turn_full_frames.jpg", "Full-raster gait/turn checkpoints; site and continuity review pending")
    native.verified_source(source, f04_sha)
    for path, digest in builder.PROTECTED:
        builder.native.verified_source(path, digest)
    value = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "source_inspection_assets_ready_visual_review_pending",
        "execution": "local", "model": "M03", "look_id": "L02",
        "source": str(source), "source_sha256": f04_sha, "bytes": source.stat().st_size,
        "full_decode": scan, "stream_inventory": inventory, "sample_extraction": samples,
        "dense_first_1p5s_indices": early, "dense_gait_turn_indices": indices,
        "foot_ground_window_native_xyxy": list(crop), "window_crops_are_inspection_only": True,
        "protected_inputs_verified_before_and_after": [
            {"path": str(path), "sha256": digest} for path, digest in builder.PROTECTED],
        "visual_qa_pass": None, "assistant_continuous_visual_playback": None,
        "user_video_approval": None, "publishable": False,
        "limitations": [
            "Sampled full/head/foot windows do not replace complete normal-speed playback.",
            "Fixed head window may miss an arcing subject and cannot prove identity or unobserved rear details.",
            "Dense samples do not measure shoe/tile motion, zero sliding, exact cadence or scene geometry.",
            "Requested generator settings are not measured settings; source metadata/streams are recorded separately.",
        ],
    }
    native.json_new(output / "technical_scan.json", value)
    return {"output_QA": str(output), "sha256": f04_sha, "frames": count,
            "seconds": count / native.FPS, "status": value["status"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f04-sha", required=True, help="Exact lowercase downloaded source SHA256")
    parser.add_argument("--version", default="v1", help="New exclusive inspection directory version:v1,v2,...")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.f04_sha, args.version), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
