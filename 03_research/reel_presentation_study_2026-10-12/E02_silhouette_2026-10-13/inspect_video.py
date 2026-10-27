from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

folder=OUT/sys.argv[1]
source=folder/('source.mp4' if len(sys.argv)<3 else sys.argv[2])
result=scan(source)
w,h=result['metadata']['size'];fps=result['metadata']['fps'];n=result['decoded_frames']
qa=folder/'qa';qa.mkdir(exist_ok=True)
indices=sorted(set(np.linspace(0,n-1,25,dtype=int).tolist()))
face_indices=sorted(set(np.linspace(0,n-1,5,dtype=int).tolist()))
whole=Image.new('RGB',(1000,1900),'white');draw=ImageDraw.Draw(whole)
faces=Image.new('RGB',(5*420,474),'white');fd=ImageDraw.Draw(faces)
boards={}
reader=imageio_ffmpeg.read_frames(str(source));next(reader)
for i,data in enumerate(reader):
    frame=Image.frombytes('RGB',(w,h),data)
    if i in indices:
        k=indices.index(i);x=k%5*200;y=k//5*380
        draw.text((x+3,y+3),f'{i/fps:.2f}s / f{i}',fill='black')
        whole.paste(frame.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
        frame.save(qa/f'frame_{i:03d}.png')
    if i in face_indices:
        k=face_indices.index(i)
        crop=frame.crop((int(w*.20),int(h*.05),int(w*.80),int(h*.40)))
        faces.paste(crop.resize((420,448),Image.Resampling.LANCZOS),(k*420,24))
        fd.text((k*420+3,3),f'{i/fps:.2f}s / f{i}',fill='black')
    block=i//48;k=i%48
    if block not in boards:boards[block]=Image.new('RGB',(1280,6*309),'white')
    board=boards[block];x=k%8*160;y=k//8*309
    ImageDraw.Draw(board).text((x+3,y+3),str(i),fill='black')
    board.paste(frame.resize((160,285),Image.Resampling.LANCZOS),(x,y+24))
whole.save(qa/'whole_25.jpg',quality=95)
faces.save(qa/'face_5.jpg',quality=95)
for block,board in boards.items():board.save(qa/f'all_{block:02d}.jpg',quality=95)
receipt={'source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scan':result,'whole_sample_frames':indices,'face_sample_frames':face_indices,'all_frame_thumbnails_exported':n,'visual_review':'pending','assistant_continuous_playback':False,'user_film_approval':None}
(folder/'technical_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':n,'fps':fps,'seconds':result['decoded_seconds'],'size':[w,h]},ensure_ascii=True))
