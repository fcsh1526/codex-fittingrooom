from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;ROOT=P.parents[5];FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def run(args):
 r=subprocess.run([str(x) for x in args],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-4000:])
 return r.stdout
src=P/'S01_source.mp4';silent=P/'M04_W45_full_source_silent.mp4'
probe=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',src]));v=next(x for x in probe['streams'] if x['codec_type']=='video')
assert (v['width'],v['height'])==(720,1280) and v['avg_frame_rate']=='24/1'
run([FF,'-v','error','-i',src,'-map','0:v:0','-f','null','-'])
run([FF,'-v','error','-y','-i',src,'-map','0:v:0','-c:v','copy','-an','-map_metadata','-1','-movflags','+faststart',silent])
qa=P/'qa';qa.mkdir(exist_ok=True)
run([FF,'-v','error','-y','-i',src,'-vf','select=not(mod(n\\,3))','-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
files=sorted(qa.glob('frame_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
for name,stride,box,cell in [('whole_contact',4,None,(210,398)),('face_contact',2,(215,65,435,330),(200,290)),('floral_contact',4,(180,220,535,620),(240,310)),('feet_contact',2,(200,900,530,1260),(200,250))]:
 selected=list(range(0,len(files),stride));cols=7;cw,ch=cell;im=Image.new('RGB',(cols*cw,((len(selected)+cols-1)//cols)*ch),'#f5f3ec');d=ImageDraw.Draw(im)
 for j,k in enumerate(selected):
  f=Image.open(files[k]);f=f.crop(box) if box else f;f.thumbnail((cw-4,ch-28));x=j%cols*cw;y=j//cols*ch;im.paste(f,(x,y+25));d.text((x+2,y),f'{k*.125:.3f}s',font=font,fill='#233b46')
 im.save(P/(name+'.jpg'),quality=96)
tech={'width':v['width'],'height':v['height'],'fps':24,'frame_count':int(v['nb_frames']),'seconds':float(v['duration']),'source_has_audio':any(x['codec_type']=='audio' for x in probe['streams']),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'silent_sha256':hashlib.sha256(silent.read_bytes()).hexdigest(),'full_decode':True,'silent_video_stream_copy':True,'native_speed':True,'sample_every_frames':3,'sample_count':len(files),'continuous_native_speed_review':False,'user_film_approval':None,'publication_approval':None}
(P/'technical_review.json').write_text(json.dumps(tech,indent=2),encoding='utf-8');(P/'source_probe.json').write_text(json.dumps(probe,indent=2),encoding='utf-8');print(json.dumps(tech))
