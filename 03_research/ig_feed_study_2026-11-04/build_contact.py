"""Build diagnostic sheets from native UI screenshots; no source-media replacement."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
for folder in HERE.iterdir():
    if not folder.is_dir() or not (folder/'native_capture.json').exists():continue
    meta=json.loads((folder/'native_capture.json').read_text(encoding='utf-8'))
    samples=sorted(meta['samples'],key=lambda s:s['t'])
    partial='Viewport' in meta.get('limits','')
    if partial:samples=samples[::2]+[samples[-1]]
    cols,cw,ch=(4,300,320) if partial else (6,225,430)
    im=Image.new('RGB',(cols*cw,((len(samples)+cols-1)//cols)*ch),'#f7f6f0');d=ImageDraw.Draw(im)
    for i,s in enumerate(samples):
        raw=Image.open(folder/s['file']).convert('RGB');r=s['rect']
        box=(max(0,round(r['x'])),max(0,round(r['y'])),min(raw.width,round(r['x']+r['width'])),min(raw.height,round(r['y']+r['height'])))
        pic=raw.crop(box);pic.thumbnail((cw-6,ch-38));x=i%cols*cw+3;y=i//cols*ch+32;im.paste(pic,(x,y));d.text((x,y-26),f"{s['t']:.2f}s",font=font,fill='#243b41')
    im.save(folder/'native_contact.png')
    print(folder.name,len(samples),meta['url'])
