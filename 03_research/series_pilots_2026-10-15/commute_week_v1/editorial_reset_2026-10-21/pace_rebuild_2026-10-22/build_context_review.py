"""Isolated F02-only partial pace context candidate from five raw native sources.

No source/media overwrite, crop, retiming, freeze, repeat, text, or audio.
All 511 decoded frames are checked against the intended raw-frame composite.
Technical fidelity is not user or dynamic acceptance.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RESET = HERE.parent
COMMUTE = RESET.parent
BRIDGE = COMMUTE / "production_bridge_2026-10-19"
HELPER = BRIDGE / "F04/close_tracking_proposal_2026-10-20/close_join_review_2026-10-21/build_close_study.py"
spec = importlib.util.spec_from_file_location("mira_pace_context_native", HELPER)
if spec is None or spec.loader is None:
    raise ImportError(HELPER)
close = importlib.util.module_from_spec(spec)
spec.loader.exec_module(close)
native = close.native
import numpy as np

SIZE, FPS, OVERLAP, TOTAL = (720, 1280), 24, 18, 511
OUT = HERE / "context_review_v1"
SOURCES = [
    ("F01_original", BRIDGE / "F01/F01_source.mp4", "6a9bf3204aadad28dc710aa914592e26851a03e47209c5bd9b682286b184fa50", 0, 78),
    ("F02_NEW_pace_partial", HERE / "F02/F02_pace_source.mp4", "f6fcd8e02e99a6dd1b6282d5b5eb5e2b0eeca0bacc10c54d83940cfa4a0bbdf6", 0, 145),
    ("F03_original", BRIDGE / "F03/F03_source.mp4", "26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5", 1, 109),
    ("F04_existing_full", RESET / "F04_motion_01/F04_source.mp4", "e32ee2f282b80dec8b8666d6755c9d2e77e5def6850bc53c89b5333927cd2208", 0, 108),
    ("F05_existing_full_to_half", RESET / "F05_half_motion_01/F05_half_source.mp4", "c2d9f0442ea0d9b9c50674fb959b96ae53a8264c3947c509aa91f05e4bec9aa9", 0, 144),
]
PROTECTED = {p: sha for _, p, sha, _, _ in SOURCES}
PROTECTED.update({
    BRIDGE / "F02/motion_retry_01/F02_source.mp4": "cc23a3e22b5d51b2db42cc87b33371f73189b25b101cc37fff3a070dd68800b0",
    RESET / "F05_half_motion_01/five_look_review_2026-10-22/v1/review.mp4": "e4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc",
    RESET / "four_look_review/v1/review.mp4": "3c0f3fa5bb0c90d0d9b5d434ada37cd5dbe130658d5bff24c01143feb77f1f94",
})
JOINS = [
    {"id": "J12", "output_half_open": [60, 78], "outgoing": ["F01_original", 60, 78], "incoming": ["F02_NEW_pace_partial", 0, 18]},
    {"id": "J23", "output_half_open": [187, 205], "outgoing": ["F02_NEW_pace_partial", 127, 145], "incoming": ["F03_original", 1, 19]},
    {"id": "J34", "output_half_open": [277, 295], "outgoing": ["F03_original", 91, 109], "incoming": ["F04_existing_full", 0, 18]},
    {"id": "J45", "output_half_open": [367, 385], "outgoing": ["F04_existing_full", 90, 108], "incoming": ["F05_existing_full_to_half", 0, 18]},
]


def selected(path, begin, end):
    with native.native_reader(path) as reader:
        for i, raw in enumerate(reader):
            if i >= end:
                break
            if i >= begin:
                yield native.Image.frombytes("RGB", SIZE, raw)


def sequence(mapping=None):
    readers = [selected(p, begin, end) for _, p, _, begin, end in SOURCES]
    output_index = 0

    def record(image, components, join=None):
        nonlocal output_index
        if mapping is not None:
            mapping.append({"output_frame": output_index, "components": components, "join": join})
        output_index += 1
        return image

    try:
        for slot, (role, path, sha, begin, end) in enumerate(SOURCES):
            start = begin + (OVERLAP if slot else 0)
            stop = end - (OVERLAP if slot < len(SOURCES) - 1 else 0)
            for index in range(start, stop):
                yield record(next(readers[slot]), [{"role": role, "native_frame": index, "weight": 1.0}])
            if slot == len(SOURCES) - 1:
                continue
            incoming_role, _, _, incoming_begin, _ = SOURCES[slot + 1]
            for k in range(OVERLAP):
                alpha = (k + 1) / OVERLAP
                image = native.Image.blend(next(readers[slot]), next(readers[slot + 1]), alpha)
                yield record(image, [
                    {"role": role, "native_frame": end - OVERLAP + k, "weight": 1 - alpha},
                    {"role": incoming_role, "native_frame": incoming_begin + k, "weight": alpha},
                ], JOINS[slot]["id"])
    finally:
        for reader in readers:
            reader.close()


def verify_fidelity(path):
    expected = sequence()
    count, total_mae, worst_mae, min_psnr = 0, 0.0, 0.0, float("inf")
    errors = []
    try:
        with native.native_reader(path) as actual:
            for i, raw in enumerate(actual):
                try:
                    intended = next(expected)
                except StopIteration as error:
                    raise ValueError("Output longer than intended 511 frames") from error
                a = np.asarray(intended, dtype=np.int16)
                b = np.frombuffer(raw, dtype=np.uint8).reshape(SIZE[1], SIZE[0], 3).astype(np.int16)
                diff = a - b
                mae = float(np.abs(diff).mean())
                mse = float(np.square(diff.astype(np.float32)).mean())
                psnr = 100.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)
                count += 1
                total_mae += mae
                worst_mae = max(worst_mae, mae)
                min_psnr = min(min_psnr, psnr)
                errors.append({"output_frame": i, "mean_absolute_RGB_error": mae, "PSNR_dB": psnr})
        try:
            next(expected)
        except StopIteration:
            pass
        else:
            raise ValueError("Output shorter than intended composite")
    finally:
        expected.close()
    passed = count == TOTAL and worst_mae <= 3.0 and min_psnr >= 32.0
    result = {"frames_compared": count, "mean_absolute_RGB_error_0_to_255": total_mae / count,
              "worst_frame_MAE": worst_mae, "minimum_frame_PSNR_dB": min_psnr,
              "codec_tolerance": {"worst_frame_MAE_max": 3.0, "minimum_PSNR_dB_min": 32.0},
              "within_codec_tolerance": passed, "pixel_or_byte_identity_claim": False}
    native.json_new(OUT / "QA/all_frame_fidelity.json", {"summary": result, "frames": errors})
    if not passed:
        raise ValueError("All-frame fidelity exceeds codec tolerance: " + json.dumps(result))
    return result


def qa_boards(path):
    qa = OUT / "QA"
    frames_dir = qa / "frames"
    frames_dir.mkdir()
    full = native.uniform_indices(TOTAL, 25)
    dense = {}
    for join in JOINS[:2]:
        begin, end = join["output_half_open"]
        dense[join["id"]] = sorted(set(range(begin - 9, end + 10, 3)) | {end - 1})
    wanted = set(full)
    for indices in dense.values():
        wanted.update(indices)
    found = {}
    with native.native_reader(path) as reader:
        for i, raw in enumerate(reader):
            if i in wanted:
                found[i] = native.Image.frombytes("RGB", SIZE, raw)
                native.image_new(frames_dir / f"f{i:04d}.png", found[i])
    if set(found) != wanted:
        raise ValueError("QA sample missing")
    native.contact_sheet([(i, found[i]) for i in full], qa / "full25.png",
                         "F02 ONLY partial context; F03 late/J34 unchanged; NOT approved")
    feet_crop = (0, 740, 720, 1280)
    for label, indices in dense.items():
        native.contact_sheet([(i, found[i]) for i in indices], qa / f"{label}_every3_full.png",
                             f"{label} new context: every3 native frames plus last overlap; NOT accepted")
        native.contact_sheet([(i, found[i].crop(feet_crop)) for i in indices], qa / f"{label}_every3_feet.png",
                             f"{label} QA FOOT CROP ONLY; output movie remains FULL native raster")
    return {"full25_indices": full, "join_every3_indices": dense,
            "frames_saved_full_native_size": list(SIZE),
            "feet_crop_QA_only_xyxy": list(feet_crop),
            "movie_crop_or_scale": False,
            "continuous_normal_speed_visual_review_performed_by_script": False}


def main():
    if os.path.lexists(OUT):
        raise FileExistsError(f"Preserve existing or partial output: {OUT}")
    for path, sha in PROTECTED.items():
        native.verified_source(path, sha)
    hashes_before = {str(path): native.sha256(path) for path in PROTECTED}
    helper_sha = native.sha256(HELPER)
    scans = {}
    for role, path, sha, begin, end in SOURCES:
        scans[role] = native.full_decode(path)
        if scans[role]["decoded_frames"] < end:
            raise ValueError(f"Insufficient frames in {role}")
        if scans[role]["metadata"].get("rotate", 0) != 0:
            raise ValueError("Rotated source not permitted")
    OUT.mkdir()
    (OUT / "QA").mkdir()
    output = OUT / "review.mp4"
    mapping = []
    frames = sequence(mapping)
    try:
        close.encode_exclusive(output, frames)
    finally:
        frames.close()
    if len(mapping) != TOTAL:
        raise ValueError(f"Mapped {len(mapping)} frames, expected 511")
    native.json_new(OUT / "QA/frame_mapping.json", mapping)
    scan = native.full_decode(output)
    if scan["decoded_frames"] != TOTAL:
        raise ValueError("Full decode count is not 511")
    streams = native.stream_inventory(output)
    if streams["audio_stream_present"]:
        raise ValueError("Silent output contains audio")
    fidelity = verify_fidelity(output)
    qa = qa_boards(output)
    for path, sha in PROTECTED.items():
        native.verified_source(path, sha)
    hashes_after = {str(path): native.sha256(path) for path in PROTECTED}
    if native.sha256(HELPER) != helper_sha:
        raise ValueError("Established helper changed during render")
    receipt = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "ONLY_F02_partial_context_candidate_NOT_user_approved",
        "operator_authority": "Root explicitly requested isolated raw-source context candidate; not user dynamic acceptance",
        "sources": [{"role": role, "path": str(path), "sha256": sha, "selected_frames_half_open": [begin, end]} for role, path, sha, begin, end in SOURCES],
        "source_scans": scans,
        "output": {"path": str(output), "sha256": native.sha256(output), "bytes": output.stat().st_size,
                   "frames": TOTAL, "fps": FPS, "size": list(SIZE), "duration_seconds": TOTAL / FPS},
        "edit": {"formula": "78+145+108+108+144-4*18=511", "joins": JOINS,
                 "blend_incoming_alpha": "(overlap_index+1)/18; overlap_index=0..17",
                 "rebuilt_direct_from_raw_sources": True, "only_source_selection_changed_from_original_EDL": "F02"},
        "full_decode": scan, "streams": streams, "fidelity": fidelity, "QA": qa,
        "protected_hashes_before": hashes_before, "protected_hashes_after": hashes_after,
        "all_protected_sources_original_F02_original_21s_and_4look_unchanged": hashes_before == hashes_after,
        "builder": {"path": str(Path(__file__).resolve()), "sha256": native.sha256(Path(__file__).resolve()),
                    "established_helper": str(HELPER), "helper_sha256_before_after": helper_sha},
        "speed_factor": 1.0, "retime": False, "crop": False, "scale": False, "text": False, "audio": False,
        "freeze_repeat_reverse_interpolation": False, "frame_order_preserved": True,
        "individual_source_PTS_measured": False,
        "external_write": False, "publication": False, "user_dynamic_approval": None,
        "assistant_continuous_normal_speed_visual_review": None,
        "limits": [
            "Only F02 is replaced. F03 late cadence and J34 are unchanged; whole-film cadence is NOT claimed fixed.",
            "New F02 can change J12 and J23; inspect both before acceptance.",
            "Direct raw-source rebuild avoids prior intermediate re-encoding, so unchanged shots are not pixel-identical to old film.",
            "Full decode/fidelity proves intended edit encoding, not gait, identity, environment, comfort or publishing pass.",
            "Existing double edges/stairs and other unmodified source limitations remain."]}
    native.json_new(OUT / "build_manifest.json", receipt)
    with (OUT / "README.md").open("x", encoding="utf-8") as stream:
        stream.write("# F02-only partial context candidate\n\nOnly F02 source replaced in the existing 511-frame five-look EDL. Native 24 fps / 720×1280; all joins retain 18 frames and incoming alpha (k+1)/18. No retiming, crop, text or audio.\n\nF03 late cadence and J34 remain unchanged. This is not a claim that whole-film cadence is repaired; no user dynamic or publication approval. Sources and original films are retained unchanged.\n\nFull decoded-output versus intended raw-frame composite checked for all 511 frames within documented CRF18 codec tolerance. QA foot crops are diagnostic only; no movie crop. See build_manifest.json and QA/.\n")
    print(json.dumps({"output": receipt["output"], "fidelity": fidelity, "manifest": str(OUT / "build_manifest.json"), "QA": str(OUT / "QA")}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
