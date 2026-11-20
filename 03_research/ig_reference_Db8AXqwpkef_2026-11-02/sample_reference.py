"""Read-only reference sampling using OpenMontage's FrameSampler."""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'openmontage'))
from tools.analysis.frame_sampler import FrameSampler

probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                        '-of', 'json', str(HERE / 'reference.mp4')],
                       capture_output=True, text=True, check=True)
(HERE / 'probe.json').write_text(probe.stdout, encoding='utf-8')
timestamps = [i / 2 for i in range(15)] + [7.1]
result = FrameSampler().execute({'input_path': str(HERE / 'reference.mp4'),
    'strategy': 'timestamps', 'timestamps': timestamps,
    'output_dir': str(HERE / 'frames_0p5s'), 'format': 'jpg', 'quality': 2})
if not result.success:
    raise RuntimeError(result.error)
(HERE / 'sampling.json').write_text(json.dumps(result.data, indent=2), encoding='utf-8')
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)
sheet = Image.new('RGB', (4 * 270, 4 * 510), '#f6f6f6')
draw = ImageDraw.Draw(sheet)
for index, frame in enumerate(result.data['frames']):
    im = Image.open(frame['path']).convert('RGB')
    im.thumbnail((264, 470))
    x, y = (index % 4) * 270 + 3, (index // 4) * 510 + 36
    sheet.paste(im, (x, y))
    draw.text((x+4, y-30), f"{frame['timestamp_seconds']:.2f}s", font=font, fill='#151515')
sheet.save(HERE / 'reference_contact_sheet.jpg', quality=92)
strip = Image.new('RGB', (1080, 510), '#f6f6f6')
strip_draw = ImageDraw.Draw(strip)
for column, index in enumerate([0, 5, 10, 15]):
    frame = result.data['frames'][index]
    im = Image.open(frame['path']).convert('RGB')
    im.thumbnail((264, 470))
    x = column * 270 + 3
    strip.paste(im, (x, 36))
    strip_draw.text((x+4, 6), f"{frame['timestamp_seconds']:.2f}s", font=font, fill='#151515')
strip.save(HERE / 'reference_four_beats.jpg', quality=92)
print(json.dumps({'frames':len(result.data['frames']), 'sheet':str(HERE / 'reference_contact_sheet.jpg')}))
