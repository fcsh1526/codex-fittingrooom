"""Consecutive hand-cloth inspection crops only; never change delivered video."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');a=p.parse_args()
source=(root/a.source).resolve();out=(root/a.output).resolve()
if not source.is_relative_to(root/'10_automation/runs/2026-W41') or not out.is_relative_to(root/'10_automation/runs/2026-W41') or out.exists():raise ValueError('Require new W41 inspection folder.')
spec=importlib.util.spec_from_file_location('native_pair',root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
decoded=mod.full_decode(source);count=decoded['decoded_frames']
out.mkdir(parents=True)
roi=(224,385,472,680); w=roi[2]-roi[0];h=roi[3]-roi[1]
entries=[]
frames=mod.selected_frames(source,0,count)
page=None
for index,frame in enumerate(frames):
    local=index%36
    if local==0:
        page=Image.new('RGB',(6*(w+8),6*(h+24)),(245,244,240));draw=ImageDraw.Draw(page)
    x=(local%6)*(w+8);y=(local//6)*(h+24)
    page.paste(frame.crop(roi),(x,y+20));draw.text((x+3,y+3),f'f{index} / {index/24:.3f}s',fill='black')
    if local==35 or index==count-1:
        name=f'contact_{index//36:02d}.jpg';page.save(out/name,quality=95)
        entries.append(dict(file=name,first_frame=index-local,last_frame=index))
record=dict(source=source.relative_to(root).as_posix(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),native_roi=roi,inspection_only=True,delivered_video_transform='none',fps=24,frames=count,boards=entries,contact_visual_result='pending',continuous_playback_review=False)
(out/'contact_inspection.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
