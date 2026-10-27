"""Append exact reviewed F05 to the protected working commute context.

Only run after root source inspection and explicit research-edit eligibility.
All old media remains unchanged. Output is a separate research candidate;
local L03/L02 approval is not approval of the entire working context or film.
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
BRIDGE = HERE.parent.parent
CLOSE = BRIDGE / "F04/close_tracking_proposal_2026-10-20"
CLOSE_HELPER = CLOSE / "close_join_review_2026-10-21/build_close_study.py"
spec = importlib.util.spec_from_file_location("mira_close_native_append", CLOSE_HELPER)
if spec is None or spec.loader is None:
    raise ImportError(f"Missing established close editor: {CLOSE_HELPER}")
close = importlib.util.module_from_spec(spec)
spec.loader.exec_module(close)
native = close.native
import numpy as np

SIZE, FPS, OVERLAP = (720, 1280), 24, 18
CONTEXT = CLOSE / "close_join_review_2026-10-21/v2/context/review.mp4"
CONTEXT_SHA = "0f1c2f8a7dbe4b79d346faa2b75c061f260b711671f51e17f88a07283e89d9bd"
ACCEPTED_ORIGINAL = BRIDGE / "F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4"
ORIGINAL_SHA = "f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33"
ACCEPTED_LOCAL = CLOSE / "close_join_review_2026-10-21/v2/local/review.mp4"
LOCAL_SHA = "7dbd3d6c8ec11203b6a4decaa44c30bbfae2576318bea241ff914460e40f7e49"
F05 = HERE.parent / "motion_01/F05_source.mp4"
FIRST_SHA = "9bc90ffa51bdad22106401647fef10fbf20b2da6faf88192b1b6f8191aba97d2"
END_SHA = "9af51b785d2bd104751cd2502deaa86f29cad217621643cef98c23d0ff1f16e7"
CONTEXT_N, F05_N, TOTAL = 585, 145, 712
JOIN_START = CONTEXT_N - OVERLAP


def fidelity(output: Path, sources) -> dict:
    expected = close.make_sequence(sources)
    count = 0
    error_sum, max_mae, min_psnr = 0.0, 0.0, float("inf")
    prefix_count, prefix_sum, prefix_max, prefix_min_psnr = 0, 0.0, 0.0, float("inf")
    try:
        with native.native_reader(output) as actual:
            for index, raw in enumerate(actual):
                intended = next(expected)
                delta = np.asarray(intended, dtype=np.int16) - np.frombuffer(raw, dtype=np.uint8).reshape(SIZE[1], SIZE[0], 3).astype(np.int16)
                mae = float(np.abs(delta).mean())
                mse = float(np.square(delta.astype(np.float32)).mean())
                psnr = 100.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)
                count += 1
                error_sum += mae
                max_mae = max(max_mae, mae)
                min_psnr = min(min_psnr, psnr)
                if index < JOIN_START:
                    prefix_count += 1
                    prefix_sum += mae
                    prefix_max = max(prefix_max, mae)
                    prefix_min_psnr = min(prefix_min_psnr, psnr)
        try:
            next(expected)
        except StopIteration:
            pass
        else:
            raise ValueError("Output shorter than planned composite")
    finally:
        expected.close()
    if count != TOTAL or prefix_count != JOIN_START:
        raise ValueError("Full-frame fidelity verification count differs")
    passed = max_mae <= 3.0 and min_psnr >= 32.0
    result = {
        "all_decoded_frames_compared": count,
        "mean_absolute_RGB_error_0_to_255": error_sum / count,
        "worst_frame_MAE": max_mae, "minimum_frame_PSNR_dB": min_psnr,
        "thresholds": {"worst_frame_MAE_max": 3.0, "minimum_frame_PSNR_dB_min": 32.0},
        "within_codec_tolerance": passed,
        "unblended_working_context": {"frames_compared": prefix_count,
            "half_open_frames": [0, JOIN_START], "mean_absolute_RGB_error": prefix_sum / prefix_count,
            "worst_frame_MAE": prefix_max, "minimum_frame_PSNR_dB": prefix_min_psnr},
        "byte_identical_or_pixel_identical_claim": False,
    }
    if not passed:
        raise ValueError("Composite fidelity outside codec tolerance: " + json.dumps(result))
    return result


def build(source_sha: str, version: str, eligible: bool) -> dict:
    if not eligible:
        raise ValueError("Root must explicitly permit this exact F05 source in a research edit")
    if not re.fullmatch(r"[0-9a-f]{64}", source_sha):
        raise ValueError("Exact lowercase inspected source SHA256 required")
    if not re.fullmatch(r"v[1-9][0-9]*", version):
        raise ValueError("Version must be v1,v2,...")
    destination = HERE / version
    if os.path.lexists(destination):
        raise FileExistsError("Preserve existing/partial output; use another version")
    protected = [(CONTEXT, CONTEXT_SHA), (F05, source_sha),
                 (ACCEPTED_ORIGINAL, ORIGINAL_SHA), (ACCEPTED_LOCAL, LOCAL_SHA)]
    for path, digest in protected:
        native.verified_source(path, digest)
    helper_sha = native.sha256(CLOSE_HELPER)
    native_helper_sha = native.sha256(close.HELPER)
    sources = [("working_context", CONTEXT, CONTEXT_N), ("F05_L04_pullback", F05, F05_N)]
    scans = {}
    for role, path, expected_count in sources:
        scan = native.full_decode(path)
        if scan["decoded_frames"] != expected_count:
            raise ValueError(f"{role} requires {expected_count} native frames")
        scans[role] = scan
    destination.mkdir()
    output = destination / "review.mp4"
    mapping = []
    images = close.make_sequence(sources, mapping)
    try:
        close.encode_exclusive(output, images)
    finally:
        images.close()
    output_scan = native.full_decode(output)
    if output_scan["decoded_frames"] != TOTAL or len(mapping) != TOTAL:
        raise ValueError("Expected exactly585+145-18=712 output frames")
    streams = native.stream_inventory(output)
    if streams["audio_stream_present"]:
        raise ValueError("Unexpected audio in silent research preview")
    comparison = fidelity(output, sources)
    qa = destination / "QA"
    boards = close.make_boards(output, qa, sources, TOTAL)
    native.json_new(qa / "frame_mapping.json", mapping)
    native.json_new(qa / "decoded_fidelity.json", comparison)
    native.json_new(qa / "technical_scan.json", output_scan)
    for path, digest in protected:
        native.verified_source(path, digest)
    if native.sha256(CLOSE_HELPER) != helper_sha or native.sha256(close.HELPER) != native_helper_sha:
        raise ValueError("An imported helper changed during encode")
    receipt = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "research_five_look_candidate_pending_visual_review",
        "execution": "local", "purpose": "Five-look continuous-route commute research sequence with final pullback",
        "model": "M03", "look_order": ["L01", "L05", "L03", "L02", "L04"],
        "sources": [{"path": str(path), "sha256": digest} for path, digest in protected],
        "source_full_decodes": scans,
        "source_eligible_for_local_research_edit_attested_by_root": eligible,
        "source_eligibility_equals_user_dynamic_approval": False,
        "user_acceptance_scope": {
            "original331frame_prefix": "historically accepted; source preserved",
            "local11p333s_L03_pushin_to_L02_close": {"sha256": LOCAL_SHA,
                "user_reply": "可以保留，繼續第五套", "accepted": True},
            "whole585frame_working_context_independently_user_accepted": False,
            "F05_first_still_SHA": FIRST_SHA, "F05_end_still_SHA": END_SHA,
            "F05_dynamic_accepted": None, "new_full_film_user_accepted": None,
        },
        "new_transition": {"type": "linear_cross_dissolve", "frames": OVERLAP,
            "seconds": OVERLAP / FPS, "output_frames_half_open": [JOIN_START, CONTEXT_N],
            "output_seconds_half_open": [JOIN_START / FPS, CONTEXT_N / FPS],
            "working_context_frames_half_open": [567, 585],
            "corresponding_F04_close_source_frames_half_open": [127, 145],
            "incoming_F05_frames_half_open": [0, OVERLAP],
            "weight": "incoming_alpha=(overlap_index+1)/18; overlap_index0..17",
            "first_still_derivation": "Wardrobe edit of extracted exact F04 actual source frame127, per root record",
        },
        "output": {"path": str(output), "sha256": native.sha256(output), "bytes": output.stat().st_size,
            "frames": TOTAL, "fps": FPS, "seconds": TOTAL / FPS, "native_size": list(SIZE),
            "frame_formula": "585+145-18=712", "full_decode": output_scan, "streams": streams},
        "fidelity": comparison, "QA": boards, "QA_folder": str(qa),
        "builder_path": str(Path(__file__).resolve()), "builder_SHA": native.sha256(Path(__file__).resolve()),
        "close_helper_path": str(CLOSE_HELPER), "close_helper_SHA": helper_sha,
        "native_helper_path": str(close.HELPER), "native_helper_SHA": native_helper_sha,
        "protected_sources_unchanged_before_and_after": True,
        "speed": {"source_factors": [1.0, 1.0], "native_order": True, "retime": False,
                  "freeze_repeat_reverse_interpolation": False, "individual_PTS_measured": False},
        "framing_transform": "none; full native raster", "text": "none", "audio": "none",
        "original_joins_rebuilt_from_original_sources": False,
        "working_context_file_modified": False, "accepted331frame_file_modified": False,
        "new_encode_has_codec_differences": True,
        "assistant_continuous_visual_review": None, "combined_dynamic_QA": "pending",
        "publishable": False, "cloud_write": False, "publication": False,
        "limitations": [
            "All-frame decoding and composite fidelity do not approve scene, face, clothes, walking, or transition comfort.",
            "The585frame working context is used as supplied; local acceptance does not establish whole-context acceptance.",
            "The original accepted331frame file and working585frame file remain byte-unchanged; new composite is re-encoded.",
            "New F05 motion and new full film need root and user visual review before any final approval.",
        ],
    }
    receipt_path = destination / "edit_receipt.json"
    native.json_new(receipt_path, receipt)
    return {"output": str(output), "sha256": receipt["output"]["sha256"], "frames": TOTAL,
            "seconds": TOTAL / FPS, "receipt": str(receipt_path), "QA": str(qa)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f05-sha", required=True)
    parser.add_argument("--source-qa-eligible", action="store_true")
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.f05_sha, args.version, args.source_qa_eligible), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
