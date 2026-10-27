"""Consecutive lower-body inspection windows; delivered media remains untouched."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('source')
parser.add_argument('output')
args = parser.parse_args()
source, output = (ROOT / args.source).resolve(), (ROOT / args.output).resolve()
week = ROOT / '10_automation/runs/2026-W41'
if not source.is_relative_to(week) or not output.is_relative_to(week) or output.exists():
    raise ValueError('Require a source and new inspection folder inside W41.')
spec = importlib.util.spec_from_file_location('native_pair', ROOT / '03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
scan = native.full_decode(source)
count = scan['decoded_frames']
output.mkdir(parents=True)
roi = (160, 775, 560, 1280)
width, height = roi[2] - roi[0], roi[3] - roi[1]
entries = []
for index, frame in enumerate(native.selected_frames(source, 0, count)):
    local = index % 36
    if local == 0:
        page = Image.new('RGB', (6 * (width + 8), 6 * (height + 24)), (245, 244, 240))
        draw = ImageDraw.Draw(page)
    x, y = (local % 6) * (width + 8), (local // 6) * (height + 24)
    page.paste(frame.crop(roi), (x, y + 20))
    draw.text((x + 3, y + 3), f'f{index} / {index / 24:.3f}s', fill='black')
    if local == 35 or index == count - 1:
        name = f'lower_body_{index // 36:02d}.jpg'
        page.save(output / name, quality=95)
        entries.append(dict(file=name, first_frame=index-local, last_frame=index))
receipt = dict(source=source.relative_to(ROOT).as_posix(), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
               native_roi=roi, inspection_only=True, delivered_video_transform='none', fps=24, frames=count,
               boards=entries, lower_body_visual_result='pending', continuous_playback_review=False)
(output / 'lower_body_inspection.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt))
