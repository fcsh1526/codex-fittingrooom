from pathlib import Path
import hashlib, json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
sys.path.insert(0, str(ROOT / '10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
plan = json.loads((OUT / 'storyboard.json').read_text(encoding='utf-8'))
source_record = json.loads((ROOT / '10_automation/runs/2026-W41/reels/M03/review_v1/composition_receipt.json').read_text(encoding='utf-8'))
delivery = json.loads((ROOT / '10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def protect():
    for r in delivery['reels']:
        assert sha(ROOT / r['source_path']) == r['sha256']
protect()
inputs=[]
for source in source_record['sources']:
    p = ROOT / source['path']
    assert sha(p) == source['sha256']
    inputs += ['-i',str(p)]
dest = OUT / 'M03_light_dark_parallel_trial_v2.mp4'
assert not dest.exists(), 'Preserve earlier trial exports'
x,y,w,h = plan['main_crop_xywh']
pw,ph = plan['panel_wh']
lx,ly = plan['left_xy']; rx,ry = plan['right_xy']
graph = (
    f'[0:v]trim=start_frame=0:end_frame=144,settb=1/24,setpts=N,crop={w}:{h}:{x}:{y},scale={pw}:{ph}:flags=lanczos,pad=720:1280:{lx}:{ly}:color=0xeee9e1,setsar=1[left];'
    f'[1:v]trim=start_frame=0:end_frame=144,settb=1/24,setpts=N,crop={w}:{h}:{x}:{y},scale={pw}:{ph}:flags=lanczos,setsar=1[right];'
    f'[left][right]overlay={rx}:{ry}:shortest=1,format=yuv420p[v]'
)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ffmpeg,'-hide_banner','-loglevel','error',*inputs,'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-crf','18','-preset','medium','-r','24','-frames:v','144','-movflags','+faststart',str(dest)],check=True)
result=scan(dest)
assert result['decoded_frames']==144 and result['metadata']['size']==(720,1280) and result['metadata']['fps']==24
assert not result['black_candidate_frames']
qa=OUT/'qa';qa.mkdir(exist_ok=True)
indices=np.linspace(0,143,25,dtype=int).tolist()
reader=imageio_ffmpeg.read_frames(str(dest));next(reader)
board=Image.new('RGB',(1080,5*408),'white');draw=ImageDraw.Draw(board)
for i,data in enumerate(reader):
    if i in indices:
        frame=Image.frombytes('RGB',(720,1280),data)
        frame.save(qa/f'frame_{i:03d}.png')
        n=indices.index(i);bx=n%5*216;by=n//5*408
        draw.text((bx+3,by+3),f'{i/24:.2f}s / f{i}',fill='black')
        board.paste(frame.resize((216,384),Image.Resampling.LANCZOS),(bx,by+24))
board.save(qa/'whole_25.jpg',quality=95)
protect()
receipt={'status':'technical_complete_sampled_review_pending','output':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),'source_records':source_record['sources'],'composition':plan,'scan':result,'source_timing':'output frame n reads frame n from each original source; no forced gesture synchronization','protected_five_films_sha256_match':True,'new_generation':False,'assistant_continuous_playback':False,'user_trial_approval':None,'drive_write':False,'published':False}
(OUT/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(dest),'seconds':result['decoded_seconds'],'frames':result['decoded_frames'],'qa':str(qa/'whole_25.jpg')},ensure_ascii=False))
