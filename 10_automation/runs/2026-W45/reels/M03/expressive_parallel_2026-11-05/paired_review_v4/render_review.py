"""Complementary native-speed selections, staggered joins, no new provider generation."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;BR=P.parent;ROOT=BR.parents[5]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
L=BR/'trial_02/source.mp4';R=BR/'L02_trial_01/source.mp4'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args):
    r=subprocess.run([str(a) for a in args],capture_output=True)
    if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-4000:])
    return r.stdout
assert h(L)=='533f789b3aab103573af3270f545aa3834a2e483805306659ff6a4fef009c3e2'
assert h(R)=='13b4f38ca17ddd2e0495775753d6ed1eb02db2bc0ed73496ebc9a98d0aa436fe'
panels=[{'tag':'l','intervals':[[126,192],[0,48]],'join':[48,66]}, {'tag':'r','intervals':[[180,210],[0,84]],'join':[12,30]}]
plan={'date':'2026-11-05','status':'prepared','viewer_purpose':'Compare navy blazer with work trousers/loafers versus cream skirt/sneakers.','performance':'Playful outfit display addressed to lens. Left shows side/back, bent knee, then waist/hip poses; right shows side-to-front return and skirt movement, then waist/hip poses.','layout_choice_receipt':str((BR/'paired_review_v1/user_layout_preference_2026-11-05.json').relative_to(ROOT)).replace('\\','/'),'panels':panels,'crop_each':[100,0,520,1280],'panel_width':356,'gutter':8,'fps':24,'frames':96,'seconds':4,'overlap_frames_each':18,'scale_each':356/520,'native_speed':True,'new_stills':0,'new_video_jobs':0,'no_freeze_duplicate_reverse_or_warp':True,'known_tradeoff':'Shorter4s edit; full rear skirt turn and high V excluded for narrow-column layout, preserved in sources. Staggered panel dissolves retain one clear outfit panel throughout each join. Not motion-physics repair.'}
put('edit_plan.json',plan)
chains=[]
for i,p in enumerate(panels):
    t=p['tag'];a,b=p['intervals'];offset=p['join'][0]/24
    chains += [f'[{i}:v:0]split=2[{t}a][{t}b]',f'[{t}a]trim=start_frame={a[0]}:end_frame={a[1]},setpts=PTS-STARTPTS,fps=24,settb=1/24[{t}1]',f'[{t}b]trim=start_frame={b[0]}:end_frame={b[1]},setpts=PTS-STARTPTS,fps=24,settb=1/24[{t}2]',f'[{t}1][{t}2]xfade=transition=fade:duration=0.75:offset={offset},trim=end_frame=96,crop=520:1280:100:0,scale=356:-2,pad=356:1280:0:(oh-ih)/2:color=0xf1eee6,setsar=1[{t}out]']
chains+=['[lout][rout]xstack=inputs=2:layout=0_0|364_0:fill=0xf1eee6,format=yuv420p[out]']
OUT=P/'M03_W45_parallel_selected_review_v4.mp4'
run([FF,'-v','error','-y','-i',L,'-i',R,'-filter_complex',';'.join(chains),'-map','[out]','-frames:v','96','-c:v','libx264','-crf','18','-preset','fast','-an','-map_metadata','-1','-movflags','+faststart',OUT])
probe=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',OUT]));v=next(s for s in probe['streams'] if s['codec_type']=='video')
assert v['nb_frames']=='96' and v['avg_frame_rate']=='24/1' and (v['width'],v['height'])==(720,1280)
assert not any(s['codec_type']=='audio' for s in probe['streams'])
run([FF,'-v','error','-i',OUT,'-f','null','-'])
qa=P/'qa';qa.mkdir(exist_ok=True)
# All frames for exact join/boundary inspection, no claim of uninterrupted watching.
run([FF,'-v','error','-y','-i',OUT,'-q:v','2',qa/'frame_%03d.jpg'])
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
for name,indices in [('whole_film_contact',list(range(0,96,6))),('boundary_contact',[0,6,12,15,18,21,24,27,30,36,42,48,51,54,57,60,63,66,72,78,84,90,95])]:
    board=Image.new('RGB',(1470,((len(indices)+6)//7)*398),'#f5f3ec');d=ImageDraw.Draw(board)
    for j,n in enumerate(indices):
        im=Image.open(qa/f'frame_{n+1:03}.jpg');im.thumbnail((206,366));x=j%7*210;y=j//7*398;board.paste(im,(x,y+25));d.text((x+2,y),f'f{n} {n/24:.3f}s',font=font,fill='#233b46')
    board.save(P/(name+'.jpg'),quality=95)
put('edit_receipt.json',{**plan,'status':'rendered_pending_visual_review','output':str(OUT.relative_to(ROOT)).replace('\\','/'),'output_sha256':h(OUT),'source_left_sha256':h(L),'source_right_sha256':h(R),'width':720,'height':1280,'audio':False,'full_decode':True,'all_frames_extracted':96,'continuous_human_native_speed_review':False,'user_film_acceptance':None,'publication_approval':None})
print(json.dumps({'output':str(OUT),'sha256':h(OUT),'seconds':4,'new_generation':False}))
