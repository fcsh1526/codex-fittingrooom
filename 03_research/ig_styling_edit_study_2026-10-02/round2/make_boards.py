import json
import math
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent / 'evidence'
pages = json.loads((root / 'research_pages.json').read_text(encoding='utf-8'))
for page in pages:
    if page.get('kind') != 'playback_sampled':
        continue
    samples = sorted([s for s in page['samples'] if not s['paused']], key=lambda s: s['time'])
    count = min(15, len(samples))
    selected = [samples[round(i*(len(samples)-1)/(count-1))] for i in range(count)]
    w, h, cols = 240, 452, 5
    board = Image.new('RGB', (w*cols, h*math.ceil(count/cols)), 'white')
    draw = ImageDraw.Draw(board)
    for i, sample in enumerate(selected):
        x, y = (i % cols)*w, (i // cols)*h
        with Image.open(root / sample['file']) as screenshot:
            # Video area observed in the 1265x712 desktop screenshots;
            # untouched original screenshots remain the primary evidence.
            crop = screenshot.crop((292, 28, 626, 624))
            crop.thumbnail((w-4, h-28))
            board.paste(crop, (x+2, y+28))
        draw.text((x+6, y+6), f"{sample['time']:.2f}s", fill='black')
    output = root / (page['slug'] + '_board.jpg')
    board.save(output, quality=95)
    print(output.name)
