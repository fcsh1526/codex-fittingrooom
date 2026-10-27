"""Decode every source frame and record technical signals, never visual approval."""
import json
import sys
from pathlib import Path
import numpy as np

root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(root / '10_automation' / '.video_dependencies'))
import imageio_ffmpeg

source = root / '10_automation/runs/2026-W37/reels/videos/M04_A_L01_upload_trial_01.mp4'
reader = imageio_ffmpeg.read_frames(str(source))
meta = next(reader)
width, height = meta['size']
count = 0
black = []
still_pairs = []
previous = None
for frame in reader:
    pixels = np.frombuffer(frame, dtype=np.uint8).reshape(height, width, 3)
    small = pixels[::8, ::8].astype(np.float32)
    if (small < 16).all(axis=2).mean() > .98:
        black.append(count)
    if previous is not None and np.abs(small - previous).mean() < .1:
        still_pairs.append([count - 1, count])
    previous = small
    count += 1
result = dict(source=str(source), metadata=meta, decoded_frames=count,
              decoded_seconds=count/meta['fps'], black_candidate_frames=black,
              near_identical_frame_pairs=still_pairs,
              note='Technical signals only. Identity, wardrobe, background, pacing and continuous playback require visual review.')
Path(__file__).with_name('M04_A_L01_upload_trial_01').joinpath('decode_scan.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
