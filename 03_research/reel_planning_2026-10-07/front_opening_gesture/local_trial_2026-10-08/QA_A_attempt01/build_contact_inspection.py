"""Native-frame free-hand/clothing QA windows only; no video or status edits."""
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '10_automation').is_dir())
SOURCE = HERE.parent / 'A_attempt_01/source.mp4'
EXPECTED = '5baaa223b437e6fde482545cc64a0d2b8c85dffec14df6397735b71c7e0b7d49'
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
import imageio_ffmpeg

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if sha(SOURCE) != EXPECTED:
    raise ValueError('Source changed')
out = HERE / 'contact_native_30_110'
if out.exists():
    raise FileExistsError('Keep existing inspection')
out.mkdir()
reader = imageio_ffmpeg.read_frames(str(SOURCE), pix_fmt='rgb24')
meta = next(reader)
if tuple(meta['size']) != (720, 1280) or meta['fps'] != 24:
    reader.close()
    raise ValueError('Source dimensions/clock changed')
roi = (80, 350, 460, 1180)
items = []
try:
    for index, raw in enumerate(reader):
        if index > 110:
            break
        if index >= 30:
            crop = Image.frombytes('RGB', (720, 1280), raw).crop(roi)
            crop.save(out / f'window_{index:06d}.png')
            items.append((index, crop))
finally:
    reader.close()
if len(items) != 81 or sha(SOURCE) != EXPECTED:
    raise ValueError('Incomplete extraction or source mutation')
boards = []
for first in range(0, len(items), 25):
    part = items[first:first+25]
    tw, th, cols = 140, 306, 5
    rows = (len(part)+cols-1)//cols
    sheet = Image.new('RGB', (cols*tw, 34 + rows*(th+24)), '#f5f3ef')
    draw = ImageDraw.Draw(sheet)
    draw.text((4, 8), 'Native free-hand/shirt contact QA; no interpolated frames', fill='black')
    for slot, (index, im) in enumerate(part):
        x, y = slot%cols*tw, 34+slot//cols*(th+24)
        draw.text((x+3, y+3), f'f{index} / {index/24:.3f}s', fill='black')
        thumb=im.copy()
        thumb.thumbnail((tw-4, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x+(tw-thumb.width)//2, y+24))
    name=f'contact_sequence_{first//25+1:02d}.jpg'
    sheet.save(out/name, quality=96)
    boards.append(name)
receipt={'date':'2026-10-08','source':SOURCE.relative_to(ROOT).as_posix(),
         'source_sha256':EXPECTED,'source_hash_matched_before_after':True,
         'native_size':[720,1280],'fps':24,'frames_inclusive':[30,110],
         'number_of_consecutive_windows':81,'QA_crop_xyxy':list(roi),
         'boards':boards,'interpolation':False,'video_rendered':False,
         'delivery_transform':'none','continuous_playback_review':False}
(out/'inspection_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'QA_folder':str(out),'frames':81,'source_unchanged':True},ensure_ascii=False))
