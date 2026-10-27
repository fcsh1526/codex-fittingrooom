"""Prepare/render an isolated new-F03 partial context after root source QA.

This file alone is preparation, not a completed render or dynamic approval.
No source is opened unless --source-sha, --source-qa-eligible and --render
are explicitly supplied. The new F03 path is fixed; no old-source fallback.
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

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACE = HERE.parent
RESET = PACE.parent
COMMUTE = RESET.parent
BRIDGE = COMMUTE / "production_bridge_2026-10-19"
BASE_BUILDER = PACE / "build_context_review.py"
NEW_F03 = PACE / "F03/F03_pace_source.mp4"
V1 = PACE / "context_review_v1/review.mp4"
V1_SHA = "799911d2a7637c7920c0d2ecec47cc36bea670142a57c9c947dacd256b24d819"


def configure(source_sha):
    """Import established read/encode/composite code, without reading a source."""
    spec = importlib.util.spec_from_file_location("mira_f03_context_base", BASE_BUILDER)
    if spec is None or spec.loader is None:
        raise ImportError(BASE_BUILDER)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    base.OUT = HERE
    base.SOURCES[2] = ("F03_NEW_pace_partial", NEW_F03, source_sha, 1, 109)
    base.PROTECTED[NEW_F03] = source_sha
    base.PROTECTED[V1] = V1_SHA
    base.JOINS = [
        {"id": "J12", "output_half_open": [60, 78], "outgoing": ["F01_original", 60, 78], "incoming": ["F02_NEW_pace_partial", 0, 18]},
        {"id": "J23", "output_half_open": [187, 205], "outgoing": ["F02_NEW_pace_partial", 127, 145], "incoming": ["F03_NEW_pace_partial", 1, 19]},
        {"id": "J34", "output_half_open": [277, 295], "outgoing": ["F03_NEW_pace_partial", 91, 109], "incoming": ["F04_existing_full", 0, 18]},
        {"id": "J45", "output_half_open": [367, 385], "outgoing": ["F04_existing_full", 90, 108], "incoming": ["F05_existing_full_to_half", 0, 18]},
    ]
    return base


def make_qa(base, output):
    native = base.native
    qa = HERE / "QA"
    frames_dir = qa / "frames"
    frames_dir.mkdir()
    full = native.uniform_indices(base.TOTAL, 25)
    dense = {}
    for join in base.JOINS[1:3]:
        begin, end = join["output_half_open"]
        dense[join["id"]] = sorted(set(range(begin - 9, end + 10, 3)) | {end - 1})
    wanted = set(full)
    for indices in dense.values():
        wanted.update(indices)
    found = {}
    with native.native_reader(output) as reader:
        for i, raw in enumerate(reader):
            if i in wanted:
                found[i] = native.Image.frombytes("RGB", base.SIZE, raw)
                native.image_new(frames_dir / f"f{i:04d}.png", found[i])
    if set(found) != wanted:
        raise ValueError("Not all QA frames decoded")
    native.contact_sheet([(i, found[i]) for i in full], qa / "full25.png",
                         "Retained F02 + NEW F03 partial context; NOT whole-film gait approval")
    feet_crop = (0, 740, 720, 1280)
    for label, indices in dense.items():
        native.contact_sheet([(i, found[i]) for i in indices], qa / f"{label}_every3_full.png",
                             f"{label}: every3 native frames plus final overlap; user review pending")
        native.contact_sheet([(i, found[i].crop(feet_crop)) for i in indices], qa / f"{label}_every3_feet.png",
                             f"{label}: QA FOOT CROP ONLY; movie remains full native raster")
    return {"full25_indices": full, "join_every3_indices": dense,
            "individual_frames_native_size": list(base.SIZE),
            "feet_crop_QA_only_xyxy": list(feet_crop), "movie_crop_or_scale": False,
            "continuous_normal_speed_visual_review_by_script": False}


def build(args):
    # Validate authority and destination before importing helpers or opening sources.
    if not args.source_sha or not re.fullmatch(r"[0-9a-f]{64}", args.source_sha):
        raise ValueError("Supply root-confirmed exact lowercase --source-sha")
    if not args.source_qa_eligible or not args.render:
        raise ValueError("Root exact-source QA and explicit --source-qa-eligible --render are required")
    for name in ("review.mp4", "QA", "build_manifest.json", "README.md"):
        if os.path.lexists(HERE / name):
            raise FileExistsError(f"Preserve existing or partial output: {HERE / name}")
    base = configure(args.source_sha)
    native = base.native
    for path, sha in base.PROTECTED.items():
        native.verified_source(path, sha)
    before = {str(path): native.sha256(path) for path in base.PROTECTED}
    helper_hashes = {str(path): native.sha256(path) for path in (BASE_BUILDER, base.HELPER)}
    scans = {}
    for role, path, sha, begin, end in base.SOURCES:
        scans[role] = native.full_decode(path)
        if scans[role]["decoded_frames"] < end:
            raise ValueError(f"Insufficient native frames: {role}")
        if scans[role]["metadata"].get("rotate", 0) != 0:
            raise ValueError("Rotated source not permitted")
    (HERE / "QA").mkdir()
    output = HERE / "review.mp4"
    mapping = []
    frames = base.sequence(mapping)
    try:
        base.close.encode_exclusive(output, frames)
    finally:
        frames.close()
    if len(mapping) != base.TOTAL:
        raise ValueError("Frame mapping is not exactly 511")
    native.json_new(HERE / "QA/frame_mapping.json", mapping)
    scan = native.full_decode(output)
    if scan["decoded_frames"] != base.TOTAL:
        raise ValueError("Encoded output is not 511 frames")
    streams = native.stream_inventory(output)
    if streams["audio_stream_present"]:
        raise ValueError("Silent output contains audio")
    fidelity = base.verify_fidelity(output)
    qa = make_qa(base, output)
    for path, sha in base.PROTECTED.items():
        native.verified_source(path, sha)
    after = {str(path): native.sha256(path) for path in base.PROTECTED}
    for path, sha in helper_hashes.items():
        native.verified_source(Path(path), sha)
    receipt = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "retained_F02_NEW_F03_partial_context_candidate_NOT_user_approved",
        "operator_exact_source_QA_eligibility": True,
        "eligibility_is_user_dynamic_approval": False,
        "source_authority": "User retained context_v1 F02 and its joins; requested continuation with F03 repair. Root separately authorized this exact new F03 for context render.",
        "sources": [{"role": role, "path": str(path), "sha256": sha, "selected_frames_half_open": [begin, end]} for role, path, sha, begin, end in base.SOURCES],
        "source_scans": scans,
        "output": {"path": str(output), "sha256": native.sha256(output), "bytes": output.stat().st_size,
                   "frames": base.TOTAL, "fps": base.FPS, "size": list(base.SIZE),
                   "duration_seconds": base.TOTAL / base.FPS},
        "edit": {"formula": "78+145+108+108+144-4*18=511", "joins": base.JOINS,
                 "blend_incoming_alpha": "(overlap_index+1)/18; overlap_index=0..17",
                 "raw_native_sources": True, "only_source_changed_from_context_v1_EDL": "F03"},
        "full_decode": scan, "streams": streams, "fidelity": fidelity, "QA": qa,
        "protected_hashes_before": before, "protected_hashes_after": after,
        "protected_hashes_unchanged": before == after,
        "builder": {"path": str(Path(__file__).resolve()), "sha256": native.sha256(Path(__file__).resolve()),
                    "established_helpers_sha256_before_after": helper_hashes},
        "speed_factor": 1.0, "retime": False, "crop": False, "scale": False,
        "text": False, "audio": False, "freeze_repeat_reverse_interpolation": False,
        "frame_order_preserved": True, "individual_source_PTS_measured": False,
        "external_write": False, "publication": False,
        "user_dynamic_approval": None, "assistant_continuous_normal_speed_visual_review": None,
        "limits": [
            "Only F03 changes from context_v1. F01, retained F02, F04 and full-to-half F05 sources/ranges remain unchanged.",
            "Both J23 and J34 require new dynamic/context review. A keyframe request does not prove literal frame timing or world continuity.",
            "No claim that the whole-film cadence, ground-relative foot support or background is repaired.",
            "Full decode/fidelity confirms the intended native edit, not aesthetics, identity, scene, comfort or publishability.",
            "All originals, context_v1 and publishing packages are retained; no external mutation."]}
    native.json_new(HERE / "build_manifest.json", receipt)
    with (HERE / "README.md").open("x", encoding="utf-8") as stream:
        stream.write("# New F03 partial context candidate\n\nRetains context_v1 F02 and all EDL ranges; replaces only F03 with the exact root-inspected new source [1,109). All four 18-frame dissolves retain alpha (k+1)/18. 511 native frames / 24 fps / 720×1280 / 21.2917 seconds; no crop, retiming, text or audio.\n\nJ23 and J34 require new review. This is not whole-film cadence, background, user or publication approval. See build_manifest.json, QA/all_frame_fidelity.json and QA/.\n")
    return {"output": receipt["output"], "fidelity": fidelity, "manifest": str(HERE / "build_manifest.json")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-sha", required=True, help="Exact downloaded F03 SHA256 provided by root")
    parser.add_argument("--source-qa-eligible", action="store_true", help="Root inspected exact F03 and permits a research context edit")
    parser.add_argument("--render", action="store_true", help="Explicit root authority to create new context media")
    args = parser.parse_args()
    print(json.dumps(build(args), ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
