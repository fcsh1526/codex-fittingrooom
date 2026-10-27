"""Consecutive hand/cloth QA windows only; preserve delivered video pixels."""
import argparse, hashlib, importlib.util, json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
p.add_argument('source'); p.add_argument('output')
a = p.parse_args()
source, output = (ROOT/a.source).resolve(), (ROOT/a.output).resolve()
week = ROOT/'10_automation/runs/2026-W41'
if not source.is_relative_to(week) or not output.is_relative_to(week) or output.exists():
    raise ValueError('Require source and new QA directory within W41.')
spec = importlib.util.spec_from_file_location('native', ROOT/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
scan = native.full_decode(source)
count = scan['decoded_frames']; output.mkdir(parents=True)
roi = (180, 400, 580, 760)
width, height = roi[2]-roi[0], roi[3]-roi[1]
boards = []
for i, frame in enumerate(native.selected_frames(source, 0, count)):
    slot = i % 36
    if slot == 0:
        page = Image.new('RGB', (6*(width+8), 6*(height+24)), '#f5f3ef')
        draw = ImageDraw.Draw(page)
    x, y = (slot%6)*(width+8), (slot//6)*(height+24)
    page.paste(frame.crop(roi), (x,y+20))
    draw.text((x+3,y+3), f'f{i} / {i/24:.3f}s', fill='black')
    if slot == 35 or i == count-1:
        name = f'cuff_contact_{i//36:02d}.jpg'
        page.save(output/name, quality=95)
        boards.append(dict(file=name, first_frame=i-slot, last_frame=i))
receipt = dict(source=source.relative_to(ROOT).as_posix(), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), native_roi=roi, inspection_only=True, delivered_video_transform='none', fps=24, frames=count, boards=boards, hand_cloth_visual_result='pending', continuous_playback_review=False)
(output/'cuff_contact_inspection.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt))
