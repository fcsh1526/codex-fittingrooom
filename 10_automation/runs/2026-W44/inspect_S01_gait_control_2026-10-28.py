from pathlib import Path
import sys,json,hashlib,subprocess
from PIL import Image,ImageDraw
r=Path.cwd();sys.path.insert(0,str(r/'10_automation/.video_dependencies'))
import imageio_ffmpeg
base=r/'10_automation/runs/2026-W44/editorial_reset_v3_2026-10-28';out=base/'S01_gait_control_01';q=out/'QA';q.mkdir(exist_ok=True)
source=out/'gait_control_source.mp4';old=base/'S01_motion_trial_01/S01_source.mp4'
def read(p):
 g=imageio_ffmpeg.read_frames(str(p),pix_fmt='rgb24');m=next(g);assert m['fps']==24 and m['size']==(720,1280),m
 frames=[Image.frombytes('RGB',(720,1280),raw) for raw in g];g.close();return m,frames
m,new=read(source);om,previous=read(old)
def board(ids,name,crop=None,cols=6):
 w=240 if crop else 180;h=round(w*((crop[3]-crop[1])/(crop[2]-crop[0]) if crop else 1280/720));rh=h+24
 im=Image.new('RGB',(cols*w,((len(ids)+cols-1)//cols)*rh),'#eeeeea');d=ImageDraw.Draw(im)
 for k,i in enumerate(ids):
  x=k%cols*w;y=k//cols*rh;f=new[i].crop(crop) if crop else new[i];im.paste(f.resize((w,h)),(x,y+24));d.text((x+4,y+5),f'f{i:03} / {i/24:.3f}s',fill='black')
 im.save(q/name,quality=94)
ids=sorted(set([0,12,24,36,48,60,72,84,96,108,120,132,len(new)-1]));board(ids,'whole_control.jpg',cols=5)
for a in [0,48,96]:board(list(range(a,min(a+48,len(new)),2)),f'feet_{a:03}.jpg',(0,720,720,1280))
ff=imageio_ffmpeg.get_ffmpeg_exe();silent=out/'gait_control_silent_review.mp4'
if not silent.exists():subprocess.run([ff,'-hide_banner','-loglevel','error','-n','-i',str(source),'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',str(silent)],check=True)
compare=out/'original_left_control_right_6s.mp4';count=min(144,len(new),len(previous))
if not compare.exists():
 g=imageio_ffmpeg.write_frames(str(compare),(720,640),fps=24,codec='libx264',pix_fmt_in='rgb24',pix_fmt_out='yuv420p',output_params=['-crf','18','-movflags','+faststart']);g.send(None)
 for i in range(count):
  im=Image.new('RGB',(720,640));im.paste(previous[i].resize((360,640)),(0,0));im.paste(new[i].resize((360,640)),(360,0));g.send(im.tobytes())
 g.close()
probe=subprocess.run([ff,'-hide_banner','-i',str(source)],capture_output=True,text=True,encoding='utf-8',errors='replace');(q/'probe.txt').write_text(probe.stderr,encoding='utf-8')
record={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'bytes':source.stat().st_size,'metadata':m,'decoded_frames':len(new),'seconds_from_count':len(new)/24,'source_full_decode':True,'silent_preview':'gait_control_silent_review.mp4','comparison':{'file':compare.name,'left':'rejected original S01 first6s','right':'new straight-camera gait control first6s','frame_count':count,'fps':24,'duration':count/24,'all_native_speed':True,'full_rasters_resized_equally_no_crop':True},'QA':'Whole control every0.5s plus0–6s feet every2frames; manual continuous playback remains unverified'}
(q/'technical_scan.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(record,ensure_ascii=False))
