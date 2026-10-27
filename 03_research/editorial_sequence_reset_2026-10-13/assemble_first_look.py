from pathlib import Path
import sys,json,hashlib,subprocess
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
a=OUT/'A1_motion_attempt_01/source.mp4';b=OUT/'A2_motion_attempt_01/source.mp4'
for p in [a,b]:assert sha(p)==json.loads((p.parent/'technical_receipt.json').read_text(encoding='utf-8'))['sha256']
an=int(sys.argv[1]);bn=int(sys.argv[2]);n=an+bn-18;offset=(an-18)/24
dest=OUT/'first_look_review_v1';dest.mkdir(exist_ok=True)
video=dest/'M03_L01_walk_to_seated_trial_v1.mp4';assert not video.exists(),'Never overwrite a prior export.'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
filters=(f'[0:v]trim=end_frame={an},settb=1/24,setpts=N,format=yuv420p,fps=24[a];'
 f'[1:v]trim=end_frame={bn},settb=1/24,setpts=N,format=yuv420p,fps=24[b];'
 f'[a][b]xfade=transition=fade:duration=0.75:offset={offset},format=yuv420p[v]')
r=subprocess.run([ffmpeg,'-hide_banner','-i',str(a),'-i',str(b),'-filter_complex',filters,'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','24','-frames:v',str(n),'-movflags','+faststart',str(video)],capture_output=True,text=True,encoding='utf-8',errors='replace')
(dest/'render_log.txt').write_text(r.stderr,encoding='utf-8');r.check_returncode()
result=scan(video);assert result['decoded_frames']==n
probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(video)],capture_output=True,text=True,encoding='utf-8',errors='replace');assert 'Audio:' not in probe.stderr
qa=dest/'join_qa';qa.mkdir(exist_ok=True)
indices=list(range(an-20,an+3));cols=6;rows=(len(indices)+5)//6
board=Image.new('RGB',(1200,380*rows),'white');draw=ImageDraw.Draw(board)
reader=imageio_ffmpeg.read_frames(str(video));next(reader)
for i,data in enumerate(reader):
 if i in indices:
  f=Image.frombytes('RGB',(720,1280),data);k=indices.index(i);x=k%cols*200;y=k//cols*380
  draw.text((x+3,y+3),f'{i/24:.3f}s f{i}',fill='black');board.paste(f.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
  if i in [an-20,an-18,an-9,an-1,an,an+2]:f.save(qa/f'join_{i:03d}.png')
board.save(qa/'join_all.jpg',quality=95)
delivery=json.loads((ROOT/'10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8-sig'));unchanged=[]
for r in delivery['reels']:
 actual=sha(ROOT/r['source_path']);assert actual==r['sha256'];unchanged.append({'model':r['model'],'sha256':actual,'unchanged':True})
save(OUT/'first_look_edit_receipt.json',{'status':'exported_frame_review_pending','file':video.relative_to(ROOT).as_posix(),'sha256':sha(video),'scan':result,'scope':'First-look same-outfit two-shot technical/editorial sub-sequence only, not formal one-model/two-look Reel delivery.','sources':[{'shot':'A1','file':a.relative_to(ROOT).as_posix(),'sha256':sha(a),'frames':[0,an],'end_exclusive':True},{'shot':'A2','file':b.relative_to(ROOT).as_posix(),'sha256':sha(b),'frames':[0,bn],'end_exclusive':True}],'transition':{'seconds':0.75,'frames':18,'start_seconds':offset,'end_seconds':an/24,'type':'cross_dissolve'},'editing':'Original24fps source speed, tail trim only, no text/audio/crop/zoom/freeze/speed effects.','user_film_approval':None,'assistant_continuous_playback':False,'protected_w41_delivery':unchanged,'drive_uploaded':False,'second_look_generated':False})
print(json.dumps({'frames':n,'seconds':n/24,'join_start':offset,'protected_originals':len(unchanged)}))
