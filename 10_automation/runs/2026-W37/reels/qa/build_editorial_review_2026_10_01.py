"""Extract a comparative editorial board from existing cuts; never modifies masters."""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
reels=root/'10_automation/runs/2026-W37/reels'
out=reels/'qa/editorial_review_2026-10-01'
out.mkdir(exist_ok=True)
specs=[
 ('M02',reels/'pilot_M02/videos/M02_scale_continuity_v4_review_01.mp4',[0,1.25,59/24,2.5,4.5,167/24]),
 ('M05',reels/'videos/M05_two_looks_fixed_environment_review_v2_01.mp4',[0,2,95/24,4,6,191/24]),
 ('M04',reels/'videos/M04_two_looks_review_v1_01.mp4',[0,1.875,89/24,3.75,5.75,191/24]),
 ('M01',reels/'videos/M01_two_looks_review_v1_01.mp4',[0,1.75,83/24,3.5,5.5,179/24])]
board=Image.new('RGB',(1080,4*380),'#f2f0ec')
d=ImageDraw.Draw(board)
for row,(name,source,times) in enumerate(specs):
    d.text((8,row*380+5),f'{name} | start / motion / before cut / after cut / motion / end',fill='black')
    for col,t in enumerate(times):
        dest=out/f'{name}_{col}_{t:.3f}s.png'
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1',str(dest)],check=True)
        with Image.open(dest) as im:
            im.thumbnail((180,320))
            board.paste(im,(col*180,row*380+30))
        d.text((col*180+6,row*380+355),f'{t:.3f}s',fill='black')
board.save(out/'four_reels_comparison.jpg',quality=95)
(out/'sources.json').write_text(json.dumps([dict(model=n,path=p.relative_to(root).as_posix(),times=t) for n,p,t in specs],indent=2),encoding='utf-8')
print('Four-film board extracted. This is sampled editorial evidence, not continuous playback.')
