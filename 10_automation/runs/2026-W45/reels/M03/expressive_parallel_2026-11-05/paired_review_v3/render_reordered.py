"""Reordered selected intervals with a wider fixed crop to retain hands."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;BR=P.parent;ROOT=BR.parents[5]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
L=BR/'trial_02/source.mp4';R=BR/'L02_trial_01/source.mp4';OLD=BR/'paired_review_v1/M03_W45_parallel_selected_review_v1.mp4'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args):
    r=subprocess.run([str(a) for a in args],capture_output=True)
    if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-4000:])
    return r.stdout
protected={str(p):h(p) for p in [L,R,OLD]}
assert protected[str(L)]=='533f789b3aab103573af3270f545aa3834a2e483805306659ff6a4fef009c3e2'
assert protected[str(R)]=='13b4f38ca17ddd2e0495775753d6ed1eb02db2bc0ed73496ebc9a98d0aa436fe'
assert protected[str(OLD)]=='3ab8dbe73a02546f12135f3cfed9e7184016e2af531038e9414688dcaeec9135'
plan={'date':'2026-11-05','status':'local_edit_test_prepared','viewer_purpose':'Compare the same navy blazer with work trousers and a cream A-line skirt, via generous outfit poses.','motivation':'A playful outfit presentation addressed to the camera, with turn revealing side/back, then frontal waist/hip poses for clear comparison.','authorization':'User selected A parallel layout; latest ok acknowledges that production direction, not film/publication approval.','main_variable':'Order plus static framing, based on internal v2 review; not a single-variable causal comparison.','left_intervals':[[126,192],[0,78]],'right_intervals':[[144,210],[0,78]],'join_output_frames':[48,66],'overlap_frames':18,'output_frames':126,'fps':24,'native_speed':True,'crop':[80,0,560,1280],'panel':[356,1280],'gutter':8,'scale':356/560,'no_ai_warp_or_optical_flow':True,'new_stills':0,'new_video_jobs':0,'expected_limit':'Double outlines can remain. Test whether frontal-return-to-frontal-start reduces face mismatch; not a physical repair or zero-ghost promise.'}
put('edit_plan.json',plan)
chains=[]
for i,(tag,a,b) in enumerate([('l',(126,192),(0,78)),('r',(144,210),(0,78))]):
    chains += [f'[{i}:v:0]split=2[{tag}a][{tag}b]',f'[{tag}a]trim=start_frame={a[0]}:end_frame={a[1]},setpts=PTS-STARTPTS,fps=24,settb=1/24[{tag}1]',f'[{tag}b]trim=start_frame={b[0]}:end_frame={b[1]},setpts=PTS-STARTPTS,fps=24,settb=1/24[{tag}2]',f'[{tag}1][{tag}2]xfade=transition=fade:duration=0.75:offset=2,trim=end_frame=126,crop=560:1280:80:0,scale=356:-2,pad=356:1280:0:(oh-ih)/2:color=0xf1eee6,setsar=1[{tag}out]']
chains+=['[lout][rout]xstack=inputs=2:layout=0_0|364_0:fill=0xf1eee6,format=yuv420p[out]']
OUT=P/'M03_W45_parallel_selected_review_v3.mp4'
run([FF,'-v','error','-y','-i',L,'-i',R,'-filter_complex',';'.join(chains),'-map','[out]','-frames:v','126','-c:v','libx264','-crf','18','-preset','fast','-an','-map_metadata','-1','-movflags','+faststart',OUT])
probe=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',OUT]));v=next(s for s in probe['streams'] if s['codec_type']=='video')
assert v['nb_frames']=='126' and v['avg_frame_rate']=='24/1' and (v['width'],v['height'])==(720,1280)
assert not any(s['codec_type']=='audio' for s in probe['streams'])
run([FF,'-v','error','-i',OUT,'-f','null','-'])
qa=P/'qa';qa.mkdir(exist_ok=True)
run([FF,'-v','error','-y','-i',OUT,'-vf','select=not(mod(n\\,3))','-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
files=sorted(qa.glob('frame_*.jpg'));board=Image.new('RGB',(1470,3*398),'#f5f3ec');d=ImageDraw.Draw(board)
for j,k in enumerate(range(0,len(files),2)):
    im=Image.open(files[k]);im.thumbnail((206,366));x=j%7*210;y=j//7*398;board.paste(im,(x,y+25));d.text((x+2,y),f'{k*.125:.2f}s',font=font,fill='#233b46')
board.save(P/'whole_film_contact.jpg',quality=95)
# Same dissolve phase in both versions, not the same output timestamp.
board=Image.new('RGB',(7*210,2*398),'#f5f3ec');d=ImageDraw.Draw(board)
phase=[0,3,6,9,12,15,18]
for row,(path,start,label) in enumerate([(OLD,60,'v1'),(OUT,48,'v2')]):
    for col,k in enumerate(phase):
        f=qa/f'{label}_join_{k:02}.jpg'
        run([FF,'-v','error','-y','-i',path,'-vf',f'select=eq(n\\,{start+k})','-frames:v','1','-q:v','2',f])
        im=Image.open(f);im.thumbnail((206,366));x=col*210;y=row*398;board.paste(im,(x,y+25));d.text((x+2,y),f'{label} +{k}/24s',font=font,fill='#233b46')
board.save(P/'join_comparison.jpg',quality=95)
assert all(h(Path(p))==sha for p,sha in protected.items())
put('edit_receipt.json',{**plan,'status':'rendered_pending_visual_review','output':str(OUT.relative_to(ROOT)).replace('\\','/'),'output_sha256':h(OUT),'seconds':126/24,'width':720,'height':1280,'audio':False,'full_decode':True,'all_126_frames_encoded':True,'source_and_v1_hashes_preserved':True,'sample_frames_every':3,'user_film_acceptance':None,'publication_approval':None,'continuous_human_visual_review':False})
print(json.dumps({'output':str(OUT),'sha256':h(OUT),'seconds':5.25,'new_generations':0}))
