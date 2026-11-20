from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;B=P.parent;ROOT=B.parents[5]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
L=B/'L01_trial_01/source.mp4';R=B/'L02_trial_01/source.mp4';O=P/'M03_W45_reference_parallel_review_v2.mp4'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):
 r=subprocess.run([str(x) for x in args],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-3000:])
 return r.stdout
assert h(L)=='eea1bdfbc5add114ee8e8e4f9a363bf9544d8976660f8b7316707807e8e62f1c'
assert h(R)=='85252ae95333fbc4062b39759be7eb882a282d3e1f89b34f8d2fd5a467c72186'
f='[0:v]trim=start_frame=0:end_frame=192,setpts=PTS-STARTPTS,crop=400:1280:160:0,scale=356:1140[left];[1:v]trim=start_frame=24:end_frame=216,setpts=PTS-STARTPTS,crop=400:1280:160:0,scale=356:1140[right];color=c=0xf5f3ec:s=720x1280:r=24:d=8[base];[base][left]overlay=0:70:shortest=1[tmp];[tmp][right]overlay=364:70:shortest=1[v]'
run([FF,'-v','error','-y','-i',L,'-i',R,'-filter_complex',f,'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-frames:v','192','-movflags','+faststart',O])
probe=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',O]));video=next(x for x in probe['streams'] if x['codec_type']=='video');assert video['nb_frames']=='192' and video['avg_frame_rate']=='24/1'
run([FF,'-v','error','-i',O,'-f','null','-'])
qa=P/'qa';qa.mkdir(exist_ok=True);run([FF,'-v','error','-y','-i',O,'-vf','select=not(mod(n\\,6))','-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
files=sorted(qa.glob('frame_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
im=Image.new('RGB',(1800,((len(files)+5)//6)*365),'#f5f3ec');d=ImageDraw.Draw(im)
for i,path in enumerate(files):
 pic=Image.open(path);pic.thumbnail((290,330));x=i%6*300;y=i//6*365;im.paste(pic,(x,y+25));d.text((x+2,y),f'{i*.25:.2f}s',font=font,fill='#123')
im.save(P/'contact.jpg',quality=94)
data={'date':'2026-11-05','status':'sampled_candidate_native_speed_review_pending','film_sha256':h(O),'source_left_sha256':h(L),'source_right_sha256':h(R),'source_intervals_frames':{'left':[0,192],'right':[24,216]},'fps':24,'frame_count':192,'duration_seconds':8,'crop_each_xywh':[160,0,400,1280],'panel_xywh':[[0,70,356,1140],[364,70,356,1140]],'native_speed':True,'audio':False,'baked_text':False,'internal_joins':[],'no_retime_freeze_repeat_or_motion_interpolation':True,'full_decode':True,'continuous_human_native_speed_review':False,'user_film_acceptance':None,'publication_approval':None,'source_jobs_added':0}
(P/'edit_receipt.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(data))
