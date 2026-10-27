"""Build isolated close-shot research candidates after exact source inspection.

This script only reads the protected prefix and the two new native sources.
Supply the exact inspected L02 source SHA and explicit local-edit eligibility.
No source, accepted film, canonical document, or remote file is overwritten.
Technical checks do not grant dynamic acceptance or publication approval.
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
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CLOSE = HERE.parent
BRIDGE_ROOT = CLOSE.parent.parent
HELPER = BRIDGE_ROOT / "F02/build_first_pair_review.py"
spec = importlib.util.spec_from_file_location("mira_guarded_close_native", HELPER)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load established native video helper: {HELPER}")
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
import numpy as np

SIZE, FPS, OVERLAP = (720, 1280), 24, 18
PUSH = CLOSE / "F03_pushin_motion_01/F03_pushin_source.mp4"
CLOSE_L02 = CLOSE / "F04_close_motion_01/F04_close_source.mp4"
PREFIX = BRIDGE_ROOT / "F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4"
PUSH_SHA = "452baf11a5d6b01e62e522bddb2c1aac8f67938c902eee86d43436cfd569b814"
PREFIX_SHA = "f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33"
COUNTS = {"protected_prefix": 331, "L03_pushin": 145, "L02_close": 145}


def encode_exclusive(path: Path, frames) -> None:
    descriptor, filename = tempfile.mkstemp(prefix=".close_study_", suffix=".mp4", dir=path.parent)
    os.close(descriptor)
    temporary = Path(filename)
    writer = native.imageio_ffmpeg.write_frames(
        str(temporary), SIZE, fps=FPS, codec="libx264", pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p", quality=None, macro_block_size=1,
        ffmpeg_log_level="error",
        output_params=["-crf", "18", "-preset", "medium", "-movflags", "+faststart", "-an"],
    )
    try:
        writer.send(None)
        for frame in frames:
            writer.send(frame.tobytes())
        writer.close()
        if not temporary.is_file() or not temporary.stat().st_size:
            raise ValueError("Encoder produced no output")
        with temporary.open("rb") as source, path.open("xb") as target:
            shutil.copyfileobj(source, target, 1024 * 1024)
    finally:
        writer.close()
        temporary.unlink(missing_ok=True)


def make_sequence(sources, mapping: list | None = None):
    """Consume native frames in order once, with 18-frame overlaps."""
    readers = [native.selected_frames(path, count) for role, path, count in sources]
    number = 0

    def record(frame, components, join=None):
        nonlocal number
        if mapping is not None:
            mapping.append({"output_frame": number, "components": components, "join": join})
        number += 1
        return frame

    try:
        for slot, (role, path, count) in enumerate(sources):
            start = OVERLAP if slot else 0
            stop = count - OVERLAP if slot < len(sources) - 1 else count
            for index in range(start, stop):
                yield record(next(readers[slot]), [{"role": role, "native_frame": index, "weight": 1.0}])
            if slot == len(sources) - 1:
                continue
            next_role = sources[slot + 1][0]
            join = f"{role}_to_{next_role}"
            for overlap_index in range(OVERLAP):
                alpha = (overlap_index + 1) / OVERLAP
                first, second = next(readers[slot]), next(readers[slot + 1])
                yield record(native.Image.blend(first, second, alpha), [
                    {"role": role, "native_frame": count - OVERLAP + overlap_index, "weight": 1 - alpha},
                    {"role": next_role, "native_frame": overlap_index, "weight": alpha},
                ], join)
    finally:
        for reader in readers:
            reader.close()


def fidelity_check(output: Path, sources, total: int) -> dict:
    """Compare decoded candidate to the intended full-raster composite, not bytes."""
    expected = make_sequence(sources)
    count, mae_sum, worst_mae, min_psnr = 0, 0.0, 0.0, float("inf")
    pure_prefix_count, prefix_mae_sum, prefix_worst_mae = 0, 0.0, 0.0
    prefix_min_psnr = float("inf")
    pure_prefix_stop = COUNTS["protected_prefix"] - OVERLAP if sources[0][0] == "protected_prefix" else 0
    try:
        with native.native_reader(output) as actual:
            for index, raw in enumerate(actual):
                intended = next(expected)
                a = np.asarray(intended, dtype=np.int16)
                b = np.frombuffer(raw, dtype=np.uint8).reshape(SIZE[1], SIZE[0], 3).astype(np.int16)
                error = a - b
                mae = float(np.abs(error).mean())
                mse = float(np.square(error.astype(np.float32)).mean())
                psnr = 100.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)
                count += 1
                mae_sum += mae
                worst_mae, min_psnr = max(worst_mae, mae), min(min_psnr, psnr)
                if index < pure_prefix_stop:
                    pure_prefix_count += 1
                    prefix_mae_sum += mae
                    prefix_worst_mae = max(prefix_worst_mae, mae)
                    prefix_min_psnr = min(prefix_min_psnr, psnr)
        try:
            next(expected)
        except StopIteration:
            pass
        else:
            raise ValueError("Candidate ended before intended composite")
    finally:
        expected.close()
    if count != total:
        raise ValueError(f"Fidelity check decoded {count}, expected {total}")
    # CRF18 introduces expected quantization differences; do not claim pixel identity.
    passed = worst_mae <= 3.0 and min_psnr >= 32.0
    result = {
        "all_output_frames_compared_to_intended_native_composite": count,
        "mean_absolute_RGB_error_0_to_255": mae_sum / count,
        "worst_frame_mean_absolute_RGB_error": worst_mae,
        "minimum_frame_PSNR_dB": min_psnr,
        "codec_tolerance": {"worst_frame_MAE_max": 3.0, "minimum_frame_PSNR_dB_min": 32.0},
        "within_codec_tolerance": passed,
        "byte_identical_or_pixel_identical_claim": False,
        "protected_prefix_pure_frames": {
            "frames_compared": pure_prefix_count,
            "output_half_open": [0, pure_prefix_stop] if pure_prefix_stop else None,
            "mean_absolute_RGB_error": prefix_mae_sum / pure_prefix_count if pure_prefix_count else None,
            "worst_frame_mean_absolute_RGB_error": prefix_worst_mae if pure_prefix_count else None,
            "minimum_frame_PSNR_dB": prefix_min_psnr if pure_prefix_count else None,
        },
    }
    if not passed:
        raise ValueError("Candidate differs from intended native composite beyond codec tolerance: " + json.dumps(result))
    return result


def make_boards(output: Path, qa: Path, sources, total: int) -> dict:
    qa.mkdir()
    frame_dir = qa / "native_frames"
    frame_dir.mkdir()
    full = native.uniform_indices(total)
    joins = []
    offset = 0
    for slot, (role, path, count) in enumerate(sources[:-1]):
        begin = offset + count - OVERLAP
        end = begin + OVERLAP
        label = f"J{slot + 1}_{role}_to_{sources[slot + 1][0]}"
        indices = list(range(max(0, begin - 8), min(total, end + 8)))
        joins.append({"id": label, "begin": begin, "end": end, "indices": indices,
                      "outgoing_role": role, "incoming_role": sources[slot + 1][0],
                      "outgoing_frames_half_open": [count - OVERLAP, count],
                      "incoming_frames_half_open": [0, OVERLAP]})
        offset = begin
    keep = set(full)
    for join in joins:
        keep.update(join["indices"])
    found = {}
    with native.native_reader(output) as reader:
        for index, raw in enumerate(reader):
            if index in keep:
                frame = native.Image.frombytes("RGB", SIZE, raw)
                found[index] = frame
                native.image_new(frame_dir / f"frame_{index:06d}.png", frame)
    if set(found) != keep:
        raise ValueError("Some full-raster QA checkpoints are missing")
    native.contact_sheet([(index, found[index]) for index in full],
                         qa / "full_25_checkpoints.png", "Full-raster checkpoints; visual review pending")
    for join_number, join in enumerate(joins, start=1):
        native.contact_sheet([(index, found[index]) for index in join["indices"]],
                             qa / f"join_{join_number}_dense.png",
                             f"{join['id']}:18 dissolve frames+8 each side; review pending")
        join["output_frames_half_open"] = [join.pop("begin"), join.pop("end")]
        join["output_seconds_half_open"] = [value / FPS for value in join["output_frames_half_open"]]
    return {"full_checkpoint_indices": full, "joins": joins,
            "all_dissolve_frames_extracted": True, "individual_frames_size": list(SIZE),
            "boards_are_reduced_full_raster_thumbnails": True, "crop": False}


def build(l02_sha: str, version: str, eligibility: bool, include_prefix: bool) -> dict:
    if not eligibility:
        raise ValueError("Root must explicitly confirm this exact L02 source is eligible for local edit")
    if not re.fullmatch(r"[0-9a-f]{64}", l02_sha):
        raise ValueError("Supply exact lowercase SHA256 of the inspected L02 source")
    if not re.fullmatch(r"v[1-9][0-9]*", version):
        raise ValueError("Version must be v1, v2, ...")
    # Keep actual media/QA paths under Windows legacy path limits as well.
    destination = HERE / version
    if os.path.lexists(destination):
        raise FileExistsError(f"Preserve prior or partial output; select another version: {destination}")
    protected = [(PUSH, PUSH_SHA), (CLOSE_L02, l02_sha), (PREFIX, PREFIX_SHA)]
    for path, digest in protected:
        native.verified_source(path, digest)
    source_scans = {}
    for role, path, count in [("L03_pushin", PUSH, 145), ("L02_close", CLOSE_L02, 145),
                              ("protected_prefix", PREFIX, 331)]:
        scan = native.full_decode(path)
        if scan["decoded_frames"] != count:
            raise ValueError(f"{role} exact count differs: {scan['decoded_frames']} != {count}")
        source_scans[role] = scan
    helper_sha = native.sha256(HELPER)
    destination.mkdir()
    configurations = [("local_close", [("L03_pushin", PUSH, 145), ("L02_close", CLOSE_L02, 145)], 272)]
    if include_prefix:
        configurations.append(("prefix_plus_close", [("protected_prefix", PREFIX, 331),
            ("L03_pushin", PUSH, 145), ("L02_close", CLOSE_L02, 145)], 585))
    outputs = []
    for label, sources, total in configurations:
        section = destination / ("local" if label == "local_close" else "context")
        section.mkdir()
        path = section / "review.mp4"
        mapping = []
        frames = make_sequence(sources, mapping)
        try:
            encode_exclusive(path, frames)
        finally:
            frames.close()
        scan = native.full_decode(path)
        if scan["decoded_frames"] != total or len(mapping) != total:
            raise ValueError(f"{label}: exact frame count does not match {total}")
        streams = native.stream_inventory(path)
        if streams["audio_stream_present"]:
            raise ValueError("Unexpected audio in silent research preview")
        fidelity = fidelity_check(path, sources, total)
        qa = section / "QA"
        boards = make_boards(path, qa, sources, total)
        native.json_new(qa / "frame_mapping.json", mapping)
        native.json_new(qa / "technical_scan.json", scan)
        native.json_new(qa / "decoded_fidelity.json", fidelity)
        result = {"role": label, "path": str(path), "sha256": native.sha256(path),
                  "bytes": path.stat().st_size, "frames": total, "seconds": total / FPS,
                  "decoded_scan": scan, "streams": streams, "fidelity": fidelity,
                  "QA_folder": str(qa), "QA": boards}
        outputs.append(result)
    for path, digest in protected:
        native.verified_source(path, digest)
    if native.sha256(HELPER) != helper_sha:
        raise ValueError("Imported helper changed during build")
    receipt = {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "status": "research_close_candidates_pending_visual_review", "execution": "local",
        "purpose": "Show full-to-close L03 camera move before same-scale L02 outfit dissolve",
        "source_eligible_for_local_edit_attested_by_operator": eligibility,
        "source_QA_eligibility_is_user_dynamic_approval": False,
        "builder_path": str(Path(__file__).resolve()), "builder_sha256": native.sha256(Path(__file__).resolve()),
        "native_helper_path": str(HELPER), "native_helper_sha256": helper_sha,
        "sources": [{"path": str(path), "sha256": digest} for path, digest in protected],
        "source_scans": source_scans, "native_size": list(SIZE), "fps": FPS,
        "overlap_frames": OVERLAP, "overlap_seconds": OVERLAP / FPS,
        "blend_weight": "incoming_alpha=(overlap_index+1)/18; overlap_index=0..17",
        "local_frame_formula": "145+145-18=272", "full_frame_formula": "331+145+145-36=585",
        "protected_prefix_join_context": {
            "prefix_original_file_unchanged_SHA_verified_before_and_after": True,
            "prefix_unblended_frames_half_open": [0, 313],
            "new_first_join_prefix_frames_half_open": [313, 331],
            "corresponding_original_F03_frames_half_open": [127, 145],
            "bridge_first_frame_is_original_F03_frame127": "root-provided source derivation; source visual match reviewed separately",
            "old_joins_are_not_rebuilt_from_original_sources": True,
            "new_encode_has_expected_codec_differences": True,
        },
        "outputs": outputs, "source_hashes_verified_unchanged_after_encode": True,
        "speed": {"all_source_factors": 1.0, "native_frame_order_preserved": True,
                  "retime": False, "reverse_repeat_freeze_interpolation": False,
                  "source_individual_PTS_measured": False},
        "framing_transform": "none; native720x1280 full raster", "text": "none", "audio": "none",
        "source_or_old_film_overwrite": False, "cloud_write": False, "publication": False,
        "assistant_continuous_visual_review": None, "user_dynamic_approval": None,
        "five_look_film_complete": False, "publishable": False,
        "limitations": [
            "This builder checks media and intended edit fidelity; it does not approve identity, wardrobe, cadence or background.",
            "No feet are visible in the planned L02 close shot; zero foot sliding cannot be verified there.",
            "Dissolve double images require normal-speed comfort review; technical encode success is not editorial approval.",
            "The accepted prefix file is preserved byte-for-byte, but its frames are re-encoded in the optional continuation.",
        ],
    }
    receipt_path = destination / "close_study_edit_receipt.json"
    native.json_new(receipt_path, receipt)
    return {"receipt": str(receipt_path), "outputs": [{key: value for key, value in item.items()
        if key in {"role", "path", "sha256", "frames", "seconds", "QA_folder"}} for item in outputs]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--l02-sha", required=True, help="Exact source SHA after root source inspection")
    parser.add_argument("--source-qa-eligible", action="store_true", help="Root permits this exact source in a local research edit")
    parser.add_argument("--include-prefix", action="store_true", help="Also render isolated protected-prefix continuation")
    parser.add_argument("--version", default="v1", help="Exclusive new version v1,v2,...")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.l02_sha, args.version, args.source_qa_eligible, args.include_prefix), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
