"""Inspection-only sheets of every combined frame for both panel bounds."""
import importlib.util, json
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('native', ROOT/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
work=ROOT/'10_automation/runs/2026-W41/reels/M04/review_v1'
video=work/'2026-W41_M04_two_looks_parallel_v1.mp4'
scan=n.full_decode(video);count=scan['decoded_frames'];out=work/'bounds_QA';out.mkdir()
files=[]
for i,frame in enumerate(n.selected_frames(video,0,count)):
    slot=i%24
    if slot==0:
        page=Image.new('RGB',(6*248,4*360),'#f5f3ef');draw=ImageDraw.Draw(page)
    x=(slot%6)*248;y=(slot//6)*360
    draw.text((x+3,y+3),f'f{i} / {i/24:.3f}s',fill='black')
    frame=frame.crop((0,145,720,1130)).resize((240,328),Image.Resampling.LANCZOS)
    page.paste(frame,(x+4,y+22))
    if slot==23 or i==count-1:
        path=out/f'parallel_bounds_{i//24:02d}.jpg';n.image_new(path,page);files.append(path.name)
n.json_new(out/'inspection.json',dict(frames=count,files=files,inspection_only=True,all_frame_bound_visual_review='pending',continuous_playback_review=False))
print(json.dumps({'frames':count,'files':files}))
