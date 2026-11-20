"""Build one native-speed two-look review from explicitly selected frame ranges."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
FFMPEG=ROOT/'openmontage/.local/bin/ffmpeg.exe'
FFPROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
A=HERE.parent/'L01_trial_01/source.mp4'
B=HERE.parent/'L02_trial_01/source.mp4'
OUT=HERE/'M01_W45_two_looks_review_v1.mp4'
def run(args):
    result=subprocess.run([str(x) for x in args],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-4000:])
    return result.stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(run([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',p]))
for src in [A,B]:
    v=next(x for x in probe(src)['streams'] if x['codec_type']=='video')
    assert (v['width'],v['height'],v['r_frame_rate'])==(720,1280,'24/1')
    assert int(v['nb_frames'])>=144
graph='[0:v]trim=start_frame=12:end_frame=144,setpts=PTS-STARTPTS,fps=24,settb=1/24,format=yuv420p[a];[1:v]trim=start_frame=0:end_frame=132,setpts=PTS-STARTPTS,fps=24,settb=1/24,format=yuv420p[b];[a][b]xfade=transition=fade:duration=0.75:offset=4.75,format=yuv420p[v]'
run([FFMPEG,'-v','error','-y','-i',A,'-i',B,'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','medium','-crf','18','-movflags','+faststart',OUT])
p=probe(OUT);v=next(x for x in p['streams'] if x['codec_type']=='video')
assert v['r_frame_rate']=='24/1' and int(v['nb_frames'])==246
assert abs(float(v['duration'])-10.25)<1e-5
assert not any(x['codec_type']=='audio' for x in p['streams'])
run([FFMPEG,'-v','error','-i',OUT,'-f','null','-'])
(HERE/'probe.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
edl={'date':'2026-11-04','fps':24,'width':720,'height':1280,'total_frames':246,'duration_seconds':10.25,'source_A':{'path':str(A.relative_to(ROOT)).replace('\\','/'),'sha256':sha(A),'range_frames_half_open':[12,144],'source_seconds':[.5,6.0],'output_start_frame':0},'source_B':{'path':str(B.relative_to(ROOT)).replace('\\','/'),'sha256':sha(B),'range_frames_half_open':[0,132],'source_seconds':[0,5.5],'output_start_frame':114},'transition':{'type':'linear_cross_dissolve','frames':18,'seconds':.75,'output_frames_half_open':[114,132],'output_seconds':[4.75,5.5]},'speed':1,'retiming':False,'freeze':False,'crop':False,'text':False,'audio':False,'output_file':OUT.name,'output_sha256':sha(OUT),'full_decode':'completed','continuous_human_visual_review':False,'user_film_acceptance':None,'publication_approval':None}
(HERE/'edit_receipt.json').write_text(json.dumps(edl,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
frames=HERE/'frames';frames.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
def sheet(times,name,cols):
    im=Image.new('RGB',(cols*225,((len(times)+cols-1)//cols)*430),'#f7f6f0');d=ImageDraw.Draw(im)
    for i,t in enumerate(times):
        out=frames/f'{name}_{i:02d}_{t:.4f}.png'
        run([FFMPEG,'-v','error','-y','-ss',t,'-i',OUT,'-frames:v','1',out])
        pic=Image.open(out).convert('RGB');pic.thumbnail((219,390));x=i%cols*225+3;y=i//cols*430+32;im.paste(pic,(x,y));d.text((x,y-26),f'{t:.3f}s',font=font,fill='#233b41')
    im.save(HERE/(name+'.png'))
whole=[i*.5 for i in range(21)]
sheet(whole,'whole_film_contact',5)
join=[4.5]+[i/24 for i in range(114,132,2)]+[5.5,5.75]
sheet(join,'join_contact',4)
run([FFMPEG,'-v','error','-y','-ss',4.25,'-i',OUT,'-t',1.75,'-an','-c:v','libx264','-crf','18','-movflags','+faststart',HERE/'join_context_native.mp4'])
print(json.dumps(edl,ensure_ascii=False))
