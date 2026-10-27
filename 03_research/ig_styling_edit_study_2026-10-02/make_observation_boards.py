import json
import math
from pathlib import Path
from PIL import Image, ImageDraw

folder = Path(__file__).resolve().parent / 'evidence'
pages = json.loads((folder / 'research_pages.json').read_text(encoding='utf-8'))
for account, kind, output in [
    ('chouchou_rei_rei', 'reel_playback_sampled_corrected', 'rei_spring_board.jpg'),
    ('missy_elz', 'reel_playback_sampled', 'missy_autumn_board.jpg'),
    ('missy_elz', 'reel_comparison_playback_sampled', 'missy_comparison_board.jpg'),
    ('lydiajanetomlinson', 'reel_playback_sampled_partial', 'lydia_workwear_board.jpg')
]:
    page = next(x for x in pages if x['account'] == account and x['kind'] == kind)
    samples = sorted(page['samples'], key=lambda x: x['time'])
    columns, width, height = 5, 270, 294
    board = Image.new('RGB', (columns*width, math.ceil(len(samples)/columns)*height), 'white')
    draw = ImageDraw.Draw(board)
    for i, sample in enumerate(samples):
        x, y = (i % columns)*width, (i // columns)*height
        with Image.open(sample.get('path') or folder / sample['file']) as img:
            img.thumbnail((width, height-24))
            board.paste(img, (x, y+24))
        draw.text((x+5, y+4), f"{sample['time']:.2f}s", fill='black')
    board.save(folder / output, quality=95)
    print(output)
