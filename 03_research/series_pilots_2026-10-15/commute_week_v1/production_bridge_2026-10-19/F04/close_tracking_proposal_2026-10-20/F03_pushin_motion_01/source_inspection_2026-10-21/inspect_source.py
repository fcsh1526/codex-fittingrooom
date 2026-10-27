from pathlib import Path
import hashlib, json, subprocess, sys, re
ROOT=Path(__file__).resolve().parents[9]
# Resolve from the known project marker rather than depending on shell cwd.
for candidate in Path(__file__).resolve().parents:
    if (candidate/'10_automation/CANONICAL_WORKFLOW.md').exists(): ROOT=candidate; break
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'F03_pushin_source.mp4'
BRIDGE=ROOT/'03_research/series_pilots_2026-10-15/commute_week_v1/production_bridge_2026-10-19'
PREFIX=BRIDGE/'F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4'
FIRST=BRIDGE/'F04/F03_actual_frame_000127.png'
LAST=HERE.parent.parent/'F03_pushin_endpoint_01/F03_M03_L03_close_endpoint_candidate_A.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
protected_before=sha(PREFIX)
assert protected_before=='f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33'
FF=imageio_ffmpeg.get_ffmpeg_exe()
meta=subprocess.run([FF,'-hide_banner','-i',str(SOURCE)],capture_output=True).stderr.decode('utf-8',errors='replace')
(HERE/'ffmpeg_stream_info.txt').write_text(meta,encoding='utf-8')
reader=imageio_ffmpeg.read_frames(str(SOURCE),pix_fmt='rgb24',output_params=['-vsync','0'])
stream=next(reader); w,h=stream['size']; fps=stream['fps']
frames=[Image.frombytes('RGB',(w,h),f) for f in reader]
count=len(frames)
indices=sorted(set(round(i*(count-1)/24) for i in range(25)))
def sheet(indices,out,cols=5,thumbw=216):
    th=round(h*thumbw/w); rh=th+28
    canvas=Image.new('RGB',(cols*thumbw,((len(indices)+cols-1)//cols)*rh),(240,240,240)); d=ImageDraw.Draw(canvas)
    for n,idx in enumerate(indices):
        x=(n%cols)*thumbw;y=(n//cols)*rh
        canvas.paste(frames[idx].resize((thumbw,th)),(x,y));d.text((x+5,y+th+5),f'f{idx:03d} / {idx/fps:.3f}s',fill='black')
    canvas.save(HERE/out,quality=94)
sheet(indices,'checkpoints_25.jpg')
sheet(list(range(max(0,count-18),count)),'last_18_frames.jpg',cols=6,thumbw=180)
for idx,name in [(0,'first'),(count//2,'middle'),(count-1,'last')]:frames[idx].save(HERE/f'{name}_f{idx:03d}.png')
compare=Image.new('RGB',(w*4,h+40),(245,245,245));d=ImageDraw.Draw(compare)
for n,(im,label) in enumerate([(Image.open(FIRST).convert('RGB'),'approved first F03 f127'),(frames[0],'actual first'),(frames[-1],'actual last'),(Image.open(LAST).convert('RGB'),'approved close endpoint')]):
    compare.paste(im.resize((w,h)),(n*w,40));d.text((n*w+10,12),label,fill='black')
compare.save(HERE/'anchor_comparison.jpg',quality=94)
silent=HERE/'F03_pushin_silent.mp4'
assert not silent.exists(),'No overwriting outputs'
remux=subprocess.run([FF,'-hide_banner','-n','-i',str(SOURCE),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(silent)],capture_output=True)
(HERE/'silent_remux_log.txt').write_text(remux.stderr.decode('utf-8',errors='replace'),encoding='utf-8')
assert remux.returncode==0,remux.stderr
def elementary(p):
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-i',str(p),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','pipe:1'],capture_output=True)
    assert r.returncode==0,r.stderr
    return hashlib.sha256(r.stdout).hexdigest()
raw1,raw2=elementary(SOURCE),elementary(silent)
assert raw1==raw2
protected_after=sha(PREFIX);assert protected_before==protected_after
report={'source':str(SOURCE),'sha256':sha(SOURCE),'bytes':SOURCE.stat().st_size,'metadata':stream,'decoded_frames':count,'derived_frame_duration_seconds':count/fps,'silent':{'path':str(silent),'sha256':sha(silent),'bytes':silent.stat().st_size,'main_h264_annexb_sha256':raw2,'source_main_h264_annexb_sha256':raw1,'identical':raw1==raw2,'remux_only':True,'retimed':False,'cropped':False,'reencoded':False},'protected_prefix_sha256_before':protected_before,'protected_prefix_sha256_after':protected_after,'visual_qa_pending':True,'continuous_playback_performed':False}
(HERE/'technical_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
