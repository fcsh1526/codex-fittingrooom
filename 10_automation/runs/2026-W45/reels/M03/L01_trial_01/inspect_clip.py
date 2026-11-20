"""Decode and sample this one clip; never label sampling as continuous visual QA."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
FFMPEG=ROOT/'openmontage/.local/bin/ffmpeg.exe'
FFPROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
src=HERE/'source.mp4'
def run(args):
    return subprocess.run([str(x) for x in args],capture_output=True,text=True,encoding='utf-8',errors='replace',check=True).stdout
probe=json.loads(run([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',src]))
(HERE/'source_probe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
video=next(s for s in probe['streams'] if s['codec_type']=='video' and not s.get('disposition',{}).get('attached_pic'))
run([FFMPEG,'-v','error','-i',src,'-f','null','-'])
review=HERE/'M03_W45_L01_trial01_silent_review.mp4'
run([FFMPEG,'-v','error','-y','-i',src,'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',review])
src_md5=run([FFMPEG,'-v','error','-i',src,'-map','0:v:0','-f','framemd5','-'])
review_md5=run([FFMPEG,'-v','error','-i',review,'-map','0:v:0','-f','framemd5','-'])
assert src_md5==review_md5,'Silent remux changed decoded frames/timing'
frames=HERE/'frames';frames.mkdir(exist_ok=True)
times=[i*.5 for i in range(int(float(video['duration'])*2)+1)]
for i,t in enumerate(times):
    run([FFMPEG,'-v','error','-y','-ss',t,'-i',src,'-map','0:v:0','-frames:v','1',frames/f'f_{i:02d}_{t:.2f}s.png'])
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',20)
sheet=Image.new('RGB',(5*225,((len(times)+4)//5)*445),'#f7f6f0');d=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    frame=Image.open(frames/f'f_{i:02d}_{t:.2f}s.png').convert('RGB');frame.thumbnail((219,400))
    x=(i%5)*225+3;y=(i//5)*445+36;sheet.paste(frame,(x,y))
    d.text((x,y-29),f'{t:.2f}s',font=font,fill='#243b41')
sheet.save(HERE/'contact_sheet.png')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
data=dict(video_asset_id=json.loads((HERE/'submission.json').read_text(encoding='utf-8'))['video_asset_id'],source_sha256=sha(src),silent_review_sha256=sha(review),width=video['width'],height=video['height'],fps=video['r_frame_rate'],frame_count=int(video['nb_frames']),duration_seconds=float(video['duration']),audio_present_in_source=any(s['codec_type']=='audio' for s in probe['streams']),silent_review_audio=False,full_file_decode='completed',silent_remux_frame_and_timing_hashes_identical=True,retiming=False,cuts=False,baked_text_added=False,sampled_seconds=times,continuous_human_visual_review=False,user_clip_acceptance=None,publication_approval=None,limits='Technical decode and sampled stills only; not physical gait/hand/identity or appeal certification.')
(HERE/'technical_review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data,ensure_ascii=False))
