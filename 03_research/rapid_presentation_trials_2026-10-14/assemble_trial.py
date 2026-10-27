from pathlib import Path
import argparse, hashlib, json, subprocess, sys

base=Path(__file__).resolve().parent
root=base.parents[1]
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg

p=argparse.ArgumentParser()
p.add_argument('--a-end',type=float,required=True)
p.add_argument('--b-start',type=float,default=0)
p.add_argument('--b-end',type=float,required=True)
p.add_argument('--version',default='v1')
args=p.parse_args()
a=base/'A_motion_attempt_01/source.mp4'
b=base/'B_motion_attempt_01/source.mp4'
out=base/f'joined_review_{args.version}'
out.mkdir(exist_ok=True)
target=out/f'M04_blue_bag_viewing_route_{args.version}.mp4'
if target.exists(): raise SystemExit('Select a fresh version; existing output preserved.')
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
for source in (a,b):
    preview=source.parent/'review_silent.mp4'
    if not preview.exists():
        subprocess.run([ffmpeg,'-y','-i',str(source),'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',str(preview)],check=True,capture_output=True)
offset=args.a_end-.75
fg=(f'[0:v:0]trim=start=0:end={args.a_end},scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,setpts=PTS-STARTPTS,fps=24[a];'
    f'[1:v:0]trim=start={args.b_start}:end={args.b_end},scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,setpts=PTS-STARTPTS,fps=24[b];'
    f'[a][b]xfade=transition=fade:duration=0.75:offset={offset}[v]')
subprocess.run([ffmpeg,'-y','-i',str(a),'-i',str(b),'-filter_complex',fg,'-map','[v]','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],check=True,capture_output=True)
r={'model':'M04','look_ids':['2026-W41-005-L01','2026-W41-005-L02'],'sources':[{'path':s.relative_to(root).as_posix(),'sha256':hashlib.sha256(s.read_bytes()).hexdigest()} for s in (a,b)],'intervals_seconds':[[0,args.a_end],[args.b_start,args.b_end]],'join_seconds':[offset,args.a_end],'join_duration':.75,'speed':'1x, no reverse/freeze/duplicate','output':target.relative_to(root).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'audio':False,'text':False,'framing':'Proportional cover and center crop; no stretch','visual_review':'pending','assistant_continuous_playback':False,'user_approval':None,'publishing_replacement':False}
(out/'edit_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target)
