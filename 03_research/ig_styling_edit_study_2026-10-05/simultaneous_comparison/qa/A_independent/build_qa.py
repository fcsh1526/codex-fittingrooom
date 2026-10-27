import json
import hashlib
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = HERE.parents[1] / 'grok_A_attempt_01' / 'source.mp4'
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
import imageio_ffmpeg

reader = imageio_ffmpeg.read_frames(str(SOURCE))
meta = next(reader)
w,h = meta['size']
fps = meta['fps']
targets = sorted(set(list(range(0,144,6)) + [143]))
crop_x = round(w*245/941)
crop_w = round(w*525/941)
boards = []
black = []
repeats = []
prev = None
n = 0
for data in reader:
    raw = np.frombuffer(data, dtype=np.uint8).reshape(h,w,3)
    sample = raw[::8,::8].astype(np.float32)
    if (sample < 16).all(axis=2).mean() > .98:
        black.append(n)
    if prev is not None and np.abs(sample-prev).mean() < .1:
        repeats.append([n-1,n])
    prev = sample
    if n in targets:
        img = Image.fromarray(raw)
        img.save(HERE / f'frame_{n:03}.png')
        crop = img.crop((crop_x,0,crop_x+crop_w,h))
        crop.save(HERE / f'crop_{n:03}.png')
        boards.append((n,img,crop))
    n += 1

for kind,dim in [('full',(180,320)),('crop',(120,320))]:
    tw,th = dim
    board = Image.new('RGB',(5*tw,5*(th+24)),'white')
    d = ImageDraw.Draw(board)
    for index,(f,img,crop) in enumerate(boards):
        item = img.copy() if kind=='full' else crop.copy()
        item.thumbnail((tw,th),Image.Resampling.LANCZOS)
        x=(index%5)*tw
        y=(index//5)*(th+24)
        d.text((x+4,y+4),f'{f/fps:.3f}s / f{f}',fill='black')
        board.paste(item,(x+(tw-item.width)//2,y+24))
    board.save(HERE / f'{kind}_25_checkpoints.jpg',quality=95)
receipt = dict(source=str(SOURCE), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(), metadata=meta,decoded_frames=n,decoded_seconds=n/fps,crop=[crop_x,0,crop_w,h],checkpoint_frames=targets,checkpoint_seconds=[f/fps for f in targets],black_candidate_frames=black,near_identical_frame_pairs=repeats,assistant_continuous_review=False,review_note='25 checkpoint extraction and full technical decode; visual review separate.')
(HERE/'extraction_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frames=n,size=[w,h],crop=receipt['crop'],checkpoints=len(boards),sha256=receipt['source_sha256'],black=black,near_identical=repeats)))
