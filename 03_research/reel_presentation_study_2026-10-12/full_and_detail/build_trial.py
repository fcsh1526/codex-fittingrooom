from pathlib import Path
import hashlib, json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
sys.path.insert(0, str(ROOT / '10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

version = 'v2' if '--v2' in sys.argv else 'v1'
plan = json.loads((OUT / ('storyboard_v2.json' if version == 'v2' else 'storyboard.json')).read_text(encoding='utf-8'))
src = ROOT / plan['source']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(src) == plan['source_sha256']
delivery = json.loads((ROOT / '10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8'))
for reel in delivery['reels']:
    assert sha(ROOT / reel['source_path']) == reel['sha256']
for anchor in ['02_brand/reference_models/M03_start_v3_face.png', '02_brand/reference_models/M03_start_v3_full.png']:
    assert (ROOT / anchor).is_file(), anchor
dest = OUT / f'M03_full_and_detail_trial_{version}.mp4'
resume_qa = '--resume-qa' in sys.argv
assert not dest.exists() or resume_qa, 'Preserve existing versions; use --resume-qa only to inspect rendered output'
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
main = plan['main']; detail = plan['detail']
mx,my,mw,mh = main['fixed_crop_xywh']; px,py = main['destination_xy']
dx,dy,dw,dh = detail['fixed_crop_xywh']; qx,qy = detail['destination_xy']; qw,qh = detail['destination_wh']
main_scale = '' if main['scale'] == 1 else ',scale=' + ':'.join(map(str,main['destination_wh'])) + ':flags=lanczos'
graph = ('[0:v]split=2[m][d];'
         f'[m]crop={mw}:{mh}:{mx}:{my}{main_scale},pad=720:1280:{px}:{py}:color=0xeee9e1[base];'
         f'[d]crop={dw}:{dh}:{dx}:{dy},scale={qw}:{qh}:flags=lanczos[detail];'
         f'[base][detail]overlay={qx}:{qy}:shortest=1,setsar=1,format=yuv420p[v]')
if not dest.exists():
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-i',str(src),'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-crf','18','-preset','medium','-fps_mode','passthrough','-movflags','+faststart',str(dest)],check=True)
result = scan(dest)
assert result['decoded_frames'] == 270 and result['metadata']['size'] == (720,1280) and result['metadata']['fps'] == 24
assert not result['black_candidate_frames']
qa = OUT / ('qa_v2' if version == 'v2' else 'qa')
qa.mkdir(exist_ok=True)
reader = imageio_ffmpeg.read_frames(str(dest))
next(reader)
selected = sorted(set(np.linspace(0,269,25,dtype=int).tolist() + list(range(118,152)) + [48]))
frames = {}
for index, data in enumerate(reader):
    if index in selected:
        frame = Image.frombytes('RGB',(720,1280),data)
        frames[index] = frame
        frame.save(qa / f'frame_{index:03d}.png')
def board(indices,name,columns=5,width=216):
    height = width*1280//720
    rows = (len(indices)+columns-1)//columns
    image = Image.new('RGB',(width*columns,(height+24)*rows),'#ffffff')
    draw = ImageDraw.Draw(image)
    for cell,index in enumerate(indices):
        x = cell%columns*width; y = cell//columns*(height+24)
        draw.text((x+3,y+3),f'{index/24:.2f}s / f{index}',fill='black')
        image.paste(frames[index].resize((width,height),Image.Resampling.LANCZOS),(x,y+24))
    image.save(qa/name,quality=95)
board(np.linspace(0,269,25,dtype=int).tolist(),'whole_25.jpg')
board(list(range(118,152)),'join_34.jpg',columns=6,width=180)
frames[48].save(qa/'phone_review_frame.png')
for reel in delivery['reels']:
    assert sha(ROOT / reel['source_path']) == reel['sha256']
receipt = {'status':'technical_decode_complete_visual_review_pending','experiment':plan['experiment'],'output':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),'scan':result,'source_path':plan['source'],'source_sha256':plan['source_sha256'],'composition':plan,'source_action_and_speed':'unchanged','source_time_mapping':'output frame n uses original accepted film frame n in both panels','cropped_detail_not_native_proof':True,'new_generation':False,'assistant_continuous_playback':False,'user_trial_approval':None,'protected_five_films_sha256_match':True,'drive_write':False,'instagram_posted':False}
(OUT/('receipt_v2.json' if version == 'v2' else 'receipt.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(dest),'duration':result['decoded_seconds'],'frames':result['decoded_frames'],'qa':str(qa/'whole_25.jpg'),'protected_five_films_preserved':True},ensure_ascii=False))
