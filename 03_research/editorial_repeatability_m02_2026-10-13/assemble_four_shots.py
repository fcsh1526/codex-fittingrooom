from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
full_root=ROOT/'10_automation/runs/2026-W41/reels/M02'
specs=[('S1','2026-W41-003-L01',full_root/'A_attempt_01/source.mp4',0,60,'571c5ddc0ef77f47d21efabc385fdac0c405680dde8ad511c449ced50c36b437'),
 ('S2','2026-W41-003-L01',BASE/'L01_motion_attempt_01/source.mp4',0,108,read(BASE/'L01_motion_attempt_01/technical_receipt.json')['sha256']),
 ('S3','2026-W41-003-L02',BASE/'L02_motion_attempt_01/source.mp4',0,108,read(BASE/'L02_motion_attempt_01/technical_receipt.json')['sha256']),
 ('S4','2026-W41-003-L02',full_root/'B_attempt_01/source.mp4',24,108,'7924c288d65aacf9ce831d14787e95c349441a5e4ae5229510dff3155125e0c5')]
sources=[];filters=[]
for i,(name,look,p,start,end,expected) in enumerate(specs):
 assert sha(p)==expected
 technical=scan(p);assert technical['metadata']['fps']==24 and list(technical['metadata']['size'])==[720,1280] and end<=technical['decoded_frames']
 if i in [1,2]:
  approval=read(BASE/('L01_seated_user_approval.json' if i==1 else 'L02_seated_user_approval.json'));assert sha(ROOT/approval['file'])==approval['sha256']
  approval_path=(BASE/('L01_seated_user_approval.json' if i==1 else 'L02_seated_user_approval.json')).relative_to(ROOT).as_posix()
 else: approval_path='10_automation/runs/2026-W41/reels/M02_full_pair_user_approval_2026-10-08.json'
 sources.append({'shot':name,'look_id':look,'file':p.relative_to(ROOT).as_posix(),'sha256':expected,'frames_end_exclusive':[start,end],'seconds':[start/24,end/24],'still_approval':approval_path,'reused_original':i in [0,3]})
 filters.append(f'[{i}:v]trim=start_frame={start}:end_frame={end},settb=1/24,setpts=N,format=yuv420p,fps=24[s{i}]')
counts=[end-start for _,_,_,start,end,_ in specs];joins=[];merged=counts[0];previous='s0'
for i in range(1,4):
 start=merged-18;label=f'x{i}';filters.append(f'[{previous}][s{i}]xfade=transition=fade:duration=0.75:offset={start/24}[{label}]')
 joins.append({'from':f'S{i}','to':f'S{i+1}','type':'cross_dissolve','start_frame':start,'end_frame_exclusive':merged,'start_seconds':start/24,'end_seconds':merged/24,'seconds':0.75,'frames':18})
 merged+=counts[i]-18;previous=label
filters.append(f'[{previous}]format=yuv420p[v]')
dest=BASE/'four_shot_review_v1';dest.mkdir(exist_ok=True);video=dest/'M02_cafe_pause_two_looks_trial_v1.mp4';assert not video.exists()
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe();cmd=[ffmpeg,'-hide_banner']
for source in sources:cmd+=['-i',str(ROOT/source['file'])]
cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','24','-frames:v',str(merged),'-movflags','+faststart',str(video)]
render=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace');(dest/'render_log.txt').write_text(render.stderr,encoding='utf-8');render.check_returncode()
result=scan(video);assert result['decoded_frames']==merged and not result['black_candidate_frames']
probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(video)],capture_output=True,text=True,encoding='utf-8',errors='replace');assert 'Audio:' not in probe.stderr
qa=dest/'join_qa';qa.mkdir(exist_ok=True);boards=[]
for j in joins:
 indices=list(range(j['start_frame']-2,j['end_frame_exclusive']+3));board=Image.new('RGB',(1200,1520),'white');boards.append((indices,board,ImageDraw.Draw(board),j))
reader=imageio_ffmpeg.read_frames(str(video));next(reader)
for i,data in enumerate(reader):
 hits=[entry for entry in boards if i in entry[0]]
 if not hits:continue
 frame=Image.frombytes('RGB',(720,1280),data)
 for indices,board,draw,j in hits:
  k=indices.index(i);x=k%6*200;y=k//6*380;draw.text((x+3,y+3),f'{i/24:.3f}s f{i}',fill='black');board.paste(frame.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
  if i in [j['start_frame'],j['start_frame']+9,j['end_frame_exclusive']-1,j['end_frame_exclusive']]:frame.save(qa/f"{j['from']}_{j['to']}_{i:03d}.png")
for indices,board,draw,j in boards:board.save(qa/f"{j['from']}_{j['to']}_all.jpg",quality=95)
protected=[]
for row in read(ROOT/'10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json')['reels']:
 actual=sha(ROOT/row['source_path']);assert actual==row['sha256'];protected.append({'model':row['model'],'sha256':actual,'unchanged':True})
save(BASE/'four_shot_edit_receipt.json',{'status':'exported_visual_review_pending','file':video.relative_to(ROOT).as_posix(),'sha256':sha(video),'scan':result,'scope':'Independent one-model M02 and both W41-003 looks research candidate. Original publishing movies preserved.','sources':sources,'transitions':joins,'editing':'Original24fps speed; source interval trims only; no text/audio/crop/zoom/freeze/retime.','timing_reason':'4.5s per seated source keeps the attention change and near-frontal return; actual12.75s replaces provisional11.25s budget.','unoverlapped_reading_seconds':{'S1':1.75,'S2':3,'S3':3,'S4':2.75},'assistant_continuous_playback':False,'user_film_approval':None,'protected_w41_delivery':protected,'drive_uploaded':False,'research_cost':{'new_still_calls':4,'by_look':{'L01':3,'L02':1},'confirmed_new_grok_results':2,'reused_full_stills':2,'reused_original_clips':2,'active_minutes':None,'pure_generation_wait_minutes':None,'user_approval_wait_minutes':None,'note':'Incremental transfer trial, not from-zero or proven efficiency.'}})
print(json.dumps({'frames':merged,'seconds':merged/24,'joins':[(j['start_seconds'],j['end_seconds']) for j in joins],'protected_originals':len(protected)}))
