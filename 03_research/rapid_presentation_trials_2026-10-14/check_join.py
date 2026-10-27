from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw
base=Path(__file__).resolve().parent
root=base.parents[1]
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
folder=base/'joined_review_v1'
reader=imageio_ffmpeg.read_frames(str(folder/'M04_blue_bag_viewing_route_v1.mp4'))
meta=next(reader)
indices=list(range(159,184))
board=Image.new('RGB',(1000,1900),'white')
draw=ImageDraw.Draw(board)
for i,data in enumerate(reader):
    if i in indices:
        k=indices.index(i);x=k%5*200;y=k//5*380
        im=Image.frombytes('RGB',tuple(meta['size']),data)
        board.paste(im.resize((200,356),Image.Resampling.LANCZOS),(x,y+24))
        draw.text((x+3,y+3),f'{i/meta["fps"]:.3f}s f{i}',fill='black')
    if i>indices[-1]:break
reader.close()
board.save(folder/'join_25.jpg',quality=95)
print('join_25.jpg written')
