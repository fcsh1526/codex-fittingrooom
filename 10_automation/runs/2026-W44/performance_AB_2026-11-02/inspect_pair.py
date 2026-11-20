"""Use OpenMontage to sample the two original clips at shared times."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'openmontage'))
from tools.analysis.frame_sampler import FrameSampler

meta={}
for label in ['A','B']:
    path=HERE/f'{label}_source.mp4'
    if not path.exists():raise FileNotFoundError(path)
    p=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],
                     capture_output=True,text=True,check=True)
    probe=json.loads(p.stdout)
    (HERE/f'{label}_probe.json').write_text(p.stdout,encoding='utf-8')
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    duration=float(v.get('duration',probe['format']['duration']))
    timestamps=[0,2,4,6,8,min(9.9,duration-.1)]
    result=FrameSampler().execute({'input_path':str(path),'strategy':'timestamps',
        'timestamps':timestamps,'output_dir':str(HERE/f'{label}_frames'),'format':'jpg','quality':2})
    if not result.success:raise RuntimeError(result.error)
    meta[label]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'video':{k:v.get(k) for k in ['width','height','r_frame_rate','duration','nb_frames']},
        'audio_present':any(s['codec_type']=='audio' for s in probe['streams']),
        'sampling':result.data,'continuous_manual_playback':False,'user_acceptance':'pending'}
    subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True,capture_output=True)
    meta[label]['full_file_decode']='completed'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:v:0','-c:v','copy','-an',
                    str(HERE/f'{label}_silent_review.mp4')],check=True,capture_output=True)

font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
sheet=Image.new('RGB',(6*225,2*445),'#f5f4f1');draw=ImageDraw.Draw(sheet)
for row,label in enumerate(['A','B']):
    for col,f in enumerate(meta[label]['sampling']['frames']):
        im=Image.open(f['path']).convert('RGB');im.thumbnail((219,400))
        x=col*225+3;y=row*445+35;sheet.paste(im,(x,y))
        draw.text((x+3,y-29),f"{label} {f['timestamp_seconds']:.1f}s",font=font,fill='#1d292d')
sheet.save(HERE/'pair_contact_sheet.jpg',quality=92)
(HERE/'technical_review.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:{x:v[x] for x in ['video','audio_present','full_file_decode']} for k,v in meta.items()}))
