"""Confirm fps normalization preserves source frames; extract boundary review samples."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).resolve().parent
ROOT=P.parents[6]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
def run(args):
    r=subprocess.run([str(x) for x in args],capture_output=True,check=True)
    return r.stdout
results=[]
for name in ['trial_02','L02_trial_01']:
    src=P.parent/name/'source.mp4'
    def hashes(filtered):
        args=[FF,'-v','error','-i',src,'-map','0:v:0']
        if filtered: args+=['-vf','fps=24']
        out=run(args+['-f','framemd5','-']).decode()
        return [s.split(',')[-1].strip() for s in out.splitlines() if not s.startswith('#')]
    a,b=hashes(False),hashes(True)
    assert len(a)==241 and a==b
    results.append({'source':name,'original_frames':len(a),'normalized_frames':len(b),'decoded_frame_hashes_identical':a==b})
folder=P/'boundary_qa';folder.mkdir(exist_ok=True)
groups=[('A','M03_W45_parallel_selected_review_v1.mp4',list(range(60,79,3))+list(range(120,126))),('B','M03_W45_full_frame_sequence_review_v1.mp4',list(range(223,242,3)))]
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',16)
for tag,name,frames in groups:
    expression='+'.join(f'eq(n\\,{n})' for n in frames)
    run([FF,'-v','error','-y','-i',P/name,'-vf',f'select={expression}','-fps_mode','vfr','-q:v','2',folder/(tag+'_%03d.jpg')])
    files=sorted(folder.glob(tag+'_*.jpg'))
    board=Image.new('RGB',(7*210,((len(files)+6)//7)*398),'#f5f3ec');d=ImageDraw.Draw(board)
    for j,(f,n) in enumerate(zip(files,frames)):
        im=Image.open(f);im.thumbnail((206,366));x=j%7*210;y=j//7*398
        board.paste(im,(x,y+25));d.text((x+2,y),f'{tag} f{n} {n/24:.3f}s',font=font,fill='#233b46')
    board.save(folder/(tag+'_boundary_contact.jpg'),quality=95)
(P/'native_frame_verification.json').write_text(json.dumps({'fps_normalization_checks':results,'boundary_samples':{x[0]:x[2] for x in groups},'uninterrupted_human_review':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps(results))
