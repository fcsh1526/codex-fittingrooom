"""Read-only source scan and separately named lossless silent review remux.
Never renders joins or writes outside this QA folder. Explicit source SHA required.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').exists())
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image,ImageDraw
parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--sha256',required=True);args=parser.parse_args()
SOURCE=Path(args.source).resolve();assert SOURCE.parent==HERE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE)==args.sha256.lower()
F05=HERE.parent.parent
BRIDGE=F05.parent
CLOSE=BRIDGE/'F04/close_tracking_proposal_2026-10-20'
F04=CLOSE/'F04_close_motion_01/F04_close_source.mp4'
FIRST=F05/'first_still_01/F05_M03_L04_start_candidate_A.png'
LAST=F05/'end_still_01/F05_M03_L04_end_candidate_A.png'
assert sha(FIRST)=='9bc90ffa51bdad22106401647fef10fbf20b2da6faf88192b1b6f8191aba97d2'
assert sha(LAST)=='9af51b785d2bd104751cd2502deaa86f29cad217621643cef98c23d0ff1f16e7'
PREFIX=BRIDGE/'F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4'
LOCAL=CLOSE/'close_join_review_2026-10-21/v2/local/review.mp4'
CONTEXT=CLOSE/'close_join_review_2026-10-21/v2/context/review.mp4'
protected=[PREFIX,LOCAL,CONTEXT,FIRST,LAST,F04]
before={str(p):sha(p) for p in protected}
assert before[str(PREFIX)]=='f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33'
assert before[str(LOCAL)]=='7dbd3d6c8ec11203b6a4decaa44c30bbfae2576318bea241ff914460e40f7e49'
FF=imageio_ffmpeg.get_ffmpeg_exe()
def decode(p):
    rd=imageio_ffmpeg.read_frames(str(p),pix_fmt='rgb24',output_params=['-vsync','0']);m=next(rd)
    return m,[Image.frombytes('RGB',m['size'],b) for b in rd]
m,frames=decode(SOURCE);pm,pframes=decode(F04)
w,h=m['size'];fps=m['fps'];n=len(frames)
stream=subprocess.run([FF,'-hide_banner','-i',str(SOURCE)],capture_output=True).stderr.decode('utf-8',errors='replace')
(HERE/'ffmpeg_stream_info.txt').write_text(stream,encoding='utf-8')
def sheet(inds,name,cols=5,tw=216,crop=None):
    sw,sh=(w,h) if crop is None else (crop[2]-crop[0],crop[3]-crop[1]);th=round(tw*sh/sw);rh=th+26
    cv=Image.new('RGB',(cols*tw,((len(inds)+cols-1)//cols)*rh),(240,240,240));d=ImageDraw.Draw(cv)
    for k,i in enumerate(inds):
        im=frames[i] if crop is None else frames[i].crop(crop)
        x=k%cols*tw;y=k//cols*rh;cv.paste(im.resize((tw,th)),(x,y));d.text((x+4,y+th+4),f'f{i:03d}/{i/fps:.3f}s',fill='black')
    cv.save(HERE/name,quality=95)
sheet([round(i*(n-1)/24) for i in range(25)],'checkpoints_25.jpg')
sheet(list(range(min(n,18))),'first18.jpg',6,180)
sheet(list(range(max(0,n-18),n)),'last18.jpg',6,180)
sheet(list(range(48,min(n,121),4)),'dense_pullback_2_to_5s.jpg',5,216)
sheet(list(range(72,min(n,145),3)),'dense_late_background.jpg',5,216)
for i in sorted(set([0,17,n//2,n-1]+list(range(24,min(n,145),12)))):frames[i].save(HERE/f'frame_{i:06d}.png')
cv=Image.new('RGB',(w*4,h+36),(240,240,240));d=ImageDraw.Draw(cv)
for k,(im,label) in enumerate([(Image.open(FIRST).convert('RGB'),'approved first'),(frames[0],'actual first'),(frames[-1],'actual last'),(Image.open(LAST).convert('RGB'),'approved end')]):
    cv.paste(im.resize((w,h)),(k*w,36));d.text((k*w+8,10),label,fill='black')
cv.save(HERE/'anchor_comparison.jpg',quality=95)
cv=Image.new('RGB',(w*2,(h+32)*3),(240,240,240));d=ImageDraw.Draw(cv)
for k,(pi,ni) in enumerate([(127,0),(136,9),(144,17)]):
    y=k*(h+32);d.text((8,y+8),f'F04 f{pi} | F05 f{ni}',fill='black');cv.paste(pframes[pi],(0,y+32));cv.paste(frames[ni],(w,y+32))
cv.save(HERE/'overlap_phase_pairs.jpg',quality=95)
silent=HERE/'F05_silent.mp4';assert not silent.exists(),'No overwriting'
r=subprocess.run([FF,'-hide_banner','-n','-i',str(SOURCE),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(silent)],capture_output=True)
(HERE/'silent_remux_log.txt').write_text(r.stderr.decode('utf-8',errors='replace'),encoding='utf-8');assert r.returncode==0
def bitsha(p):
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-i',str(p),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','pipe:1'],capture_output=True);assert r.returncode==0;return hashlib.sha256(r.stdout).hexdigest()
a,b=bitsha(SOURCE),bitsha(silent);assert a==b
after={str(p):sha(p) for p in protected};assert before==after
report={'source':str(SOURCE),'sha256':sha(SOURCE),'bytes':SOURCE.stat().st_size,'metadata':m,'decoded_frames':n,'derived_frame_duration_seconds':n/fps,'silent':{'path':str(silent),'sha256':sha(silent),'bytes':silent.stat().st_size,'source_main_h264_annexb_sha256':a,'silent_main_h264_annexb_sha256':b,'identical':True,'remux_only':True,'crop':False,'retime':False,'reencode':False},'protected_hashes_before':before,'protected_hashes_after':after,'continuous_playback_performed':False,'visual_review_pending':True}
(HERE/'technical_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps(report,indent=2,ensure_ascii=False))
