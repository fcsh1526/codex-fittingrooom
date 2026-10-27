from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').exists())
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image,ImageDraw
FF=imageio_ffmpeg.get_ffmpeg_exe()
SOURCE=HERE.parent/'F04_close_source.mp4'
BASE=HERE.parent.parent
BRIDGE=BASE/'F03_pushin_motion_01/F03_pushin_source.mp4'
FIRST=BASE/'F04_close_start_01/F04_M03_L02_close_start_candidate_A.png'
PREFIX=BASE.parent.parent/'F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(PREFIX);assert before=='f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33'
def decode(p):
    rd=imageio_ffmpeg.read_frames(str(p),pix_fmt='rgb24',output_params=['-vsync','0']); m=next(rd);s=m['size'];return m,[Image.frombytes('RGB',s,f) for f in rd]
meta,frames=decode(SOURCE); bm,bframes=decode(BRIDGE)
w,h=meta['size'];fps=meta['fps'];count=len(frames)
stream=subprocess.run([FF,'-hide_banner','-i',str(SOURCE)],capture_output=True).stderr.decode('utf-8',errors='replace')
(HERE/'ffmpeg_stream_info.txt').write_text(stream,encoding='utf-8')
def sheet(inds,out,cols=5,tw=216,crop=None):
    srcsize=(w,h) if crop is None else (crop[2]-crop[0],crop[3]-crop[1]);th=round(tw*srcsize[1]/srcsize[0]);rh=th+28
    cv=Image.new('RGB',(cols*tw,((len(inds)+cols-1)//cols)*rh),(240,240,240));d=ImageDraw.Draw(cv)
    for n,i in enumerate(inds):
        im=frames[i] if crop is None else frames[i].crop(crop)
        x=n%cols*tw;y=n//cols*rh;cv.paste(im.resize((tw,th)),(x,y));d.text((x+5,y+th+5),f'f{i:03d}/{i/fps:.3f}s',fill='black')
    cv.save(HERE/out,quality=95)
sheet([round(n*(count-1)/24) for n in range(25)],'checkpoints_25.jpg')
sheet(list(range(72,121,4)),'dense_3_to_5s.jpg',cols=5,tw=240)
sheet(list(range(84,121)),'dense_object_3p5_to_5s.jpg',cols=6,tw=240,crop=(380,300,720,1080))
for i in [0,72,84,88,92,96,100,104,108,112,116,120,144]:frames[i].save(HERE/f'frame_{i:06d}.png')
sheet(list(range(18)),'first18.jpg',cols=6,tw=180)
sheet(list(range(count-18,count)),'last18.jpg',cols=6,tw=180)
cv=Image.new('RGB',(720*3,1280+40),(240,240,240));d=ImageDraw.Draw(cv)
for n,(im,label) in enumerate([(bframes[-1],'bridge last'),(Image.open(FIRST).convert('RGB'),'approved L02 first'),(frames[0],'actual L02 first')]):
    cv.paste(im.resize((720,1280)),(720*n,40));d.text((720*n+8,12),label,fill='black')
cv.save(HERE/'anchor_comparison.jpg',quality=95)
# Three paired phases from actual 18-frame potential overlap, not a joined film.
cv=Image.new('RGB',(720*2,(1280+32)*3),(240,240,240));d=ImageDraw.Draw(cv)
for n,(ai,bi) in enumerate([(127,0),(136,9),(144,17)]):
    yy=n*(1280+32);d.text((8,yy+8),f'bridge f{ai} | L02 f{bi}',fill='black')
    cv.paste(bframes[ai],(0,yy+32));cv.paste(frames[bi],(720,yy+32))
cv.save(HERE/'overlap_phase_pairs.jpg',quality=95)
silent=HERE/'F04_close_silent.mp4';assert not silent.exists()
r=subprocess.run([FF,'-hide_banner','-n','-i',str(SOURCE),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(silent)],capture_output=True)
(HERE/'silent_remux_log.txt').write_text(r.stderr.decode('utf-8',errors='replace'),encoding='utf-8');assert r.returncode==0
def bits(p):
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-i',str(p),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','pipe:1'],capture_output=True);assert r.returncode==0;return hashlib.sha256(r.stdout).hexdigest()
a,b=bits(SOURCE),bits(silent);assert a==b
after=sha(PREFIX);assert after==before
report={'source':str(SOURCE),'sha256':sha(SOURCE),'bytes':SOURCE.stat().st_size,'metadata':meta,'decoded_frames':count,'derived_frame_duration_seconds':count/fps,'silent':{'path':str(silent),'sha256':sha(silent),'bytes':silent.stat().st_size,'source_main_h264_annexb_sha256':a,'silent_main_h264_annexb_sha256':b,'identical':True,'remux_only':True,'cropped':False,'retimed':False,'reencoded':False},'prefix_sha256_before':before,'prefix_sha256_after':after,'continuous_playback_performed':False,'visual_review_pending':True}
(HERE/'technical_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
