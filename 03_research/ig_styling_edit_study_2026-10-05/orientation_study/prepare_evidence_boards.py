"""Display live screenshot samples in capture order without pretending exact video frames."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / 'evidence' / 'lydia_jackets'
samples = json.loads((EVIDENCE / 'samples.json').read_text(encoding='utf-8'))
cycle = 0
last = None
annotated = []
for sample in samples:
    before, after = sample['before'][0], sample['after'][0]
    if last is not None and before['time'] < last:
        cycle += 1
    annotated.append(dict(sample, capture_cycle=cycle,
                          crosses_loop=after['time'] < before['time'],
                          valid_playing=not before['paused'] and not after['paused']))
    last = after['time']
for start in range(0, len(annotated), 13):
    subset = annotated[start:start + 13]
    canvas = Image.new('RGB', (4 * 220, 4 * 412), '#eeeeee')
    draw = ImageDraw.Draw(canvas)
    for offset, sample in enumerate(subset):
        frame = Image.open(EVIDENCE / sample['file']).convert('RGB')
        box = sample['before'][0]['box']
        crop = frame.crop((round(box['x']), round(box['y']),
                           round(box['x'] + box['width']), round(box['y'] + box['height'])))
        crop.thumbnail((214, 382))
        x, y = (offset % 4) * 220 + 3, (offset // 4) * 412 + 26
        canvas.paste(crop, (x, y))
        a, b = sample['before'][0]['time'], sample['after'][0]['time']
        draw.text((x, y - 22), f"#{sample['index']:02d} c{sample['capture_cycle']} {a:.2f}-{b:.2f}s", fill='black')
    canvas.save(EVIDENCE / f'board_{start // 13 + 1:02d}.jpg', quality=93)
(EVIDENCE / 'annotated_samples.json').write_text(json.dumps(annotated, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'samples': len(samples), 'boards': 4, 'capture_cycles': cycle + 1,
                  'cross_loop_samples': [s['index'] for s in annotated if s['crosses_loop']],
                  'invalid_paused_samples': [s['index'] for s in annotated if not s['valid_playing']]}, indent=2))
