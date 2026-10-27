from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan
folder=OUT/sys.argv[1];src=folder/'source.mp4'
result=scan(src);w,h=result['metadata']['size'];n=result['decoded_frames'];fps=result['metadata']['fps']
assert (w,h)==(720,1280) and fps==24 and n>=240
qa=folder/'qa';qa.mkdir(exist_ok=True)
indices=np.linspace(0,n-1,25,dtype=int).tolist()
whole=Image.new('RGB',(1000,1900),'white');d=ImageDraw.Draw(whole)
boards={};reader=imageio_ffmpeg.read_frames(str(src));next(reader)
for i,data in enumerate(reader):
    frame=Image.frombytes('RGB',(w,h),data)
    if i in indices:
        k=indices.index(i);x=k%5*200;y=k//5*380
        d.text((x+3,y+3),f'{i/fps:.2f}s / f{i}',fill='black')
        whole.paste(frame.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
        frame.save(qa/f'frame_{i:03d}.png')
    block=i//48;k=i%48
    if block not in boards: boards[block]=Image.new('RGB',(1280,6*309),'white')
    b=boards[block];bd=ImageDraw.Draw(b);x=k%8*160;y=k//8*309
    bd.text((x+3,y+3),str(i),fill='black');b.paste(frame.resize((160,285),Image.Resampling.LANCZOS),(x,y+24))
whole.save(qa/'whole_25.jpg',quality=95)
for j,b in boards.items(): b.save(qa/f'all_{j:02d}.jpg',quality=95)
faces=Image.new('RGB',(5*420,464),'white');fd=ImageDraw.Draw(faces)
for k,j in enumerate([0,6,12,18,24]):
    i=indices[j];frame=Image.open(qa/f'frame_{i:03d}.png')
    faces.paste(frame.crop((150,60,570,500)),(k*420,24));fd.text((k*420+3,3),f'{i/fps:.2f}s',fill='black')
faces.save(qa/'face_5.jpg',quality=95)
receipt={'source':src.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scan':result,'whole_sample_frames':indices,'all_frame_thumbnails_exported':n,'visual_review':'pending','continuous_playback':False,'user_film_approval':None}
(folder/'technical_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':n,'seconds':result['decoded_seconds'],'source':str(src),'sha256':receipt['sha256']},ensure_ascii=False))
