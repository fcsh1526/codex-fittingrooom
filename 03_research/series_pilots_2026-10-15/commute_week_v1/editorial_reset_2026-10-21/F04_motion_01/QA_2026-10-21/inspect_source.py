"""Inspect one explicitly identified F04 source; no joining or outside-folder writes."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').exists())
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--sha256',required=True);a=ap.parse_args()
SRC=Path(a.source).resolve();assert SRC.parent==HERE.parent and SRC.name=='F04_source.mp4'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SRC)==a.sha256.lower(),'Source identity mismatch'
RESET=HERE.parent.parent;COMMUTE=RESET.parent;BRIDGE=COMMUTE/'production_bridge_2026-10-19'
FIRST=RESET/'F04_full_start_01/F04_M03_L02_full_start_candidate_A.png'
LATE=RESET/'F04_full_late_01/F04_M03_L02_full_late_candidate_A.png'
assert sha(FIRST)=='03b45655b7bef2b97b3ef19de6cc9b864b86341d908114e149f0653c8dfd36f0'
assert sha(LATE)=='f9b3c4e0bf0ba2abd0924697e48a05454df8b9578667c1cb363905e9b36392ff'
PREFIX=BRIDGE/'F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4'
PAIR=BRIDGE/'F02/motion_retry_01/F01_F02_gait_fix_review_v1.mp4'
OLD=BRIDGE/'F05/five_look_review_2026-10-21/v1/review.mp4'
protected=[FIRST,LATE,PREFIX,PAIR,OLD]
before={str(p):sha(p) for p in protected}
assert before[str(PREFIX)]=='f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33'
assert before[str(PAIR)]=='54da666276fd89fc93461fc25bbe2aa805e565beff8f708bf071b78118a462dd'
assert before[str(OLD)]=='be262d6771141eeda11d2671cc5c1a87b7a03d869aacf60c117e5d5bc8b38b03'
FF=imageio_ffmpeg.get_ffmpeg_exe()
rd=imageio_ffmpeg.read_frames(str(SRC),pix_fmt='rgb24',output_params=['-vsync','0']);m=next(rd);w,h=m['size'];fps=m['fps']
frames=[Image.frombytes('RGB',(w,h),b) for b in rd];n=len(frames)
def sheet(indices,name,cols=5,tw=216):
    th=round(h*tw/w);rh=th+26;cv=Image.new('RGB',(cols*tw,((len(indices)+cols-1)//cols)*rh),(240,240,240));d=ImageDraw.Draw(cv)
    for k,i in enumerate(indices):
        x=k%cols*tw;y=k//cols*rh;cv.paste(frames[i].resize((tw,th)),(x,y));d.text((x+4,y+th+4),f'f{i:03d}/{i/fps:.3f}s',fill='black')
    cv.save(HERE/name,quality=95)
sheet([round(k*(n-1)/24) for k in range(25)],'checkpoints_25.jpg')
sheet(list(range(min(18,n))),'first18.jpg',6,180)
sheet(list(range(max(0,n-18),n)),'last18.jpg',6,180)
sheet(list(range(80,min(n,111),2)),'dense_frames080_to110.jpg',4,240)
sheet(list(range(90,min(n,108))),'prospective_out_overlap_f090_to107.jpg',6,180)
anchor=round(fps*13/3)
for i in sorted(set([0,17,90,anchor,107,n//2,n-1]+list(range(24,n,12)))):
    if i<n:frames[i].save(HERE/f'frame_{i:06d}.png')
cv=Image.new('RGB',(w*4,h+36),(240,240,240));d=ImageDraw.Draw(cv)
for k,(im,label) in enumerate([(Image.open(FIRST).convert('RGB'),'approved first'),(frames[0],'actual f0'),(frames[min(anchor,n-1)],f'actual f{anchor}'),(Image.open(LATE).convert('RGB'),'approved late guide')]):
    cv.paste(im.resize((w,h)),(k*w,36));d.text((k*w+6,10),label,fill='black')
cv.save(HERE/'anchor_comparison.jpg',quality=95)
cv=Image.new('RGB',(w*3,h+36),(240,240,240));d=ImageDraw.Draw(cv)
for k,(im,label) in enumerate([(Image.open(RESET/'source_audit/F03_f091.png').convert('RGB'),'previous F03 f91'),(Image.open(FIRST).convert('RGB'),'approved F04 first'),(frames[0],'actual F04 f0')]):
    cv.paste(im.resize((w,h)),(k*w,36));d.text((k*w+6,10),label,fill='black')
cv.save(HERE/'input_boundary_comparison.jpg',quality=95)
info=subprocess.run([FF,'-hide_banner','-i',str(SRC)],capture_output=True).stderr.decode('utf-8',errors='replace');(HERE/'ffmpeg_stream_info.txt').write_text(info,encoding='utf-8')
SILENT=HERE/'F04_silent.mp4';assert not SILENT.exists(),'No overwriting'
r=subprocess.run([FF,'-hide_banner','-n','-i',str(SRC),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(SILENT)],capture_output=True)
(HERE/'silent_remux_log.txt').write_text(r.stderr.decode('utf-8',errors='replace'),encoding='utf-8');assert r.returncode==0
def bitsha(p):
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-i',str(p),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','pipe:1'],capture_output=True);assert r.returncode==0;return hashlib.sha256(r.stdout).hexdigest()
bh1,bh2=bitsha(SRC),bitsha(SILENT);assert bh1==bh2
after={str(p):sha(p) for p in protected};assert before==after
report={'source':str(SRC),'sha256':sha(SRC),'bytes':SRC.stat().st_size,'metadata':m,'fully_decoded':True,'decoded_frames':n,'derived_frame_duration_seconds':n/fps,'requested_late_anchor_seconds':13/3,'nearest_late_frame_index':anchor,'native_frame90_107_exported':n>107,'prospective_first108_interval_only_if_24fps':fps==24.0,'silent':{'path':str(SILENT),'sha256':sha(SILENT),'bytes':SILENT.stat().st_size,'source_main_h264_annexb_sha256':bh1,'silent_main_h264_annexb_sha256':bh2,'identical':True,'stream_copy_only':True,'cropped':False,'retimed':False,'reencoded':False},'protected_hashes_before':before,'protected_hashes_after':after,'continuous_playback_performed':False,'visual_review_pending':True}
(HERE/'technical_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
