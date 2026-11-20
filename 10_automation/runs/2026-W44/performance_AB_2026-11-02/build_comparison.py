"""Native-speed diagnostic side-by-side and denser early-action frames."""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]/'openmontage'))
from tools.analysis.frame_sampler import FrameSampler

subprocess.run(['ffmpeg','-v','error','-y','-i',str(HERE/'A_source.mp4'),
 '-i',str(HERE/'B_source.mp4'),'-filter_complex','[0:v][1:v]hstack=inputs=2:shortest=1[v]',
 '-map','[v]','-c:v','libx264','-preset','fast','-crf','18','-an','-movflags','+faststart',
 str(HERE/'review_side_by_side.mp4')],capture_output=True,check=True)
probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',
 str(HERE/'review_side_by_side.mp4')],capture_output=True,text=True,check=True)
(HERE/'comparison_probe.json').write_text(probe.stdout,encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
sheet=Image.new('RGB',(11*180,2*355),'#f5f4f1');draw=ImageDraw.Draw(sheet)
for row,label in enumerate(['A','B']):
    result=FrameSampler().execute({'input_path':str(HERE/f'{label}_source.mp4'),
      'strategy':'timestamps','timestamps':[i*.5 for i in range(11)],
      'output_dir':str(HERE/f'{label}_early_dense'),'format':'jpg','quality':2})
    if not result.success:raise RuntimeError(result.error)
    (HERE/f'{label}_early_sampling.json').write_text(json.dumps(result.data,indent=2),encoding='utf-8')
    for col,f in enumerate(result.data['frames']):
        im=Image.open(f['path']).convert('RGB');im.thumbnail((176,313))
        x=col*180+2;y=row*355+31;sheet.paste(im,(x,y))
        draw.text((x+2,y-28),f"{label} {f['timestamp_seconds']:.1f}s",font=font,fill='#1d292d')
sheet.save(HERE/'early_action_contact.jpg',quality=94)
(HERE/'comparison_mapping.json').write_text(json.dumps({'left':'A','right':'B',
 'presentation':'Full original duration, native speed, no audio, no baked labels; no trims, retime or freeze.',
 'path':'review_side_by_side.mp4'},indent=2),encoding='utf-8')
v=json.loads(probe.stdout)['streams'][0]
print(json.dumps({k:v.get(k) for k in ['width','height','r_frame_rate','nb_frames','duration']}))
