"""Make a clean two-shot review cut from selected intervals; no QA status implied."""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / '.video_dependencies'))
import imageio_ffmpeg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('first', type=Path)
    parser.add_argument('second', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--first-start', type=float, required=True)
    parser.add_argument('--first-duration', type=float, required=True)
    parser.add_argument('--second-start', type=float, required=True)
    parser.add_argument('--second-duration', type=float, required=True)
    args = parser.parse_args()
    if min(args.first_start, args.second_start) < 0 or min(args.first_duration, args.second_duration) <= 0:
        parser.error('Starts must be nonnegative and durations must be positive.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    filter_graph = (
        f'[0:v]trim=start={args.first_start}:duration={args.first_duration},setpts=PTS-STARTPTS,'
        'fps=24,format=yuv420p[v0];'
        f'[1:v]trim=start={args.second_start}:duration={args.second_duration},setpts=PTS-STARTPTS,'
        'fps=24,format=yuv420p[v1];'
        '[v0][v1]concat=n=2:v=1:a=0[out]'
    )
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(args.first), '-i', str(args.second),
        '-filter_complex', filter_graph, '-map', '[out]',
        '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart',
        '-an', str(args.output),
    ], check=True)
    print(args.output)


if __name__ == '__main__':
    main()
