"""Inspect the exact L01 trial; preserve timing and make the proposed crop testable."""
from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent; ROOT=B.parents[5]; P=B/'L02_trial_01'
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def run(args):
    r=subprocess.run([str(x) for x in args],capture_output=True)
    if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-4000:])
    return r.stdout
def put(name,v):(P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=P/'source.mp4'
pr=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',src]));put('source_probe.json',pr)
v=next(s for s in pr['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'],v['avg_frame_rate'])==(720,1280,'24/1'),v
assert 9.8<float(v['duration'])<10.3,v['duration']
run([FF,'-v','error','-i',src,'-map','0:v:0','-f','null','-'])
silent=P/'M03_W45_reference_L02_trial01_silent.mp4'
run([FF,'-v','error','-y','-i',src,'-map','0:v:0','-c:v','copy','-an','-map_metadata','-1','-movflags','+faststart',silent])
panel=P/'M03_W45_reference_L02_trial01_panel_diagnostic.mp4'
run([FF,'-v','error','-y','-i',src,'-filter_complex','[0:v]crop=400:1034:180:130,scale=356:920,pad=720:1280:0:180:color=0xf5f3ec[v]','-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',panel])
qa=P/'qa';qa.mkdir(exist_ok=True)
run([FF,'-v','error','-y','-i',src,'-vf','select=not(mod(n\\,3))','-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
files=sorted(qa.glob('frame_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
for name,stride,crop,cell in [('whole_film_contact',4,None,(210,398)),('upper_body_contact',2,(120,50,680,760),(250,345)),('planned_panel_contact',2,(180,130,580,1164),(160,440))]:
    selected=list(range(0,len(files),stride));cols=7;cw,ch=cell
    im=Image.new('RGB',(cols*cw,((len(selected)+cols-1)//cols)*ch),'#f5f3ec');d=ImageDraw.Draw(im)
    for j,k in enumerate(selected):
        f=Image.open(files[k]);f=f.crop(crop) if crop else f;f.thumbnail((cw-4,ch-28))
        x=j%cols*cw;y=j//cols*ch;im.paste(f,(x,y+25));d.text((x+2,y),f'{k*.125:.3f}s',font=font,fill='#233b46')
    im.save(P/(name+'.jpg'),quality=95)
tech={'width':720,'height':1280,'fps':24,'frame_count':int(v['nb_frames']),'seconds':float(v['duration']),
 'source_has_audio':any(s['codec_type']=='audio' for s in pr['streams']),'source_sha256':sha(src),
 'silent_path':silent.relative_to(ROOT).as_posix(),'silent_sha256':sha(silent),'full_decode':True,
 'native_speed':True,'silent_video_stream_copy':True,'extracted_every_frames':3,'sample_count':len(files),
 'panel_diagnostic_path':panel.relative_to(ROOT).as_posix(),'panel_crop_xywh':[180,130,400,1034],
 'panel_output_xywh':[0,180,356,920],'panel_sha256':sha(panel),
 'panel_note':'Left panel only; right blank intentionally. Diagnostic, not finished film.',
 'uninterrupted_human_review':False,'user_film_acceptance':None,'publication_approval':None}
put('technical_review.json',tech)
sub=json.loads((P/'submission.json').read_text(encoding='utf-8'));sub.update(status='downloaded_pending_visual_review',**tech);put('submission.json',sub)
print(json.dumps(tech,ensure_ascii=False))
