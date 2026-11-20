"""Decode and extract source samples without retiming or claiming human acceptance."""
import json,sys,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[5];P=BASE/sys.argv[1]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def run(args):
 r=subprocess.run([str(a) for a in args],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-3000:])
 return r.stdout
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):(P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
src=P/'source.mp4';silent=P/('M03_W45_natural_'+sys.argv[1]+'_silent_review.mp4')
pr=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',src]));put('source_probe.json',pr)
v=next(s for s in pr['streams'] if s['codec_type']=='video');assert v['width']==720 and v['height']==1280 and v['avg_frame_rate']=='24/1';assert 5.9<float(v['duration'])<6.2
run([FF,'-v','error','-i',src,'-map','0:v:0','-f','null','-'])
run([FF,'-v','error','-y','-i',src,'-map','0:v:0','-c:v','copy','-an','-map_metadata','-1','-movflags','+faststart',silent])
qa=P/'qa';qa.mkdir(exist_ok=True)
run([FF,'-v','error','-y','-i',src,'-vf','select=not(mod(n\\,3))','-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
files=sorted(qa.glob('frame_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
for name,selected,crop,cell in [('whole_film_contact',list(range(0,len(files),4)),None,(210,398)),('upper_body_contact',list(range(0,len(files),2)),(130,110,650,720),(250,330)),('panel_fit_contact',list(range(0,len(files),2)),(135,0,585,1280),(150,455))]:
 cols=7;cw,ch=cell;rows=(len(selected)+cols-1)//cols;im=Image.new('RGB',(cols*cw,rows*ch),'#f5f3ec');d=ImageDraw.Draw(im)
 for j,k in enumerate(selected):
  f=Image.open(files[k]);f=f.crop(crop) if crop else f;f.thumbnail((cw-4,ch-28));x=j%cols*cw;y=j//cols*ch;im.paste(f,(x,y+25));d.text((x+2,y),f'{k*.125:.3f}s',font=font,fill='#233b46')
 im.save(P/(name+'.jpg'),quality=95)
tech={'width':720,'height':1280,'fps':24,'frame_count':int(v['nb_frames']),'seconds':float(v['duration']),'source_has_audio':any(s['codec_type']=='audio' for s in pr['streams']),'source_sha256':h(src),'silent_path':str(silent.relative_to(ROOT)).replace('\\','/'),'silent_sha256':h(silent),'full_decode':True,'native_speed':True,'silent_video_stream_copy':True,'new_frames_generated':False,'extracted_every_frames':3,'whole_film_board_samples':len(range(0,len(files),4)),'upper_board_samples':len(range(0,len(files),2)),'panel_fit_board_samples':len(range(0,len(files),2)),'uninterrupted_human_review':False,'user_film_acceptance':None}
put('technical_review.json',tech)
sub=json.loads((P/'submission.json').read_text(encoding='utf-8'));sub.update(status='downloaded_pending_visual_review',**tech);put('submission.json',sub)
print(json.dumps(tech))
