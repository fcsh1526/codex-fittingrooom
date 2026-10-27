"""Append an inspected NEW full-to-half F05 source to the accepted four-look film.

No generation, browser access, retiming, crop, scale, text, or publication.
The default source does not exist until the new Grok result is downloaded.
Rendering requires an exact source SHA plus explicit root QA eligibility.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
MOTION = HERE.parent
RESET = MOTION.parent
COMMUTE = RESET.parent
HELPER = COMMUTE / "production_bridge_2026-10-19/F04/close_tracking_proposal_2026-10-20/close_join_review_2026-10-21/build_close_study.py"
PREFIX = RESET / "four_look_review/v1/review.mp4"
PREFIX_SHA = "3c0f3fa5bb0c90d0d9b5d434ada37cd5dbe130658d5bff24c01143feb77f1f94"
DEFAULT_SOURCE = MOTION / "F05_half_source.mp4"
PREFIX_COUNT, F05_COUNT, OVERLAP, FPS = 385, 144, 18, 24
JOIN_START = PREFIX_COUNT - OVERLAP  # 367
TOTAL = PREFIX_COUNT + F05_COUNT - OVERLAP  # 511
SIZE = (720, 1280)


def load_helper():
    # Avoid generating __pycache__ beside helpers outside this new output folder.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("mira_f05_half_close_helper", HELPER)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load established local video helper: {HELPER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def intended_sequence(native, source: Path, mapping: list | None = None):
    """Preserve prefix [0,367), blend 18, then append F05 [18,144)."""
    prefix_frames = native.selected_frames(PREFIX, PREFIX_COUNT)
    f05_frames = native.selected_frames(source, F05_COUNT)
    output_index = 0

    def record(image, prefix_index, f05_index, alpha):
        nonlocal output_index
        if mapping is not None:
            mapping.append({"output_frame": output_index,
                            "accepted_prefix_native_frame": prefix_index,
                            "F05_native_frame": f05_index, "F05_alpha": alpha})
        output_index += 1
        return image

    try:
        for index in range(JOIN_START):
            yield record(next(prefix_frames), index, None, 0.0)
        for index in range(OVERLAP):
            alpha = (index + 1) / OVERLAP
            image = native.Image.blend(next(prefix_frames), next(f05_frames), alpha)
            yield record(image, JOIN_START + index, index, alpha)
        for index in range(OVERLAP, F05_COUNT):
            yield record(next(f05_frames), None, index, 1.0)
    finally:
        prefix_frames.close()
        f05_frames.close()


def compare_fidelity(native, source: Path, output: Path):
    """Full decoded output versus intended native composite, with CRF18 tolerance."""
    import numpy as np

    expected = intended_sequence(native, source)
    count, mae_sum, worst, min_psnr = 0, 0.0, 0.0, float("inf")
    pure_count, pure_sum, pure_worst, pure_psnr = 0, 0.0, 0.0, float("inf")
    try:
        with native.native_reader(output) as reader:
            for index, raw in enumerate(reader):
                try:
                    intended = next(expected)
                except StopIteration as error:
                    raise ValueError("Output has more frames than the intended 511") from error
                a = np.asarray(intended, dtype=np.int16)
                b = np.frombuffer(raw, dtype=np.uint8).reshape(SIZE[1], SIZE[0], 3).astype(np.int16)
                error = a - b
                mae = float(np.abs(error).mean())
                mse = float(np.square(error.astype(np.float32)).mean())
                psnr = 100.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)
                count += 1
                mae_sum += mae
                worst, min_psnr = max(worst, mae), min(min_psnr, psnr)
                if index < JOIN_START:
                    pure_count += 1
                    pure_sum += mae
                    pure_worst, pure_psnr = max(pure_worst, mae), min(pure_psnr, psnr)
        try:
            next(expected)
        except StopIteration:
            pass
        else:
            raise ValueError("Output ended before the intended 511-frame composite")
    finally:
        expected.close()
    if count != TOTAL or pure_count != JOIN_START:
        raise ValueError(f"Wrong fidelity counts: total={count}, pure_prefix={pure_count}")
    passed = worst <= 3.0 and min_psnr >= 32.0
    result = {"all_output_frames_compared_to_intended_native_composite": count,
              "mean_absolute_RGB_error_0_to_255": mae_sum / count,
              "worst_frame_mean_absolute_RGB_error": worst,
              "minimum_frame_PSNR_dB": min_psnr,
              "codec_tolerance": {"worst_frame_MAE_max": 3.0, "minimum_frame_PSNR_dB_min": 32.0},
              "within_codec_tolerance": passed, "pixel_or_byte_identity_claim": False,
              "protected_prefix_pure_frames": {"frames_compared": pure_count,
                  "output_half_open": [0, JOIN_START], "mean_absolute_RGB_error": pure_sum / pure_count,
                  "worst_frame_mean_absolute_RGB_error": pure_worst, "minimum_frame_PSNR_dB": pure_psnr}}
    if not passed:
        raise ValueError("Encoding differs beyond the established tolerance: " + json.dumps(result))
    return result


def make_qa(native, output: Path, qa: Path):
    qa.mkdir()
    frames_dir = qa / "frames"
    frames_dir.mkdir()
    full = native.uniform_indices(TOTAL, 25)
    dense = list(range(JOIN_START - 8, PREFIX_COUNT + 8))
    # Source time, not a promise that the generated push-in follows these times.
    closing = [JOIN_START + index for index in (18, 36, 54, 72, 84, 96, 108, 120, 132, 143)]
    wanted = set(full + dense + closing)
    found = {}
    with native.native_reader(output) as reader:
        for index, raw in enumerate(reader):
            if index in wanted:
                found[index] = native.Image.frombytes("RGB", SIZE, raw)
                native.image_new(frames_dir / f"f{index:04d}.png", found[index])
    if set(found) != wanted:
        raise ValueError("Not all requested QA frames were decoded")
    native.contact_sheet([(index, found[index]) for index in full], qa / "full25.png",
                         "Five looks: technical samples only; normal-speed visual review pending")
    native.contact_sheet([(index, found[index]) for index in dense], qa / "J45_dense.png",
                         "J45:18 dissolve frames+8 each side; ghosting/phase require visual review")
    native.contact_sheet([(index, found[index]) for index in closing], qa / "F05_progress.png",
                         "F05 source progression: confirm full-outfit reading before continuous push-in")
    return {"full_25_checkpoint_indices": full, "dense_J45_indices": dense,
            "all_18_new_dissolve_frames_extracted": True, "F05_progress_output_indices": closing,
            "individual_frames_size": list(SIZE), "contact_sheets_are_reduced_full_raster": True,
            "normal_speed_visual_review_completed_by_this_script": False}


def build(args):
    source = Path(args.source).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"NEW F05 source is not downloaded yet: {source}. No output was created; do not substitute an old F05 clip.")
    if source.parent != MOTION.resolve():
        raise ValueError("Use the new source inside F05_half_motion_01; old F05 sources are not accepted by this builder")
    if not args.source_sha or not re.fullmatch(r"[0-9a-f]{64}", args.source_sha):
        raise ValueError("Supply exact lowercase --source-sha after root inspection of this NEW source")
    if not re.fullmatch(r"v[1-9][0-9]*", args.version):
        raise ValueError("Use a new version v1, v2, ...")
    if not args.preflight_only and not args.source_qa_eligible:
        raise ValueError("Root must explicitly permit this exact source with --source-qa-eligible before rendering")
    destination = HERE / args.version
    if not args.preflight_only and os.path.lexists(destination):
        raise FileExistsError(f"Preserve existing/partial output; select another version: {destination}")
    close = load_helper()
    native = close.native
    native.verified_source(PREFIX, PREFIX_SHA)
    native.verified_source(source, args.source_sha)
    prefix_scan, source_scan = native.full_decode(PREFIX), native.full_decode(source)
    if prefix_scan["decoded_frames"] != PREFIX_COUNT:
        raise ValueError("Accepted prefix must decode to exactly 385 frames")
    if source_scan["decoded_frames"] < F05_COUNT:
        raise ValueError(f"New F05 requires at least 144 native frames, got {source_scan['decoded_frames']}")
    for scan in (prefix_scan, source_scan):
        if scan["metadata"].get("rotate", 0) != 0:
            raise ValueError("Rotation is not permitted; native upright full raster required")
    preflight = {"status": "preflight_pass_not_visual_approval", "source": str(source),
                 "source_sha256": args.source_sha, "source_scan": source_scan,
                 "accepted_prefix_scan": prefix_scan, "planned_frames": TOTAL,
                 "planned_seconds": TOTAL / FPS, "output_created": False}
    if args.preflight_only:
        return preflight
    helper_sha = native.sha256(HELPER)
    destination.mkdir()
    output = destination / "review.mp4"
    mapping = []
    frames = intended_sequence(native, source, mapping)
    try:
        # Established writer uses an exclusive output and a temp file in output.parent.
        close.encode_exclusive(output, frames)
    finally:
        frames.close()
    scan = native.full_decode(output)
    if scan["decoded_frames"] != TOTAL or len(mapping) != TOTAL:
        raise ValueError("Encoded count or mapping does not equal385+144-18=511")
    streams = native.stream_inventory(output)
    if streams["audio_stream_present"]:
        raise ValueError("Silent research preview unexpectedly has an audio stream")
    fidelity = compare_fidelity(native, source, output)
    qa = make_qa(native, output, destination / "QA")
    native.json_new(destination / "QA/frame_mapping.json", mapping)
    native.verified_source(PREFIX, PREFIX_SHA)
    native.verified_source(source, args.source_sha)
    if native.sha256(HELPER) != helper_sha:
        raise ValueError("Imported helper changed during render")
    receipt = {"created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "five_look_research_candidate_pending_root_and_user_visual_review",
        "builder_path": str(Path(__file__).resolve()), "builder_sha256": native.sha256(Path(__file__).resolve()),
        "helper_path": str(HELPER), "helper_sha256": helper_sha,
        "source_QA_eligibility_attested_by_operator": args.source_qa_eligible,
        "source_QA_eligibility_is_user_video_approval": False,
        "sources": [{"role": "accepted385_prefix", "path": str(PREFIX), "sha256": PREFIX_SHA,
                     "selected_frames_half_open": [0, PREFIX_COUNT]},
                    {"role": "NEW_F05_full_to_half", "path": str(source), "sha256": args.source_sha,
                     "selected_frames_half_open": [0, F05_COUNT], "actual_decoded_source_frames": source_scan["decoded_frames"]}],
        "source_scans": {"accepted_prefix": prefix_scan, "NEW_F05": source_scan},
        "output": {"path": str(output), "sha256": native.sha256(output), "bytes": output.stat().st_size,
                   "frames": TOTAL, "fps": FPS, "duration_seconds": TOTAL / FPS, "size": list(SIZE)},
        "edit": {"formula": "385+144-18=511", "prefix_pure_frames_half_open": [0, JOIN_START],
                 "new_dissolve_output_frames_half_open": [JOIN_START, PREFIX_COUNT],
                 "new_dissolve_seconds_half_open": [JOIN_START / FPS, PREFIX_COUNT / FPS],
                 "outgoing_prefix_frames_half_open": [367, 385],
                 "incoming_F05_frames_half_open": [0, 18], "then_F05_frames_half_open": [18, 144],
                 "blend_incoming_alpha": "(overlap_index+1)/18; overlap_index=0..17",
                 "earlier_joins_are_not_rebuilt_from_raw_sources": True,
                 "prefix_file_sha_preserved_but_frames_reencoded": True},
        "full_decode": scan, "streams": streams, "fidelity": fidelity, "QA": qa,
        "source_hashes_verified_unchanged_after_encode": True,
        "speed": {"source_factor": 1.0, "retime": False, "frame_order_preserved": True,
                  "reverse_repeat_freeze_interpolation": False, "individual_source_PTS_measured": False},
        "crop": False, "scale": False, "text": False, "audio": False,
        "external_write": False, "publication": False,
        "assistant_continuous_normal_speed_visual_review": None, "user_dynamic_approval": None,
        "limits": ["All-frame decoding and codec fidelity do not establish gait, wardrobe, identity, scene or rhythm quality.",
                   "Root must inspect the new J45 and full-to-half motion; only the earlier four-look exact film has user acceptance.",
                   "No normal-speed continuous playback or publishability is inferred by this script.",
                   "Earlier accepted double edges and short stairs remain in the protected prefix."]}
    receipt_path = destination / "edit_receipt.json"
    native.json_new(receipt_path, receipt)
    return {"receipt": str(receipt_path), "output": receipt["output"], "QA_folder": str(destination / "QA")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="NEW native source in F05_half_motion_01")
    parser.add_argument("--source-sha", help="Exact lowercase SHA256 of the root-inspected source")
    parser.add_argument("--source-qa-eligible", action="store_true", help="Root permits exact source in a research edit")
    parser.add_argument("--preflight-only", action="store_true", help="Decode/check inputs without creating media or QA")
    parser.add_argument("--version", default="v1", help="Exclusive new output version v1,v2,...")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args), ensure_ascii=False, indent=2))
    except Exception as error:
        print(json.dumps({"status": "stopped_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
