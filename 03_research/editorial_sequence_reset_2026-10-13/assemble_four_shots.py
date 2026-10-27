from pathlib import Path
import hashlib, json, subprocess, sys
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]; BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

counts=[int(n) for n in sys.argv[1:5]]
assert len(counts)==4 and all(n>36 for n in counts)
shots=['A1','A2','B1','B2']; sources=[]
for name,n in zip(shots,counts):
    source=BASE/f'{name}_motion_attempt_01/source.mp4'
    qa=read(source.parent/'technical_receipt.json')
    approval=read(BASE/f'{name}_user_approval_2026-10-13.json')
    assert sha(source)==qa['sha256'] and sha(ROOT/approval['file'])==approval['sha256']
    assert n<=qa['scan']['decoded_frames']
    assert qa['scan']['metadata']['fps']==24 and qa['scan']['metadata']['size']==[720,1280]
    sources.append({'shot':name,'look_id':'2026-W41-004-L01' if name.startswith('A') else '2026-W41-004-L02','file':source.relative_to(ROOT).as_posix(),'sha256':sha(source),'frames':[0,n],'end_exclusive':True,'seconds':[0,n/24],'still_approval':approval,'browser_receipt':(source.parent/'browser_receipt.json').relative_to(ROOT).as_posix(),'technical_receipt':(source.parent/'technical_receipt.json').relative_to(ROOT).as_posix()})

dest=BASE/'four_shot_review_v1';dest.mkdir(exist_ok=True)
video=dest/'M03_lunch_outing_two_looks_trial_v1.mp4'
assert not video.exists(),'Never overwrite an existing export.'
filters=[]
for i,n in enumerate(counts):filters.append(f'[{i}:v]trim=end_frame={n},settb=1/24,setpts=N,format=yuv420p,fps=24[s{i}]')
joins=[]; merged=counts[0]; previous='s0'
for i in range(1,4):
    start=merged-18;label=f'x{i}'
    filters.append(f'[{previous}][s{i}]xfade=transition=fade:duration=0.75:offset={start/24}[{label}]')
    joins.append({'from':shots[i-1],'to':shots[i],'type':'cross_dissolve','start_frame':start,'end_frame_exclusive':merged,'start_seconds':start/24,'end_seconds':merged/24,'seconds':0.75,'frames':18})
    merged+=counts[i]-18;previous=label
filters.append(f'[{previous}]format=yuv420p[v]')
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe();cmd=[ffmpeg,'-hide_banner']
for source in sources:cmd+=['-i',str(ROOT/source['file'])]
cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','24','-frames:v',str(merged),'-movflags','+faststart',str(video)]
render=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
(dest/'render_log.txt').write_text(render.stderr,encoding='utf-8');render.check_returncode()
result=scan(video);assert result['decoded_frames']==merged and not result['black_candidate_frames']
probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(video)],capture_output=True,text=True,encoding='utf-8',errors='replace');assert 'Audio:' not in probe.stderr

qa_dir=dest/'join_qa';qa_dir.mkdir(exist_ok=True)
boards=[]
for j in joins:
    indices=list(range(j['start_frame']-2,j['end_frame_exclusive']+3))
    board=Image.new('RGB',(1200,380*4),'white')
    boards.append((indices,board,ImageDraw.Draw(board),j))
reader=imageio_ffmpeg.read_frames(str(video));next(reader)
for i,data in enumerate(reader):
    hits=[entry for entry in boards if i in entry[0]]
    if not hits:continue
    frame=Image.frombytes('RGB',(720,1280),data)
    for indices,board,draw,j in hits:
        k=indices.index(i);x=k%6*200;y=k//6*380
        draw.text((x+3,y+3),f'{i/24:.3f}s / f{i}',fill='black')
        board.paste(frame.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
        if i in [j['start_frame'],j['start_frame']+9,j['end_frame_exclusive']-1,j['end_frame_exclusive']]:frame.save(qa_dir/f"{j['from']}_{j['to']}_{i:03d}.png")
for indices,board,draw,j in boards:board.save(qa_dir/f"{j['from']}_{j['to']}_all.jpg",quality=95)

delivery=read(ROOT/'10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json');protected=[]
for row in delivery['reels']:
    actual=sha(ROOT/row['source_path']);assert actual==row['sha256']
    protected.append({'model':row['model'],'sha256':actual,'unchanged':True})
save(BASE/'four_shot_edit_receipt.json',{'status':'exported_frame_review_pending','file':video.relative_to(ROOT).as_posix(),'sha256':sha(video),'scan':result,'scope':'Separate M03 same-day lunch-story research candidate with exactly one model and both W41-004 looks. Not approved weekly replacement; Carousel and full production package incomplete.','sources':sources,'transitions':joins,'editing':'Original24fps speed; tail trims only; no text/audio/crop/zoom/freeze/retime.','assistant_continuous_playback':False,'user_film_approval':None,'first_look_direction_approval':'first_look_direction_acceptance_2026-10-13.json','protected_w41_delivery':protected,'drive_uploaded':False})
print(json.dumps({'frames':merged,'seconds':merged/24,'joins':[(j['start_seconds'],j['end_seconds']) for j in joins],'protected_originals':len(protected)}))
