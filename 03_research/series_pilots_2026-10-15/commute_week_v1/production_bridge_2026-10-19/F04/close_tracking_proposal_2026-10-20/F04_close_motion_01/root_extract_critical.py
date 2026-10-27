from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / '10_automation' / '.video_dependencies'))
import imageio_ffmpeg
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / 'root_critical_2026-10-21'
OUT.mkdir(exist_ok=True)
reader = imageio_ffmpeg.read_frames(str(HERE / 'F04_close_source.mp4'), pix_fmt='rgb24')
meta = next(reader)
indices = [0, 60, 84, 96, 108, 120, 144]
frames = {}
for i, frame in enumerate(reader):
    if i in indices:
        im = Image.frombytes('RGB', meta['size'], frame)
        im.save(OUT / f'f{i:03}.png')
        frames[i] = im
sheet = Image.new('RGB', (1200, 1112), 'white')
d = ImageDraw.Draw(sheet)
for n, i in enumerate(indices):
    x, y = (n % 4) * 300, (n // 4) * 556
    sheet.paste(frames[i].resize((300, 533)), (x, y))
    d.text((x + 6, y + 536), f'f{i} / {i/24:.3f}s', fill='black')
sheet.save(OUT / 'critical_sheet.jpg', quality=92)
print(str(OUT / 'critical_sheet.jpg'))
