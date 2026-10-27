"""Bound approved geometry-reset F04 inputs for source inspection only.

Import is read-only and processes no media. The earlier inspector supplies
decode/metadata/25-frame/head/early-mid-late QA. Additional dense windows cover
the exact middle and late road/gait ranges. There is deliberately no build().
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
GEOMETRY = HERE.parent
F04 = GEOMETRY.parent
SOURCE = HERE / "F04_source.mp4"
REJECTED_SOURCES = {
    "d83c6c18fa7d058c3eb3b374afad70db0a51cf0c561ba2c6bd4a255041d0bb50",
    "25252192b6ce6052d88bd645fba47496246be59b23c953e5b3ad68f29ef11739",
    "619053fe0270f2f506a633eb7a1efd0a06aac3b2c8cb2d8016f9730784e0d706",
}
BASE_BUILDER = F04 / "build_four_shot_review.py"
BASE_INSPECTOR = F04 / "inspect_F04_source.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load read-only helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The old builder is imported for existing hash/stream functions only. Its
# encode/build functions are never called and protected earlier media stay read-only.
append = load("mira_geometry_f04_readonly_tools", BASE_BUILDER)
inspector = load("mira_geometry_f04_inspect_base", BASE_INSPECTOR)
native = append.native
PROTECTED = [
    (append.PREFIX, append.PREFIX_SHA),
    (F04 / "F04_M03_L02_start_candidate_A.png",
     "98687eb8365828d67850ddc03d57e48d9d28ad4628f9f62c727bcb166e002457"),
    (GEOMETRY / "photographic_midpoint_01/F04_M03_L02_mid_camera_no_planter_v3.png",
     "0a4fe3eb96bf2473cb441844e770ec1ed391718eceb997bcf38b50a886b5b22f"),
    (GEOMETRY / "photographic_endpoint_01/F04_M03_L02_end_camera_correction_v2.png",
     "e3117eef0d3854bb279d2070a08378b9eefacbabeae0889c057cbcf75e52e8e9"),
]


def require_new_source(digest):
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Require exact lowercase SHA256 of the newly downloaded F04 source")
    if digest in REJECTED_SOURCES:
        raise ValueError("Rejected prior failed F04 source; require the new geometry-reset trial")
    native.verified_source(SOURCE, digest)
    for path, expected in PROTECTED:
        native.verified_source(path, expected)


def provenance(output, sha, wrapper):
    wrapper = Path(wrapper).resolve()
    native.json_new(output / "motion_control_execution.json", {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "context": str(Path(__file__).resolve()),
        "context_sha256": native.sha256(Path(__file__).resolve()),
        "wrapper": str(wrapper), "wrapper_sha256": native.sha256(wrapper),
        "borrowed_stream_hash_helper": str(BASE_BUILDER),
        "borrowed_stream_hash_helper_sha256": native.sha256(BASE_BUILDER),
        "borrowed_inspector": str(BASE_INSPECTOR),
        "borrowed_inspector_sha256": native.sha256(BASE_INSPECTOR),
        "source": str(SOURCE), "source_sha256": sha,
        "protected_inputs_verified_before_and_after": [
            {"path": str(path), "sha256": digest} for path, digest in PROTECTED],
        "rejected_previous_source_sha256": sorted(REJECTED_SOURCES),
        "source_inspection_only": True, "four_shot_composite_built": False,
        "requested_midpoint_control_is_not_proof_of_generator_settings": True,
        "new_source_visual_qa_pass": None, "normal_speed_full_playback": None,
        "user_video_approval": None, "publishable": False,
    })


def add_dense_road_gait_windows(output, sha, count):
    """Add full/native samples every2 frames; crops remain QA-only."""
    if count <= 120:
        raise ValueError("Source lacks native frame120 required for complete4-5s inspection")
    windows = {
        "2p5_to_3p5s": list(range(60, min(count, 85), 2)),
        "4_to_5s": list(range(96, min(count, 121), 2)),
    }
    indices = sorted({index for window in windows.values() for index in window})
    if not all(windows.values()):
        raise ValueError("Source is too short for requested 2.5-3.5s and4-5s inspection windows")
    frames = {}
    for index, frame in enumerate(inspector.native.selected_frames(SOURCE, 0, count)):
        if index not in indices:
            continue
        target = output / "frames" / f"frame_{index:06d}.png"
        if not target.exists():
            inspector.native.image_new(target, frame)
        frames[index] = frame
    if set(frames) != set(indices):
        raise ValueError("Not every requested dense road/gait frame was extracted")
    crop = (0, 700, 720, 1280)
    for label, selected in windows.items():
        inspector.native.sheet([(index, frames[index].crop(crop)) for index in selected],
                               output / f"gait_road_{label}_ground_windows.jpg",
                               f"QA-only native foot/road: {label}, every2frames; grounding unverified")
        inspector.native.sheet([(index, frames[index]) for index in selected],
                               output / f"gait_road_{label}_full_frames.jpg",
                               f"Full-raster native road/gait: {label}; site review pending")
    native.json_new(output / "dense_road_gait_windows.json", {
        "source": str(SOURCE), "source_sha256": sha,
        "fps": inspector.native.FPS, "windows_native_indices": windows,
        "native_interval_frames": 2, "native_interval_seconds": 2 / inspector.native.FPS,
        "requested_seconds_inclusive": [[2.5, 3.5], [4.0, 5.0]],
        "actual_window_reaches_both_requested_endpoints": count > 120,
        "full_resolution_counterparts": "frames/frame_NNNNNN.png",
        "foot_road_window_native_xyxy": list(crop), "window_crops_are_inspection_only": True,
        "retiming_or_media_edit": False, "gait_or_geometry_automatic_pass": False,
        "visual_qa_pass": None, "normal_speed_full_playback": None,
    })


def inspect(sha, version, wrapper):
    require_new_source(sha)
    inspector.HERE = HERE
    # Base inspector uses this object for protected hashes and stream tools only.
    class Configuration:
        pass
    config = Configuration()
    config.PROTECTED = PROTECTED
    config.native = native
    inspector.builder = config
    result = inspector.inspect(sha, version)
    output = Path(result["output_QA"])
    add_dense_road_gait_windows(output, sha, result["frames"])
    require_new_source(sha)
    provenance(output, sha, wrapper)
    result["dense_extra_windows_seconds"] = [[2.5, 3.5], [4.0, 5.0]]
    result["four_shot_composite_built"] = False
    return result
