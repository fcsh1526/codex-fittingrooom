from pathlib import Path
import hashlib, json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
delivery=json.loads((ROOT/'10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8'))
def protect():
    for r in delivery['reels']: assert sha(ROOT/r['source_path'])==r['sha256']
protect()
sources=[];inputs=[]
for letter in ['A','B']:
    r=json.loads((OUT/f'{letter}_attempt_01/technical_receipt.json').read_text(encoding='utf-8'))
    p=ROOT/r['source_path'];assert sha(p)==r['sha256']
    inputs+=['-i',str(p)];sources.append({'path':r['source_path'],'sha256':r['sha256'],'interval_frames':[0,144]})
dest=OUT/'M03_turn_silhouette_parallel_v1.mp4'
assert not dest.exists()
graph=('[0:v]trim=start_frame=0:end_frame=144,settb=1/24,setpts=N,crop=408:1120:170:90,scale=344:944:flags=lanczos,pad=720:1280:12:168:color=0xeee9e1,setsar=1[left];'
       '[1:v]trim=start_frame=0:end_frame=144,settb=1/24,setpts=N,crop=408:1120:170:90,scale=344:944:flags=lanczos,setsar=1[right];'
       '[left][right]overlay=364:168:shortest=1,format=yuv420p[v]')
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-hide_banner','-loglevel','error',*inputs,'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-crf','18','-preset','medium','-r','24','-frames:v','144','-movflags','+faststart',str(dest)],check=True)
result=scan(dest)
assert result['decoded_frames']==144 and result['metadata']['size']==(720,1280) and result['metadata']['fps']==24
assert not result['black_candidate_frames']
qa=OUT/'qa';qa.mkdir(exist_ok=True)
indices=np.linspace(0,143,25,dtype=int).tolist()
board=Image.new('RGB',(1080,2040),'white');d=ImageDraw.Draw(board)
bounds=Image.new('RGB',(12*180,12*344),'white');bd=ImageDraw.Draw(bounds)
reader=imageio_ffmpeg.read_frames(str(dest));next(reader)
for i,data in enumerate(reader):
    frame=Image.frombytes('RGB',(720,1280),data)
    if i in indices:
        frame.save(qa/f'frame_{i:03d}.png')
        n=indices.index(i);x=n%5*216;y=n//5*408
        d.text((x+3,y+3),f'{i/24:.2f}s / f{i}',fill='black')
        board.paste(frame.resize((216,384),Image.Resampling.LANCZOS),(x,y+24))
    x=i%12*180;y=i//12*344
    bd.text((x+3,y+3),str(i),fill='black')
    bounds.paste(frame.resize((180,320),Image.Resampling.LANCZOS),(x,y+24))
board.save(qa/'whole_25.jpg',quality=95)
# Split consecutive bound samples into three manageable boards.
for j in range(3): bounds.crop((0,j*4*344,2160,(j+1)*4*344)).save(qa/f'bounds_{j:02d}.jpg',quality=95)
protect()
receipt={'status':'technical_complete_visual_review_pending','output':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),'sources':sources,'crop_xywh':[170,90,408,1120],'panel_wh':[344,944],'left_xy':[12,168],'right_xy':[364,168],'scan':result,'source_timing':'output n reads source n, native24fps; independent gestures retained','new_generation':True,'text':False,'audio':False,'internal_cut':False,'protected_five_films_sha256_match':True,'continuous_playback':False,'user_approval':None,'drive_write':False,'published':False}
(OUT/'composition_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(dest),'seconds':result['decoded_seconds'],'frames':result['decoded_frames']},ensure_ascii=False))
