"""Native-speed editorial variants; never overwrite accepted source media."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;BR=P.parent;ROOT=BR.parents[5]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
A=BR/'trial_02/source.mp4';B=BR/'L02_trial_01/source.mp4'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):
 r=subprocess.run(list(map(str,args)),capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-5000:])
 return r
def put(name,v):(P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert h(A)=='533f789b3aab103573af3270f545aa3834a2e483805306659ff6a4fef009c3e2'
assert h(B)=='13b4f38ca17ddd2e0495775753d6ed1eb02db2bc0ed73496ebc9a98d0aa436fe'
common=[FF,'-v','error','-y','-i',A,'-i',B]
filterA=';'.join([
'[0:v:0]fps=24,split=2[la][lb]','[1:v:0]fps=24,split=2[ra][rb]',
'[la]trim=start_frame=0:end_frame=78,setpts=PTS-STARTPTS,fps=24,settb=1/24[l1]',
'[lb]trim=start_frame=126:end_frame=192,setpts=PTS-STARTPTS,fps=24,settb=1/24[l2]',
'[ra]trim=start_frame=0:end_frame=78,setpts=PTS-STARTPTS,fps=24,settb=1/24[r1]',
'[rb]trim=start_frame=144:end_frame=210,setpts=PTS-STARTPTS,fps=24,settb=1/24[r2]',
'[l1][l2]xfade=transition=fade:duration=0.75:offset=2.5,trim=end_frame=126,crop=450:1280:135:0,scale=356:-2,pad=356:1280:0:(oh-ih)/2:color=0xf1eee6,setsar=1[L]',
'[r1][r2]xfade=transition=fade:duration=0.75:offset=2.5,trim=end_frame=126,crop=450:1280:135:0,scale=356:-2,pad=356:1280:0:(oh-ih)/2:color=0xf1eee6,setsar=1[R]',
'[L][R]xstack=inputs=2:layout=0_0|364_0:fill=0xf1eee6,format=yuv420p[out]'])
enc=['-map','[out]','-c:v','libx264','-preset','fast','-crf','18','-an','-map_metadata','-1','-movflags','+faststart']
paired=P/'M03_W45_parallel_selected_review_v1.mp4'
run(common+['-filter_complex',filterA]+enc+['-frames:v','126',paired])
filterB='[0:v:0]setpts=PTS-STARTPTS,fps=24,settb=1/24[a];[1:v:0]setpts=PTS-STARTPTS,fps=24,settb=1/24[b];[a][b]xfade=transition=fade:duration=0.75:offset=9.2916666667,trim=end_frame=464,setsar=1,format=yuv420p[out]'
sequential=P/'M03_W45_full_frame_sequence_review_v1.mp4'
run(common+['-filter_complex',filterB]+enc+['-frames:v','464',sequential])
outputs=[]
for path,expected in [(paired,126),(sequential,464)]:
 probe=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',path]).stdout)
 v=next(x for x in probe['streams'] if x['codec_type']=='video');assert int(v['nb_frames'])==expected and v['avg_frame_rate']=='24/1'
 assert not any(x['codec_type']=='audio' for x in probe['streams'])
 run([FF,'-v','error','-i',path,'-f','null','-'])
 qa=P/(path.stem+'_qa');qa.mkdir(exist_ok=True)
 run([FF,'-v','error','-y','-i',path,'-vf',"select=not(mod(n\\,6))",'-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
 files=sorted(qa.glob('*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
 selected=list(range(len(files))) if expected==126 else list(range(0,len(files),4))
 cols=7;rows=(len(selected)+cols-1)//cols;board=Image.new('RGB',(1470,rows*398),'#f5f3ec');d=ImageDraw.Draw(board)
 for j,k in enumerate(selected):
  x=j%cols*210;y=j//cols*398;im=Image.open(files[k]);im.thumbnail((206,366));board.paste(im,(x,y+25));d.text((x+2,y),f'{k*.25:.2f}s',font=font,fill='#233b46')
 board.save(P/(path.stem+'_contact.jpg'),quality=94)
 outputs.append({'path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':h(path),'fps':24,'frames':expected,'seconds':expected/24,'width':720,'height':1280,'audio':False,'full_decode':True,'contact_samples':len(selected)})
put('edit_receipt.json',{'date':'2026-11-05','status':'review_candidates_not_user_accepted','source_left':{'path':str(A.relative_to(ROOT)).replace('\\','/'),'sha256':h(A),'user_acceptance_scope':'exact source performance; not final layout or publication'},'source_right':{'path':str(B.relative_to(ROOT)).replace('\\','/'),'sha256':h(B),'user_acceptance':None},'A':{'left_source_frames':[[0,78],[126,192]],'right_source_frames':[[0,78],[144,210]],'output_transition_frames':[60,78],'overlap_frames':18,'crop_each_source':[135,0,450,1280],'panel_size':[356,1280],'gutter':8,'scale_each':356/450,'rationale':'Select waist, side-turn, knee and skirt movement that fit the narrow columns. High V and broad palms remain in full sources and variantB; this is editorial selection, not a motion-defect repair.'},'B':{'left_source_frames':[0,241],'right_source_frames':[0,241],'output_transition_frames':[223,241],'overlap_frames':18,'scale_each':1,'rationale':'Optional alternate layout preserves full performance and larger figures. Not silently substituted for original parallel intent.'},'outputs':outputs,'native_speed':True,'no_freeze_duplicate_reverse_or_retime':True,'baked_text':False,'uninterrupted_human_visual_review':False,'user_film_acceptance':None,'publication_approval':None})
print(json.dumps({'outputs':outputs,'source_hashes_preserved':True}))
