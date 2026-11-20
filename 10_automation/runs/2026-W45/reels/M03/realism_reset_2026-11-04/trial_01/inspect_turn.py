"""Targeted quarter-second diagnostic crops of the actual turn, not an edited master."""
import subprocess,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').is_file());FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
frames=HERE/'turn_frames';frames.mkdir(exist_ok=True)
indices=list(range(18,103,6))
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
for f in indices:
    subprocess.run([str(FF),'-v','error','-y','-ss',str(f/24),'-i',str(HERE/'source.mp4'),'-frames:v','1',str(frames/f'f{f:03d}.png')],check=True)
def sheet(name,box,w,h):
    im=Image.new('RGB',(5*w,((len(indices)+4)//5)*h),'#f7f6f0');d=ImageDraw.Draw(im)
    for i,f in enumerate(indices):
        pic=Image.open(frames/f'f{f:03d}.png').convert('RGB').crop(box);pic.thumbnail((w-6,h-38))
        x=i%5*w+3;y=i//5*h+32;im.paste(pic,(x,y));d.text((x,y-26),f'{f/24:.2f}s / f{f}',font=font,fill='#243b41')
    im.save(HERE/(name+'.png'))
sheet('turn_face_diagnostic',(220,170,450,470),225,320)
sheet('turn_hands_bag_diagnostic',(220,420,495,880),240,430)
sheet('turn_feet_diagnostic',(220,950,450,1180),225,270)
(HERE/'turn_sampling.json').write_text(json.dumps({'fps':24,'zero_based_source_frames':indices,'source_seconds':[f/24 for f in indices],'diagnostic_crops_only':True,'master_crop':False,'does_not_certify':'Native temporal comfort, realism or zero physical errors.'},indent=2)+'\n',encoding='utf-8')
print('15turn samples .75–4.25s, diagnostic face/hands-bag/feet only; master untouched.')
