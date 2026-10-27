import json, math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

folder = Path(sys.argv[1])
step = float(sys.argv[2]) if len(sys.argv) > 2 else 0.7
samples = json.loads((folder / 'samples.json').read_text(encoding='utf-8'))
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
crop = (292, 29, 626, 623)
if (folder / 'meta.json').exists():
    meta = json.loads((folder / 'meta.json').read_text(encoding='utf-8'))
    crop = tuple(meta.get('pixel_crop', crop))
cycles, group, prev = [], [], None
invalid = []
for s in samples:
    a, b = s['before'], s['after']
    t = a.get('time')
    valid = (t is not None and b.get('time') is not None and
             a.get('duration') and b.get('duration') and
             not a.get('paused') and not b.get('paused') and b['time'] >= t)
    if prev is not None and t is not None and t < prev:
        if group: cycles.append(group)
        group = []
    prev = t
    if valid: group.append(s)
    else: invalid.append(s['i'])
if group: cycles.append(group)
index = {'crop':crop, 'sample_step':step, 'invalid':invalid, 'cycles':[]}
for ci, cycle in enumerate(cycles):
    picks, last = [], -999
    for s in cycle:
        if s['before']['time'] >= last + step:
            picks.append(s)
            last = s['before']['time']
    if picks[-1] != cycle[-1]: picks.append(cycle[-1])
    cols, cw, ch = 6, 196, 383
    board = Image.new('RGB', (cols*cw, 42+math.ceil(len(picks)/cols)*ch), '#e9e8e3')
    d = ImageDraw.Draw(board)
    d.text((12,12), f'{folder.name} | capture cycle {ci+1} | timestamp brackets, not exact frames', fill='black', font=font)
    for j,s in enumerate(picks):
        x,y=(j%cols)*cw, 42+(j//cols)*ch
        im=Image.open(folder/s['file']).crop(crop).convert('RGB')
        im.thumbnail((186,332))
        board.paste(im,(x+(cw-im.width)//2,y))
        d.text((x+6,y+337),f"#{s['i']:03d} {s['before']['time']:.2f}-{s['after']['time']:.2f}s", fill='black',font=font)
    path=folder/f'cycle_{ci+1:02d}_board.jpg'
    board.save(path, quality=90)
    index['cycles'].append({'board':path.name,'samples':[s['i'] for s in cycle], 'displayed':[s['i'] for s in picks], 'start':cycle[0]['before']['time'],'end':cycle[-1]['after']['time']})
(folder/'board_index.json').write_text(json.dumps(index,indent=2),encoding='utf-8')
print(json.dumps(index,ensure_ascii=False))
