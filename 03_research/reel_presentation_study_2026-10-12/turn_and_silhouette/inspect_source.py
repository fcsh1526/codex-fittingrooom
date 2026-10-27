from pathlib import Path
import hashlib, json, sys
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
letter=sys.argv[1]
folder=OUT/f'{letter}_attempt_01'
src=folder/'source.mp4'
result=scan(src)
w,h=result['metadata']['size'];n=result['decoded_frames']
assert (w,h)==(720,1280) and n>=144 and result['metadata']['fps']==24
qa=folder/'qa';qa.mkdir(exist_ok=True)
indices=np.linspace(0,n-1,25,dtype=int).tolist()
board=Image.new('RGB',(1000,5*380),'white');draw=ImageDraw.Draw(board)
feet=[]
reader=imageio_ffmpeg.read_frames(str(src));next(reader)
for i,data in enumerate(reader):
    frame=Image.frombytes('RGB',(w,h),data)
    if i in indices:
        k=indices.index(i);x=k%5*200;y=k//5*380
        draw.text((x+3,y+3),f'{i/24:.2f}s / f{i}',fill='black')
        board.paste(frame.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
        frame.save(qa/f'frame_{i:03d}.png')
    feet.append(frame.crop((160,840,570,1240)))
board.save(qa/'whole_25.jpg',quality=95)
for start in range(0,n,48):
    footboard=Image.new('RGB',(8*160,6*180),'white');dd=ImageDraw.Draw(footboard)
    for j in range(start,min(start+48,n)):
        k=j-start;x=k%8*160;y=k//8*180
        dd.text((x+3,y+3),str(j),fill='black')
        footboard.paste(feet[j].resize((160,156),Image.Resampling.LANCZOS),(x,y+24))
    footboard.save(qa/f'feet_{start//48:02d}.jpg',quality=95)
faceboard=Image.new('RGB',(350*5,374),'white')
fd=ImageDraw.Draw(faceboard)
for k,i in enumerate([indices[j] for j in [0,6,12,18,24]]):
    frame=Image.open(qa/f'frame_{i:03d}.png')
    faceboard.paste(frame.crop((210,100,560,450)),(k*350,24))
    fd.text((k*350+3,3),f'{i/24:.2f}s / f{i}',fill='black')
faceboard.save(qa/'face_5.jpg',quality=95)
receipt={'source_path':src.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scan':result,'whole_sample_frames':indices,'feet_frames_exported':list(range(n)),'visual_review':'pending; decoded/exported images do not imply inspected','continuous_playback':False,'user_approval':None}
(folder/'technical_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'letter':letter,'frames':n,'duration':result['decoded_seconds'],'sha256':receipt['sha256']},ensure_ascii=False))
