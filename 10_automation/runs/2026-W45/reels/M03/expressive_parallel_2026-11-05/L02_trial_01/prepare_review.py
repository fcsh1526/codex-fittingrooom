"""Create native-speed silent review and honest visual samples for skirt trial01."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;ROOT=P.parents[6]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def run(args):return subprocess.run(list(map(str,args)),capture_output=True,check=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):(P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
src=P/'source.mp4';silent=P/'M03_W45_skirt_expressive_trial01_silent_review.mp4'
pr=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',src]).stdout);put('source_probe.json',pr)
v=next(x for x in pr['streams'] if x['codec_type']=='video' and not x.get('disposition',{}).get('attached_pic'))
assert v['width']==720 and v['height']==1280 and v['avg_frame_rate']=='24/1'
assert 9.9<float(v['duration'])<10.2
run([FF,'-v','error','-i',src,'-map','0:v:0','-f','null','-'])
run([FF,'-v','error','-y','-i',src,'-map','0:v:0','-c:v','copy','-an','-map_metadata','-1','-movflags','+faststart',silent])
qa=P/'qa';qa.mkdir(exist_ok=True)
run([FF,'-v','error','-y','-i',src,'-map','0:v:0','-vf',"select=not(mod(n\\,6))",'-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
files=sorted(qa.glob('frame_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
selected=list(range(0,len(files),2));cols=7;rows=(len(selected)+cols-1)//cols
im=Image.new('RGB',(cols*210,rows*398),'#f5f3ec');d=ImageDraw.Draw(im)
for j,k in enumerate(selected):
 x=j%cols*210;y=j//cols*398;f=Image.open(files[k]);f.thumbnail((206,366));im.paste(f,(x,y+26));d.text((x+2,y),f'{k*.25:.2f}s',font=font,fill='#243b45')
im.save(P/'whole_film_contact.jpg',quality=94)
selected=[k for k in range(len(files)) if 1.5<=k*.25<=7.0]
im=Image.new('RGB',(1500,((len(selected)+5)//6)*395),'#f5f3ec');d=ImageDraw.Draw(im)
for j,k in enumerate(selected):
 x=j%6*250;y=j//6*395;f=Image.open(files[k]).crop((130,0,650,800));f.thumbnail((240,365));im.paste(f,(x,y+25));d.text((x+3,y),f'{k*.25:.2f}s',font=font,fill='#243b45')
im.save(P/'upper_body_contact.jpg',quality=94)
tech={'full_decode_exit_code':0,'width':v['width'],'height':v['height'],'fps':24,'frame_count':int(v['nb_frames']),'duration_seconds':float(v['duration']),'source_has_audio':any(x['codec_type']=='audio' for x in pr['streams']),'source_sha256':h(src),'silent_sha256':h(silent),'silent_video_stream_copy':True,'retimed':False,'whole_film_samples':len(range(0,len(files),2)),'upper_body_samples':len(selected),'continuous_human_review':False,'user_acceptance':None}
put('technical_review.json',tech);print(json.dumps(tech))
