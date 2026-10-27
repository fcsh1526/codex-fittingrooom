"""Extract native retry QA after download; never infer a visual/gait pass.

Run from any working directory. All outputs are new and exclusive in this
folder. No media is processed at import time. --f03-sha is mandatory.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f03-sha", required=True,
                        help="Exact lowercase SHA256 of the downloaded retry source")
    args = parser.parse_args()
    root = next(p for p in HERE.parents if (p / "10_automation/CANONICAL_WORKFLOW.md").is_file())
    native = load("mira_f03_retry_source_tools", root / "03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py")
    pair = load("mira_f03_retry_pair_tools", HERE.parent.parent / "F02/build_first_pair_review.py")
    source = HERE / "F03_source.mp4"
    out = HERE / "QA_source"
    receipt_path = HERE / "technical_scan.json"
    if out.exists() or receipt_path.exists():
        raise FileExistsError("Preserve existing/partial QA outputs; do not overwrite them")
    pair.verified_source(source, args.f03_sha)
    scan = native.full_decode(source)
    inventory = pair.stream_inventory(source)
    out.mkdir()
    samples = native.extract_boards(source, out, 0, scan["decoded_frames"])
    early_indices = list(range(0, min(37, scan["decoded_frames"]), 2))
    gait_indices = sorted(set(early_indices) | set(range(60, min(85, scan["decoded_frames"]), 3))
                          | set(range(120, min(145, scan["decoded_frames"]), 3)))
    early, gait = [], []
    for index, frame in enumerate(native.selected_frames(source, 0, scan["decoded_frames"])):
        if index not in gait_indices:
            continue
        target = out / "frames" / f"frame_{index:06d}.png"
        if not target.exists():
            native.image_new(target, frame)
        crop = frame.crop((80, 820, 650, 1230))
        gait.append((index, crop))
        if index in early_indices:
            early.append((index, crop))
    native.sheet(early, out / "gait_first_1p5s_every_two_frames.jpg",
                 "QA-only native opening foot/ground windows; no retiming")
    native.sheet(gait, out / "gait_early_mid_late_windows.jpg",
                 "QA-only native foot/ground windows; visual review pending")
    pair.verified_source(source, args.f03_sha)
    receipt = {
        "recorded_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "source": str(source), "source_sha256": args.f03_sha,
        "bytes": source.stat().st_size, "full_decode": scan,
        "stream_inventory": inventory, "sample_extraction": samples,
        "gait_window_native_xyxy": [80, 820, 650, 1230],
        "early_native_indices": early_indices, "gait_indices": gait_indices,
        "gait_windows_inspection_only": True, "retime": False,
        "visual_qa_pass": None, "assistant_continuous_visual_playback": False,
        "user_video_approval": None, "publishable": False,
        "requested_settings_are_not_actual_settings": True,
    }
    native.json_new(receipt_path, receipt)
    print(json.dumps({"sha256": args.f03_sha, "frames": scan["decoded_frames"],
                      "seconds": scan["frame_count_over_fps_seconds"],
                      "receipt": str(receipt_path), "QA": str(out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
