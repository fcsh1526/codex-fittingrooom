"""One composited shot from two full continuous native sources; no edit joins."""
import hashlib,json,sys,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent;ROOT=B.parents[5];P=B/'paired_review_v1';P.mkdir(exist_ok=True)
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args):
 r=subprocess.run([str(a) for a in args],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-3000:])
 return r.stdout
src=[B/'L01_trial_01/source.mp4',B/'L02_trial_01/source.mp4'];expected=['9fdca42aa8a3141601c8ab9c262f0d13c5c5432b0de12b4bcd1d8f5d146c511b','6ce2f27eaf5db550e27da1da1a7a8284ce4b347670e1cc2d6ef37b13a520d1e0']
assert [h(s) for s in src]==expected
plan={'date':'2026-11-05','layout':'A parallel','viewer_purpose':'Same navy blazer with formal dark trousers/loafers versus light skirt/sneakers, natural response to photographer and one turn.','shot_count':1,'panel_source_frames':{'left':[0,145],'right':[0,145]},'source_sha256':expected,'crop_each_source':[160,0,400,1280],'panel_width':356,'gutter':8,'scale_each':356/400,'fps':24,'frames':145,'seconds':145/24,'native_speed':True,'internal_joins':[],'transition_note':'No temporal shot cut exists: two continuous panels for the whole film. Existing0.75s rule remains for actual joins; not replaced with a hard cut.','baked_text':False,'audio':False,'new_still_calls':0,'new_source_jobs':2,'no_freeze_repeat_reverse_retime_or_flow':True,'user_film_acceptance':None,'publication_approval':None}
put('edit_plan.json',plan)
chains=[]
for i,tag in enumerate(['l','r']):chains.append(f'[{i}:v:0]crop=400:1280:160:0,scale=356:-2,pad=356:1280:0:(oh-ih)/2:color=0xf1eee6,setsar=1[{tag}]')
chains.append('[l][r]xstack=inputs=2:layout=0_0|364_0:fill=0xf1eee6,format=yuv420p[out]')
out=P/'M03_W45_natural_parallel_review_v1.mp4'
run([FF,'-v','error','-y','-i',src[0],'-i',src[1],'-filter_complex',';'.join(chains),'-map','[out]','-c:v','libx264','-preset','fast','-crf','18','-an','-frames:v','145','-map_metadata','-1','-movflags','+faststart',out])
pr=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',out]));v=next(s for s in pr['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))==(720,1280,'24/1',145)
assert not any(s['codec_type']=='audio' for s in pr['streams']);run([FF,'-v','error','-i',out,'-f','null','-'])
qa=P/'qa';qa.mkdir(exist_ok=True);run([FF,'-v','error','-y','-i',out,'-vf','select=not(mod(n\\,3))','-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
files=sorted(qa.glob('frame_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
for name,indices in [('whole_film_contact',list(range(0,len(files),4))),('motion_contact',list(range(0,len(files),2)))]:
 board=Image.new('RGB',(1470,((len(indices)+6)//7)*398),'#f5f3ec');d=ImageDraw.Draw(board)
 for j,k in enumerate(indices):
  im=Image.open(files[k]);im.thumbnail((206,366));x=j%7*210;y=j//7*398;board.paste(im,(x,y+25));d.text((x+2,y),f'{k*.125:.3f}s',font=font,fill='#233b46')
 board.save(P/(name+'.jpg'),quality=95)
assert [h(s) for s in src]==expected
put('edit_receipt.json',{**plan,'status':'candidate_pending_visual_and_user_review','output_path':str(out.relative_to(ROOT)).replace('\\','/'),'output_sha256':h(out),'width':720,'height':1280,'full_decode':True,'source_files_unchanged':True,'sample_frames_every':3,'whole_board_samples':13,'motion_board_samples':25,'continuous_human_native_speed_review':False})
print(json.dumps({'output':str(out),'sha256':h(out),'seconds':145/24,'internal_joins':0,'sources_preserved':True}))
