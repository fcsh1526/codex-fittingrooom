from pathlib import Path
import argparse,hashlib,json,sys,subprocess
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CURRENT_STATUS.md').exists())
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser();ap.add_argument('--source-sha',required=True);a=ap.parse_args()
SRC=HERE.parent/'F05_half_source.mp4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert SRC.exists() and sha(SRC)==a.source_sha.lower(),'Missing/wrong new F05 source'
RESET=HERE.parent.parent
FIRST=RESET/'F05_full_start_01/F05_M03_L04_full_start_candidate_A.png'
LATE=RESET/'F05_half_late_01/F05_M03_L04_half_late_candidate_A.png'
PREFIX=RESET/'four_look_review/v1/review.mp4'
assert sha(FIRST)=='ac588ec1674df43923140e17f46c4734706cf834f2b7f5599aeeec60376f9c82'
assert sha(LATE)=='114300736fbcf321316d20ce992f968bcb39d9dcea0e85542f0491ee97539ab7'
assert sha(PREFIX)=='3c0f3fa5bb0c90d0d9b5d434ada37cd5dbe130658d5bff24c01143feb77f1f94'
protected={str(p):sha(p) for p in [FIRST,LATE,PREFIX]}
rd=imageio_ffmpeg.read_frames(str(SRC),pix_fmt='rgb24',output_params=['-vsync','0']);m=next(rd);w,h=m['size'];fps=m['fps']
frames=[Image.frombytes('RGB',(w,h),b) for b in rd];n=len(frames)
def sheet(indices,name,cols=5,tw=216):
 th=round(h*tw/w);rh=th+26;cv=Image.new('RGB',(cols*tw,((len(indices)+cols-1)//cols)*rh),'#f0f0f0');d=ImageDraw.Draw(cv)
 for k,i in enumerate(indices):
  x=k%cols*tw;y=k//cols*rh;cv.paste(frames[i].resize((tw,th)),(x,y));d.text((x+4,y+th+4),f'f{i:03d}/{i/fps:.3f}s',fill='black')
 cv.save(HERE/name,quality=95)
sheet([round(k*(n-1)/24) for k in range(25)],'checkpoints_25.jpg')
sheet(list(range(min(n,18))),'first18.jpg',6,180)
sheet(list(range(60,min(n,145),4)),'pushin_dense_f060_to144.jpg',5,216)
for i in [0,17,24,48,72,90,96,108,120,128,132,143,144]:
 if i<n:frames[i].save(HERE/f'frame_{i:06d}.png')
anchor=round(fps*16/3)
cv=Image.new('RGB',(w*4,h+36),'#f0f0f0');d=ImageDraw.Draw(cv)
for k,(im,label) in enumerate([(Image.open(FIRST).convert('RGB'),'approved first'),(frames[0],'actual f0'),(frames[min(n-1,anchor)],f'actual f{anchor}'),(Image.open(LATE).convert('RGB'),'approved half guide')]):
 cv.paste(im.resize((w,h)),(k*w,36));d.text((k*w+5,10),label,fill='black')
cv.save(HERE/'anchor_comparison.jpg',quality=95)
FF=imageio_ffmpeg.get_ffmpeg_exe()
info=subprocess.run([FF,'-hide_banner','-i',str(SRC)],capture_output=True).stderr.decode('utf-8',errors='replace')
(HERE/'ffmpeg_stream_info.txt').write_text(info,encoding='utf-8')
silent=HERE/'F05_half_silent.mp4'
assert not silent.exists(),'Do not overwrite a prior remux'
rr=subprocess.run([FF,'-hide_banner','-n','-i',str(SRC),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(silent)],capture_output=True)
(HERE/'silent_remux_log.txt').write_text(rr.stderr.decode('utf-8',errors='replace'),encoding='utf-8');assert rr.returncode==0
def bitsha(p):
 rr=subprocess.run([FF,'-hide_banner','-loglevel','error','-i',str(p),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','pipe:1'],capture_output=True);assert rr.returncode==0;return hashlib.sha256(rr.stdout).hexdigest()
b1,b2=bitsha(SRC),bitsha(silent);assert b1==b2
assert protected=={str(Path(p)):sha(Path(p)) for p in protected}
r={'source':str(SRC),'sha256':sha(SRC),'bytes':SRC.stat().st_size,'metadata':m,'fully_decoded':True,'decoded_frames':n,'derived_frame_duration_seconds':n/fps,'selected_frames_if_eligible':[0,144],'requested_half_keyframe_s':16/3,'nearest_half_frame':anchor,'silent':{'path':str(silent),'sha256':sha(silent),'bytes':silent.stat().st_size,'source_main_h264_annexb_sha256':b1,'silent_main_h264_annexb_sha256':b2,'identical':True,'stream_copy_only':True,'retimed':False,'cropped':False,'reencoded':False},'protected_hashes_unchanged':True,'continuous_playback_performed':False,'visual_review_pending':True}
(HERE/'technical_report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:r[k] for k in ['sha256','bytes','decoded_frames','derived_frame_duration_seconds','silent']},ensure_ascii=False))

