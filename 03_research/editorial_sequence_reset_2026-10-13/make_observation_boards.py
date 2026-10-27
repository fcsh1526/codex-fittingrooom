from pathlib import Path
import json,math,sys
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
folder=OUT/(sys.argv[1] if len(sys.argv)>1 else 'fudge_daily')
d=json.loads((folder/'samples.json').read_text(encoding='utf-8'))
samples=sorted(d['samples'],key=lambda x:x['before'][0]['time'])
for start in range(0,len(samples),12):
 block=samples[start:start+12];board=Image.new('RGB',(960,1440),'white');draw=ImageDraw.Draw(board)
 for k,s in enumerate(block):
  before=s['before'][0];after=s['after'][0];r=before['rect'];x=k%4*240;y=k//4*480
  draw.text((x+3,y+3),f"#{s['index']:03d} {before['time']:.2f}-{after['time']:.2f}s",fill='black')
  im=Image.open(folder/s['file']).convert('RGB').crop((round(r['x']),round(r['y']),round(r['x']+r['width']),round(r['y']+r['height'])))
  board.paste(im.resize((240,427),Image.Resampling.LANCZOS),(x,y+30))
 board.save(folder/f'board_{start//12:02d}.jpg',quality=95)
print('Four browser-observation boards saved. Labels are capture brackets, not cut times.')
