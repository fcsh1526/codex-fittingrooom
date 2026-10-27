from pathlib import Path
from PIL import Image,ImageDraw
import json
base=Path(__file__).resolve().parent/'jenaby_DJnnv5OPD6k'
samples=json.loads((base/'samples.json').read_text(encoding='utf-8'))
for block in range((len(samples)+39)//40):
 rows=samples[block*40:(block+1)*40];board=Image.new('RGB',(1440,1720),'white');draw=ImageDraw.Draw(board)
 for k,row in enumerate(rows):
  im=Image.open(base/f"sample_{row['index']:03d}.png");r=row['before']['rect'];crop=im.crop((round(r['x']),round(r['y']),round(r['x']+r['width']),round(r['y']+r['height'])))
  x=k%8*180;y=k//8*344;draw.text((x+3,y+3),f"{row['index']} {row['before']['time']:.2f}-{row['after_time']:.2f}",fill='black')
  board.paste(crop.resize((180,320)),(x,y+24))
 board.save(base/f'board_{block:02d}.jpg',quality=95)
print(json.dumps({'count':len(samples),'screenshot_pixels':list(Image.open(base/'sample_000.png').size),'video_ui_rect':samples[0]['before']['rect']}))
