import json,hashlib,subprocess
from pathlib import Path
base=Path('10_automation/runs/2026-W46/reels/M01')
t=base/'N04_trial_01'
ff=Path('openmontage/.local/bin/ffmpeg.exe').resolve()
def run(args):
    p=subprocess.run([str(ff),*map(str,args)],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode:raise RuntimeError(p.stderr)
    return p
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
decode=run(['-hide_banner','-i',t/'source.mp4','-map','0:v:0','-f','null','-'])
(t/'decode_log.txt').write_text(decode.stderr,encoding='utf-8')
run(['-v','error','-y','-i',t/'source.mp4','-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',t/'N04_silent_review.mp4'])
a=run(['-v','error','-i',t/'source.mp4','-map','0:v:0','-f','framemd5','-']).stdout
b=run(['-v','error','-i',t/'N04_silent_review.mp4','-map','0:v:0','-f','framemd5','-']).stdout
assert a==b
assert len([l for l in a.splitlines() if l and not l.startswith('#')])==145
run(['-v','error','-y','-i',t/'source.mp4','-vf',"select='not(mod(n,12))',scale=180:320,tile=5x3",'-frames:v','1',t/'contact_sheet.png'])
segments=[
('N01','N01_trial_01/source.mp4',18,48),
('N02','L01_S02_trial_01/source.mp4',0,18),
('N03','L01_S01_trial_01/source.mp4',66,108),
('N04','N04_trial_01/source.mp4',36,72),
('N05','L01_S02_trial_01/source.mp4',114,144)]
inputs=[]
filters=[]
for i,(shot,path,start,end) in enumerate(segments):
    inputs.extend(['-i',base/path])
    filters.append(f'[{i}:v:0]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS[v{i}]')
filters.append(''.join(f'[v{i}]' for i in range(5))+'concat=n=5:v=1:a=0[v]')
edit=base/'opening_five_beats_v1'
edit.mkdir(exist_ok=True)
out=edit/'M01_first_five_beats_6p5s.mp4'
run(['-v','error','-y',*inputs,'-filter_complex',';'.join(filters),'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',out])
d=run(['-v','error','-i',out,'-map','0:v:0','-f','framemd5','-']).stdout
assert len([l for l in d.splitlines() if l and not l.startswith('#')])==156
edl=[];cursor=0
for shot,path,start,end in segments:
    edl.append(dict(shot=shot,path=(base/path).as_posix(),sha256=sha(base/path),source_frames=[start,end],output_frames=[cursor,cursor+end-start]))
    cursor+=end-start
meta=dict(output=out.as_posix(),sha256=sha(out),frame_count=156,fps=24,duration=6.5,native_speed=True,audio=False,baked_text=False,segments=edl,
    stage='N01-N05 draft of eight-beat 13.5-second plan',visual_review='pending',user_acceptance='pending')
(edit/'edit_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)

