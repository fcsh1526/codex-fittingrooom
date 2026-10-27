from pathlib import Path
import sys,json,hashlib,subprocess
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
a=ROOT/'10_automation/runs/2026-W41/reels/M02/A_attempt_01/source.mp4'
b=OUT/'L01_motion_attempt_01/source.mp4'
assert sha(a)=='571c5ddc0ef77f47d21efabc385fdac0c405680dde8ad511c449ced50c36b437'
assert sha(b)=='ed6acbd36c3c33fa3aae4d0e8146cff93e45f264b995ffb66142a4dca7225e24'
an=60;bn=108;n=an+bn-18;offset=(an-18)/24
dest=OUT/'first_look_review_v1';dest.mkdir(exist_ok=True)
video=dest/'M02_L01_cafe_pause_trial_v1.mp4';assert not video.exists()
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
filters=(f'[0:v]trim=end_frame={an},settb=1/24,setpts=N,format=yuv420p,fps=24[a];'
 f'[1:v]trim=end_frame={bn},settb=1/24,setpts=N,format=yuv420p,fps=24[b];'
 f'[a][b]xfade=transition=fade:duration=0.75:offset={offset},format=yuv420p[v]')
r=subprocess.run([ffmpeg,'-hide_banner','-i',str(a),'-i',str(b),'-filter_complex',filters,'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','24','-frames:v',str(n),'-movflags','+faststart',str(video)],capture_output=True,text=True,encoding='utf-8',errors='replace')
(dest/'render_log.txt').write_text(r.stderr,encoding='utf-8');r.check_returncode()
result=scan(video);assert result['decoded_frames']==n
probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(video)],capture_output=True,text=True,encoding='utf-8',errors='replace');assert 'Audio:' not in probe.stderr
qa=dest/'join_qa';qa.mkdir(exist_ok=True)
indices=list(range(an-20,an+3));board=Image.new('RGB',(1200,1520),'white');draw=ImageDraw.Draw(board)
reader=imageio_ffmpeg.read_frames(str(video));next(reader)
for i,data in enumerate(reader):
 if i in indices:
  f=Image.frombytes('RGB',(720,1280),data);k=indices.index(i);x=k%6*200;y=k//6*380
  draw.text((x+3,y+3),f'{i/24:.3f}s f{i}',fill='black');board.paste(f.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
  if i in [40,42,51,59,60,62]:f.save(qa/f'join_{i:03d}.png')
board.save(qa/'join_all.jpg',quality=95)
delivery=json.loads((ROOT/'10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8-sig'));unchanged=[]
for row in delivery['reels']:
 actual=sha(ROOT/row['source_path']);assert actual==row['sha256'];unchanged.append({'model':row['model'],'sha256':actual,'unchanged':True})
save(OUT/'first_look_edit_receipt.json',{'status':'exported_visual_review_pending','file':video.relative_to(ROOT).as_posix(),'sha256':sha(video),'scan':result,'scope':'Same-outfit L01 two-shot sub-sequence, not complete one-model/two-look delivery.','sources':[{'shot':'S1','file':a.relative_to(ROOT).as_posix(),'sha256':sha(a),'frames_end_exclusive':[0,an]},{'shot':'S2','file':b.relative_to(ROOT).as_posix(),'sha256':sha(b),'frames_end_exclusive':[0,bn]}],'transition':{'seconds':0.75,'frames':18,'start_seconds':offset,'end_seconds':an/24,'type':'cross_dissolve'},'timing_reason':'4.5 seated seconds retain the attention change and near-frontal return; supersedes provisional3.75s proof budget for this sub-sequence only.','editing':'Original24fps source speed, trims only, no text/audio/crop/zoom/freeze/speed effects.','user_film_approval':None,'assistant_continuous_playback':False,'protected_w41_delivery':unchanged,'drive_uploaded':False})
print(json.dumps({'frames':n,'seconds':n/24,'join_start':offset,'protected_originals':len(unchanged)}))
