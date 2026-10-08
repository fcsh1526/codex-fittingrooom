"""Record all-frame decode and technical signals; never grants visual approval."""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent / '.video_dependencies'))
import imageio_ffmpeg

def scan(source):
    reader = imageio_ffmpeg.read_frames(str(source))
    meta = next(reader)
    w, h = meta['size']
    black, still, n, previous = [], [], 0, None
    for frame in reader:
        pixels = np.frombuffer(frame,dtype=np.uint8).reshape(h,w,3)[::8,::8].astype(np.float32)
        if (pixels < 16).all(axis=2).mean() > .98:
            black.append(n)
        if previous is not None and np.abs(pixels-previous).mean() < .1:
            still.append([n-1,n])
        previous = pixels
        n += 1
    return dict(source=str(source),metadata=meta,decoded_frames=n,decoded_seconds=n/meta['fps'],
                black_candidate_frames=black,near_identical_frame_pairs=still,
                note='Technical signals only. Continuous visual review and user approval remain separate.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    result = scan(args.source)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
