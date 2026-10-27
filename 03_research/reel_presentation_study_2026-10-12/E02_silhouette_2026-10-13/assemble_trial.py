from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
first=OUT/'B_attempt_02/source.mp4'
second=OUT/'A_attempt_01/source.mp4'
assert sha(first)=='e30b68bcfc3230a24a95fd79e8a72d0e911baf4c6d8d4ab0270e42fd9b57149f'
assert sha(second)=='eba18458169845f884bc6cea5e0cc9dd40bcf233df4dd385c33e5fdc0f344be1'
video=OUT/'review_v1/M05_E02_silhouette_two_looks_v1.mp4'
video.parent.mkdir(exist_ok=True)
assert not video.exists(),'Export a new version; never overwrite.'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
filters=('[0:v]trim=end_frame=96,settb=1/24,setpts=N,format=yuv420p,fps=24[a];'
         '[1:v]trim=end_frame=114,settb=1/24,setpts=N,format=yuv420p,fps=24[b];'
         '[a][b]xfade=transition=fade:duration=0.75:offset=3.25,format=yuv420p[v]')
cmd=[ffmpeg,'-hide_banner','-i',str(first),'-i',str(second),'-filter_complex',filters,'-map','[v]','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-r','24','-frames:v','192','-movflags','+faststart',str(video)]
r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
(video.parent/'render_log.txt').write_text(r.stderr,encoding='utf-8');r.check_returncode()
result=scan(video)
assert result['decoded_frames']==192 and result['metadata']['fps']==24
assert list(result['metadata']['size'])==[720,1280]
probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(video)],capture_output=True,text=True,encoding='utf-8',errors='replace')
assert 'Audio:' not in probe.stderr
qa=video.parent/'join_qa';qa.mkdir(exist_ok=True)
board=Image.new('RGB',(1400,1140),'white');d=ImageDraw.Draw(board)
indices=list(range(76,97))
reader=imageio_ffmpeg.read_frames(str(video));next(reader)
for i,data in enumerate(reader):
    if i in indices:
        frame=Image.frombytes('RGB',(720,1280),data);k=indices.index(i);x=k%7*200;y=k//7*380
        d.text((x+3,y+3),f'{i/24:.3f}s f{i}',fill='black');board.paste(frame.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
        if i in [76,78,84,87,90,95,96]:frame.save(qa/f'join_{i:03d}.png')
board.save(qa/'transition_all_21.jpg',quality=95)
protected=json.loads((ROOT/'10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8-sig'))
unchanged=[]
for reel in protected['reels']:
    actual=sha(ROOT/reel['source_path']);assert actual==reel['sha256']
    unchanged.append({'model':reel['model'],'sha256':actual,'unchanged':True})
save(OUT/'edit_receipt.json',{'status':'exported_visual_review_pending','file':video.relative_to(ROOT).as_posix(),'sha256':sha(video),'scan':result,'sources':[{'attempt':'B_attempt_02','look':'2026-W41-001-L02','sha256':sha(first),'frames':[0,96],'end_exclusive':True,'purpose':'Front proportion, slight weight adjustment.'},{'attempt':'A_attempt_01','look':'2026-W41-001-L01','sha256':sha(second),'frames':[0,114],'end_exclusive':True,'purpose':'Shallow turn reveals jacket edge and trouser silhouette, then returns front.'}],'transition':{'type':'cross_dissolve','seconds':0.75,'frames':18,'start_seconds':3.25,'end_seconds':4.0},'replan':'A01 originally rejected for duplicate turn; B02 instead stayed frontal. Reassign B02 as front shot and A01 as turn shot, avoiding another generation. B01 back-facing source excluded. A02 retained as frontal alternate only. This does not validate exact requested motion control.','editing':'Tail holds shortened only; native source speed24fps, no crop/zoom/freeze/reverse/internal cuts/text/audio.','generation_count':4,'retries_by_look':{'L01':1,'L02':1},'assistant_continuous_playback':False,'user_film_approval':None,'protected_w41_originals':unchanged,'drive_uploaded':False,'published':False})
print(json.dumps({'frames':192,'seconds':result['decoded_seconds'],'protected_originals':len(unchanged)}))
