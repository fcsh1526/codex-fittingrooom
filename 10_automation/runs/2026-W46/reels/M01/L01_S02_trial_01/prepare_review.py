"""Prepare native-speed review from verified downloaded S02 source."""
import hashlib,json,subprocess
from pathlib import Path
r=Path.cwd()
base=r/'10_automation/runs/2026-W46/reels/M01'
s01=base/'L01_S01_trial_01/source.mp4'
t=base/'L01_S02_trial_01'
src=t/'source.mp4'
ff=r/'openmontage/.local/bin/ffmpeg.exe'
def call(args):
    result=subprocess.run([str(ff),*map(str,args)],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
dec=call(['-hide_banner','-i',src,'-map','0:v:0','-f','null','-'])
(t/'decode_log.txt').write_text(dec.stderr,encoding='utf-8')
call(['-v','error','-y','-i',src,'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',t/'S02_silent_review.mp4'])
a=call(['-v','error','-i',src,'-map','0:v:0','-f','framemd5','-']).stdout
b=call(['-v','error','-i',t/'S02_silent_review.mp4','-map','0:v:0','-f','framemd5','-']).stdout
assert a==b
frame_lines=[x for x in a.splitlines() if x and not x.startswith('#')]
assert len(frame_lines)==145
call(['-v','error','-y','-i',src,'-vf',"select='not(mod(n,12))',scale=180:320,tile=5x3",'-frames:v','1',t/'contact_sheet.png'])
edit=base/'paired_review_v1'
edit.mkdir(exist_ok=True)
out=edit/'M01_W46_seated_shoe_review_v1.mp4'
call(['-v','error','-y','-i',s01,'-i',src,'-filter_complex',
      '[0:v:0]trim=start_frame=0:end_frame=132,setpts=PTS-STARTPTS[a];[1:v:0]trim=start_frame=0:end_frame=66,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]',
      '-map','[v]','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',out])
call(['-v','error','-y','-i',out,'-vf',"select='between(n,120,144)*not(mod(n-120,3))',scale=180:320,tile=5x2",'-frames:v','1',edit/'join_contact.png'])
call(['-v','error','-i',out,'-f','null','-'])
meta=dict(source_sha256=sha(src),silent_sha256=sha(t/'S02_silent_review.mp4'),video_decode='pass',
    width=720,height=1280,fps=24,frame_count=145,duration_seconds=145/24,
    silent_copy_frames_and_timing_match=True,continuous_visual_review='pending',user_acceptance='pending')
(t/'technical_review.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
edl=dict(output=out.relative_to(r).as_posix(),sha256=sha(out),fps=24,frame_count=198,duration_seconds=8.25,
    native_speed=True,baked_text=False,audio=False,transition='hard cut at frame 132 / 5.50 seconds',
    segments=[dict(path=s01.relative_to(r).as_posix(),sha256=sha(s01),source_frames=[0,132],output_frames=[0,132]),
              dict(path=src.relative_to(r).as_posix(),sha256=sha(src),source_frames=[0,66],output_frames=[132,198])],
    status='review_candidate',user_acceptance='pending',continuous_visual_review='pending')
(edit/'edit_manifest.json').write_text(json.dumps(edl,ensure_ascii=False,indent=2),encoding='utf-8')
html="""<!doctype html><meta charset="utf-8"><title>M01 W46 review</title><style>body{background:#222;color:#eee;font:16px sans-serif}video{height:82vh;display:block}button{font-size:18px;margin:8px}</style><button onclick="v.currentTime=0;v.playbackRate=1;v.play()">Play from start at 1x</button><span id="status">Ready</span><video id="v" controls muted preload="auto" src="M01_W46_seated_shoe_review_v1.mp4"></video><script>const v=document.getElementById('v');v.ontimeupdate=()=>document.getElementById('status').textContent=v.currentTime.toFixed(2)+' / '+v.duration.toFixed(2)+' seconds, rate '+v.playbackRate;v.onended=()=>document.getElementById('status').textContent='Ended at '+v.currentTime.toFixed(2)+' seconds, rate '+v.playbackRate;</script>"""
(edit/'review_player.html').write_text(html,encoding='utf-8')
print(out)
