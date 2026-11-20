"""Decode original, preserve native-speed silent copy, make review samples."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;ROOT=P.parents[6]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def run(args):return subprocess.run(list(map(str,args)),capture_output=True,check=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):(P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
source=P/'source.mp4';silent=P/'M03_W45_expressive_trial01_silent_review.mp4'
probe=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',source]).stdout)
put('source_probe.json',probe)
v=next(x for x in probe['streams'] if x['codec_type']=='video' and not x.get('disposition',{}).get('attached_pic'))
assert (v['width'],v['height'],v['nb_frames'],v['avg_frame_rate'])==(720,1280,'145','24/1')
decode=run([FF,'-v','error','-i',source,'-map','0:v:0','-f','null','-'])
run([FF,'-v','error','-y','-i',source,'-map','0:v:0','-c:v','copy','-an','-map_metadata','-1','-movflags','+faststart',silent])
qa=P/'qa';qa.mkdir(exist_ok=True)
run([FF,'-v','error','-y','-i',source,'-map','0:v:0','-vf',"select=not(mod(n\\,6))",'-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',20)
files=sorted(qa.glob('frame_*.jpg'));assert len(files)==25
board=Image.new('RGB',(1440,2200),'#f5f3ec');d=ImageDraw.Draw(board)
for i,p in enumerate(files):
 x=(i%6)*240;y=(i//6)*440
 im=Image.open(p);im.thumbnail((234,416));board.paste(im,(x,y+24))
 d.text((x+3,y),f'f{i*6:03d} / {i*.25:.2f}s',font=font,fill='#253a45')
board.save(P/'whole_film_contact.jpg',quality=94)
arms=Image.new('RGB',(1500,1600),'#f5f3ec');d=ImageDraw.Draw(arms)
for j,k in enumerate(range(1,17)):
 im=Image.open(files[k]).crop((150,0,620,800));im.thumbnail((285,365))
 x=(j%5)*300;y=(j//5)*400;arms.paste(im,(x,y+26));d.text((x+5,y),f'{k*.25:.2f}s',font=font,fill='#253a45')
arms.save(P/'upper_body_contact.jpg',quality=94)
panel=Image.new('RGB',(1440,1600),'#f5f3ec');d=ImageDraw.Draw(panel)
for j,k in enumerate([0,4,8,12,16,20]):
 im=Image.open(files[k]);im.thumbnail((240,427));x=j*240
 panel.paste(im,(x,30));d.text((x+5,0),f'{k*.25:.2f}s',font=font,fill='#253a45')
 # Fixed candidate column, no tracking or retiming; keep full image in top row for diagnosis.
 im=Image.open(files[k]).crop((181,0,537,1280));im.thumbnail((240,864));panel.paste(im,(x,515))
 d.text((x+4,1385),'固定雙欄窗口',font=font,fill='#253a45')
panel.save(P/'panel_fit_contact.jpg',quality=94)
integrity=json.loads((P/'prompt_integrity.json').read_text(encoding='utf-8-sig'))
integrity['media']=[x for x in integrity['media'] if 'a9d31a19-5434-4f47-8682-f8963b6f1d86' in x.get('src','') and x['rect']['height']>200]
put('prompt_integrity.json',integrity)
put('technical_review.json',{'full_decode_exit_code':0,'width':720,'height':1280,'fps':24,'frame_count':145,'duration_seconds':145/24,'source_audio':'AAC','silent_copy_video_stream_copy':True,'source_sha256':h(source),'silent_sha256':h(silent),'whole_film_sample_count':25,'visual_approval':None,'continuous_human_review':False})
print(json.dumps({'source_sha256':h(source),'silent_sha256':h(silent),'frames':145,'seconds':145/24,'full_decode':True,'samples':25}))
