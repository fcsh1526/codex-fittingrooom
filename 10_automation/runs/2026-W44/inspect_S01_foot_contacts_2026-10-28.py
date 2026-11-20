from pathlib import Path
import sys,json,hashlib
from PIL import Image,ImageDraw
r=Path.cwd();sys.path.insert(0,str(r/'10_automation/.video_dependencies'))
import imageio_ffmpeg
b=r/'10_automation/runs/2026-W44/editorial_reset_v3_2026-10-28/S01_motion_trial_01'
p=b/'S01_source.mp4';assert hashlib.sha256(p.read_bytes()).hexdigest()=='6b249dd3eece25149324d4003a56ef961cb18d480ba18a7f668aa0f54b72c446'
q=b/'foot_contact_diagnosis';q.mkdir(exist_ok=True)
g=imageio_ffmpeg.read_frames(str(p),pix_fmt='rgb24');m=next(g);frames=[Image.frombytes('RGB',tuple(m['size']),raw) for raw in g];g.close()
for start,end in [(0,48),(48,96),(96,144)]:
 ids=list(range(start,end,2));im=Image.new('RGB',(1440,4*210),'#eeeeea');d=ImageDraw.Draw(im)
 for k,i in enumerate(ids):
  crop=frames[i].crop((0,720,720,1280)).resize((240,187));x=k%6*240;y=k//6*210
  im.paste(crop,(x,y+23));d.text((x+4,y+5),f'f{i:03} / {i/24:.3f}s',fill='black')
 im.save(q/f'feet_f{start:03}_f{end-2:03}.jpg',quality=95)
for i in [0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,132,136,140]:
 frames[i].save(q/f'f{i:03}.png')
record={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'crop':[0,720,720,1280],'sampling':'Every2frames for0–6s foot+ground contact sheets; every4frames full-resolution samples. Same crop for all frames; no alignment, stabilization, tracking or retiming.', 'limits':'Screen-coordinate drift includes camera motion; foot world-lock requires same-ground landmark comparison. No metric 3D foot sliding estimate or cause certified.'}
(q/'extraction_receipt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(q)
