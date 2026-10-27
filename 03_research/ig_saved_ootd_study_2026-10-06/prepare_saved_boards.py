"""Make review-only contact sheets from playing-browser screenshot evidence.

Original captures, metadata and their historical wrap values remain unchanged.
The corrected coverage describes sampling evidence, never full video QA.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def first_media(value):
    if isinstance(value, list):
        return value[0] if value else {}
    return value if isinstance(value, dict) else {}


def metadata_region(meta):
    for key in ("video_region_css", "video_region", "media_region"):
        region = meta.get(key)
        if isinstance(region, dict) and all(k in region for k in ("x", "y", "width", "height")):
            return key, region
    return None, None


def metadata_path_for(folder):
    direct = folder / "metadata.json"
    if direct.exists():
        return direct
    source_id = re.sub(r"_(?:(?:top|middle)_)?pass\d+$", "", folder.name)
    linked = folder.parent / source_id / "metadata.json"
    return linked if linked.exists() else None


def font(size=14):
    for path in (
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    ):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def describe_samples(folder, samples, duration):
    records = []
    cycle = 0
    previous_after = None
    epsilon = 0.015
    for source in samples:
        before = first_media(source.get("before"))
        after = first_media(source.get("after"))
        try:
            lower, upper = float(before["time"]), float(after["time"])
        except (KeyError, TypeError, ValueError):
            records.append({"file": source.get("file"), "usable": False, "reason": "missing media time"})
            continue
        inter_wrap = previous_after is not None and lower < previous_after - epsilon
        if inter_wrap:
            cycle += 1
        cycle_before = cycle
        intra_wrap = upper < lower - epsilon
        if intra_wrap:
            cycle += 1
        playing = before.get("paused") is False and after.get("paused") is False
        valid = playing and not intra_wrap and upper >= lower and (folder / source["file"]).exists()
        row = {
            "file": source["file"],
            "before_seconds": lower,
            "after_seconds": upper,
            "cycle_before": cycle_before,
            "cycle_after": cycle,
            "inter_capture_wrap": inter_wrap,
            "intra_capture_wrap": intra_wrap,
            "absolute_bracket_seconds": [cycle_before * duration + lower, cycle * duration + upper],
            "playing_before_and_after": playing,
            "usable": valid,
            "capture_bracket_width_seconds": upper - lower if not intra_wrap else None,
            "wide_capture_bracket": not intra_wrap and upper - lower > 0.35,
            "representative_time_seconds": (lower + upper) / 2 if valid else None,
            "reason": "crossing bracket: exact screenshot phase uncertain" if intra_wrap else (None if valid else "not playing or invalid/missing evidence"),
        }
        records.append(row)
        previous_after = upper
    return records


def make_boards(folder: Path):
    metadata_path = metadata_path_for(folder)
    if metadata_path is None:
        raise ValueError(f"Missing direct or explicitly named same-source metadata: {folder}")
    meta = load_json(metadata_path)
    raw = load_json(folder / "samples.json")
    samples = raw["samples"] if isinstance(raw, dict) else raw
    duration = float(meta.get("duration_media_seconds") or meta.get("duration") or first_media(samples[0].get("before"))["duration"])
    records = describe_samples(folder, samples, duration)
    valid = [row for row in records if row["usable"]]
    if not valid:
        raise ValueError(f"No valid playing timestamp brackets in {folder}")
    bin_count = 24 if duration <= 15 else 36
    selected = []
    unused = list(valid)
    for number in range(bin_count):
        target = duration * (number + 0.5) / bin_count
        if not unused:
            break
        chosen = min(unused, key=lambda row: abs(row["representative_time_seconds"] - target))
        unused.remove(chosen)
        selected.append({**chosen, "target_bin": number, "target_seconds": target})
    selected.sort(key=lambda row: row["representative_time_seconds"])

    region_key, region = metadata_region(meta)
    screenshot_mode = raw.get("screenshot_mode", meta.get("screenshot_mode")) if isinstance(raw, dict) else meta.get("screenshot_mode")
    partial_viewport = screenshot_mode in ("viewport_top_only", "viewport_middle_only")
    if partial_viewport:
        region_key, region = None, None
    qa = folder / "qa"
    qa.mkdir(exist_ok=True)
    per_board = math.ceil(len(selected) / 2)
    names = []
    label_font = font(13)
    header_font = font(18)
    for board_index in range(2):
        group = selected[board_index * per_board:(board_index + 1) * per_board]
        if not group:
            continue
        columns = 6
        rows = math.ceil(len(group) / columns)
        tile_w, image_h, label_h, header_h = 202, 359, 42, 65
        board = Image.new("RGB", (columns * tile_w, header_h + rows * (image_h + label_h)), "#f4f1ed")
        draw = ImageDraw.Draw(board)
        title = f"{meta.get('author', '')} | {meta.get('id', folder.name)} | {duration:.3f}s | board {board_index + 1}"
        draw.text((10, 8), title, fill="#191919", font=header_font)
        warning = "PARTIAL VIEWPORT ONLY; uncropped full body unobserved; bracketed times, no exact cuts/audio" if partial_viewport else "PLAYING SCREENSHOT SAMPLES; timestamps bracket capture, not exact cut times; audio unreviewed"
        draw.text((10, 36), warning, fill="#303030", font=label_font)
        for index, row in enumerate(group):
            with Image.open(folder / row["file"]) as original:
                picture = original.convert("RGB")
            if region:
                # Metadata contains the observed browser media rectangle. This
                # evidence-only crop never changes the underlying captures.
                x, y = round(region["x"]), round(region["y"])
                right, bottom = round(region["x"] + region["width"]), round(region["y"] + region["height"])
                excess = max(-x, -y, right - picture.width, bottom - picture.height, 0)
                if excess > 2:
                    raise ValueError(f"Observed media region exceeds {row['file']} bounds by more than CSS rounding")
                actual_box = (max(0, x), max(0, y), min(picture.width, right), min(picture.height, bottom))
                row["qa_crop_pixels"] = list(actual_box)
                row["qa_crop_css_rounding_clamp_pixels"] = excess
                picture = picture.crop(actual_box)
            picture.thumbnail((tile_w - 8, image_h - 4), Image.Resampling.LANCZOS)
            col, r = index % columns, index // columns
            left, top = col * tile_w, header_h + r * (image_h + label_h)
            board.paste(picture, (left + (tile_w - picture.width) // 2, top + (image_h - picture.height) // 2))
            broad = " BROAD" if row["wide_capture_bracket"] else ""
            draw.text((left + 5, top + image_h + 2), f"{row['file']} c{row['cycle_before']}{broad}", fill="#191919", font=label_font)
            draw.text((left + 5, top + image_h + 20), f"{row['before_seconds']:.3f}-{row['after_seconds']:.3f}s", fill="#191919", font=label_font)
        name = f"playing_samples_board_{board_index + 1:02d}.jpg"
        board.save(qa / name, quality=94)
        names.append(name)

    touched_bins = sorted({min(bin_count - 1, int(row["representative_time_seconds"] / duration * bin_count)) for row in valid})
    output = {
        "source": meta.get("url") or (raw.get("post") if isinstance(raw, dict) else None),
        "duration_seconds": duration,
        "source_metadata_file": str(metadata_path.relative_to(folder.parent)),
        "capture_screenshot_mode": screenshot_mode,
        "framing_limit": f"{screenshot_mode}; only the actually visible portion, no uncropped whole-frame/whole-video claim" if partial_viewport else None,
        "originals_modified": False,
        "original_wrap_field_used": False,
        "cycle_inference": "before/after media time decreases, including intra-capture crossings; epsilon 0.015s",
        "sample_count": len(records),
        "valid_playing_non_crossing_samples": len(valid),
        "wide_capture_bracket_samples": sum(row["wide_capture_bracket"] for row in valid),
        "inferred_cycle_span": [min(row["cycle_before"] for row in records if "cycle_before" in row), max(row["cycle_after"] for row in records if "cycle_after" in row)],
        "observed_media_time_range_valid_samples": [min(row["before_seconds"] for row in valid), max(row["after_seconds"] for row in valid)],
        "sampling_time_bin_count": bin_count,
        "sampling_time_bins_with_valid_midpoint": touched_bins,
        "observed_region_metadata_key": region_key,
        "observed_region": region,
        "boards": names,
        "representatives": selected,
        "corrected_samples": records,
        "limits": [
            "Samples across playback loops do not establish continuous normal-speed whole-video review.",
            "Crossing capture brackets are uncertain and excluded from representative boards.",
            "Representative screenshots do not establish exact cut times or unheard audio rhythm.",
            "Brackets longer than 0.35s are marked BROAD; midpoint is a layout aid, not the actual captured frame time.",
            "Displayed likes and user selection do not establish view count or editing-related exposure causality.",
        ],
    }
    (qa / "corrected_coverage.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"folder": str(folder), "samples": len(records), "valid": len(valid), "bins_touched": len(touched_bins), "cycles": output["inferred_cycle_span"], "boards": names, "roi": region}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--study-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()
    folders = [args.study_dir / name for name in args.only] if args.only else sorted(args.study_dir.iterdir())
    for folder in folders:
        if folder.is_dir() and metadata_path_for(folder) and (folder / "samples.json").exists():
            raw = load_json(folder / "samples.json")
            samples = raw.get("samples", []) if isinstance(raw, dict) else raw
            if samples:
                print(json.dumps(make_boards(folder), ensure_ascii=False))
            else:
                print(json.dumps({"folder": str(folder), "skipped": "no screenshot samples"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
