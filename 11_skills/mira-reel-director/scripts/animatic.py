"""Play storyboard stills at their planned durations in a silent 9:16 MP4."""
import argparse
import json
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def positive_integer(value, label):
    if type(value) is not int or value < 1:
        raise ValueError(f"{label} must be a positive integer")
    return value


def render(board, output, ffmpeg):
    data = json.loads(board.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("board must be an object")
    fps = positive_integer(data.get("fps"), "fps")
    panels = data.get("panels")
    if not isinstance(panels, list) or not panels:
        raise ValueError("provide at least one storyboard panel")
    if output.suffix.lower() != ".mp4" or output.exists():
        raise ValueError("choose a new .mp4 output path")

    inputs, filters, labels = [], [], []
    total = 0
    for index, panel in enumerate(panels):
        if not isinstance(panel, dict) or not isinstance(panel.get("image"), str):
            raise ValueError(f"panel {index + 1} needs an image path")
        frames = positive_integer(panel.get("frames"), f"panel {index + 1} frames")
        path = board.parent / panel["image"]
        if not path.is_file():
            raise ValueError(f"missing storyboard image: {path}")
        inputs.extend(["-loop", "1", "-framerate", str(fps), "-i", str(path)])
        filters.append(
            f"[{index}:v]trim=end_frame={frames},setpts=PTS-STARTPTS,"
            "scale=360:640:force_original_aspect_ratio=decrease:force_divisible_by=2,"
            f"pad=360:640:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[p{index}]"
        )
        labels.append(f"[p{index}]")
        total += frames
    filters.append("".join(labels) + f"concat=n={len(panels)}:v=1:a=0,setpts=N/({fps}*TB)[v]")
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as scratch:
        result = Path(scratch) / "preview.mp4"
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", *inputs,
                        "-filter_complex", ";".join(filters), "-map", "[v]", "-an",
                        "-r", str(fps), "-c:v", "libx264", "-movflags", "+faststart",
                        str(result)], check=True)
        # Publish exclusively, including when two renders target the same name.
        if os.name == "nt":
            result.rename(output)  # Windows rename refuses an existing destination.
        else:
            os.link(result, output)
    return total, fps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("board", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()
    try:
        frames, fps = render(args.board, args.output, args.ffmpeg)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{args.output} ({frames} planned frames at {fps} fps)")


if __name__ == "__main__":
    main()
