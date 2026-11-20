"""Diagnostic frame crops only; never alter the source/master pictures."""
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5];M03=HERE.parent
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',19)
def inspect(source,times,name,box):
    frames=HERE/name;frames.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(6*220,((len(times)+5)//6)*300),'#f7f6f0');d=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        out=frames/f'{i:03d}_{t:.4f}.png'
        subprocess.run([str(FF),'-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1',str(out)],check=True)
        pic=Image.open(out).convert('RGB').crop(box);pic.thumbnail((214,263))
        x=i%6*220+3;y=i//6*300+32;sheet.paste(pic,(x,y));d.text((x,y-26),f'{t:.3f}s',font=font,fill='#243b41')
    sheet.save(HERE/f'{name}.png')
inspect(M03/'L02_trial_01/source.mp4',[i/8 for i in range(6,21)],'L02_early_expression',(242,188,430,440))
inspect(M03/'L01_trial_02/source.mp4',[i/4 for i in range(6,17)],'L01_expression',(240,180,440,450))
inspect(M03/'L02_trial_01/source.mp4',[i/4 for i in range(20,29)],'L02_ending',(185,120,560,625))
print(HERE)
